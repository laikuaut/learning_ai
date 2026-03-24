# ==============================
# 正規化チェッカー
# 応用情報技術者：データベース設計
# ==============================
# 学べる内容:
#   - 関数従属性（functional dependency）の分析
#   - 第1正規形（1NF）: 繰り返し項目の排除
#   - 第2正規形（2NF）: 部分関数従属の排除
#   - 第3正規形（3NF）: 推移的関数従属の排除
#   - ボイス・コッド正規形（BCNF）
#   - 正規化の手順と分解
#   - 応用情報技術者試験のデータベース設計問題への対応力
#
# 実行方法:
#   python 01_正規化チェッカー.py
# ==============================


class FunctionalDependency:
    """関数従属性を表すクラスです

    例: {社員番号} → {名前, 部署}
    determinant（決定項）が決まれば dependent（従属項）が一意に決まります
    """

    def __init__(self, determinant, dependent):
        """
        determinant: 決定項（集合）
        dependent: 従属項（集合）
        """
        self.determinant = frozenset(determinant)
        self.dependent = frozenset(dependent)

    def __str__(self):
        det = ", ".join(sorted(self.determinant))
        dep = ", ".join(sorted(self.dependent))
        return f"{{{det}}} → {{{dep}}}"

    def __repr__(self):
        return str(self)


class Relation:
    """リレーション（テーブル）を表すクラスです"""

    def __init__(self, name, attributes, primary_key, fds=None, sample_data=None):
        """
        name: リレーション名
        attributes: 全属性の集合
        primary_key: 主キー（属性の集合）
        fds: 関数従属性のリスト
        sample_data: サンプルデータ（辞書のリスト）
        """
        self.name = name
        self.attributes = set(attributes)
        self.primary_key = frozenset(primary_key)
        self.fds = fds if fds else []
        self.sample_data = sample_data if sample_data else []

    def display(self):
        """リレーションの情報を表示します"""
        print(f"\n  ■ リレーション: {self.name}")
        print(f"    属性: {{{', '.join(sorted(self.attributes))}}}")
        pk_str = ", ".join(sorted(self.primary_key))
        print(f"    主キー: {{{pk_str}}}")
        if self.fds:
            print("    関数従属性:")
            for fd in self.fds:
                print(f"      {fd}")
        if self.sample_data:
            self._display_sample()

    def _display_sample(self):
        """サンプルデータを表示します"""
        if not self.sample_data:
            return
        cols = sorted(self.attributes)
        widths = {col: max(len(col), max(len(str(row.get(col, ""))) for row in self.sample_data))
                  for col in cols}

        header = " | ".join(f"{col:<{widths[col]}}" for col in cols)
        sep = "-+-".join("-" * widths[col] for col in cols)
        print(f"    サンプルデータ:")
        print(f"      {header}")
        print(f"      {sep}")
        for row in self.sample_data:
            line = " | ".join(f"{str(row.get(col, '')):<{widths[col]}}" for col in cols)
            print(f"      {line}")


def compute_closure(attributes, fds):
    """属性集合の閉包（closure）を計算します

    与えられた属性集合から、関数従属性を適用して導出できる
    全ての属性を求めます
    """
    closure = set(attributes)
    changed = True
    while changed:
        changed = False
        for fd in fds:
            if fd.determinant.issubset(closure) and not fd.dependent.issubset(closure):
                closure = closure.union(fd.dependent)
                changed = True
    return closure


def find_candidate_keys(all_attributes, fds):
    """候補キーを見つけます

    候補キー = 閉包が全属性集合と等しくなる最小の属性集合
    """
    from itertools import combinations

    all_attrs = set(all_attributes)
    candidate_keys = []

    # 属性数1から順に探索します
    for size in range(1, len(all_attrs) + 1):
        for combo in combinations(sorted(all_attrs), size):
            combo_set = frozenset(combo)
            # 既に見つかった候補キーのスーパーキーではないことを確認します
            is_superkey_of_candidate = False
            for ck in candidate_keys:
                if ck.issubset(combo_set):
                    is_superkey_of_candidate = True
                    break
            if is_superkey_of_candidate:
                continue

            closure = compute_closure(combo_set, fds)
            if closure == all_attrs:
                candidate_keys.append(combo_set)

        if candidate_keys and size > min(len(ck) for ck in candidate_keys):
            break

    return candidate_keys


def check_1nf(relation):
    """第1正規形（1NF）をチェックします

    条件: 全ての属性が原子値（atomic value）であること
    ※ サンプルデータがある場合、リスト値をチェックします
    """
    print("\n  === 第1正規形（1NF）チェック ===")
    print("  条件: 全ての属性値が原子値（これ以上分解できない値）であること")

    violations = []
    for i, row in enumerate(relation.sample_data):
        for col, val in row.items():
            if isinstance(val, (list, tuple)):
                violations.append((i, col, val))

    if violations:
        print("  結果: 1NF違反が見つかりました")
        for row_idx, col, val in violations:
            print(f"    行{row_idx}: {col} = {val} ← 繰り返し項目!")
        return False
    else:
        print("  結果: 1NF を満たしています")
        return True


def check_2nf(relation):
    """第2正規形（2NF）をチェックします

    条件: 1NFを満たし、全ての非キー属性が主キーに完全関数従属していること
    （部分関数従属がないこと）
    """
    print("\n  === 第2正規形（2NF）チェック ===")
    print("  条件: 非キー属性が主キーの一部に従属していないこと（部分関数従属の排除）")

    pk = relation.primary_key
    non_key = relation.attributes - pk
    violations = []

    if len(pk) <= 1:
        print("  判定: 主キーが単一属性のため、部分関数従属は発生しません")
        print("  結果: 2NF を満たしています")
        return True

    # 主キーの真部分集合で非キー属性を決定できるかチェックします
    from itertools import combinations
    for size in range(1, len(pk)):
        for subset in combinations(pk, size):
            subset_set = frozenset(subset)
            closure = compute_closure(subset_set, relation.fds)
            partial_deps = closure.intersection(non_key)
            if partial_deps:
                violations.append((subset_set, partial_deps))

    if violations:
        print("  結果: 2NF違反（部分関数従属）が見つかりました")
        for det, deps in violations:
            det_str = ", ".join(sorted(det))
            deps_str = ", ".join(sorted(deps))
            print(f"    {{{det_str}}} → {{{deps_str}}}  ← 部分関数従属!")
        return False
    else:
        print("  結果: 2NF を満たしています")
        return True


def check_3nf(relation):
    """第3正規形（3NF）をチェックします

    条件: 2NFを満たし、推移的関数従属がないこと
    """
    print("\n  === 第3正規形（3NF）チェック ===")
    print("  条件: 非キー属性が他の非キー属性に従属していないこと（推移的関数従属の排除）")

    pk = relation.primary_key
    non_key = relation.attributes - pk
    candidate_keys = find_candidate_keys(relation.attributes, relation.fds)
    all_key_attrs = set()
    for ck in candidate_keys:
        all_key_attrs.update(ck)

    violations = []
    for fd in relation.fds:
        # 決定項がスーパーキーでないかチェックします
        closure = compute_closure(fd.determinant, relation.fds)
        is_superkey = closure == relation.attributes

        if not is_superkey:
            # 従属項にキー属性でない属性が含まれているかチェックします
            non_trivial = fd.dependent - fd.determinant
            non_key_deps = non_trivial - all_key_attrs
            if non_key_deps:
                violations.append((fd, non_key_deps))

    if violations:
        print("  結果: 3NF違反（推移的関数従属）が見つかりました")
        for fd, deps in violations:
            deps_str = ", ".join(sorted(deps))
            print(f"    {fd}  ← 推移的関数従属!")
        return False
    else:
        print("  結果: 3NF を満たしています")
        return True


def check_bcnf(relation):
    """ボイス・コッド正規形（BCNF）をチェックします

    条件: 全ての非自明な関数従属性で、決定項がスーパーキーであること
    """
    print("\n  === ボイス・コッド正規形（BCNF）チェック ===")
    print("  条件: 全ての関数従属性の決定項がスーパーキーであること")

    violations = []
    for fd in relation.fds:
        # 自明な従属性（A→A）は除外します
        non_trivial = fd.dependent - fd.determinant
        if not non_trivial:
            continue

        closure = compute_closure(fd.determinant, relation.fds)
        is_superkey = closure == relation.attributes

        if not is_superkey:
            violations.append(fd)

    if violations:
        print("  結果: BCNF違反が見つかりました")
        for fd in violations:
            print(f"    {fd}  ← 決定項がスーパーキーではありません!")
        return False
    else:
        print("  結果: BCNF を満たしています")
        return True


def normalize_to_3nf(relation):
    """3NFへの正規化を実行します（分解手順を表示します）"""
    print(f"\n  ━━━ {relation.name} の正規化手順 ━━━")

    pk = relation.primary_key
    decomposed = []
    remaining_attrs = set(relation.attributes)

    # 部分関数従属の分解（2NF化）
    if len(pk) > 1:
        from itertools import combinations
        for size in range(1, len(pk)):
            for subset in combinations(pk, size):
                subset_set = frozenset(subset)
                closure = compute_closure(subset_set, relation.fds)
                partial_deps = closure.intersection(relation.attributes - pk)
                if partial_deps:
                    new_attrs = set(subset_set) | partial_deps
                    decomposed.append({
                        "name": f"{relation.name}_{len(decomposed)+1}",
                        "attrs": new_attrs,
                        "key": subset_set,
                        "reason": "部分関数従属の分解（2NF化）",
                    })
                    remaining_attrs -= partial_deps

    # 推移的関数従属の分解（3NF化）
    non_key = remaining_attrs - pk
    for fd in relation.fds:
        if fd.determinant != pk and not fd.determinant.issubset(pk):
            non_trivial = fd.dependent - fd.determinant
            if non_trivial and non_trivial.issubset(non_key):
                new_attrs = set(fd.determinant) | non_trivial
                decomposed.append({
                    "name": f"{relation.name}_{len(decomposed)+1}",
                    "attrs": new_attrs,
                    "key": fd.determinant,
                    "reason": "推移的関数従属の分解（3NF化）",
                })
                remaining_attrs -= non_trivial

    if remaining_attrs:
        decomposed.insert(0, {
            "name": f"{relation.name}_主",
            "attrs": remaining_attrs,
            "key": pk,
            "reason": "主テーブル",
        })

    # 結果の表示
    if len(decomposed) <= 1:
        print("  → 分解不要です（既に正規化されています）")
    else:
        print(f"  → {len(decomposed)} 個のリレーションに分解します:")
        for d in decomposed:
            print(f"\n    ■ {d['name']}")
            print(f"      属性: {{{', '.join(sorted(d['attrs']))}}}")
            print(f"      主キー: {{{', '.join(sorted(d['key']))}}}")
            print(f"      理由: {d['reason']}")

    return decomposed


def full_check(relation):
    """全正規形のチェックを実行します"""
    print(f"\n{'='*55}")
    print(f"  正規化レベル判定: {relation.name}")
    print(f"{'='*55}")
    relation.display()

    # 候補キーの表示
    candidate_keys = find_candidate_keys(relation.attributes, relation.fds)
    print(f"\n  候補キー:")
    for ck in candidate_keys:
        print(f"    {{{', '.join(sorted(ck))}}}")

    is_1nf = check_1nf(relation)
    if not is_1nf:
        print("\n  ★ 正規化レベル: 非正規形（1NF未満）")
        return

    is_2nf = check_2nf(relation)
    if not is_2nf:
        print("\n  ★ 正規化レベル: 第1正規形（1NF）")
        normalize_to_3nf(relation)
        return

    is_3nf = check_3nf(relation)
    if not is_3nf:
        print("\n  ★ 正規化レベル: 第2正規形（2NF）")
        normalize_to_3nf(relation)
        return

    is_bcnf = check_bcnf(relation)
    if not is_bcnf:
        print("\n  ★ 正規化レベル: 第3正規形（3NF）")
        return

    print("\n  ★ 正規化レベル: ボイス・コッド正規形（BCNF）")


# ============================================================
# 対話モード
# ============================================================

def interactive_mode():
    """対話型の正規化チェッカーです"""
    print("\n" + "=" * 55)
    print("  正規化チェッカー - 対話モード")
    print("=" * 55)
    print("  属性と関数従属性を入力して、正規化レベルを判定します。")
    print("-" * 55)

    while True:
        print("\n  操作を選択:")
        print("    1. 新しいリレーションを分析")
        print("    2. 閉包を計算")
        print("    0. 終了")
        choice = input("  選択 (0-2): ").strip()

        if choice == "0":
            print("  正規化チェッカーを終了します。")
            break

        elif choice == "1":
            name = input("  リレーション名: ").strip() or "R"
            attrs_str = input("  属性（カンマ区切り）: ").strip()
            if not attrs_str:
                print("  ※ 属性を入力してください。")
                continue

            attributes = [a.strip() for a in attrs_str.split(",")]
            pk_str = input("  主キー（カンマ区切り）: ").strip()
            primary_key = [a.strip() for a in pk_str.split(",")]

            print("  関数従属性を入力します（空行で終了）:")
            print("  形式: 決定項1,決定項2 -> 従属項1,従属項2")
            fds = []
            while True:
                fd_str = input("    FD: ").strip()
                if not fd_str:
                    break
                if "->" not in fd_str:
                    print("    ※ '→' または '->' を使って入力してください。")
                    continue
                parts = fd_str.replace("→", "->").split("->")
                det = [a.strip() for a in parts[0].split(",")]
                dep = [a.strip() for a in parts[1].split(",")]
                fds.append(FunctionalDependency(det, dep))

            relation = Relation(name, attributes, primary_key, fds)
            full_check(relation)

        elif choice == "2":
            attrs_str = input("  全属性（カンマ区切り）: ").strip()
            attributes = [a.strip() for a in attrs_str.split(",")]

            print("  関数従属性を入力（空行で終了）:")
            fds = []
            while True:
                fd_str = input("    FD: ").strip()
                if not fd_str:
                    break
                parts = fd_str.replace("→", "->").split("->")
                det = [a.strip() for a in parts[0].split(",")]
                dep = [a.strip() for a in parts[1].split(",")]
                fds.append(FunctionalDependency(det, dep))

            target_str = input("  閉包を求める属性集合（カンマ区切り）: ").strip()
            target = [a.strip() for a in target_str.split(",")]

            closure = compute_closure(frozenset(target), fds)
            print(f"  → {{{', '.join(sorted(target))}}}+ = {{{', '.join(sorted(closure))}}}")

        else:
            print("  ※ 0-2の番号を入力してください。")


# === デモンストレーション ===
print("=" * 55)
print("  正規化チェッカー")
print("  ～ テーブル設計の正規化レベルを判定しよう ～")
print("=" * 55)

# --- 例1: 1NF違反（非正規形） ---
print("\n\n━━━ 例1: 非正規形のテーブル ━━━")
r1 = Relation(
    "受注",
    ["受注番号", "顧客名", "商品"],
    ["受注番号"],
    sample_data=[
        {"受注番号": "A001", "顧客名": "田中", "商品": ["PC", "マウス"]},
        {"受注番号": "A002", "顧客名": "佐藤", "商品": ["タブレット"]},
        {"受注番号": "A003", "顧客名": "鈴木", "商品": ["PC", "キーボード", "モニター"]},
    ]
)
r1.display()
check_1nf(r1)
print("  → 「商品」列に複数の値が入っています。1行1商品に分解する必要があります。")

# --- 例2: 2NF違反 ---
print("\n\n━━━ 例2: 2NF違反（部分関数従属あり） ━━━")
r2 = Relation(
    "受注明細",
    ["受注番号", "商品番号", "顧客名", "商品名", "数量"],
    ["受注番号", "商品番号"],
    fds=[
        FunctionalDependency(["受注番号"], ["顧客名"]),
        FunctionalDependency(["商品番号"], ["商品名"]),
        FunctionalDependency(["受注番号", "商品番号"], ["数量"]),
    ],
    sample_data=[
        {"受注番号": "A001", "商品番号": "P01", "顧客名": "田中", "商品名": "PC", "数量": 2},
        {"受注番号": "A001", "商品番号": "P02", "顧客名": "田中", "商品名": "マウス", "数量": 2},
        {"受注番号": "A002", "商品番号": "P01", "顧客名": "佐藤", "商品名": "PC", "数量": 1},
    ]
)
full_check(r2)

# --- 例3: 3NF違反 ---
print("\n\n━━━ 例3: 3NF違反（推移的関数従属あり） ━━━")
r3 = Relation(
    "社員",
    ["社員番号", "名前", "部署コード", "部署名"],
    ["社員番号"],
    fds=[
        FunctionalDependency(["社員番号"], ["名前", "部署コード"]),
        FunctionalDependency(["部署コード"], ["部署名"]),
    ],
    sample_data=[
        {"社員番号": "E001", "名前": "田中", "部署コード": "D01", "部署名": "営業部"},
        {"社員番号": "E002", "名前": "佐藤", "部署コード": "D01", "部署名": "営業部"},
        {"社員番号": "E003", "名前": "鈴木", "部署コード": "D02", "部署名": "開発部"},
    ]
)
full_check(r3)

# --- 例4: BCNF満足 ---
print("\n\n━━━ 例4: BCNF を満たすテーブル ━━━")
r4 = Relation(
    "社員_正規化済",
    ["社員番号", "名前", "部署コード"],
    ["社員番号"],
    fds=[
        FunctionalDependency(["社員番号"], ["名前", "部署コード"]),
    ],
    sample_data=[
        {"社員番号": "E001", "名前": "田中", "部署コード": "D01"},
        {"社員番号": "E002", "名前": "佐藤", "部署コード": "D01"},
        {"社員番号": "E003", "名前": "鈴木", "部署コード": "D02"},
    ]
)
full_check(r4)

# --- 正規形のまとめ ---
print("\n\n━━━ 正規形のまとめ ━━━")
print("""
  ■ 正規形の段階

  非正規形    繰り返し項目あり
      ↓      （繰り返し項目を排除）
  第1正規形   全属性が原子値
      ↓      （部分関数従属を排除）
  第2正規形   非キー属性が主キー全体に完全関数従属
      ↓      （推移的関数従属を排除）
  第3正規形   非キー属性間の従属なし
      ↓      （全FDの決定項がスーパーキー）
  BCNF       最も厳密な正規形

  ■ 試験のポイント
  - 「どの正規形を満たすか？」→ 関数従属性を見て判定します
  - 「正規化の手順」→ 段階的に分解します
  - 「正規化のメリット」→ データの冗長性排除、更新異常の防止
  - 「正規化のデメリット」→ テーブル増加、JOINが増えて性能低下の可能性
""")

# --- 閉包のデモ ---
print("━━━ 閉包（Closure）の計算デモ ━━━")
demo_fds = [
    FunctionalDependency(["A"], ["B"]),
    FunctionalDependency(["B"], ["C"]),
    FunctionalDependency(["C", "D"], ["E"]),
]
print("  関数従属性:")
for fd in demo_fds:
    print(f"    {fd}")
print()

test_attrs = [["A"], ["A", "D"], ["B", "D"]]
for attrs in test_attrs:
    closure = compute_closure(frozenset(attrs), demo_fds)
    print(f"  {{{', '.join(attrs)}}}+ = {{{', '.join(sorted(closure))}}}")

# --- 対話モード ---
print()
interactive_mode()

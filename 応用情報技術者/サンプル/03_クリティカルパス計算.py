# ==============================
# クリティカルパス計算ツール
# 応用情報技術者：プロジェクトマネジメント
# ==============================
# 学べる内容:
#   - PERT（Program Evaluation and Review Technique）
#   - クリティカルパス法（CPM: Critical Path Method）
#   - 最早開始時刻（ES）と最早終了時刻（EF）
#   - 最遅開始時刻（LS）と最遅終了時刻（LF）
#   - 余裕時間（フロート / スラック）
#   - ネットワーク図の可視化
#   - 応用情報技術者試験のスケジュール管理問題への対応力
#
# 実行方法:
#   python 03_クリティカルパス計算.py
# ==============================


class Activity:
    """アクティビティ（作業）を表すクラスです"""

    def __init__(self, name, duration, predecessors=None, description=""):
        """
        name: アクティビティ名
        duration: 所要日数
        predecessors: 先行アクティビティのリスト
        description: 作業内容の説明
        """
        self.name = name
        self.duration = duration
        self.predecessors = predecessors if predecessors else []
        self.description = description

        # 前進計算（forward pass）の結果
        self.es = 0  # ES: 最早開始時刻（Earliest Start）
        self.ef = 0  # EF: 最早終了時刻（Earliest Finish）

        # 後退計算（backward pass）の結果
        self.ls = 0  # LS: 最遅開始時刻（Latest Start）
        self.lf = 0  # LF: 最遅終了時刻（Latest Finish）

        # 余裕時間
        self.total_float = 0   # トータルフロート（全余裕）
        self.free_float = 0    # フリーフロート（自由余裕）
        self.is_critical = False  # クリティカルパス上かどうか

    def __str__(self):
        predecessors_str = ", ".join(self.predecessors) if self.predecessors else "なし"
        return (f"  {self.name}: 所要{self.duration}日, "
                f"先行=[{predecessors_str}], "
                f"ES={self.es}, EF={self.ef}, "
                f"LS={self.ls}, LF={self.lf}, "
                f"TF={self.total_float}")


class CriticalPathCalculator:
    """クリティカルパス法（CPM）の計算エンジンです"""

    def __init__(self, project_name):
        self.project_name = project_name
        self.activities = {}  # name → Activity
        self.order = []  # トポロジカル順序

    def add_activity(self, name, duration, predecessors=None, description=""):
        """アクティビティを追加します"""
        activity = Activity(name, duration, predecessors, description)
        self.activities[name] = activity

    def _topological_sort(self):
        """トポロジカルソートを実行します（依存関係順に並べます）"""
        in_degree = {name: 0 for name in self.activities}
        for act in self.activities.values():
            for pred in act.predecessors:
                if pred in self.activities:
                    in_degree[act.name] = in_degree.get(act.name, 0) + 1

        # 入次数0のノードをキューに追加します
        queue = [name for name, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            queue.sort()  # 安定した順序のためソートします
            node = queue.pop(0)
            result.append(node)

            for act in self.activities.values():
                if node in act.predecessors:
                    in_degree[act.name] -= 1
                    if in_degree[act.name] == 0:
                        queue.append(act.name)

        self.order = result
        return result

    def calculate(self):
        """クリティカルパスを計算します"""
        if not self.activities:
            print("  ※ アクティビティがありません。")
            return

        self._topological_sort()

        # === 前進計算（Forward Pass） ===
        print("\n  ■ ステップ1: 前進計算（Forward Pass）")
        print("    最早開始時刻(ES)と最早終了時刻(EF)を求めます")
        print("    計算式: EF = ES + 所要日数")
        print()

        for name in self.order:
            act = self.activities[name]
            if not act.predecessors:
                act.es = 0
            else:
                # 先行アクティビティの最大EFがESになります
                max_ef = 0
                for pred_name in act.predecessors:
                    if pred_name in self.activities:
                        pred = self.activities[pred_name]
                        max_ef = max(max_ef, pred.ef)
                act.es = max_ef

            act.ef = act.es + act.duration
            predecessors_str = ", ".join(act.predecessors) if act.predecessors else "なし"
            print(f"    {act.name}: ES={act.es}, EF={act.es}+{act.duration}={act.ef}"
                  f"  (先行: {predecessors_str})")

        # プロジェクト完了時刻
        project_end = max(act.ef for act in self.activities.values())
        print(f"\n    → プロジェクト最短完了日数: {project_end}日")

        # === 後退計算（Backward Pass） ===
        print(f"\n  ■ ステップ2: 後退計算（Backward Pass）")
        print("    最遅終了時刻(LF)と最遅開始時刻(LS)を求めます")
        print("    計算式: LS = LF - 所要日数")
        print()

        # 最終アクティビティのLFを設定します
        for act in self.activities.values():
            act.lf = project_end

        # 逆順で後退計算します
        for name in reversed(self.order):
            act = self.activities[name]

            # 後続アクティビティがあれば、その最小LSがLFになります
            successors = [a for a in self.activities.values()
                         if name in a.predecessors]
            if successors:
                act.lf = min(s.ls for s in successors)

            act.ls = act.lf - act.duration
            print(f"    {act.name}: LF={act.lf}, LS={act.lf}-{act.duration}={act.ls}")

        # === 余裕時間（Float）の計算 ===
        print(f"\n  ■ ステップ3: 余裕時間（フロート）の計算")
        print("    トータルフロート(TF) = LS - ES = LF - EF")
        print("    TF=0 のアクティビティがクリティカルパス上にあります")
        print()

        for name in self.order:
            act = self.activities[name]
            act.total_float = act.ls - act.es

            # フリーフロートの計算
            successors = [a for a in self.activities.values()
                         if name in a.predecessors]
            if successors:
                min_es = min(s.es for s in successors)
                act.free_float = min_es - act.ef
            else:
                act.free_float = project_end - act.ef

            act.is_critical = (act.total_float == 0)
            critical_mark = " ★ クリティカル!" if act.is_critical else ""
            print(f"    {act.name}: TF={act.total_float}, FF={act.free_float}{critical_mark}")

        return project_end

    def get_critical_path(self):
        """クリティカルパスを取得します"""
        critical = [name for name in self.order
                    if self.activities[name].is_critical]
        return critical

    def display_summary(self):
        """計算結果のサマリーを表示します"""
        project_end = max(act.ef for act in self.activities.values())
        critical_path = self.get_critical_path()

        print(f"\n  {'='*60}")
        print(f"  プロジェクト: {self.project_name}")
        print(f"  {'='*60}")

        # アクティビティ一覧表
        print(f"\n  ■ アクティビティ一覧")
        print(f"    {'名前':<6} {'日数':>4} {'ES':>4} {'EF':>4} "
              f"{'LS':>4} {'LF':>4} {'TF':>4} {'FF':>4} {'CP':>4}")
        print("    " + "-" * 52)

        for name in self.order:
            act = self.activities[name]
            cp = "★" if act.is_critical else ""
            print(f"    {act.name:<6} {act.duration:>4} {act.es:>4} {act.ef:>4} "
                  f"{act.ls:>4} {act.lf:>4} {act.total_float:>4} {act.free_float:>4} {cp:>4}")

        # クリティカルパス
        path_str = " → ".join(critical_path)
        path_duration = sum(self.activities[n].duration for n in critical_path)
        print(f"\n  ■ クリティカルパス")
        print(f"    {path_str}")
        print(f"    合計日数: {project_end}日")

        # ネットワーク図（簡易表示）
        self._display_network()

        # ガントチャート風表示
        self._display_gantt(project_end)

    def _display_network(self):
        """ネットワーク図を簡易表示します"""
        print(f"\n  ■ ネットワーク図（簡易表示）")

        # レベル分け（同じESの作業をグループ化します）
        levels = {}
        for name in self.order:
            act = self.activities[name]
            es = act.es
            if es not in levels:
                levels[es] = []
            levels[es].append(name)

        for es in sorted(levels.keys()):
            acts = levels[es]
            for name in acts:
                act = self.activities[name]
                mark = "★" if act.is_critical else " "
                succ = [a.name for a in self.activities.values()
                        if name in a.predecessors]
                succ_str = " → ".join(succ) if succ else "(完了)"
                print(f"    {mark} [{act.name}]({act.duration}日) → {succ_str}")

    def _display_gantt(self, project_end):
        """ガントチャート風の表示をします"""
        print(f"\n  ■ ガントチャート")

        # ヘッダー（日数目盛り）
        scale = max(1, project_end // 40 + 1)
        display_width = project_end // scale + 1

        header_nums = ""
        for i in range(0, project_end + 1, 5):
            pos = i // scale
            header_nums += f"{i:<5}"
        print(f"    {'':>8} {header_nums}")

        for name in self.order:
            act = self.activities[name]
            start = act.es // scale
            end = act.ef // scale
            float_end = (act.es + act.duration + act.total_float) // scale

            bar = "." * start
            bar += "#" * (end - start)
            if act.total_float > 0:
                bar += "~" * (float_end - end)

            mark = "★" if act.is_critical else " "
            print(f"    {mark}{act.name:>6}: {bar}")

        print(f"    {'':>8} # = 作業期間, ~ = 余裕時間")


def pert_estimate(optimistic, most_likely, pessimistic):
    """PERT三点見積もりを計算します

    期待値 = (楽観値 + 4×最可能値 + 悲観値) / 6
    標準偏差 = (悲観値 - 楽観値) / 6
    """
    expected = (optimistic + 4 * most_likely + pessimistic) / 6
    std_dev = (pessimistic - optimistic) / 6
    variance = std_dev ** 2

    print(f"    楽観値(O)={optimistic}, 最可能値(M)={most_likely}, 悲観値(P)={pessimistic}")
    print(f"    期待値 = ({optimistic} + 4×{most_likely} + {pessimistic}) / 6 = {expected:.1f}")
    print(f"    標準偏差 = ({pessimistic} - {optimistic}) / 6 = {std_dev:.2f}")
    print(f"    分散 = {std_dev:.2f}^2 = {variance:.2f}")

    return expected, std_dev, variance


# ============================================================
# 対話モード
# ============================================================

def interactive_mode():
    """対話型のクリティカルパス計算ツールです"""
    print("\n" + "=" * 55)
    print("  クリティカルパス計算 - 対話モード")
    print("=" * 55)
    print("  操作を選んでください:")
    print("    1. 新しいプロジェクトを分析")
    print("    2. PERT三点見積もり")
    print("    0. 終了")
    print("-" * 55)

    while True:
        choice = input("\n  選択 (0-2): ").strip()

        if choice == "0":
            print("  クリティカルパス計算を終了します。")
            break

        elif choice == "1":
            name = input("  プロジェクト名: ").strip() or "プロジェクト"
            calc = CriticalPathCalculator(name)

            print("  アクティビティを入力します（空行で終了）:")
            print("  形式: 名前 所要日数 先行作業1,先行作業2")
            print("  例: B 5 A")
            print("  例: A 3")

            while True:
                line = input("    > ").strip()
                if not line:
                    break
                parts = line.split()
                if len(parts) < 2:
                    print("    ※ 名前と所要日数を入力してください。")
                    continue
                try:
                    act_name = parts[0]
                    duration = int(parts[1])
                    predecessors = parts[2].split(",") if len(parts) > 2 else []
                    calc.add_activity(act_name, duration, predecessors)
                    print(f"    → {act_name} (所要{duration}日) を追加しました")
                except ValueError:
                    print("    ※ 所要日数は整数で入力してください。")

            if calc.activities:
                calc.calculate()
                calc.display_summary()

        elif choice == "2":
            try:
                print("  PERT三点見積もり")
                o = float(input("  楽観値（日数）: "))
                m = float(input("  最可能値（日数）: "))
                p = float(input("  悲観値（日数）: "))
                pert_estimate(o, m, p)
            except ValueError:
                print("  ※ 数値を入力してください。")

        else:
            print("  ※ 0-2の番号を入力してください。")


# === デモンストレーション ===
print("=" * 55)
print("  クリティカルパス計算ツール")
print("  ～ プロジェクトの最短完了日数を求めよう ～")
print("=" * 55)

# --- デモ1: 基本的なクリティカルパス計算 ---
print("\n━━━ デモ1: システム開発プロジェクト ━━━")
print("""
  プロジェクトの作業一覧:
    A: 要件定義      3日  先行: なし
    B: 基本設計      5日  先行: A
    C: DB設計        4日  先行: A
    D: 詳細設計      6日  先行: B
    E: プログラミング 8日  先行: C, D
    F: テスト        4日  先行: E
    G: ドキュメント   3日  先行: B
""")

calc1 = CriticalPathCalculator("システム開発")
calc1.add_activity("A", 3, [], "要件定義")
calc1.add_activity("B", 5, ["A"], "基本設計")
calc1.add_activity("C", 4, ["A"], "DB設計")
calc1.add_activity("D", 6, ["B"], "詳細設計")
calc1.add_activity("E", 8, ["C", "D"], "プログラミング")
calc1.add_activity("F", 4, ["E"], "テスト")
calc1.add_activity("G", 3, ["B"], "ドキュメント作成")

calc1.calculate()
calc1.display_summary()

# --- デモ2: より大きなプロジェクト ---
print("\n\n━━━ デモ2: Webサイト構築プロジェクト ━━━")

calc2 = CriticalPathCalculator("Webサイト構築")
calc2.add_activity("A", 2, [], "企画・要件整理")
calc2.add_activity("B", 3, ["A"], "デザイン策定")
calc2.add_activity("C", 4, ["A"], "サーバー準備")
calc2.add_activity("D", 5, ["B"], "フロントエンド開発")
calc2.add_activity("E", 6, ["B", "C"], "バックエンド開発")
calc2.add_activity("F", 2, ["D"], "UI テスト")
calc2.add_activity("G", 3, ["E"], "API テスト")
calc2.add_activity("H", 2, ["F", "G"], "結合テスト")
calc2.add_activity("I", 1, ["H"], "リリース")

calc2.calculate()
calc2.display_summary()

# --- デモ3: PERT三点見積もり ---
print("\n\n━━━ デモ3: PERT三点見積もり ━━━")
print("  作業日数が不確実な場合、3つの見積もりから期待値を求めます")
print("  計算式: 期待値 = (O + 4M + P) / 6")
print()

pert_tasks = [
    ("要件定義", 2, 3, 7),
    ("設計", 3, 5, 10),
    ("開発", 5, 8, 15),
    ("テスト", 2, 4, 8),
]

total_expected = 0
total_variance = 0
for task_name, o, m, p in pert_tasks:
    print(f"\n  ■ {task_name}")
    expected, std_dev, variance = pert_estimate(o, m, p)
    total_expected += expected
    total_variance += variance

total_std = total_variance ** 0.5
print(f"\n  ■ プロジェクト全体の見積もり")
print(f"    合計期待値: {total_expected:.1f}日")
print(f"    合計分散: {total_variance:.2f}")
print(f"    合計標準偏差: {total_std:.2f}日")
print(f"    68%信頼区間: {total_expected - total_std:.1f}日 ～ {total_expected + total_std:.1f}日")
print(f"    95%信頼区間: {total_expected - 2*total_std:.1f}日 ～ {total_expected + 2*total_std:.1f}日")

# --- 試験ポイント ---
print("""

━━━ 試験頻出ポイント ━━━

  ■ 用語の整理
    ES (Earliest Start)   = 最早開始時刻（これより早く始められない）
    EF (Earliest Finish)  = 最早終了時刻 = ES + 所要日数
    LS (Latest Start)     = 最遅開始時刻（これまでに始めないと遅延）
    LF (Latest Finish)    = 最遅終了時刻（これまでに終わらないと遅延）
    TF (Total Float)      = 全余裕 = LS - ES = LF - EF

  ■ クリティカルパスの特徴
    - TF = 0 のアクティビティを結んだ最長経路です
    - プロジェクトの最短完了日数を決めます
    - クリティカルパス上の作業が遅れると全体が遅れます
    - 複数のクリティカルパスが存在する場合もあります

  ■ 計算手順
    1. 前進計算 → ES, EF を求めます（先頭から末尾へ）
    2. 後退計算 → LS, LF を求めます（末尾から先頭へ）
    3. TF = LS - ES で余裕を計算します
    4. TF = 0 の経路がクリティカルパスです

  ■ PERT三点見積もり
    期待値 = (O + 4M + P) / 6
    標準偏差 = (P - O) / 6
""")

# --- 対話モード ---
interactive_mode()

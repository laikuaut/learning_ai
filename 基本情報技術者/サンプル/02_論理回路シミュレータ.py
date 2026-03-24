# ==============================
# 論理回路シミュレータ
# 基本情報技術者：論理回路・ブール代数
# ==============================
# 学べる内容:
#   - 基本論理ゲート（AND, OR, NOT, XOR, NAND, NOR）
#   - 真理値表（truth table）の生成
#   - 半加算器（half adder）と全加算器（full adder）
#   - 複合回路の構成
#   - ド・モルガンの法則（De Morgan's laws）
#   - 基本情報技術者試験の論理回路問題への対応力
#
# 実行方法:
#   python 02_論理回路シミュレータ.py
# ==============================


# === 基本論理ゲート ===

def gate_and(a, b):
    """AND ゲート: 両方1のとき1を返します"""
    return a & b


def gate_or(a, b):
    """OR ゲート: どちらか1のとき1を返します"""
    return a | b


def gate_not(a):
    """NOT ゲート: 入力を反転します"""
    return 1 - a


def gate_xor(a, b):
    """XOR ゲート: 異なるとき1を返します"""
    return a ^ b


def gate_nand(a, b):
    """NAND ゲート: AND の否定です"""
    return gate_not(gate_and(a, b))


def gate_nor(a, b):
    """NOR ゲート: OR の否定です"""
    return gate_not(gate_or(a, b))


def gate_xnor(a, b):
    """XNOR ゲート: XOR の否定です（一致回路）"""
    return gate_not(gate_xor(a, b))


# === 真理値表の生成 ===

def print_truth_table_2input(gate_name, gate_func):
    """2入力ゲートの真理値表を表示します"""
    print(f"\n  ■ {gate_name} ゲートの真理値表")
    print(f"    {'A':>3} {'B':>3} │ {'出力':>4}")
    print(f"    {'─'*3} {'─'*3} ┼ {'─'*4}")
    for a in (0, 1):
        for b in (0, 1):
            result = gate_func(a, b)
            print(f"    {a:>3} {b:>3} │ {result:>4}")


def print_truth_table_1input(gate_name, gate_func):
    """1入力ゲートの真理値表を表示します"""
    print(f"\n  ■ {gate_name} ゲートの真理値表")
    print(f"    {'A':>3} │ {'出力':>4}")
    print(f"    {'─'*3} ┼ {'─'*4}")
    for a in (0, 1):
        result = gate_func(a)
        print(f"    {a:>3} │ {result:>4}")


# === 回路図表示 ===

def show_gate_symbols():
    """論理ゲートの回路記号をアスキーアートで表示します"""
    print("\n  ■ 論理ゲートの回路記号")

    print("""
    AND ゲート          OR ゲート           NOT ゲート
    A ──┐               A ──┐               A ──┐
        ├──┤── 出力         ├──)── 出力         ├>o── 出力
    B ──┘               B ──┘

    NAND ゲート         NOR ゲート          XOR ゲート
    A ──┐               A ──┐               A ──┐
        ├──┤o── 出力        ├──)o── 出力        ├──)=── 出力
    B ──┘               B ──┘               B ──┘
    """)


# === 半加算器と全加算器 ===

def half_adder(a, b):
    """半加算器（half adder）: 1ビットの加算を行います
    桁上がり（carry）と合計（sum）を返します"""
    s = gate_xor(a, b)   # 合計: XOR
    c = gate_and(a, b)   # 桁上がり: AND
    return s, c


def full_adder(a, b, cin):
    """全加算器（full adder）: 桁上がり入力付きの1ビット加算です
    半加算器2つとOR1つで構成されます"""
    # 第1半加算器: A と B を加算します
    s1, c1 = half_adder(a, b)
    # 第2半加算器: 第1の合計と桁上がり入力を加算します
    s2, c2 = half_adder(s1, cin)
    # 最終的な桁上がり: 2つの桁上がりの OR です
    cout = gate_or(c1, c2)
    return s2, cout


def multi_bit_adder(a_bits, b_bits):
    """複数ビットの加算器です（全加算器を連結します）"""
    n = len(a_bits)
    result = []
    carry = 0

    # 下位ビットから加算します
    for i in range(n - 1, -1, -1):
        s, carry = full_adder(a_bits[i], b_bits[i], carry)
        result.insert(0, s)

    return result, carry


# === ド・モルガンの法則 ===

def demonstrate_de_morgan():
    """ド・モルガンの法則を実際に検証します"""
    print("\n━━━ ド・モルガンの法則の検証 ━━━")
    print("  法則1: NOT(A AND B) = (NOT A) OR (NOT B)")
    print("  法則2: NOT(A OR B) = (NOT A) AND (NOT B)")

    print(f"\n  ■ 法則1の検証: ¬(A ∧ B) = (¬A) ∨ (¬B)")
    print(f"    {'A':>3} {'B':>3} │ {'¬(A∧B)':>7} {'(¬A)∨(¬B)':>10} │ {'一致?':>5}")
    print(f"    {'─'*3} {'─'*3} ┼ {'─'*7} {'─'*10} ┼ {'─'*5}")
    for a in (0, 1):
        for b in (0, 1):
            left = gate_not(gate_and(a, b))
            right = gate_or(gate_not(a), gate_not(b))
            match = "✓" if left == right else "✗"
            print(f"    {a:>3} {b:>3} │ {left:>7} {right:>10} │ {match:>5}")

    print(f"\n  ■ 法則2の検証: ¬(A ∨ B) = (¬A) ∧ (¬B)")
    print(f"    {'A':>3} {'B':>3} │ {'¬(A∨B)':>7} {'(¬A)∧(¬B)':>10} │ {'一致?':>5}")
    print(f"    {'─'*3} {'─'*3} ┼ {'─'*7} {'─'*10} ┼ {'─'*5}")
    for a in (0, 1):
        for b in (0, 1):
            left = gate_not(gate_or(a, b))
            right = gate_and(gate_not(a), gate_not(b))
            match = "✓" if left == right else "✗"
            print(f"    {a:>3} {b:>3} │ {left:>7} {right:>10} │ {match:>5}")

    print("\n  → すべて一致！ ド・モルガンの法則が成り立つことを確認できました。")


# === 対話モード ===

def interactive_mode():
    """対話型の論理回路シミュレータです"""
    print("\n" + "=" * 55)
    print("  論理回路シミュレータ - 対話モード")
    print("=" * 55)
    print("  操作を選んでください:")
    print("    1. 論理ゲートをテスト")
    print("    2. 半加算器をテスト")
    print("    3. 全加算器をテスト")
    print("    4. 複数ビット加算")
    print("    5. 論理式を評価")
    print("    0. 終了")
    print("-" * 55)

    while True:
        choice = input("\n  選択 (0-5): ").strip()

        if choice == "0":
            print("  論理回路シミュレータを終了します。")
            break

        elif choice == "1":
            print("  ゲートを選択: AND / OR / NOT / XOR / NAND / NOR")
            gate = input("  ゲート名: ").strip().upper()

            gates_2input = {
                "AND": gate_and, "OR": gate_or, "XOR": gate_xor,
                "NAND": gate_nand, "NOR": gate_nor, "XNOR": gate_xnor,
            }
            gates_1input = {"NOT": gate_not}

            if gate in gates_2input:
                try:
                    a = int(input("  入力A (0 or 1): "))
                    b = int(input("  入力B (0 or 1): "))
                    if a in (0, 1) and b in (0, 1):
                        result = gates_2input[gate](a, b)
                        print(f"  → {gate}({a}, {b}) = {result}")
                    else:
                        print("  ※ 0 または 1 を入力してください。")
                except ValueError:
                    print("  ※ 正しい値を入力してください。")
            elif gate in gates_1input:
                try:
                    a = int(input("  入力A (0 or 1): "))
                    if a in (0, 1):
                        result = gates_1input[gate](a)
                        print(f"  → {gate}({a}) = {result}")
                    else:
                        print("  ※ 0 または 1 を入力してください。")
                except ValueError:
                    print("  ※ 正しい値を入力してください。")
            else:
                print("  ※ 無効なゲート名です。")

        elif choice == "2":
            try:
                a = int(input("  入力A (0 or 1): "))
                b = int(input("  入力B (0 or 1): "))
                if a in (0, 1) and b in (0, 1):
                    s, c = half_adder(a, b)
                    print(f"\n  半加算器の結果:")
                    print(f"    入力:   A={a}, B={b}")
                    print(f"    合計S:  {s}  (XOR)")
                    print(f"    桁上C:  {c}  (AND)")
                else:
                    print("  ※ 0 または 1 を入力してください。")
            except ValueError:
                print("  ※ 正しい値を入力してください。")

        elif choice == "3":
            try:
                a = int(input("  入力A (0 or 1): "))
                b = int(input("  入力B (0 or 1): "))
                cin = int(input("  桁上がり入力Cin (0 or 1): "))
                if all(v in (0, 1) for v in (a, b, cin)):
                    s, cout = full_adder(a, b, cin)
                    print(f"\n  全加算器の結果:")
                    print(f"    入力:     A={a}, B={b}, Cin={cin}")
                    print(f"    合計S:    {s}")
                    print(f"    桁上Cout: {cout}")
                    print(f"    検算:     {a}+{b}+{cin} = {a+b+cin} → S={s}, C={cout} ({cout*2+s})")
                else:
                    print("  ※ 0 または 1 を入力してください。")
            except ValueError:
                print("  ※ 正しい値を入力してください。")

        elif choice == "4":
            try:
                a_str = input("  2進数A (例: 1010): ").strip()
                b_str = input("  2進数B (例: 0110): ").strip()

                if not all(c in "01" for c in a_str) or not all(c in "01" for c in b_str):
                    print("  ※ 0と1のみで入力してください。")
                    continue

                # ビット数を揃えます
                max_len = max(len(a_str), len(b_str))
                a_str = a_str.zfill(max_len)
                b_str = b_str.zfill(max_len)

                a_bits = [int(c) for c in a_str]
                b_bits = [int(c) for c in b_str]

                result_bits, carry = multi_bit_adder(a_bits, b_bits)
                result_str = "".join(str(b) for b in result_bits)

                # 10進数での検算
                a_dec = int(a_str, 2)
                b_dec = int(b_str, 2)
                r_dec = int(result_str, 2) + carry * (2 ** max_len)

                print(f"\n  複数ビット加算の結果:")
                print(f"    {'':>8} {a_str}  ({a_dec})")
                print(f"    +  {'':>{max_len - len(b_str)}}{b_str}  ({b_dec})")
                print(f"    {'─' * (max_len + 3)}")
                if carry:
                    print(f"    = {carry}{result_str}  ({r_dec})")
                else:
                    print(f"      {result_str}  ({r_dec})")
            except ValueError:
                print("  ※ 正しい値を入力してください。")

        elif choice == "5":
            print("  論理式の例: A AND B, A OR (NOT B), (A XOR B) AND C")
            print("  ※ 簡易パーサーです。A, B, C の3変数に対応しています。")
            try:
                a = int(input("  A (0 or 1): "))
                b = int(input("  B (0 or 1): "))
                c = int(input("  C (0 or 1) [不要なら0]: "))
                expr = input("  論理式: ").strip().upper()

                # 簡易的な論理式評価
                # 変数を値に置換します
                eval_expr = expr.replace("A", str(a)).replace("B", str(b)).replace("C", str(c))
                eval_expr = eval_expr.replace("AND", "&").replace("OR", "|")
                eval_expr = eval_expr.replace("XOR", "^").replace("NOT ", "1-")
                eval_expr = eval_expr.replace("NAND", "nand").replace("NOR", "nor")

                try:
                    # 安全な評価（数値と演算子のみ）
                    allowed = set("0123456789&|^()-+ ")
                    if all(c in allowed for c in eval_expr):
                        result = eval(eval_expr) & 1  # 1ビットに制限します
                        print(f"  → {expr} (A={a}, B={b}, C={c}) = {result}")
                    else:
                        print("  ※ 対応していない演算子が含まれています。")
                except Exception:
                    print("  ※ 論理式の評価に失敗しました。")
            except ValueError:
                print("  ※ 正しい値を入力してください。")

        else:
            print("  ※ 0-5の番号を入力してください。")


# === デモンストレーション ===
print("=" * 55)
print("  論理回路シミュレータ")
print("  ～ デジタル回路の世界を体験しよう ～")
print("=" * 55)

# --- 1. ゲートの回路記号 ---
show_gate_symbols()

# --- 2. 全ゲートの真理値表 ---
print("━━━ 1. 基本論理ゲートの真理値表 ━━━")

gates_2input = [
    ("AND",  gate_and),
    ("OR",   gate_or),
    ("XOR",  gate_xor),
    ("NAND", gate_nand),
    ("NOR",  gate_nor),
    ("XNOR", gate_xnor),
]

print_truth_table_1input("NOT", gate_not)
for name, func in gates_2input:
    print_truth_table_2input(name, func)

# --- 3. 半加算器 ---
print("\n\n━━━ 2. 半加算器（Half Adder） ━━━")
print("  構成: XOR ゲート(合計) + AND ゲート(桁上がり)")
print("""
    A ──┬──[XOR]──── S（合計）
        │
    B ──┼──[AND]──── C（桁上がり）
  """)
print(f"    {'A':>3} {'B':>3} │ {'S(合計)':>7} {'C(桁上)':>7}")
print(f"    {'─'*3} {'─'*3} ┼ {'─'*7} {'─'*7}")
for a in (0, 1):
    for b in (0, 1):
        s, c = half_adder(a, b)
        print(f"    {a:>3} {b:>3} │ {s:>7} {c:>7}")

# --- 4. 全加算器 ---
print("\n\n━━━ 3. 全加算器（Full Adder） ━━━")
print("  構成: 半加算器2つ + OR ゲート1つ")
print("""
    A ──┐                    ┌──[OR]── Cout
    B ──┤─[半加算器1]─ C1 ──┤
        └── S1 ──┐          │
                 ├─[半加算器2]─ C2
    Cin ─────────┘
                 └── S（合計）
  """)
print(f"    {'A':>3} {'B':>3} {'Cin':>4} │ {'S(合計)':>7} {'Cout':>5}")
print(f"    {'─'*3} {'─'*3} {'─'*4} ┼ {'─'*7} {'─'*5}")
for a in (0, 1):
    for b in (0, 1):
        for cin in (0, 1):
            s, cout = full_adder(a, b, cin)
            print(f"    {a:>3} {b:>3} {cin:>4} │ {s:>7} {cout:>5}")

# --- 5. 複数ビット加算器のデモ ---
print("\n\n━━━ 4. 4ビット加算器のデモ ━━━")
test_pairs = [
    ([0, 1, 0, 1], [0, 0, 1, 1]),  # 5 + 3
    ([1, 0, 1, 0], [0, 1, 1, 0]),  # 10 + 6
    ([1, 1, 1, 1], [0, 0, 0, 1]),  # 15 + 1（オーバーフロー）
]

for a_bits, b_bits in test_pairs:
    a_str = "".join(str(b) for b in a_bits)
    b_str = "".join(str(b) for b in b_bits)
    a_dec = int(a_str, 2)
    b_dec = int(b_str, 2)

    result_bits, carry = multi_bit_adder(a_bits, b_bits)
    r_str = "".join(str(b) for b in result_bits)
    r_dec = int(r_str, 2) + carry * 16

    print(f"\n    {a_str} ({a_dec:>2})")
    print(f"  + {b_str} ({b_dec:>2})")
    print(f"  ─────────")
    if carry:
        print(f"  {carry} {r_str} ({r_dec:>2})  ※ オーバーフロー!")
    else:
        print(f"    {r_str} ({r_dec:>2})")

# --- 6. ド・モルガンの法則 ---
print()
demonstrate_de_morgan()

# --- 対話モード ---
print()
interactive_mode()

# ==============================
# 基数変換ツール
# 基本情報技術者：数値表現
# ==============================
# 学べる内容:
#   - 2進数（binary）、8進数（octal）、10進数（decimal）、16進数（hexadecimal）の相互変換
#   - 2の補数（two's complement）の計算
#   - ビット演算の基礎
#   - 小数の2進数変換
#   - 基本情報技術者試験の数値表現問題への対応力
#
# 実行方法:
#   python 01_基数変換ツール.py
# ==============================


def decimal_to_binary(n, bits=8):
    """10進数を2進数に変換します（正の整数）"""
    if n == 0:
        return "0" * bits
    result = ""
    temp = n
    while temp > 0:
        result = str(temp % 2) + result
        temp //= 2
    return result.zfill(bits)


def decimal_to_octal(n):
    """10進数を8進数に変換します"""
    if n == 0:
        return "0"
    result = ""
    temp = n
    while temp > 0:
        result = str(temp % 8) + result
        temp //= 8
    return result


def decimal_to_hex(n):
    """10進数を16進数に変換します"""
    hex_chars = "0123456789ABCDEF"
    if n == 0:
        return "0"
    result = ""
    temp = n
    while temp > 0:
        result = hex_chars[temp % 16] + result
        temp //= 16
    return result


def binary_to_decimal(binary_str):
    """2進数（文字列）を10進数に変換します"""
    result = 0
    for i, bit in enumerate(reversed(binary_str)):
        if bit == "1":
            result += 2 ** i
    return result


def show_conversion_process(decimal_val, base, base_name):
    """変換の計算過程を表示します"""
    print(f"\n  【{decimal_val} を {base_name} に変換する過程】")
    temp = decimal_val
    remainders = []
    step = 1
    while temp > 0:
        quotient = temp // base
        remainder = temp % base
        if base == 16:
            hex_chars = "0123456789ABCDEF"
            remainder_str = hex_chars[remainder]
        else:
            remainder_str = str(remainder)
        print(f"    ステップ{step}: {temp} ÷ {base} = {quotient} ... 余り {remainder_str}")
        remainders.append(remainder_str)
        temp = quotient
        step += 1
    result = "".join(reversed(remainders))
    print(f"    → 余りを下から読むと: {result}")
    return result


def twos_complement(n, bits=8):
    """2の補数を計算します（負の数の表現）"""
    if n >= 0:
        return decimal_to_binary(n, bits)

    # 正の数の2進数を求めます
    positive_binary = decimal_to_binary(abs(n), bits)
    print(f"\n  【2の補数の計算過程】")
    print(f"    元の数:     {abs(n)} (10進数)")
    print(f"    2進数:      {positive_binary}")

    # ステップ1: ビット反転（1の補数）
    inverted = ""
    for bit in positive_binary:
        inverted += "0" if bit == "1" else "1"
    print(f"    ビット反転:  {inverted}  ← 1の補数（one's complement）")

    # ステップ2: 1を加算
    carry = 1
    result = list(inverted)
    for i in range(len(result) - 1, -1, -1):
        if result[i] == "1" and carry == 1:
            result[i] = "0"
        elif result[i] == "0" and carry == 1:
            result[i] = "1"
            carry = 0
            break
    result_str = "".join(result)
    print(f"    +1:          {result_str}  ← 2の補数（two's complement）")
    return result_str


def twos_complement_to_decimal(binary_str):
    """2の補数表現の2進数を10進数に変換します"""
    bits = len(binary_str)
    if binary_str[0] == "1":
        # 負の数：2の補数を逆変換します
        # ビット反転して+1すると元の正の数になります
        inverted = ""
        for bit in binary_str:
            inverted += "0" if bit == "1" else "1"
        positive_val = binary_to_decimal(inverted) + 1
        return -positive_val
    else:
        return binary_to_decimal(binary_str)


def decimal_fraction_to_binary(fraction, max_digits=10):
    """小数部分を2進数に変換します"""
    print(f"\n  【小数 0.{str(fraction).split('.')[-1] if '.' in str(fraction) else fraction} を2進数に変換する過程】")
    result = "0."
    temp = fraction if isinstance(fraction, float) else float(f"0.{fraction}")
    # 整数部分を除去します
    temp = temp - int(temp)
    step = 1
    seen = set()
    for _ in range(max_digits):
        if temp == 0:
            break
        if temp in seen:
            result += "..."
            print(f"    → 循環小数が検出されました")
            break
        seen.add(temp)
        temp *= 2
        bit = int(temp)
        result += str(bit)
        print(f"    ステップ{step}: {temp:.6f} の整数部 = {bit}, 小数部 = {temp - bit:.6f}")
        temp -= bit
        step += 1
    print(f"    → 結果: {result}")
    return result


def interactive_conversion():
    """対話型の基数変換ツールです"""
    print("\n" + "=" * 55)
    print("  基数変換ツール - 対話モード")
    print("=" * 55)
    print("  変換元の基数を選んでください:")
    print("    1. 10進数 → 2進数 / 8進数 / 16進数")
    print("    2. 2進数 → 10進数")
    print("    3. 8進数 → 10進数")
    print("    4. 16進数 → 10進数")
    print("    5. 2の補数計算")
    print("    6. 小数の2進数変換")
    print("    0. 終了")
    print("-" * 55)

    while True:
        choice = input("\n  選択 (0-6): ").strip()

        if choice == "0":
            print("  基数変換ツールを終了します。")
            break

        elif choice == "1":
            try:
                val = int(input("  10進数の値を入力: "))
                if val < 0:
                    print("  ※ 正の整数を入力してください（負の数は選択肢5へ）")
                    continue
                print(f"\n  === {val} (10進数) の変換結果 ===")

                # 2進数
                show_conversion_process(val, 2, "2進数")
                bin_result = decimal_to_binary(val, max(8, val.bit_length()))
                print(f"    2進数:  {bin_result}")

                # 8進数
                show_conversion_process(val, 8, "8進数")
                oct_result = decimal_to_octal(val)
                print(f"    8進数:  {oct_result}")

                # 16進数
                show_conversion_process(val, 16, "16進数")
                hex_result = decimal_to_hex(val)
                print(f"    16進数: {hex_result}")

                # Python組み込み関数での検算
                print(f"\n  【Python組み込み関数での検算】")
                print(f"    bin({val}) = {bin(val)}")
                print(f"    oct({val}) = {oct(val)}")
                print(f"    hex({val}) = {hex(val)}")
            except ValueError:
                print("  ※ 正しい整数を入力してください。")

        elif choice == "2":
            binary = input("  2進数を入力 (例: 11010110): ").strip()
            if all(c in "01" for c in binary) and binary:
                result = binary_to_decimal(binary)
                print(f"\n  === 変換過程 ===")
                for i, bit in enumerate(binary):
                    pos = len(binary) - 1 - i
                    if bit == "1":
                        print(f"    位置{pos}: {bit} × 2^{pos} = {2**pos}")
                print(f"    → {binary} (2進数) = {result} (10進数)")
            else:
                print("  ※ 0と1のみで入力してください。")

        elif choice == "3":
            octal = input("  8進数を入力 (例: 327): ").strip()
            if all(c in "01234567" for c in octal) and octal:
                result = 0
                print(f"\n  === 変換過程 ===")
                for i, digit in enumerate(octal):
                    pos = len(octal) - 1 - i
                    val = int(digit) * (8 ** pos)
                    result += val
                    print(f"    位置{pos}: {digit} × 8^{pos} = {val}")
                print(f"    → {octal} (8進数) = {result} (10進数)")
            else:
                print("  ※ 0-7の数字のみで入力してください。")

        elif choice == "4":
            hex_str = input("  16進数を入力 (例: 1A3F): ").strip().upper()
            valid_hex = all(c in "0123456789ABCDEF" for c in hex_str) and hex_str
            if valid_hex:
                result = 0
                print(f"\n  === 変換過程 ===")
                for i, digit in enumerate(hex_str):
                    pos = len(hex_str) - 1 - i
                    val = int(digit, 16) * (16 ** pos)
                    result += val
                    print(f"    位置{pos}: {digit} × 16^{pos} = {val}")
                print(f"    → {hex_str} (16進数) = {result} (10進数)")
            else:
                print("  ※ 0-9, A-Fの文字のみで入力してください。")

        elif choice == "5":
            try:
                val = int(input("  整数を入力（負の数OK）: "))
                bits = int(input("  ビット数 (8/16/32) [デフォルト:8]: ").strip() or "8")
                if bits not in (8, 16, 32):
                    bits = 8
                    print("  ※ 8ビットで計算します。")

                # 表現可能範囲をチェックします
                min_val = -(2 ** (bits - 1))
                max_val = 2 ** (bits - 1) - 1
                if val < min_val or val > max_val:
                    print(f"  ※ {bits}ビットで表現可能な範囲は {min_val} ～ {max_val} です。")
                    continue

                result = twos_complement(val, bits)
                print(f"\n  === 結果 ===")
                print(f"    {val} (10進数) の{bits}ビット2の補数表現: {result}")

                # 検算
                back = twos_complement_to_decimal(result)
                print(f"    逆変換による検算: {result} → {back} (10進数)")
            except ValueError:
                print("  ※ 正しい整数を入力してください。")

        elif choice == "6":
            try:
                val = float(input("  小数を入力 (例: 0.625): "))
                if val < 0 or val >= 1:
                    print("  ※ 0以上1未満の小数を入力してください。")
                    continue
                decimal_fraction_to_binary(val)
            except ValueError:
                print("  ※ 正しい小数を入力してください。")

        else:
            print("  ※ 0-6の番号を入力してください。")


# === デモンストレーション ===
print("=" * 55)
print("  基数変換ツール")
print("  ～ 2進/8進/10進/16進の世界を体験しよう ～")
print("=" * 55)

# --- 1. 基本的な基数変換 ---
print("\n━━━ 1. 基本的な基数変換 ━━━")
demo_values = [42, 100, 255]
for val in demo_values:
    print(f"\n  ■ {val} (10進数)")
    print(f"    2進数:  {decimal_to_binary(val)}")
    print(f"    8進数:  {decimal_to_octal(val)}")
    print(f"    16進数: {decimal_to_hex(val)}")

# --- 2. 変換の計算過程 ---
print("\n\n━━━ 2. 変換の計算過程（試験で頻出！） ━━━")
show_conversion_process(156, 2, "2進数")
show_conversion_process(156, 16, "16進数")

# --- 3. 2の補数 ---
print("\n\n━━━ 3. 2の補数（負の数の表現） ━━━")
print("\n  ■ 8ビットでの2の補数表現")
test_values = [5, -5, 127, -128, 0]
for val in test_values:
    result = twos_complement(val, 8)
    back = twos_complement_to_decimal(result)
    print(f"    {val:>4} → {result}  (検算: {back})")

# --- 4. 2の補数の加算 ---
print("\n\n━━━ 4. 2の補数の加算（コンピュータの引き算） ━━━")
a, b = 25, -10
a_bin = twos_complement(a, 8)
b_bin = twos_complement(b, 8)
print(f"\n  {a} + ({b}) を2の補数で計算します:")
print(f"    {a:>4} → {a_bin}")
print(f"    {b:>4} → {b_bin}")

# 加算のシミュレーション
carry = 0
result_bits = []
for i in range(7, -1, -1):
    bit_sum = int(a_bin[i]) + int(b_bin[i]) + carry
    result_bits.insert(0, str(bit_sum % 2))
    carry = bit_sum // 2
result_str = "".join(result_bits)
result_val = twos_complement_to_decimal(result_str)
print(f"    加算結果: {result_str}")
print(f"    10進数:   {result_val}")
print(f"    検算:     {a} + ({b}) = {a + b} ✓" if result_val == a + b else f"    ※ オーバーフロー")

# --- 5. 小数の2進数変換 ---
print("\n\n━━━ 5. 小数の2進数変換 ━━━")
print("  ■ 0.625 を2進数に変換（試験頻出パターン）")
decimal_fraction_to_binary(0.625)
print("\n  ■ 0.1 を2進数に変換（循環小数になる例）")
decimal_fraction_to_binary(0.1, 8)

# --- 6. 基数間の対応表 ---
print("\n\n━━━ 6. 基数間の対応表 ━━━")
print(f"  {'10進':>5} {'2進':>9} {'8進':>5} {'16進':>4}")
print("  " + "-" * 28)
for i in range(16):
    print(f"  {i:>5} {decimal_to_binary(i, 4):>9} {decimal_to_octal(i):>5} {decimal_to_hex(i):>4}")

# --- 対話モード ---
print("\n")
interactive_conversion()

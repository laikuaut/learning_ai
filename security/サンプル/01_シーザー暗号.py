# ==============================
# シーザー暗号（Caesar Cipher）
# 情報セキュリティ基礎：古典暗号の仕組みを体験するサンプル
# ==============================
# 学べる内容:
#   - 暗号化と復号の基本概念
#   - シーザー暗号（シフト暗号）のアルゴリズム
#   - ブルートフォース（総当たり）攻撃の仕組み
#   - 暗号の強度と鍵空間の概念
#   - 文字コード（ord / chr）の操作
#
# 実行方法:
#   python 01_シーザー暗号.py
#
# ※ 本プログラムは教育目的で作成されています
# ※ シーザー暗号は現代では安全な暗号ではありません
# ==============================


def explain_caesar_cipher():
    """シーザー暗号の仕組みをアスキーアートで解説します"""
    print("""
  ┌──────────────────────────────────────────────────┐
  │              シーザー暗号とは？                    │
  └──────────────────────────────────────────────────┘

  古代ローマの将軍ユリウス・カエサル（シーザー）が使った暗号です。
  アルファベットを一定の文字数だけ「ずらす」ことで暗号化します。

  【鍵（シフト数）= 3 の場合】

  平文:   A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
          ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
  暗号文: D E F G H I J K L M N O P Q R S T U V W X Y Z A B C
                                                      ↑ 末尾で先頭に戻る

  例: HELLO → KHOOR（各文字を3つ後ろにずらす）

  【暗号化の流れ】
  平文（plaintext）  + 鍵（key） → 暗号文（ciphertext）
  暗号文（ciphertext）+ 鍵（key） → 平文（plaintext）

  【弱点】
  - 鍵空間がたった25通り（シフト数 1〜25）
  - ブルートフォース攻撃で簡単に解読可能
  - 文字の出現頻度が保存される（頻度分析に弱い）
    """)


def encrypt_caesar(plaintext, shift):
    """シーザー暗号で暗号化します

    Args:
        plaintext: 平文
        shift: シフト数（鍵）

    Returns:
        暗号文
    """
    result = []

    for char in plaintext:
        if char.isalpha():
            # 大文字・小文字を判定
            if char.isupper():
                # A=65 を基準にシフト
                shifted = (ord(char) - ord('A') + shift) % 26 + ord('A')
            else:
                # a=97 を基準にシフト
                shifted = (ord(char) - ord('a') + shift) % 26 + ord('a')
            result.append(chr(shifted))
        else:
            # アルファベット以外はそのまま
            result.append(char)

    return "".join(result)


def decrypt_caesar(ciphertext, shift):
    """シーザー暗号を復号します

    復号は「逆方向にシフト」するのと同じです。
    つまり、encrypt_caesar に (26 - shift) を渡すのと同じ結果になります。
    """
    return encrypt_caesar(ciphertext, -shift)


def encrypt_japanese(plaintext, shift):
    """日本語のひらがなもシーザー暗号風にシフトします（おまけ）"""
    # ひらがな: U+3041 (ぁ) 〜 U+3093 (ん) = 83文字
    HIRAGANA_START = 0x3041
    HIRAGANA_END = 0x3093
    HIRAGANA_COUNT = HIRAGANA_END - HIRAGANA_START + 1

    result = []
    for char in plaintext:
        code = ord(char)
        if HIRAGANA_START <= code <= HIRAGANA_END:
            shifted = (code - HIRAGANA_START + shift) % HIRAGANA_COUNT + HIRAGANA_START
            result.append(chr(shifted))
        elif char.isalpha():
            # アルファベットは通常のシーザー暗号
            if char.isupper():
                shifted = (ord(char) - ord('A') + shift) % 26 + ord('A')
            else:
                shifted = (ord(char) - ord('a') + shift) % 26 + ord('a')
            result.append(chr(shifted))
        else:
            result.append(char)

    return "".join(result)


def brute_force_attack(ciphertext):
    """ブルートフォース（総当たり）攻撃を実行します"""
    print("\n" + "=" * 55)
    print("  ブルートフォース攻撃（総当たり攻撃）")
    print("=" * 55)
    print(f"\n  暗号文: {ciphertext}")
    print(f"\n  全25通りのシフト数を試します:\n")
    print(f"  {'シフト':<8} {'復号結果'}")
    print(f"  {'─' * 8} {'─' * 40}")

    results = []
    for shift in range(1, 26):
        decrypted = decrypt_caesar(ciphertext, shift)
        results.append((shift, decrypted))
        print(f"  shift={shift:<3} {decrypted}")

    print(f"\n  ※ 25通りすべてを試すだけで解読できてしまいます。")
    print(f"     これがシーザー暗号の弱点です。")

    return results


def show_shift_table(shift):
    """シフト対応表を表示します"""
    print(f"\n  シフト数 = {shift} の対応表:")
    print(f"  平文:   ", end="")
    for i in range(26):
        print(f"{chr(65 + i)} ", end="")
    print()
    print(f"  暗号文: ", end="")
    for i in range(26):
        shifted = (i + shift) % 26
        print(f"{chr(65 + shifted)} ", end="")
    print()


def frequency_analysis(text):
    """文字の出現頻度を分析します"""
    # アルファベットのみカウント
    freq = {}
    total = 0
    for char in text.upper():
        if char.isalpha():
            freq[char] = freq.get(char, 0) + 1
            total += 1

    if total == 0:
        print("  ※ アルファベットが含まれていません。")
        return

    print(f"\n  文字頻度分析（全{total}文字）:")
    print(f"  {'文字':<4} {'回数':<6} {'割合':<8} {'バー'}")
    print(f"  {'─' * 4} {'─' * 6} {'─' * 8} {'─' * 30}")

    # 頻度順にソート
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    for char, count in sorted_freq:
        percentage = count / total * 100
        bar = "█" * int(percentage / 2)
        print(f"  {char:<4} {count:<6} {percentage:>5.1f}%  {bar}")

    # 英語での最頻出文字は E（約12.7%）
    print(f"\n  ※ 英語では E が最も多く出現します（約12.7%）。")
    if sorted_freq:
        most_common = sorted_freq[0][0]
        likely_shift = (ord(most_common) - ord('E')) % 26
        print(f"     最頻出文字 '{most_common}' から推測すると、")
        print(f"     シフト数は {likely_shift} の可能性があります。")


def demo_mode():
    """デモモード: シーザー暗号の暗号化・復号・攻撃を実演します"""
    print("\n" + "=" * 55)
    print("  【デモモード】シーザー暗号の実演")
    print("=" * 55)

    # 基本的な暗号化
    plaintext = "HELLO WORLD"
    shift = 3

    print(f"\n  ◆ 基本的な暗号化")
    show_shift_table(shift)
    encrypted = encrypt_caesar(plaintext, shift)
    print(f"\n  平文:    {plaintext}")
    print(f"  鍵:      シフト数 = {shift}")
    print(f"  暗号文:  {encrypted}")

    # 復号
    decrypted = decrypt_caesar(encrypted, shift)
    print(f"\n  ◆ 復号")
    print(f"  暗号文:  {encrypted}")
    print(f"  鍵:      シフト数 = {shift}")
    print(f"  平文:    {decrypted}")

    # 長い文章の例
    print(f"\n  ◆ 文章の暗号化例")
    message = "The quick brown fox jumps over the lazy dog"
    shift2 = 13
    encrypted2 = encrypt_caesar(message, shift2)
    print(f"  平文:    {message}")
    print(f"  鍵:      シフト数 = {shift2}（ROT13）")
    print(f"  暗号文:  {encrypted2}")
    print(f"  ※ ROT13は2回適用すると元に戻る特殊なシフト数です")
    print(f"  再適用:  {encrypt_caesar(encrypted2, shift2)}")

    # ブルートフォース攻撃
    print(f"\n  ◆ ブルートフォース攻撃の実演")
    brute_force_attack("KHOOR ZRUOG")

    # 頻度分析
    print(f"\n  ◆ 頻度分析")
    long_cipher = encrypt_caesar(
        "To be or not to be that is the question "
        "Whether tis nobler in the mind to suffer",
        7
    )
    print(f"  暗号文: {long_cipher}")
    frequency_analysis(long_cipher)


def interactive_mode():
    """対話モード: ユーザーが自分で暗号化・復号を体験します"""
    print("\n" + "=" * 55)
    print("  【対話モード】シーザー暗号体験")
    print("=" * 55)

    while True:
        print("\n  操作を選んでください:")
        print("  1. 暗号化する")
        print("  2. 復号する")
        print("  3. ブルートフォース攻撃を試す")
        print("  4. 頻度分析を行う")
        print("  5. シフト対応表を表示")
        print("  6. 日本語（ひらがな）暗号化（おまけ）")
        print("  7. メニューに戻る")

        choice = input("\n  選択 (1-7): ").strip()

        if choice == "1":
            text = input("  暗号化する文章を入力: ")
            try:
                shift = int(input("  シフト数を入力 (1-25): ").strip())
                if not 1 <= shift <= 25:
                    print("  ※ 1〜25 の整数を入力してください。")
                    continue
                show_shift_table(shift)
                result = encrypt_caesar(text, shift)
                print(f"\n  平文:   {text}")
                print(f"  暗号文: {result}")
            except ValueError:
                print("  ※ 有効な数値を入力してください。")

        elif choice == "2":
            text = input("  復号する暗号文を入力: ")
            try:
                shift = int(input("  シフト数を入力 (1-25): ").strip())
                if not 1 <= shift <= 25:
                    print("  ※ 1〜25 の整数を入力してください。")
                    continue
                result = decrypt_caesar(text, shift)
                print(f"\n  暗号文: {text}")
                print(f"  平文:   {result}")
            except ValueError:
                print("  ※ 有効な数値を入力してください。")

        elif choice == "3":
            text = input("  解読したい暗号文を入力: ")
            brute_force_attack(text)

        elif choice == "4":
            text = input("  分析する文章（暗号文）を入力: ")
            frequency_analysis(text)

        elif choice == "5":
            try:
                shift = int(input("  シフト数を入力 (1-25): ").strip())
                if 1 <= shift <= 25:
                    show_shift_table(shift)
                else:
                    print("  ※ 1〜25 の整数を入力してください。")
            except ValueError:
                print("  ※ 有効な数値を入力してください。")

        elif choice == "6":
            text = input("  暗号化するひらがなを入力: ")
            try:
                shift = int(input("  シフト数を入力 (1-82): ").strip())
                encrypted = encrypt_japanese(text, shift)
                print(f"\n  平文:   {text}")
                print(f"  暗号文: {encrypted}")
                decrypted = encrypt_japanese(encrypted, -shift)
                print(f"  復号:   {decrypted}")
            except ValueError:
                print("  ※ 有効な数値を入力してください。")

        elif choice == "7":
            break
        else:
            print("  ※ 1〜7 の数字を入力してください。")


# --- メインプログラム ---
if __name__ == "__main__":
    print("+" + "=" * 53 + "+")
    print("|        シーザー暗号体験ツール                      |")
    print("|        〜 古典暗号の世界へようこそ 〜              |")
    print("+" + "=" * 53 + "+")

    # シーザー暗号の解説
    explain_caesar_cipher()

    while True:
        print("\n  モードを選択してください:")
        print("  1. デモモード（暗号化・復号・攻撃を実演）")
        print("  2. 対話モード（自分で体験）")
        print("  3. 終了")

        mode = input("\n  選択 (1-3): ").strip()

        if mode == "1":
            demo_mode()
        elif mode == "2":
            interactive_mode()
        elif mode == "3":
            print("\n  ご利用ありがとうございました！")
            break
        else:
            print("  ※ 1〜3 の数字を入力してください。")

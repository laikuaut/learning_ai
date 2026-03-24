# ==============================
# 共通鍵暗号シミュレータ（XOR暗号）
# 情報セキュリティ基礎：共通鍵暗号の仕組みを体験するサンプル
# ==============================
# 学べる内容:
#   - 共通鍵暗号（対称鍵暗号）の基本概念
#   - XOR（排他的論理和）演算の性質
#   - XOR暗号による暗号化・復号の仕組み
#   - 鍵の長さとセキュリティの関係
#   - ワンタイムパッド（完全秘匿暗号）の概念
#   - 共通鍵暗号と公開鍵暗号の違い
#
# 実行方法:
#   python 04_共通鍵暗号シミュレータ.py
#
# ※ 本プログラムは教育目的で作成されています
# ※ XOR暗号単体は現代の実用には不十分です
# ==============================

import os
import binascii


def explain_symmetric_encryption():
    """共通鍵暗号の仕組みをアスキーアートで解説します"""
    print("""
  ┌──────────────────────────────────────────────────┐
  │            共通鍵暗号（対称鍵暗号）とは？          │
  └──────────────────────────────────────────────────┘

  暗号化と復号に「同じ鍵」を使う方式です。

  【暗号化の流れ】
                      共通鍵（同じ鍵）
                         ┌───┐
    平文 ───→ 暗号化 ──→│鍵 │──→ 暗号文 ──→ 復号 ──→ 平文
    "Hello"   (ロック)   └───┘   "xK#2a"   (解錠)    "Hello"
                         ┌───┐
                         │鍵 │（同じ鍵を使用）
                         └───┘

  【XOR（排他的論理和）の性質】
  XOR は「2つのビットが異なるとき 1、同じとき 0」になる演算です。

  ┌───┬───┬───────┐
  │ A │ B │ A XOR B │
  ├───┼───┼───────┤
  │ 0 │ 0 │   0     │
  │ 0 │ 1 │   1     │
  │ 1 │ 0 │   1     │
  │ 1 │ 1 │   0     │
  └───┴───┴───────┘

  【XOR暗号の魔法】
  データ XOR 鍵 = 暗号文
  暗号文 XOR 鍵 = データ  ← 同じ鍵でXORすると元に戻る！

  【代表的な共通鍵暗号アルゴリズム】
  ┌──────┬──────────┬──────────────────────────┐
  │ DES  │ 56bit鍵  │ 古い。現在は非推奨        │
  │ 3DES │ 168bit鍵 │ DESを3回適用。まだ使用される│
  │ AES  │ 128/256bit│ 現在の標準。最も推奨       │
  └──────┴──────────┴──────────────────────────┘

  【共通鍵暗号 vs 公開鍵暗号】
  ┌────────────┬────────────────┬────────────────┐
  │            │ 共通鍵暗号      │ 公開鍵暗号      │
  ├────────────┼────────────────┼────────────────┤
  │ 鍵の数     │ 1つ（共通）     │ 2つ（公開/秘密）│
  │ 速度       │ 高速            │ 低速            │
  │ 鍵配送問題 │ あり            │ なし            │
  │ 用途       │ データ暗号化    │ 鍵交換、認証    │
  │ 代表例     │ AES             │ RSA, ECDSA     │
  └────────────┴────────────────┴────────────────┘
    """)


def xor_encrypt(data_bytes, key_bytes):
    """XOR暗号で暗号化します

    データの各バイトを鍵の対応するバイトとXOR演算します。
    鍵がデータより短い場合は繰り返し使います。
    """
    result = bytearray()
    key_length = len(key_bytes)

    for i, byte in enumerate(data_bytes):
        # 鍵を繰り返し使用
        key_byte = key_bytes[i % key_length]
        result.append(byte ^ key_byte)

    return bytes(result)


def xor_decrypt(cipher_bytes, key_bytes):
    """XOR暗号を復号します

    XOR の性質上、暗号化と復号は同じ操作です。
    cipher XOR key = plaintext（暗号化と全く同じ関数）
    """
    return xor_encrypt(cipher_bytes, key_bytes)


def visualize_xor_process(text, key_text):
    """XOR暗号化の過程をビットレベルで視覚化します"""
    data_bytes = text.encode("utf-8")
    key_bytes = key_text.encode("utf-8")

    # 表示する文字数を制限
    display_len = min(len(data_bytes), 6)

    print(f"\n  平文:  \"{text}\"")
    print(f"  鍵:    \"{key_text}\"")
    print()

    print(f"  【XOR演算の過程（先頭{display_len}バイト）】")
    print(f"  {'バイト':>6} {'文字':>4} {'2進数':>12} {'16進数':>6}")
    print(f"  {'─' * 6} {'─' * 4} {'─' * 12} {'─' * 6}")

    cipher_bytes = bytearray()

    for i in range(display_len):
        d = data_bytes[i]
        k = key_bytes[i % len(key_bytes)]
        c = d ^ k

        d_char = chr(d) if 32 <= d < 127 else "."
        k_char = chr(k) if 32 <= k < 127 else "."
        c_char = chr(c) if 32 <= c < 127 else "."

        print(f"  平文  : '{d_char}'  {format(d, '08b')}   0x{d:02X}")
        print(f"  鍵    : '{k_char}'  {format(k, '08b')}   0x{k:02X}")
        print(f"  ────── XOR ──────────────")
        print(f"  暗号文: '{c_char}'  {format(c, '08b')}   0x{c:02X}")
        print()

        cipher_bytes.append(c)

    # 全体の暗号化結果
    full_cipher = xor_encrypt(data_bytes, key_bytes)
    cipher_hex = binascii.hexlify(full_cipher).decode()

    print(f"  【暗号化結果（全体）】")
    print(f"  16進数: {cipher_hex}")
    print(f"  バイト数: {len(full_cipher)}")

    # 復号の確認
    decrypted = xor_decrypt(full_cipher, key_bytes)
    print(f"\n  【復号結果】")
    print(f"  復号文: \"{decrypted.decode('utf-8')}\"")
    print(f"  ※ 同じ鍵でXORすると元のデータに戻ります")


def demonstrate_key_reuse_weakness():
    """鍵の再利用の危険性を実演します"""
    print("\n" + "=" * 55)
    print("  鍵の再利用の危険性")
    print("=" * 55)
    print("""
  同じ鍵で異なるメッセージを暗号化すると、
  鍵を知らなくても情報が漏洩する可能性があります。

  暗号文1 XOR 暗号文2 = 平文1 XOR 平文2
  （鍵が打ち消し合ってしまう！）
    """)

    key = b"SECRET"
    msg1 = "HELLO!"
    msg2 = "ATTACK"

    cipher1 = xor_encrypt(msg1.encode(), key)
    cipher2 = xor_encrypt(msg2.encode(), key)

    # 2つの暗号文をXOR
    xored = bytes(a ^ b for a, b in zip(cipher1, cipher2))
    # 平文同士のXOR
    plain_xored = bytes(a ^ b for a, b in zip(msg1.encode(), msg2.encode()))

    print(f"  メッセージ1: \"{msg1}\"")
    print(f"  メッセージ2: \"{msg2}\"")
    print(f"  共通鍵:      \"{key.decode()}\"")
    print(f"\n  暗号文1: {binascii.hexlify(cipher1).decode()}")
    print(f"  暗号文2: {binascii.hexlify(cipher2).decode()}")
    print(f"\n  暗号文1 XOR 暗号文2: {binascii.hexlify(xored).decode()}")
    print(f"  平文1  XOR 平文2:   {binascii.hexlify(plain_xored).decode()}")
    print(f"\n  → 結果が一致！鍵なしで平文同士の関係がわかってしまいます。")
    print(f"     これが「鍵の再利用は危険」と言われる理由です。")


def demonstrate_one_time_pad():
    """ワンタイムパッド（完全秘匿暗号）を実演します"""
    print("\n" + "=" * 55)
    print("  ワンタイムパッド（One-Time Pad）")
    print("=" * 55)
    print("""
  XOR暗号でも、以下の条件を満たせば「理論上解読不可能」になります:
  1. 鍵の長さがデータと同じかそれ以上
  2. 鍵が完全にランダム
  3. 鍵を一度しか使わない（ワンタイム）
    """)

    message = "TOP SECRET MESSAGE"
    msg_bytes = message.encode("utf-8")

    # メッセージと同じ長さのランダムな鍵を生成
    key = os.urandom(len(msg_bytes))

    cipher = xor_encrypt(msg_bytes, key)
    decrypted = xor_decrypt(cipher, key)

    print(f"  平文:       \"{message}\"")
    print(f"  鍵（ランダム）: {binascii.hexlify(key).decode()}")
    print(f"  鍵の長さ:   {len(key)}バイト（平文と同じ長さ）")
    print(f"  暗号文:     {binascii.hexlify(cipher).decode()}")
    print(f"  復号結果:   \"{decrypted.decode('utf-8')}\"")

    print(f"\n  ※ この暗号文から鍵なしで元のメッセージを推測することは")
    print(f"     数学的に不可能です（情報理論的に安全）。")
    print(f"     ただし、鍵の安全な配送と管理が実用上の大きな課題です。")


def demonstrate_key_length_importance():
    """鍵の長さの重要性を実演します"""
    print("\n" + "=" * 55)
    print("  鍵の長さとセキュリティ")
    print("=" * 55)

    message = "This is a secret message for demonstration purposes."
    msg_bytes = message.encode("utf-8")

    keys = [
        ("A", "1文字（8ビット）- 非常に弱い"),
        ("AB", "2文字（16ビット）- 弱い"),
        ("ABCDEFGH", "8文字（64ビット）- やや弱い"),
        ("ABCDEFGHIJKLMNOP", "16文字（128ビット）- AES相当"),
    ]

    print(f"\n  平文: \"{message}\"")
    print(f"  平文の長さ: {len(msg_bytes)}バイト\n")

    for key_str, description in keys:
        key_bytes = key_str.encode("utf-8")
        cipher = xor_encrypt(msg_bytes, key_bytes)
        cipher_hex = binascii.hexlify(cipher).decode()

        print(f"  鍵: \"{key_str}\" ({description})")
        print(f"  暗号文: {cipher_hex[:60]}...")

        # 繰り返しパターンの検出
        key_len = len(key_bytes)
        if len(msg_bytes) > key_len * 2:
            # 鍵の長さごとにパターンが繰り返されるか確認
            pattern_found = True
            for i in range(key_len, min(key_len * 2, len(cipher))):
                # 同じ平文バイトに対応する暗号文が一致するか
                pass
            print(f"  ※ 鍵が短いと暗号文にパターンが現れやすくなります")
        print()

    print(f"  ポイント: 鍵は最低でも128ビット（16バイト）以上が推奨です。")
    print(f"  AES暗号では128/192/256ビットの鍵長が使われます。")


def demo_mode():
    """デモモード: 共通鍵暗号の各機能を実演します"""
    print("\n" + "=" * 55)
    print("  【デモモード】共通鍵暗号シミュレーション")
    print("=" * 55)

    # XOR暗号化の視覚化
    print("\n  ◆ XOR暗号化の過程")
    visualize_xor_process("Hello!", "KEY")

    # 鍵の再利用の危険性
    print("\n  ◆ 鍵の再利用の危険性")
    demonstrate_key_reuse_weakness()

    # ワンタイムパッド
    print("\n  ◆ ワンタイムパッド")
    demonstrate_one_time_pad()

    # 鍵の長さの重要性
    print("\n  ◆ 鍵の長さの重要性")
    demonstrate_key_length_importance()


def interactive_mode():
    """対話モード: ユーザーが自分で暗号化・復号を体験します"""
    print("\n" + "=" * 55)
    print("  【対話モード】共通鍵暗号体験")
    print("=" * 55)

    while True:
        print("\n  操作を選んでください:")
        print("  1. テキストを暗号化")
        print("  2. 暗号文を復号（16進数入力）")
        print("  3. XOR演算の過程を視覚化")
        print("  4. ランダムな鍵を生成")
        print("  5. メニューに戻る")

        choice = input("\n  選択 (1-5): ").strip()

        if choice == "1":
            plaintext = input("  暗号化するテキストを入力: ")
            key_text = input("  鍵（パスワード）を入力: ")
            if plaintext and key_text:
                plain_bytes = plaintext.encode("utf-8")
                key_bytes = key_text.encode("utf-8")
                cipher = xor_encrypt(plain_bytes, key_bytes)
                cipher_hex = binascii.hexlify(cipher).decode()

                print(f"\n  平文:   \"{plaintext}\"")
                print(f"  鍵:     \"{key_text}\"")
                print(f"  暗号文（16進数）: {cipher_hex}")
                print(f"\n  ※ この16進数文字列を保存して、復号に使えます。")
            else:
                print("  ※ テキストと鍵の両方を入力してください。")

        elif choice == "2":
            cipher_hex = input("  暗号文（16進数）を入力: ").strip()
            key_text = input("  鍵（パスワード）を入力: ")
            try:
                cipher_bytes = binascii.unhexlify(cipher_hex)
                key_bytes = key_text.encode("utf-8")
                decrypted = xor_decrypt(cipher_bytes, key_bytes)
                try:
                    result = decrypted.decode("utf-8")
                    print(f"\n  復号結果: \"{result}\"")
                except UnicodeDecodeError:
                    print(f"\n  復号結果（バイナリ）: {binascii.hexlify(decrypted).decode()}")
                    print(f"  ※ 鍵が間違っている可能性があります。")
            except (ValueError, binascii.Error):
                print("  ※ 有効な16進数文字列を入力してください。")

        elif choice == "3":
            text = input("  テキストを入力: ")
            key = input("  鍵を入力: ")
            if text and key:
                visualize_xor_process(text, key)
            else:
                print("  ※ テキストと鍵の両方を入力してください。")

        elif choice == "4":
            try:
                length = int(input("  鍵の長さ（バイト数、例: 16）: ").strip())
                if 1 <= length <= 256:
                    random_key = os.urandom(length)
                    print(f"\n  生成された鍵（16進数）: {binascii.hexlify(random_key).decode()}")
                    print(f"  鍵の長さ: {length}バイト（{length * 8}ビット）")
                    print(f"\n  ※ この鍵は暗号学的に安全な乱数で生成されています。")
                else:
                    print("  ※ 1〜256 の範囲で指定してください。")
            except ValueError:
                print("  ※ 有効な数値を入力してください。")

        elif choice == "5":
            break
        else:
            print("  ※ 1〜5 の数字を入力してください。")


# --- メインプログラム ---
if __name__ == "__main__":
    print("+" + "=" * 53 + "+")
    print("|        共通鍵暗号シミュレータ                      |")
    print("|        〜 XOR暗号で暗号化の仕組みを体験 〜         |")
    print("+" + "=" * 53 + "+")

    # 共通鍵暗号の解説
    explain_symmetric_encryption()

    while True:
        print("\n  モードを選択してください:")
        print("  1. デモモード（各機能を実演）")
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

# ==============================
# ハッシュ値計算ツール
# 情報セキュリティ基礎：ハッシュ関数の仕組みを体験するサンプル
# ==============================
# 学べる内容:
#   - ハッシュ関数の基本概念と特徴
#   - MD5, SHA-1, SHA-256, SHA-512 の違い
#   - 文字列のハッシュ値計算
#   - ファイルのハッシュ値計算（改ざん検知）
#   - ハッシュの一方向性と衝突耐性
#   - ソルト（salt）の概念
#
# 実行方法:
#   python 02_ハッシュ値計算ツール.py
#
# ※ 本プログラムは教育目的で作成されています
# ==============================

import hashlib
import os
import time
import tempfile


def explain_hash():
    """ハッシュ関数の仕組みをアスキーアートで解説します"""
    print("""
  ┌──────────────────────────────────────────────────┐
  │              ハッシュ関数とは？                    │
  └──────────────────────────────────────────────────┘

  任意の長さのデータを、固定長の「ハッシュ値」に変換する関数です。
  ハッシュ値は「デジタル指紋」とも呼ばれます。

  【基本的な仕組み】
    入力データ            ハッシュ関数           ハッシュ値
  ┌──────────┐         ┌──────────┐       ┌──────────────┐
  │ "Hello"  │──────→ │ SHA-256  │──→   │ 185f8db3...  │
  └──────────┘         └──────────┘       └──────────────┘
  ┌──────────────┐     ┌──────────┐       ┌──────────────┐
  │ 巨大ファイル  │──→ │ SHA-256  │──→   │ 3a7bd3e2...  │
  │ (数GB)       │     └──────────┘       └──────────────┘
  └──────────────┘                  常に固定長（256ビット）

  【ハッシュ関数の3つの重要な性質】
  ┌─────────────┬──────────────────────────────────────┐
  │ 一方向性     │ ハッシュ値から元データの復元が不可能  │
  │ 衝突耐性     │ 異なるデータが同じハッシュ値になりにくい│
  │ 雪崩効果     │ 入力が1ビット変わると出力が大きく変化  │
  └─────────────┴──────────────────────────────────────┘

  【主なハッシュアルゴリズム】
  ┌──────────┬────────┬──────────────────────────────┐
  │ MD5      │ 128bit │ 非推奨（衝突が発見済み）      │
  │ SHA-1    │ 160bit │ 非推奨（衝突が発見済み）      │
  │ SHA-256  │ 256bit │ 推奨（現在の標準）            │
  │ SHA-512  │ 512bit │ 推奨（より高い安全性）        │
  └──────────┴────────┴──────────────────────────────┘
    """)


def hash_string(text, algorithm="sha256"):
    """文字列のハッシュ値を計算します"""
    data = text.encode("utf-8")
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()


def hash_all_algorithms(text):
    """主要な全アルゴリズムでハッシュ値を計算して比較します"""
    print(f"\n  入力文字列: \"{text}\"")
    print(f"  入力バイト数: {len(text.encode('utf-8'))} bytes")
    print()

    algorithms = [
        ("MD5", "md5", 128),
        ("SHA-1", "sha1", 160),
        ("SHA-256", "sha256", 256),
        ("SHA-512", "sha512", 512),
    ]

    print(f"  {'アルゴリズム':<12} {'ビット数':<10} {'ハッシュ値'}")
    print(f"  {'─' * 12} {'─' * 10} {'─' * 50}")

    for name, algo, bits in algorithms:
        digest = hash_string(text, algo)
        # 長いハッシュ値は改行して表示
        if len(digest) > 50:
            print(f"  {name:<12} {bits:<10} {digest[:50]}")
            print(f"  {'':>24}{digest[50:]}")
        else:
            print(f"  {name:<12} {bits:<10} {digest}")


def demonstrate_avalanche_effect():
    """雪崩効果（Avalanche Effect）を実演します"""
    print("\n" + "=" * 55)
    print("  雪崩効果（Avalanche Effect）の実演")
    print("=" * 55)
    print("\n  入力が1文字だけ異なるとハッシュ値はどう変わるでしょう？\n")

    pairs = [
        ("Hello", "hello"),    # 大文字小文字の違い
        ("test", "tess"),      # 1文字だけ違う
        ("abc", "abd"),        # 末尾1文字の違い
        ("password", "password1"),  # 1文字追加
    ]

    for text1, text2 in pairs:
        hash1 = hash_string(text1, "sha256")
        hash2 = hash_string(text2, "sha256")

        # 異なるビット数を計算
        diff_bits = 0
        for c1, c2 in zip(hash1, hash2):
            xor = int(c1, 16) ^ int(c2, 16)
            diff_bits += bin(xor).count("1")

        print(f"  入力1: \"{text1}\"")
        print(f"  SHA-256: {hash1}")
        print(f"  入力2: \"{text2}\"")
        print(f"  SHA-256: {hash2}")
        print(f"  → 異なるビット数: {diff_bits}/256 ({diff_bits / 256 * 100:.1f}%)")
        print(f"     ※ 理想的には約50%が変化します")
        print()


def demonstrate_tamper_detection():
    """ファイルの改ざん検知をデモします"""
    print("\n" + "=" * 55)
    print("  ファイル改ざん検知のデモ")
    print("=" * 55)

    # テスト用の一時ファイルを作成
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                      delete=False, encoding="utf-8") as f:
        original_content = "これは重要なドキュメントです。改ざんされていないことを確認します。"
        f.write(original_content)
        temp_path = f.name

    try:
        # 元のハッシュ値を計算
        print(f"\n  ステップ1: 元のファイルのハッシュ値を記録")
        original_hash = hash_file(temp_path)
        print(f"  ファイル: {os.path.basename(temp_path)}")
        print(f"  SHA-256:  {original_hash}")

        # ファイルを「改ざん」
        print(f"\n  ステップ2: ファイルを改ざん（1文字追加）")
        with open(temp_path, "a", encoding="utf-8") as f:
            f.write("。")  # たった1文字追加

        # 改ざん後のハッシュ値
        tampered_hash = hash_file(temp_path)
        print(f"  SHA-256:  {tampered_hash}")

        # 比較
        print(f"\n  ステップ3: ハッシュ値を比較")
        if original_hash == tampered_hash:
            print(f"  結果: 一致 → ファイルは改ざんされていません")
        else:
            print(f"  結果: 不一致 → ファイルが改ざんされています！")
            print(f"  元:   {original_hash}")
            print(f"  現在: {tampered_hash}")
            print(f"\n  ※ たった1文字の変更でも、ハッシュ値は完全に異なります。")
            print(f"     これがハッシュ関数による改ざん検知の仕組みです。")

    finally:
        # 一時ファイルを削除
        os.unlink(temp_path)


def hash_file(filepath):
    """ファイルのSHA-256ハッシュ値を計算します"""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            sha256.update(chunk)
    return sha256.hexdigest()


def demonstrate_salt():
    """ソルト（salt）の重要性を実演します"""
    print("\n" + "=" * 55)
    print("  ソルト（salt）の重要性")
    print("=" * 55)

    print("""
  パスワードをハッシュ化して保存するとき、
  「ソルト」を付加することで安全性が大幅に向上します。

  【ソルトなしの場合の問題点】
  同じパスワードは常に同じハッシュ値になります。
  → レインボーテーブル攻撃（事前計算されたハッシュ値の辞書）に弱い
    """)

    password = "password123"

    # ソルトなし
    print(f"  パスワード: \"{password}\"")
    print(f"\n  【ソルトなし】")
    hash_no_salt = hash_string(password, "sha256")
    print(f"  SHA-256: {hash_no_salt}")
    print(f"  ※ 同じパスワードなら毎回同じハッシュ値です")

    # ソルトあり
    print(f"\n  【ソルトあり】")
    for i in range(3):
        salt = os.urandom(16).hex()  # ランダムなソルトを生成
        salted_hash = hash_string(salt + password, "sha256")
        print(f"  ソルト {i + 1}: {salt}")
        print(f"  SHA-256:  {salted_hash}")
        print()

    print(f"  ※ ソルトが違うと同じパスワードでも異なるハッシュ値になります。")
    print(f"     ユーザーごとに異なるソルトを使うのがベストプラクティスです。")


def demo_mode():
    """デモモード: ハッシュ関数の各機能を実演します"""
    print("\n" + "=" * 55)
    print("  【デモモード】ハッシュ関数の実演")
    print("=" * 55)

    # 基本的なハッシュ計算
    print("\n  ◆ 各アルゴリズムによるハッシュ値の比較")
    hash_all_algorithms("Hello, World!")

    # 雪崩効果
    print("\n  ◆ 雪崩効果の実演")
    demonstrate_avalanche_effect()

    # 改ざん検知
    print("\n  ◆ ファイル改ざん検知")
    demonstrate_tamper_detection()

    # ソルト
    print("\n  ◆ ソルトの重要性")
    demonstrate_salt()


def interactive_mode():
    """対話モード: ユーザーが自分でハッシュ値を計算します"""
    print("\n" + "=" * 55)
    print("  【対話モード】ハッシュ値計算")
    print("=" * 55)

    while True:
        print("\n  操作を選んでください:")
        print("  1. 文字列のハッシュ値を計算")
        print("  2. ファイルのハッシュ値を計算")
        print("  3. 2つの文字列のハッシュ値を比較")
        print("  4. 雪崩効果を確認")
        print("  5. ソルト付きハッシュを計算")
        print("  6. メニューに戻る")

        choice = input("\n  選択 (1-6): ").strip()

        if choice == "1":
            text = input("  ハッシュ値を計算する文字列を入力: ")
            if text:
                hash_all_algorithms(text)
            else:
                print("  ※ 文字列を入力してください。")

        elif choice == "2":
            filepath = input("  ファイルパスを入力: ").strip()
            if os.path.isfile(filepath):
                print(f"\n  ファイル: {filepath}")
                print(f"  サイズ:   {os.path.getsize(filepath)} bytes")
                file_hash = hash_file(filepath)
                print(f"  SHA-256:  {file_hash}")
            else:
                print(f"  ※ ファイルが見つかりません: {filepath}")

        elif choice == "3":
            text1 = input("  1つ目の文字列: ")
            text2 = input("  2つ目の文字列: ")
            hash1 = hash_string(text1, "sha256")
            hash2 = hash_string(text2, "sha256")
            print(f"\n  文字列1: \"{text1}\"")
            print(f"  SHA-256: {hash1}")
            print(f"  文字列2: \"{text2}\"")
            print(f"  SHA-256: {hash2}")
            if hash1 == hash2:
                print(f"\n  結果: 一致 → 同じ内容です")
            else:
                print(f"\n  結果: 不一致 → 異なる内容です")

        elif choice == "4":
            text = input("  基準となる文字列を入力: ")
            if text:
                modified = text[:-1] + chr(ord(text[-1]) + 1) if text else "a"
                hash1 = hash_string(text, "sha256")
                hash2 = hash_string(modified, "sha256")
                print(f"\n  元の文字列:   \"{text}\"")
                print(f"  SHA-256:      {hash1}")
                print(f"  変更後:       \"{modified}\"")
                print(f"  SHA-256:      {hash2}")
                diff = sum(1 for a, b in zip(hash1, hash2) if a != b)
                print(f"  異なる16進文字数: {diff}/{len(hash1)}")

        elif choice == "5":
            text = input("  パスワード文字列を入力: ")
            salt = os.urandom(16).hex()
            salted = salt + text
            result = hash_string(salted, "sha256")
            print(f"\n  パスワード: \"{text}\"")
            print(f"  ソルト:     {salt}")
            print(f"  SHA-256:    {result}")
            print(f"\n  ※ 保存時はソルトとハッシュ値をセットで保存します。")

        elif choice == "6":
            break
        else:
            print("  ※ 1〜6 の数字を入力してください。")


# --- メインプログラム ---
if __name__ == "__main__":
    print("+" + "=" * 53 + "+")
    print("|        ハッシュ値計算ツール                        |")
    print("|        〜 デジタル指紋の世界を体験 〜              |")
    print("+" + "=" * 53 + "+")

    # ハッシュ関数の解説
    explain_hash()

    while True:
        print("\n  モードを選択してください:")
        print("  1. デモモード（各機能を実演）")
        print("  2. 対話モード（自分で計算）")
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

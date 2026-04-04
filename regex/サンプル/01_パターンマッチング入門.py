"""
正規表現サンプル01：パターンマッチング入門
==========================================

学べる内容:
  - re.search(), re.findall(), re.sub() の基本的な使い方
  - メタ文字 \d, \w, \s の使い方
  - エスケープの仕組み

実行方法:
  python 01_パターンマッチング入門.py
"""

import re


def main():
    print("=" * 50)
    print("正規表現パターンマッチング入門")
    print("=" * 50)

    # --- 1. re.search(): 最初のマッチを探す ---
    print("\n--- 1. re.search() ---")
    text = "今日は2026年4月5日、気温は22度です。"

    # 4桁の数字を探す
    result = re.search(r"\d{4}", text)
    if result:
        print(f"テキスト: {text}")
        print(f"最初の4桁の数字: {result.group()}")
        print(f"位置: {result.start()}〜{result.end()}")

    # --- 2. re.findall(): すべてのマッチを探す ---
    print("\n--- 2. re.findall() ---")
    text = "連絡先: 090-1234-5678 または 03-9876-5432"

    # すべての数字の塊を探す
    numbers = re.findall(r"\d+", text)
    print(f"テキスト: {text}")
    print(f"見つかった数字: {numbers}")

    # 電話番号パターンで探す
    phones = re.findall(r"\d{2,4}-\d{4}-\d{4}", text)
    print(f"見つかった電話番号: {phones}")

    # --- 3. re.sub(): 置換 ---
    print("\n--- 3. re.sub() ---")
    text = "パスワードは abc123 です。IDは user456 です。"

    # 数字を「*」に置換
    masked = re.sub(r"\d", "*", text)
    print(f"元テキスト: {text}")
    print(f"数字マスク: {masked}")

    # --- 4. メタ文字の実験 ---
    print("\n--- 4. メタ文字の比較 ---")
    text = "Hello World 123 !@#"

    print(f"テキスト: '{text}'")
    print(f"  \\d (数字)      : {re.findall(r'\\d', text)}")
    print(f"  \\D (数字以外)  : {re.findall(r'\\D', text)}")
    print(f"  \\w (単語文字)  : {re.findall(r'\\w', text)}")
    print(f"  \\W (単語以外)  : {re.findall(r'\\W', text)}")
    print(f"  \\s (空白)      : {re.findall(r'\\s', text)}")
    print(f"  \\S (空白以外)  : {re.findall(r'\\S', text)}")

    # --- 5. 対話モード ---
    print("\n--- 5. 対話モード ---")
    print("正規表現パターンを入力して試してみましょう。")
    print("終了するには 'quit' と入力してください。")

    sample_text = "私のメールは tanaka@example.com で、電話は 090-1234-5678 です。誕生日は 1990-05-15 です。"
    print(f"\n対象テキスト:\n  {sample_text}\n")

    while True:
        pattern = input("パターン> ").strip()
        if pattern.lower() == "quit":
            break
        if not pattern:
            continue

        try:
            results = re.findall(pattern, sample_text)
            if results:
                print(f"  マッチ: {results}")
            else:
                print("  マッチなし")
        except re.error as e:
            print(f"  エラー: {e}")

    print("\nお疲れさまでした！")


if __name__ == "__main__":
    main()

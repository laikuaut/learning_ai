"""
正規表現サンプル05：正規表現テスター
====================================

学べる内容:
  - 正規表現のインタラクティブなテスト方法
  - マッチ結果の詳細表示（位置、グループ）
  - よく使うパターンのライブラリ
  - re モジュールの各関数の使い分け

実行方法:
  python 05_正規表現テスター.py
"""

import re


# よく使うパターン集
PATTERN_LIBRARY = {
    "メールアドレス": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "電話番号（日本）": r"0\d{1,3}-?\d{2,4}-?\d{3,4}",
    "郵便番号": r"\d{3}-?\d{4}",
    "日付（YYYY-MM-DD）": r"\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])",
    "URL": r"https?://[^\s<>\"]+",
    "IPアドレス": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
    "全角数字": r"[０-９]+",
    "HTMLタグ": r"<[^>]+>",
    "日本語（ひらがな）": r"[\u3040-\u309F]+",
    "日本語（カタカナ）": r"[\u30A0-\u30FF]+",
}


def test_pattern_detail(pattern_str, text, flags=0):
    """パターンの詳細テスト結果を表示"""
    try:
        pattern = re.compile(pattern_str, flags)
    except re.error as e:
        print(f"  ❌ パターンエラー: {e}")
        return

    print(f"\n  パターン: {pattern_str}")
    print(f"  テキスト: {text}")
    print(f"  {'-' * 40}")

    # search
    match = pattern.search(text)
    if match:
        print(f"  search(): '{match.group()}' (位置: {match.start()}-{match.end()})")
        if match.groups():
            print(f"    グループ: {match.groups()}")
        if match.groupdict():
            print(f"    名前付き: {match.groupdict()}")
    else:
        print(f"  search(): マッチなし")

    # findall
    results = pattern.findall(text)
    print(f"  findall(): {results} ({len(results)}件)")

    # finditer（位置情報付き）
    matches = list(pattern.finditer(text))
    if matches:
        print(f"  finditer():")
        for m in matches:
            print(f"    '{m.group()}' at [{m.start()}:{m.end()}]")

    # マッチ位置をビジュアル表示
    if matches:
        print(f"\n  マッチ位置の可視化:")
        print(f"    {text}")
        markers = [" "] * len(text)
        for m in matches:
            for i in range(m.start(), m.end()):
                if i < len(markers):
                    markers[i] = "^"
        print(f"    {''.join(markers)}")


def interactive_mode():
    """対話式テストモード"""
    print("\n--- 対話式テストモード ---")
    print("パターンとテキストを入力してテストできます。")
    print("コマンド: 'back'=戻る, 'lib'=パターンライブラリ")

    current_text = "山田太郎 yamada@example.com 090-1234-5678 東京都新宿区 2026-04-05"
    print(f"\nデフォルトテキスト: {current_text}")

    while True:
        print()
        cmd = input("パターン（または 'text' でテキスト変更）> ").strip()

        if cmd.lower() == "back":
            break
        elif cmd.lower() == "lib":
            show_library(current_text)
        elif cmd.lower() == "text":
            new_text = input("新しいテキスト> ")
            if new_text:
                current_text = new_text
                print(f"  テキストを更新しました: {current_text}")
        elif cmd:
            test_pattern_detail(cmd, current_text)


def show_library(text=""):
    """パターンライブラリを表示・テスト"""
    print("\n--- パターンライブラリ ---")
    for i, (name, pattern) in enumerate(PATTERN_LIBRARY.items(), 1):
        print(f"  {i:2d}. {name}")
        print(f"      パターン: {pattern}")
        if text:
            results = re.findall(pattern, text)
            if results:
                print(f"      マッチ: {results}")
        print()


def function_comparison():
    """re モジュールの各関数の比較デモ"""
    print("\n--- re モジュール関数の比較 ---")
    text = "abc 123 def 456 ghi"
    pattern = r"\d+"

    print(f"  テキスト: '{text}'")
    print(f"  パターン: {pattern}")
    print()

    # match vs search
    print("  re.match():")
    result = re.match(pattern, text)
    print(f"    結果: {result}")
    print(f"    → 文字列の先頭からマッチを試みる（先頭が数字でないのでNone）")

    print("\n  re.search():")
    result = re.search(pattern, text)
    print(f"    結果: '{result.group()}' at position {result.start()}")
    print(f"    → 文字列全体から最初のマッチを探す")

    print("\n  re.findall():")
    result = re.findall(pattern, text)
    print(f"    結果: {result}")
    print(f"    → すべてのマッチをリストで返す")

    print("\n  re.finditer():")
    for m in re.finditer(pattern, text):
        print(f"    '{m.group()}' at [{m.start()}:{m.end()}]")
    print(f"    → すべてのマッチをイテレータで返す（位置情報付き）")

    print("\n  re.sub():")
    result = re.sub(pattern, "NUM", text)
    print(f"    結果: '{result}'")
    print(f"    → マッチ部分を置換")

    print("\n  re.split():")
    result = re.split(r"\s+", text)
    print(f"    結果: {result}")
    print(f"    → パターンで分割")

    print("\n  re.fullmatch():")
    result = re.fullmatch(r"\d+", "12345")
    print(f"    '12345' → {result.group() if result else None}")
    result = re.fullmatch(r"\d+", "123abc")
    print(f"    '123abc' → {result}")
    print(f"    → 文字列全体がパターンと完全一致するか")


def main():
    print("=" * 50)
    print("正規表現テスター")
    print("=" * 50)

    while True:
        print("\nメニュー:")
        print("  1. 対話式テスト")
        print("  2. パターンライブラリ")
        print("  3. re関数の比較デモ")
        print("  q. 終了")

        choice = input("\n選択> ").strip()

        if choice == "q":
            break
        elif choice == "1":
            interactive_mode()
        elif choice == "2":
            sample = "田中太郎 tanaka@example.com 090-1234-5678 〒100-0001 https://example.com 192.168.1.1"
            print(f"\nテスト対象: {sample}")
            show_library(sample)
        elif choice == "3":
            function_comparison()

    print("\nお疲れさまでした！")


if __name__ == "__main__":
    main()

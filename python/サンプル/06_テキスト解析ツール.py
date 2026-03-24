# ==============================
# テキスト解析ツール
# 第6章：文字列操作の総合サンプル
# ==============================
# 学べる内容:
#   - split(), join(), replace(), strip()
#   - find(), count(), startswith(), endswith()
#   - f文字列と書式指定
#   - 正規表現（re モジュール）
#   - 文字列の判定メソッド（isdigit, isalpha 等）
#   - スライスと文字列の操作テクニック
# ==============================

import re
from collections import Counter


def count_words(text):
    """単語数をカウントする（split で分割）"""
    words = text.split()
    return len(words)


def count_chars(text, ignore_spaces=True):
    """文字数をカウントする"""
    if ignore_spaces:
        return len(text.replace(" ", "").replace("\n", ""))
    return len(text)


def count_lines(text):
    """行数をカウントする"""
    if not text:
        return 0
    return len(text.split("\n"))


def find_word_frequency(text, top_n=10):
    """単語の出現頻度を集計する（Counter を活用）"""
    # 記号を除去し、小文字に統一して分割
    cleaned = re.sub(r"[、。！？「」\n]", " ", text)
    words = cleaned.split()
    # 空文字列を除外
    words = [w for w in words if w]
    return Counter(words).most_common(top_n)


def find_pattern(text, pattern):
    """正規表現でパターンを検索する"""
    matches = re.findall(pattern, text)
    return matches


def replace_words(text, replacements):
    """複数の単語を一括置換する（辞書で置換ルールを管理）"""
    result = text
    for old, new in replacements.items():
        result = result.replace(old, new)
    return result


def extract_emails(text):
    """テキストからメールアドレスを抽出する（正規表現）"""
    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+"
    return re.findall(pattern, text)


def extract_urls(text):
    """テキストからURLを抽出する（正規表現）"""
    pattern = r"https?://[a-zA-Z0-9._/~?&=%#+-]+"
    return re.findall(pattern, text)


def extract_numbers(text):
    """テキストから数値を抽出する（整数・小数対応）"""
    pattern = r"-?\d+\.?\d*"
    return [float(n) if "." in n else int(n) for n in re.findall(pattern, text)]


def censor_text(text, words_to_censor):
    """指定した単語を伏せ字にする"""
    result = text
    for word in words_to_censor:
        # 単語と同じ長さの「*」で置換
        result = result.replace(word, "*" * len(word))
    return result


def text_statistics(text):
    """テキストの統計情報をまとめて返す"""
    lines = text.split("\n")
    words = text.split()

    stats = {
        "行数": len(lines),
        "単語数": len(words),
        "文字数（空白含む）": len(text),
        "文字数（空白除く）": count_chars(text),
        "平均行長": round(sum(len(l) for l in lines) / len(lines), 1) if lines else 0,
        "最長行の文字数": max(len(l) for l in lines) if lines else 0,
        "最短行の文字数": min(len(l) for l in lines) if lines else 0,
    }
    return stats


def format_table(headers, rows, col_width=12):
    """データを表形式にフォーマットする（f文字列の書式指定）"""
    # ヘッダー行
    header_line = "".join(f"{h:<{col_width}}" for h in headers)
    separator = "-" * (col_width * len(headers))

    # データ行
    data_lines = []
    for row in rows:
        line = "".join(f"{str(v):<{col_width}}" for v in row)
        data_lines.append(line)

    return "\n".join([header_line, separator] + data_lines)


# === メインプログラム ===

sample_text = """Pythonは初心者に優しいプログラミング言語です。
Pythonはデータ分析やWeb開発など幅広い分野で活用されています。
公式サイト: https://www.python.org/
お問い合わせ: info@example.com または support@python-school.jp
Pythonのバージョンは3.12が最新です。
プログラミングを学ぶには実際に手を動かすことが大切です。
今日の気温は28.5度、明日は32度の予報です。"""

print("=" * 50)
print("  テキスト解析ツール")
print("=" * 50)

# --- テキスト統計 ---
print("\n【テキスト統計】")
stats = text_statistics(sample_text)
for key, value in stats.items():
    print(f"  {key:<18}: {value}")

# --- 単語頻度 ---
print("\n【単語出現頻度 TOP5】")
freq = find_word_frequency(sample_text, 5)
for rank, (word, count) in enumerate(freq, start=1):
    bar = "#" * count
    print(f"  {rank}. {word:<10} {count}回 {bar}")

# --- 情報抽出 ---
print("\n【メールアドレス抽出】")
emails = extract_emails(sample_text)
for email in emails:
    user, domain = email.split("@")
    print(f"  {email}  (ユーザー: {user}, ドメイン: {domain})")

print("\n【URL抽出】")
urls = extract_urls(sample_text)
for url in urls:
    print(f"  {url}")

print("\n【数値抽出】")
numbers = extract_numbers(sample_text)
print(f"  見つかった数値: {numbers}")
if numbers:
    print(f"  合計: {sum(numbers)}, 平均: {sum(numbers)/len(numbers):.1f}")

# --- テキスト加工 ---
print("\n【テキスト置換】")
replacements = {"Python": "パイソン", "プログラミング": "コーディング"}
modified = replace_words(sample_text.split("\n")[0], replacements)
print(f"  元: {sample_text.split(chr(10))[0]}")
print(f"  後: {modified}")

# --- 伏せ字機能 ---
print("\n【伏せ字処理】")
censored = censor_text(sample_text.split("\n")[3], ["info@example.com", "support@python-school.jp"])
print(f"  {censored}")


# === 対話モード ===
print("\n\n" + "=" * 50)
print("  対話モード - テキストを分析します")
print("=" * 50)

while True:
    print("\n--- メニュー ---")
    print("1. テキストの統計を表示")
    print("2. パターン検索（正規表現）")
    print("3. テキスト置換")
    print("4. 終了")

    choice = input("選択 (1-4): ").strip()

    if choice == "1":
        text = input("テキストを入力: ")
        stats = text_statistics(text)
        for key, value in stats.items():
            print(f"  {key}: {value}")

    elif choice == "2":
        text = input("テキストを入力: ")
        pattern = input("検索パターン（正規表現）: ")
        try:
            matches = find_pattern(text, pattern)
            if matches:
                print(f"  {len(matches)}件見つかりました: {matches}")
            else:
                print("  マッチする箇所はありません")
        except re.error as e:
            print(f"  正規表現エラー: {e}")

    elif choice == "3":
        text = input("テキストを入力: ")
        old = input("置換前の文字列: ")
        new = input("置換後の文字列: ")
        result = text.replace(old, new)
        count = text.count(old)
        print(f"  {count}箇所を置換しました")
        print(f"  結果: {result}")

    elif choice == "4":
        print("終了します。")
        break
    else:
        print("1〜4の数字を入力してください。")

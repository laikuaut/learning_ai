# ==============================
# モジュール活用ツール
# 第10章：モジュールとパッケージの実践
# ==============================
# 学べる内容:
#   - 標準ライブラリの活用（os, sys, math, statistics, collections, itertools）
#   - datetime による日付・時刻操作
#   - random によるランダム処理
#   - json によるデータ保存
#   - hashlib によるハッシュ計算
#   - urllib.request による簡易HTTP通信
#   - argparse コマンドライン引数（紹介）
#   - モジュールの使い分けと組み合わせ
# 実行方法:
#   python 10_モジュール活用ツール.py
# ==============================

import os
import sys
import math
import statistics
import random
import string
import hashlib
import json
import textwrap
from datetime import datetime, date, timedelta
from collections import Counter, defaultdict
from pathlib import Path


# === ツール1：日付・時刻ユーティリティ ===

def date_tools():
    """日付・時刻に関する便利ツール集"""
    print("\n" + "=" * 50)
    print("  日付・時刻ユーティリティ")
    print("=" * 50)

    while True:
        print("\n  1. 今日の日付と時刻")
        print("  2. 日付の差を計算")
        print("  3. N日後/前の日付")
        print("  4. 曜日を調べる")
        print("  5. 年齢を計算")
        print("  0. 戻る")

        choice = input("  選択: ").strip()

        if choice == "1":
            now = datetime.now()
            print(f"\n  現在の日時: {now.strftime('%Y年%m月%d日 %H時%M分%S秒')}")
            print(f"  ISO形式:    {now.isoformat()}")
            print(f"  タイムスタンプ: {now.timestamp()}")
            weekdays = ["月", "火", "水", "木", "金", "土", "日"]
            print(f"  曜日: {weekdays[now.weekday()]}曜日")

        elif choice == "2":
            try:
                d1 = input("  日付1 (YYYY-MM-DD): ").strip()
                d2 = input("  日付2 (YYYY-MM-DD): ").strip()
                date1 = datetime.strptime(d1, "%Y-%m-%d")
                date2 = datetime.strptime(d2, "%Y-%m-%d")
                diff = abs((date2 - date1).days)
                print(f"\n  {d1} と {d2} の差: {diff}日")
                print(f"  （約 {diff // 7}週間 {diff % 7}日）")
            except ValueError:
                print("  日付の形式が不正です。")

        elif choice == "3":
            try:
                days = int(input("  何日後？（負数で前）: ").strip())
                target = date.today() + timedelta(days=days)
                direction = "後" if days >= 0 else "前"
                print(f"\n  今日から {abs(days)}日{direction}: "
                      f"{target.strftime('%Y年%m月%d日')}")
            except ValueError:
                print("  数値を入力してください。")

        elif choice == "4":
            try:
                d = input("  日付 (YYYY-MM-DD): ").strip()
                target = datetime.strptime(d, "%Y-%m-%d")
                weekdays = ["月", "火", "水", "木", "金", "土", "日"]
                print(f"\n  {d} は {weekdays[target.weekday()]}曜日です。")
            except ValueError:
                print("  日付の形式が不正です。")

        elif choice == "5":
            try:
                birthday = input("  生年月日 (YYYY-MM-DD): ").strip()
                born = datetime.strptime(birthday, "%Y-%m-%d").date()
                today = date.today()
                age = today.year - born.year
                # 今年の誕生日がまだ来ていなければ1歳引く
                if (today.month, today.day) < (born.month, born.day):
                    age -= 1
                print(f"\n  現在の年齢: {age}歳")
                # 次の誕生日までの日数
                next_birthday = born.replace(year=today.year)
                if next_birthday < today:
                    next_birthday = born.replace(year=today.year + 1)
                days_until = (next_birthday - today).days
                print(f"  次の誕生日まで: {days_until}日")
            except ValueError:
                print("  日付の形式が不正です。")

        elif choice == "0":
            break


# === ツール2：数学・統計ツール ===

def math_tools():
    """数学・統計に関するツール集"""
    print("\n" + "=" * 50)
    print("  数学・統計ツール")
    print("=" * 50)

    while True:
        print("\n  1. 統計計算（平均・中央値・標準偏差）")
        print("  2. 素数判定")
        print("  3. 最大公約数と最小公倍数")
        print("  4. 進数変換")
        print("  5. 三角関数の計算")
        print("  0. 戻る")

        choice = input("  選択: ").strip()

        if choice == "1":
            try:
                nums_input = input("  数値をカンマ区切りで入力: ").strip()
                nums = [float(x.strip()) for x in nums_input.split(",")]
                if len(nums) < 2:
                    print("  2つ以上の数値を入力してください。")
                    continue
                print(f"\n  データ: {nums}")
                print(f"  個数:     {len(nums)}")
                print(f"  合計:     {sum(nums):.2f}")
                print(f"  平均:     {statistics.mean(nums):.2f}")
                print(f"  中央値:   {statistics.median(nums):.2f}")
                print(f"  最大値:   {max(nums):.2f}")
                print(f"  最小値:   {min(nums):.2f}")
                if len(nums) >= 2:
                    print(f"  標準偏差: {statistics.stdev(nums):.2f}")
                    print(f"  分散:     {statistics.variance(nums):.2f}")
            except ValueError:
                print("  数値を正しく入力してください。")

        elif choice == "2":
            try:
                n = int(input("  判定する数: ").strip())
                if n < 2:
                    print(f"  {n} は素数ではありません。")
                    continue
                # 素数判定（試し割り法）
                is_prime = True
                for i in range(2, int(math.sqrt(n)) + 1):
                    if n % i == 0:
                        is_prime = False
                        break
                if is_prime:
                    print(f"  {n} は素数です！")
                else:
                    # 素因数分解も表示
                    factors = []
                    temp = n
                    d = 2
                    while d * d <= temp:
                        while temp % d == 0:
                            factors.append(d)
                            temp //= d
                        d += 1
                    if temp > 1:
                        factors.append(temp)
                    print(f"  {n} は素数ではありません。")
                    print(f"  素因数分解: {' x '.join(map(str, factors))}")
            except ValueError:
                print("  整数を入力してください。")

        elif choice == "3":
            try:
                a = int(input("  1つ目の数: ").strip())
                b = int(input("  2つ目の数: ").strip())
                gcd = math.gcd(a, b)
                lcm = abs(a * b) // gcd
                print(f"\n  最大公約数 (GCD): {gcd}")
                print(f"  最小公倍数 (LCM): {lcm}")
            except ValueError:
                print("  整数を入力してください。")

        elif choice == "4":
            try:
                num = int(input("  10進数の数値: ").strip())
                print(f"\n  10進数: {num}")
                print(f"   2進数: {bin(num)}")
                print(f"   8進数: {oct(num)}")
                print(f"  16進数: {hex(num)}")
            except ValueError:
                print("  整数を入力してください。")

        elif choice == "5":
            try:
                angle = float(input("  角度（度）: ").strip())
                rad = math.radians(angle)
                print(f"\n  {angle}度 = {rad:.4f}ラジアン")
                print(f"  sin({angle}°) = {math.sin(rad):.6f}")
                print(f"  cos({angle}°) = {math.cos(rad):.6f}")
                print(f"  tan({angle}°) = {math.tan(rad):.6f}")
            except ValueError:
                print("  数値を入力してください。")

        elif choice == "0":
            break


# === ツール3：テキスト解析・変換ツール ===

def text_tools():
    """テキストの解析と変換ツール"""
    print("\n" + "=" * 50)
    print("  テキスト解析・変換ツール")
    print("=" * 50)

    while True:
        print("\n  1. 文字数・単語数カウント")
        print("  2. 文字出現頻度ランキング")
        print("  3. パスワード生成")
        print("  4. ハッシュ値の計算")
        print("  5. テキスト折り返し整形")
        print("  0. 戻る")

        choice = input("  選択: ").strip()

        if choice == "1":
            text = input("  テキスト: ").strip()
            if not text:
                print("  テキストを入力してください。")
                continue
            print(f"\n  文字数（全体）:  {len(text)}")
            print(f"  文字数（空白除く）: {len(text.replace(' ', ''))}")
            words = text.split()
            print(f"  単語数:          {len(words)}")
            # 日本語の文字種別カウント
            hiragana = sum(1 for c in text if '\u3040' <= c <= '\u309f')
            katakana = sum(1 for c in text if '\u30a0' <= c <= '\u30ff')
            kanji = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
            ascii_chars = sum(1 for c in text if c.isascii() and c.isalpha())
            digits = sum(1 for c in text if c.isdigit())
            print(f"  ひらがな: {hiragana}  カタカナ: {katakana}  漢字: {kanji}")
            print(f"  英字: {ascii_chars}  数字: {digits}")

        elif choice == "2":
            text = input("  テキスト: ").strip()
            if not text:
                print("  テキストを入力してください。")
                continue
            # collections.Counter で文字の出現頻度を集計
            counter = Counter(text.replace(" ", ""))
            print("\n  文字出現頻度 TOP10:")
            for char, count in counter.most_common(10):
                bar = "#" * count
                print(f"    '{char}': {count}回 {bar}")

        elif choice == "3":
            try:
                length = int(input("  パスワードの長さ (8〜64): ").strip())
                length = max(8, min(64, length))
            except ValueError:
                length = 12

            count = 5
            print(f"\n  生成されたパスワード（{length}文字 x {count}個）:")

            for i in range(count):
                # 英大文字・小文字・数字・記号を含むパスワード
                chars = string.ascii_letters + string.digits + "!@#$%&*"
                # random.choices で必要な文字種を確保
                password = [
                    random.choice(string.ascii_uppercase),
                    random.choice(string.ascii_lowercase),
                    random.choice(string.digits),
                    random.choice("!@#$%&*"),
                ]
                password += random.choices(chars, k=length - 4)
                random.shuffle(password)
                print(f"    {i + 1}. {''.join(password)}")

        elif choice == "4":
            text = input("  テキスト: ").strip()
            if not text:
                print("  テキストを入力してください。")
                continue
            # hashlib でハッシュ値を計算
            encoded = text.encode("utf-8")
            print(f"\n  入力: {text}")
            print(f"  MD5:    {hashlib.md5(encoded).hexdigest()}")
            print(f"  SHA-1:  {hashlib.sha1(encoded).hexdigest()}")
            print(f"  SHA-256:{hashlib.sha256(encoded).hexdigest()}")

        elif choice == "5":
            text = input("  長い文章を入力: ").strip()
            if not text:
                print("  テキストを入力してください。")
                continue
            try:
                width = int(input("  1行の文字数 (デフォルト40): ").strip() or "40")
            except ValueError:
                width = 40
            # textwrap で折り返し整形
            wrapped = textwrap.fill(text, width=width)
            print(f"\n  整形結果（{width}文字折り返し）:")
            print("  " + "-" * width)
            for line in wrapped.split("\n"):
                print(f"  {line}")
            print("  " + "-" * width)

        elif choice == "0":
            break


# === ツール4：ファイル・システム情報ツール ===

def system_tools():
    """システムとファイルに関するツール"""
    print("\n" + "=" * 50)
    print("  ファイル・システム情報ツール")
    print("=" * 50)

    while True:
        print("\n  1. Python環境情報")
        print("  2. カレントディレクトリの内容")
        print("  3. ファイルサイズの人間可読変換")
        print("  4. パス操作デモ（pathlib）")
        print("  0. 戻る")

        choice = input("  選択: ").strip()

        if choice == "1":
            print(f"\n  Python バージョン: {sys.version}")
            print(f"  プラットフォーム: {sys.platform}")
            print(f"  OS名:           {os.name}")
            print(f"  カレントディレクトリ: {os.getcwd()}")
            print(f"  実行ファイル:    {sys.executable}")
            print(f"  モジュール検索パス:")
            for p in sys.path[:5]:
                print(f"    {p}")
            if len(sys.path) > 5:
                print(f"    ... 他 {len(sys.path) - 5} パス")

        elif choice == "2":
            target = input("  ディレクトリ（Enterで現在地）: ").strip() or "."
            target_path = Path(target)
            if not target_path.is_dir():
                print(f"  '{target}' はディレクトリではありません。")
                continue

            items = list(target_path.iterdir())
            dirs = [i for i in items if i.is_dir()]
            files = [i for i in items if i.is_file()]

            print(f"\n  ディレクトリ: {target_path.resolve()}")
            print(f"  フォルダ: {len(dirs)}個 / ファイル: {len(files)}個")
            print()
            for d in sorted(dirs):
                print(f"    [DIR]  {d.name}/")
            for f in sorted(files):
                size = f.stat().st_size
                print(f"    [FILE] {f.name} ({format_size(size)})")

        elif choice == "3":
            try:
                size = int(input("  バイト数: ").strip())
                print(f"\n  {size} バイト = {format_size(size)}")
            except ValueError:
                print("  数値を入力してください。")

        elif choice == "4":
            path_str = input("  パスを入力 (例: /home/user/docs/file.txt): ").strip()
            if not path_str:
                path_str = "/home/user/project/src/main.py"
            p = Path(path_str)
            print(f"\n  元のパス:   {p}")
            print(f"  ファイル名: {p.name}")
            print(f"  拡張子:     {p.suffix}")
            print(f"  拡張子なし: {p.stem}")
            print(f"  親ディレクトリ: {p.parent}")
            print(f"  全パーツ:   {list(p.parts)}")
            # パスの結合
            new_path = p.parent / "new_file.txt"
            print(f"  結合例:     {new_path}")
            # 拡張子の変更
            print(f"  拡張子変更: {p.with_suffix('.md')}")

        elif choice == "0":
            break


def format_size(size_bytes):
    """バイト数を人間が読みやすい形式に変換する"""
    # math.log を使ったスマートな単位変換
    if size_bytes == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    # 1024 を底とする対数で単位を決定
    i = int(math.log(size_bytes, 1024))
    i = min(i, len(units) - 1)
    size = size_bytes / (1024 ** i)
    return f"{size:.1f} {units[i]}"


# === ツール5：データ集計・分析ツール ===

def data_tools():
    """コレクション操作を使ったデータ集計ツール"""
    print("\n" + "=" * 50)
    print("  データ集計・分析ツール")
    print("=" * 50)

    # サンプルデータ（アンケート結果）
    sample_data = {
        "好きなプログラミング言語": [
            "Python", "JavaScript", "Python", "TypeScript", "Go",
            "Python", "Rust", "JavaScript", "Python", "TypeScript",
            "C++", "Python", "JavaScript", "Go", "Python",
            "TypeScript", "Rust", "Python", "JavaScript", "Python",
        ],
        "プログラミング経験年数": [
            1, 3, 2, 5, 10, 1, 8, 3, 2, 4,
            15, 1, 6, 7, 2, 3, 5, 1, 4, 2,
        ],
    }

    print("\n  【サンプルデータ：プログラマーアンケート (20人)】")

    # Counter で集計
    lang_counter = Counter(sample_data["好きなプログラミング言語"])
    print("\n  好きな言語ランキング:")
    for rank, (lang, count) in enumerate(lang_counter.most_common(), 1):
        bar = "#" * (count * 2)
        print(f"    {rank}位 {lang:<12} {count:>2}票 {bar}")

    # statistics で統計量
    years = sample_data["プログラミング経験年数"]
    print(f"\n  経験年数の統計:")
    print(f"    平均:   {statistics.mean(years):.1f}年")
    print(f"    中央値: {statistics.median(years):.1f}年")
    print(f"    最頻値: {statistics.mode(years)}年")
    print(f"    標準偏差: {statistics.stdev(years):.1f}年")

    # defaultdict で経験年数をグループ化
    groups = defaultdict(list)
    for lang, year in zip(
        sample_data["好きなプログラミング言語"],
        sample_data["プログラミング経験年数"]
    ):
        groups[lang].append(year)

    print("\n  言語別の平均経験年数:")
    for lang, years_list in sorted(groups.items(),
                                   key=lambda x: statistics.mean(x[1]),
                                   reverse=True):
        avg = statistics.mean(years_list)
        print(f"    {lang:<12} 平均 {avg:.1f}年 ({len(years_list)}人)")

    # JSON出力のデモ
    print("\n  結果をJSON形式で表示:")
    result = {
        "ランキング": {lang: count for lang, count in lang_counter.most_common()},
        "統計": {
            "平均経験年数": round(statistics.mean(
                sample_data["プログラミング経験年数"]), 1),
            "回答者数": len(sample_data["好きなプログラミング言語"]),
        }
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


# === メインプログラム ===

print("+" + "-" * 34 + "+")
print("|    モジュール活用ツール集       |")
print("+" + "-" * 34 + "+")
print("Python標準ライブラリの便利な機能を")
print("体験できるツール集です。")

while True:
    print("\n--- メインメニュー ---")
    print("1. 日付・時刻ユーティリティ  (datetime)")
    print("2. 数学・統計ツール          (math, statistics)")
    print("3. テキスト解析・変換        (hashlib, collections)")
    print("4. ファイル・システム情報     (os, sys, pathlib)")
    print("5. データ集計・分析デモ       (collections, json)")
    print("6. 終了")

    choice = input("選択 (1-6): ").strip()

    if choice == "1":
        date_tools()
    elif choice == "2":
        math_tools()
    elif choice == "3":
        text_tools()
    elif choice == "4":
        system_tools()
    elif choice == "5":
        data_tools()
    elif choice == "6":
        print("お疲れさまでした！")
        break
    else:
        print("1〜6の数字を入力してください。")

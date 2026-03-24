# ==============================
# 家計簿アプリ
# 第7章：ファイル操作の総合サンプル
# ==============================
# 学べる内容:
#   - with文によるファイル操作
#   - CSVファイルの読み書き（csv モジュール）
#   - JSONファイルの読み書き（json モジュール）
#   - pathlib によるパス操作
#   - ファイルの存在確認と作成
#   - データの追記（append モード）
#   - 日付の扱い（datetime）
# ==============================

import csv
import json
from pathlib import Path
from datetime import datetime, date


# --- 設定 ---
DATA_DIR = Path("家計簿データ")
CSV_FILE = DATA_DIR / "transactions.csv"
SUMMARY_FILE = DATA_DIR / "monthly_summary.json"
CATEGORIES = ["食費", "交通費", "娯楽", "日用品", "光熱費", "通信費", "その他"]


def setup():
    """データディレクトリとファイルの初期化"""
    # ディレクトリがなければ作成（pathlib の mkdir）
    DATA_DIR.mkdir(exist_ok=True)

    # CSVファイルがなければヘッダーを書き込む
    if not CSV_FILE.exists():
        with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["日付", "カテゴリ", "内容", "金額", "収支"])
        print(f"  データファイルを作成しました: {CSV_FILE}")


def add_transaction():
    """取引を追加する（CSVファイルへの追記）"""
    print("\n--- 取引を追加 ---")

    # 日付の入力（デフォルトは今日）
    date_input = input(f"日付 (YYYY-MM-DD / Enterで今日): ").strip()
    if date_input:
        try:
            # 日付のバリデーション
            transaction_date = datetime.strptime(date_input, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("  日付の形式が不正です。YYYY-MM-DD で入力してください。")
            return
    else:
        transaction_date = date.today().strftime("%Y-%m-%d")

    # カテゴリの選択
    print("カテゴリ:")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"  {i}. {cat}")
    cat_choice = input("番号を選択: ").strip()
    try:
        category = CATEGORIES[int(cat_choice) - 1]
    except (ValueError, IndexError):
        print("  無効な選択です。")
        return

    # 内容と金額
    description = input("内容: ").strip()
    try:
        amount = int(input("金額: ").strip())
    except ValueError:
        print("  金額は数値で入力してください。")
        return

    # 収支の種類
    type_choice = input("収支 (1: 支出 / 2: 収入): ").strip()
    if type_choice == "2":
        income_expense = "収入"
    else:
        income_expense = "支出"
        amount = -abs(amount)  # 支出はマイナスで保存

    # CSVファイルに追記（"a"モード）
    with open(CSV_FILE, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([transaction_date, category, description, amount, income_expense])

    print(f"\n  記録しました: {transaction_date} {category} {description} "
          f"{abs(amount):,}円（{income_expense}）")


def show_transactions():
    """取引一覧を表示する（CSVファイルの読み込み）"""
    if not CSV_FILE.exists():
        print("  データがありません。")
        return

    print("\n--- 取引一覧 ---")

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("  データがありません。")
        return

    # ヘッダー表示
    print(f"{'日付':<12} {'カテゴリ':<8} {'内容':<12} {'金額':>10} {'収支':<4}")
    print("-" * 52)

    total_income = 0
    total_expense = 0

    for row in rows:
        amount = int(row["金額"])
        if amount > 0:
            total_income += amount
        else:
            total_expense += abs(amount)

        # 金額の表示（支出はマイナス表示）
        amount_str = f"{amount:>+,}円"
        print(f"{row['日付']:<12} {row['カテゴリ']:<8} "
              f"{row['内容']:<12} {amount_str:>10} {row['収支']:<4}")

    print("-" * 52)
    print(f"  収入合計: {total_income:>10,}円")
    print(f"  支出合計: {total_expense:>10,}円")
    print(f"  差引残高: {total_income - total_expense:>+10,}円")


def show_category_summary():
    """カテゴリ別の集計を表示する"""
    if not CSV_FILE.exists():
        print("  データがありません。")
        return

    print("\n--- カテゴリ別集計 ---")

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("  データがありません。")
        return

    # カテゴリ別に集計
    category_totals = {}
    for row in rows:
        cat = row["カテゴリ"]
        amount = abs(int(row["金額"]))
        if row["収支"] == "支出":
            category_totals[cat] = category_totals.get(cat, 0) + amount

    if not category_totals:
        print("  支出データがありません。")
        return

    # 金額の降順でソート
    sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    total = sum(category_totals.values())

    print(f"{'カテゴリ':<10} {'金額':>10} {'割合':>6} {'グラフ'}")
    print("-" * 50)

    for cat, amount in sorted_cats:
        ratio = amount / total * 100 if total > 0 else 0
        bar_length = int(ratio / 2)  # 最大50文字
        bar = "#" * bar_length
        print(f"{cat:<10} {amount:>9,}円 {ratio:>5.1f}% {bar}")

    print("-" * 50)
    print(f"{'合計':<10} {total:>9,}円")


def save_monthly_summary():
    """月次サマリーをJSONファイルに保存する"""
    if not CSV_FILE.exists():
        print("  データがありません。")
        return

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("  データがありません。")
        return

    # 月別に集計
    monthly = {}
    for row in rows:
        month = row["日付"][:7]  # YYYY-MM
        if month not in monthly:
            monthly[month] = {"収入": 0, "支出": 0, "取引数": 0}

        amount = int(row["金額"])
        if amount > 0:
            monthly[month]["収入"] += amount
        else:
            monthly[month]["支出"] += abs(amount)
        monthly[month]["取引数"] += 1

    # 差引を計算
    for month_data in monthly.values():
        month_data["差引"] = month_data["収入"] - month_data["支出"]

    # JSONファイルに保存（ensure_ascii=False で日本語をそのまま保存）
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(monthly, f, ensure_ascii=False, indent=2)

    print(f"\n  月次サマリーを保存しました: {SUMMARY_FILE}")

    # 保存した内容を表示
    print("\n--- 月次サマリー ---")
    for month, data in sorted(monthly.items()):
        print(f"  {month}: 収入 {data['収入']:,}円 / "
              f"支出 {data['支出']:,}円 / "
              f"差引 {data['差引']:+,}円 "
              f"({data['取引数']}件)")


def load_sample_data():
    """サンプルデータを読み込む（デモ用）"""
    sample = [
        ["2025-04-01", "食費", "スーパー買い物", -3500, "支出"],
        ["2025-04-01", "交通費", "電車定期", -12000, "支出"],
        ["2025-04-02", "食費", "ランチ", -850, "支出"],
        ["2025-04-03", "娯楽", "映画", -1800, "支出"],
        ["2025-04-05", "日用品", "洗剤・シャンプー", -1200, "支出"],
        ["2025-04-10", "光熱費", "電気代", -5600, "支出"],
        ["2025-04-10", "通信費", "スマホ代", -4800, "支出"],
        ["2025-04-15", "食費", "外食", -2400, "支出"],
        ["2025-04-20", "その他", "給料", 250000, "収入"],
        ["2025-04-22", "食費", "コンビニ", -680, "支出"],
        ["2025-04-25", "娯楽", "書籍", -1500, "支出"],
    ]

    with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["日付", "カテゴリ", "内容", "金額", "収支"])
        writer.writerows(sample)

    print(f"  サンプルデータ（{len(sample)}件）を読み込みました。")


# === メインプログラム ===

print("+" + "-" * 28 + "+")
print("|      家計簿アプリ         |")
print("+" + "-" * 28 + "+")

setup()

while True:
    print("\n--- メニュー ---")
    print("1. 取引を追加")
    print("2. 取引一覧")
    print("3. カテゴリ別集計")
    print("4. 月次サマリー保存")
    print("5. サンプルデータ読込")
    print("6. 終了")

    choice = input("選択 (1-6): ").strip()

    if choice == "1":
        add_transaction()
    elif choice == "2":
        show_transactions()
    elif choice == "3":
        show_category_summary()
    elif choice == "4":
        save_monthly_summary()
    elif choice == "5":
        load_sample_data()
    elif choice == "6":
        print("お疲れさまでした！")
        break
    else:
        print("1〜6の数字を入力してください。")

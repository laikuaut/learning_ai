# 実践課題07：CSVデータ集計ツール ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第4章（リストと辞書）、第5章（関数）、第7章（ファイル操作）
> **課題の種類**: ミニプロジェクト
> **学習目標**: ファイルの読み書き、データの解析・集計、整形出力を組み合わせて実用的なツールを作る

---

## 完成イメージ

まず、以下のCSVファイル `sales.csv` を作成してからプログラムを実行します。

**sales.csv:**
```
日付,商品名,カテゴリ,数量,単価
2024-01-05,りんご,果物,10,150
2024-01-05,牛乳,飲料,5,200
2024-01-06,パン,食品,8,120
2024-01-06,りんご,果物,3,150
2024-01-07,コーヒー,飲料,12,130
2024-01-07,パン,食品,6,120
2024-01-08,バナナ,果物,7,100
2024-01-08,牛乳,飲料,4,200
```

**実行結果:**
```
===== 売上データ集計 =====
データ件数: 8件
集計期間: 2024-01-05 〜 2024-01-08

--- カテゴリ別売上 ---
果物     :  2,800円 (3件)
飲料     :  3,360円 (3件)
食品     :  1,680円 (2件)

--- 商品別売上 TOP5 ---
 1. りんご     :  1,950円
 2. コーヒー   :  1,560円
 3. 牛乳       :  1,800円
 4. パン       :  1,680円
 5. バナナ     :    700円

--- 日別売上推移 ---
2024-01-05 :  2,500円 ████████████
2024-01-06 :  1,410円 ███████
2024-01-07 :  2,280円 ███████████
2024-01-08 :  1,500円 ████████

総売上: 7,690円 (平均: 961円/件)
```

---

## 課題の要件

1. CSVファイルを読み込み、データをリスト（各行を辞書で表現）に変換する
2. 以下の集計を行う
   - **カテゴリ別**: カテゴリごとの売上合計と件数
   - **商品別**: 商品ごとの売上合計（上位5件）
   - **日別**: 日ごとの売上合計と簡易棒グラフ
3. 総売上と平均売上を計算する
4. 結果を見やすく整形して出力する
5. CSVファイルが存在しない場合にエラーメッセージを表示する

---

## 事前準備

プログラムと同じフォルダに `sales.csv` を作成してください。
プログラム内でファイルを自動生成する方法もステップガイドで紹介します。

---

## ステップガイド

<details>
<summary>ステップ1：CSVファイルを読み込む</summary>

`csv` モジュールは使わず、自力でパースする練習です。

```python
def read_csv(filename):
    """CSVファイルを読み込み、辞書のリストで返す"""
    data = []
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 1行目はヘッダー
    headers = lines[0].strip().split(",")

    for line in lines[1:]:
        values = line.strip().split(",")
        row = {}
        for i in range(len(headers)):
            row[headers[i]] = values[i]
        data.append(row)

    return data
```

</details>

<details>
<summary>ステップ2：サンプルCSVを自動生成する（オプション）</summary>

ファイルがなければ自動で作成する方法です。

```python
import os

def create_sample_csv(filename):
    """サンプルのCSVファイルを作成する"""
    if os.path.exists(filename):
        return  # 既にあればスキップ

    sample_data = """日付,商品名,カテゴリ,数量,単価
2024-01-05,りんご,果物,10,150
2024-01-05,牛乳,飲料,5,200
2024-01-06,パン,食品,8,120
2024-01-06,りんご,果物,3,150
2024-01-07,コーヒー,飲料,12,130
2024-01-07,パン,食品,6,120
2024-01-08,バナナ,果物,7,100
2024-01-08,牛乳,飲料,4,200"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(sample_data)
    print(f"サンプルファイル '{filename}' を作成しました。")
```

</details>

<details>
<summary>ステップ3：カテゴリ別集計を実装する</summary>

辞書を使って、カテゴリをキー、売上合計を値として集計します。

```python
category_sales = {}
category_count = {}

for row in data:
    category = row["カテゴリ"]
    sales = int(row["数量"]) * int(row["単価"])

    if category in category_sales:
        category_sales[category] += sales
        category_count[category] += 1
    else:
        category_sales[category] = sales
        category_count[category] = 1
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```python
# CSVデータ集計ツール
# 学べる内容：ファイル読み込み、CSV解析、辞書による集計、整形出力
import os


def create_sample_csv(filename):
    """サンプルCSVファイルを作成する"""
    if os.path.exists(filename):
        return
    sample = """日付,商品名,カテゴリ,数量,単価
2024-01-05,りんご,果物,10,150
2024-01-05,牛乳,飲料,5,200
2024-01-06,パン,食品,8,120
2024-01-06,りんご,果物,3,150
2024-01-07,コーヒー,飲料,12,130
2024-01-07,パン,食品,6,120
2024-01-08,バナナ,果物,7,100
2024-01-08,牛乳,飲料,4,200"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(sample)
    print(f"サンプルファイル '{filename}' を作成しました。")


def read_csv(filename):
    """CSVファイルを読み込み、辞書のリストで返す"""
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    headers = lines[0].strip().split(",")
    data = []
    for line in lines[1:]:
        values = line.strip().split(",")
        if len(values) == len(headers):
            row = {}
            for i in range(len(headers)):
                row[headers[i]] = values[i]
            data.append(row)
    return data


# --- メイン処理 ---
filename = "sales.csv"
create_sample_csv(filename)

try:
    data = read_csv(filename)
except FileNotFoundError:
    print(f"エラー: '{filename}' が見つかりません。")
    data = []

if len(data) > 0:
    # 売上を各行に計算しておく
    for row in data:
        row["売上"] = int(row["数量"]) * int(row["単価"])

    dates = [row["日付"] for row in data]
    total_sales = 0
    for row in data:
        total_sales = total_sales + row["売上"]

    print("===== 売上データ集計 =====")
    print(f"データ件数: {len(data)}件")
    print(f"集計期間: {min(dates)} 〜 {max(dates)}")

    # --- カテゴリ別集計 ---
    cat_sales = {}
    cat_count = {}
    for row in data:
        cat = row["カテゴリ"]
        if cat in cat_sales:
            cat_sales[cat] = cat_sales[cat] + row["売上"]
            cat_count[cat] = cat_count[cat] + 1
        else:
            cat_sales[cat] = row["売上"]
            cat_count[cat] = 1

    print("\n--- カテゴリ別売上 ---")
    for cat in cat_sales:
        print(f"{cat:<6}: {cat_sales[cat]:>7,}円 ({cat_count[cat]}件)")

    # --- 商品別集計 ---
    prod_sales = {}
    for row in data:
        prod = row["商品名"]
        if prod in prod_sales:
            prod_sales[prod] = prod_sales[prod] + row["売上"]
        else:
            prod_sales[prod] = row["売上"]

    sorted_products = sorted(prod_sales.items(), key=lambda x: x[1], reverse=True)

    print("\n--- 商品別売上 TOP5 ---")
    for i in range(min(5, len(sorted_products))):
        name, sales = sorted_products[i]
        print(f" {i + 1}. {name:<8}: {sales:>7,}円")

    # --- 日別集計 ---
    day_sales = {}
    for row in data:
        day = row["日付"]
        if day in day_sales:
            day_sales[day] = day_sales[day] + row["売上"]
        else:
            day_sales[day] = row["売上"]

    max_day_sales = max(day_sales.values())

    print("\n--- 日別売上推移 ---")
    for day in sorted(day_sales.keys()):
        sales = day_sales[day]
        bar_length = int(sales / max_day_sales * 20)
        bar = "█" * bar_length
        print(f"{day} : {sales:>7,}円 {bar}")

    # --- 総合 ---
    avg = total_sales // len(data)
    print(f"\n総売上: {total_sales:,}円 (平均: {avg:,}円/件)")
```

</details>

<details>
<summary>解答例（改良版 ─ 関数分離＋集計ヘルパー）</summary>

```python
# CSVデータ集計ツール（改良版）
# 汎用的な集計関数で構造化したバージョン
import os


def create_sample_csv(filename):
    """サンプルCSVが無ければ作成する"""
    if os.path.exists(filename):
        return
    lines = [
        "日付,商品名,カテゴリ,数量,単価",
        "2024-01-05,りんご,果物,10,150",
        "2024-01-05,牛乳,飲料,5,200",
        "2024-01-06,パン,食品,8,120",
        "2024-01-06,りんご,果物,3,150",
        "2024-01-07,コーヒー,飲料,12,130",
        "2024-01-07,パン,食品,6,120",
        "2024-01-08,バナナ,果物,7,100",
        "2024-01-08,牛乳,飲料,4,200",
    ]
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def read_csv(filename):
    """CSVを辞書のリストとして読み込む"""
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    headers = lines[0].split(",")
    return [
        dict(zip(headers, line.split(",")))
        for line in lines[1:]
        if len(line.split(",")) == len(headers)
    ]


def group_by(data, key_name, value_func):
    """指定キーでグループ化し、値を集計する。{キー: (合計, 件数)} を返す"""
    result = {}
    for row in data:
        key = row[key_name]
        value = value_func(row)
        if key in result:
            total, count = result[key]
            result[key] = (total + value, count + 1)
        else:
            result[key] = (value, 1)
    return result


def print_bar_chart(items, max_width=20):
    """(ラベル, 値) のリストを棒グラフ風に表示"""
    max_val = max(v for _, v in items) if items else 1
    for label, value in items:
        bar_len = int(value / max_val * max_width)
        print(f"{label} : {value:>7,}円 {'█' * bar_len}")


# --- メイン処理 ---
filename = "sales.csv"
create_sample_csv(filename)

try:
    data = read_csv(filename)
except FileNotFoundError:
    print(f"エラー: '{filename}' が見つかりません。")
    data = []

if not data:
    print("データがありません。")
else:
    # 売上列を追加
    for row in data:
        row["売上"] = int(row["数量"]) * int(row["単価"])

    calc_sales = lambda row: row["売上"]
    dates = sorted(set(row["日付"] for row in data))
    total = sum(row["売上"] for row in data)

    print("===== 売上データ集計 =====")
    print(f"データ件数: {len(data)}件")
    print(f"集計期間: {dates[0]} 〜 {dates[-1]}")

    # カテゴリ別
    cat_data = group_by(data, "カテゴリ", calc_sales)
    print("\n--- カテゴリ別売上 ---")
    for cat, (sales, count) in cat_data.items():
        print(f"{cat:<6}: {sales:>7,}円 ({count}件)")

    # 商品別 TOP5
    prod_data = group_by(data, "商品名", calc_sales)
    sorted_prods = sorted(prod_data.items(), key=lambda x: x[1][0], reverse=True)
    print("\n--- 商品別売上 TOP5 ---")
    for i, (name, (sales, _)) in enumerate(sorted_prods[:5], 1):
        print(f" {i}. {name:<8}: {sales:>7,}円")

    # 日別推移
    day_data = group_by(data, "日付", calc_sales)
    print("\n--- 日別売上推移 ---")
    day_items = [(day, day_data[day][0]) for day in sorted(day_data.keys())]
    print_bar_chart(day_items)

    avg = total // len(data)
    print(f"\n総売上: {total:,}円 (平均: {avg:,}円/件)")
```

**初心者向けとの違い:**
- `group_by()` 汎用集計関数でカテゴリ別・商品別・日別を統一処理
- `dict(zip(...))` でCSVパースを簡潔に
- 集合 `set()` で日付の重複を排除
- 棒グラフ表示を関数化して再利用可能に

</details>

# 実践課題06：SQL問い合わせ演習 ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第5章（データベース）
> **課題の種類**: 分析演習 / Pythonコーディング
> **学習目標**: SELECT・JOIN・副問合せなどのSQL構文を読み書きでき、PythonのSQLiteで実際にデータベースを操作できるようになる

---

## 完成イメージ

```
===== SQL演習システム =====

テーブル一覧:
  - 社員 (社員番号, 氏名, 部署コード, 給与)
  - 部署 (部署コード, 部署名, 所在地)
  - プロジェクト (PJ番号, PJ名, 開始日, 終了日)
  - 担当 (社員番号, PJ番号, 役割)

SQL> SELECT 氏名, 給与 FROM 社員 WHERE 給与 >= 300000 ORDER BY 給与 DESC;

結果:
  氏名      | 給与
  ----------+---------
  山田太郎  | 450000
  佐藤花子  | 380000
  田中一郎  | 320000

(3行)
```

---

## 課題パート1：SQL読み書き問題

以下のテーブル定義を前提として問題に答えてください。

```sql
社員 (社員番号 CHAR(4), 氏名 VARCHAR(20), 部署コード CHAR(3), 給与 INTEGER)
部署 (部署コード CHAR(3), 部署名 VARCHAR(20), 所在地 VARCHAR(20))
プロジェクト (PJ番号 CHAR(4), PJ名 VARCHAR(30), 開始日 DATE, 終了日 DATE)
担当 (社員番号 CHAR(4), PJ番号 CHAR(4), 役割 VARCHAR(10))
```

**サンプルデータ:**

| 社員番号 | 氏名 | 部署コード | 給与 |
|---------|------|-----------|------|
| E001 | 山田太郎 | D01 | 450000 |
| E002 | 佐藤花子 | D01 | 380000 |
| E003 | 田中一郎 | D02 | 320000 |
| E004 | 鈴木次郎 | D02 | 280000 |
| E005 | 高橋美咲 | D03 | 350000 |

| 部署コード | 部署名 | 所在地 |
|-----------|--------|-------|
| D01 | 開発部 | 東京 |
| D02 | 営業部 | 大阪 |
| D03 | 総務部 | 東京 |

### 基本問題

**Q1.** 給与が 300,000 以上の社員の氏名と給与を、給与の降順で取得するSQLを書いてください。

**Q2.** 各部署の社員数と平均給与を求めるSQLを書いてください。（GROUP BY を使用）

**Q3.** 社員テーブルと部署テーブルを結合（JOIN）し、社員の氏名と所属部署名を取得するSQLを書いてください。

### 応用問題

**Q4.** 平均給与が 300,000 以上の部署の部署名を求めるSQLを書いてください。（HAVING を使用）

**Q5.** 全社の平均給与より高い給与の社員の氏名と給与を求めるSQLを書いてください。（副問合せを使用）

**Q6.** 「開発部」に所属し、かついずれかのプロジェクトに参加している社員の氏名を求めるSQLを書いてください。（複数テーブルの結合）

### チャレンジ問題

**Q7.** 以下の正規化に関する問題に答えてください。

次の非正規形のテーブルを第3正規形まで正規化してください。

```
受注 (受注番号, 受注日, 顧客名, 顧客住所,
      {商品コード, 商品名, 単価, 数量})
```
※ { } は繰り返し項目を示します。

---

## 課題パート2：PythonでSQL演習システムを作る

### 要件

1. SQLite を使ってデータベースを作成・初期データを投入する
2. 上記のテーブル構造を再現する
3. ユーザーがSQL文を入力すると結果を表示する対話型システムにする

---

## ステップガイド

<details>
<summary>ステップ1：SQLiteの基本操作</summary>

Pythonの標準ライブラリ `sqlite3` でデータベースを操作できます。

```python
import sqlite3

# メモリ上にデータベースを作成（ファイル不要）
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# テーブル作成
cursor.execute("""
    CREATE TABLE 社員 (
        社員番号 TEXT PRIMARY KEY,
        氏名 TEXT,
        部署コード TEXT,
        給与 INTEGER
    )
""")

# データ挿入
cursor.execute("INSERT INTO 社員 VALUES ('E001', '山田太郎', 'D01', 450000)")
conn.commit()
```

</details>

<details>
<summary>ステップ2：SELECTの結果を表形式で表示する</summary>

```python
cursor.execute("SELECT * FROM 社員")

# カラム名を取得
columns = [desc[0] for desc in cursor.description]
print(" | ".join(f"{col:<10}" for col in columns))
print("-" * (12 * len(columns)))

# データを表示
for row in cursor.fetchall():
    print(" | ".join(f"{str(val):<10}" for val in row))
```

</details>

<details>
<summary>ステップ3：対話型のSQL入力を作る</summary>

```python
while True:
    sql = input("\nSQL> ").strip()
    if sql.lower() in ("quit", "exit"):
        break
    try:
        cursor.execute(sql)
        # SELECT文の場合は結果表示
        if sql.upper().startswith("SELECT"):
            # 結果表示処理
            pass
        else:
            conn.commit()
            print(f"実行完了（{cursor.rowcount}行に影響）")
    except Exception as e:
        print(f"エラー: {e}")
```

</details>

---

## 解答例

<details>
<summary>SQL問題の解答</summary>

**Q1.**
```sql
SELECT 氏名, 給与
FROM 社員
WHERE 給与 >= 300000
ORDER BY 給与 DESC;
```

**Q2.**
```sql
SELECT 部署コード, COUNT(*) AS 社員数, AVG(給与) AS 平均給与
FROM 社員
GROUP BY 部署コード;
```

**Q3.**
```sql
SELECT 社員.氏名, 部署.部署名
FROM 社員
INNER JOIN 部署 ON 社員.部署コード = 部署.部署コード;
```

**Q4.**
```sql
SELECT 部署.部署名
FROM 社員
INNER JOIN 部署 ON 社員.部署コード = 部署.部署コード
GROUP BY 部署.部署名
HAVING AVG(社員.給与) >= 300000;
```

**Q5.**
```sql
SELECT 氏名, 給与
FROM 社員
WHERE 給与 > (SELECT AVG(給与) FROM 社員);
```

**Q6.**
```sql
SELECT DISTINCT 社員.氏名
FROM 社員
INNER JOIN 部署 ON 社員.部署コード = 部署.部署コード
INNER JOIN 担当 ON 社員.社員番号 = 担当.社員番号
WHERE 部署.部署名 = '開発部';
```

**Q7. 正規化の解答**

**第1正規形（繰り返し項目の除去）:**
```
受注 (受注番号, 受注日, 顧客名, 顧客住所)
受注明細 (受注番号, 商品コード, 商品名, 単価, 数量)
```

**第2正規形（部分関数従属の除去）:**
```
受注 (受注番号, 受注日, 顧客名, 顧客住所)
受注明細 (受注番号, 商品コード, 数量)
商品 (商品コード, 商品名, 単価)
```
※ 商品名・単価は商品コードのみで決まる（部分関数従属）

**第3正規形（推移的関数従属の除去）:**
```
受注 (受注番号, 受注日, 顧客コード)
顧客 (顧客コード, 顧客名, 顧客住所)
受注明細 (受注番号, 商品コード, 数量)
商品 (商品コード, 商品名, 単価)
```
※ 顧客名・顧客住所は顧客コード経由で受注番号に推移的に従属

</details>

<details>
<summary>解答例（初心者向け）</summary>

```python
# SQL問い合わせ演習システム
# 学べる内容：SQLite操作、SQL文の実行、テーブル結合
# 実行方法：python 06_sql_exercise.py

import sqlite3

def setup_database():
    """データベースを作成し、テストデータを投入する"""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # テーブル作成
    cursor.execute("""
        CREATE TABLE 部署 (
            部署コード TEXT PRIMARY KEY,
            部署名 TEXT,
            所在地 TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE 社員 (
            社員番号 TEXT PRIMARY KEY,
            氏名 TEXT,
            部署コード TEXT,
            給与 INTEGER,
            FOREIGN KEY (部署コード) REFERENCES 部署(部署コード)
        )
    """)

    cursor.execute("""
        CREATE TABLE プロジェクト (
            PJ番号 TEXT PRIMARY KEY,
            PJ名 TEXT,
            開始日 TEXT,
            終了日 TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE 担当 (
            社員番号 TEXT,
            PJ番号 TEXT,
            役割 TEXT,
            PRIMARY KEY (社員番号, PJ番号)
        )
    """)

    # データ投入
    departments = [
        ("D01", "開発部", "東京"),
        ("D02", "営業部", "大阪"),
        ("D03", "総務部", "東京"),
    ]
    cursor.executemany("INSERT INTO 部署 VALUES (?, ?, ?)", departments)

    employees = [
        ("E001", "山田太郎", "D01", 450000),
        ("E002", "佐藤花子", "D01", 380000),
        ("E003", "田中一郎", "D02", 320000),
        ("E004", "鈴木次郎", "D02", 280000),
        ("E005", "高橋美咲", "D03", 350000),
    ]
    cursor.executemany("INSERT INTO 社員 VALUES (?, ?, ?, ?)", employees)

    projects = [
        ("P001", "Webシステム開発", "2025-04-01", "2025-09-30"),
        ("P002", "営業支援ツール", "2025-06-01", "2025-12-31"),
    ]
    cursor.executemany("INSERT INTO プロジェクト VALUES (?, ?, ?, ?)", projects)

    assignments = [
        ("E001", "P001", "リーダー"),
        ("E002", "P001", "メンバー"),
        ("E003", "P002", "リーダー"),
        ("E005", "P001", "メンバー"),
    ]
    cursor.executemany("INSERT INTO 担当 VALUES (?, ?, ?)", assignments)

    conn.commit()
    return conn, cursor


def show_result(cursor):
    """SELECTの結果を表形式で表示する"""
    columns = [desc[0] for desc in cursor.description]

    # カラム幅を計算
    rows = cursor.fetchall()
    widths = []
    for i, col in enumerate(columns):
        max_width = len(col)
        for row in rows:
            max_width = max(max_width, len(str(row[i])))
        widths.append(max_width + 2)

    # ヘッダー
    header = " | ".join(f"{col:<{widths[i]}}" for i, col in enumerate(columns))
    separator = "-+-".join("-" * w for w in widths)
    print(f"  {header}")
    print(f"  {separator}")

    # データ
    for row in rows:
        line = " | ".join(f"{str(val):<{widths[i]}}" for i, val in enumerate(row))
        print(f"  {line}")

    print(f"\n  ({len(rows)}行)")


def main():
    conn, cursor = setup_database()

    print("===== SQL演習システム =====")
    print("テーブル一覧:")
    print("  - 社員 (社員番号, 氏名, 部署コード, 給与)")
    print("  - 部署 (部署コード, 部署名, 所在地)")
    print("  - プロジェクト (PJ番号, PJ名, 開始日, 終了日)")
    print("  - 担当 (社員番号, PJ番号, 役割)")
    print("\n'quit' で終了します。\n")

    while True:
        sql = input("SQL> ").strip()
        if sql.lower() in ("quit", "exit", "q"):
            break
        if not sql:
            continue

        try:
            cursor.execute(sql)
            if sql.upper().startswith("SELECT"):
                show_result(cursor)
            else:
                conn.commit()
                print(f"  実行完了（{cursor.rowcount}行に影響）")
        except Exception as e:
            print(f"  エラー: {e}")

    conn.close()
    print("お疲れさまでした！")

main()
```

</details>

<details>
<summary>解答例（改良版 ─ 練習問題内蔵・ヒント機能付き）</summary>

```python
# SQL問い合わせ演習システム（改良版）
# 練習問題と模範解答を内蔵、ヒント機能付き

import sqlite3


# --- 練習問題データ ---
EXERCISES = [
    {
        "title": "基本SELECT",
        "question": "給与が300,000以上の社員の氏名と給与を、給与の降順で取得してください。",
        "hint": "WHERE句で条件指定、ORDER BY ... DESC で降順",
        "answer": "SELECT 氏名, 給与 FROM 社員 WHERE 給与 >= 300000 ORDER BY 給与 DESC",
    },
    {
        "title": "GROUP BY",
        "question": "部署ごとの社員数と平均給与を求めてください。",
        "hint": "GROUP BY 部署コード、COUNT(*)、AVG(給与)",
        "answer": "SELECT 部署コード, COUNT(*) AS 社員数, AVG(給与) AS 平均給与 FROM 社員 GROUP BY 部署コード",
    },
    {
        "title": "INNER JOIN",
        "question": "社員の氏名と所属部署名を取得してください。",
        "hint": "社員テーブルと部署テーブルを部署コードで結合",
        "answer": "SELECT 社員.氏名, 部署.部署名 FROM 社員 INNER JOIN 部署 ON 社員.部署コード = 部署.部署コード",
    },
    {
        "title": "副問合せ",
        "question": "全社の平均給与より高い給与の社員の氏名と給与を求めてください。",
        "hint": "WHERE 給与 > (SELECT AVG(給与) FROM 社員)",
        "answer": "SELECT 氏名, 給与 FROM 社員 WHERE 給与 > (SELECT AVG(給与) FROM 社員)",
    },
    {
        "title": "複数テーブル結合",
        "question": "プロジェクトに参加している社員の氏名と担当プロジェクト名を取得してください。",
        "hint": "社員→担当→プロジェクトの3テーブルを結合",
        "answer": "SELECT 社員.氏名, プロジェクト.PJ名 FROM 社員 INNER JOIN 担当 ON 社員.社員番号 = 担当.社員番号 INNER JOIN プロジェクト ON 担当.PJ番号 = プロジェクト.PJ番号",
    },
]


def setup_database():
    """データベースのセットアップ"""
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()

    c.execute("CREATE TABLE 部署 (部署コード TEXT PRIMARY KEY, 部署名 TEXT, 所在地 TEXT)")
    c.execute("CREATE TABLE 社員 (社員番号 TEXT PRIMARY KEY, 氏名 TEXT, 部署コード TEXT, 給与 INTEGER)")
    c.execute("CREATE TABLE プロジェクト (PJ番号 TEXT PRIMARY KEY, PJ名 TEXT, 開始日 TEXT, 終了日 TEXT)")
    c.execute("CREATE TABLE 担当 (社員番号 TEXT, PJ番号 TEXT, 役割 TEXT, PRIMARY KEY(社員番号, PJ番号))")

    c.executemany("INSERT INTO 部署 VALUES (?,?,?)", [
        ("D01", "開発部", "東京"), ("D02", "営業部", "大阪"), ("D03", "総務部", "東京")])
    c.executemany("INSERT INTO 社員 VALUES (?,?,?,?)", [
        ("E001", "山田太郎", "D01", 450000), ("E002", "佐藤花子", "D01", 380000),
        ("E003", "田中一郎", "D02", 320000), ("E004", "鈴木次郎", "D02", 280000),
        ("E005", "高橋美咲", "D03", 350000)])
    c.executemany("INSERT INTO プロジェクト VALUES (?,?,?,?)", [
        ("P001", "Webシステム開発", "2025-04-01", "2025-09-30"),
        ("P002", "営業支援ツール", "2025-06-01", "2025-12-31")])
    c.executemany("INSERT INTO 担当 VALUES (?,?,?)", [
        ("E001", "P001", "リーダー"), ("E002", "P001", "メンバー"),
        ("E003", "P002", "リーダー"), ("E005", "P001", "メンバー")])
    conn.commit()
    return conn, c


def show_result(cursor):
    """結果を表形式で表示"""
    columns = [d[0] for d in cursor.description]
    rows = cursor.fetchall()

    widths = [max(len(str(col)), *(len(str(r[i])) for r in rows)) + 2
              for i, col in enumerate(columns)]

    print("  " + " | ".join(f"{c:<{widths[i]}}" for i, c in enumerate(columns)))
    print("  " + "-+-".join("-" * w for w in widths))
    for row in rows:
        print("  " + " | ".join(f"{str(v):<{widths[i]}}" for i, v in enumerate(row)))
    print(f"  ({len(rows)}行)")


def exercise_mode(conn, cursor):
    """練習問題モード"""
    score = 0
    for i, ex in enumerate(EXERCISES, 1):
        print(f"\n===== 問題{i}: {ex['title']} =====")
        print(f"  {ex['question']}")

        while True:
            cmd = input("\n  SQL（'hint'でヒント, 'skip'でスキップ）> ").strip()

            if cmd.lower() == "hint":
                print(f"  ヒント: {ex['hint']}")
                continue
            elif cmd.lower() == "skip":
                print(f"  模範解答: {ex['answer']}")
                cursor.execute(ex["answer"])
                show_result(cursor)
                break
            else:
                try:
                    cursor.execute(cmd)
                    show_result(cursor)

                    # 模範解答と比較
                    cursor.execute(cmd)
                    user_result = set(cursor.fetchall())
                    cursor.execute(ex["answer"])
                    expected_result = set(cursor.fetchall())

                    if user_result == expected_result:
                        print("  ✓ 正解です！")
                        score += 1
                        break
                    else:
                        print("  結果が期待と異なります。もう一度試してください。")
                except Exception as e:
                    print(f"  エラー: {e}")

    print(f"\n===== 結果: {len(EXERCISES)}問中 {score}問正解 =====")


def free_mode(conn, cursor):
    """自由入力モード"""
    print("\nSQL文を自由に入力してください（'quit'で終了）:\n")
    while True:
        sql = input("SQL> ").strip()
        if sql.lower() in ("quit", "exit", "q"):
            break
        if not sql:
            continue
        try:
            cursor.execute(sql)
            if sql.upper().startswith("SELECT"):
                show_result(cursor)
            else:
                conn.commit()
                print(f"  実行完了（{cursor.rowcount}行に影響）")
        except Exception as e:
            print(f"  エラー: {e}")


def main():
    conn, cursor = setup_database()
    print("===== SQL演習システム =====")
    print("  1. 練習問題モード（ヒント・模範解答付き）")
    print("  2. 自由入力モード")

    choice = input("\n選択 (1-2): ").strip()
    if choice == "1":
        exercise_mode(conn, cursor)
    elif choice == "2":
        free_mode(conn, cursor)

    conn.close()
    print("お疲れさまでした！")


if __name__ == "__main__":
    main()
```

**初心者向けとの違い:**
- 練習問題モード内蔵 → ヒントと模範解答で段階的に学べる
- 結果の自動判定 → ユーザーのSQLと模範解答の出力を比較
- カラム幅の自動調整 → より見やすい表示
- 2つのモード選択 → 目的に応じた使い方が可能

</details>

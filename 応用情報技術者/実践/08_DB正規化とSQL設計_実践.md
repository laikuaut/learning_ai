# 実践課題08：データベース正規化とSQL設計 ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第3章（データベース応用）
> **課題の種類**: 設計課題 / 分析演習
> **学習目標**: 非正規形のテーブルを第3正規形まで正規化し、適切なSQL文を設計できるようになる。午後問題の典型パターンに対応する力を養う

---

## 完成イメージ

非正規形のデータから正規化を段階的に進め、最終的にE-R図とCREATE TABLE文を完成させます。

```
===== DB正規化シミュレータ =====

--- 非正規形（元データ） ---
受注番号 | 受注日     | 顧客名      | 商品1    | 数量1 | 商品2    | 数量2 | 商品3  | 数量3
J001     | 2025-04-01 | A商事       | ボールペン| 100   | ノート   | 50    | 消しゴム| 200

→ 繰り返し項目あり（商品・数量の組が複数）

--- 第1正規形 ---
受注番号 | 受注日     | 顧客名 | 商品名    | 数量
J001     | 2025-04-01 | A商事  | ボールペン | 100
J001     | 2025-04-01 | A商事  | ノート    | 50
J001     | 2025-04-01 | A商事  | 消しゴム  | 200

→ 部分関数従属あり（顧客名は受注番号のみに依存）

--- 第2正規形 ---
[受注テーブル] 受注番号(PK), 受注日, 顧客名
[受注明細テーブル] 受注番号(FK), 商品名(PK), 数量

--- 第3正規形 ---
推移的関数従属の除去が必要な場合、さらにテーブルを分割
```

---

## 課題の要件

### パート1：正規化演習（筆記）

以下の非正規形テーブルを第3正規形まで正規化してください。

**テーブル：社員研修記録**

| 社員番号 | 社員名 | 部署コード | 部署名 | 研修コード1 | 研修名1 | 受講日1 | 成績1 | 研修コード2 | 研修名2 | 受講日2 | 成績2 |
|---------|--------|-----------|--------|-----------|--------|---------|------|-----------|--------|---------|------|
| E001 | 田中太郎 | D10 | 営業部 | T01 | ビジネスマナー | 2025-04-10 | A | T03 | セキュリティ基礎 | 2025-05-15 | B |
| E002 | 鈴木花子 | D20 | 開発部 | T02 | Python入門 | 2025-04-20 | A | T03 | セキュリティ基礎 | 2025-05-15 | A |
| E003 | 佐藤一郎 | D10 | 営業部 | T01 | ビジネスマナー | 2025-04-10 | B | - | - | - | - |

**課題1:** 関数従属性を全て洗い出してください。
**課題2:** 第1正規形にしてください（繰り返し項目の排除）。
**課題3:** 第2正規形にしてください（部分関数従属の排除）。
**課題4:** 第3正規形にしてください（推移的関数従属の排除）。
**課題5:** E-R図を描いてください。

---

### パート2：SQL設計演習

正規化後のテーブルに対して以下のSQLを作成してください。

1. テーブル定義（CREATE TABLE）
2. 「営業部の社員が受講した研修の一覧（社員名、研修名、成績）」を取得するSELECT文
3. 「研修ごとの受講者数と平均成績」を集計するSELECT文
4. 「まだ研修を1つも受講していない社員」を抽出するSELECT文

---

### パート3：Pythonコーディング

SQLiteを使って正規化後のテーブルを作成し、データを投入して上記のクエリを実行するプログラムを作成してください。

---

## ステップガイド

<details>
<summary>パート1のステップ1：関数従属性の分析</summary>

関数従属性（Functional Dependency）とは、「Aの値が決まればBの値が一意に決まる」関係（A → B）のことです。

```
社員番号 → 社員名, 部署コード
部署コード → 部署名
研修コード → 研修名
{社員番号, 研修コード} → 受講日, 成績
```

ポイント:
- 主キー全体に依存しているか（完全関数従属）？
- 主キーの一部にだけ依存していないか（部分関数従属）？
- 非キー属性が別の非キー属性に依存していないか（推移的関数従属）？

</details>

<details>
<summary>パート1のステップ2：正規化の手順</summary>

```
[非正規形] 繰り返し項目あり
    ↓ 繰り返し項目を行に展開
[第1正規形(1NF)] 全ての属性が原子値
    ↓ 部分関数従属を除去
[第2正規形(2NF)] 完全関数従属のみ
    ↓ 推移的関数従属を除去
[第3正規形(3NF)] 推移的関数従属なし
```

</details>

---

## 解答例

<details>
<summary>パート1：正規化の解答</summary>

**課題1：関数従属性**

```
社員番号 → 社員名, 部署コード       （社員が決まれば名前と部署が決まる）
部署コード → 部署名                  （部署コードが決まれば部署名が決まる）
研修コード → 研修名                  （研修コードが決まれば研修名が決まる）
{社員番号, 研修コード} → 受講日, 成績  （社員と研修の組で受講情報が決まる）
```

**課題2：第1正規形（1NF）**

繰り返し項目（研修コード1/2...）を排除し、1行1レコードにします。

| 社員番号 | 社員名 | 部署コード | 部署名 | 研修コード | 研修名 | 受講日 | 成績 |
|---------|--------|-----------|--------|-----------|--------|--------|------|
| E001 | 田中太郎 | D10 | 営業部 | T01 | ビジネスマナー | 2025-04-10 | A |
| E001 | 田中太郎 | D10 | 営業部 | T03 | セキュリティ基礎 | 2025-05-15 | B |
| E002 | 鈴木花子 | D20 | 開発部 | T02 | Python入門 | 2025-04-20 | A |
| E002 | 鈴木花子 | D20 | 開発部 | T03 | セキュリティ基礎 | 2025-05-15 | A |
| E003 | 佐藤一郎 | D10 | 営業部 | T01 | ビジネスマナー | 2025-04-10 | B |

主キー: {社員番号, 研修コード}

**課題3：第2正規形（2NF）**

部分関数従属を除去します。

- 社員番号 → 社員名, 部署コード（主キーの一部のみに依存）→ 分離
- 研修コード → 研修名（主キーの一部のみに依存）→ 分離

```
[社員テーブル]
  社員番号(PK), 社員名, 部署コード

[研修テーブル]
  研修コード(PK), 研修名

[受講記録テーブル]
  社員番号(PK,FK), 研修コード(PK,FK), 受講日, 成績
```

**課題4：第3正規形（3NF）**

推移的関数従属を除去します。

- 社員番号 → 部署コード → 部署名（推移的関数従属）→ 部署テーブルを分離

```
[社員テーブル]
  社員番号(PK), 社員名, 部署コード(FK)

[部署テーブル]
  部署コード(PK), 部署名

[研修テーブル]
  研修コード(PK), 研修名

[受講記録テーブル]
  社員番号(PK,FK), 研修コード(PK,FK), 受講日, 成績
```

**課題5：E-R図**

```
┌──────┐    ┌──────────┐    ┌──────┐
│ 部署  │1  N│   社員    │    │ 研修  │
│      ├───→│         │    │      │
│部署CD │    │社員番号   │    │研修CD │
│部署名  │    │社員名    │    │研修名  │
└──────┘    │部署CD(FK)│    └──┬───┘
             └────┬─────┘       │
                  │N           │N
                  └──┐     ┌──┘
                     ↓     ↓
                ┌──────────────┐
                │  受講記録     │
                │社員番号(FK)  │
                │研修CD(FK)   │
                │受講日        │
                │成績          │
                └──────────────┘
```

</details>

<details>
<summary>パート2：SQL文の解答</summary>

**1. CREATE TABLE文**

```sql
CREATE TABLE departments (
    dept_code VARCHAR(10) PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL
);

CREATE TABLE employees (
    emp_id VARCHAR(10) PRIMARY KEY,
    emp_name VARCHAR(50) NOT NULL,
    dept_code VARCHAR(10) NOT NULL,
    FOREIGN KEY (dept_code) REFERENCES departments(dept_code)
);

CREATE TABLE trainings (
    training_code VARCHAR(10) PRIMARY KEY,
    training_name VARCHAR(100) NOT NULL
);

CREATE TABLE training_records (
    emp_id VARCHAR(10),
    training_code VARCHAR(10),
    attend_date DATE NOT NULL,
    grade CHAR(1) NOT NULL,
    PRIMARY KEY (emp_id, training_code),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
    FOREIGN KEY (training_code) REFERENCES trainings(training_code)
);
```

**2. 営業部の社員が受講した研修の一覧**

```sql
SELECT e.emp_name, t.training_name, r.grade
FROM employees e
INNER JOIN training_records r ON e.emp_id = r.emp_id
INNER JOIN trainings t ON r.training_code = t.training_code
INNER JOIN departments d ON e.dept_code = d.dept_code
WHERE d.dept_name = '営業部'
ORDER BY e.emp_name, r.attend_date;
```

**3. 研修ごとの受講者数と平均成績**

```sql
SELECT t.training_name,
       COUNT(*) AS attendee_count,
       -- 成績をA=4, B=3, C=2, D=1に変換して平均
       AVG(CASE r.grade
           WHEN 'A' THEN 4 WHEN 'B' THEN 3
           WHEN 'C' THEN 2 WHEN 'D' THEN 1
       END) AS avg_grade_score
FROM trainings t
INNER JOIN training_records r ON t.training_code = r.training_code
GROUP BY t.training_code, t.training_name
ORDER BY attendee_count DESC;
```

**4. まだ研修を受講していない社員**

```sql
-- 方法1: NOT EXISTS
SELECT e.emp_id, e.emp_name
FROM employees e
WHERE NOT EXISTS (
    SELECT 1 FROM training_records r WHERE r.emp_id = e.emp_id
);

-- 方法2: LEFT JOIN + IS NULL
SELECT e.emp_id, e.emp_name
FROM employees e
LEFT JOIN training_records r ON e.emp_id = r.emp_id
WHERE r.emp_id IS NULL;
```

</details>

<details>
<summary>パート3：Pythonコーディングの解答（初心者向け）</summary>

```python
# DB正規化とSQL設計シミュレータ
# 学べる内容：正規化、SQLiteによるDB操作、JOIN、集計関数
# 実行方法：python db_normalization.py

import sqlite3

# --- データベース作成（メモリ上） ---
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# --- テーブル作成 ---
cursor.executescript("""
    CREATE TABLE departments (
        dept_code TEXT PRIMARY KEY,
        dept_name TEXT NOT NULL
    );

    CREATE TABLE employees (
        emp_id TEXT PRIMARY KEY,
        emp_name TEXT NOT NULL,
        dept_code TEXT NOT NULL,
        FOREIGN KEY (dept_code) REFERENCES departments(dept_code)
    );

    CREATE TABLE trainings (
        training_code TEXT PRIMARY KEY,
        training_name TEXT NOT NULL
    );

    CREATE TABLE training_records (
        emp_id TEXT,
        training_code TEXT,
        attend_date TEXT NOT NULL,
        grade TEXT NOT NULL,
        PRIMARY KEY (emp_id, training_code),
        FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
        FOREIGN KEY (training_code) REFERENCES trainings(training_code)
    );
""")

# --- データ投入 ---
cursor.executemany("INSERT INTO departments VALUES (?, ?)", [
    ("D10", "営業部"), ("D20", "開発部"), ("D30", "総務部"),
])

cursor.executemany("INSERT INTO employees VALUES (?, ?, ?)", [
    ("E001", "田中太郎", "D10"),
    ("E002", "鈴木花子", "D20"),
    ("E003", "佐藤一郎", "D10"),
    ("E004", "高橋次郎", "D30"),  # 研修未受講の社員
])

cursor.executemany("INSERT INTO trainings VALUES (?, ?)", [
    ("T01", "ビジネスマナー"),
    ("T02", "Python入門"),
    ("T03", "セキュリティ基礎"),
])

cursor.executemany("INSERT INTO training_records VALUES (?, ?, ?, ?)", [
    ("E001", "T01", "2025-04-10", "A"),
    ("E001", "T03", "2025-05-15", "B"),
    ("E002", "T02", "2025-04-20", "A"),
    ("E002", "T03", "2025-05-15", "A"),
    ("E003", "T01", "2025-04-10", "B"),
])

conn.commit()

# --- クエリ実行と結果表示 ---
print("===== DB正規化シミュレータ =====\n")

# 1. 営業部の社員が受講した研修
print("--- 営業部の社員が受講した研修 ---")
cursor.execute("""
    SELECT e.emp_name, t.training_name, r.grade
    FROM employees e
    INNER JOIN training_records r ON e.emp_id = r.emp_id
    INNER JOIN trainings t ON r.training_code = t.training_code
    INNER JOIN departments d ON e.dept_code = d.dept_code
    WHERE d.dept_name = '営業部'
    ORDER BY e.emp_name, r.attend_date
""")
print(f"{'社員名':<12} | {'研修名':<18} | 成績")
print("-" * 40)
for row in cursor.fetchall():
    print(f"{row[0]:<12} | {row[1]:<18} | {row[2]}")

# 2. 研修ごとの受講者数
print("\n--- 研修ごとの受講者数と平均成績 ---")
cursor.execute("""
    SELECT t.training_name, COUNT(*) as cnt,
           AVG(CASE r.grade
               WHEN 'A' THEN 4 WHEN 'B' THEN 3
               WHEN 'C' THEN 2 WHEN 'D' THEN 1
           END) as avg_score
    FROM trainings t
    INNER JOIN training_records r ON t.training_code = r.training_code
    GROUP BY t.training_code, t.training_name
    ORDER BY cnt DESC
""")
print(f"{'研修名':<18} | {'受講者数':>8} | {'平均成績':>8}")
print("-" * 45)
for row in cursor.fetchall():
    grade_map = {4: "A", 3: "B", 2: "C", 1: "D"}
    avg_display = f"{row[2]:.1f}"
    print(f"{row[0]:<18} | {row[1]:>8}名 | {avg_display:>8}")

# 3. 研修未受講の社員
print("\n--- 研修未受講の社員 ---")
cursor.execute("""
    SELECT e.emp_id, e.emp_name
    FROM employees e
    LEFT JOIN training_records r ON e.emp_id = r.emp_id
    WHERE r.emp_id IS NULL
""")
results = cursor.fetchall()
if results:
    for row in results:
        print(f"  {row[0]}: {row[1]}")
else:
    print("  全社員が何らかの研修を受講済みです。")

conn.close()
```

</details>

<details>
<summary>パート3：Pythonコーディングの解答（改良版 ─ 対話的操作付き）</summary>

```python
# DB正規化とSQL設計シミュレータ（改良版）
# 学べる内容：正規化、対話的SQL操作、データ整合性の確認
# 実行方法：python db_normalization_advanced.py

import sqlite3

def setup_database():
    """データベースのセットアップ"""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.executescript("""
        CREATE TABLE departments (
            dept_code TEXT PRIMARY KEY,
            dept_name TEXT NOT NULL UNIQUE
        );
        CREATE TABLE employees (
            emp_id TEXT PRIMARY KEY,
            emp_name TEXT NOT NULL,
            dept_code TEXT NOT NULL,
            FOREIGN KEY (dept_code) REFERENCES departments(dept_code)
        );
        CREATE TABLE trainings (
            training_code TEXT PRIMARY KEY,
            training_name TEXT NOT NULL
        );
        CREATE TABLE training_records (
            emp_id TEXT,
            training_code TEXT,
            attend_date TEXT NOT NULL,
            grade TEXT NOT NULL CHECK(grade IN ('A','B','C','D')),
            PRIMARY KEY (emp_id, training_code),
            FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
            FOREIGN KEY (training_code) REFERENCES trainings(training_code)
        );
    """)

    # サンプルデータ投入
    cursor.executemany("INSERT INTO departments VALUES (?,?)", [
        ("D10","営業部"),("D20","開発部"),("D30","総務部")])
    cursor.executemany("INSERT INTO employees VALUES (?,?,?)", [
        ("E001","田中太郎","D10"),("E002","鈴木花子","D20"),
        ("E003","佐藤一郎","D10"),("E004","高橋次郎","D30")])
    cursor.executemany("INSERT INTO trainings VALUES (?,?)", [
        ("T01","ビジネスマナー"),("T02","Python入門"),("T03","セキュリティ基礎")])
    cursor.executemany("INSERT INTO training_records VALUES (?,?,?,?)", [
        ("E001","T01","2025-04-10","A"),("E001","T03","2025-05-15","B"),
        ("E002","T02","2025-04-20","A"),("E002","T03","2025-05-15","A"),
        ("E003","T01","2025-04-10","B")])
    conn.commit()
    return conn

def show_tables(cursor):
    """テーブル構造を表示"""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        print(f"\n  [{table}]")
        for col in columns:
            pk = " (PK)" if col[5] else ""
            nullable = "" if col[3] else " NULL許可"
            print(f"    {col[1]:<20} {col[2]:<10}{pk}{nullable}")

def run_query(cursor, description, sql):
    """クエリを実行して結果を表示"""
    print(f"\n--- {description} ---")
    print(f"SQL: {sql}\n")
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    # ヘッダー
    header = " | ".join(f"{c:<15}" for c in columns)
    print(header)
    print("-" * len(header))
    for row in rows:
        print(" | ".join(f"{str(v):<15}" for v in row))
    print(f"\n({len(rows)}行)")

# --- メイン ---
print("===== DB正規化シミュレータ（改良版） =====\n")

conn = setup_database()
cursor = conn.cursor()

print("【テーブル構造（第3正規形）】")
show_tables(cursor)

# プリセットクエリ
queries = [
    ("全社員と所属部署",
     "SELECT e.emp_id, e.emp_name, d.dept_name FROM employees e JOIN departments d ON e.dept_code = d.dept_code"),
    ("営業部の受講研修一覧",
     "SELECT e.emp_name, t.training_name, r.grade, r.attend_date FROM employees e JOIN training_records r ON e.emp_id = r.emp_id JOIN trainings t ON r.training_code = t.training_code JOIN departments d ON e.dept_code = d.dept_code WHERE d.dept_name = '営業部'"),
    ("研修別受講者数",
     "SELECT t.training_name, COUNT(*) as count FROM trainings t JOIN training_records r ON t.training_code = r.training_code GROUP BY t.training_code ORDER BY count DESC"),
    ("研修未受講者",
     "SELECT e.emp_id, e.emp_name FROM employees e LEFT JOIN training_records r ON e.emp_id = r.emp_id WHERE r.emp_id IS NULL"),
]

print("\n\n【クエリ実行結果】")
for desc, sql in queries:
    run_query(cursor, desc, sql)

# 対話モード
print("\n\n--- 自由にSQLを実行できます（exitで終了） ---")
while True:
    sql = input("\nSQL> ").strip()
    if sql.lower() == "exit":
        break
    if not sql:
        continue
    try:
        cursor.execute(sql)
        if cursor.description:
            columns = [d[0] for d in cursor.description]
            rows = cursor.fetchall()
            print(" | ".join(columns))
            print("-" * 50)
            for row in rows:
                print(" | ".join(str(v) for v in row))
            print(f"({len(rows)}行)")
        else:
            conn.commit()
            print(f"実行完了（{cursor.rowcount}行に影響）")
    except Exception as e:
        print(f"エラー: {e}")

conn.close()
```

**初心者向けとの違い:**
- テーブル構造を自動表示し、正規化結果を確認できる
- 対話モードで自由にSQLを実行・検証できる
- PRAGMA foreign_keys を有効にし、外部キー制約を実際に検証可能
- CHECK制約など、データ整合性の仕組みも体験できる

</details>

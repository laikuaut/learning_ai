# 実践課題05：SQLインジェクション脆弱性分析 ★2

> **難易度**: ★★☆☆☆（基礎）
> **前提知識**: 第3章（データベース応用）、第5章（セキュリティ応用）
> **課題の種類**: 分析演習 / ケーススタディ
> **学習目標**: SQLインジェクションの原理を理解し、脆弱なコードの発見と安全なコードへの修正ができるようになる

---

## 完成イメージ

以下のような脆弱なコードを読み解き、攻撃手法を特定し、安全なコードに書き換える演習です。

```
===== SQLインジェクション脆弱性チェッカー =====

--- 脆弱なコード ---
query = "SELECT * FROM users WHERE name = '" + user_input + "'"

ユーザー入力をシミュレート: ' OR '1'='1

生成されるSQL:
  SELECT * FROM users WHERE name = '' OR '1'='1'

[危険] WHERE句が常にTRUEとなり、全レコードが取得されます。

--- 安全なコード（パラメータ化クエリ） ---
query = "SELECT * FROM users WHERE name = ?"
params = (user_input,)

生成される実行: パラメータ化により入力はリテラル値として処理されます。
[安全] SQLインジェクションは発生しません。
```

---

## 課題の要件

### パート1：脆弱性分析（コードリーディング）

以下の5つのコード断片を読み、それぞれ脆弱かどうかを判定し、攻撃方法を説明してください。

**コード1:**
```python
# ログイン処理
username = input("ユーザー名: ")
password = input("パスワード: ")
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
cursor.execute(query)
```

**コード2:**
```python
# 商品検索
search_word = input("検索ワード: ")
query = "SELECT * FROM products WHERE name LIKE ?"
cursor.execute(query, (f"%{search_word}%",))
```

**コード3:**
```python
# ユーザー削除
user_id = input("削除するユーザーID: ")
query = "DELETE FROM users WHERE id = " + user_id
cursor.execute(query)
```

**コード4:**
```python
# 並べ替え
sort_column = input("並べ替えカラム（name/price/date）: ")
allowed = ["name", "price", "date"]
if sort_column in allowed:
    query = f"SELECT * FROM products ORDER BY {sort_column}"
    cursor.execute(query)
```

**コード5:**
```python
# レポート生成
table_name = input("テーブル名: ")
query = f"SELECT COUNT(*) FROM {table_name}"
cursor.execute(query)
```

---

### パート2：Pythonコーディング

SQLインジェクションのシミュレータを作成してください。

1. 疑似SQLクエリを文字列連結で生成する「脆弱版」関数
2. パラメータ化クエリを模擬する「安全版」関数
3. 複数の攻撃パターンで両者の挙動を比較表示する

---

## ステップガイド

<details>
<summary>パート1の解答方針</summary>

各コードについて以下の観点でチェックしましょう。

1. ユーザー入力がSQL文に直接埋め込まれていないか？
2. パラメータ化クエリ（プレースホルダ `?` や `%s`）を使っているか？
3. 入力値のバリデーション（ホワイトリスト検証）はあるか？

```
脆弱性チェックフロー:
  ユーザー入力あり？
    → YES → SQL文に直接連結/埋め込み？
              → YES → パラメータ化されている？
                        → NO  → [脆弱]
                        → YES → [安全]
              → NO（ホワイトリスト等）→ [安全]
    → NO → [安全]
```

</details>

<details>
<summary>パート2のステップ1：脆弱版関数を作る</summary>

```python
def vulnerable_query(template, user_input):
    """脆弱なクエリ生成（文字列連結）"""
    return template.replace("{input}", user_input)
```

</details>

<details>
<summary>パート2のステップ2：安全版関数を作る</summary>

```python
def safe_query(template, user_input):
    """安全なクエリ生成（パラメータ化のシミュレーション）"""
    # 特殊文字をエスケープしてリテラル値として扱う
    escaped = user_input.replace("'", "''")
    return template, f"パラメータ: [{escaped}]"
```

</details>

---

## 解答例

<details>
<summary>パート1：脆弱性分析の解答</summary>

**コード1: 脆弱**
- 攻撃方法: ユーザー名に `' OR '1'='1' --` と入力すると、WHERE句が `username='' OR '1'='1' --' AND password='...'` となり、パスワードチェックがコメントアウトされて全ユーザーでログイン可能になります。
- 修正: `cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))`

**コード2: 安全**
- プレースホルダ `?` を使用し、`cursor.execute()` の第2引数でパラメータを渡しています。
- LIKE句の `%` はアプリケーション側で付与しており、SQL文自体にユーザー入力は直接埋め込まれていません。
- 注意: LIKE句の `%` や `_` のワイルドカードを悪用されるリスクは残りますが、SQLインジェクションではありません。

**コード3: 脆弱**
- 攻撃方法: IDに `1 OR 1=1` と入力すると `DELETE FROM users WHERE id = 1 OR 1=1` となり、全レコードが削除されます。
- さらに `1; DROP TABLE users` のような入力でテーブル自体を削除される可能性もあります。
- 修正: `cursor.execute("DELETE FROM users WHERE id = ?", (int(user_id),))`

**コード4: 安全**
- ホワイトリスト（`allowed`リスト）で許可されたカラム名のみを受け入れています。
- ユーザー入力が直接SQL文に入りますが、事前に固定値との一致を検証しているため安全です。
- ORDER BY句はパラメータ化できないため、このホワイトリスト方式が正しいアプローチです。

**コード5: 脆弱**
- 攻撃方法: テーブル名に `users; DROP TABLE users --` と入力するとテーブルが削除されます。
- テーブル名やカラム名はプレースホルダを使えないため、ホワイトリスト検証が必要です。
- 修正: `allowed_tables = ["users", "products", "orders"]` のようなホワイトリストで検証する。

</details>

<details>
<summary>パート2：シミュレータの解答（初心者向け）</summary>

```python
# SQLインジェクション脆弱性チェッカー
# 学べる内容：SQLインジェクションの原理と対策
# 実行方法：python sql_injection_checker.py

def build_vulnerable_query(base, field, user_input):
    """脆弱なクエリ生成（文字列連結）"""
    return f"{base} WHERE {field} = '{user_input}'"

def build_safe_query(base, field, user_input):
    """安全なクエリ生成（パラメータ化のシミュレーション）"""
    escaped = user_input.replace("'", "''")
    query = f"{base} WHERE {field} = ?"
    return query, escaped

# --- 攻撃パターン ---
attack_patterns = [
    ("通常入力", "tanaka"),
    ("常にTRUE", "' OR '1'='1"),
    ("UNION攻撃", "' UNION SELECT username, password FROM admin --"),
    ("テーブル削除", "'; DROP TABLE users --"),
    ("コメント攻撃", "admin'--"),
]

print("===== SQLインジェクション脆弱性チェッカー =====\n")

base_query = "SELECT * FROM users"
field = "name"

for label, payload in attack_patterns:
    print(f"--- {label} ---")
    print(f"入力値: {payload}\n")

    # 脆弱版
    vuln = build_vulnerable_query(base_query, field, payload)
    print(f"[脆弱] {vuln}")

    # 安全版
    safe_q, safe_p = build_safe_query(base_query, field, payload)
    print(f"[安全] {safe_q}")
    print(f"       パラメータ: [{safe_p}]")

    # 判定
    if "'" in payload and payload != payload.replace("'", ""):
        print("→ 脆弱版では特殊文字がSQL構文として解釈される危険があります")
        print("→ 安全版ではパラメータとして処理され、SQL構文に影響しません")
    print()
```

</details>

<details>
<summary>パート2：シミュレータの解答（改良版 ─ 詳細判定付き）</summary>

```python
# SQLインジェクション脆弱性チェッカー（改良版）
# 学べる内容：SQLインジェクションの分類、リスク評価
# 実行方法：python sql_injection_advanced.py

import re

def analyze_payload(payload):
    """攻撃ペイロードを分析し、攻撃種別とリスクレベルを返す"""
    risks = []

    if "OR" in payload.upper() and ("=" in payload or "1" in payload):
        risks.append(("認証バイパス", "高", "WHERE句を常にTRUEにする"))
    if "UNION" in payload.upper():
        risks.append(("UNIONインジェクション", "高", "他テーブルのデータを抽出"))
    if "DROP" in payload.upper() or "DELETE" in payload.upper():
        risks.append(("破壊的攻撃", "致命的", "テーブル/データの削除"))
    if "--" in payload or "/*" in payload:
        risks.append(("コメントインジェクション", "中", "SQL文の一部を無効化"))
    if ";" in payload:
        risks.append(("スタッキングクエリ", "高", "複数のSQL文を実行"))

    return risks

def build_vulnerable_query(base, field, user_input):
    return f"{base} WHERE {field} = '{user_input}'"

# --- 攻撃パターン ---
attack_patterns = [
    ("通常入力", "tanaka"),
    ("認証バイパス", "' OR '1'='1"),
    ("UNIONベース", "' UNION SELECT username, password FROM admin --"),
    ("スタッキング", "'; DROP TABLE users; --"),
    ("コメント攻撃", "admin'--"),
    ("数値型攻撃", "1 OR 1=1"),
    ("LIKE悪用", "%" ),
]

print("===== SQLインジェクション脆弱性分析ツール =====\n")

base_query = "SELECT * FROM users"
field = "name"

summary = {"安全": 0, "中": 0, "高": 0, "致命的": 0}

for label, payload in attack_patterns:
    print(f"{'='*50}")
    print(f"テストケース: {label}")
    print(f"ペイロード:   {payload}")

    vuln_query = build_vulnerable_query(base_query, field, payload)
    print(f"\n生成SQL: {vuln_query}")

    risks = analyze_payload(payload)
    if not risks:
        print("判定: [安全] 特殊な攻撃パターンは検出されませんでした")
        summary["安全"] += 1
    else:
        for risk_type, level, desc in risks:
            print(f"判定: [{level}] {risk_type} - {desc}")
            summary[level] = summary.get(level, 0) + 1
    print()

# --- サマリー ---
print("=" * 50)
print("テスト結果サマリー")
print(f"  安全: {summary.get('安全', 0)}件")
print(f"  中リスク: {summary.get('中', 0)}件")
print(f"  高リスク: {summary.get('高', 0)}件")
print(f"  致命的: {summary.get('致命的', 0)}件")
print()
print("対策:")
print("  1. パラメータ化クエリ（プレースホルダ）を必ず使用する")
print("  2. 入力値のバリデーション（型チェック、長さ制限）")
print("  3. データベースユーザーの権限を最小限にする（最小権限の原則）")
print("  4. WAF（Web Application Firewall）の導入")
```

**初心者向けとの違い:**
- 攻撃ペイロードを自動分析し、攻撃種別とリスクレベルを判定する機能を追加
- テスト結果のサマリーと対策を表示
- 実務的なセキュリティ評価の考え方を体験できる

</details>

---

## 確認問題

**問1:** 次のコードの脆弱性を指摘し、修正してください。
```python
page = input("ページ番号: ")
query = f"SELECT * FROM articles LIMIT 10 OFFSET {int(page) * 10}"
```

<details>
<summary>解答</summary>

一見 `int()` で数値変換しているため安全に見えますが、`int()` が失敗した場合の例外処理がありません。`int()` の変換自体は整数値しか通さないため、SQLインジェクションには耐えますが、不正入力でプログラムがクラッシュする可能性があります。

```python
# 改善版
try:
    page = int(input("ページ番号: "))
    if page < 0:
        page = 0
except ValueError:
    page = 0
query = "SELECT * FROM articles LIMIT 10 OFFSET ?"
cursor.execute(query, (page * 10,))
```

</details>

**問2:** ORDER BY句にユーザー入力を使いたい場合、なぜパラメータ化クエリが使えないのですか？安全な方法は何ですか？

<details>
<summary>解答</summary>

ORDER BY句の対象はカラム名（識別子）であり、SQL文の構造の一部です。パラメータ化クエリのプレースホルダはリテラル値（データ）の代入にしか使えず、識別子には使えません。

安全な方法はホワイトリスト方式です。
```python
allowed_columns = {"name": "name", "price": "price", "date": "created_at"}
sort_key = input("並び順: ")
if sort_key in allowed_columns:
    column = allowed_columns[sort_key]
    query = f"SELECT * FROM products ORDER BY {column}"
```

</details>

# 第5章：Pythonでの正規表現（reモジュール詳解）

## この章のゴール

- `re` モジュールの主要関数（match, search, fullmatch, findall, finditer, sub, subn, split, compile）を使い分けられる
- フラグ（IGNORECASE, MULTILINE, DOTALL, VERBOSE）を適切に指定できる
- マッチオブジェクト（Match Object）のメソッドを使いこなせる
- 用途に応じて最適な関数を選択できる

---

## 5.1 検索関数の使い分け：match / search / fullmatch

Pythonの `re` モジュールには、文字列の**どこを**検査するかが異なる3つの関数があります。

```
【3つの検索関数の違い】

文字列: "Hello, World!"

re.match(r"Hello", ...)     →  ✅ 先頭が "Hello" なのでマッチ
re.match(r"World", ...)     →  ❌ 先頭は "World" ではないので不一致

re.search(r"World", ...)    →  ✅ 文字列のどこかに "World" があるのでマッチ
re.search(r"Python", ...)   →  ❌ どこにも "Python" がないので不一致

re.fullmatch(r"Hello, World!", ...)  →  ✅ 文字列全体が一致
re.fullmatch(r"Hello", ...)          →  ❌ 文字列全体ではないので不一致
```

### re.match() ― 先頭マッチ

`re.match(pattern, string)` は、文字列の**先頭**がパターンに一致するか判定します。

```python
import re

text = "2026-04-05 は今日の日付です"

# 先頭が日付パターンかチェック
result = re.match(r"\d{4}-\d{2}-\d{2}", text)
if result:
    print(f"マッチ: {result.group()}")  # マッチ: 2026-04-05

# 先頭が "今日" ではないのでマッチしない
result2 = re.match(r"今日", text)
print(result2)  # None
```

### re.search() ― 部分マッチ

`re.search(pattern, string)` は、文字列の**どこか**にパターンと一致する部分があるか検索します。最初に見つかった1件だけを返します。

```python
import re

text = "問い合わせは 03-1234-5678 または 06-9876-5432 まで"

# 文字列のどこかで電話番号パターンを検索（最初の1件）
result = re.search(r"\d{2,4}-\d{2,4}-\d{4}", text)
if result:
    print(f"最初の電話番号: {result.group()}")  # 最初の電話番号: 03-1234-5678
```

### re.fullmatch() ― 完全一致

`re.fullmatch(pattern, string)` は、文字列**全体**がパターンに一致するか判定します。入力値のバリデーション（検証）に最適です。

```python
import re

# メールアドレスの簡易バリデーション
def is_valid_email(email):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.fullmatch(pattern, email) is not None

print(is_valid_email("user@example.com"))    # True
print(is_valid_email("invalid-email"))       # False
print(is_valid_email("user@example.com "))   # False（末尾にスペース）
```

### 3関数の比較表

| 関数 | 検索範囲 | 主な用途 | 戻り値 |
|---|---|---|---|
| `re.match()` | 文字列の先頭のみ | ログ行の先頭パース | Match or None |
| `re.search()` | 文字列全体を検索 | テキスト中のパターン検索 | Match or None |
| `re.fullmatch()` | 文字列全体が一致 | 入力値のバリデーション | Match or None |

> **よくある間違い**: `re.match()` は文字列全体の一致を判定しません。`re.match(r"\d+", "123abc")` は `"123"` にマッチします。全体一致を確認するには `re.fullmatch()` を使うか、パターンの末尾に `$` を付けてください。

---

## 5.2 すべてのマッチを取得：findall / finditer

### re.findall() ― マッチ文字列のリスト

`re.findall(pattern, string)` は、パターンに一致する**すべての部分文字列**をリストで返します。

```python
import re

text = "価格: 100円、送料: 250円、合計: 350円"

# すべての数字列を抽出
prices = re.findall(r"\d+", text)
print(prices)  # ['100', '250', '350']

# キャプチャグループがある場合はグループの内容が返る
pairs = re.findall(r"(\w+): (\d+)円", text)
print(pairs)  # [('価格', '100'), ('送料', '250'), ('合計', '350')]
```

> **重要**: キャプチャグループ `()` があると、`findall()` はグループの内容を返します。グループが1つならリスト of 文字列、複数ならリスト of タプルになります。パターン全体を取得したい場合は `(?:...)` 非キャプチャグループを使うか、`finditer()` を使いましょう。

### re.finditer() ― マッチオブジェクトのイテレータ

`re.finditer(pattern, string)` は、マッチごとに**マッチオブジェクト**を返すイテレータ（Iterator）を返します。位置情報やグループ情報が必要なときに使います。

```python
import re

text = "電話: 03-1234-5678、FAX: 06-9876-5432"

for m in re.finditer(r"\d{2,4}-\d{2,4}-\d{4}", text):
    print(f"番号: {m.group()}, 位置: {m.start()}〜{m.end()}")

# 出力:
# 番号: 03-1234-5678, 位置: 4〜16
# 番号: 06-9876-5432, 位置: 22〜34
```

### findall と finditer の使い分け

```
【使い分けの指針】

マッチした文字列だけほしい → findall()
  例: テキスト中の全URLをリストで取得

マッチの位置情報も必要    → finditer()
  例: テキスト中のキーワードの出現位置を記録

メモリ効率を重視          → finditer()
  例: 巨大なログファイルからエラーを抽出
```

---

## 5.3 置換：sub / subn

### re.sub() ― パターンに一致する部分を置換

`re.sub(pattern, repl, string, count=0)` は、パターンにマッチした部分を `repl` で置き換えます。

```python
import re

text = "電話番号は 03-1234-5678 です"

# 電話番号をマスキング
masked = re.sub(r"\d{2,4}-\d{2,4}-\d{4}", "XXX-XXXX-XXXX", text)
print(masked)  # 電話番号は XXX-XXXX-XXXX です
```

#### count引数で置換回数を制限

```python
import re

text = "apple apple apple"
result = re.sub(r"apple", "orange", text, count=2)
print(result)  # orange orange apple
```

#### 関数を使った高度な置換

`repl` に関数を渡すと、マッチオブジェクトを受け取って置換文字列を動的に生成できます。

```python
import re

text = "価格は100円と250円と500円です"

# 全価格を2倍にする
def double_price(match):
    price = int(match.group())
    return str(price * 2)

result = re.sub(r"\d+", double_price, text)
print(result)  # 価格は200円と500円と1000円です
```

#### 後方参照を使った置換

```python
import re

text = "2026-04-05"

# YYYY-MM-DD → MM/DD/YYYY に変換
result = re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\2/\3/\1", text)
print(result)  # 04/05/2026
```

### re.subn() ― 置換結果と回数のタプル

`re.subn()` は `re.sub()` と同じ置換を行いますが、**（置換後の文字列, 置換回数）**のタプルを返します。

```python
import re

text = "apple banana apple cherry apple"
result, count = re.subn(r"apple", "grape", text)
print(f"結果: {result}")    # 結果: grape banana grape cherry grape
print(f"置換回数: {count}")  # 置換回数: 3
```

> **実務でのポイント**: 置換が何件行われたかログに記録したいときに `re.subn()` が便利です。

---

## 5.4 分割：re.split()

`re.split(pattern, string, maxsplit=0)` は、パターンを区切りとして文字列を分割します。組み込みの `str.split()` より柔軟な分割が可能です。

### 基本的な分割

```python
import re

text = "りんご、バナナ,ぶどう、 メロン"

# カンマ（全角・半角）と前後の空白で分割
fruits = re.split(r"[、,]\s*", text)
print(fruits)  # ['りんご', 'バナナ', 'ぶどう', 'メロン']
```

### 複数の区切り文字での分割

```python
import re

# セミコロン、カンマ、スペースのいずれかで分割
data = "apple;banana, cherry grape"
items = re.split(r"[;,\s]\s*", data)
print(items)  # ['apple', 'banana', 'cherry', 'grape']
```

### maxsplit で分割回数を制限

```python
import re

text = "one:two:three:four:five"
result = re.split(r":", text, maxsplit=2)
print(result)  # ['one', 'two', 'three:four:five']
```

### キャプチャグループ付きの分割

パターンにキャプチャグループ `()` があると、区切り文字自体も結果に含まれます。

```python
import re

text = "2026-04-05"
result = re.split(r"(-)", text)
print(result)  # ['2026', '-', '04', '-', '05']

# 非キャプチャグループなら区切り文字は含まれない
result2 = re.split(r"(?:-)", text)
print(result2)  # ['2026', '04', '05']
```

> **よくある間違い**: `re.split(r"(,)", "a,b,c")` とすると `['a', ',', 'b', ',', 'c']` となり、区切り文字がリストに含まれます。意図しない場合は `(?:,)` や単に `,` を使いましょう。

---

## 5.5 パターンのコンパイル：re.compile()

### なぜコンパイルするのか

同じパターンを何度も使う場合、`re.compile()` でコンパイル済みパターンオブジェクト（compiled pattern object）を作っておくと効率的です。

```
【コンパイルの効果】

毎回パターン文字列を渡す場合:
  re.search(r"\d{4}-\d{2}-\d{2}", text1)  → 内部でコンパイル
  re.search(r"\d{4}-\d{2}-\d{2}", text2)  → また内部でコンパイル
  re.search(r"\d{4}-\d{2}-\d{2}", text3)  → またまた内部でコンパイル

事前にコンパイルしておく場合:
  pattern = re.compile(r"\d{4}-\d{2}-\d{2}")  → 1回だけコンパイル
  pattern.search(text1)  → コンパイル済みを再利用
  pattern.search(text2)  → コンパイル済みを再利用
  pattern.search(text3)  → コンパイル済みを再利用
```

### 基本的な使い方

```python
import re

# パターンをコンパイル
date_pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})")

texts = [
    "作成日: 2026-04-05",
    "更新日: 2026-03-15",
    "期限なし",
]

for text in texts:
    m = date_pattern.search(text)
    if m:
        print(f"{text} → 日付: {m.group()}")
    else:
        print(f"{text} → 日付なし")

# 出力:
# 作成日: 2026-04-05 → 日付: 2026-04-05
# 更新日: 2026-03-15 → 日付: 2026-03-15
# 期限なし → 日付なし
```

### コンパイル済みオブジェクトのメソッド

コンパイル済みオブジェクトは、`re` モジュールと同じメソッドを持っています。

```python
import re

pattern = re.compile(r"\b\w+@\w+\.\w+\b")

text = "連絡先: user@example.com または admin@test.org"

# search, findall, finditer, sub, split すべて使える
print(pattern.findall(text))  # ['user@example.com', 'admin@test.org']
print(pattern.sub("[メール]", text))  # 連絡先: [メール] または [メール]
```

> **実務でのポイント**: Pythonは内部的にパターンをキャッシュ（最大512個）しています。少数のパターンを使う場合はコンパイルしなくても性能差はわずかですが、コードの可読性を高めるためにも、繰り返し使うパターンは `compile()` しておくのがベストプラクティスです。

---

## 5.6 フラグ（Flags）

`re` モジュールの関数やコンパイルにフラグを渡すことで、マッチングの挙動を変更できます。

### re.IGNORECASE (re.I) ― 大文字小文字を無視

```python
import re

text = "Python python PYTHON"
results = re.findall(r"python", text, re.IGNORECASE)
print(results)  # ['Python', 'python', 'PYTHON']
```

### re.MULTILINE (re.M) ― 複数行モード

`^` と `$` が文字列全体の先頭・末尾ではなく、**各行の先頭・末尾**にマッチするようになります。

```python
import re

text = """1行目: Hello
2行目: World
3行目: Python"""

# デフォルト: ^ は文字列全体の先頭のみ
result1 = re.findall(r"^\d+行目", text)
print(result1)  # ['1行目']

# MULTILINE: ^ が各行の先頭にマッチ
result2 = re.findall(r"^\d+行目", text, re.MULTILINE)
print(result2)  # ['1行目', '2行目', '3行目']
```

```
【MULTILINEフラグの効果】

テキスト:
┌──────────────┐
│ 1行目: Hello │  ← ^ がマッチ（デフォルトでもMULTILINEでも）
│ 2行目: World │  ← ^ がマッチ（MULTILINEのみ）
│ 3行目: Python│  ← ^ がマッチ（MULTILINEのみ）
└──────────────┘
```

### re.DOTALL (re.S) ― ドットが改行にもマッチ

通常 `.` は改行文字 `\n` にマッチしませんが、`re.DOTALL` を指定すると改行にもマッチします。

```python
import re

text = """<div>
  Hello
  World
</div>"""

# デフォルト: . は改行にマッチしない
result1 = re.search(r"<div>(.+)</div>", text)
print(result1)  # None

# DOTALL: . が改行にもマッチ
result2 = re.search(r"<div>(.+)</div>", text, re.DOTALL)
print(result2.group(1))  # \n  Hello\n  World\n
```

### re.VERBOSE (re.X) ― 冗長モード（コメント付きパターン）

パターン内に**空白やコメント**を書けるようになり、複雑なパターンの可読性が向上します。

```python
import re

# VERBOSEなしの場合（読みにくい）
pattern_simple = r"^(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"

# VERBOSEありの場合（読みやすい）
pattern_verbose = re.compile(r"""
    ^                       # 文字列の先頭
    (\d{4})                 # 年: 4桁の数字
    -                       # ハイフン
    (0[1-9]|1[0-2])         # 月: 01〜12
    -                       # ハイフン
    (0[1-9]|[12]\d|3[01])   # 日: 01〜31
    $                       # 文字列の末尾
""", re.VERBOSE)

print(pattern_verbose.fullmatch("2026-04-05"))    # マッチ
print(pattern_verbose.fullmatch("2026-13-05"))    # None（月が不正）
```

### フラグの組み合わせ

複数のフラグはビットOR演算子 `|` で組み合わせます。

```python
import re

text = """name: Alice
Name: Bob
NAME: Charlie"""

# 大文字小文字無視 + 複数行モード
results = re.findall(r"^name: (\w+)", text, re.IGNORECASE | re.MULTILINE)
print(results)  # ['Alice', 'Bob', 'Charlie']
```

### インラインフラグ

パターンの中にフラグを埋め込むこともできます。

```python
import re

# (?i) = IGNORECASE, (?m) = MULTILINE, (?s) = DOTALL, (?x) = VERBOSE
result = re.findall(r"(?i)python", "Python PYTHON python")
print(result)  # ['Python', 'PYTHON', 'python']
```

### フラグ一覧表

| フラグ | 短縮形 | インライン | 効果 |
|---|---|---|---|
| `re.IGNORECASE` | `re.I` | `(?i)` | 大文字小文字を区別しない |
| `re.MULTILINE` | `re.M` | `(?m)` | `^` `$` が各行にマッチ |
| `re.DOTALL` | `re.S` | `(?s)` | `.` が改行にもマッチ |
| `re.VERBOSE` | `re.X` | `(?x)` | 空白・コメントを無視 |
| `re.ASCII` | `re.A` | `(?a)` | `\w` 等をASCIIに限定 |

---

## 5.7 マッチオブジェクトのメソッド

`re.search()` や `re.match()` が返すマッチオブジェクト（Match Object）には、マッチ結果を取り出すための便利なメソッドが用意されています。

### group() ― マッチした文字列の取得

```python
import re

text = "名前: 田中太郎、年齢: 30歳"
m = re.search(r"名前: (\S+)、年齢: (\d+)歳", text)

if m:
    print(m.group())    # 名前: 田中太郎、年齢: 30歳（マッチ全体）
    print(m.group(0))   # 名前: 田中太郎、年齢: 30歳（group()と同じ）
    print(m.group(1))   # 田中太郎（1番目のグループ）
    print(m.group(2))   # 30（2番目のグループ）
    print(m.group(1, 2))  # ('田中太郎', '30')（複数指定）
```

### groups() ― 全グループをタプルで取得

```python
import re

text = "2026-04-05"
m = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)

if m:
    print(m.groups())  # ('2026', '04', '05')

    # アンパック代入と組み合わせ
    year, month, day = m.groups()
    print(f"{year}年{month}月{day}日")  # 2026年04月05日
```

### groupdict() ― 名前付きグループを辞書で取得

名前付きグループ `(?P<name>...)` を使った場合に活用できます。

```python
import re

text = "2026-04-05"
m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", text)

if m:
    print(m.groupdict())  # {'year': '2026', 'month': '04', 'day': '05'}

    d = m.groupdict()
    print(f"{d['year']}年{d['month']}月{d['day']}日")  # 2026年04月05日
```

### span(), start(), end() ― マッチ位置の取得

```python
import re

text = "メールアドレス: user@example.com をご利用ください"
m = re.search(r"\S+@\S+", text)

if m:
    print(f"マッチ文字列: {m.group()}")    # user@example.com
    print(f"開始位置: {m.start()}")         # 9
    print(f"終了位置: {m.end()}")           # 25
    print(f"位置タプル: {m.span()}")        # (9, 25)

    # グループの位置も取得可能
    m2 = re.search(r"(\S+)@(\S+)", text)
    print(f"ユーザー名の位置: {m2.span(1)}")  # (9, 13)
    print(f"ドメインの位置: {m2.span(2)}")    # (14, 25)
```

### マッチオブジェクトのメソッド一覧

| メソッド | 説明 | 戻り値 |
|---|---|---|
| `group()` / `group(0)` | マッチ全体の文字列 | str |
| `group(n)` | n番目のグループの文字列 | str |
| `groups()` | 全グループのタプル | tuple |
| `groupdict()` | 名前付きグループの辞書 | dict |
| `start()` / `start(n)` | マッチ（グループn）の開始位置 | int |
| `end()` / `end(n)` | マッチ（グループn）の終了位置 | int |
| `span()` / `span(n)` | マッチ（グループn）の (start, end) | tuple |

> **よくある間違い**: `re.search()` がマッチしなかった場合 `None` を返します。`None` に対して `.group()` を呼ぶと `AttributeError` になるため、必ず `if m:` でチェックしてから使いましょう。

---

## 5.8 実践例：ログファイルの解析

ここまで学んだ関数を組み合わせた実践例です。

```python
import re

# サンプルログデータ
log_data = """
2026-04-05 10:23:15 [INFO] Server started on port 8080
2026-04-05 10:25:30 [WARNING] High memory usage: 85%
2026-04-05 10:30:45 [ERROR] Connection timeout: database server unreachable
2026-04-05 10:31:00 [INFO] Retrying connection...
2026-04-05 10:31:05 [ERROR] Connection failed: max retries exceeded
""".strip()

# 1. ログのパターンをコンパイル
log_pattern = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2})\s+"
    r"(?P<time>\d{2}:\d{2}:\d{2})\s+"
    r"\[(?P<level>\w+)\]\s+"
    r"(?P<message>.+)"
)

# 2. 全行を解析
print("=== ログ解析結果 ===")
for m in log_pattern.finditer(log_data):
    d = m.groupdict()
    print(f"[{d['level']:>7}] {d['date']} {d['time']} - {d['message']}")

# 3. ERRORレベルだけ抽出
print("\n=== エラーログのみ ===")
error_pattern = re.compile(r".*\[ERROR\]\s+(.+)", re.MULTILINE)
errors = error_pattern.findall(log_data)
for err in errors:
    print(f"  ❗ {err}")

# 4. ログレベルの集計
levels = re.findall(r"\[(\w+)\]", log_data)
from collections import Counter
level_counts = Counter(levels)
print(f"\n=== レベル別集計 ===")
for level, count in level_counts.most_common():
    print(f"  {level}: {count}件")

# 出力:
# === ログ解析結果 ===
# [   INFO] 2026-04-05 10:23:15 - Server started on port 8080
# [WARNING] 2026-04-05 10:25:30 - High memory usage: 85%
# [  ERROR] 2026-04-05 10:30:45 - Connection timeout: database server unreachable
# [   INFO] 2026-04-05 10:31:00 - Retrying connection...
# [  ERROR] 2026-04-05 10:31:05 - Connection failed: max retries exceeded
#
# === エラーログのみ ===
#   ❗ Connection timeout: database server unreachable
#   ❗ Connection failed: max retries exceeded
#
# === レベル別集計 ===
#   INFO: 2件
#   ERROR: 2件
#   WARNING: 1件
```

---

## ポイントまとめ

```
【第5章のポイント】

1. 検索関数の使い分け
   ┌─────────────┬────────────────────────┐
   │ match()     │ 先頭がパターンに一致   │
   │ search()    │ どこかにパターンがある │
   │ fullmatch() │ 全体がパターンに一致   │
   │ findall()   │ 全マッチをリストで取得 │
   │ finditer()  │ 全マッチをイテレータで │
   └─────────────┴────────────────────────┘

2. 置換と分割
   ┌─────────────┬────────────────────────┐
   │ sub()       │ マッチ部分を置換       │
   │ subn()      │ 置換 + 回数を返す      │
   │ split()     │ パターンで文字列を分割 │
   └─────────────┴────────────────────────┘

3. compile() で繰り返し使うパターンを事前コンパイル

4. フラグで挙動をカスタマイズ
   IGNORECASE / MULTILINE / DOTALL / VERBOSE

5. マッチオブジェクトで詳細情報を取得
   group() / groups() / groupdict() / span()
```

---

次の章では、ここまでの知識を活かして**実践的なパターン集**を学んでいきます。メールアドレス、URL、電話番号など、現場でよく使うパターンを「簡易版」と「厳密版」で紹介します。

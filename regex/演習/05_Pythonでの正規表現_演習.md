# 第5章 演習：Pythonでの正規表現（reモジュール詳解）

---

## 問題1：match / search / fullmatch の使い分け（基本）

以下の3つの文字列について、`re.match()`、`re.search()`、`re.fullmatch()` をそれぞれ使い、パターン `r"\d+"` で数字がマッチするかどうかを調べてください。結果が `None` か、マッチオブジェクトかを表示してください。

```python
texts = ["123abc", "abc123", "456"]
```

**期待される出力：**
```
--- 123abc ---
match:     123
search:    123
fullmatch: None
--- abc123 ---
match:     None
search:    123
fullmatch: None
--- 456 ---
match:     456
search:    456
fullmatch: 456
```

<details>
<summary>ヒント</summary>

- `re.match()` は先頭から調べます
- `re.search()` は文字列全体から探します
- `re.fullmatch()` は文字列全体が一致するかを調べます
- マッチオブジェクトが `None` でない場合に `.group()` で文字列を取り出せます

</details>

<details>
<summary>解答例</summary>

```python
import re

texts = ["123abc", "abc123", "456"]

for text in texts:
    print(f"--- {text} ---")

    # match: 先頭から
    m = re.match(r"\d+", text)
    print(f"match:     {m.group() if m else None}")

    # search: どこかに
    s = re.search(r"\d+", text)
    print(f"search:    {s.group() if s else None}")

    # fullmatch: 全体が
    f = re.fullmatch(r"\d+", text)
    print(f"fullmatch: {f.group() if f else None}")
```

</details>

---

## 問題2：findall と finditer の使い分け（基本）

以下のテキストから、金額（数字＋「円」）をすべて抽出してください。

1. `re.findall()` で金額のリストを取得
2. `re.finditer()` で金額と出現位置を表示

```python
text = "商品A: 1500円、商品B: 2800円、送料: 500円、合計: 4800円"
```

**期待される出力：**
```
findall: ['1500円', '2800円', '500円', '4800円']
finditer:
  1500円 (位置: 5〜10)
  2800円 (位置: 15〜20)
  500円 (位置: 24〜28)
  4800円 (位置: 33〜38)
```

<details>
<summary>ヒント</summary>

- 金額のパターンは `\d+円` です
- `findall()` はマッチした文字列のリストを返します
- `finditer()` はマッチオブジェクトを返すので、`.start()` と `.end()` で位置を取得できます

</details>

<details>
<summary>解答例</summary>

```python
import re

text = "商品A: 1500円、商品B: 2800円、送料: 500円、合計: 4800円"

# findall
results = re.findall(r"\d+円", text)
print(f"findall: {results}")

# finditer
print("finditer:")
for m in re.finditer(r"\d+円", text):
    print(f"  {m.group()} (位置: {m.start()}〜{m.end()})")
```

</details>

---

## 問題3：re.sub() による置換（基本）

以下のテキスト中の電話番号をすべて `***-****-****` にマスキングしてください。

```python
text = "本社: 03-1234-5678、支社: 06-9876-5432、携帯: 090-1111-2222"
```

**期待される出力：**
```
本社: ***-****-****、支社: ***-****-****、携帯: ***-****-****
```

<details>
<summary>ヒント</summary>

- 電話番号のパターンは `\d{2,3}-\d{4}-\d{4}` です
- `re.sub(パターン, 置換文字列, テキスト)` で一括置換できます

</details>

<details>
<summary>解答例</summary>

```python
import re

text = "本社: 03-1234-5678、支社: 06-9876-5432、携帯: 090-1111-2222"

# 電話番号をマスキング
masked = re.sub(r"\d{2,3}-\d{4}-\d{4}", "***-****-****", text)
print(masked)
```

</details>

---

## 問題4：re.split() による分割（基本）

以下のCSV風テキストを適切に分割してリストにしてください。区切り文字はカンマですが、カンマの前後に空白が入る場合があります。

```python
text = "田中太郎, 30,東京都 , エンジニア,  Python"
```

**期待される出力：**
```
['田中太郎', '30', '東京都', 'エンジニア', 'Python']
```

<details>
<summary>ヒント</summary>

- `re.split()` のパターンで、カンマの前後にある空白も含めて区切り文字にします
- `\s*,\s*` のようなパターンを使いましょう

</details>

<details>
<summary>解答例</summary>

```python
import re

text = "田中太郎, 30,東京都 , エンジニア,  Python"

# カンマの前後の空白ごと分割
result = re.split(r"\s*,\s*", text)
print(result)
# ['田中太郎', '30', '東京都', 'エンジニア', 'Python']
```

</details>

---

## 問題5：フラグの活用（応用）

以下の複数行テキストから、各行の先頭にある日付（YYYY-MM-DD形式）をすべて抽出してください。大文字・小文字の違いを無視して、行末の "ok" または "OK" も同時にチェックしてください。

```python
text = """2026-04-01 システム起動 OK
2026-04-02 バッチ処理完了 ok
2026-04-03 エラー発生 NG
2026-04-04 復旧完了 Ok"""
```

1. 各行の先頭の日付をすべて抽出（`re.MULTILINE` を使用）
2. 末尾が "ok"（大文字小文字不問）の行だけを抽出（`re.MULTILINE | re.IGNORECASE` を使用）

**期待される出力：**
```
全日付: ['2026-04-01', '2026-04-02', '2026-04-03', '2026-04-04']
OK行: ['2026-04-01 システム起動 OK', '2026-04-02 バッチ処理完了 ok', '2026-04-04 復旧完了 Ok']
```

<details>
<summary>ヒント</summary>

- `^` は `re.MULTILINE` フラグで各行の先頭にマッチします
- `$` は `re.MULTILINE` フラグで各行の末尾にマッチします
- フラグは `|` で組み合わせられます

</details>

<details>
<summary>解答例</summary>

```python
import re

text = """2026-04-01 システム起動 OK
2026-04-02 バッチ処理完了 ok
2026-04-03 エラー発生 NG
2026-04-04 復旧完了 Ok"""

# 1. 各行先頭の日付を抽出
dates = re.findall(r"^\d{4}-\d{2}-\d{2}", text, re.MULTILINE)
print(f"全日付: {dates}")

# 2. 末尾がOK（大文字小文字不問）の行を抽出
ok_lines = re.findall(r"^.+ok$", text, re.MULTILINE | re.IGNORECASE)
print(f"OK行: {ok_lines}")
```

</details>

---

## 問題6：マッチオブジェクトの活用（応用）

以下のテキストから名前付きグループを使って、名前・年齢・職業を抽出し、辞書のリストとして整理してください。

```python
text = """名前:田中太郎 年齢:30 職業:エンジニア
名前:佐藤花子 年齢:25 職業:デザイナー
名前:鈴木一郎 年齢:35 職業:マネージャー"""
```

**期待される出力：**
```
{'name': '田中太郎', 'age': '30', 'job': 'エンジニア'}
{'name': '佐藤花子', 'age': '25', 'job': 'デザイナー'}
{'name': '鈴木一郎', 'age': '35', 'job': 'マネージャー'}
```

<details>
<summary>ヒント</summary>

- 名前付きグループは `(?P<name>パターン)` の形式で書きます
- `re.finditer()` でマッチオブジェクトを順に取得し、`.groupdict()` で辞書に変換できます

</details>

<details>
<summary>解答例</summary>

```python
import re

text = """名前:田中太郎 年齢:30 職業:エンジニア
名前:佐藤花子 年齢:25 職業:デザイナー
名前:鈴木一郎 年齢:35 職業:マネージャー"""

# 名前付きグループでパターンを定義
pattern = re.compile(r"名前:(?P<name>\S+)\s+年齢:(?P<age>\d+)\s+職業:(?P<job>\S+)")

people = []
for m in pattern.finditer(text):
    person = m.groupdict()
    people.append(person)
    print(person)

# 出力:
# {'name': '田中太郎', 'age': '30', 'job': 'エンジニア'}
# {'name': '佐藤花子', 'age': '25', 'job': 'デザイナー'}
# {'name': '鈴木一郎', 'age': '35', 'job': 'マネージャー'}
```

</details>

---

## 問題7：re.sub() の関数置換（応用）

以下のテキスト中の温度（数字＋℃）を、摂氏から華氏に変換して置き換えてください。華氏の計算式は `F = C * 9/5 + 32` です。小数点以下は1桁に丸めてください。

```python
text = "東京: 20℃、大阪: 22℃、札幌: 5℃、那覇: 28℃"
```

**期待される出力：**
```
東京: 68.0°F、大阪: 71.6°F、札幌: 41.0°F、那覇: 82.4°F
```

<details>
<summary>ヒント</summary>

- `re.sub()` の第2引数に関数を渡すと、マッチオブジェクトを受け取って動的に置換文字列を生成できます
- 関数の中で `match.group()` を使って数値部分を取り出します

</details>

<details>
<summary>解答例</summary>

```python
import re

text = "東京: 20℃、大阪: 22℃、札幌: 5℃、那覇: 28℃"

def celsius_to_fahrenheit(match):
    celsius = int(match.group(1))
    fahrenheit = celsius * 9 / 5 + 32
    return f"{fahrenheit:.1f}°F"

result = re.sub(r"(\d+)℃", celsius_to_fahrenheit, text)
print(result)
# 東京: 68.0°F、大阪: 71.6°F、札幌: 41.0°F、那覇: 82.4°F
```

</details>

---

## 問題8：re.compile() と re.VERBOSE（チャレンジ）

以下の要件を満たすパスワードバリデーターを、`re.compile()` と `re.VERBOSE` を使って作成してください。

**パスワード要件：**
- 8文字以上20文字以下
- 半角英大文字を1文字以上含む
- 半角英小文字を1文字以上含む
- 半角数字を1文字以上含む
- 使用可能な文字は英数字と記号 `!@#$%^&*` のみ

**テストケース：**
```python
tests = [
    ("Abc12345", True),       # OK
    ("abc12345", False),      # 大文字なし
    ("ABC12345", False),      # 小文字なし
    ("Abcdefgh", False),      # 数字なし
    ("Ab1", False),           # 8文字未満
    ("Pass1234!@#", True),    # OK（記号含む）
    ("Pass 1234", False),     # スペースは不可
]
```

**期待される出力：**
```
Abc12345     → True  (期待: True) ✅
abc12345     → False (期待: False) ✅
ABC12345     → False (期待: False) ✅
Abcdefgh     → False (期待: False) ✅
Ab1          → False (期待: False) ✅
Pass1234!@#  → True  (期待: True) ✅
Pass 1234    → False (期待: False) ✅
```

<details>
<summary>ヒント</summary>

- 先読み `(?=...)` を使って各条件をチェックします
- `(?=.*[A-Z])` は「文字列のどこかに大文字がある」を意味します
- `re.VERBOSE` を使うとパターンにコメントが書けて読みやすくなります
- `re.fullmatch()` で文字列全体を検証します

</details>

<details>
<summary>解答例</summary>

```python
import re

# VERBOSEモードでコメント付きパターン
password_pattern = re.compile(r"""
    (?=.*[A-Z])          # 大文字を1文字以上含む（先読み）
    (?=.*[a-z])          # 小文字を1文字以上含む（先読み）
    (?=.*\d)             # 数字を1文字以上含む（先読み）
    [A-Za-z\d!@#$%^&*]   # 使用可能な文字のみ
    {8,20}               # 8文字以上20文字以下
""", re.VERBOSE)

tests = [
    ("Abc12345", True),
    ("abc12345", False),
    ("ABC12345", False),
    ("Abcdefgh", False),
    ("Ab1", False),
    ("Pass1234!@#", True),
    ("Pass 1234", False),
]

for password, expected in tests:
    result = password_pattern.fullmatch(password) is not None
    status = "✅" if result == expected else "❌"
    print(f"{password:<12} → {str(result):<5} (期待: {expected}) {status}")
```

</details>

---

## 問題9：総合問題 ― アクセスログの解析（チャレンジ）

以下のWebサーバーアクセスログを解析して、各情報を抽出・集計してください。

```python
log = """192.168.1.10 - - [05/Apr/2026:10:15:30] "GET /index.html HTTP/1.1" 200 1024
192.168.1.20 - - [05/Apr/2026:10:16:45] "POST /api/login HTTP/1.1" 302 256
10.0.0.5 - - [05/Apr/2026:10:17:00] "GET /style.css HTTP/1.1" 200 4096
192.168.1.10 - - [05/Apr/2026:10:18:30] "GET /about.html HTTP/1.1" 200 2048
10.0.0.5 - - [05/Apr/2026:10:19:15] "GET /api/data HTTP/1.1" 404 128
192.168.1.20 - - [05/Apr/2026:10:20:00] "GET /index.html HTTP/1.1" 200 1024"""
```

以下を実装してください：

1. 名前付きグループでIP、日時、メソッド、パス、ステータスコード、サイズを抽出
2. ステータスコード別のアクセス数を集計
3. IPアドレス別のアクセス数を集計
4. 404エラーのパスを一覧表示

**期待される出力：**
```
=== ログ解析 ===
192.168.1.10 | GET  /index.html  | 200
192.168.1.20 | POST /api/login   | 302
10.0.0.5     | GET  /style.css   | 200
192.168.1.10 | GET  /about.html  | 200
10.0.0.5     | GET  /api/data    | 404
192.168.1.20 | GET  /index.html  | 200

=== ステータスコード別 ===
200: 4件
302: 1件
404: 1件

=== IP別アクセス数 ===
192.168.1.10: 2件
192.168.1.20: 2件
10.0.0.5: 2件

=== 404エラー ===
/api/data
```

<details>
<summary>ヒント</summary>

- ログの各フィールドを名前付きグループ `(?P<name>...)` で抽出します
- `re.compile()` と `re.finditer()` を組み合わせましょう
- `collections.Counter` を使うと集計が簡単です
- パターンは `re.VERBOSE` で読みやすく書くのがおすすめです

</details>

<details>
<summary>解答例</summary>

```python
import re
from collections import Counter

log = """192.168.1.10 - - [05/Apr/2026:10:15:30] "GET /index.html HTTP/1.1" 200 1024
192.168.1.20 - - [05/Apr/2026:10:16:45] "POST /api/login HTTP/1.1" 302 256
10.0.0.5 - - [05/Apr/2026:10:17:00] "GET /style.css HTTP/1.1" 200 4096
192.168.1.10 - - [05/Apr/2026:10:18:30] "GET /about.html HTTP/1.1" 200 2048
10.0.0.5 - - [05/Apr/2026:10:19:15] "GET /api/data HTTP/1.1" 404 128
192.168.1.20 - - [05/Apr/2026:10:20:00] "GET /index.html HTTP/1.1" 200 1024"""

# VERBOSEモードでパターンを定義
pattern = re.compile(r"""
    (?P<ip>\d+\.\d+\.\d+\.\d+)       # IPアドレス
    \s+-\s+-\s+                        # " - - "
    \[(?P<datetime>[^\]]+)\]           # [日時]
    \s+"                               # スペースと開始引用符
    (?P<method>\w+)                    # HTTPメソッド
    \s+(?P<path>\S+)                   # パス
    \s+HTTP/[\d.]+"                    # HTTPバージョンと終了引用符
    \s+(?P<status>\d+)                 # ステータスコード
    \s+(?P<size>\d+)                   # サイズ
""", re.VERBOSE)

# 1. 各行を解析して表示
print("=== ログ解析 ===")
entries = []
for m in pattern.finditer(log):
    d = m.groupdict()
    entries.append(d)
    print(f"{d['ip']:<12} | {d['method']:<4} {d['path']:<13} | {d['status']}")

# 2. ステータスコード別集計
print("\n=== ステータスコード別 ===")
status_counts = Counter(e['status'] for e in entries)
for status, count in sorted(status_counts.items()):
    print(f"{status}: {count}件")

# 3. IP別アクセス数
print("\n=== IP別アクセス数 ===")
ip_counts = Counter(e['ip'] for e in entries)
for ip, count in ip_counts.items():
    print(f"{ip}: {count}件")

# 4. 404エラーのパス
print("\n=== 404エラー ===")
for e in entries:
    if e['status'] == '404':
        print(e['path'])
```

</details>

---

## 振り返りチェックリスト

- [ ] `match()`, `search()`, `fullmatch()` の違いを説明できる
- [ ] `findall()` と `finditer()` を用途に応じて使い分けられる
- [ ] `sub()` で文字列置換と関数置換の両方ができる
- [ ] `split()` で柔軟な文字列分割ができる
- [ ] `compile()` でパターンを事前コンパイルする利点を理解している
- [ ] フラグ（IGNORECASE, MULTILINE, DOTALL, VERBOSE）を適切に使える
- [ ] マッチオブジェクトのメソッド（group, groups, groupdict, span）を使いこなせる

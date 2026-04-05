# 実践課題02：ReActパターン手動トレース ★1

> **難易度**: ★☆☆☆☆
> **前提知識**: 第2章（エージェントの基本アーキテクチャ）
> **課題の種類**: 設計課題
> **学習目標**: ReAct（Reasoning + Acting）パターンの思考→行動→観察サイクルを手動でトレースし、エージェントの内部動作を直感的に理解できるようになること

---

## 完成イメージ

以下のようなReActトレースログを手書きで作成します。

```
┌──────────────────────────────────────────────────────┐
│  ユーザー質問: 「東京の明日の天気を教えて」            │
└──────────────┬───────────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────────┐
│  Thought 1: 天気情報が必要。天気APIを呼び出そう       │
│  Action 1:  weather_api.get("Tokyo", "tomorrow")     │
│  Observation 1: {"temp": 22, "condition": "晴れ"}    │
├──────────────────────────────────────────────────────┤
│  Thought 2: 情報が得られた。ユーザーに回答しよう       │
│  Action 2:  respond("明日の東京は晴れ、気温22℃です")  │
│  Observation 2: （ユーザーに回答完了）                 │
└──────────────────────────────────────────────────────┘
```

最終成果物は、3つの異なるシナリオに対するReActトレースログです。

---

## 課題の要件

1. 以下の3つのシナリオについて、ReActパターンのトレースログを作成すること
   - **シナリオA**: 「Python で JSON ファイルを読み込むコードを書いて」（ツール不要、知識ベースで回答）
   - **シナリオB**: 「今日のドル円の為替レートを教えて」（外部API呼び出しが必要）
   - **シナリオC**: 「この CSV ファイルのデータを集計して、売上トップ3の商品を教えて」（複数ステップのツール利用が必要）
2. 各トレースログには以下の要素を含めること
   - **Thought**（思考）: エージェントが何を考えたか
   - **Action**（行動）: どのツールをどんな引数で呼んだか
   - **Observation**（観察）: ツールからどんな結果が返ったか
3. 各ステップの **Thought** では、エージェントの判断理由を具体的に記述すること
4. ツール呼び出しは**関数呼び出し形式**（例: `tool_name(arg1, arg2)`）で記述すること
5. エラーが発生するケースも1つ以上含めること（ツールがエラーを返した場合のリカバリー）
6. 最終的にエージェントが **finish** アクションで応答を返すまでのフローを完結させること

---

## ステップガイド

<details>
<summary>ステップ1：ReActパターンの基本構造を確認する</summary>

ReActパターンは以下のサイクルを繰り返します。

```
while not finished:
    thought = LLM("現在の状況を踏まえて、次に何をすべきか？")
    action = LLM("具体的にどのツールを、どう呼ぶか？")
    observation = execute(action)
    context.append(thought, action, observation)
```

**ポイント**:
- Thought は「なぜそのActionを選んだか」の理由付けです
- Action は必ず利用可能なツールの中から選びます
- Observation はツールの実行結果であり、LLMが生成するものではありません

</details>

<details>
<summary>ステップ2：利用可能なツールセットを定義する</summary>

トレースを書く前に、エージェントが使えるツールを定義しましょう。

```
利用可能ツール:
- web_search(query: str) → str        # Web検索を実行し結果を返す
- weather_api(city: str, date: str) → dict  # 天気情報を取得
- exchange_rate(from: str, to: str) → float # 為替レートを取得
- read_file(path: str) → str          # ファイルを読み込む
- run_python(code: str) → str          # Pythonコードを実行
- respond(message: str) → None         # ユーザーに最終回答を返す
```

**よくある間違い**: 利用可能ツールにないツールを使ってしまうケースがあります。エージェントは定義されたツールの中からしか選べません。

</details>

<details>
<summary>ステップ3：シナリオごとにトレースを書く</summary>

各シナリオで以下を考えましょう。

1. ユーザーの質問を受け取ったエージェントが最初に何を考えるか
2. その思考に基づいてどのツールを選ぶか（またはツール不要で直接回答するか）
3. ツールの結果を見て、次に何をすべきか判断する
4. 必要な情報がすべて揃ったら `respond` で最終回答を返す

シナリオCでは「ファイル読み込み → コード実行 → 結果解釈 → 回答」のように複数ステップが必要になります。

</details>

<details>
<summary>ステップ4：エラーケースを含める</summary>

シナリオBまたはCの中で、ツールがエラーを返すケースを1つ入れましょう。

例:
```
Thought 2: 為替レートAPIを呼び出したがエラーが返った。
           Web検索でフォールバックしよう。
Action 2:  web_search("USD JPY exchange rate today")
Observation 2: "本日のドル円レートは154.32円です（出典: ○○）"
```

このように、エラー発生時にエージェントが代替手段を考える様子を記述します。

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

### 利用可能ツール定義

```
- web_search(query: str) → str
- exchange_rate(from_currency: str, to_currency: str) → float
- read_file(path: str) → str
- run_python(code: str) → str
- respond(message: str) → None
```

### シナリオA: 「PythonでJSONファイルを読み込むコードを書いて」

```
User: PythonでJSONファイルを読み込むコードを書いて

Thought 1: これはプログラミングの知識に関する質問です。
           Pythonの標準ライブラリ json を使ったコードを
           知識から生成できるので、外部ツールは不要です。
           直接回答しましょう。

Action 1:  respond("""
import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(data)
""")

Observation 1: （ユーザーに回答を返しました）

→ 完了（1ステップで終了）
```

### シナリオB: 「今日のドル円の為替レートを教えて」

```
User: 今日のドル円の為替レートを教えて

Thought 1: リアルタイムの為替レートが必要です。
           exchange_rate ツールを使って取得しましょう。

Action 1:  exchange_rate("USD", "JPY")

Observation 1: Error: "API rate limit exceeded. Please try again later."

Thought 2: APIがレートリミットでエラーになりました。
           代替手段として Web 検索を使いましょう。

Action 2:  web_search("USD JPY exchange rate today")

Observation 2: "本日の米ドル/円相場は154.32円（15:00時点）"

Thought 3: Web検索で為替レートが取得できました。
           この情報をもとにユーザーに回答します。

Action 3:  respond("本日のドル円為替レートは1ドル＝約154.32円です（15:00時点）。")

Observation 3: （ユーザーに回答を返しました）

→ 完了（エラーリカバリーを含む3ステップ）
```

### シナリオC: 「このCSVファイルのデータを集計して、売上トップ3の商品を教えて」

```
User: sales.csv のデータを集計して、売上トップ3の商品を教えて

Thought 1: まずCSVファイルの中身を確認する必要があります。
           read_file ツールでファイルを読み込みましょう。

Action 1:  read_file("sales.csv")

Observation 1:
"product,quantity,price
りんご,150,200
みかん,300,100
バナナ,80,150
ぶどう,50,400
メロン,20,800"

Thought 2: CSVの構造がわかりました。
           売上 = quantity × price で計算して、
           トップ3を求めるPythonコードを実行しましょう。

Action 2:  run_python("""
import csv
import io

data = \"\"\"product,quantity,price
りんご,150,200
みかん,300,100
バナナ,80,150
ぶどう,50,400
メロン,20,800\"\"\"

reader = csv.DictReader(io.StringIO(data))
sales = []
for row in reader:
    total = int(row['quantity']) * int(row['price'])
    sales.append((row['product'], total))

sales.sort(key=lambda x: x[1], reverse=True)
for rank, (product, total) in enumerate(sales[:3], 1):
    print(f"{rank}位: {product} (売上: {total:,}円)")
""")

Observation 2:
"1位: りんご (売上: 30,000円)
2位: みかん (売上: 30,000円)
3位: ぶどう (売上: 20,000円)"

Thought 3: 集計結果が得られました。
           りんごとみかんが同額で1位タイです。
           この結果をユーザーにわかりやすく伝えましょう。

Action 3:  respond("""
sales.csv の売上トップ3は以下のとおりです。

1位: りんご（売上: 30,000円）
1位: みかん（売上: 30,000円）※同額
3位: ぶどう（売上: 20,000円）

※売上 = 数量 × 単価 で計算しています。
""")

Observation 3: （ユーザーに回答を返しました）

→ 完了（3ステップ）
```

</details>

<details>
<summary>解答例（改良版）</summary>

改良版では、以下の点を強化しています。

- **Thought に判断基準を明示**: 「なぜそのツールを選んだか」をより詳細に記述
- **分岐条件を明示**: 「もし〜なら〜する」という条件分岐の思考を記述
- **メタ認知的な振り返り**: 各シナリオ終了後にエージェントの行動を分析

### 利用可能ツール定義（改良版）

```json
{
  "tools": [
    {
      "name": "web_search",
      "description": "Web検索を実行し、上位結果を返す",
      "parameters": {"query": "string"},
      "returns": "string（検索結果のサマリー）"
    },
    {
      "name": "exchange_rate",
      "description": "リアルタイム為替レートを取得する",
      "parameters": {"from_currency": "string", "to_currency": "string"},
      "returns": "float（為替レート）"
    },
    {
      "name": "read_file",
      "description": "ファイルの内容を読み込む",
      "parameters": {"path": "string"},
      "returns": "string（ファイル内容）"
    },
    {
      "name": "run_python",
      "description": "Pythonコードを実行して結果を返す",
      "parameters": {"code": "string"},
      "returns": "string（実行結果の標準出力）"
    },
    {
      "name": "respond",
      "description": "ユーザーに最終回答を返す",
      "parameters": {"message": "string"},
      "returns": "null"
    }
  ]
}
```

### シナリオC（改良版）: 複数ステップ＋エラーリカバリー

```
User: sales.csv のデータを集計して、売上トップ3の商品を教えて

── ステップ 1 ──────────────────────────────────────

Thought 1:
  - 目標: CSVデータを集計してトップ3を求める
  - 必要な情報: CSVファイルの内容（構造が不明）
  - 選択: read_file でまずファイル構造を確認する
  - 理由: 構造がわからないままコードを書くと失敗する可能性が高い

Action 1: read_file("sales.csv")

Observation 1:
  "product,quantity,price\nりんご,150,200\nみかん,300,100\n
   バナナ,80,150\nぶどう,50,400\nメロン,20,800"

── ステップ 2 ──────────────────────────────────────

Thought 2:
  - CSVの構造を確認: 3列（product, quantity, price）
  - 「売上」の定義が明示されていない
    → 一般的に「売上 = quantity × price」と解釈する
  - 集計にはPythonコードの実行が適切
  - pandas は外部ライブラリなので、標準ライブラリの csv を使う

Action 2: run_python("""
import csv, io

data = open('sales.csv', 'r', encoding='utf-8').read()
reader = csv.DictReader(io.StringIO(data))
sales = [(r['product'], int(r['quantity']) * int(r['price'])) for r in reader]
sales.sort(key=lambda x: x[1], reverse=True)
for i, (p, s) in enumerate(sales[:3], 1):
    print(f"{i}位: {p} ({s:,}円)")
""")

Observation 2:
  Error: "FileNotFoundError: [Errno 2] No such file or directory: 'sales.csv'"

── ステップ 3（エラーリカバリー）──────────────────

Thought 3:
  - run_python の実行環境にはファイルが存在しない
  - 対策: ステップ1で取得したファイル内容をコード内に
    直接埋め込んで実行する
  - 学び: ツール間でファイルシステムが共有されるとは
    限らない。データは明示的に渡すべき

Action 3: run_python("""
import csv, io

csv_data = \"\"\"product,quantity,price
りんご,150,200
みかん,300,100
バナナ,80,150
ぶどう,50,400
メロン,20,800\"\"\"

reader = csv.DictReader(io.StringIO(csv_data))
sales = [(r['product'], int(r['quantity']) * int(r['price'])) for r in reader]
sales.sort(key=lambda x: x[1], reverse=True)

print("=== 売上ランキング（全商品）===")
for i, (p, s) in enumerate(sales, 1):
    bar = "█" * (s // 2000)
    print(f"  {i}位: {p:＜6s} {s:>8,}円 {bar}")

print(f"\\n=== トップ3 ===")
for i, (p, s) in enumerate(sales[:3], 1):
    print(f"  {i}位: {p}（{s:,}円）")
""")

Observation 3:
  "=== 売上ランキング（全商品）===
    1位: りんご  30,000円 ███████████████
    2位: みかん  30,000円 ███████████████
    3位: ぶどう  20,000円 ██████████
    4位: メロン  16,000円 ████████
    5位: バナナ  12,000円 ██████

  === トップ3 ===
    1位: りんご（30,000円）
    2位: みかん（30,000円）
    3位: ぶどう（20,000円）"

── ステップ 4 ──────────────────────────────────────

Thought 4:
  - 集計結果が正常に得られた
  - りんごとみかんが同額なので、順位表現に注意が必要
  - 全商品のランキングも付記するとユーザーにとって親切

Action 4: respond("""
sales.csv を集計しました。売上（数量×単価）のトップ3は以下のとおりです。

| 順位 | 商品   | 売上     |
|------|--------|---------|
| 1位  | りんご | 30,000円 |
| 1位  | みかん | 30,000円 |
| 3位  | ぶどう | 20,000円 |

※りんごとみかんは売上が同額のため、同率1位としています。
※売上 = 数量 × 単価 で計算しています。
""")

Observation 4: （ユーザーに回答を返しました）

→ 完了（4ステップ、エラーリカバリー1回を含む）
```

### 各シナリオの分析

| シナリオ | ステップ数 | ツール使用回数 | エラー回数 | 特徴 |
|----------|-----------|---------------|-----------|------|
| A（コード生成） | 1 | 0（respond のみ） | 0 | 知識ベースで即回答 |
| B（為替レート） | 3 | 2 + respond | 1 | API エラーからの回復 |
| C（CSV集計） | 4 | 3 + respond | 1 | 複合ツール利用＋エラー回復 |

**プロの知見**: 実際のエージェント開発では、このようなトレースログを記録・分析することが**デバッグの基本**です。問題が発生した際に「どのステップの Thought が誤っていたのか」「Observation の解釈が間違っていたのか」を特定できるよう、ログ設計は初期段階から組み込むべきです。

</details>

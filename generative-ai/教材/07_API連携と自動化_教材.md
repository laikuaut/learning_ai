# 第7章：API連携と自動化

## この章のゴール
生成AIのAPI（Application Programming Interface）を理解し、Pythonを使った実装やノーコードツールとの連携を通じて、業務の自動化ワークフローを設計・構築できるようになることを目指します。

## 学習目標
- 生成AI APIの仕組み（REST API、認証、リクエスト/レスポンス）を理解する
- 主要な生成AI API（Anthropic、OpenAI、Google）の違いと使い分けを説明できる
- Pythonを使って生成AI APIを呼び出すコードを書ける
- ノーコード/ローコードツールと生成AIを連携させる方法を知る
- ワークフロー自動化の設計パターンとエラーハンドリングを理解する
- コスト管理とトークン最適化の手法を実践できる

---

## 7.1 生成AI APIの基本

### APIとは何か

API（Application Programming Interface）とは、ソフトウェア同士が通信するための「窓口」です。生成AIのAPIを使うと、プログラムから直接AIモデルにリクエストを送り、応答を受け取ることができます。

```
┌──────────────┐     HTTPリクエスト      ┌──────────────┐
│              │ ──────────────────────> │              │
│  あなたの     │   (プロンプト+設定)      │  生成AI      │
│  アプリ       │                        │  サーバー     │
│              │ <────────────────────── │              │
└──────────────┘     HTTPレスポンス       └──────────────┘
                   (生成されたテキスト)
```

### REST APIの基本構造

生成AI APIのほとんどはREST（Representational State Transfer）形式を採用しています。

| 要素 | 説明 | 例 |
|------|------|-----|
| エンドポイント（Endpoint） | APIの接続先URL | `https://api.anthropic.com/v1/messages` |
| HTTPメソッド（Method） | 操作の種類 | `POST`（データ送信） |
| ヘッダー（Headers） | 認証情報や形式指定 | `x-api-key: sk-ant-...` |
| リクエストボディ（Body） | 送信するデータ本体 | JSON形式のプロンプト |
| レスポンス（Response） | サーバーからの応答 | JSON形式の生成結果 |

### 認証の仕組み

APIを利用するにはAPIキー（API Key）が必要です。APIキーは「鍵」のようなもので、誰がリクエストを送っているかを識別し、利用料金の計算に使われます。

```
APIキー取得の流れ：

1. サービスのWebサイトでアカウント作成
2. ダッシュボードでAPIキーを発行
3. キーを安全に保管（環境変数を推奨）
4. リクエスト時にヘッダーに含めて送信
```

**環境変数でAPIキーを管理する方法（推奨）：**

```bash
# .env ファイルに記載（※ .gitignore に必ず追加すること）
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

```python
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
```

> **よくある間違い**
> - APIキーをソースコードに直接書いてしまう（GitHubに公開されると不正利用される）
> - APIキーを `.gitignore` に含めずにリポジトリにコミットしてしまう
> - 本番用と開発用のAPIキーを分けていない

### リクエストとレスポンスの構造

典型的なリクエスト（Anthropic APIの例）：

```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": "Pythonでフィボナッチ数列を生成する関数を書いてください"
    }
  ]
}
```

典型的なレスポンス：

```json
{
  "id": "msg_01234567890",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "以下はPythonでフィボナッチ数列を生成する関数です..."
    }
  ],
  "model": "claude-sonnet-4-20250514",
  "usage": {
    "input_tokens": 25,
    "output_tokens": 150
  }
}
```

**ポイントまとめ**
- 生成AI APIはREST形式で、HTTPリクエストを送って応答を受け取る
- 認証にはAPIキーを使い、環境変数で安全に管理する
- レスポンスにはトークン使用量が含まれ、コスト管理に活用できる

---

## 7.2 主要APIの比較

### Anthropic API（Claude）

Anthropic社が提供するClaude APIです。長文処理や複雑な推論に強みがあります。

| 項目 | 内容 |
|------|------|
| エンドポイント | `https://api.anthropic.com/v1/messages` |
| 認証ヘッダー | `x-api-key` |
| 主要モデル | Claude Opus 4, Claude Sonnet 4 |
| 最大コンテキスト | 200Kトークン |
| 特徴 | 長文理解、安全性重視、日本語品質が高い |

### OpenAI API（GPT）

OpenAI社が提供するGPTシリーズのAPIです。最も広く利用されています。

| 項目 | 内容 |
|------|------|
| エンドポイント | `https://api.openai.com/v1/chat/completions` |
| 認証ヘッダー | `Authorization: Bearer sk-...` |
| 主要モデル | GPT-4o, GPT-4o mini |
| 最大コンテキスト | 128Kトークン |
| 特徴 | エコシステムが豊富、プラグイン連携 |

### Google AI API（Gemini）

Google社が提供するGeminiシリーズのAPIです。マルチモーダル（Multimodal）対応が充実しています。

| 項目 | 内容 |
|------|------|
| エンドポイント | `https://generativelanguage.googleapis.com/v1beta/` |
| 認証 | APIキーまたはOAuth 2.0 |
| 主要モデル | Gemini 2.0 Flash, Gemini 2.5 Pro |
| 最大コンテキスト | 1Mトークン（Gemini 2.5 Pro） |
| 特徴 | マルチモーダル、Google Workspace連携 |

### 料金比較（目安・2026年時点）

```
コスト比較イメージ（入力100万トークンあたり）：

 低コスト ◄─────────────────────────────► 高コスト

 GPT-4o mini    Claude Sonnet 4    GPT-4o    Claude Opus 4
   $0.15           $3.00           $2.50        $15.00
```

> **よくある間違い**
> - 1つのAPIだけに依存してしまう（障害時に業務が停止する）
> - モデルの性能だけで選び、コストやレイテンシーを考慮しない
> - 最新・最高性能モデルを常に使ってしまう（用途に合った選択が重要）

**ポイントまとめ**
- 各社APIはエンドポイントや認証方式が異なるが、基本的な構造は共通
- 用途・コスト・品質のバランスでモデルを選択する
- フォールバック（Fallback）として複数APIに対応しておくと安心

---

## 7.3 Pythonでの実装例

### 事前準備

```bash
# 必要なパッケージのインストール
pip install anthropic openai python-dotenv
```

### Anthropic SDK を使った基本実装

```python
"""
Anthropic API (Claude) の基本的な呼び出し例
学べる内容：APIクライアントの初期化、メッセージ送信、レスポンス取得
実行方法：python basic_anthropic.py
"""
import os
from dotenv import load_dotenv
import anthropic

# 環境変数の読み込み
load_dotenv()

# クライアントの初期化（環境変数 ANTHROPIC_API_KEY を自動的に使用）
client = anthropic.Anthropic()

# メッセージの送信
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "日本の四季について、それぞれ一言で説明してください。"
        }
    ]
)

# レスポンスの表示
print(message.content[0].text)
print(f"\n--- 使用トークン ---")
print(f"入力: {message.usage.input_tokens} トークン")
print(f"出力: {message.usage.output_tokens} トークン")
```

### システムプロンプトを使った実装

```python
"""
システムプロンプトでAIの役割を定義する例
"""
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="あなたはプロの料理研究家です。家庭で簡単に作れるレシピを提案してください。材料は5つ以内、手順は3ステップ以内で説明してください。",
    messages=[
        {
            "role": "user",
            "content": "冷蔵庫に卵と玉ねぎがあります。何が作れますか？"
        }
    ]
)

print(message.content[0].text)
```

### 会話履歴を保持するチャット実装

```python
"""
複数回のやり取り（マルチターン）を行うチャットボットの例
"""
import anthropic

client = anthropic.Anthropic()
conversation_history = []

def chat(user_message: str) -> str:
    """ユーザーのメッセージを送信し、応答を返す"""
    # ユーザーメッセージを履歴に追加
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # APIリクエスト送信
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="あなたは親切なアシスタントです。簡潔に回答してください。",
        messages=conversation_history
    )

    # アシスタントの応答を履歴に追加
    assistant_message = response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })

    return assistant_message

# 使用例
print(chat("Pythonとは何ですか？"))
print("---")
print(chat("その特徴を3つ教えてください。"))  # 前の文脈を踏まえて回答
print("---")
print(chat("その中で一番重要なのは？"))  # さらに文脈を踏まえる
```

### ストリーミング出力の実装

```python
"""
ストリーミング（Streaming）でリアルタイムに応答を表示する例
"""
import anthropic

client = anthropic.Anthropic()

# ストリーミングでメッセージを送信
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "日本の有名な祭りを5つ紹介してください。"
        }
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

print()  # 最終改行
```

### エラーハンドリング

```python
"""
API呼び出し時のエラー処理パターン
"""
import anthropic
import time

client = anthropic.Anthropic()

def safe_api_call(messages: list, max_retries: int = 3) -> str:
    """リトライ機能付きのAPI呼び出し"""
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=messages
            )
            return response.content[0].text

        except anthropic.RateLimitError:
            # レート制限に達した場合、待機してリトライ
            wait_time = 2 ** attempt  # 指数バックオフ
            print(f"レート制限に達しました。{wait_time}秒待機します...")
            time.sleep(wait_time)

        except anthropic.APIConnectionError:
            print("接続エラーが発生しました。ネットワークを確認してください。")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise

        except anthropic.APIStatusError as e:
            print(f"APIエラー: ステータス {e.status_code}")
            raise

    raise Exception("最大リトライ回数に達しました")

# 使用例
result = safe_api_call([
    {"role": "user", "content": "こんにちは"}
])
print(result)
```

> **よくある間違い**
> - エラーハンドリングを実装せず、API障害で全体が停止する
> - リトライ時に待機時間を入れず、レート制限をさらに悪化させる
> - 会話履歴を無制限に蓄積し、トークン上限を超えてしまう

**ポイントまとめ**
- Anthropic SDKを使えば数行でAPI呼び出しが可能
- 会話履歴はリスト形式で管理し、毎回のリクエストに含める
- ストリーミングでUXを向上させ、エラーハンドリングで信頼性を確保する

---

## 7.4 ノーコード/ローコードツール連携

### 主要ツールの比較

コードを書かずに（ノーコード（No-Code））、または最小限のコードで（ローコード（Low-Code））生成AIを組み込めるツールが増えています。

| ツール | 特徴 | 料金目安 | 向いている用途 |
|--------|------|----------|----------------|
| Zapier | 最大級のアプリ連携数 | 無料〜月$20+ | 既存SaaSツール間の連携 |
| Make (旧Integromat) | 視覚的なフロー設計 | 無料〜月$9+ | 複雑な分岐処理 |
| Dify | AIアプリ構築特化 | OSS（無料）〜 | RAG、チャットボット |
| n8n | セルフホスト可能 | OSS（無料）〜 | データ処理、社内ツール |

### 自動化の例：メール要約ワークフロー

```
Zapier での構成例：

┌─────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐
│ Gmail   │───>│ フィルタ  │───>│ Claude   │───>│ Slack   │
│ 新着受信 │    │ 条件分岐  │    │ 要約生成  │    │ 通知送信 │
└─────────┘    └──────────┘    └──────────┘    └─────────┘

トリガー:        条件:           アクション:      アクション:
新着メール受信   件名に「重要」   メール本文を     要約をSlackの
                を含む          3行に要約        #通知チャンネルに投稿
```

### Difyを使ったRAGチャットボットの構築

Dify（ディファイ）はオープンソースのAIアプリ開発プラットフォームです。RAG（Retrieval-Augmented Generation：検索拡張生成）を簡単に実装できます。

```
Dify RAGチャットボットの構成：

┌─────────────────────────────────────────────┐
│  Dify プラットフォーム                        │
│                                             │
│  ┌──────┐   ┌───────────┐   ┌───────────┐  │
│  │ 文書  │──>│ ベクトル   │──>│ ナレッジ   │  │
│  │ アップ │   │ 変換      │   │ ベース     │  │
│  └──────┘   └───────────┘   └─────┬─────┘  │
│                                   │        │
│  ┌──────┐                   ┌─────▼─────┐  │
│  │ ユーザ │──────────────────>│ AI応答生成 │  │
│  │ 質問  │                   │(検索+生成) │  │
│  └──────┘                   └───────────┘  │
└─────────────────────────────────────────────┘
```

**ポイントまとめ**
- ノーコードツールを使えばプログラミング不要でAI自動化が可能
- 用途に応じてツールを選択（SaaS連携ならZapier、AI特化ならDify）
- セルフホスト型（n8n、Dify OSS）はデータを社内に留めたい場合に有効

---

## 7.5 ワークフロー自動化の設計

### 自動化設計の3要素

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  トリガー     │───>│  処理フロー   │───>│  アクション   │
│  (Trigger)   │    │  (Process)   │    │  (Action)    │
│              │    │              │    │              │
│  何がきっかけ │    │  何をするか   │    │  結果をどう   │
│  で動くか     │    │              │    │  するか       │
└──────────────┘    └──────────────┘    └──────────────┘
```

### トリガーの種類

| トリガー種別 | 例 | 適用場面 |
|---|---|---|
| 時間ベース | 毎朝9時に実行 | 日次レポート生成 |
| イベントベース | メール受信時 | 問い合わせ自動応答 |
| Webhook | 外部からのHTTPリクエスト | システム間連携 |
| 手動 | ボタンクリック | オンデマンド処理 |

### 実践例：議事録自動生成ワークフロー

```python
"""
議事録の自動整形ワークフロー
入力：会議の文字起こしテキスト
出力：構造化された議事録
"""
import anthropic
from datetime import datetime

client = anthropic.Anthropic()

def generate_minutes(transcript: str, meeting_title: str) -> str:
    """文字起こしから議事録を自動生成する"""

    system_prompt = """あなたは議事録作成の専門家です。
以下のルールに従って、文字起こしテキストから議事録を作成してください：

1. 参加者の発言を要約し、議題ごとに整理する
2. 決定事項を明確にリストアップする
3. アクションアイテム（担当者・期限）を抽出する
4. 次回の議題や宿題を整理する

出力形式はMarkdownとしてください。"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": f"会議名: {meeting_title}\n日時: {datetime.now().strftime('%Y年%m月%d日')}\n\n--- 文字起こし ---\n{transcript}"
            }
        ]
    )

    return response.content[0].text

# 使用例
transcript = """
田中：では新製品の発売スケジュールについて話しましょう。
鈴木：開発は予定通り来月末に完了見込みです。
佐藤：マーケティング素材の準備は2週間必要です。
田中：では発売は再来月の15日にしましょう。鈴木さん、最終テストを来月20日までにお願いします。
鈴木：承知しました。
田中：佐藤さんはプレスリリースの草案を来週中にお願いします。
佐藤：分かりました。
"""

minutes = generate_minutes(transcript, "新製品発売スケジュール会議")
print(minutes)
```

### エラーハンドリング設計

```
エラー発生時のフロー：

  正常処理 ─────────────────────> 完了
      │
      ├── API障害 ──> リトライ（最大3回）──> 失敗通知
      │
      ├── 入力不正 ──> バリデーションエラー ──> ユーザー通知
      │
      └── タイムアウト ──> 処理中断 ──> 管理者通知
```

**ポイントまとめ**
- 自動化は「トリガー → 処理 → アクション」の3要素で設計する
- エラーハンドリングは自動化の信頼性に直結する
- 小さく始めて段階的に自動化範囲を広げるのがベストプラクティス

---

## 7.6 コスト管理と最適化

### トークンとコストの関係

生成AIの料金はトークン（Token）単位で計算されます。トークンとは、テキストを処理する最小単位のことです。

```
トークン数の目安：

英語: 1トークン ≒ 4文字 (約0.75単語)
日本語: 1トークン ≒ 1〜2文字

例：「今日はいい天気ですね」→ 約10〜12トークン
例：「Hello, world!」→ 約4トークン
```

### コスト最適化の戦略

| 戦略 | 方法 | 削減効果 |
|------|------|----------|
| モデル選択 | 簡単なタスクには軽量モデルを使う | 50〜90%削減 |
| プロンプト最適化 | 簡潔で的確な指示にする | 10〜30%削減 |
| キャッシュ活用 | 同一リクエストの結果を再利用 | 大幅削減（用途依存） |
| バッチ処理 | リクエストをまとめて送信 | API呼び出し回数削減 |
| max_tokens制限 | 出力トークン数の上限を適切に設定 | 無駄な出力を防止 |

### モデルの使い分け例

```python
"""
タスクの複雑さに応じてモデルを切り替える例
"""
import anthropic

client = anthropic.Anthropic()

def smart_call(task: str, complexity: str = "low") -> str:
    """複雑さに応じてモデルを自動選択する"""

    # タスクの複雑さに応じたモデル選択
    model_map = {
        "low": "claude-haiku-4-20250514",       # 簡単なタスク（低コスト）
        "medium": "claude-sonnet-4-20250514",    # 標準的なタスク
        "high": "claude-opus-4-20250514",        # 複雑な推論が必要なタスク
    }

    model = model_map.get(complexity, "claude-sonnet-4-20250514")

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": task}]
    )

    return response.content[0].text

# 使用例
# 簡単な分類タスク → Haiku（低コスト）
result1 = smart_call("「この商品最高！」はポジティブ？ネガティブ？", "low")

# 標準的な要約タスク → Sonnet（中コスト）
result2 = smart_call("以下の文章を3行に要約してください：...", "medium")

# 複雑な分析タスク → Opus（高コスト）
result3 = smart_call("この契約書の法的リスクを分析してください：...", "high")
```

### キャッシュの実装例

```python
"""
簡易キャッシュでAPI呼び出しを削減する例
"""
import hashlib
import json
import os
import anthropic

client = anthropic.Anthropic()
CACHE_DIR = "./api_cache"

def cached_api_call(prompt: str, model: str = "claude-sonnet-4-20250514") -> str:
    """キャッシュ付きAPI呼び出し"""

    # プロンプトからキャッシュキーを生成
    cache_key = hashlib.md5(f"{model}:{prompt}".encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.json")

    # キャッシュがあればそれを返す
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            cached = json.load(f)
        print("[キャッシュヒット] API呼び出しをスキップしました")
        return cached["response"]

    # キャッシュがなければAPIを呼び出す
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.content[0].text

    # 結果をキャッシュに保存
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump({"prompt": prompt, "response": result}, f, ensure_ascii=False)

    return result
```

### 使用量モニタリング

```python
"""
トークン使用量を記録・集計する簡易モニタリング
"""
import anthropic
from datetime import datetime

client = anthropic.Anthropic()

# 使用量の記録
usage_log = []

def tracked_call(prompt: str) -> str:
    """使用量を記録しながらAPIを呼び出す"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    # 使用量を記録
    usage_log.append({
        "timestamp": datetime.now().isoformat(),
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "model": "claude-sonnet-4-20250514"
    })

    return response.content[0].text

def print_usage_summary():
    """使用量のサマリーを表示"""
    total_input = sum(log["input_tokens"] for log in usage_log)
    total_output = sum(log["output_tokens"] for log in usage_log)

    print(f"=== 使用量サマリー ===")
    print(f"API呼び出し回数: {len(usage_log)}")
    print(f"入力トークン合計: {total_input:,}")
    print(f"出力トークン合計: {total_output:,}")
    print(f"合計トークン: {total_input + total_output:,}")
```

> **よくある間違い**
> - すべてのタスクに最高性能のモデルを使い、コストが急増する
> - キャッシュを使わず、同じ質問に対して毎回APIを呼び出す
> - トークン使用量をモニタリングせず、月末に請求額に驚く
> - max_tokensを不必要に大きく設定して無駄なトークンを消費する

**ポイントまとめ**
- タスクの複雑さに応じてモデルを使い分けるのが最大のコスト削減策
- キャッシュを活用して同一リクエストのAPI呼び出しを削減する
- 使用量を定期的にモニタリングし、予算超過を防ぐ
- Anthropic APIの Prompt Caching 機能も積極的に活用する

---

## まとめ

本章では、生成AI APIの基本からPythonでの実装、ノーコードツール連携、ワークフロー自動化、コスト管理まで幅広く学びました。

```
学習の全体像：

  API基本     →  主要API比較   →  Python実装
  (7.1)          (7.2)           (7.3)
                                    │
  コスト管理  ←  ワークフロー  ←  ノーコード連携
  (7.6)         設計 (7.5)       (7.4)
```

次章では、生成AIの利用に伴う倫理的課題、法的規制、リスク管理について学びます。技術を正しく活用するための知識を身につけましょう。

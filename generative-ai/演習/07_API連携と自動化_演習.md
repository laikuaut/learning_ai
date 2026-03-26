# 第7章 演習：API連携と自動化

---

## 基本問題

### 問題1：REST APIの基本概念

REST APIで使用される以下のHTTPメソッドについて、それぞれの役割と使用場面を説明してください。

- GET
- POST
- PUT
- DELETE

また、生成AI APIを呼び出す際に最も頻繁に使用されるメソッドはどれか、その理由とともに答えてください。

<details>
<summary>ヒント</summary>

REST APIのHTTPメソッドは、CRUD操作（Create, Read, Update, Delete）に対応しています。生成AI APIでは、モデルにテキストを「送信」してレスポンスを受け取る操作が中心です。
</details>

<details>
<summary>解答例</summary>

```
■ 各HTTPメソッドの役割

| メソッド | 役割           | 使用場面                         |
|---------|---------------|----------------------------------|
| GET     | リソースの取得  | モデル一覧の取得、使用量の確認      |
| POST    | リソースの作成  | テキスト生成リクエストの送信        |
| PUT     | リソースの更新  | 設定情報の更新、ファインチューニング |
| DELETE  | リソースの削除  | APIキーの無効化、データの削除       |

■ 最も頻繁に使用されるメソッド：POST

理由：
- 生成AI APIでは、プロンプト（入力テキスト）をサーバーに送信し、
  生成結果を受け取るのが主な操作です
- この「データを送信して新しいリソース（生成テキスト）を作成する」
  操作はPOSTメソッドに該当します
- Anthropic API、OpenAI APIともにメッセージ生成エンドポイントは
  POST /v1/messages（またはPOST /v1/chat/completions）です
```
</details>

---

### 問題2：API認証方式の理解

以下の3つのAPI認証方式について、仕組みとメリット・デメリットを整理してください。

1. APIキー認証
2. OAuth 2.0
3. JWT（JSON Web Token）

生成AI APIで最も一般的に使用されている方式はどれか、その理由も説明してください。

<details>
<summary>ヒント</summary>

認証方式の選択は「セキュリティレベル」「実装の手軽さ」「用途」によって異なります。生成AI APIは通常、サーバー間通信（バックエンド→API）で使用される点に着目してください。
</details>

<details>
<summary>解答例</summary>

```
■ 認証方式の比較

1. APIキー認証
   仕組み：固定の文字列をリクエストヘッダーに含めて認証
   メリット：実装が簡単、すぐに利用開始できる
   デメリット：キーが漏洩すると不正利用される、権限の細かい制御が難しい

2. OAuth 2.0
   仕組み：認可サーバーからアクセストークンを取得し、それを使って認証
   メリット：権限の範囲を細かく制御可能、トークンに有効期限がある
   デメリット：実装が複雑、認可フローの理解が必要

3. JWT（JSON Web Token）
   仕組み：署名付きのJSONトークンで認証情報を伝達
   メリット：サーバー側で状態を保持しなくてよい（ステートレス）
   デメリット：トークンサイズが大きい、一度発行すると無効化が難しい

■ 生成AI APIで最も一般的な方式：APIキー認証

理由：
- サーバー間通信が主な用途であり、シンプルな認証で十分
- 開発者がすぐに利用を開始できる手軽さを重視
- ダッシュボードからキーの発行・無効化が容易
- 例：Anthropic APIは x-api-key ヘッダーにAPIキーを設定
- 例：OpenAI APIは Authorization: Bearer <APIキー> で認証
```
</details>

---

### 問題3：APIレスポンスの解析

以下のAnthropic API（Claude）のレスポンスJSON（簡略版）を読み、各フィールドの意味を説明してください。また、生成されたテキストの本文と、使用されたトークン数を抽出してください。

```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Pythonでファイルを読み込むには、open()関数を使用します。"
    }
  ],
  "model": "claude-sonnet-4-20250514",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 25,
    "output_tokens": 42
  }
}
```

**期待される出力例：**
```
本文: Pythonでファイルを読み込むには、open()関数を使用します。
入力トークン数: 25
出力トークン数: 42
合計トークン数: 67
```

<details>
<summary>ヒント</summary>

JSONレスポンスの `content` フィールドは配列になっています。テキストは `content[0].text` でアクセスできます。トークン数は `usage` オブジェクト内にあります。
</details>

<details>
<summary>解答例</summary>

```
■ 各フィールドの説明

| フィールド     | 意味                                         |
|--------------|----------------------------------------------|
| id           | メッセージの一意な識別子                        |
| type         | レスポンスの種類（"message" = 通常のメッセージ） |
| role         | 発言者の役割（"assistant" = AIの応答）          |
| content      | 生成されたコンテンツの配列                      |
| content.type | コンテンツの種類（"text" = テキスト）            |
| content.text | 生成されたテキスト本文                          |
| model        | 使用されたモデルの名前                          |
| stop_reason  | 生成が停止した理由（"end_turn" = 正常終了）      |
| usage        | トークン使用量の情報                            |

■ Pythonでの抽出コード

import json

# response_dataはAPIレスポンスを格納した辞書
response_data = {  # 上記のJSONデータ  }

# テキスト本文の抽出
text = response_data["content"][0]["text"]
print(f"本文: {text}")

# トークン数の抽出
input_tokens = response_data["usage"]["input_tokens"]
output_tokens = response_data["usage"]["output_tokens"]
total_tokens = input_tokens + output_tokens

print(f"入力トークン数: {input_tokens}")
print(f"出力トークン数: {output_tokens}")
print(f"合計トークン数: {total_tokens}")

# 出力：
# 本文: Pythonでファイルを読み込むには、open()関数を使用します。
# 入力トークン数: 25
# 出力トークン数: 42
# 合計トークン数: 67
```
</details>

---

## 応用問題

### 問題4：Anthropic APIを使ったPythonコード作成

Anthropic API（Claude）を呼び出して、テキストを生成するPythonスクリプトを作成してください。以下の要件を満たすこと。

**要件：**
- `anthropic` ライブラリを使用すること
- 環境変数 `ANTHROPIC_API_KEY` からAPIキーを取得すること
- システムプロンプトに「あなたは丁寧なプログラミング講師です」を設定
- ユーザーメッセージを引数で受け取れること
- レスポンスから生成テキストとトークン使用量を表示すること

**期待される出力例：**
```
=== Claude API レスポンス ===
生成テキスト:
Pythonの変数は、データを格納する名前付きの箱のようなものです。
...（以下略）

トークン使用量:
  入力: 35 tokens
  出力: 128 tokens
  合計: 163 tokens
```

<details>
<summary>ヒント</summary>

`anthropic` ライブラリでは `anthropic.Anthropic()` でクライアントを作成し、`client.messages.create()` でメッセージを生成します。環境変数の取得には `os.environ.get()` を使います。
</details>

<details>
<summary>解答例</summary>

```python
import os
import sys
import anthropic

def generate_response(user_message: str) -> None:
    """Anthropic APIを呼び出してテキストを生成する"""

    # APIキーの取得（環境変数から自動的に読み込まれる）
    # ANTHROPIC_API_KEY が設定されていない場合はエラーになる
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("エラー: 環境変数 ANTHROPIC_API_KEY が設定されていません。")
        sys.exit(1)

    # クライアントの作成
    client = anthropic.Anthropic(api_key=api_key)

    # APIリクエスト
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="あなたは丁寧なプログラミング講師です。",
        messages=[
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    # レスポンスの表示
    print("=== Claude API レスポンス ===")
    print("生成テキスト:")
    print(response.content[0].text)
    print()
    print("トークン使用量:")
    print(f"  入力: {response.usage.input_tokens} tokens")
    print(f"  出力: {response.usage.output_tokens} tokens")
    total = response.usage.input_tokens + response.usage.output_tokens
    print(f"  合計: {total} tokens")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python api_call.py '質問文'")
        sys.exit(1)

    user_message = sys.argv[1]
    generate_response(user_message)

# 実行例:
# python api_call.py "Pythonの変数について教えてください"
```
</details>

---

### 問題5：エラーハンドリングの実装

問題4のコードを拡張し、以下のエラーケースに対応するエラーハンドリングを追加してください。

**対応すべきエラー：**
1. APIキー未設定・無効
2. レートリミット超過（HTTP 429）
3. サーバーエラー（HTTP 500系）
4. ネットワークタイムアウト
5. 不正なリクエスト（HTTP 400）

**要件：**
- 各エラーに対して適切なエラーメッセージを表示すること
- レートリミット超過時はリトライ処理を実装すること（最大3回、指数バックオフ）
- エラー内容をログに記録すること

**期待される出力例（レートリミット時）：**
```
警告: レートリミットに達しました。10秒後にリトライします... (1/3)
警告: レートリミットに達しました。20秒後にリトライします... (2/3)
=== Claude API レスポンス ===
生成テキスト:
...
```

<details>
<summary>ヒント</summary>

`anthropic` ライブラリは特定の例外クラスを提供しています。`anthropic.RateLimitError`、`anthropic.APIStatusError` などを使い分けます。指数バックオフは `time.sleep(base_wait * (2 ** attempt))` で実装できます。
</details>

<details>
<summary>解答例</summary>

```python
import os
import sys
import time
import logging
import anthropic

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("api_calls.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

MAX_RETRIES = 3       # 最大リトライ回数
BASE_WAIT = 10        # 基本待機時間（秒）

def call_api_with_retry(client, user_message: str, retries: int = MAX_RETRIES):
    """リトライ機能付きAPI呼び出し"""

    for attempt in range(retries):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system="あなたは丁寧なプログラミング講師です。",
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            return response

        except anthropic.RateLimitError as e:
            # レートリミット超過 → リトライ
            wait_time = BASE_WAIT * (2 ** attempt)
            logger.warning(
                f"レートリミットに達しました。"
                f"{wait_time}秒後にリトライします... "
                f"({attempt + 1}/{retries})"
            )
            if attempt < retries - 1:
                time.sleep(wait_time)
            else:
                logger.error("リトライ回数の上限に達しました。")
                raise

        except anthropic.AuthenticationError as e:
            # APIキー無効（HTTP 401）
            logger.error(f"認証エラー: APIキーが無効です。 詳細: {e}")
            raise

        except anthropic.BadRequestError as e:
            # 不正なリクエスト（HTTP 400）
            logger.error(f"リクエストエラー: {e}")
            raise

        except anthropic.InternalServerError as e:
            # サーバーエラー（HTTP 500系）
            wait_time = BASE_WAIT * (2 ** attempt)
            logger.warning(
                f"サーバーエラーが発生しました。"
                f"{wait_time}秒後にリトライします... "
                f"({attempt + 1}/{retries})"
            )
            if attempt < retries - 1:
                time.sleep(wait_time)
            else:
                logger.error("サーバーエラーが継続しています。")
                raise

        except anthropic.APITimeoutError as e:
            # タイムアウト
            logger.error(f"タイムアウト: APIからの応答がありません。 詳細: {e}")
            raise

        except anthropic.APIConnectionError as e:
            # ネットワーク接続エラー
            logger.error(f"接続エラー: ネットワークを確認してください。 詳細: {e}")
            raise

    return None

def main():
    # APIキーの確認
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("環境変数 ANTHROPIC_API_KEY が設定されていません。")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("使い方: python api_call_robust.py '質問文'")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    user_message = sys.argv[1]

    try:
        response = call_api_with_retry(client, user_message)
        if response:
            print("=== Claude API レスポンス ===")
            print("生成テキスト:")
            print(response.content[0].text)
            print()
            print("トークン使用量:")
            print(f"  入力: {response.usage.input_tokens} tokens")
            print(f"  出力: {response.usage.output_tokens} tokens")
            total = response.usage.input_tokens + response.usage.output_tokens
            print(f"  合計: {total} tokens")
            logger.info(f"API呼び出し成功 - トークン: {total}")
    except Exception as e:
        logger.error(f"API呼び出しに失敗しました: {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```
</details>

---

### 問題6：ストリーミングレスポンスの実装

Anthropic APIのストリーミング機能を使って、生成テキストをリアルタイムに表示するPythonスクリプトを作成してください。

**要件：**
- ストリーミングでトークンが到着するたびに即座に表示すること
- 生成完了後にトークン使用量のサマリーを表示すること
- 通常モードとストリーミングモードを `--stream` フラグで切り替えられること

**期待される出力例（ストリーミング時）：**
```
[ストリーミングモード]
Python の 変数 は 、 データ を 格納 する ための 名前 付き の 容器 です 。...

--- 生成完了 ---
入力トークン: 30
出力トークン: 95
```

<details>
<summary>ヒント</summary>

ストリーミングは `client.messages.stream()` をコンテキストマネージャとして使用します。`with client.messages.stream(...) as stream:` の形で呼び出し、`stream.text_stream` でテキストチャンクを逐次取得できます。
</details>

<details>
<summary>解答例</summary>

```python
import os
import sys
import anthropic

def stream_response(client, user_message: str) -> None:
    """ストリーミングモードでAPIを呼び出す"""
    print("[ストリーミングモード]")

    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="あなたは丁寧なプログラミング講師です。",
        messages=[
            {"role": "user", "content": user_message}
        ]
    ) as stream:
        # テキストチャンクを逐次表示
        for text in stream.text_stream:
            print(text, end="", flush=True)

        print()  # 改行

    # ストリーム完了後、最終メッセージからトークン使用量を取得
    final_message = stream.get_final_message()
    print()
    print("--- 生成完了 ---")
    print(f"入力トークン: {final_message.usage.input_tokens}")
    print(f"出力トークン: {final_message.usage.output_tokens}")

def normal_response(client, user_message: str) -> None:
    """通常モードでAPIを呼び出す"""
    print("[通常モード]")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="あなたは丁寧なプログラミング講師です。",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    print(response.content[0].text)
    print()
    print("--- 生成完了 ---")
    print(f"入力トークン: {response.usage.input_tokens}")
    print(f"出力トークン: {response.usage.output_tokens}")

def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("エラー: 環境変数 ANTHROPIC_API_KEY が設定されていません。")
        sys.exit(1)

    # --stream フラグの判定
    use_stream = "--stream" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--stream"]

    if not args:
        print("使い方: python streaming.py [--stream] '質問文'")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    user_message = args[0]

    if use_stream:
        stream_response(client, user_message)
    else:
        normal_response(client, user_message)

if __name__ == "__main__":
    main()

# 実行例:
# python streaming.py --stream "Pythonのリスト内包表記について教えてください"
# python streaming.py "Pythonのリスト内包表記について教えてください"
```
</details>

---

## チャレンジ問題

### 問題7：ワークフロー自動化システムの設計

あなたは社内のカスタマーサポートチームから、以下の業務を自動化するシステムの設計を依頼されました。

**自動化したい業務フロー：**
1. メールで届く問い合わせを受信する
2. 生成AIで問い合わせ内容を分類する（技術的質問 / 請求関連 / クレーム / その他）
3. 分類結果に応じて適切な部署の担当者に振り分ける
4. 生成AIで回答のドラフトを作成する
5. 担当者がドラフトを確認・編集して返信する

**設計要件：**
- システム構成図（どのサービス/APIをどう連携させるか）
- APIコール数の見積もり（1日あたり500件の問い合わせを想定）
- 月間コストの試算（Anthropic APIの料金体系を使用）
- エラー発生時のフォールバック戦略
- セキュリティ上の考慮事項

**期待される出力例（コスト試算部分）：**
```
■ 月間コスト試算

前提条件：
  - 1日あたり500件の問い合わせ
  - 月間稼働日数：22日
  - 月間総件数：11,000件
  - モデル：Claude Sonnet（入力 $3/100万トークン、出力 $15/100万トークン）

1. 分類処理（1件あたり）
   入力: 問い合わせ文（平均500トークン）+ システムプロンプト（200トークン）= 700トークン
   出力: 分類結果（約50トークン）
   月間: 700 × 11,000 = 7,700,000 入力トークン → $23.10
         50 × 11,000 = 550,000 出力トークン → $8.25

2. ドラフト作成（1件あたり）
   入力: 問い合わせ文 + コンテキスト（平均1,000トークン）+ システムプロンプト（500トークン）= 1,500トークン
   出力: 回答ドラフト（平均400トークン）
   月間: 1,500 × 11,000 = 16,500,000 入力トークン → $49.50
         400 × 11,000 = 4,400,000 出力トークン → $66.00

月間API費用合計: 約 $146.85（約22,000円）
※ 為替レート1ドル=150円で計算
```

<details>
<summary>ヒント</summary>

以下の観点で設計を進めてください。

1. システム構成：メール受信（IMAP/Webhook）→ 分類API → 振り分けロジック → ドラフト生成API → 承認UI
2. コスト試算：各処理ステップごとにトークン数を見積もり、Anthropic APIの料金表を適用
3. フォールバック：API障害時は人間にエスカレーション、キューイングで処理を遅延させる
4. セキュリティ：個人情報のマスキング、APIキーの安全な管理、通信の暗号化
</details>

<details>
<summary>解答例</summary>

```
■ システム構成図

[メール受信]
    │
    ▼
[メールサーバー (IMAP/Webhook)]
    │
    ▼
[メッセージキュー (例: Amazon SQS)]
    │
    ▼
[分類サービス] ──→ [Anthropic API: Claude]
    │                  分類プロンプト実行
    ▼
[振り分けロジック]
    │
    ├─→ 技術的質問 → 技術サポートチーム
    ├─→ 請求関連   → 経理チーム
    ├─→ クレーム   → カスタマーサクセスチーム
    └─→ その他     → 一般サポートチーム
    │
    ▼
[ドラフト生成サービス] ──→ [Anthropic API: Claude]
    │                         ドラフト生成プロンプト実行
    ▼
[承認UI (Webダッシュボード)]
    │
    ▼
[担当者が確認・編集]
    │
    ▼
[メール返信送信]

■ APIコール数の見積もり（1日あたり）

| 処理            | 1件あたりの呼び出し数 | 1日の件数 | 1日の呼び出し数 |
|----------------|--------------------:|----------:|--------------:|
| 分類処理         | 1回                | 500件     | 500回         |
| ドラフト作成      | 1回                | 500件     | 500回         |
| リトライ（5%想定）| -                  | -         | 50回          |
| 合計            | -                  | -         | 1,050回       |

月間APIコール数: 1,050 × 22日 = 23,100回

■ 月間コスト試算

前提条件：
  - モデル：Claude Sonnet
  - 入力: $3 / 100万トークン
  - 出力: $15 / 100万トークン
  - 月間件数：11,000件

1. 分類処理
   入力トークン: (問い合わせ文500 + システムプロンプト200) × 11,000 = 7,700,000
   出力トークン: 50 × 11,000 = 550,000
   コスト: ($3 × 7.7) + ($15 × 0.55) = $23.10 + $8.25 = $31.35

2. ドラフト生成
   入力トークン: (問い合わせ文500 + コンテキスト500 + システムプロンプト500) × 11,000 = 16,500,000
   出力トークン: 400 × 11,000 = 4,400,000
   コスト: ($3 × 16.5) + ($15 × 4.4) = $49.50 + $66.00 = $115.50

3. リトライ処理（5%分）
   分類: $31.35 × 0.05 = $1.57
   ドラフト: $115.50 × 0.05 = $5.78
   リトライコスト: $7.35

月間API費用合計: $31.35 + $115.50 + $7.35 = $154.20（約23,100円）
※ 為替レート1ドル=150円で計算

■ エラー発生時のフォールバック戦略

1. API一時障害（レートリミット、500エラー）
   → メッセージキューに戻し、指数バックオフでリトライ（最大5回）
   → リトライ上限到達後は「手動対応キュー」に移動

2. API長期障害
   → 分類処理: ルールベースのキーワードマッチングで暫定分類
   → ドラフト生成: テンプレート返信を使用（「確認中です」等）
   → 管理者にアラート通知

3. 分類精度が低い場合
   → 信頼度スコアが閾値（0.8）未満の場合は人間がレビュー
   → 分類結果のフィードバックを蓄積し、プロンプトを定期改善

4. 個別リクエスト失敗
   → Dead Letter Queue（DLQ）に格納
   → 日次バッチで再処理 or 手動確認

■ セキュリティ上の考慮事項

1. 個人情報の保護
   - APIに送信する前に個人情報（氏名、住所、電話番号等）をマスキング
   - マスキングした情報はローカルDBに保持し、返信時に復元
   - 例: "田中太郎" → "[NAME_001]"

2. APIキーの管理
   - 環境変数またはシークレットマネージャー（AWS Secrets Manager等）で管理
   - ソースコードにAPIキーをハードコードしない
   - キーのローテーションを定期的に実施（90日ごと）

3. 通信の暗号化
   - HTTPS通信のみ使用（TLS 1.2以上）
   - 社内ネットワークからのみAPIアクセスを許可（IP制限）

4. データ保持ポリシー
   - APIプロバイダーのデータ保持ポリシーを確認
   - 機密性の高い問い合わせはAPI送信対象から除外するルールを設定
   - 監査ログを最低1年間保持

5. アクセス制御
   - 承認UIへのアクセスは担当者のみ（RBAC）
   - 操作ログを記録し、不正利用を検知
```
</details>

---

### 問題8：マルチステップAPIパイプラインの実装設計

以下の要件を満たす「技術ブログ自動生成パイプライン」を設計し、主要部分のPythonコードを作成してください。

**パイプラインの流れ：**
1. トピックのキーワードを入力として受け取る
2. Step 1: キーワードからブログ記事のアウトラインを生成する
3. Step 2: アウトラインの各セクションについて本文を生成する
4. Step 3: 生成された記事全体を校正・改善する
5. 最終結果をMarkdownファイルとして出力する

**要件：**
- 各ステップの入出力を明確に定義すること
- 各ステップ間でコンテキスト（前のステップの出力）を適切に引き継ぐこと
- 途中経過を表示すること
- 合計トークン使用量とコストを計算して表示すること

**期待される出力例：**
```
=== 技術ブログ自動生成パイプライン ===
トピック: Pythonの型ヒント

[Step 1/3] アウトライン生成中...
  → 5セクションのアウトラインを生成しました

[Step 2/3] 本文生成中...
  → セクション 1/5: 型ヒントとは 完了 (245トークン)
  → セクション 2/5: 基本的な型アノテーション 完了 (312トークン)
  → セクション 3/5: 複雑な型の表現 完了 (289トークン)
  → セクション 4/5: mypyによる静的型チェック 完了 (276トークン)
  → セクション 5/5: 実践的なベストプラクティス 完了 (298トークン)

[Step 3/3] 校正・改善中...
  → 校正完了

=== 完了 ===
出力ファイル: output/python-type-hints.md
合計トークン使用量:
  入力: 12,450 tokens
  出力: 4,820 tokens
  合計: 17,270 tokens
推定コスト: $0.11
```

<details>
<summary>ヒント</summary>

パイプラインの各ステップをそれぞれ関数として切り出すと整理しやすくなります。

1. `generate_outline(topic)` → アウトライン（セクション見出しリスト）を返す
2. `generate_section(outline, section_title)` → セクション本文を返す
3. `proofread(full_article)` → 校正済み記事を返す

各ステップの出力を次のステップの入力として渡し、トークン使用量を累積していきます。アウトラインはJSON形式で出力させると、プログラムで扱いやすくなります。
</details>

<details>
<summary>解答例</summary>

```python
import os
import sys
import json
import anthropic

class TokenTracker:
    """トークン使用量を追跡するクラス"""

    def __init__(self):
        self.total_input = 0
        self.total_output = 0

    def add(self, usage):
        self.total_input += usage.input_tokens
        self.total_output += usage.output_tokens

    def get_total(self) -> int:
        return self.total_input + self.total_output

    def estimate_cost(self, input_price=3.0, output_price=15.0) -> float:
        """コスト推定（USD）- Claude Sonnet料金"""
        input_cost = (self.total_input / 1_000_000) * input_price
        output_cost = (self.total_output / 1_000_000) * output_price
        return input_cost + output_cost

    def summary(self) -> str:
        cost = self.estimate_cost()
        return (
            f"  入力: {self.total_input:,} tokens\n"
            f"  出力: {self.total_output:,} tokens\n"
            f"  合計: {self.get_total():,} tokens\n"
            f"推定コスト: ${cost:.2f}"
        )


def call_api(client, system_prompt: str, user_prompt: str, tracker: TokenTracker) -> str:
    """API呼び出しの共通処理"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )
    tracker.add(response.usage)
    return response.content[0].text


def step1_generate_outline(client, topic: str, tracker: TokenTracker) -> list:
    """Step 1: アウトライン生成"""
    print("[Step 1/3] アウトライン生成中...")

    system_prompt = (
        "あなたは技術ブログのライターです。"
        "与えられたトピックについてブログ記事のアウトラインを作成してください。"
        "出力はJSON配列形式で、各セクションのタイトルのみを返してください。"
        '例: ["セクション1", "セクション2", "セクション3"]'
    )
    user_prompt = f"トピック: {topic}\n\n5つのセクションで構成されるアウトラインを作成してください。"

    result = call_api(client, system_prompt, user_prompt, tracker)

    # JSON部分を抽出してパース
    try:
        # レスポンスからJSON配列を抽出
        start = result.index("[")
        end = result.rindex("]") + 1
        sections = json.loads(result[start:end])
    except (ValueError, json.JSONDecodeError):
        # パース失敗時はテキストを行分割
        sections = [line.strip("- ").strip() for line in result.strip().split("\n") if line.strip()]

    print(f"  → {len(sections)}セクションのアウトラインを生成しました")
    return sections


def step2_generate_sections(client, topic: str, sections: list, tracker: TokenTracker) -> list:
    """Step 2: 各セクションの本文生成"""
    print("[Step 2/3] 本文生成中...")

    system_prompt = (
        "あなたは技術ブログのライターです。"
        "指定されたセクションについて、分かりやすい解説を書いてください。"
        "Markdownフォーマットで、コード例も含めてください。"
    )

    section_contents = []
    for i, section_title in enumerate(sections):
        user_prompt = (
            f"ブログ記事のトピック: {topic}\n"
            f"アウトライン全体: {json.dumps(sections, ensure_ascii=False)}\n\n"
            f"以下のセクションの本文を書いてください:\n"
            f"## {section_title}"
        )

        before_output = tracker.total_output
        content = call_api(client, system_prompt, user_prompt, tracker)
        tokens_used = tracker.total_output - before_output

        section_contents.append({
            "title": section_title,
            "content": content
        })
        print(f"  → セクション {i+1}/{len(sections)}: {section_title} 完了 ({tokens_used}トークン)")

    return section_contents


def step3_proofread(client, topic: str, full_article: str, tracker: TokenTracker) -> str:
    """Step 3: 校正・改善"""
    print("[Step 3/3] 校正・改善中...")

    system_prompt = (
        "あなたは技術記事の編集者です。"
        "以下の記事を校正・改善してください。"
        "修正点：誤字脱字、文章の流れ、技術的正確性、読みやすさ。"
        "改善した記事全文をMarkdown形式で出力してください。"
    )
    user_prompt = f"以下の技術ブログ記事（トピック: {topic}）を校正してください:\n\n{full_article}"

    result = call_api(client, system_prompt, user_prompt, tracker)
    print("  → 校正完了")
    return result


def assemble_article(topic: str, sections: list) -> str:
    """セクションを結合して記事全文を組み立てる"""
    article = f"# {topic}\n\n"
    for section in sections:
        article += f"## {section['title']}\n\n"
        article += section["content"] + "\n\n"
    return article


def save_article(topic: str, content: str) -> str:
    """記事をMarkdownファイルとして保存する"""
    os.makedirs("output", exist_ok=True)
    # ファイル名をトピックから生成（簡易的な処理）
    filename = topic.replace(" ", "-").replace("　", "-").lower()
    filepath = f"output/{filename}.md"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("エラー: 環境変数 ANTHROPIC_API_KEY が設定されていません。")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("使い方: python blog_pipeline.py 'トピック'")
        sys.exit(1)

    topic = sys.argv[1]
    client = anthropic.Anthropic(api_key=api_key)
    tracker = TokenTracker()

    print("=== 技術ブログ自動生成パイプライン ===")
    print(f"トピック: {topic}\n")

    # Step 1: アウトライン生成
    sections = step1_generate_outline(client, topic, tracker)
    print()

    # Step 2: 各セクションの本文生成
    section_contents = step2_generate_sections(client, topic, sections, tracker)
    print()

    # 記事を組み立て
    raw_article = assemble_article(topic, section_contents)

    # Step 3: 校正・改善
    final_article = step3_proofread(client, topic, raw_article, tracker)
    print()

    # ファイルに保存
    filepath = save_article(topic, final_article)

    print("=== 完了 ===")
    print(f"出力ファイル: {filepath}")
    print("合計トークン使用量:")
    print(tracker.summary())

if __name__ == "__main__":
    main()

# 実行例:
# python blog_pipeline.py "Pythonの型ヒント"
```
</details>

---

**お疲れさまでした！** この章では、生成AI APIの基本概念から実践的なコード実装、そしてワークフロー自動化の設計まで幅広く学びました。実際にAPIを呼び出すコードを書いて動かしてみることで、理解が深まります。

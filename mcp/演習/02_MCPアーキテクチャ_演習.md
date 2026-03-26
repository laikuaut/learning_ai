# 第2章 演習：MCPアーキテクチャ

## 基本問題

### 問題2-1：JSON-RPCメッセージの種類分類
以下のJSON-RPCメッセージが「Request（リクエスト）」「Response（レスポンス）」「Notification（通知）」のどれに該当するかを答えてください。

```json
(A) {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}

(B) {"jsonrpc": "2.0", "id": 1, "result": {"tools": [{"name": "get_weather"}]}}

(C) {"jsonrpc": "2.0", "method": "notifications/initialized"}

(D) {"jsonrpc": "2.0", "id": 2, "error": {"code": -32601, "message": "Method not found"}}

(E) {"jsonrpc": "2.0", "method": "notifications/tools/list_changed"}

(F) {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_weather", "arguments": {"city": "Tokyo"}}}
```

**期待される出力例：**
```
(A) Request（idとmethodの両方を持つ）
(B) Response - 成功（idとresultを持つ）
(C) Notification（methodを持つがidがない）
(D) Response - エラー（idとerrorを持つ）
(E) Notification（methodを持つがidがない）
(F) Request（idとmethodの両方を持つ）
```

<details>
<summary>ヒント</summary>

JSON-RPCメッセージの3種類は以下の構造で判別できます：

- **Request**：`id` と `method` の両方を持つ。応答を期待するメッセージです
- **Response**：`id` を持ち、`result`（成功）または `error`（失敗）を含む
- **Notification**：`method` を持つが `id` がない。応答を期待しない一方向のメッセージです

</details>

<details>
<summary>解答例</summary>

```
(A) Request
    → id: 1 と method: "tools/list" の両方を持つため、応答を期待するリクエストです

(B) Response（成功）
    → id: 1 と result を持つため、(A)のリクエストに対する成功レスポンスです

(C) Notification
    → method: "notifications/initialized" を持ちますが id がないため、通知です
    → 初期化完了を相手に知らせるメッセージで、応答は不要です

(D) Response（エラー）
    → id: 2 と error を持つため、何らかのリクエストに対するエラーレスポンスです
    → エラーコード -32601 は「Method not found（メソッド未対応）」を意味します

(E) Notification
    → method: "notifications/tools/list_changed" を持ちますが id がないため、通知です
    → ツール一覧が変更されたことをクライアントに知らせるメッセージです

(F) Request
    → id: 3 と method: "tools/call" の両方を持つため、ツール呼び出しのリクエストです
```

**まとめ：**
| 種類 | id | method | result/error |
|---|:---:|:---:|:---:|
| Request | あり | あり | なし |
| Response | あり | なし | あり |
| Notification | なし | あり | なし |

</details>

### 問題2-2：stdioとStreamable HTTPの使い分け
以下のシナリオにおいて、MCPのトランスポート方式として「stdio（標準入出力）」と「Streamable HTTP」のどちらが適切かを答え、理由を述べてください。

1. ローカルPCで動作するClaude Desktopから、同じPC上のファイルシステムMCPサーバーに接続する
2. クラウド上のAIアプリケーションから、社内ネットワーク内のデータベースMCPサーバーに接続する
3. VS Codeの拡張機能が、ローカルで起動したGit操作用MCPサーバーと通信する
4. SaaS型のAIチャットアプリから、インターネット上に公開されたMCPサーバーに接続する
5. CI/CDパイプライン内のスクリプトから、同一コンテナ内のMCPサーバーに接続する

**期待される出力例：**
```
1. stdio（同一マシン上のローカル通信のため）
2. Streamable HTTP（ネットワーク越しのリモート通信のため）
3. stdio（ローカルプロセス間通信のため）
4. Streamable HTTP（インターネット経由のリモート通信のため）
5. stdio（同一コンテナ内のローカル通信のため）
```

<details>
<summary>ヒント</summary>

2つのトランスポートの使い分けの基本原則：

- **stdio**：HostとServerが**同一マシン上**にある場合に使います。Hostがサーバープロセスを子プロセスとして起動し、標準入出力（stdin/stdout）でJSON-RPCメッセージをやり取りします
- **Streamable HTTP**：HostとServerが**異なるマシン**にある場合、またはネットワーク越しに通信する場合に使います。HTTPベースの通信で、Server-Sent Events（SSE）を利用したストリーミングにも対応します

</details>

<details>
<summary>解答例</summary>

```
1. stdio
   理由：Claude Desktopとファイルシステムサーバーは同一PC上で動作します。
   Hostがサーバープロセスを直接起動し、stdin/stdoutで通信するのが最もシンプルです。

2. Streamable HTTP
   理由：クラウド上のアプリと社内ネットワーク内のサーバーはネットワーク越しの
   通信が必要です。HTTP(S)を使うことで、ファイアウォールやプロキシも通過できます。

3. stdio
   理由：VS Codeの拡張機能とGit操作サーバーは同一マシン上で動作します。
   VS Codeがサーバープロセスを子プロセスとして起動するのが一般的です。

4. Streamable HTTP
   理由：インターネット経由のリモート接続です。
   HTTPS通信によりセキュリティも確保でき、認証ヘッダの付与も容易です。

5. stdio
   理由：同一コンテナ内のプロセス間通信です。
   ネットワークのオーバーヘッドがなく、最も効率的に通信できます。
```

**判断のフローチャート：**
```
MCPサーバーは同一マシン上にある？
  ├── はい → stdio（子プロセスとして起動、stdin/stdout通信）
  └── いいえ → Streamable HTTP（HTTP(S)経由、SSE対応）
```

</details>

### 問題2-3：ライフサイクルの順序
MCPの接続ライフサイクルにおける以下のイベントを、正しい時系列順に並べ替えてください。

(A) クライアントがサーバーのツール一覧を取得する（tools/list）
(B) クライアントが `initialized` 通知を送信する
(C) サーバーが `initialize` レスポンスで自身のケーパビリティを返す
(D) クライアントが `initialize` リクエストを送信する
(E) ユーザーの操作に応じてツールを呼び出す（tools/call）
(F) クライアントまたはサーバーが接続を終了する（close）
(G) サーバーがプロセスを起動し、接続が確立される

**期待される出力例：**
```
G → D → C → B → A → E → F
```

<details>
<summary>ヒント</summary>

MCPのライフサイクルは大きく3つのフェーズに分かれます：

1. **初期化フェーズ（Initialization）**：接続確立とケーパビリティのネゴシエーション
2. **運用フェーズ（Operation）**：実際のツール呼び出しやリソース取得
3. **終了フェーズ（Shutdown）**：接続のクリーンな終了

初期化フェーズ内の順序に注意してください。`initialized` 通知は、ケーパビリティのネゴシエーション完了を示す重要なシグナルです。

</details>

<details>
<summary>解答例</summary>

**正しい順序：**
```
G → D → C → B → A → E → F
```

**各ステップの詳細：**

| 順序 | 記号 | イベント | フェーズ |
|:---:|:---:|---|---|
| 1 | G | サーバープロセスの起動・接続確立 | 初期化 |
| 2 | D | クライアント → サーバー：`initialize` リクエスト送信（プロトコルバージョン、クライアントのケーパビリティを含む） | 初期化 |
| 3 | C | サーバー → クライアント：`initialize` レスポンス返却（サーバーのケーパビリティを含む） | 初期化 |
| 4 | B | クライアント → サーバー：`initialized` 通知送信（初期化完了の合図） | 初期化 |
| 5 | A | クライアント → サーバー：`tools/list` でツール一覧を取得 | 運用 |
| 6 | E | クライアント → サーバー：`tools/call` でツールを実行 | 運用 |
| 7 | F | 接続の終了（close） | 終了 |

**シーケンス図：**
```
  Client                    Server
    │                         │
    │  ──── (G) 接続確立 ────→ │
    │                         │
    │  ── (D) initialize ───→ │
    │                         │
    │  ←── (C) response ──── │
    │                         │
    │  ── (B) initialized ──→ │
    │                         │
    │  ── (A) tools/list ───→ │
    │  ←──── response ─────── │
    │                         │
    │  ── (E) tools/call ───→ │
    │  ←──── response ─────── │
    │                         │
    │  ──── (F) close ──────→ │
    │                         │
```

**重要なポイント：**
- `initialized` 通知はNotificationです（idなし、応答不要）
- `initialized` を送信する前に、クライアントはツール呼び出しなどの操作を行ってはいけません
- サーバーも `initialized` を受け取るまでリクエストを送信してはいけません

</details>

### 問題2-4：JSON-RPCエラーコード
以下のエラーコードが意味する内容を答えてください。また、どのような状況で発生するかを具体例とともに説明してください。

1. `-32700`
2. `-32600`
3. `-32601`
4. `-32602`
5. `-32603`

**期待される出力例：**
```
1. -32700: Parse error（パースエラー）
   例：不正なJSONが送信された場合（括弧の閉じ忘れ等）
2. -32600: Invalid Request（不正なリクエスト）
   ...
```

<details>
<summary>ヒント</summary>

これらはJSON-RPC 2.0仕様で事前に定義されたエラーコードです。-32000〜-32099の範囲はサーバー定義のエラーに予約されています。

</details>

<details>
<summary>解答例</summary>

| コード | 名称 | 説明 | 具体例 |
|---|---|---|---|
| -32700 | Parse error | 不正なJSONを受信した | `{"jsonrpc": "2.0", "method": "test"` のように閉じ括弧がないJSON |
| -32600 | Invalid Request | JSON自体は正しいがJSON-RPCリクエストとして不正 | `jsonrpc` フィールドがない、または `"2.0"` 以外の値が指定された |
| -32601 | Method not found | 指定されたメソッドが存在しない | サーバーが `tools/call` に対応していないのに呼び出された |
| -32602 | Invalid params | メソッドのパラメータが不正 | `tools/call` に必須の `name` パラメータが欠落している |
| -32603 | Internal error | サーバー内部のエラー | ツール実行中にサーバー側で例外が発生した |

**補足：**
- -32000〜-32099はサーバー定義のエラー用に予約されたコード範囲です
- MCPではこれらに加えて、独自のエラーコードを定義することもできます

</details>

---

## 応用問題

### 問題2-5：ツール呼び出しの完全なメッセージシーケンス
ユーザーが「東京の天気を教えて」と質問し、AIが `get_weather` ツールを使って回答するまでの、MCPメッセージの完全なシーケンスをJSON形式で記述してください。

以下の前提条件に従ってください：
- MCPサーバーは `weather-server` で、`get_weather` ツールを提供している
- 接続は確立済み（初期化フェーズは完了）とする
- `get_weather` ツールは `city` パラメータを受け取り、天気情報を返す

記述するメッセージ：
(1) Host内のAIモデルがツール呼び出しを決定した後、ClientからServerへの `tools/call` リクエスト
(2) Serverからの実行結果レスポンス
(3) (任意) エラーが発生した場合のレスポンス例

**期待される出力例：**
```json
// (1) tools/call リクエスト
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "city": "Tokyo"
    }
  }
}

// (2) 成功レスポンス
{ ... }
```

<details>
<summary>ヒント</summary>

- `tools/call` のレスポンスには `content` 配列が含まれ、各要素には `type` と `text` があります
- `isError` フィールドでツール実行自体のエラーを示します（JSON-RPCレベルのエラーとは別）
- ツール実行エラーの場合でも、JSON-RPCレベルでは成功レスポンス（`result`）として返し、`isError: true` で区別します

</details>

<details>
<summary>解答例</summary>

```json
// ===== (1) Client → Server: tools/call リクエスト =====
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "city": "Tokyo"
    }
  }
}

// ===== (2) Server → Client: 成功レスポンス =====
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "東京の天気：晴れ、気温22°C、湿度45%"
      }
    ],
    "isError": false
  }
}

// ===== (3) Server → Client: ツール実行エラーの場合 =====
// ※ JSON-RPCレベルでは「成功」レスポンスだが、isErrorでエラーを通知
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "天気情報の取得に失敗しました: API rate limit exceeded"
      }
    ],
    "isError": true
  }
}

// ===== (参考) JSON-RPCレベルのエラーの場合 =====
// ※ ツールが存在しない等、プロトコルレベルの問題
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32601,
    "message": "Tool not found: get_weather"
  }
}
```

**重要なポイント：**
- ツール実行時のエラー（APIエラー等）は `result.isError: true` で表現します
- JSON-RPCレベルのエラー（`error`フィールド）は、メソッドが存在しない等のプロトコルレベルの問題に使います
- この2種類のエラーの区別は、エラーハンドリングにおいて重要です

**全体の流れ（Hostの内部動作を含む）：**
```
ユーザー: 「東京の天気を教えて」
    │
    ▼
Host（AIモデル）: ツール呼び出しが必要と判断
    │
    ▼
Client → Server: tools/call（get_weather, city=Tokyo）
    │
    ▼
Server: 外部APIで天気情報を取得
    │
    ▼
Server → Client: result（天気情報）
    │
    ▼
Host（AIモデル）: 結果をもとに自然言語で回答を生成
    │
    ▼
ユーザーへ: 「東京は現在晴れで、気温は22°C、湿度は45%です。」
```

</details>

### 問題2-6：ケーパビリティネゴシエーションの設計
以下の2つのシナリオについて、`initialize` リクエストとレスポンスのJSON-RPCメッセージを設計してください。

**シナリオA：** 基本的なツール呼び出しのみをサポートするシンプルなクライアントとサーバー

**シナリオB：** リソース購読（subscription）、ツール一覧変更通知、プロンプト機能をフルサポートするクライアントとサーバー

**期待される出力例（シナリオA）：**
```json
// Client → Server: initialize リクエスト
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-03-26",
    "capabilities": {},
    "clientInfo": { "name": "SimpleClient", "version": "1.0.0" }
  }
}
// Server → Client: initialize レスポンス
{ ... }
```

<details>
<summary>ヒント</summary>

- `capabilities` オブジェクトに、サポートする機能を宣言します
- クライアント側のケーパビリティ例：`roots`（ファイルシステムルートの提供）、`sampling`（モデルへのサンプリング要求）
- サーバー側のケーパビリティ例：`tools`（ツール提供）、`resources`（リソース提供）、`prompts`（プロンプト提供）
- `listChanged: true` はツール一覧等の動的変更通知をサポートすることを示します

</details>

<details>
<summary>解答例</summary>

**シナリオA：シンプルな構成**

```json
// Client → Server: initialize リクエスト
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-03-26",
    "capabilities": {},
    "clientInfo": {
      "name": "SimpleClient",
      "version": "1.0.0"
    }
  }
}

// Server → Client: initialize レスポンス
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-03-26",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "SimpleWeatherServer",
      "version": "1.0.0"
    }
  }
}

// Client → Server: initialized 通知
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

**シナリオB：フル機能構成**

```json
// Client → Server: initialize リクエスト
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-03-26",
    "capabilities": {
      "roots": {
        "listChanged": true
      },
      "sampling": {}
    },
    "clientInfo": {
      "name": "AdvancedAIHost",
      "version": "2.0.0"
    }
  }
}

// Server → Client: initialize レスポンス
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-03-26",
    "capabilities": {
      "tools": {
        "listChanged": true
      },
      "resources": {
        "subscribe": true,
        "listChanged": true
      },
      "prompts": {
        "listChanged": true
      }
    },
    "serverInfo": {
      "name": "EnterpriseServer",
      "version": "2.0.0"
    }
  }
}

// Client → Server: initialized 通知
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

**ケーパビリティの比較表：**

| ケーパビリティ | シナリオA | シナリオB | 説明 |
|---|:---:|:---:|---|
| tools | あり | あり（listChanged） | ツール提供。listChangedでツール追加・削除を動的に通知 |
| resources | なし | あり（subscribe, listChanged） | リソース提供。subscribeでリソース変更のリアルタイム通知 |
| prompts | なし | あり（listChanged） | プロンプトテンプレート提供 |
| roots（クライアント側） | なし | あり（listChanged） | ファイルシステムルートの提供 |
| sampling（クライアント側） | なし | あり | サーバーからモデルへのサンプリング要求を許可 |

**重要なポイント：**
- ケーパビリティネゴシエーションにより、クライアントとサーバーは互いの対応機能を把握します
- サーバーが `resources` を宣言していなければ、クライアントは `resources/list` を呼び出しません
- `listChanged: true` は運用中にケーパビリティが動的に変化することをサポートする宣言です

</details>

### 問題2-7：プロトコルバージョンの不一致
クライアントが `protocolVersion: "2025-03-26"` で `initialize` を送信しましたが、サーバーは `"2024-11-05"` までしか対応していません。この場合、どのようなレスポンスが返されるべきか、JSON-RPCメッセージを記述してください。また、クライアントはどのように対応すべきかを説明してください。

**期待される出力例：**
```json
// サーバーからのレスポンス
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    ...
  }
}
// クライアントの対応方針の説明
```

<details>
<summary>ヒント</summary>

- サーバーは自身がサポートする最新のバージョンをレスポンスで返します
- クライアントは返されたバージョンに対応できるかどうかを判断します
- バージョンの互換性がない場合、クライアントは接続を切断します

</details>

<details>
<summary>解答例</summary>

**サーバーからのレスポンス：**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "LegacyServer",
      "version": "1.0.0"
    }
  }
}
```

**クライアントの対応：**

1. サーバーが返した `protocolVersion: "2024-11-05"` を確認します
2. クライアントがそのバージョンに対応しているかを判断します
   - **対応可能な場合**：そのバージョンで通信を継続し、`initialized` 通知を送信します
   - **対応不可の場合**：接続を切断します

```json
// 対応可能な場合 → initialized を送信して運用フェーズへ
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}

// 対応不可の場合 → 接続を切断（close）
// クライアントはユーザーに「サーバーのプロトコルバージョンが
// 対応範囲外です」とエラーメッセージを表示します
```

**重要なポイント：**
- MCPのバージョンネゴシエーションは「サーバーが最終的なバージョンを決定する」方式です
- クライアントは希望するバージョンを提示し、サーバーは自身がサポートする範囲内で選択します
- 完全な後方互換性は保証されないため、バージョン不一致時のフォールバック処理は重要です

</details>

---

## チャレンジ問題

### 問題2-8：カスタムトランスポートの設計（WebSocket）
MCPの標準トランスポートはstdioとStreamable HTTPですが、WebSocketベースのカスタムトランスポートを設計してください。

以下の項目について設計書を作成してください：

(1) **設計の動機**：なぜWebSocketトランスポートが必要なのか（stdioやStreamable HTTPでは不十分なユースケース）
(2) **接続フロー**：WebSocket接続の確立から初期化完了までのシーケンス
(3) **メッセージフォーマット**：WebSocketフレームでJSON-RPCメッセージをどのように送受信するか
(4) **再接続とエラーハンドリング**：切断時の再接続ポリシーとエラー処理の設計
(5) **セキュリティ考慮事項**：認証、暗号化、オリジン検証など

**期待される出力例（一部）：**
```
(1) 設計の動機：
    - リアルタイム双方向通信が必要なユースケース（例：ライブコーディング支援）
    - サーバーからのプッシュ通知を低レイテンシで受信したい
    - Streamable HTTPのSSEは単方向であり、真の双方向通信には制約がある

(2) 接続フロー：
    1. クライアントが wss://server.example.com/mcp にWebSocket接続を開始
    2. ...
```

<details>
<summary>ヒント</summary>

**設計のポイント：**
- WebSocketの利点は「永続的な双方向通信」と「低レイテンシ」です
- Streamable HTTPとの違いを明確にしましょう（SSEは一方向、ポーリング不要等）
- 再接続時にMCPのセッション状態をどう復元するかが重要な設計判断です
- `wss://`（TLS付き）を前提とし、認証にはサブプロトコルやクエリパラメータを活用できます

</details>

<details>
<summary>解答例</summary>

## WebSocketトランスポート設計書

### (1) 設計の動機

| 課題 | stdio | Streamable HTTP | WebSocket |
|---|---|---|---|
| リモート接続 | 不可 | 可能 | 可能 |
| 双方向リアルタイム通信 | 可能（ローカルのみ） | SSEは一方向 | 完全な双方向 |
| サーバーからのプッシュ | - | SSEで可能だがHTTP接続の制約あり | ネイティブ対応 |
| レイテンシ | 最小 | HTTP接続のオーバーヘッド | 永続接続で低レイテンシ |
| 接続数 | プロセス単位 | リクエストごとにHTTP接続 | 1本の永続接続 |

**WebSocketが適するユースケース：**
- リアルタイムコラボレーション（複数ユーザーが同時にAIアシスタントを使用）
- 高頻度のツール呼び出し（ライブコーディング支援、リアルタイムモニタリング等）
- サーバーからの頻繁なプッシュ通知（リソース変更のリアルタイム通知等）

---

### (2) 接続フロー

```
  Client                              Server
    │                                    │
    │  1. WebSocket Upgrade Request      │
    │  GET /mcp HTTP/1.1                 │
    │  Upgrade: websocket                │
    │  Sec-WebSocket-Protocol: mcp-v1    │
    │  Authorization: Bearer <token>     │
    │  ─────────────────────────────────→ │
    │                                    │
    │  2. WebSocket Upgrade Response     │
    │  HTTP/1.1 101 Switching Protocols  │
    │  ←───────────────────────────────── │
    │                                    │
    │  === WebSocket接続確立 ===          │
    │                                    │
    │  3. initialize リクエスト           │
    │  {"jsonrpc":"2.0","id":1,          │
    │   "method":"initialize",...}       │
    │  ─────────────────────────────────→ │
    │                                    │
    │  4. initialize レスポンス           │
    │  {"jsonrpc":"2.0","id":1,          │
    │   "result":{...}}                  │
    │  ←───────────────────────────────── │
    │                                    │
    │  5. initialized 通知               │
    │  {"jsonrpc":"2.0",                 │
    │   "method":"notifications/         │
    │    initialized"}                   │
    │  ─────────────────────────────────→ │
    │                                    │
    │  === 運用フェーズ開始 ===           │
    │                                    │
```

---

### (3) メッセージフォーマット

```
WebSocketフレーム構造：
┌─────────────────────────────────┐
│ opcode: 0x1 (テキストフレーム)    │
│ payload: JSON-RPCメッセージ(UTF-8)│
└─────────────────────────────────┘
```

**ルール：**
- 1つのWebSocketテキストフレームに1つのJSON-RPCメッセージを格納します
- バイナリフレームは使用しません（テキストフレームのみ）
- メッセージサイズの上限は1MB（設定で変更可能）とします
- 大きなレスポンスは `content` 配列内の複数要素に分割して返します

```json
// 送信例（1フレーム = 1メッセージ）
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search","arguments":{"query":"MCP"}}}
```

---

### (4) 再接続とエラーハンドリング

**再接続ポリシー：**
```
再接続戦略：指数バックオフ + ジッタ

初回リトライ: 1秒後
2回目: 2秒後
3回目: 4秒後
4回目: 8秒後
...
最大間隔: 30秒
最大リトライ回数: 10回
ジッタ: ±20%のランダム遅延を付加
```

**セッション復元フロー：**
```
1. WebSocket切断を検出
2. 指数バックオフで再接続を試行
3. WebSocket接続が再確立されたら：
   a. 新しい initialize リクエストを送信
   b. ケーパビリティを再ネゴシエーション
   c. 必要に応じて tools/list、resources/list を再取得
   d. 未完了のリクエストがあればリトライ
```

**エラー処理：**
| イベント | 対応 |
|---|---|
| WebSocket close (1000) | 正常終了。再接続しない |
| WebSocket close (1001) | サーバーシャットダウン。再接続を試行 |
| WebSocket close (1006) | 異常切断。即座に再接続を試行 |
| Ping/Pong タイムアウト | 接続が切れたと判断し、再接続を試行 |
| JSON パースエラー | エラーログを記録し、該当メッセージを破棄 |

---

### (5) セキュリティ考慮事項

**必須要件：**

1. **暗号化**：必ず `wss://`（TLS over WebSocket）を使用します。平文の `ws://` はローカル開発環境以外では禁止です

2. **認証**：WebSocketハンドシェイク時に認証を行います
   ```
   GET /mcp HTTP/1.1
   Upgrade: websocket
   Authorization: Bearer <JWT_TOKEN>
   ```

3. **オリジン検証**：サーバーは `Origin` ヘッダを検証し、許可されたオリジンからの接続のみ受け入れます
   ```
   許可リスト: ["https://app.example.com", "https://ide.example.com"]
   ```

4. **レート制限**：1接続あたりのメッセージ送信レートを制限します（例：100メッセージ/秒）

5. **メッセージサイズ制限**：1メッセージあたりの最大サイズを制限します（例：1MB）

6. **Ping/Pong によるキープアライブ**：30秒間隔でPingフレームを送信し、接続の生存を確認します。応答がない場合はタイムアウトとして切断します

</details>

### 問題2-9：メッセージフローの総合演習
以下のシナリオにおいて、MCPの接続開始から終了までの全メッセージフローをJSON-RPCメッセージで記述してください。

**シナリオ：**
データベース検索MCPサーバー（`db-server`）を使って、ユーザーが「売上トップ3の商品を教えて」と質問する。サーバーは以下の機能を持つ：
- Tools: `query_database`（SQLクエリの実行）
- Resources: `schema://tables`（テーブル一覧）

**記述する全メッセージ：**
1. 接続確立と初期化（initialize → response → initialized）
2. ツール一覧の取得（tools/list）
3. リソースの取得（resources/read でテーブルスキーマを参照）
4. ツール呼び出し（tools/call でSQLクエリ実行）
5. 接続終了

**期待される出力例（冒頭部分）：**
```json
// === 1. 初期化フェーズ ===

// (1-a) Client → Server: initialize
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": { ... }
}
...
```

<details>
<summary>ヒント</summary>

- 全部で7〜8個のメッセージ（リクエスト+レスポンスのペア、および通知）になります
- `resources/read` では URI を指定してリソースを取得します
- `query_database` ツールのパラメータにはSQLクエリ文字列を含めます
- 最後の接続終了にはcloseメソッドまたはトランスポート切断を使います

</details>

<details>
<summary>解答例</summary>

```json
// ================================================================
// === 1. 初期化フェーズ ===
// ================================================================

// (1-a) Client → Server: initialize リクエスト
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-03-26",
    "capabilities": {
      "roots": {}
    },
    "clientInfo": {
      "name": "AIAssistant",
      "version": "1.0.0"
    }
  }
}

// (1-b) Server → Client: initialize レスポンス
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-03-26",
    "capabilities": {
      "tools": {},
      "resources": {}
    },
    "serverInfo": {
      "name": "db-server",
      "version": "1.0.0"
    }
  }
}

// (1-c) Client → Server: initialized 通知
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}

// ================================================================
// === 2. ツール一覧の取得 ===
// ================================================================

// (2-a) Client → Server: tools/list リクエスト
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}

// (2-b) Server → Client: tools/list レスポンス
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "query_database",
        "description": "SQLクエリを実行してデータベースから情報を取得します",
        "inputSchema": {
          "type": "object",
          "properties": {
            "sql": {
              "type": "string",
              "description": "実行するSQLクエリ"
            }
          },
          "required": ["sql"]
        }
      }
    ]
  }
}

// ================================================================
// === 3. リソースの取得（テーブルスキーマの参照） ===
// ================================================================

// (3-a) Client → Server: resources/read リクエスト
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "resources/read",
  "params": {
    "uri": "schema://tables"
  }
}

// (3-b) Server → Client: resources/read レスポンス
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "contents": [
      {
        "uri": "schema://tables",
        "mimeType": "application/json",
        "text": "{\"tables\":[{\"name\":\"products\",\"columns\":[\"id\",\"name\",\"price\",\"sales_count\"]},{\"name\":\"orders\",\"columns\":[\"id\",\"product_id\",\"quantity\",\"order_date\"]}]}"
      }
    ]
  }
}

// ================================================================
// === 4. ツール呼び出し（SQLクエリ実行） ===
// ================================================================

// (4-a) Client → Server: tools/call リクエスト
// ※ Hostの AIモデルがスキーマ情報をもとにSQLを生成した結果
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "query_database",
    "arguments": {
      "sql": "SELECT name, sales_count FROM products ORDER BY sales_count DESC LIMIT 3"
    }
  }
}

// (4-b) Server → Client: tools/call レスポンス
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "| 順位 | 商品名 | 販売数 |\n|------|--------|--------|\n| 1 | ワイヤレスイヤホン | 15,230 |\n| 2 | スマートウォッチ | 12,450 |\n| 3 | モバイルバッテリー | 9,870 |"
      }
    ],
    "isError": false
  }
}

// ================================================================
// === 5. 接続終了 ===
// ================================================================

// (5) Client側がトランスポートを切断して接続を終了
// stdioの場合：サーバープロセスを終了
// Streamable HTTPの場合：HTTP接続を閉じる
// ※ close通知を送信することもできます
```

**全体のシーケンス図：**
```
  Client                              Server (db-server)
    │                                    │
    │  ─── (1-a) initialize ──────────→  │
    │  ←── (1-b) response ────────────  │
    │  ─── (1-c) initialized ─────────→  │
    │                                    │
    │  ─── (2-a) tools/list ──────────→  │
    │  ←── (2-b) response ────────────  │
    │                                    │
    │  ─── (3-a) resources/read ──────→  │
    │  ←── (3-b) response ────────────  │
    │                                    │
    │  [Hostの AIモデルがSQLを生成]       │
    │                                    │
    │  ─── (4-a) tools/call ──────────→  │
    │  ←── (4-b) response ────────────  │
    │                                    │
    │  [Hostの AIモデルが回答を生成]      │
    │  [→ユーザーへ回答を表示]            │
    │                                    │
    │  ─── (5) 切断 ──────────────────→  │
    │                                    │
```

**メッセージIDの採番：**
- 各リクエストに連番（1, 2, 3, 4...）のIDを振っています
- レスポンスは対応するリクエストと同じIDを持ちます
- 通知（Notification）にはIDがありません

</details>

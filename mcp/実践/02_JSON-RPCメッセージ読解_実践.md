# 実践課題02：JSON-RPCメッセージ読解 ★1

> **難易度**: ★☆☆☆☆（入門）
> **前提知識**: 第2章（MCPアーキテクチャ）
> **課題の種類**: コードリーディング
> **学習目標**: MCPで使われるJSON-RPC 2.0メッセージの構造を読み解き、リクエスト・レスポンス・通知の違いを正確に区別できるようになる

---

## 完成イメージ

以下のようなJSON-RPCメッセージを読み、各フィールドの意味と通信の流れを説明できるようになります。

```json
// リクエスト（クライアント → サーバー）
{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {...}}

// レスポンス（サーバー → クライアント）
{"jsonrpc": "2.0", "id": 1, "result": {...}}

// 通知（idなし、返信不要）
{"jsonrpc": "2.0", "method": "notifications/initialized"}
```

最終的に、MCPの初期化からツール呼び出しまでの一連のメッセージを時系列で並べ、各メッセージの役割を解説した資料を作成します。

---

## 課題の要件

1. JSON-RPC 2.0 の3種類のメッセージ（リクエスト、レスポンス、通知）の構造を説明する
2. 以下の10個のMCPメッセージを読み解き、種類・方向・目的を記入する
3. メッセージを正しい時系列順に並べ替える
4. 各メッセージのフィールド（`jsonrpc`, `id`, `method`, `params`, `result`, `error`）の役割を説明する
5. エラーレスポンスの読み方を理解する

---

## 読み解くメッセージ一覧

以下の10個のメッセージを分析してください。順序はランダムです。

### メッセージA

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-03-26",
    "capabilities": {
      "roots": { "listChanged": true }
    },
    "clientInfo": {
      "name": "my-app",
      "version": "1.0.0"
    }
  }
}
```

### メッセージB

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-03-26",
    "capabilities": {
      "tools": { "listChanged": true },
      "resources": { "subscribe": true }
    },
    "serverInfo": {
      "name": "weather-server",
      "version": "0.1.0"
    }
  }
}
```

### メッセージC

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

### メッセージD

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

### メッセージE

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "get_weather",
        "description": "指定された都市の天気情報を取得します",
        "inputSchema": {
          "type": "object",
          "properties": {
            "city": {
              "type": "string",
              "description": "都市名（例：東京）"
            }
          },
          "required": ["city"]
        }
      }
    ]
  }
}
```

### メッセージF

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "city": "東京"
    }
  }
}
```

### メッセージG

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "東京の天気: 晴れ、気温25℃、湿度60%"
      }
    ]
  }
}
```

### メッセージH

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "city": ""
    }
  }
}
```

### メッセージI

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "エラー: 都市名が空です"
      }
    ],
    "isError": true
  }
}
```

### メッセージJ

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "error": {
    "code": -32601,
    "message": "Method not found: unknown/method"
  }
}
```

---

## ステップガイド

<details>
<summary>ステップ1：JSON-RPC 2.0の3種類のメッセージを整理する</summary>

JSON-RPC 2.0 には3種類のメッセージがあります。

| 種類 | 特徴 | 必須フィールド |
|------|------|---------------|
| リクエスト（Request） | 処理を依頼し、レスポンスを期待する | `jsonrpc`, `id`, `method` |
| レスポンス（Response） | リクエストへの返答 | `jsonrpc`, `id`, `result` または `error` |
| 通知（Notification） | 一方的に送る。返答を期待しない | `jsonrpc`, `method`（`id` がない） |

**見分け方のコツ**:
- `id` があり `method` がある → リクエスト
- `id` があり `result` または `error` がある → レスポンス
- `id` がなく `method` がある → 通知

</details>

<details>
<summary>ステップ2：各メッセージの種類と方向を特定する</summary>

各メッセージを以下の表に記入してみましょう。

| メッセージ | 種類 | 方向 | 目的 |
|-----------|------|------|------|
| A | ? | ? → ? | ? |
| B | ? | ? → ? | ? |
| C | ? | ? → ? | ? |
| ... | ... | ... | ... |

ヒント：
- `initialize` メソッドは常にクライアントからサーバーへ送られます
- 通知は `notifications/` で始まるメソッド名を持つことが多いです
- レスポンスの `id` は、対応するリクエストの `id` と一致します

</details>

<details>
<summary>ステップ3：時系列順に並べ替える</summary>

MCPの通信は以下の順番で行われます。

1. **初期化フェーズ**: initialize → レスポンス → initialized 通知
2. **機能発見フェーズ**: tools/list → レスポンス
3. **通常通信フェーズ**: tools/call → レスポンス

`id` の値もヒントになります。`id` は通常リクエストごとに1ずつ増加します。

</details>

<details>
<summary>ステップ4：エラーの種類を理解する</summary>

MCPのエラーには2種類あります。

**1. ツール実行エラー（アプリケーションレベル）**
- レスポンスの `result` 内に `isError: true` が含まれる
- ツール自体は正常に呼ばれたが、処理中にエラーが発生した

**2. プロトコルエラー（JSON-RPCレベル）**
- レスポンスに `error` オブジェクトが含まれる
- メソッドが見つからない、パラメータが不正など、プロトコルレベルの問題

```
ツール実行エラー: {"id": 4, "result": {"isError": true, ...}}
  → ツールは呼ばれたが、入力値が不正だった等

プロトコルエラー: {"id": 5, "error": {"code": -32601, ...}}
  → そもそもメソッドが見つからなかった
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

### 1. メッセージ分析表

| メッセージ | 種類 | 方向 | id | method / 対応method | 目的 |
|-----------|------|------|-----|-------------------|------|
| A | リクエスト | クライアント → サーバー | 1 | `initialize` | 接続初期化。プロトコルバージョンとクライアント情報を送信 |
| B | レスポンス | サーバー → クライアント | 1 | (initialize への応答) | サーバーの機能（capabilities）と情報を返答 |
| C | 通知 | クライアント → サーバー | なし | `notifications/initialized` | 初期化完了を通知（返答不要） |
| D | リクエスト | クライアント → サーバー | 2 | `tools/list` | サーバーが提供するツール一覧を要求 |
| E | レスポンス | サーバー → クライアント | 2 | (tools/list への応答) | ツール一覧（get_weather）を返答 |
| F | リクエスト | クライアント → サーバー | 3 | `tools/call` | get_weather ツールを「東京」で呼び出し |
| G | レスポンス | サーバー → クライアント | 3 | (tools/call への応答) | ツール実行結果（天気情報）を返答 |
| H | リクエスト | クライアント → サーバー | 4 | `tools/call` | get_weather ツールを空の都市名で呼び出し |
| I | レスポンス | サーバー → クライアント | 4 | (tools/call への応答) | ツール実行エラー（都市名が空） |
| J | レスポンス | サーバー → クライアント | 5 | (不明なメソッドへの応答) | プロトコルエラー（メソッドが存在しない） |

### 2. 時系列順

```
時系列    方向                    メッセージ
──────   ─────────────────────  ──────────
  1      Client → Server        A: initialize リクエスト
  2      Server → Client        B: initialize レスポンス
  3      Client → Server        C: initialized 通知
  4      Client → Server        D: tools/list リクエスト
  5      Server → Client        E: tools/list レスポンス
  6      Client → Server        F: tools/call (東京) リクエスト
  7      Server → Client        G: tools/call (東京) レスポンス
  8      Client → Server        H: tools/call (空文字) リクエスト
  9      Server → Client        I: tools/call (空文字) エラーレスポンス
  10     (何らかのリクエスト)     → J: プロトコルエラーレスポンス
```

### 3. フィールドの意味まとめ

| フィールド | 説明 | 例 |
|-----------|------|-----|
| `jsonrpc` | JSON-RPCバージョン（常に`"2.0"`） | `"2.0"` |
| `id` | リクエストとレスポンスを紐づける識別子 | `1`, `2`, `3` |
| `method` | 呼び出すメソッド名 | `"initialize"`, `"tools/call"` |
| `params` | メソッドに渡すパラメータ | `{"name": "get_weather", ...}` |
| `result` | 処理成功時の結果 | `{"tools": [...]}` |
| `error` | プロトコルエラー時のエラー情報 | `{"code": -32601, ...}` |

### 4. エラーの違い

```
■ ツール実行エラー（メッセージI）
  ・id: 4 のリクエスト(H)への応答
  ・result.isError = true
  ・意味：ツールは正常に呼ばれたが、入力が不正だった
  ・例：都市名が空文字列

■ プロトコルエラー（メッセージJ）
  ・id: 5 の不明なリクエストへの応答
  ・error.code = -32601（Method not found）
  ・意味：指定されたメソッド自体が存在しない
  ・例：存在しないメソッド名を呼び出した
```

</details>

<details>
<summary>解答例（改良版）</summary>

改良版では、メッセージの流れをシーケンス図として整理し、Pythonでメッセージを生成・検証するコードも含めます。

### 1. シーケンス図

```
  Client                                Server
    │                                      │
    │  ──── 初期化フェーズ ────              │
    │                                      │
    │  A: initialize (id=1)                │
    │─────────────────────────────────────→│
    │      protocolVersion: "2025-03-26"   │
    │      clientInfo: {name: "my-app"}    │
    │                                      │
    │  B: initialize response (id=1)       │
    │←─────────────────────────────────────│
    │      capabilities: {tools, resources}│
    │      serverInfo: {name: "weather"}   │
    │                                      │
    │  C: notifications/initialized        │
    │─────────────────────────────────────→│
    │      （通知：idなし、応答なし）        │
    │                                      │
    │  ──── 機能発見フェーズ ────            │
    │                                      │
    │  D: tools/list (id=2)                │
    │─────────────────────────────────────→│
    │                                      │
    │  E: tools/list response (id=2)       │
    │←─────────────────────────────────────│
    │      tools: [{name: "get_weather"}]  │
    │                                      │
    │  ──── 通常通信フェーズ ────            │
    │                                      │
    │  F: tools/call (id=3)                │
    │─────────────────────────────────────→│
    │      name: "get_weather"             │
    │      arguments: {city: "東京"}        │
    │                                      │
    │  G: tools/call response (id=3)       │
    │←─────────────────────────────────────│
    │      content: "東京の天気: 晴れ..."   │
    │                                      │
    │  ──── エラーケース ────               │
    │                                      │
    │  H: tools/call (id=4)                │
    │─────────────────────────────────────→│
    │      arguments: {city: ""}           │
    │                                      │
    │  I: tools/call response (id=4)       │
    │←─────────────────────────────────────│
    │      isError: true                   │
    │      "都市名が空です"                 │
    │                                      │
    │  (不明なメソッド呼び出し id=5)         │
    │─────────────────────────────────────→│
    │                                      │
    │  J: error response (id=5)            │
    │←─────────────────────────────────────│
    │      code: -32601 (Method not found) │
    │                                      │
```

### 2. Pythonでメッセージを検証するコード

```python
"""
MCP JSON-RPCメッセージの種類を判定するプログラム
学べること：JSON-RPC 2.0メッセージの構造と分類
"""
import json


def classify_message(msg: dict) -> str:
    """JSON-RPCメッセージの種類を判定します。"""
    if "method" in msg and "id" in msg:
        return "リクエスト (Request)"
    elif "method" in msg and "id" not in msg:
        return "通知 (Notification)"
    elif "result" in msg and "id" in msg:
        return "成功レスポンス (Success Response)"
    elif "error" in msg and "id" in msg:
        return "エラーレスポンス (Error Response)"
    else:
        return "不明なメッセージ"


def get_direction(msg: dict) -> str:
    """メッセージの通信方向を推定します。"""
    if "method" in msg:
        # リクエスト・通知は基本的にクライアント → サーバー
        # ※ サーバーからの通知もあるが、ここでは基本パターン
        return "Client → Server"
    else:
        # レスポンスはサーバー → クライアント
        return "Server → Client"


def analyze_message(label: str, msg_json: str) -> None:
    """メッセージを分析して結果を表示します。"""
    msg = json.loads(msg_json)
    msg_type = classify_message(msg)
    direction = get_direction(msg)

    print(f"\n{'='*50}")
    print(f"メッセージ {label}")
    print(f"  種類:   {msg_type}")
    print(f"  方向:   {direction}")
    print(f"  id:     {msg.get('id', 'なし')}")

    if "method" in msg:
        print(f"  method: {msg['method']}")
    if "error" in msg:
        print(f"  error:  code={msg['error']['code']}, "
              f"message={msg['error']['message']}")
    if "result" in msg and isinstance(msg["result"], dict):
        if msg["result"].get("isError"):
            print(f"  ※ ツール実行エラー（isError=true）")


# メッセージの定義
messages = {
    "A": '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}',
    "B": '{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2025-03-26"}}',
    "C": '{"jsonrpc":"2.0","method":"notifications/initialized"}',
    "D": '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}',
    "E": '{"jsonrpc":"2.0","id":2,"result":{"tools":[]}}',
    "F": '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_weather"}}',
    "G": '{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"晴れ"}]}}',
    "H": '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"get_weather","arguments":{"city":""}}}',
    "I": '{"jsonrpc":"2.0","id":4,"result":{"content":[{"type":"text","text":"エラー"}],"isError":true}}',
    "J": '{"jsonrpc":"2.0","id":5,"error":{"code":-32601,"message":"Method not found"}}',
}

# 分析実行
for label, msg_json in sorted(messages.items()):
    analyze_message(label, msg_json)
```

### 3. JSON-RPCエラーコード一覧

実務で遭遇しやすいエラーコードを整理しておくと、デバッグに役立ちます。

| コード | 名前 | 説明 |
|--------|------|------|
| -32700 | Parse error | JSONの構文が不正 |
| -32600 | Invalid Request | JSON-RPCの形式が不正 |
| -32601 | Method not found | 指定されたメソッドが存在しない |
| -32602 | Invalid params | パラメータが不正 |
| -32603 | Internal error | サーバー内部エラー |

### 初心者向けとの違い

| ポイント | 初心者向け | 改良版 |
|---------|-----------|--------|
| 表現方法 | 表形式 | シーケンス図で時間軸を可視化 |
| 検証方法 | 目視のみ | Pythonコードで自動判定 |
| エラー理解 | 2種類の違い | エラーコード一覧を含む実務的な知識 |
| 応用 | メッセージの読み方のみ | メッセージの生成・検証スキル |

改良版のポイントは、**読むだけでなくコードで検証できるスキル**を身につけることです。実際のMCP開発では、デバッグ時にJSON-RPCメッセージをログから読み解く場面が頻繁にあります。

</details>

---

## よくある間違い

| 間違い | 正しい理解 |
|--------|-----------|
| 通知にもレスポンスが返ると思う | 通知（Notification）にはレスポンスが返りません。`id` フィールドがないことが目印です |
| `error` と `isError` を混同する | `error` はJSON-RPCレベルのエラー（プロトコル違反）、`isError` はツール実行結果のエラー（アプリケーションレベル）です |
| `id` が連番でなければならないと思う | `id` は一意であれば良く、連番である必要はありません。ただし、同一セッション内で重複してはいけません |
| 全メッセージが同期的に処理されると思う | JSON-RPC 2.0 は非同期処理をサポートしており、リクエストの応答順は送信順とは限りません（MCPでは通常順序通りですが、仕様上は保証されません） |

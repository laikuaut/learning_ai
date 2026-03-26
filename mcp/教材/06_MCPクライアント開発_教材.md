# 第6章：MCPクライアント開発

## 学習目標

- MCPクライアントの役割とアーキテクチャを理解する
- PythonでMCPクライアントを実装し、サーバーと通信できる
- TypeScriptでMCPクライアントを実装できる
- LLM（大規模言語モデル）とMCPクライアントを統合するパターンを習得する
- 複数MCPサーバーへの同時接続を管理できる
- エラーハンドリングとリトライ戦略を設計できる

---

## 6.1 MCPクライアントとは

MCPクライアント（MCP Client）は、ホストアプリケーション内でMCPサーバーと通信するコンポーネントです。Claude DesktopやCursorなどのアプリは内部にMCPクライアントを持っており、ユーザーが意識することなくMCPサーバーと通信しています。

### クライアントの位置づけ

```
┌──────────────────────────────────────────────────┐
│            ホストアプリケーション                  │
│  ┌────────────────────────────────────────────┐  │
│  │                LLM / AI                    │  │
│  │   「このツールを呼びたい」                   │  │
│  └──────────┬─────────────────────────────────┘  │
│             │                                    │
│  ┌──────────▼─────────────────────────────────┐  │
│  │          MCPクライアント                    │  │
│  │  ・サーバーへの接続管理                     │  │
│  │  ・ツール/リソース/プロンプトの一覧取得     │  │
│  │  ・ツール呼び出しの実行                     │  │
│  │  ・レスポンスの受信・中継                   │  │
│  └──────┬──────────┬──────────┬───────────────┘  │
└─────────┼──────────┼──────────┼──────────────────┘
          │          │          │  JSON-RPC
    ┌─────▼───┐ ┌────▼────┐ ┌──▼──────────┐
    │ Server  │ │ Server  │ │  Server     │
    │    A    │ │    B    │ │     C       │
    └─────────┘ └─────────┘ └─────────────┘
```

### クライアントの主な役割

| 役割 | 説明 |
|---|---|
| **接続管理** | サーバーとの接続確立・維持・切断 |
| **能力交渉** | サーバーがサポートする機能の確認（Capability Negotiation） |
| **一覧取得** | ツール・リソース・プロンプトの一覧を取得 |
| **呼び出し実行** | ツールの実行、リソースの読み取り、プロンプトの取得 |
| **通知処理** | サーバーからの通知（リソース更新等）を受信 |

### 通信フロー

```
クライアント                         サーバー
    │                                   │
    │──── initialize ─────────────────→ │  ① 初期化リクエスト
    │←─── initialize response ────────  │  ② 能力情報の応答
    │──── initialized（通知）──────────→ │  ③ 初期化完了の通知
    │                                   │
    │──── tools/list ─────────────────→ │  ④ ツール一覧取得
    │←─── tools/list response ────────  │
    │                                   │
    │──── tools/call ─────────────────→ │  ⑤ ツール実行
    │←─── tools/call response ────────  │
    │                                   │
```

> **ポイントまとめ**
> - MCPクライアントはホストアプリとMCPサーバーの橋渡し役
> - 初期化 → 能力交渉 → 一覧取得 → 実行 の順で通信する
> - 1つのクライアントは1つのサーバーに対応するのが基本

---

## 6.2 Pythonクライアントの実装

Python MCP SDKを使って、MCPクライアントを実装します。

### 必要なパッケージのインストール

```bash
pip install mcp
```

### 基本的な接続とツール一覧取得

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # サーバーの起動パラメータを定義
    server_params = StdioServerParameters(
        command="python",
        args=["my_server.py"],  # MCPサーバーのスクリプトパス
    )

    # サーバーに接続
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # ① 初期化（能力交渉）
            await session.initialize()

            # ② ツール一覧を取得
            tools_result = await session.list_tools()
            print("=== 利用可能なツール ===")
            for tool in tools_result.tools:
                print(f"  {tool.name}: {tool.description}")

            # ③ リソース一覧を取得
            resources_result = await session.list_resources()
            print("\n=== 利用可能なリソース ===")
            for resource in resources_result.resources:
                print(f"  {resource.uri}: {resource.name}")

            # ④ プロンプト一覧を取得
            prompts_result = await session.list_prompts()
            print("\n=== 利用可能なプロンプト ===")
            for prompt in prompts_result.prompts:
                print(f"  {prompt.name}: {prompt.description}")

asyncio.run(main())
```

### ツールの実行

```python
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["my_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # ツールを実行
            result = await session.call_tool(
                "create_task",
                arguments={
                    "title": "MCPクライアントの実装",
                    "priority": "high",
                },
            )

            # 結果を表示
            for content in result.content:
                if content.type == "text":
                    print(f"結果: {content.text}")

            # エラーの確認
            if result.isError:
                print("ツールの実行でエラーが発生しました")

asyncio.run(main())
```

### リソースの読み取り

```python
async def read_resource(session: ClientSession):
    """リソースを読み取る例です。"""

    # 静的リソースの読み取り
    result = await session.read_resource("config://app/settings")
    for content in result.contents:
        if content.text:
            print(f"設定内容:\n{content.text}")

    # 動的リソース（テンプレート）の読み取り
    result = await session.read_resource("users://u001/profile")
    for content in result.contents:
        if content.text:
            print(f"プロフィール:\n{content.text}")
```

### プロンプトの取得

```python
async def get_prompt(session: ClientSession):
    """プロンプトを取得する例です。"""

    result = await session.get_prompt(
        "code_review",
        arguments={
            "code": "def add(a, b): return a + b",
            "language": "python",
        },
    )

    # プロンプトのメッセージを表示
    for message in result.messages:
        print(f"[{message.role}]")
        if isinstance(message.content, str):
            print(message.content)
        else:
            print(message.content.text)
```

### よくある間違い

| 間違い | 正しい方法 |
|---|---|
| `initialize()` を呼ばずにツールを実行する | 必ず最初に `initialize()` を呼ぶ |
| 同期関数の中で `await` を使おうとする | `asyncio.run()` でasync関数を実行する |
| セッションを閉じずに終了する | `async with` で自動クリーンアップを保証する |
| ツール名を間違える | `list_tools()` で正確な名前を確認してから呼ぶ |

> **ポイントまとめ**
> - `StdioServerParameters` でサーバーの起動方法を指定する
> - `stdio_client` + `ClientSession` の二重 `async with` で接続を管理する
> - `initialize()` → `list_tools()` → `call_tool()` が基本フロー
> - 結果の `content` はリスト形式で、`type` で種類を判別する

---

## 6.3 TypeScriptクライアントの実装

TypeScript MCP SDKを使った実装を紹介します。

### 必要なパッケージのインストール

```bash
npm install @modelcontextprotocol/sdk
```

### 基本的な接続とツール一覧取得

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

async function main() {
  // トランスポートの作成（stdioで通信）
  const transport = new StdioClientTransport({
    command: "python",
    args: ["my_server.py"],
  });

  // クライアントの作成
  const client = new Client(
    {
      name: "my-client",
      version: "1.0.0",
    },
    {
      capabilities: {},  // クライアントの能力を宣言
    }
  );

  // サーバーに接続
  await client.connect(transport);

  // ツール一覧を取得
  const tools = await client.listTools();
  console.log("=== 利用可能なツール ===");
  for (const tool of tools.tools) {
    console.log(`  ${tool.name}: ${tool.description}`);
  }

  // ツールを実行
  const result = await client.callTool({
    name: "create_task",
    arguments: {
      title: "TypeScriptクライアントのテスト",
      priority: "medium",
    },
  });

  console.log("結果:", result.content);

  // クリーンアップ
  await client.close();
}

main().catch(console.error);
```

### SSE（Server-Sent Events）トランスポート

HTTP経由で接続する場合は、SSEトランスポートを使います。

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";

async function connectViaSSE() {
  const transport = new SSEClientTransport(
    new URL("http://localhost:8080/sse")
  );

  const client = new Client(
    { name: "sse-client", version: "1.0.0" },
    { capabilities: {} }
  );

  await client.connect(transport);

  // 以降の操作はstdioと同じ
  const tools = await client.listTools();
  console.log(tools);

  await client.close();
}
```

### Python と TypeScript の比較

| 項目 | Python | TypeScript |
|---|---|---|
| パッケージ | `mcp` | `@modelcontextprotocol/sdk` |
| クライアントクラス | `ClientSession` | `Client` |
| 接続方法 | `stdio_client()` + `ClientSession()` | `StdioClientTransport` + `client.connect()` |
| ツール実行 | `session.call_tool(name, arguments=...)` | `client.callTool({ name, arguments })` |
| クリーンアップ | `async with` で自動 | `client.close()` を明示的に呼ぶ |

> **ポイントまとめ**
> - TypeScriptでは `Client` クラスと `Transport` クラスを組み合わせる
> - stdio と SSE の2種類のトランスポートが利用可能
> - APIの構造はPythonとほぼ同じなので、片方を覚えればもう片方も理解しやすい

---

## 6.4 LLMとの統合パターン

MCPクライアントの真価は、LLM（大規模言語モデル）と統合したときに発揮されます。ここではAnthropic SDK + MCPクライアントを組み合わせたパターンを紹介します。

### 統合アーキテクチャ

```
ユーザー
  │  「明日の天気を調べて」
  ▼
┌──────────────────────────────────────────┐
│           ホストアプリケーション           │
│                                          │
│  ① MCPクライアントでツール一覧を取得      │
│  ② ツール一覧をLLMに渡して会話           │
│  ③ LLMが「このツールを呼んで」と応答     │
│  ④ MCPクライアントでツールを実行          │
│  ⑤ 結果をLLMに返す                       │
│  ⑥ LLMが最終回答を生成                   │
│                                          │
│  ┌────────────┐      ┌───────────────┐   │
│  │  Anthropic  │      │ MCPクライアント│   │
│  │  SDK (LLM)  │◄────►│              │   │
│  └────────────┘      └──────┬────────┘   │
└─────────────────────────────┼────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   MCPサーバー      │
                    │  (天気API等)       │
                    └───────────────────┘
```

### 完全な実装例: Anthropic SDK + MCP

```python
import asyncio
import json
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPChatAgent:
    """MCPサーバーと連携するチャットエージェントです。"""

    def __init__(self):
        self.anthropic = Anthropic()  # ANTHROPIC_API_KEY 環境変数を使用
        self.session: ClientSession | None = None
        self.tools: list = []

    async def connect_to_server(self, server_script: str):
        """MCPサーバーに接続し、ツール一覧を取得します。"""
        server_params = StdioServerParameters(
            command="python",
            args=[server_script],
        )

        # 接続（注意: この実装ではcontextを手動管理）
        self._stdio_context = stdio_client(server_params)
        read, write = await self._stdio_context.__aenter__()

        self._session_context = ClientSession(read, write)
        self.session = await self._session_context.__aenter__()

        await self.session.initialize()

        # ツール一覧を取得してAnthropic API形式に変換
        tools_result = await self.session.list_tools()
        self.tools = [
            {
                "name": tool.name,
                "description": tool.description or "",
                "input_schema": tool.inputSchema,
            }
            for tool in tools_result.tools
        ]
        print(f"{len(self.tools)}個のツールを取得しました")

    async def chat(self, user_message: str) -> str:
        """ユーザーのメッセージに対してLLM + MCPで応答します。"""
        messages = [{"role": "user", "content": user_message}]

        # ツール使用ループ
        while True:
            # LLMに問い合わせ
            response = self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                tools=self.tools,
                messages=messages,
            )

            # レスポンスを解析
            assistant_content = response.content
            messages.append({"role": "assistant", "content": assistant_content})

            # ツール呼び出しがなければ終了
            tool_use_blocks = [
                block for block in assistant_content
                if block.type == "tool_use"
            ]
            if not tool_use_blocks:
                # テキスト応答を抽出して返す
                text_parts = [
                    block.text for block in assistant_content
                    if block.type == "text"
                ]
                return "\n".join(text_parts)

            # ツールを実行して結果をメッセージに追加
            tool_results = []
            for tool_use in tool_use_blocks:
                print(f"  ツール実行: {tool_use.name}({tool_use.input})")

                result = await self.session.call_tool(
                    tool_use.name,
                    arguments=tool_use.input,
                )

                # MCP結果をAnthropic API形式に変換
                result_text = ""
                for content in result.content:
                    if content.type == "text":
                        result_text += content.text

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": result_text,
                    "is_error": result.isError,
                })

            messages.append({"role": "user", "content": tool_results})

    async def cleanup(self):
        """接続をクリーンアップします。"""
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._stdio_context:
            await self._stdio_context.__aexit__(None, None, None)


async def main():
    agent = MCPChatAgent()
    try:
        await agent.connect_to_server("my_server.py")

        # 対話ループ
        while True:
            user_input = input("\nあなた: ")
            if user_input.lower() in ("quit", "exit", "終了"):
                break

            response = await agent.chat(user_input)
            print(f"\nAI: {response}")
    finally:
        await agent.cleanup()

asyncio.run(main())
```

### ツール使用ループの詳細フロー

```
ユーザー入力: 「在庫切れの商品を補充して」
     │
     ▼
┌─ LLM呼び出し（1回目）──────────────────────┐
│  messages: [user: "在庫切れの商品を補充して"]│
│  tools: [list_items, restock_item, ...]     │
│                                              │
│  → LLMの応答: tool_use("list_items", {})    │
└──────────────────────────────────────────────┘
     │
     ▼ MCPクライアントでツール実行
     │ 結果: [{"name":"キーボード","stock":0}]
     │
     ▼
┌─ LLM呼び出し（2回目）──────────────────────┐
│  messages: [user, assistant, tool_result]    │
│                                              │
│  → LLMの応答: tool_use("restock_item",      │
│                 {"item_id":"item_003",       │
│                  "quantity": 50})            │
└──────────────────────────────────────────────┘
     │
     ▼ MCPクライアントでツール実行
     │ 結果: "50個補充しました"
     │
     ▼
┌─ LLM呼び出し（3回目）──────────────────────┐
│  messages: [user, asst, tool, asst, tool]   │
│                                              │
│  → LLMの応答: text("キーボードの在庫を      │
│    50個補充しました。")                      │
└──────────────────────────────────────────────┘
     │
     ▼ ツール呼び出しなし → ループ終了
```

> **ポイントまとめ**
> - MCPのツール定義をAnthropic APIの `tools` パラメータに変換して渡す
> - LLMがツール呼び出しを返す限りループを継続する
> - ツール結果は `tool_result` としてメッセージ履歴に追加する
> - `isError` フラグでエラーをLLMに伝え、適切なリカバリーを促す

---

## 6.5 複数サーバーの管理

実用的なアプリケーションでは、複数のMCPサーバーに同時接続することが一般的です。

### 複数サーバー接続の管理クラス

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MultiServerManager:
    """複数のMCPサーバーへの接続を管理するクラスです。"""

    def __init__(self):
        self.sessions: dict[str, ClientSession] = {}
        self.tools: dict[str, dict] = {}  # tool_name -> {server, tool_info}
        self._contexts: list = []  # クリーンアップ用

    async def add_server(self, name: str, command: str, args: list[str]):
        """MCPサーバーを追加して接続します。

        Args:
            name: サーバーの識別名（例: "file-server"）
            command: 起動コマンド
            args: コマンド引数
        """
        server_params = StdioServerParameters(command=command, args=args)

        stdio_ctx = stdio_client(server_params)
        read, write = await stdio_ctx.__aenter__()
        self._contexts.append(stdio_ctx)

        session_ctx = ClientSession(read, write)
        session = await session_ctx.__aenter__()
        self._contexts.append(session_ctx)

        await session.initialize()
        self.sessions[name] = session

        # ツールを登録（名前空間を付与）
        tools_result = await session.list_tools()
        for tool in tools_result.tools:
            namespaced_name = f"{name}__{tool.name}"
            self.tools[namespaced_name] = {
                "server": name,
                "original_name": tool.name,
                "info": {
                    "name": namespaced_name,
                    "description": f"[{name}] {tool.description or ''}",
                    "input_schema": tool.inputSchema,
                },
            }

        print(f"サーバー '{name}' に接続しました"
              f"（ツール数: {len(tools_result.tools)}）")

    def get_all_tools(self) -> list[dict]:
        """全サーバーのツールをまとめて返します。"""
        return [entry["info"] for entry in self.tools.values()]

    async def call_tool(self, namespaced_name: str, arguments: dict) -> str:
        """名前空間付きツール名でツールを実行します。"""
        if namespaced_name not in self.tools:
            raise ValueError(f"ツール '{namespaced_name}' が見つかりません")

        entry = self.tools[namespaced_name]
        server_name = entry["server"]
        original_name = entry["original_name"]

        session = self.sessions[server_name]
        result = await session.call_tool(original_name, arguments=arguments)

        texts = []
        for content in result.content:
            if content.type == "text":
                texts.append(content.text)
        return "\n".join(texts)

    async def cleanup(self):
        """全接続をクリーンアップします。"""
        for ctx in reversed(self._contexts):
            await ctx.__aexit__(None, None, None)


# 使用例
async def main():
    manager = MultiServerManager()

    # 複数サーバーに接続
    await manager.add_server(
        "files", "python", ["file_server.py"]
    )
    await manager.add_server(
        "database", "python", ["db_server.py"]
    )
    await manager.add_server(
        "api", "python", ["api_server.py"]
    )

    # 全ツール一覧（LLMに渡す）
    all_tools = manager.get_all_tools()
    print(f"\n合計 {len(all_tools)} 個のツールが利用可能:")
    for tool in all_tools:
        print(f"  {tool['name']}: {tool['description']}")

    # ツール実行（名前空間付き）
    result = await manager.call_tool(
        "database__search_users",
        {"query": "田中"},
    )
    print(f"\n検索結果: {result}")

    await manager.cleanup()

asyncio.run(main())
```

### 名前空間の設計

```
名前空間なし（衝突の危険）:
  file_server:  search → "search"
  db_server:    search → "search"   ← 衝突！

名前空間あり（安全）:
  file_server:  search → "files__search"
  db_server:    search → "database__search"  ← 一意
```

### よくある間違い

| 間違い | 正しい方法 |
|---|---|
| ツール名が衝突して上書きされる | 名前空間（プレフィックス）で区別する |
| 全サーバーを直列で接続する | `asyncio.gather()` で並列接続する |
| 1つのサーバーの障害で全体が止まる | サーバーごとに独立してエラーハンドリングする |

> **ポイントまとめ**
> - 複数サーバーのツール名は名前空間で管理して衝突を防ぐ
> - サーバーごとに独立した `ClientSession` を保持する
> - 全サーバーのツールをまとめてLLMに渡すことで、AIが適切に選択できる

---

## 6.6 エラーハンドリングとリトライ

MCPクライアント開発では、ネットワーク障害やサーバークラッシュへの対処が不可欠です。

### エラーの種類と対処法

| エラーの種類 | 原因 | 対処法 |
|---|---|---|
| **接続エラー** | サーバーが起動しない | パス・コマンドの確認、リトライ |
| **タイムアウト** | サーバーの応答が遅い | タイムアウト値の調整、リトライ |
| **サーバークラッシュ** | サーバープロセスが異常終了 | 再接続、フォールバック |
| **プロトコルエラー** | 不正なリクエスト/レスポンス | ログ出力、バージョン確認 |
| **ツール実行エラー** | ツール内部でエラー発生 | `isError` を確認、LLMにリカバリーを委ねる |

### リトライ付き接続

```python
import asyncio
import logging
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger(__name__)

async def connect_with_retry(
    server_params: StdioServerParameters,
    max_retries: int = 3,
    retry_delay: float = 2.0,
) -> tuple:
    """リトライ付きでMCPサーバーに接続します。

    Args:
        server_params: サーバーのパラメータ
        max_retries: 最大リトライ回数
        retry_delay: リトライ間隔（秒）

    Returns:
        (stdio_context, session_context, session) のタプル
    """
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"接続試行 {attempt}/{max_retries}")

            stdio_ctx = stdio_client(server_params)
            read, write = await stdio_ctx.__aenter__()

            session_ctx = ClientSession(read, write)
            session = await session_ctx.__aenter__()

            await session.initialize()

            logger.info("接続成功")
            return stdio_ctx, session_ctx, session

        except Exception as e:
            logger.warning(f"接続失敗（試行 {attempt}）: {e}")
            if attempt < max_retries:
                logger.info(f"{retry_delay}秒後にリトライします...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # 指数バックオフ
            else:
                logger.error("最大リトライ回数に達しました")
                raise
```

### タイムアウト付きツール実行

```python
async def call_tool_with_timeout(
    session: ClientSession,
    tool_name: str,
    arguments: dict,
    timeout: float = 30.0,
) -> str:
    """タイムアウト付きでツールを実行します。

    Args:
        session: MCPセッション
        tool_name: ツール名
        arguments: ツールの引数
        timeout: タイムアウト（秒）

    Returns:
        ツールの実行結果（テキスト）

    Raises:
        TimeoutError: タイムアウトした場合
    """
    try:
        result = await asyncio.wait_for(
            session.call_tool(tool_name, arguments=arguments),
            timeout=timeout,
        )

        texts = []
        for content in result.content:
            if content.type == "text":
                texts.append(content.text)

        if result.isError:
            logger.warning(f"ツール '{tool_name}' がエラーを返しました")

        return "\n".join(texts)

    except asyncio.TimeoutError:
        logger.error(
            f"ツール '{tool_name}' が{timeout}秒でタイムアウトしました"
        )
        raise TimeoutError(
            f"ツール '{tool_name}' の実行が{timeout}秒でタイムアウトしました"
        )
```

### 自動再接続を備えたクライアント

```python
class ResilientMCPClient:
    """障害耐性を持つMCPクライアントです。"""

    def __init__(self, server_params: StdioServerParameters):
        self.server_params = server_params
        self.session: ClientSession | None = None
        self._stdio_ctx = None
        self._session_ctx = None

    async def ensure_connected(self):
        """接続を確認し、切れていれば再接続します。"""
        if self.session is not None:
            return  # 接続済み

        logger.info("サーバーに接続します...")
        self._stdio_ctx, self._session_ctx, self.session = (
            await connect_with_retry(self.server_params)
        )

    async def call_tool_safe(
        self,
        tool_name: str,
        arguments: dict,
        max_retries: int = 2,
    ) -> str:
        """安全にツールを実行します（再接続・リトライ対応）。

        Args:
            tool_name: ツール名
            arguments: ツールの引数
            max_retries: 最大リトライ回数
        """
        for attempt in range(1, max_retries + 1):
            try:
                await self.ensure_connected()
                return await call_tool_with_timeout(
                    self.session, tool_name, arguments
                )
            except (ConnectionError, TimeoutError, OSError) as e:
                logger.warning(
                    f"ツール実行失敗（試行 {attempt}）: {e}"
                )
                # セッションをリセットして再接続を促す
                await self._close_session()
                if attempt >= max_retries:
                    raise

        raise RuntimeError("予期しないエラー")

    async def _close_session(self):
        """セッションを閉じます。"""
        self.session = None
        try:
            if self._session_ctx:
                await self._session_ctx.__aexit__(None, None, None)
            if self._stdio_ctx:
                await self._stdio_ctx.__aexit__(None, None, None)
        except Exception:
            pass  # クリーンアップのエラーは無視
        finally:
            self._session_ctx = None
            self._stdio_ctx = None


# 使用例
async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["my_server.py"],
    )

    client = ResilientMCPClient(server_params)

    # 障害が起きても自動リカバリー
    result = await client.call_tool_safe(
        "search_products",
        {"query": "ノートPC"},
    )
    print(f"結果: {result}")

asyncio.run(main())
```

### ログ出力のベストプラクティス

```python
import logging

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger("mcp-client")

# 接続時
logger.info("サーバー '%s' に接続しました", server_name)

# ツール実行時
logger.info("ツール '%s' を実行します（引数: %s）", tool_name, arguments)

# エラー時
logger.error("ツール '%s' の実行に失敗しました: %s", tool_name, error)

# デバッグ時（本番では出力しない）
logger.debug("レスポンス詳細: %s", response)
```

### よくある間違い

| 間違い | 正しい方法 |
|---|---|
| リトライ間隔を固定にする | 指数バックオフ（2秒→4秒→8秒）で負荷を分散する |
| 全てのエラーでリトライする | 接続エラーのみリトライ。ツールのビジネスエラーはリトライしない |
| エラーを握りつぶす（`except: pass`） | ログに記録し、必要に応じて上位に伝播する |
| タイムアウトを設定しない | 必ずタイムアウトを設定し、無限待ちを防ぐ |
| 再接続時にリソースをリークする | 再接続前に古いセッションを確実にクリーンアップする |

> **ポイントまとめ**
> - 接続エラーには指数バックオフ付きリトライで対処する
> - ツール実行には必ずタイムアウトを設定する
> - サーバークラッシュ時は自動再接続で復旧する
> - ログを適切に出力し、障害時の原因特定を容易にする
> - `isError` フラグによるツールエラーはリトライではなく、LLMに判断を委ねる

# 実践課題07：MCPクライアント実装設計 ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第2章（MCPアーキテクチャ）、第5章（MCPの3つの機能）、第6章（MCPクライアント開発）
> **課題の種類**: ミニプロジェクト
> **学習目標**: MCPクライアントを実装し、MCPサーバーと接続してツールを呼び出せるようになる。LLMとの統合の仕組みを理解し、複数サーバーの管理方法を学ぶ

---

## 完成イメージ

MCPクライアントを実装し、MCPサーバーと接続してツール一覧の取得やツールの呼び出しを行います。

```
┌──────────────────────────────────────────────────────────┐
│  MCPクライアント（自作）                                   │
│                                                          │
│  1. サーバーに接続（stdio トランスポート）                  │
│  2. 初期化ハンドシェイク（initialize → initialized）       │
│  3. ツール一覧を取得（tools/list）                         │
│  4. ツールを呼び出し（tools/call）                         │
│  5. 結果を表示                                            │
│                                                          │
│  ┌──────────┐  JSON-RPC   ┌──────────────┐              │
│  │ Client   ├────────────→│ MCPサーバー    │              │
│  │          │←────────────┤ (子プロセス)  │              │
│  └──────────┘  stdio      └──────────────┘              │
│                                                          │
│  さらに：LLM統合フロー                                    │
│  ユーザー入力 → LLM判断 → ツール呼び出し → 結果をLLMへ    │
│                          → 最終回答をユーザーへ            │
└──────────────────────────────────────────────────────────┘
```

---

## 課題の要件

1. MCP Python SDK（`mcp` パッケージ）を使ってクライアントを実装する
2. stdio トランスポートでMCPサーバーに接続する
3. 以下の操作を順番に行うスクリプトを作成する
   - サーバーへの接続と初期化
   - ツール一覧の取得と表示
   - 特定ツールの呼び出しと結果表示
   - 接続の終了
4. LLMと統合する場合のフロー図を設計する
5. 複数サーバーを管理する設計を考える

---

## ステップガイド

<details>
<summary>ステップ1：MCPクライアントの接続フローを理解する</summary>

MCPクライアントがサーバーと通信する流れは以下の通りです。

```
┌─────────────── 通信フロー ───────────────┐
│                                          │
│  1. サーバープロセスを起動                 │
│     └→ stdio（標準入出力）で接続          │
│                                          │
│  2. initialize リクエスト送信             │
│     └→ サーバーの capabilities を受信     │
│                                          │
│  3. initialized 通知を送信               │
│     └→ サーバーが操作可能状態になる       │
│                                          │
│  4. 操作を実行                           │
│     ├→ tools/list（ツール一覧取得）       │
│     ├→ tools/call（ツール呼び出し）       │
│     ├→ resources/list（リソース一覧取得） │
│     └→ prompts/list（プロンプト一覧取得） │
│                                          │
│  5. 接続を閉じる                          │
│                                          │
└──────────────────────────────────────────┘
```

</details>

<details>
<summary>ステップ2：基本的なクライアントコードを書く</summary>

MCP Python SDKの `ClientSession` を使ってクライアントを実装します。

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# サーバーへの接続パラメータ
server_params = StdioServerParameters(
    command="uv",
    args=["run", "server.py"],
)

# サーバーに接続
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # 初期化
        await session.initialize()

        # ツール一覧取得
        tools = await session.list_tools()

        # ツール呼び出し
        result = await session.call_tool("tool_name", {"arg": "value"})
```

</details>

<details>
<summary>ステップ3：LLM統合のフローを設計する</summary>

MCPクライアントをLLMと統合する場合、以下のループで動作します。

```
ユーザー入力
    │
    ▼
┌────────────────┐
│ LLMに送信       │ ← ユーザーメッセージ + 利用可能なツール情報
└────────┬───────┘
         │
         ▼
┌────────────────┐
│ LLMが判断      │ ← ツールを使うべきか？どのツールを？
└────────┬───────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  ツール    テキスト
  呼び出し  回答
    │         │
    ▼         │
┌──────────┐  │
│ MCP経由で │  │
│ ツール実行│  │
└────┬─────┘  │
     │        │
     ▼        │
┌──────────┐  │
│ 結果を    │  │
│ LLMに送信 │  │
└────┬─────┘  │
     │        │
     ▼        ▼
┌────────────────┐
│ 最終回答を表示  │
└────────────────┘
```

ポイント：
- LLMがツールを呼ぶかどうかを判断します
- ツール結果はLLMに返され、LLMが最終回答を生成します
- このループが「エージェントループ（agent loop）」です

</details>

<details>
<summary>ステップ4：複数サーバー管理を設計する</summary>

実際のアプリケーションでは、複数のMCPサーバーを同時に利用します。

```
┌───────────── ホスト ─────────────────────────┐
│                                              │
│  ┌──────────────┐  ┌──────────────┐         │
│  │ Client A     │  │ Client B     │   ...   │
│  │ →天気サーバー │  │ →ファイル     │         │
│  └──────┬───────┘  │  サーバー    │         │
│         │          └──────┬───────┘         │
│         │                 │                  │
│  ┌──────┴─────────────────┴───────┐         │
│  │  ツールルーター                  │         │
│  │  get_weather → Client A         │         │
│  │  read_file   → Client B         │         │
│  └────────────────────────────────┘         │
└──────────────────────────────────────────────┘
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```python
"""
MCPクライアント（初心者向け）
学べること：MCPサーバーへの接続、ツール一覧取得、ツール呼び出し
実行方法：uv run client.py
前提：同じディレクトリに server.py（MCPサーバー）が存在すること
"""
import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """MCPサーバーに接続し、ツールを操作するクライアントです。"""

    # ── 1. サーバーへの接続 ──
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"],
    )

    print("MCPサーバーに接続中...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # ── 2. 初期化 ──
            init_result = await session.initialize()
            print(f"接続成功！")
            print(f"  サーバー名: {init_result.serverInfo.name}")
            print(f"  バージョン: {init_result.serverInfo.version}")
            print(f"  プロトコル: {init_result.protocolVersion}")
            print()

            # ── 3. ツール一覧の取得 ──
            tools_result = await session.list_tools()
            print(f"利用可能なツール（{len(tools_result.tools)}個）:")
            for tool in tools_result.tools:
                print(f"  ・{tool.name}: {tool.description}")
                if tool.inputSchema.get("properties"):
                    for param, info in tool.inputSchema["properties"].items():
                        required = param in tool.inputSchema.get("required", [])
                        req_mark = "（必須）" if required else "（オプション）"
                        print(f"      - {param}: {info.get('description', '')} {req_mark}")
            print()

            # ── 4. ツールの呼び出し ──
            if tools_result.tools:
                tool_name = tools_result.tools[0].name
                print(f"ツール '{tool_name}' を呼び出します...")

                # サーバーによって引数が異なります
                # ここでは例として greet ツールを想定
                try:
                    result = await session.call_tool(
                        tool_name,
                        arguments={"name": "テストユーザー"},
                    )
                    print(f"結果:")
                    for content in result.content:
                        print(f"  {content.text}")
                except Exception as e:
                    print(f"エラー: {e}")

            # ── 5. リソース一覧の取得 ──
            try:
                resources_result = await session.list_resources()
                if resources_result.resources:
                    print(f"\n利用可能なリソース（{len(resources_result.resources)}個）:")
                    for res in resources_result.resources:
                        print(f"  ・{res.uri}: {res.name}")
            except Exception:
                print("\n（リソースは未対応）")

            # ── 6. プロンプト一覧の取得 ──
            try:
                prompts_result = await session.list_prompts()
                if prompts_result.prompts:
                    print(f"\n利用可能なプロンプト（{len(prompts_result.prompts)}個）:")
                    for prompt in prompts_result.prompts:
                        print(f"  ・{prompt.name}: {prompt.description}")
            except Exception:
                print("（プロンプトは未対応）")

    print("\n接続を終了しました。")


if __name__ == "__main__":
    asyncio.run(main())
```

### テスト用サーバー

クライアントのテスト用に簡単なサーバーも用意します。

```python
# server.py（テスト用MCPサーバー）
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("test-server")

@mcp.tool()
def greet(name: str) -> str:
    """指定された名前で挨拶を返します。

    Args:
        name: 挨拶する相手の名前
    """
    return f"こんにちは、{name}さん！MCPサーバーからの挨拶です。"

@mcp.tool()
def add(a: int, b: int) -> str:
    """2つの数を足し算します。

    Args:
        a: 1つ目の数
        b: 2つ目の数
    """
    return f"{a} + {b} = {a + b}"

@mcp.resource("test://info")
def get_info() -> str:
    """サーバーの情報です。"""
    return "テストサーバー v1.0 - MCPクライアントの動作確認用"

if __name__ == "__main__":
    mcp.run()
```

</details>

<details>
<summary>解答例（改良版）</summary>

改良版では、LLMとの統合フローと複数サーバー管理を実装します。

```python
"""
MCPクライアント（改良版）── LLM統合 + 複数サーバー管理
学べること：エージェントループ、複数サーバー管理、ツールルーティング
実行方法：uv run client_advanced.py
"""
import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPServerConnection:
    """1つのMCPサーバーとの接続を管理するクラスです。"""

    def __init__(self, name: str, command: str, args: list[str]):
        self.name = name
        self.command = command
        self.args = args
        self.session: ClientSession | None = None
        self.tools: list[dict] = []

    async def connect(self, read, write):
        """サーバーに接続して初期化します。"""
        self.session = ClientSession(read, write)
        await self.session.__aenter__()
        init_result = await self.session.initialize()
        print(f"  [{self.name}] 接続成功 - {init_result.serverInfo.name}")

        # ツール一覧を取得
        tools_result = await self.session.list_tools()
        self.tools = [
            {
                "name": t.name,
                "description": t.description,
                "input_schema": t.inputSchema,
            }
            for t in tools_result.tools
        ]
        print(f"  [{self.name}] ツール {len(self.tools)}個を検出")

    async def call_tool(self, tool_name: str, arguments: dict) -> str:
        """ツールを呼び出します。"""
        if self.session is None:
            raise RuntimeError(f"サーバー {self.name} に接続されていません")
        result = await self.session.call_tool(tool_name, arguments)
        texts = [c.text for c in result.content if hasattr(c, "text")]
        return "\n".join(texts)

    async def disconnect(self):
        """接続を閉じます。"""
        if self.session:
            await self.session.__aexit__(None, None, None)
            self.session = None


class MCPClientManager:
    """複数のMCPサーバーを統合管理するクライアントです。"""

    def __init__(self):
        self.connections: dict[str, MCPServerConnection] = {}
        self.tool_router: dict[str, str] = {}  # tool_name → server_name

    def register_server(self, name: str, command: str, args: list[str]):
        """サーバーを登録します。"""
        self.connections[name] = MCPServerConnection(name, command, args)

    async def connect_all(self):
        """全サーバーに接続します。"""
        print("サーバーに接続中...\n")
        for name, conn in self.connections.items():
            server_params = StdioServerParameters(
                command=conn.command,
                args=conn.args,
            )
            # 注: 実際にはコンテキストマネージャの管理が必要
            # ここでは概念的な実装を示します
            print(f"  {name} に接続中...")

    def build_tool_router(self):
        """全サーバーのツールを統合し、ルーティングテーブルを構築します。"""
        self.tool_router.clear()
        for name, conn in self.connections.items():
            for tool in conn.tools:
                tool_name = tool["name"]
                if tool_name in self.tool_router:
                    print(
                        f"  ⚠ ツール名重複: {tool_name} "
                        f"({self.tool_router[tool_name]} と {name})"
                    )
                else:
                    self.tool_router[tool_name] = name

        print(f"\nツールルーティングテーブル（{len(self.tool_router)}ツール）:")
        for tool_name, server_name in sorted(self.tool_router.items()):
            print(f"  {tool_name} → {server_name}")

    def get_all_tools_for_llm(self) -> list[dict]:
        """LLMに渡すツール定義の一覧を返します。"""
        all_tools = []
        for conn in self.connections.values():
            for tool in conn.tools:
                all_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool["description"],
                        "parameters": tool["input_schema"],
                    },
                })
        return all_tools

    async def route_tool_call(self, tool_name: str, arguments: dict) -> str:
        """ツール呼び出しを適切なサーバーにルーティングします。"""
        server_name = self.tool_router.get(tool_name)
        if server_name is None:
            raise ValueError(f"不明なツール: {tool_name}")

        conn = self.connections[server_name]
        print(f"  [{server_name}] {tool_name} を呼び出し中...")
        return await conn.call_tool(tool_name, arguments)


def simulate_llm_response(user_message: str, tools: list[dict]) -> dict:
    """LLMの応答をシミュレートします（実際にはAPI呼び出し）。

    本番では Anthropic API や OpenAI API を使用します。
    ここではデモ用に固定の応答を返します。
    """
    # デモ用：ユーザーメッセージに「天気」が含まれればツール呼び出し
    if "天気" in user_message:
        return {
            "type": "tool_call",
            "tool_name": "get_current_weather",
            "arguments": {"city": "東京"},
        }
    else:
        return {
            "type": "text",
            "content": f"承知しました。「{user_message}」についてお答えします。",
        }


async def agent_loop(manager: MCPClientManager):
    """エージェントループ（LLM + MCPツール呼び出し）のデモです。"""
    print("\n=== エージェントループ デモ ===\n")

    tools = manager.get_all_tools_for_llm()
    print(f"LLMに渡すツール数: {len(tools)}")
    print()

    user_message = "東京の天気を教えてください"
    print(f"ユーザー: {user_message}")
    print()

    # ステップ1: LLMに問い合わせ
    llm_response = simulate_llm_response(user_message, tools)
    print(f"LLM判断: {json.dumps(llm_response, ensure_ascii=False, indent=2)}")
    print()

    if llm_response["type"] == "tool_call":
        # ステップ2: ツール呼び出し
        tool_name = llm_response["tool_name"]
        arguments = llm_response["arguments"]

        try:
            result = await manager.route_tool_call(tool_name, arguments)
            print(f"ツール結果: {result}")
        except Exception as e:
            print(f"ツールエラー: {e}")
            result = f"エラーが発生しました: {e}"

        # ステップ3: 結果をLLMに渡して最終回答生成（シミュレート）
        print(f"\nLLM最終回答: {result} の情報をもとにお伝えします。")

    else:
        print(f"LLM回答: {llm_response['content']}")


# ── エントリーポイント ──

async def main():
    """複数サーバー管理のデモです。"""

    # サーバー登録（実際に接続する場合はコンテキストマネージャが必要）
    manager = MCPClientManager()
    manager.register_server("weather", "uv", ["run", "weather_server.py"])
    manager.register_server("files", "uv", ["run", "file_server.py"])

    print("=== MCPクライアントマネージャー ===\n")
    print("登録済みサーバー:")
    for name, conn in manager.connections.items():
        print(f"  ・{name}: {conn.command} {' '.join(conn.args)}")

    print("\n注: 実際にサーバーを起動するには、")
    print("各サーバーのPythonファイルが必要です。")
    print("\n--- エージェントループの概念設計 ---")
    print()
    print("1. ユーザー入力を受け取る")
    print("2. LLMに「利用可能ツール一覧 + ユーザーメッセージ」を送信")
    print("3. LLMがツール呼び出しを返した場合:")
    print("   a. tool_router でサーバーを特定")
    print("   b. MCPサーバーにツール呼び出しを転送")
    print("   c. 結果をLLMに返して最終回答を生成")
    print("4. LLMがテキスト回答を返した場合:")
    print("   a. そのまま表示")
    print("5. 1に戻る（対話ループ）")


if __name__ == "__main__":
    asyncio.run(main())
```

### 初心者向けとの違い

| ポイント | 初心者向け | 改良版 |
|---------|-----------|--------|
| スコープ | 1サーバーとの通信 | 複数サーバーの統合管理 |
| アーキテクチャ | 手続き的な直列処理 | クラスベースの設計（接続管理、ルーティング） |
| LLM統合 | なし | エージェントループの設計と実装 |
| ツール管理 | 手動で名前を指定 | ルーティングテーブルによる自動振り分け |
| エラー処理 | try-except のみ | 接続状態の管理、ツール名重複検出 |

**実務のポイント**: MCPクライアントの本質は「LLMとMCPサーバーを仲介するエージェントループ」です。LLMがツールの使い方を判断し、MCPクライアントが実際の呼び出しを行い、結果をLLMに返すというサイクルを理解することが、MCPシステム全体の設計で最も重要です。

</details>

---

## よくある間違い

| 間違い | 正しい理解 |
|--------|-----------|
| クライアントがツールの使い方を決定する | ツールをいつ・どう使うかを判断するのは**LLM**です。クライアントはLLMの指示に従ってサーバーにリクエストを転送するだけです |
| `initialize()` を呼ばずにツールを使おうとする | 初期化ハンドシェイクは必須です。`initialize()` → `initialized` 通知の後でないとツール呼び出しはできません |
| 同期処理で実装する | MCP Python SDKは非同期（`async/await`）ベースです。`asyncio.run()` で実行しましょう |
| 複数サーバーのツール名が重複しても気にしない | ツール名が重複すると、LLMがどちらを呼ぶべきか判断できません。プレフィックスで名前空間を分けるか、重複を検出して警告しましょう |
| サーバーの切断処理を忘れる | `async with` やコンテキストマネージャで確実にリソースを解放しましょう。子プロセスが残るとメモリリークの原因になります |

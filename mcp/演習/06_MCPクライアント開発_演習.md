# 第6章 演習：MCPクライアントの実装

MCPクライアントの役割を理解し、実際にPythonでクライアントを実装できるようになりましょう。サーバーとの接続からLLM統合、さらにマルチサーバー管理までを段階的に学びます。

---

## 基本問題

### 問題6-1：MCPクライアントの役割

MCPクライアントの役割について、以下の質問に答えてください。

1. MCPアーキテクチャにおいて、クライアントはどの層に位置しますか？（ホスト・クライアント・サーバーの3層で説明してください）
2. クライアントが担う主な責務を4つ挙げてください。
3. クライアントとホストの違いを説明してください。
4. 1つのホストアプリケーションが複数のクライアントを持つことは可能ですか？その場合、どのような構成になりますか？

<details>
<summary>ヒント</summary>

MCPのアーキテクチャは3層構造です。

- **ホスト（Host）**：ユーザーが操作するアプリケーション（例：Claude Desktop、IDEプラグイン）
- **クライアント（Client）**：ホスト内に存在し、1つのサーバーとの接続を管理する
- **サーバー（Server）**：外部のデータやツールへのアクセスを提供する
</details>

<details>
<summary>解答例</summary>

1. クライアントは**中間層**に位置します。ホスト（Host）とサーバー（Server）の間で、プロトコルレベルの通信を管理します。

```
┌─────────────────────────────────┐
│  ホスト（Host）                    │
│  例：Claude Desktop               │
│                                   │
│  ┌───────────┐  ┌───────────┐   │
│  │ クライアント1 │  │ クライアント2 │   │
│  └─────┬─────┘  └─────┬─────┘   │
└────────┼──────────────┼─────────┘
         │              │
   ┌─────┴─────┐  ┌─────┴─────┐
   │ サーバーA   │  │ サーバーB   │
   └───────────┘  └───────────┘
```

2. クライアントの主な責務：
   - **接続管理**：サーバーとのトランスポート接続の確立・維持・切断
   - **プロトコル処理**：JSON-RPCメッセージの送受信、リクエスト/レスポンスの対応付け
   - **機能ネゴシエーション**：初期化時にサーバーのcapabilitiesを確認し、利用可能な機能を把握する
   - **リクエストのルーティング**：ホストからの要求を適切なサーバーメソッドに変換して送信する

3. ホストとクライアントの違い：
   - **ホスト**はユーザー向けのアプリケーション全体を指し、UI・LLM統合・セキュリティポリシーなどを管理します
   - **クライアント**はホスト内に存在するプロトコル通信の管理モジュールで、1つのサーバーとの1対1の接続を担当します

4. **可能**です。1つのホストが複数のクライアントインスタンスを生成し、それぞれが異なるサーバーに接続する構成が一般的です。例えば、Claude DesktopがファイルシステムサーバーとGitHubサーバーの両方に同時接続する場合、内部に2つのクライアントが存在します。

</details>

---

### 問題6-2：接続フローの順序

MCPクライアントがサーバーに接続して、ツールを呼び出すまでの流れを正しい順序に並び替えてください。

以下の手順がランダムに並んでいます。

- A. サーバーが `initialize` レスポンスを返す（serverInfo、capabilitiesを含む）
- B. クライアントが `tools/call` でツールを実行する
- C. クライアントがトランスポート接続を確立する（stdio起動 または SSE接続）
- D. クライアントが `tools/list` で利用可能なツール一覧を取得する
- E. クライアントが `initialized` 通知を送信する
- F. クライアントが `initialize` リクエストを送信する（clientInfo、capabilitiesを含む）
- G. サーバーがツールの実行結果を返す

正しい順序を答えてください。

<details>
<summary>ヒント</summary>

大きな流れは以下の3フェーズです。

1. **接続フェーズ**：トランスポートの確立
2. **初期化フェーズ**：initializeリクエスト → レスポンス → initialized通知
3. **操作フェーズ**：機能の利用（list → call）
</details>

<details>
<summary>解答例</summary>

正しい順序：**C → F → A → E → D → B → G**

```
1. [C] トランスポート接続を確立（stdio起動 or SSE接続）
   ↓
2. [F] クライアント → サーバー：initialize リクエスト
   （clientInfo、capabilities を送信）
   ↓
3. [A] サーバー → クライアント：initialize レスポンス
   （serverInfo、capabilities を返す）
   ↓
4. [E] クライアント → サーバー：initialized 通知
   （初期化完了を通知。これ以降、通常のリクエストが可能になる）
   ↓
5. [D] クライアント → サーバー：tools/list
   （利用可能なツール一覧を取得）
   ↓
6. [B] クライアント → サーバー：tools/call
   （特定のツールを実行）
   ↓
7. [G] サーバー → クライアント：ツール実行結果を返す
```

<!-- ポイント：
     - initialized通知はレスポンスを必要としない「通知」（Notification）です
     - tools/listを先に呼んでツール一覧を把握してからtools/callするのが正しい流れ
     - initializeの前にtools/callを呼ぶとエラーになります -->

</details>

---

### 問題6-3：ツール呼び出しコードの穴埋め

以下のPythonコード（MCP Python SDKを使用）には空欄があります。空欄（①〜⑥）を埋めてください。

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # サーバーの接続パラメータを定義
    server_params = StdioServerParameters(
        command="python",              # ①: 実行コマンド
        args=["server.py"],            # サーバースクリプト
    )

    # stdioトランスポートで接続
    async with stdio_client(server_params) as (read, write):
        async with ___①___(read, write) as session:
            # 初期化
            await session.___②___()

            # ツール一覧を取得
            tools_result = await session.___③___()
            print("利用可能なツール:")
            for tool in tools_result.___④___:
                print(f"  - {tool.name}: {tool.description}")

            # ツールを呼び出す
            result = await session.___⑤___(
                name="add",
                arguments={"a": 3, "b": 5}
            )

            # 結果を表示
            print(f"実行結果: {result.___⑥___[0].text}")

asyncio.run(main())
```

期待される出力例：

```
利用可能なツール:
  - add: 2つの数値を加算します
実行結果: 8
```

<details>
<summary>ヒント</summary>

MCP Python SDKの主要なメソッド名を思い出しましょう。

- セッションの作成にはどのクラスを使いますか？
- 初期化メソッドの名前は？
- ツール一覧の取得とツール呼び出しのメソッド名は？
- レスポンスのツール一覧はどのプロパティに格納されていますか？
- ツール実行結果はどのプロパティで取得できますか？
</details>

<details>
<summary>解答例</summary>

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        # ① ClientSession — MCPクライアントセッションを作成
        async with ClientSession(read, write) as session:
            # ② initialize — サーバーとの初期化ハンドシェイクを実行
            await session.initialize()

            # ③ list_tools — 利用可能なツール一覧を取得
            tools_result = await session.list_tools()
            print("利用可能なツール:")
            # ④ tools — ツール一覧が格納されたプロパティ
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # ⑤ call_tool — 指定した名前のツールを実行
            result = await session.call_tool(
                name="add",
                arguments={"a": 3, "b": 5}
            )

            # ⑥ content — 実行結果のコンテンツ配列
            print(f"実行結果: {result.content[0].text}")

asyncio.run(main())
```

<!-- 各空欄の解説：
     ① ClientSession：MCP通信を管理するセッションオブジェクト
     ② initialize()：protocolVersion, capabilities等を交換する初期化処理
     ③ list_tools()：サーバーが公開しているツール一覧を取得
     ④ tools：ListToolsResultのプロパティ。Toolオブジェクトのリスト
     ⑤ call_tool()：nameとargumentsを指定してツールを実行
     ⑥ content：CallToolResultのプロパティ。TextContent等のリスト -->

</details>

---

### 問題6-4：トランスポートの理解

MCPがサポートする2つのトランスポート方式について、以下の表を完成させてください。

| 項目 | stdio | SSE (HTTP+Server-Sent Events) |
|------|-------|------------------------------|
| 接続方式 | ① | ② |
| 適したユースケース | ③ | ④ |
| サーバーの起動方法 | ⑤ | ⑥ |
| 複数クライアントの同時接続 | ⑦ | ⑧ |

<details>
<summary>解答例</summary>

| 項目 | stdio | SSE (HTTP+Server-Sent Events) |
|------|-------|------------------------------|
| 接続方式 | ① クライアントがサーバープロセスを子プロセスとして起動し、標準入出力（stdin/stdout）で通信 | ② HTTPでサーバーに接続し、Server-Sent Eventsでサーバーからのメッセージを受信、HTTPのPOSTでクライアントからのメッセージを送信 |
| 適したユースケース | ③ ローカル環境でのツール連携。CLIツールやデスクトップアプリ（例：Claude Desktop） | ④ リモートサーバーとの連携。ネットワーク越しの通信や、Webアプリケーションとの統合 |
| サーバーの起動方法 | ⑤ クライアントがサーバーの実行コマンドを指定して子プロセスとして起動する | ⑥ サーバーは独立したHTTPサーバーとして事前に起動しておく |
| 複数クライアントの同時接続 | ⑦ 不可（1プロセスにつき1クライアント） | ⑧ 可能（HTTPサーバーなので複数の同時接続に対応） |

<!-- 補足：
     - 2025年以降、SSEに代わるStreamable HTTPトランスポートも仕様策定中です
     - stdioはシンプルで設定が容易ですが、ローカル通信に限定されます
     - SSEはネットワーク越しに使えますが、HTTPサーバーのセットアップが必要です -->

</details>

---

## 応用問題

### 問題6-5：PythonでMCPクライアントを実装する

以下の仕様を満たすMCPクライアントをPythonで実装してください。

**仕様：**
1. stdioトランスポートでサーバーに接続する
2. サーバーの情報（名前、バージョン）を表示する
3. 利用可能なツール一覧を取得して一覧表示する
4. 利用可能なリソース一覧を取得して一覧表示する
5. ユーザーからの入力を受け付け、指定されたツール名と引数でツールを呼び出す
6. エラーハンドリングを適切に行う

期待される出力例：

```
=== MCP クライアント ===
サーバーに接続中...
接続成功: my-server v1.0.0

【利用可能なツール】
  1. add - 2つの数値を加算します
  2. search - ドキュメントを検索します

【利用可能なリソース】
  1. config://app - アプリケーション設定

ツール名を入力してください (終了: quit): add
引数をJSON形式で入力してください: {"a": 10, "b": 20}

実行結果:
  30

ツール名を入力してください (終了: quit): quit
切断しました。
```

<details>
<summary>ヒント</summary>

以下の構成で実装しましょう。

1. `StdioServerParameters` でサーバー接続パラメータを定義
2. `stdio_client` でトランスポートを確立
3. `ClientSession` でセッションを管理
4. `session.initialize()` の戻り値からサーバー情報を取得
5. `session.list_tools()` と `session.list_resources()` で一覧取得
6. ループ内で `input()` を使ってユーザー入力を受け付ける
7. `session.call_tool()` でツールを実行
8. `try/except` でエラーをキャッチ
</details>

<details>
<summary>解答例</summary>

```python
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run_client(server_command: str, server_args: list[str]):
    """MCPクライアントのメイン処理"""

    # サーバー接続パラメータ
    server_params = StdioServerParameters(
        command=server_command,
        args=server_args,
    )

    print("=== MCP クライアント ===")
    print("サーバーに接続中...")

    # stdioトランスポートで接続
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初期化（サーバー情報を取得）
            init_result = await session.initialize()
            server_info = init_result.serverInfo
            print(f"接続成功: {server_info.name} v{server_info.version}")
            print()

            # ツール一覧を取得
            tools_result = await session.list_tools()
            print("【利用可能なツール】")
            if tools_result.tools:
                for i, tool in enumerate(tools_result.tools, 1):
                    print(f"  {i}. {tool.name} - {tool.description}")
            else:
                print("  （ツールはありません）")
            print()

            # リソース一覧を取得
            try:
                resources_result = await session.list_resources()
                print("【利用可能なリソース】")
                if resources_result.resources:
                    for i, resource in enumerate(resources_result.resources, 1):
                        print(f"  {i}. {resource.uri} - {resource.name}")
                else:
                    print("  （リソースはありません）")
            except Exception:
                # サーバーがresourcesをサポートしていない場合
                print("【リソース】サーバーがリソース機能をサポートしていません")
            print()

            # 対話ループ
            while True:
                tool_name = input("ツール名を入力してください (終了: quit): ").strip()
                if tool_name.lower() == "quit":
                    break

                # ツール名の存在確認
                available_names = [t.name for t in tools_result.tools]
                if tool_name not in available_names:
                    print(f"エラー: '{tool_name}' は存在しません。"
                          f"利用可能: {', '.join(available_names)}")
                    print()
                    continue

                # 引数の入力
                args_input = input("引数をJSON形式で入力してください: ").strip()
                try:
                    arguments = json.loads(args_input) if args_input else {}
                except json.JSONDecodeError as e:
                    print(f"エラー: JSON形式が不正です - {e}")
                    print()
                    continue

                # ツール呼び出し
                try:
                    result = await session.call_tool(
                        name=tool_name,
                        arguments=arguments,
                    )
                    print("\n実行結果:")
                    # isErrorフラグを確認
                    if result.isError:
                        print(f"  エラー: {result.content[0].text}")
                    else:
                        for content in result.content:
                            print(f"  {content.text}")
                except Exception as e:
                    print(f"  ツール実行エラー: {e}")
                print()

    print("切断しました。")


async def main():
    # サーバーのコマンドとスクリプトを指定
    await run_client("python", ["server.py"])


if __name__ == "__main__":
    asyncio.run(main())
```

<!-- 実装ポイント：
     - async with でセッションのライフサイクルを管理（自動的にクリーンアップ）
     - initialize() の戻り値から serverInfo を取得する
     - list_resources() はサーバーがcapabilitiesでresourcesを宣言していない場合に
       エラーになる可能性があるため、try/exceptで囲む
     - call_tool() の結果は isError フラグで成功/失敗を判定する
     - ユーザー入力のバリデーション（ツール名の存在確認、JSONパース）を行う -->

</details>

---

### 問題6-6：LLM統合ループの実装

MCPクライアントとLLM（大規模言語モデル）を統合して、ユーザーの自然言語の質問に対してMCPツールを自動的に呼び出す「エージェントループ」を実装してください。

**処理フロー：**

```
ユーザー入力
    ↓
LLMに送信（利用可能なツール情報を含む）
    ↓
LLMの応答を確認
    ├─ テキスト応答 → ユーザーに表示して終了
    └─ ツール呼び出し要求 → MCPでツール実行 → 結果をLLMに返す → 繰り返し
```

以下の擬似コード（Pythonライク）をもとに、ループ処理の本体部分を実装してください。LLMのAPIは簡略化したものを使ってかまいません。

```python
# 使用するクラス・関数（擬似的に定義済みとする）
# - session: MCPのClientSession（初期化済み）
# - llm_client: LLM APIクライアント
# - tools: session.list_tools() で取得済みのツール一覧

async def agent_loop(session, llm_client, tools, user_message: str) -> str:
    """
    ユーザーのメッセージを受け取り、必要に応じてToolを呼び出しながら
    最終的な回答を返すエージェントループ
    """
    # ここを実装してください
    pass
```

期待される動作例：

```
ユーザー: 東京の天気を教えて
  → LLM: get_weather ツールを呼び出したい（tool_use）
  → MCP: get_weather(city="Tokyo") を実行 → "晴れ、25℃"
  → LLM: "東京の天気は晴れで、気温は25℃です。"
  → ユーザーに表示
```

<details>
<summary>ヒント</summary>

エージェントループの構造：

1. `messages` リストにユーザーメッセージを追加
2. LLMにメッセージ送信（ツール定義も付与）
3. LLMの応答を確認
   - `tool_use` が含まれていれば → MCPの `call_tool` を実行 → 結果を `messages` に追加 → 2に戻る
   - テキストのみなら → テキストを返して終了
4. 無限ループを防ぐため、最大ループ回数を設けましょう
</details>

<details>
<summary>解答例</summary>

```python
import json


def tools_to_llm_format(tools):
    """
    MCPのツール定義をLLM API用のフォーマットに変換します。
    （Anthropic Messages API形式の例）
    """
    llm_tools = []
    for tool in tools:
        llm_tools.append({
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema,
        })
    return llm_tools


async def agent_loop(session, llm_client, tools, user_message: str) -> str:
    """
    ユーザーのメッセージを受け取り、必要に応じてToolを呼び出しながら
    最終的な回答を返すエージェントループ。
    """
    # LLM用のツール定義に変換
    llm_tools = tools_to_llm_format(tools)

    # メッセージ履歴を初期化
    messages = [
        {"role": "user", "content": user_message}
    ]

    # 最大ループ回数（無限ループ防止）
    max_iterations = 10

    for i in range(max_iterations):
        # LLMにリクエストを送信
        response = llm_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=llm_tools,
            messages=messages,
        )

        # レスポンスの内容を解析
        # stop_reason が "tool_use" の場合、ツール呼び出しが必要
        if response.stop_reason == "end_turn":
            # テキスト応答のみ → 最終回答として返す
            final_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text
            return final_text

        # アシスタントの応答をメッセージ履歴に追加
        messages.append({
            "role": "assistant",
            "content": response.content,
        })

        # ツール呼び出しの処理
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                tool_name = block.name
                tool_args = block.input
                tool_use_id = block.id

                print(f"  [ツール呼び出し] {tool_name}({json.dumps(tool_args, ensure_ascii=False)})")

                # MCPサーバーでツールを実行
                try:
                    result = await session.call_tool(
                        name=tool_name,
                        arguments=tool_args,
                    )

                    # ツール実行結果をテキストとして取得
                    result_text = ""
                    for content in result.content:
                        if hasattr(content, "text"):
                            result_text += content.text

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": result_text,
                    })
                    print(f"  [ツール結果] {result_text}")

                except Exception as e:
                    # ツール実行エラーの場合もLLMに伝える
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": f"エラー: {str(e)}",
                        "is_error": True,
                    })

        # ツール結果をメッセージ履歴に追加
        messages.append({
            "role": "user",
            "content": tool_results,
        })

    # 最大ループ回数に達した場合
    return "（最大試行回数に達しました。処理を中断します。）"


# === メインの使用例 ===
async def main():
    # （省略：session、llm_client、toolsは初期化済みとする）

    print("=== MCPエージェント ===")
    print("質問を入力してください（終了: quit）\n")

    while True:
        user_input = input("あなた: ").strip()
        if user_input.lower() == "quit":
            break

        # エージェントループを実行
        answer = await agent_loop(session, llm_client, tools, user_input)
        print(f"\nアシスタント: {answer}\n")
```

<!-- 実装ポイント：
     - LLMの応答にtool_useブロックが含まれる限りループを続ける
     - tool_use_id を正しく対応させることで、LLMがどのツール呼び出しの結果かを識別できる
     - エラーが発生してもis_error: trueでLLMに伝え、LLMが適切にリカバリーできるようにする
     - 無限ループ防止のためmax_iterationsを設ける（実務では5〜20程度）
     - ツール定義の変換（tools_to_llm_format）はLLMプロバイダのAPI仕様に合わせる必要がある -->

</details>

---

### 問題6-7：リソースの読み取りとプロンプトの利用

以下のコードを完成させてください。MCPサーバーからリソースを読み取り、プロンプトを取得して活用する処理です。

```python
async def use_resources_and_prompts(session):
    """リソースとプロンプトを活用する例"""

    # === Part 1: リソースの読み取り ===

    # リソース一覧を取得
    resources = await session.___A___()
    print("【リソース一覧】")
    for r in resources.resources:
        print(f"  {r.uri} ({r.mimeType})")

    # 特定のリソースを読み取り
    content = await session.___B___(uri="config://app")
    for item in content.___C___:
        if hasattr(item, 'text'):
            print(f"設定内容: {item.text}")

    # === Part 2: リソーステンプレートの利用 ===

    # テンプレート一覧を取得
    templates = await session.___D___()
    print("\n【リソーステンプレート】")
    for t in templates.resourceTemplates:
        print(f"  {t.uriTemplate} - {t.name}")

    # テンプレートに値を埋めてリソースを読み取り
    user_data = await session.read_resource(uri="users://user123/profile")

    # === Part 3: プロンプトの利用 ===

    # プロンプト一覧を取得
    prompts = await session.___E___()
    print("\n【プロンプト一覧】")
    for p in prompts.prompts:
        print(f"  {p.name} - {p.description}")

    # プロンプトを取得（引数付き）
    prompt_result = await session.___F___(
        name="code_review",
        arguments={"code": "def hello(): print('hi')"}
    )
    print("\n【プロンプトメッセージ】")
    for msg in prompt_result.___G___:
        print(f"  [{msg.role}] {msg.content}")
```

<details>
<summary>ヒント</summary>

MCP Python SDKの主要メソッドの対応表を参考にしましょう。

| 操作 | メソッド名 |
|------|-----------|
| リソース一覧 | list_resources |
| リソース読み取り | read_resource |
| テンプレート一覧 | list_resource_templates |
| プロンプト一覧 | list_prompts |
| プロンプト取得 | get_prompt |
</details>

<details>
<summary>解答例</summary>

```python
async def use_resources_and_prompts(session):
    """リソースとプロンプトを活用する例"""

    # === Part 1: リソースの読み取り ===

    # A: list_resources — リソース一覧を取得
    resources = await session.list_resources()
    print("【リソース一覧】")
    for r in resources.resources:
        print(f"  {r.uri} ({r.mimeType})")

    # B: read_resource — 指定URIのリソースを読み取り
    content = await session.read_resource(uri="config://app")
    # C: contents — 読み取り結果のコンテンツ配列
    for item in content.contents:
        if hasattr(item, 'text'):
            print(f"設定内容: {item.text}")

    # === Part 2: リソーステンプレートの利用 ===

    # D: list_resource_templates — テンプレート一覧を取得
    templates = await session.list_resource_templates()
    print("\n【リソーステンプレート】")
    for t in templates.resourceTemplates:
        print(f"  {t.uriTemplate} - {t.name}")

    user_data = await session.read_resource(uri="users://user123/profile")

    # === Part 3: プロンプトの利用 ===

    # E: list_prompts — プロンプト一覧を取得
    prompts = await session.list_prompts()
    print("\n【プロンプト一覧】")
    for p in prompts.prompts:
        print(f"  {p.name} - {p.description}")

    # F: get_prompt — 引数を渡してプロンプトを取得
    prompt_result = await session.get_prompt(
        name="code_review",
        arguments={"code": "def hello(): print('hi')"}
    )
    # G: messages — プロンプトのメッセージ配列
    print("\n【プロンプトメッセージ】")
    for msg in prompt_result.messages:
        print(f"  [{msg.role}] {msg.content}")
```

<!-- 各空欄の解説：
     A. list_resources()：サーバーが公開している静的リソースの一覧を返す
     B. read_resource(uri=...)：指定URIのリソース内容を読み取る
     C. contents：ReadResourceResultのプロパティ。ResourceContentsのリスト
     D. list_resource_templates()：URIテンプレートの一覧を返す
     E. list_prompts()：サーバーが公開しているプロンプトの一覧を返す
     F. get_prompt(name=..., arguments=...)：引数を渡してプロンプトを展開
     G. messages：GetPromptResultのプロパティ。PromptMessageのリスト -->

</details>

---

## チャレンジ問題

### 問題6-8：マルチサーバークライアントの設計と実装

複数のMCPサーバーに同時接続し、統合的に管理する「マルチサーバークライアント」を設計・実装してください。

**要件：**

1. 設定ファイル（JSON）から複数サーバーの接続情報を読み取る
2. 全サーバーに同時接続する
3. 全サーバーのツールを統合して一覧表示する（サーバー名のプレフィックス付き）
4. ツール呼び出し時に、適切なサーバーにリクエストをルーティングする
5. 1つのサーバーが接続エラーになっても他のサーバーは動作を継続する

**設定ファイルの形式：**

```json
{
  "servers": {
    "filesystem": {
      "command": "python",
      "args": ["servers/filesystem_server.py"],
      "description": "ファイルシステム操作"
    },
    "github": {
      "command": "python",
      "args": ["servers/github_server.py"],
      "description": "GitHub操作"
    },
    "database": {
      "command": "python",
      "args": ["servers/database_server.py"],
      "description": "データベース操作"
    }
  }
}
```

**期待される動作：**

```
=== マルチサーバー MCP クライアント ===

サーバー接続中...
  ✓ filesystem (ファイルシステム操作) - 3 tools
  ✓ github (GitHub操作) - 5 tools
  ✗ database (データベース操作) - 接続エラー: サーバーが見つかりません

【統合ツール一覧】（2サーバー / 8ツール）
  filesystem::read_file    - ファイルを読み取ります
  filesystem::write_file   - ファイルに書き込みます
  filesystem::list_dir     - ディレクトリ一覧を取得します
  github::create_issue     - イシューを作成します
  github::list_repos       - リポジトリ一覧を取得します
  github::create_pr        - プルリクエストを作成します
  github::search_code      - コードを検索します
  github::get_file         - リポジトリのファイルを取得します

ツール名を入力 (終了: quit): github::create_issue
引数 (JSON): {"title": "バグ修正", "body": "ログイン画面のエラー"}
  → github サーバーに転送...
  → 結果: Issue #42 を作成しました
```

<details>
<summary>ヒント</summary>

設計のポイント：

1. **サーバー管理クラス** を作成し、各サーバーへの接続情報とセッションを保持する
2. **ツール名にプレフィックス** を付けて名前の衝突を防ぐ（`server_name::tool_name`）
3. **ルーティングテーブル** を持ち、ツール名からどのサーバーのセッションに送るかをマッピングする
4. 接続は `asyncio.gather` で並行に行い、`return_exceptions=True` で個別エラーを処理する
5. `contextlib.AsyncExitStack` を使うと、動的な数のasync contextmanagerを管理できます
</details>

<details>
<summary>解答例</summary>

```python
import asyncio
import json
from contextlib import AsyncExitStack
from dataclasses import dataclass, field
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@dataclass
class ServerConnection:
    """1つのMCPサーバーとの接続情報を保持するクラス"""
    name: str
    description: str
    session: ClientSession | None = None
    tools: list = field(default_factory=list)
    connected: bool = False
    error: str | None = None


class MultiServerClient:
    """
    複数のMCPサーバーに同時接続し、統合管理するクライアント。
    ツール名に「サーバー名::」プレフィックスを付けてルーティングします。
    """

    def __init__(self, config_path: str):
        # 設定ファイルを読み込み
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        # サーバー接続情報の辞書
        self.connections: dict[str, ServerConnection] = {}
        # ツール名 → サーバー名のルーティングテーブル
        self.routing_table: dict[str, str] = {}
        # async contextmanagerの管理用
        self.exit_stack = AsyncExitStack()

    async def connect_all(self):
        """全サーバーに接続します"""
        print("サーバー接続中...")

        for server_name, server_config in self.config["servers"].items():
            conn = ServerConnection(
                name=server_name,
                description=server_config.get("description", ""),
            )
            self.connections[server_name] = conn

            try:
                # サーバーパラメータを作成
                params = StdioServerParameters(
                    command=server_config["command"],
                    args=server_config.get("args", []),
                    env=server_config.get("env"),
                )

                # stdioトランスポートで接続
                transport = await self.exit_stack.enter_async_context(
                    stdio_client(params)
                )
                read, write = transport

                # セッションを作成
                session = await self.exit_stack.enter_async_context(
                    ClientSession(read, write)
                )

                # 初期化
                await session.initialize()

                # ツール一覧を取得
                tools_result = await session.list_tools()

                # 接続情報を更新
                conn.session = session
                conn.tools = tools_result.tools
                conn.connected = True

                # ルーティングテーブルに登録
                for tool in tools_result.tools:
                    prefixed_name = f"{server_name}::{tool.name}"
                    self.routing_table[prefixed_name] = server_name

                print(f"  ✓ {server_name} ({conn.description})"
                      f" - {len(conn.tools)} tools")

            except Exception as e:
                conn.error = str(e)
                print(f"  ✗ {server_name} ({conn.description})"
                      f" - 接続エラー: {e}")

    def list_all_tools(self):
        """全サーバーのツールを統合して一覧表示します"""
        connected_count = sum(
            1 for c in self.connections.values() if c.connected
        )
        total_tools = sum(
            len(c.tools) for c in self.connections.values() if c.connected
        )

        print(f"\n【統合ツール一覧】"
              f"（{connected_count}サーバー / {total_tools}ツール）")

        for server_name, conn in self.connections.items():
            if not conn.connected:
                continue
            for tool in conn.tools:
                prefixed = f"{server_name}::{tool.name}"
                print(f"  {prefixed:<30} - {tool.description}")

    async def call_tool(self, prefixed_name: str, arguments: dict) -> str:
        """
        プレフィックス付きツール名でツールを呼び出します。
        適切なサーバーにルーティングして実行します。
        """
        # ルーティングテーブルからサーバーを特定
        if prefixed_name not in self.routing_table:
            return f"エラー: ツール '{prefixed_name}' が見つかりません"

        server_name = self.routing_table[prefixed_name]
        conn = self.connections[server_name]

        if not conn.connected or conn.session is None:
            return f"エラー: サーバー '{server_name}' は接続されていません"

        # プレフィックスを除去して元のツール名を取得
        original_name = prefixed_name.split("::", 1)[1]

        print(f"  → {server_name} サーバーに転送...")

        # MCPサーバーでツールを実行
        try:
            result = await conn.session.call_tool(
                name=original_name,
                arguments=arguments,
            )

            # 結果をテキストに変換
            texts = []
            for content in result.content:
                if hasattr(content, "text"):
                    texts.append(content.text)
            return "  → 結果: " + "\n".join(texts)

        except Exception as e:
            return f"  → 実行エラー: {e}"

    async def close(self):
        """全接続をクリーンアップします"""
        await self.exit_stack.aclose()


async def main():
    """マルチサーバークライアントのメイン処理"""
    print("=== マルチサーバー MCP クライアント ===\n")

    client = MultiServerClient("mcp_servers.json")

    try:
        # 全サーバーに接続
        await client.connect_all()

        # 統合ツール一覧を表示
        client.list_all_tools()
        print()

        # 対話ループ
        while True:
            tool_name = input("ツール名を入力 (終了: quit): ").strip()
            if tool_name.lower() == "quit":
                break

            args_str = input("引数 (JSON): ").strip()
            try:
                arguments = json.loads(args_str) if args_str else {}
            except json.JSONDecodeError as e:
                print(f"  JSON解析エラー: {e}\n")
                continue

            result = await client.call_tool(tool_name, arguments)
            print(result)
            print()

    finally:
        await client.close()
        print("全サーバーから切断しました。")


if __name__ == "__main__":
    asyncio.run(main())
```

<!-- 設計ポイント：
     1. AsyncExitStackを使うことで、動的な数のサーバー接続をクリーンに管理できる
     2. ルーティングテーブル（dict）により、ツール名から即座にサーバーを特定できる（O(1)）
     3. 各サーバーの接続エラーを個別にハンドリングし、他のサーバーに影響を与えない
     4. プレフィックス「server_name::tool_name」で名前空間を分離し、
        異なるサーバーが同名のツールを持っていても衝突しない
     5. finallyブロックで確実にクリーンアップを行い、子プロセスが残らないようにする

     発展的な改善案：
     - サーバーの再接続機能（接続が切れた場合の自動リトライ）
     - ツール呼び出しのタイムアウト設定
     - LLM統合時にtool descriptionにサーバー情報を付加する
     - リソースやプロンプトも同様に統合管理する -->

</details>

---

### 問題6-9：エラーハンドリングとリトライの設計

MCPクライアントにおけるエラーハンドリングとリトライの戦略を設計してください。以下の各シナリオに対して、適切な対処方針とPythonのコード例を記述してください。

**シナリオ：**

1. サーバーとの接続がタイムアウトした場合
2. ツール呼び出しがサーバー側エラー（内部エラー）で失敗した場合
3. サーバーが途中で予期せず切断された場合
4. ツール呼び出しの結果が `isError: true` で返ってきた場合

各シナリオについて以下を記述してください。
- エラーの種類と原因
- 対処方針（リトライすべきか、ユーザーに通知すべきか等）
- Pythonのコード例

<details>
<summary>ヒント</summary>

エラーの性質によって対処が変わります。

- **一時的エラー**（タイムアウト、ネットワーク不安定）→ リトライが有効
- **永続的エラー**（認証失敗、存在しないツール名）→ リトライは無意味
- **サーバー側エラー**（内部エラー）→ 状況に応じてリトライまたは報告
- **ビジネスロジックエラー**（isError: true）→ LLMにフィードバックして別の方法を試す

リトライには指数バックオフ（exponential backoff）を採用するのが一般的です。
</details>

<details>
<summary>解答例</summary>

```python
import asyncio
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class RetryConfig:
    """リトライ設定"""
    max_retries: int = 3           # 最大リトライ回数
    base_delay: float = 1.0        # 初期待機時間（秒）
    max_delay: float = 30.0        # 最大待機時間（秒）
    exponential_base: float = 2.0  # 指数の底


async def retry_with_backoff(func, config: RetryConfig, error_types: tuple):
    """
    指数バックオフ付きのリトライラッパー。
    指定したエラータイプに該当する場合のみリトライします。
    """
    last_error = None
    for attempt in range(config.max_retries + 1):
        try:
            return await func()
        except error_types as e:
            last_error = e
            if attempt < config.max_retries:
                # 指数バックオフで待機時間を計算
                delay = min(
                    config.base_delay * (config.exponential_base ** attempt),
                    config.max_delay,
                )
                logger.warning(
                    f"リトライ {attempt + 1}/{config.max_retries} "
                    f"({delay:.1f}秒後): {e}"
                )
                await asyncio.sleep(delay)
            else:
                logger.error(f"最大リトライ回数に到達: {e}")
    raise last_error


# === シナリオ1：接続タイムアウト ===

async def connect_with_retry(server_params, config=RetryConfig()):
    """
    サーバー接続にリトライを適用します。
    タイムアウトは一時的なエラーのため、リトライが有効です。
    """
    async def attempt_connect():
        # タイムアウトを設定して接続を試行
        try:
            return await asyncio.wait_for(
                establish_connection(server_params),
                timeout=10.0,  # 10秒でタイムアウト
            )
        except asyncio.TimeoutError:
            raise ConnectionError("サーバー接続がタイムアウトしました")

    # 一時的エラー（ConnectionError）はリトライ対象
    return await retry_with_backoff(
        attempt_connect,
        config,
        error_types=(ConnectionError, OSError),
    )


# === シナリオ2：ツール呼び出しのサーバー側エラー ===

async def call_tool_with_retry(session, name, arguments, config=RetryConfig()):
    """
    ツール呼び出しにリトライを適用します。
    サーバー内部エラー（5xx相当）はリトライ、
    クライアントエラー（4xx相当）はリトライしません。
    """
    async def attempt_call():
        try:
            result = await session.call_tool(name=name, arguments=arguments)
            return result
        except Exception as e:
            error_code = getattr(e, "code", None)
            # JSON-RPCのエラーコードで判断
            # -32603（Internal error）はリトライ対象
            # -32602（Invalid params）はリトライしない
            if error_code == -32603:
                raise  # リトライ対象として再送出
            elif error_code == -32602:
                logger.error(f"引数エラー（リトライ不可）: {e}")
                raise  # 呼び出し元に即座に伝播
            else:
                raise

    return await retry_with_backoff(
        attempt_call,
        config,
        error_types=(Exception,),  # 実務ではより具体的な例外型を指定
    )


# === シナリオ3：予期せぬ切断 ===

class ResilientSession:
    """
    接続が切れた場合に自動再接続するセッションラッパー。
    """
    def __init__(self, server_params):
        self.server_params = server_params
        self.session = None
        self._connected = False

    async def ensure_connected(self):
        """接続が切れていれば再接続します"""
        if not self._connected or self.session is None:
            logger.info("再接続を試みます...")
            self.session = await connect_with_retry(self.server_params)
            self._connected = True
            logger.info("再接続に成功しました")

    async def call_tool(self, name, arguments):
        """切断を検知した場合、再接続してリトライします"""
        try:
            await self.ensure_connected()
            return await self.session.call_tool(
                name=name, arguments=arguments
            )
        except (ConnectionError, BrokenPipeError, EOFError) as e:
            # 接続が切れた → 再接続を試みる
            logger.warning(f"接続切断を検知: {e}")
            self._connected = False
            await self.ensure_connected()
            # 再接続後にリトライ（1回のみ）
            return await self.session.call_tool(
                name=name, arguments=arguments
            )


# === シナリオ4：isError: true の処理 ===

async def handle_tool_result(session, name, arguments, llm_client, messages):
    """
    ツール実行結果の isError を確認し、
    エラーの場合はLLMにフィードバックして対処を委ねます。
    """
    result = await session.call_tool(name=name, arguments=arguments)

    if result.isError:
        # isErrorはビジネスロジックエラー（例：ファイルが見つからない）
        # → リトライではなく、LLMにエラー内容を伝えて判断を委ねる
        error_text = result.content[0].text if result.content else "不明なエラー"
        logger.info(f"ツール '{name}' がエラーを返しました: {error_text}")

        # LLMにエラー情報を伝える
        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": "...",  # 実際のIDを使用
                "content": f"エラー: {error_text}",
                "is_error": True,
            }],
        })
        # LLMは別のツールを試す、引数を変えて再試行する、
        # またはユーザーに状況を説明する等の判断を行う
        return None

    return result
```

<!-- エラーハンドリングの設計指針まとめ：

     1. 接続タイムアウト → 指数バックオフでリトライ（一時的障害の可能性が高い）
     2. サーバー内部エラー → エラーコードで判断してリトライ or 即失敗
     3. 予期せぬ切断 → 自動再接続 + 1回リトライ
     4. isError: true → リトライせず、LLMにフィードバックして判断を委ねる

     実務でのベストプラクティス：
     - 全てのリトライにはmax_retriesの上限を設ける
     - 指数バックオフにジッター（ランダム要素）を加えると、
       複数クライアントからの同時リトライを分散できる
     - ログを適切に出力し、障害の診断に役立てる
     - ユーザーへの通知は、リトライを全て使い切った後に行う -->

</details>

---

**お疲れさまでした！** この章の演習を通じて、MCPクライアントの実装に必要な知識が身についたはずです。接続管理、ツール呼び出し、LLM統合、マルチサーバー管理、そしてエラーハンドリングまで、実践的なスキルを習得できました。次の章では、実際にMCPサーバーを構築する演習に進みます。

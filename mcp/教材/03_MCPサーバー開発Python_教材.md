# 第3章：MCPサーバー開発（Python）

## 学習目標

- Python で MCP サーバーを構築できるようになる
- FastMCP を使ったツール・リソース・プロンプトの実装方法を理解する
- Claude Desktop や Claude Code と連携する設定方法を身につける
- MCP Inspector を使ったデバッグ手法を習得する

---

## 3.1 開発環境のセットアップ

| 項目 | 要件 |
|------|------|
| Python | 3.10 以上 |
| パッケージマネージャ | `uv`（推奨）または `pip` |
| MCP SDK | `mcp` パッケージ |

### uv を使ったセットアップ（推奨）

`uv` は高速な Python パッケージマネージャです。MCP 公式が推奨しています。

```bash
# uv のインストール
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# プロジェクト作成とパッケージインストール
uv init my-mcp-server
cd my-mcp-server
uv add "mcp[cli]"
```

### pip を使ったセットアップ

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install "mcp[cli]"
```

> **ポイントまとめ**
> - Python 3.10 以上が必須です（型ヒントの新構文を使用するため）
> - `mcp[cli]` で CLI ツール（MCP Inspector 等）も一緒にインストールされます

---

## 3.2 FastMCP による最小サーバー

FastMCP は、MCP サーバーを簡潔に記述するための高レベル API です。デコレータ（Decorator）ベースで直感的にツールやリソースを定義できます。

```python
# server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-first-server")

@mcp.tool()
def greet(name: str) -> str:
    """指定された名前で挨拶を返します。"""
    return f"こんにちは、{name}さん！"

if __name__ == "__main__":
    mcp.run()
```

```bash
uv run server.py        # uv の場合
python server.py         # pip の場合
```

### 処理の流れ

```
+-------------------+  stdin/stdout  +-------------------+
|   AI アシスタント   | <-- JSON-RPC --> |   MCP サーバー    |
|  (Claude等)       |   リクエスト     |  (server.py)      |
|  "greet を呼んで"  | ------------->  |  greet("太郎")    |
|  結果を受け取る     | <------------- |  → "こんにちは！"  |
+-------------------+                +-------------------+
```

### よくある間違い

| 間違い | 正しい書き方 |
|--------|-------------|
| `FastMCP()` と引数なし | `FastMCP("server-name")` のように名前を指定する |
| `@mcp.tool` と括弧なし | `@mcp.tool()` と括弧を付ける |
| `mcp.run()` を `if __name__` の外に書く | 必ずガード内に書く |

> **ポイントまとめ**
> - `FastMCP` はサーバー名を引数に取ります
> - `@mcp.tool()` デコレータで関数がツールとして公開されます
> - `mcp.run()` はデフォルトで stdio トランスポート（Transport）を使用します

---

## 3.3 ツール（Tool）の実装

ツール（Tool）は、AI が呼び出して処理を実行する機能です。関数の **型ヒント（Type Hint）** からスキーマ（Schema）が自動生成され、**docstring** がツールの説明になります。

### パラメータの型と対応

| Python 型ヒント | JSON Schema 型 | 説明 |
|-----------------|----------------|------|
| `str` | `string` | 文字列 |
| `int` | `integer` | 整数 |
| `float` | `number` | 数値 |
| `bool` | `boolean` | 真偽値 |
| `list[str]` | `array` | 配列 |

### 基本的なツールとオプション引数

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("tool-demo")

@mcp.tool()
def add(a: float, b: float) -> str:
    """2つの数値を加算します。

    Args:
        a: 1つ目の数値
        b: 2つ目の数値
    """
    return f"{a} + {b} = {a + b}"

@mcp.tool()
def search_items(query: str, category: str = "all", max_results: int = 10) -> str:
    """アイテムを検索します。

    Args:
        query: 検索キーワード
        category: カテゴリ（all, books, electronics）
        max_results: 最大取得件数（デフォルト: 10）
    """
    return f"「{query}」で{category}を検索（最大{max_results}件）"
```

デフォルト値を持つパラメータは、自動的にオプション（Optional）として扱われます。

### エラーハンドリング

```python
@mcp.tool()
def divide(a: float, b: float) -> str:
    """割り算を行います。

    Args:
        a: 割られる数
        b: 割る数
    """
    if b == 0:
        raise ValueError("0で割ることはできません。")
    return f"{a} / {b} = {a / b}"
```

`raise ValueError(...)` で例外を送出すると、MCP SDK がエラーレスポンスとしてクライアントに返します。

### よくある間違い

| 間違い | 正しい方法 |
|--------|-----------|
| 戻り値を `dict` で返す | `str` で返す |
| docstring を書かない | 必ず書く（AI の理解に必要） |
| 例外を握りつぶす | 適切なメッセージで `raise` する |

> **ポイントまとめ**
> - 型ヒントが JSON Schema に変換され、AI がパラメータを理解します
> - docstring はツールの説明として公開されるため丁寧に書きましょう
> - エラー時は `ValueError` 等を `raise` するとクライアントに通知されます

---

## 3.4 リソース（Resource）の実装

リソース（Resource）は、AI にデータやコンテキスト情報を読み取り専用で提供する機能です。

### 静的リソース

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("resource-demo")

@mcp.resource("config://app/settings")
def get_app_settings() -> str:
    """アプリケーションの設定情報を返します。"""
    return "バージョン: 2.1.0\n環境: production\nデバッグ: OFF"
```

### URI スキーム設計

```
config://app/settings     ... 設定情報
docs://api/reference      ... ドキュメント
data://users/list         ... データ一覧
```

### 動的リソース（リソーステンプレート）

URI に `{パラメータ名}` を含めると、動的にリソースを生成できます。

```python
@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    """指定ユーザーのプロフィールを返します。"""
    profiles = {"001": "田中太郎, 開発部", "002": "鈴木花子, 企画部"}
    return profiles.get(user_id, f"ユーザー {user_id} は未登録です")
```

### ツールとリソースの使い分け

| リソース (Resource) | ツール (Tool) |
|---------------------|---------------|
| データの読み取り専用 | 処理の実行（副作用あり） |
| URI でアクセス | 関数呼び出しでアクセス |
| 例: 設定情報、ドキュメント | 例: 計算、API呼び出し |

> **ポイントまとめ**
> - リソースは読み取り専用のデータ提供手段です
> - `{パラメータ名}` で動的リソースを作れます

---

## 3.5 プロンプト（Prompt）の実装

プロンプト（Prompt）は、再利用可能なプロンプトテンプレートを定義する機能です。

### 基本のプロンプトと引数付きプロンプト

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("prompt-demo")

@mcp.prompt()
def code_review() -> str:
    """コードレビューを依頼するプロンプトです。"""
    return """経験豊富なシニアエンジニアとして、以下の観点でレビューしてください：
1. バグや潜在的な問題  2. パフォーマンス  3. 可読性  4. セキュリティ"""

@mcp.prompt()
def explain_code(language: str, level: str = "beginner") -> str:
    """コード解説プロンプトです。

    Args:
        language: プログラミング言語
        level: 解説レベル（beginner, intermediate, advanced）
    """
    names = {"beginner": "初心者", "intermediate": "中級者", "advanced": "上級者"}
    target = names.get(level, "初心者")
    return f"{target}向けに、以下の{language}コードを解説してください。"
```

### 複数メッセージのプロンプト

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import UserMessage, AssistantMessage

mcp = FastMCP("multi-message-prompt")

@mcp.prompt()
def debug_help(error_message: str) -> list:
    """デバッグ支援プロンプトです。

    Args:
        error_message: エラーメッセージ
    """
    return [
        UserMessage(f"以下のエラーが発生しています:\n```\n{error_message}\n```"),
        AssistantMessage("エラー内容を確認しました。いくつか質問させてください。"),
        UserMessage("はい、お願いします。"),
    ]
```

> **ポイントまとめ**
> - 引数で動的にプロンプト内容を変えられます
> - `UserMessage` / `AssistantMessage` で複数ターンの会話を定義できます

---

## 3.6 サーバーの起動と接続

### Claude Desktop の設定（claude_desktop_config.json）

| OS | 設定ファイルのパス |
|----|-------------------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/my-mcp-server", "server.py"]
    }
  }
}
```

### Claude Code の設定（.mcp.json）

プロジェクトルートに `.mcp.json` を配置するか、CLI で追加します。

```bash
claude mcp add my-server -- uv run --directory /path/to/my-mcp-server server.py
```

### 完全な実装例

```python
# server.py - ツール・リソース・プロンプトを含む完全な例
import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-complete-server")

@mcp.tool()
def get_current_time() -> str:
    """現在の日時を返します。"""
    return datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

@mcp.tool()
def calculate_bmi(height_cm: float, weight_kg: float) -> str:
    """BMIを計算します。

    Args:
        height_cm: 身長（cm）
        weight_kg: 体重（kg）
    """
    if height_cm <= 0 or weight_kg <= 0:
        raise ValueError("身長と体重は正の数を指定してください。")
    bmi = weight_kg / (height_cm / 100) ** 2
    return f"BMI: {bmi:.1f}"

@mcp.resource("info://server/status")
def server_status() -> str:
    """サーバーの状態を返します。"""
    return "ステータス: 正常稼働中"

@mcp.prompt()
def summarize(topic: str) -> str:
    """要約を依頼するプロンプトです。

    Args:
        topic: 要約するトピック
    """
    return f"「{topic}」について3つのポイントに絞って簡潔に要約してください。"

if __name__ == "__main__":
    mcp.run()
```

### よくある間違い

| 間違い | 正しい方法 |
|--------|-----------|
| 設定ファイルに相対パスを書く | 絶対パスを使う |
| 仮想環境外の `python` を指定 | 仮想環境内の Python パスを指定する |
| サーバーに `print()` を入れる | stdout は通信用なので使わない（3.7 参照） |

> **ポイントまとめ**
> - Claude Desktop は `claude_desktop_config.json`、Claude Code は `.mcp.json` で設定します
> - パスは必ず絶対パスで指定しましょう

---

## 3.7 デバッグ手法

### MCP Inspector

MCP Inspector は、サーバーをブラウザ上で対話的にテストできるツールです。

```bash
npx @modelcontextprotocol/inspector uv run server.py
```

```
+---------------------------------------------+
|          MCP Inspector (ブラウザ)             |
|  [Tools]  [Resources]  [Prompts]            |
|                                             |
|  ツール: greet                               |
|  | name: [太郎] |  [実行]                    |
|  結果: "こんにちは、太郎さん！"               |
|                                             |
|  --- ログ ---                                |
|  → {"method":"tools/call",...}              |
|  ← {"content":[{"type":"text",...}]}        |
+---------------------------------------------+
```

### ログ出力（print は使わない）

stdout は JSON-RPC 通信に使われるため、`print()` は通信を破壊します。`logging` + `sys.stderr` を使いましょう。

```python
import sys, logging
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.DEBUG, stream=sys.stderr,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("debug-demo")

@mcp.tool()
def process_data(data: str) -> str:
    """データを処理します。

    Args:
        data: 処理するデータ
    """
    logger.info(f"process_data 呼び出し: data={data}")
    result = data.upper()
    logger.info(f"処理完了: result={result}")
    return result
```

### よくあるトラブルと対処法

| トラブル | 原因 | 対処法 |
|---------|------|--------|
| サーバーが起動しない | Python バージョンが古い | 3.10 以上か確認 |
| ツールが表示されない | デコレータの `()` が抜けている | `@mcp.tool()` と括弧を付ける |
| 通信エラー | `print()` を使っている | `logging` + `stderr` に変更 |
| 設定が読まれない | JSON 構文エラー | バリデータで確認 |
| パスが見つからない | 相対パス | 絶対パスに変更 |

### デバッグの手順

```
1. MCP Inspector で動作確認  →  2. stderr にログ出力
      ↓                              ↓
3. クライアントのログ確認  →  4. JSON-RPC メッセージ検証
```

> **ポイントまとめ**
> - MCP Inspector は開発の必須ツールです。最初にここでテストしましょう
> - `print()` は絶対に使わず、`logging` + `sys.stderr` を使いましょう
> - トラブル時はバージョン、パス設定、JSON 構文を順に確認しましょう

# 第3章 演習：FastMCPによるPythonサーバー開発

---

## 基本問題

---

### 問題1：最小構成のMCPサーバー（基本）

FastMCPを使って、「Hello, MCP!」と返すだけの最小構成のMCPサーバーを作成してください。
サーバー名は `"greeting-server"` とします。

**期待される出力（ツール呼び出し結果）：**
```
Hello, MCP!
```

<details>
<summary>ヒント</summary>

- `from mcp.server.fastmcp import FastMCP` でインポートします
- `FastMCP("サーバー名")` でインスタンスを生成します
- `@mcp.tool()` デコレータでツールを登録します
- `mcp.run()` でサーバーを起動します

</details>

<details>
<summary>解答例</summary>

```python
# FastMCPをインポート
from mcp.server.fastmcp import FastMCP

# サーバーインスタンスを生成（名前を指定）
mcp = FastMCP("greeting-server")

# @mcp.tool() でツールを登録
@mcp.tool()
def greet() -> str:
    """挨拶メッセージを返します。"""
    return "Hello, MCP!"

# サーバーを起動
if __name__ == "__main__":
    mcp.run()
```

**ポイント：**
- `FastMCP()` の引数はサーバーの識別名です
- `@mcp.tool()` を付けた関数が、MCPツールとして公開されます
- docstringはクライアント側でツールの説明として表示されます

</details>

---

### 問題2：型ヒントとdocstringの役割（基本）

以下のコードには問題があります。FastMCPにおける型ヒントとdocstringの役割を踏まえて、正しく修正してください。

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("calc-server")

@mcp.tool()
def add(a, b):
    return a + b
```

**修正後にツールスキーマとして期待される情報：**
```
ツール名: add
説明: 2つの数値を加算して結果を返します。
パラメータ:
  - a (number): 足される数
  - b (number): 足す数
```

<details>
<summary>ヒント</summary>

- FastMCPは型ヒントからJSONスキーマのパラメータ型を自動生成します
- 型ヒントがないと、クライアントはどんな値を渡すべきかわかりません
- docstringはツールの説明（description）として使われます
- 引数の説明は `Annotated` と `Field` で付与できます

</details>

<details>
<summary>解答例</summary>

```python
from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

mcp = FastMCP("calc-server")

@mcp.tool()
def add(
    a: Annotated[float, Field(description="足される数")],
    b: Annotated[float, Field(description="足す数")]
) -> float:
    """2つの数値を加算して結果を返します。"""
    return a + b
```

**ポイント：**
- `float` 型ヒントにより、JSONスキーマでは `number` 型として公開されます
- docstringがツール全体の説明になります
- `Annotated` + `Field(description=...)` で各パラメータの説明を付与できます
- 型ヒントがないとFastMCPはスキーマを正しく生成できません

</details>

---

### 問題3：複数ツールの登録（基本）

1つのMCPサーバーに以下の3つのツールを登録してください。

1. `to_upper(text: str) -> str` ：テキストを大文字に変換
2. `to_lower(text: str) -> str` ：テキストを小文字に変換
3. `char_count(text: str) -> int` ：テキストの文字数を返す

**期待される出力例：**
```
to_upper("hello") → "HELLO"
to_lower("WORLD") → "world"
char_count("MCP") → 3
```

<details>
<summary>ヒント</summary>

- 1つの `FastMCP` インスタンスに対して `@mcp.tool()` を複数回使えます
- 各関数にdocstringを忘れずに付けましょう

</details>

<details>
<summary>解答例</summary>

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("text-tools")

@mcp.tool()
def to_upper(text: str) -> str:
    """テキストを大文字に変換します。"""
    return text.upper()

@mcp.tool()
def to_lower(text: str) -> str:
    """テキストを小文字に変換します。"""
    return text.lower()

@mcp.tool()
def char_count(text: str) -> int:
    """テキストの文字数を返します。"""
    return len(text)

if __name__ == "__main__":
    mcp.run()
```

**ポイント：**
- `@mcp.tool()` は何度でも使用でき、すべての関数がツールとして公開されます
- 関数名がそのままツール名になります
- 返り値の型ヒント（`-> str`, `-> int`）も正しく指定しましょう

</details>

---

### 問題4：Resourceの基本（基本）

`@mcp.resource()` を使って、サーバーのバージョン情報を返すリソースを作成してください。
リソースURIは `config://version` とします。

**期待される出力（リソース読み取り結果）：**
```
MyApp v2.1.0 - Released 2026-03-01
```

<details>
<summary>ヒント</summary>

- `@mcp.resource("URI")` でリソースを登録します
- リソースはツールと異なり、引数を取らずデータを返す用途に使います

</details>

<details>
<summary>解答例</summary>

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("config-server")

# @mcp.resource() でリソースを登録
@mcp.resource("config://version")
def get_version() -> str:
    """アプリケーションのバージョン情報を返します。"""
    return "MyApp v2.1.0 - Released 2026-03-01"

if __name__ == "__main__":
    mcp.run()
```

**ポイント：**
- `@mcp.resource()` の引数にリソースのURIを指定します
- リソースはLLMが「読み取る」データを提供する仕組みです
- ツール（Tool）は「操作」、リソース（Resource）は「参照」という使い分けが重要です

</details>

---

### 問題5：Promptの基本（基本）

`@mcp.prompt()` を使って、コードレビューを依頼するプロンプトテンプレートを作成してください。
引数として `code`（レビュー対象コード）と `language`（プログラミング言語）を受け取ります。

**期待される出力（プロンプト展開結果）：**
```
以下のPythonコードをレビューしてください。

コード:
print("hello")

観点：
- バグや潜在的な問題はないか
- 可読性は十分か
- パフォーマンスの改善余地はあるか
```

<details>
<summary>ヒント</summary>

- `@mcp.prompt()` でプロンプトテンプレートを登録します
- 引数はテンプレート内で利用でき、LLMに渡すメッセージを組み立てます

</details>

<details>
<summary>解答例</summary>

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("review-server")

@mcp.prompt()
def code_review(code: str, language: str) -> list[base.Message]:
    """指定されたコードのレビューを依頼するプロンプトです。"""
    return [
        base.UserMessage(
            content=f"""以下の{language}コードをレビューしてください。

コード:
{code}

観点：
- バグや潜在的な問題はないか
- 可読性は十分か
- パフォーマンスの改善余地はあるか"""
        )
    ]

if __name__ == "__main__":
    mcp.run()
```

**ポイント：**
- `@mcp.prompt()` はLLMに渡すプロンプトのテンプレートを定義します
- `Message` オブジェクトのリストを返すのが正式な形式です
- プロンプトはクライアント側でユーザーが選択して利用します

</details>

---

## 応用問題

---

### 問題6：単位変換ツールサーバー（応用）

以下の単位変換ツールを持つMCPサーバーを実装してください。

1. `celsius_to_fahrenheit(celsius: float) -> str`：摂氏→華氏
2. `km_to_miles(km: float) -> str`：キロメートル→マイル
3. `kg_to_pounds(kg: float) -> str`：キログラム→ポンド

各ツールは変換結果を見やすい文字列で返してください。

**期待される出力例：**
```
celsius_to_fahrenheit(100) → "100.0°C = 212.0°F"
km_to_miles(10) → "10.0km = 6.21miles"
kg_to_pounds(5) → "5.0kg = 11.02lbs"
```

<details>
<summary>ヒント</summary>

- 華氏 = 摂氏 × 9/5 + 32
- 1km = 0.621371 miles
- 1kg = 2.20462 pounds
- `round()` で小数点以下の桁数を制御しましょう

</details>

<details>
<summary>解答例</summary>

```python
from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

mcp = FastMCP("unit-converter")

@mcp.tool()
def celsius_to_fahrenheit(
    celsius: Annotated[float, Field(description="摂氏温度")]
) -> str:
    """摂氏温度を華氏温度に変換します。"""
    fahrenheit = round(celsius * 9 / 5 + 32, 2)
    return f"{celsius}°C = {fahrenheit}°F"

@mcp.tool()
def km_to_miles(
    km: Annotated[float, Field(description="キロメートル")]
) -> str:
    """キロメートルをマイルに変換します。"""
    miles = round(km * 0.621371, 2)
    return f"{km}km = {miles}miles"

@mcp.tool()
def kg_to_pounds(
    kg: Annotated[float, Field(description="キログラム")]
) -> str:
    """キログラムをポンドに変換します。"""
    pounds = round(kg * 2.20462, 2)
    return f"{kg}kg = {pounds}lbs"

if __name__ == "__main__":
    mcp.run()
```

**ポイント：**
- 返り値を `str` にすることで、LLMが結果をそのまま自然言語として扱いやすくなります
- `Annotated` + `Field` で各引数に説明を付けると、LLMが適切に引数を設定できます

</details>

---

### 問題7：テキスト分析ツールサーバー（応用）

テキストを受け取り、以下の分析結果を辞書で返すMCPツール `analyze_text` を実装してください。

分析項目：
- 文字数（スペース含む）
- 文字数（スペース除く）
- 単語数（スペース区切り）
- 行数
- 最も長い行の文字数

**期待される出力例：**
```json
{
  "total_chars": 45,
  "chars_no_spaces": 38,
  "word_count": 8,
  "line_count": 3,
  "longest_line_length": 20
}
```

<details>
<summary>ヒント</summary>

- `len(text)` で全文字数が取れます
- `text.replace(" ", "")` でスペースを除去できます
- `text.split()` で単語に分割できます
- `text.split("\n")` で行に分割できます
- `max()` と `len()` を組み合わせて最長行を求めます

</details>

<details>
<summary>解答例</summary>

```python
from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

mcp = FastMCP("text-analyzer")

@mcp.tool()
def analyze_text(
    text: Annotated[str, Field(description="分析対象のテキスト")]
) -> dict:
    """テキストの統計情報を分析して返します。"""
    lines = text.split("\n")
    return {
        "total_chars": len(text),
        "chars_no_spaces": len(text.replace(" ", "")),
        "word_count": len(text.split()),
        "line_count": len(lines),
        "longest_line_length": max(len(line) for line in lines)
    }

if __name__ == "__main__":
    mcp.run()
```

**ポイント：**
- 返り値を `dict` にすると、FastMCPが自動的にJSON形式に変換してクライアントへ返します
- LLMは構造化されたデータを受け取ることで、正確に情報を伝えられます

</details>

---

### 問題8：リソーステンプレートの活用（応用）

`@mcp.resource()` のURIテンプレート機能を使って、ユーザーIDに応じたプロフィール情報を返すリソースを作成してください。

URIは `users://{user_id}/profile` の形式とします。以下のダミーデータを使ってください。

```python
USERS = {
    "u001": {"name": "田中太郎", "role": "エンジニア", "level": 5},
    "u002": {"name": "佐藤花子", "role": "デザイナー", "level": 3},
    "u003": {"name": "鈴木一郎", "role": "マネージャー", "level": 7},
}
```

**期待される出力例（users://u001/profile の読み取り結果）：**
```
名前: 田中太郎
役割: エンジニア
レベル: 5
```

<details>
<summary>ヒント</summary>

- URIテンプレートでは `{パラメータ名}` の部分が関数の引数に自動マッピングされます
- 存在しないユーザーIDの場合はエラーメッセージを返しましょう

</details>

<details>
<summary>解答例</summary>

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("user-server")

USERS = {
    "u001": {"name": "田中太郎", "role": "エンジニア", "level": 5},
    "u002": {"name": "佐藤花子", "role": "デザイナー", "level": 3},
    "u003": {"name": "鈴木一郎", "role": "マネージャー", "level": 7},
}

# URIテンプレートを使ったリソース定義
@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    """指定されたユーザーIDのプロフィール情報を返します。"""
    if user_id not in USERS:
        return f"エラー: ユーザーID '{user_id}' は見つかりません。"

    user = USERS[user_id]
    return f"名前: {user['name']}\n役割: {user['role']}\nレベル: {user['level']}"

if __name__ == "__main__":
    mcp.run()
```

**ポイント：**
- `{user_id}` の部分がリソーステンプレートとして機能し、動的なURIに対応できます
- テンプレート内の変数名と関数の引数名は一致させる必要があります
- 存在しないIDへのアクセスに対するエラーハンドリングも重要です

</details>

---

### 問題9：エラーハンドリング付きツール（応用）

以下の仕様を満たすJSON解析ツールを実装してください。

- ツール名：`parse_json`
- 入力：JSON文字列
- 正常時：パースした結果のキー一覧と値の型を返す
- 異常時：エラーメッセージを返す（サーバーがクラッシュしないこと）

**期待される出力例（正常時）：**
```
解析結果（3個のキー）:
  - name: str
  - age: int
  - active: bool
```

**期待される出力例（異常時）：**
```
JSON解析エラー: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

<details>
<summary>ヒント</summary>

- `json.loads()` でパースし、`try/except` で `json.JSONDecodeError` を捕捉します
- `type(value).__name__` で値の型名を取得できます

</details>

<details>
<summary>解答例</summary>

```python
import json
from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

mcp = FastMCP("json-parser")

@mcp.tool()
def parse_json(
    json_string: Annotated[str, Field(description="解析対象のJSON文字列")]
) -> str:
    """JSON文字列を解析し、構造情報を返します。"""
    try:
        data = json.loads(json_string)

        # 辞書の場合はキーと型を一覧表示
        if isinstance(data, dict):
            lines = [f"解析結果（{len(data)}個のキー）:"]
            for key, value in data.items():
                type_name = type(value).__name__
                lines.append(f"  - {key}: {type_name}")
            return "\n".join(lines)

        # リストの場合は要素数と型を表示
        elif isinstance(data, list):
            return f"解析結果: {len(data)}個の要素を持つ配列"

        else:
            return f"解析結果: {type(data).__name__} 型の値 = {data}"

    except json.JSONDecodeError as e:
        # エラーを返すが、サーバーはクラッシュしない
        return f"JSON解析エラー: {e}"

if __name__ == "__main__":
    mcp.run()
```

**ポイント：**
- MCPツール内で例外が発生するとサーバー全体に影響する可能性があります
- `try/except` で例外を捕捉し、エラーメッセージとして返すのがベストプラクティスです
- LLMはエラーメッセージを見て、ユーザーに修正方法を提案できます

</details>

---

## チャレンジ問題

---

### 問題10：総合MCPサーバーの設計と実装（チャレンジ）

以下の仕様を満たす「タスク管理MCPサーバー」を設計・実装してください。
Tools、Resources、Promptsの3つの機能をすべて組み合わせます。

**仕様：**

**Tools（ツール）：**
1. `add_task(title, priority)` - タスクを追加（priorityは "high" / "medium" / "low"）
2. `complete_task(task_id)` - タスクを完了にする
3. `list_tasks(status)` - タスク一覧を返す（status: "all" / "pending" / "completed"）

**Resources（リソース）：**
1. `tasks://summary` - タスクの統計サマリー（総数、完了数、未完了数、優先度別集計）
2. `tasks://{task_id}/detail` - 個別タスクの詳細情報

**Prompts（プロンプト）：**
1. `daily_report` - 当日のタスク状況をレポートするプロンプトテンプレート

**期待される動作例：**
```
# ツールの使用例
add_task("MCPの学習", "high")
→ "タスクを追加しました: [T001] MCPの学習 (優先度: high)"

add_task("ドキュメント整理", "low")
→ "タスクを追加しました: [T002] ドキュメント整理 (優先度: low)"

complete_task("T001")
→ "タスク [T001] を完了にしました: MCPの学習"

list_tasks("all")
→ "[✓] T001: MCPの学習 (high)
   [ ] T002: ドキュメント整理 (low)"

# リソースの読み取り例
tasks://summary
→ "総タスク数: 2 | 完了: 1 | 未完了: 1
   優先度別: high=1, medium=0, low=1"

# プロンプトの使用例
daily_report
→ "以下は本日のタスク状況です。分析してアドバイスをお願いします。..."
```

<details>
<summary>ヒント</summary>

- タスクデータはサーバー内のグローバル辞書で管理します（永続化不要）
- タスクIDは `T001`, `T002` のように連番で自動生成します
- `Literal["high", "medium", "low"]` を使うと、引数の選択肢を制限できます
- Resourceのサマリーは関数内で毎回辞書を集計します
- Promptではタスク一覧を埋め込んだメッセージを返します

</details>

<details>
<summary>解答例</summary>

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from typing import Annotated, Literal
from pydantic import Field
from datetime import datetime

mcp = FastMCP("task-manager")

# タスクデータを保持する辞書
tasks: dict[str, dict] = {}
task_counter = 0

def generate_task_id() -> str:
    """連番のタスクIDを生成します。"""
    global task_counter
    task_counter += 1
    return f"T{task_counter:03d}"

# ==================== Tools ====================

@mcp.tool()
def add_task(
    title: Annotated[str, Field(description="タスクのタイトル")],
    priority: Annotated[
        Literal["high", "medium", "low"],
        Field(description="優先度（high / medium / low）")
    ]
) -> str:
    """新しいタスクを追加します。"""
    task_id = generate_task_id()
    tasks[task_id] = {
        "title": title,
        "priority": priority,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }
    return f"タスクを追加しました: [{task_id}] {title} (優先度: {priority})"

@mcp.tool()
def complete_task(
    task_id: Annotated[str, Field(description="完了にするタスクのID（例: T001）")]
) -> str:
    """指定されたタスクを完了にします。"""
    if task_id not in tasks:
        return f"エラー: タスク {task_id} は存在しません。"

    if tasks[task_id]["status"] == "completed":
        return f"タスク {task_id} は既に完了しています。"

    tasks[task_id]["status"] = "completed"
    tasks[task_id]["completed_at"] = datetime.now().isoformat()
    return f"タスク [{task_id}] を完了にしました: {tasks[task_id]['title']}"

@mcp.tool()
def list_tasks(
    status: Annotated[
        Literal["all", "pending", "completed"],
        Field(description="フィルタ条件（all / pending / completed）")
    ] = "all"
) -> str:
    """タスク一覧を返します。"""
    if not tasks:
        return "タスクはまだ登録されていません。"

    lines = []
    for task_id, task in tasks.items():
        if status != "all" and task["status"] != status:
            continue
        mark = "✓" if task["status"] == "completed" else " "
        lines.append(f"[{mark}] {task_id}: {task['title']} ({task['priority']})")

    if not lines:
        return f"条件 '{status}' に一致するタスクはありません。"

    return "\n".join(lines)

# ==================== Resources ====================

@mcp.resource("tasks://summary")
def get_task_summary() -> str:
    """タスクの統計サマリーを返します。"""
    total = len(tasks)
    completed = sum(1 for t in tasks.values() if t["status"] == "completed")
    pending = total - completed

    # 優先度別集計
    priority_count = {"high": 0, "medium": 0, "low": 0}
    for task in tasks.values():
        priority_count[task["priority"]] += 1

    return (
        f"総タスク数: {total} | 完了: {completed} | 未完了: {pending}\n"
        f"優先度別: high={priority_count['high']}, "
        f"medium={priority_count['medium']}, "
        f"low={priority_count['low']}"
    )

@mcp.resource("tasks://{task_id}/detail")
def get_task_detail(task_id: str) -> str:
    """個別タスクの詳細情報を返します。"""
    if task_id not in tasks:
        return f"エラー: タスク {task_id} は存在しません。"

    t = tasks[task_id]
    status_text = "完了" if t["status"] == "completed" else "未完了"
    detail = (
        f"タスクID: {task_id}\n"
        f"タイトル: {t['title']}\n"
        f"優先度: {t['priority']}\n"
        f"状態: {status_text}\n"
        f"作成日時: {t['created_at']}"
    )
    if t["completed_at"]:
        detail += f"\n完了日時: {t['completed_at']}"
    return detail

# ==================== Prompts ====================

@mcp.prompt()
def daily_report() -> list[base.Message]:
    """本日のタスク状況をレポートするプロンプトです。"""
    # 現在のタスク一覧を組み立てる
    if not tasks:
        task_info = "現在タスクは登録されていません。"
    else:
        lines = []
        for task_id, task in tasks.items():
            mark = "✓" if task["status"] == "completed" else " "
            lines.append(f"[{mark}] {task_id}: {task['title']} (優先度: {task['priority']})")
        task_info = "\n".join(lines)

    total = len(tasks)
    completed = sum(1 for t in tasks.values() if t["status"] == "completed")

    return [
        base.UserMessage(
            content=f"""以下は本日のタスク状況です。分析してアドバイスをお願いします。

日時: {datetime.now().strftime('%Y-%m-%d %H:%M')}
総タスク数: {total} | 完了: {completed} | 未完了: {total - completed}

タスク一覧:
{task_info}

以下の観点でアドバイスをください：
1. 優先度の高い未完了タスクはあるか
2. 今日中に完了すべきタスクの提案
3. タスク管理の改善点"""
        )
    ]

if __name__ == "__main__":
    mcp.run()
```

**ポイント：**
- Tools / Resources / Prompts の3つを組み合わせることで、LLMに豊富なコンテキストを提供できます
- `Literal` 型を使うことで、LLMが不正な値を渡すリスクを減らせます
- グローバル変数でのデータ管理はプロトタイプ向けです。本番環境ではデータベースを使います
- Promptsの中からサーバー内のデータを参照することで、動的なプロンプトが生成できます

</details>

---

### 問題11：Contextを活用したログ出力とプログレス通知（チャレンジ）

FastMCPの `Context` オブジェクトを使って、以下の機能を持つファイル処理シミュレーションツールを実装してください。

**仕様：**
- ツール名：`process_files`
- 引数：`file_count`（処理するファイル数）
- 動作：
  - 処理開始をログに記録
  - 各ファイル処理ごとにプログレスを通知
  - 処理完了をログに記録
  - 処理結果のサマリーを返す

**期待される動作例（file_count=3の場合）：**
```
[ログ] ファイル処理を開始します（3ファイル）
[プログレス] 1/3 完了 (33%)
[プログレス] 2/3 完了 (67%)
[プログレス] 3/3 完了 (100%)
[ログ] ファイル処理が完了しました

結果: 3ファイルの処理が正常に完了しました。
```

<details>
<summary>ヒント</summary>

- `from mcp.server.fastmcp import FastMCP, Context` でContextをインポートします
- 関数の引数に `ctx: Context` を追加すると、FastMCPが自動的に注入します
- `ctx.info()` / `ctx.debug()` / `ctx.warning()` / `ctx.error()` でログを出力します
- `await ctx.report_progress(current, total)` でプログレスを通知します
- Context を使う場合は関数を `async def` にする必要があります

</details>

<details>
<summary>解答例</summary>

```python
import asyncio
from mcp.server.fastmcp import FastMCP, Context
from typing import Annotated
from pydantic import Field

mcp = FastMCP("file-processor")

@mcp.tool()
async def process_files(
    file_count: Annotated[int, Field(description="処理するファイル数", ge=1, le=100)],
    ctx: Context
) -> str:
    """指定された数のファイルを処理するシミュレーションです。"""
    # 処理開始のログ
    ctx.info(f"ファイル処理を開始します（{file_count}ファイル）")

    processed = 0
    errors = 0

    for i in range(1, file_count + 1):
        # ファイル処理のシミュレーション（0.5秒待機）
        await asyncio.sleep(0.5)

        processed += 1

        # プログレスの通知
        await ctx.report_progress(i, file_count)
        ctx.debug(f"ファイル {i}/{file_count} を処理しました")

    # 処理完了のログ
    ctx.info("ファイル処理が完了しました")

    return f"結果: {processed}ファイルの処理が正常に完了しました。（エラー: {errors}件）"

if __name__ == "__main__":
    mcp.run()
```

**ポイント：**
- `Context` はFastMCPがツール呼び出し時に自動注入する特別な引数です
- `Context` はMCPスキーマ上のパラメータには含まれません（LLMには見えない内部引数です）
- `report_progress()` はクライアントにリアルタイムで進捗を通知できます
- `async def` にすることで、非同期処理（I/O待ち等）を効率的に行えます
- `Field(ge=1, le=100)` でバリデーションも設定できます

</details>

---

**お疲れさまでした！** この演習を通じて、FastMCPによるPython MCPサーバー開発の基本から応用までを実践できました。次の章ではTypeScript SDKを使ったサーバー開発に挑戦します。

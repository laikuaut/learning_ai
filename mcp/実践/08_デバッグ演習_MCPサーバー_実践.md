# 実践課題08：デバッグ演習 ─ MCPサーバー ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第2章（MCPアーキテクチャ）、第3章（MCPサーバー開発Python）、第5章（MCPの3つの機能）、第8章（運用・セキュリティ）
> **課題の種類**: デバッグ
> **学習目標**: バグのあるMCPサーバーコードを読み解き、原因を特定して修正する力を養う。MCPプロトコル、FastMCP API、セキュリティの知識を総合的に活用する

---

## 課題の説明

以下の「TODO管理MCPサーバー」には **10個のバグ** が埋め込まれています。プログラムを分析し、すべてのバグを見つけて修正してください。

バグの種類は以下に分類されます。

```
┌─────────────────────────────────────────────────┐
│  バグの分類                                       │
│                                                  │
│  ■ 構文・型エラー（2個）                           │
│    → Pythonの文法やFastMCPの型定義の間違い         │
│                                                  │
│  ■ ロジックエラー（3個）                           │
│    → コードは動くが、結果が意図と異なる             │
│                                                  │
│  ■ API使用ミス（3個）                              │
│    → FastMCPやMCPプロトコルの仕様を誤って使用      │
│                                                  │
│  ■ セキュリティバグ（2個）                         │
│    → 攻撃に対して脆弱な実装                        │
│                                                  │
└─────────────────────────────────────────────────┘
```

### 進め方

1. 以下のバグ入りコードを読む
2. 各バグのコメント（`# バグN`）を手がかりに問題を特定する
3. 修正内容とその理由を記述する
4. 修正後のコードを動作確認する

---

## バグ入りコード

以下のコードを `todo_server_buggy.py` として保存してください。

```python
"""
TODO管理MCPサーバー（バグ入り版）
このコードには10個のバグが含まれています。すべて修正してください。
"""
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("todo-server")

# ── データストア ──
todos: list[dict] = []
next_id = 1


# ── Tools ──

@mcp.tool()
def add_todo(title: str, priority: str = "中" description: str = "") -> str:  # バグ1
    """TODOを追加します。

    Args:
        title: TODOのタイトル
        priority: 優先度（"高" / "中" / "低"）
        description: 詳細な説明
    """
    global next_id

    todo = {
        "id": next_id,
        "title": title,
        "priority": priority,
        "description": description,
        "done": False,
    }
    todos.append(todo)
    next_id += 1
    return f"TODOを追加しました（ID: {todo['id']}）"


@mcp.tool()
def complete_todo(todo_id: str) -> str:  # バグ2
    """指定IDのTODOを完了にします。

    Args:
        todo_id: 完了にするTODOのID
    """
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = True
            return f"TODO「{todo['title']}」を完了にしました"
    return f"ID {todo_id} のTODOが見つかりません"


@mcp.tool()
def delete_todo(todo_id: int) -> str:
    """指定IDのTODOを削除します。

    Args:
        todo_id: 削除するTODOのID
    """
    for todo in todos:  # バグ3
        if todo["id"] == todo_id:
            todos.remove(todo)
            return f"TODO「{todo['title']}」を削除しました"
    return f"ID {todo_id} のTODOが見つかりません"


@mcp.tool()
def search_todos(keyword: str) -> str:
    """キーワードでTODOを検索します。

    Args:
        keyword: 検索キーワード
    """
    results = []
    for todo in todos:
        if keyword in todo["title"]:  # バグ4
            results.append(todo)

    lines = [f"検索結果: {len(results)}件"]
    for todo in results:
        status = "✓" if todo["done"] else "○"
        lines.append(f"  {status} [{todo['id']}] {todo['title']}")
    return "\n".join(lines)


@mcp.tool()
def list_todos(show_completed: bool = True) -> str:
    """TODO一覧を表示します。

    Args:
        show_completed: 完了済みも表示するか
    """
    filtered = todos
    if not show_completed:
        filtered = [t for t in todos if t["done"]]  # バグ5

    if not filtered:
        return "TODOはありません"

    lines = [f"TODO一覧（{len(filtered)}件）:"]
    for todo in filtered:
        status = "✓" if todo["done"] else "○"
        lines.append(
            f"  {status} [{todo['id']}] {todo['title']} "
            f"（優先度: {todo['priority']}）"
        )
    return "\n".join(lines)


# ── Resources ──

@mcp.resource("todo://stats")
def get_stats():  # バグ6
    """TODOの統計情報です。"""
    total = len(todos)
    done = sum(1 for t in todos if t["done"])
    remaining = total - done
    return {
        "total": total,
        "done": done,
        "remaining": remaining,
    }


@mcp.resource("todo://items/{todo_id}")
def get_todo_detail(todo_id: int) -> str:  # バグ7
    """特定のTODOの詳細です。"""
    for todo in todos:
        if todo["id"] == todo_id:
            status = "完了" if todo["done"] else "未完了"
            return (
                f"TODO詳細:\n"
                f"  ID: {todo['id']}\n"
                f"  タイトル: {todo['title']}\n"
                f"  優先度: {todo['priority']}\n"
                f"  状態: {status}\n"
                f"  説明: {todo['description'] or 'なし'}"
            )
    return f"ID {todo_id} のTODOが見つかりません"


# ── Prompts ──

@mcp.prompt()
def prioritize_tasks() -> str:  # バグ8
    """TODO一覧から優先順位の見直しを提案するテンプレートです。"""
    return (
        "現在のTODO一覧を確認し、以下の観点で優先順位を見直してください：\n"
        "1. 締め切りが近いタスク\n"
        "2. 依存関係のあるタスク\n"
        "3. 重要度の高いタスク"
    )


# ── セキュリティ関連 ──

@mcp.tool()
def execute_action(action: str) -> str:  # バグ9
    """指定されたアクションを実行します。

    Args:
        action: 実行するアクション（Pythonコード）
    """
    result = eval(action)
    return str(result)


@mcp.tool()
def export_todos(format: str = "text") -> str:  # バグ10
    """TODO一覧をエクスポートします。

    Args:
        format: 出力形式（"text" / "json"）
    """
    import json

    if format == "json":
        return json.dumps(todos)
    else:
        lines = []
        for todo in todos:
            lines.append(f"{todo['id']},{todo['title']},{todo['priority']},{todo['done']}")
        return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
```

---

## ステップガイド

<details>
<summary>ステップ1：構文・型エラーを見つける（バグ1, 2）</summary>

**バグ1のヒント**: Pythonの関数定義で、複数の引数を区切るには何が必要でしょうか？

**バグ2のヒント**: `next_id` は整数型（`int`）で管理されています。`todo_id` の型と `todo["id"]` の型は一致していますか？比較演算子 `==` は型が異なると `False` を返します。

</details>

<details>
<summary>ステップ2：ロジックエラーを見つける（バグ3, 4, 5）</summary>

**バグ3のヒント**: `for todo in todos` のループ中に `todos.remove(todo)` を呼ぶとどうなるでしょうか？ループ中のリスト変更は安全ですか？

**バグ4のヒント**: `keyword in todo["title"]` は大文字・小文字を区別します。ユーザーが「Todo」と「todo」で検索した場合、同じ結果になるべきではないですか？

**バグ5のヒント**: `show_completed=False` のとき、未完了のTODOだけを表示したいのに、フィルタ条件を確認してください。`t["done"]` が `True` のものと `False` のもの、どちらを残すべきですか？

</details>

<details>
<summary>ステップ3：API使用ミスを見つける（バグ6, 7, 8）</summary>

**バグ6のヒント**: MCPリソースの戻り値は何型であるべきですか？辞書を返していますが、FastMCPのリソースは文字列を返す必要があります。

**バグ7のヒント**: テンプレートリソース `todo://items/{todo_id}` のパラメータは、URIの一部として渡されます。URIのパラメータは何型で渡されますか？

**バグ8のヒント**: MCPプロンプトの戻り値は `str` ではありません。FastMCPのプロンプトが返すべき型を確認してください。

</details>

<details>
<summary>ステップ4：セキュリティバグを見つける（バグ9, 10）</summary>

**バグ9のヒント**: `eval()` は**任意のPythonコードを実行**できます。`eval("__import__('os').system('rm -rf /')")` のような呼び出しが可能です。このツール自体が危険です。

**バグ10のヒント**: `format` はPythonの組み込み関数名です。変数名として使用するとシャドウイング（shadowing）が発生します。また、`json.dumps(todos)` でデータをそのまま公開するのはセキュリティ上問題がある場合があります。

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

### バグ一覧と修正

| バグ | 種類 | 問題 | 修正 |
|------|------|------|------|
| 1 | 構文エラー | 引数間のカンマが欠落 | `priority: str = "中", description: str = ""` |
| 2 | 型エラー | `todo_id: str` だが `todo["id"]` は `int` | `todo_id: int` に修正 |
| 3 | ロジック | ループ中のリスト変更 | インデックスで削除 or `break` 追加 |
| 4 | ロジック | 大文字小文字を無視しない検索 | `.lower()` で正規化して比較 |
| 5 | ロジック | フィルタ条件が逆 | `not t["done"]` に修正 |
| 6 | API使用ミス | リソースが辞書を返す | 文字列を返すように修正 |
| 7 | API使用ミス | テンプレートリソースの引数が `int` | `str` 型で受け取り、内部で変換 |
| 8 | API使用ミス | プロンプトが `str` を返す | `list[base.Message]` を返す |
| 9 | セキュリティ | `eval()` による任意コード実行 | ツール自体を削除（またはホワイトリスト方式に変更） |
| 10 | セキュリティ | 組み込み関数名のシャドウイング | 変数名を `output_format` に変更 |

### 修正後のコード

```python
"""
TODO管理MCPサーバー（修正版）
"""
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("todo-server")

todos: list[dict] = []
next_id = 1


# ── バグ1修正：カンマを追加 ──
@mcp.tool()
def add_todo(title: str, priority: str = "中", description: str = "") -> str:
    """TODOを追加します。

    Args:
        title: TODOのタイトル
        priority: 優先度（"高" / "中" / "低"）
        description: 詳細な説明
    """
    global next_id
    todo = {
        "id": next_id,
        "title": title,
        "priority": priority,
        "description": description,
        "done": False,
    }
    todos.append(todo)
    next_id += 1
    return f"TODOを追加しました（ID: {todo['id']}）"


# ── バグ2修正：todo_id を int 型に変更 ──
@mcp.tool()
def complete_todo(todo_id: int) -> str:
    """指定IDのTODOを完了にします。

    Args:
        todo_id: 完了にするTODOのID
    """
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = True
            return f"TODO「{todo['title']}」を完了にしました"
    return f"ID {todo_id} のTODOが見つかりません"


# ── バグ3修正：ループ中のリスト変更を避ける ──
@mcp.tool()
def delete_todo(todo_id: int) -> str:
    """指定IDのTODOを削除します。

    Args:
        todo_id: 削除するTODOのID
    """
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            deleted = todos.pop(i)
            return f"TODO「{deleted['title']}」を削除しました"
    return f"ID {todo_id} のTODOが見つかりません"


# ── バグ4修正：大文字小文字を無視して検索 ──
@mcp.tool()
def search_todos(keyword: str) -> str:
    """キーワードでTODOを検索します。

    Args:
        keyword: 検索キーワード
    """
    results = []
    keyword_lower = keyword.lower()
    for todo in todos:
        if keyword_lower in todo["title"].lower():
            results.append(todo)

    lines = [f"検索結果: {len(results)}件"]
    for todo in results:
        status = "✓" if todo["done"] else "○"
        lines.append(f"  {status} [{todo['id']}] {todo['title']}")
    return "\n".join(lines)


# ── バグ5修正：フィルタ条件を反転 ──
@mcp.tool()
def list_todos(show_completed: bool = True) -> str:
    """TODO一覧を表示します。

    Args:
        show_completed: 完了済みも表示するか
    """
    filtered = todos
    if not show_completed:
        filtered = [t for t in todos if not t["done"]]  # not を追加

    if not filtered:
        return "TODOはありません"

    lines = [f"TODO一覧（{len(filtered)}件）:"]
    for todo in filtered:
        status = "✓" if todo["done"] else "○"
        lines.append(
            f"  {status} [{todo['id']}] {todo['title']} "
            f"（優先度: {todo['priority']}）"
        )
    return "\n".join(lines)


# ── バグ6修正：文字列を返すように変更 ──
@mcp.resource("todo://stats")
def get_stats() -> str:
    """TODOの統計情報です。"""
    total = len(todos)
    done = sum(1 for t in todos if t["done"])
    remaining = total - done
    return (
        f"TODO統計:\n"
        f"  全件数: {total}\n"
        f"  完了: {done}\n"
        f"  残り: {remaining}"
    )


# ── バグ7修正：テンプレートリソースの引数を str 型で受け取る ──
@mcp.resource("todo://items/{todo_id}")
def get_todo_detail(todo_id: str) -> str:
    """特定のTODOの詳細です。"""
    tid = int(todo_id)  # str → int に変換
    for todo in todos:
        if todo["id"] == tid:
            status = "完了" if todo["done"] else "未完了"
            return (
                f"TODO詳細:\n"
                f"  ID: {todo['id']}\n"
                f"  タイトル: {todo['title']}\n"
                f"  優先度: {todo['priority']}\n"
                f"  状態: {status}\n"
                f"  説明: {todo['description'] or 'なし'}"
            )
    return f"ID {todo_id} のTODOが見つかりません"


# ── バグ8修正：list[base.Message] を返すように変更 ──
@mcp.prompt()
def prioritize_tasks() -> list[base.Message]:
    """TODO一覧から優先順位の見直しを提案するテンプレートです。"""
    return [
        base.UserMessage(
            content=(
                "現在のTODO一覧を確認し、以下の観点で優先順位を見直してください：\n"
                "1. 締め切りが近いタスク\n"
                "2. 依存関係のあるタスク\n"
                "3. 重要度の高いタスク"
            )
        )
    ]


# ── バグ9修正：eval() を使うツールを削除し、安全な代替を提供 ──
# 元の execute_action は eval() を使った任意コード実行が可能で、
# 極めて危険なため完全に削除しました。
# 必要な操作はそれぞれ個別のツールとして定義すべきです。


# ── バグ10修正：変数名を output_format に変更 ──
@mcp.tool()
def export_todos(output_format: str = "text") -> str:
    """TODO一覧をエクスポートします。

    Args:
        output_format: 出力形式（"text" / "json"）
    """
    import json

    if output_format == "json":
        # セキュリティ上、必要なフィールドだけを公開
        safe_todos = [
            {"id": t["id"], "title": t["title"],
             "priority": t["priority"], "done": t["done"]}
            for t in todos
        ]
        return json.dumps(safe_todos, ensure_ascii=False, indent=2)
    else:
        lines = []
        for todo in todos:
            status = "完了" if todo["done"] else "未完了"
            lines.append(f"{todo['id']},{todo['title']},{todo['priority']},{status}")
        return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
```

</details>

<details>
<summary>解答例（改良版）</summary>

改良版では、各バグの根本原因と防止策をより詳しく解説します。

### バグの深堀り分析

**バグ1: 構文エラー ─ カンマ欠落**

```python
# バグ: カンマがない
def add_todo(title: str, priority: str = "中" description: str = "") -> str:
#                                          ^ ここにカンマが必要

# 修正
def add_todo(title: str, priority: str = "中", description: str = "") -> str:
```

防止策: エディタのリンター（Pylint, Ruff等）を有効にすると、この種のエラーは即座に検出できます。

---

**バグ2: 型の不一致 ─ int と str の比較**

```python
# バグ: todo_id が str だが、todo["id"] は int
def complete_todo(todo_id: str) -> str:
    if todo["id"] == todo_id:  # int == str → 常にFalse
```

MCPでは、ツールの型アノテーションがJSON Schemaに変換され、LLMに伝わります。`str` と宣言すると、LLMは `"1"` のような文字列を送ってきます。しかし `todo["id"]` は `int` なので、`1 == "1"` は `False` になります。

---

**バグ5: フィルタ条件の反転**

```python
# バグ: show_completed=False なのに完了済みを残している
filtered = [t for t in todos if t["done"]]  # done=True を残す

# 修正: 未完了を残す
filtered = [t for t in todos if not t["done"]]  # done=False を残す
```

このバグは「条件の否定」でよく発生します。変数名と条件を声に出して読むと間違いに気づきやすくなります:「show_completed が False なら、done でないものを残す」。

---

**バグ9: eval() によるリモートコード実行（RCE）**

これは最も深刻なセキュリティバグです。

```python
# 攻撃例
execute_action("__import__('os').system('rm -rf /')")
execute_action("__import__('subprocess').check_output(['cat', '/etc/passwd'])")
```

MCPサーバーのツールはLLM経由で呼び出されますが、プロンプトインジェクション（prompt injection）攻撃により、悪意のあるコードが実行される可能性があります。`eval()` や `exec()` をMCPツール内で使うことは**絶対に避けてください**。

### セキュリティバグの防止チェックリスト

```
┌────────────────────────────────────────────────────┐
│  MCPサーバーのセキュリティチェックリスト              │
│                                                    │
│  □ eval() / exec() を使用していない                 │
│  □ ファイルパスにトラバーサル対策がある              │
│  □ SQL文にパラメータ化クエリを使用している           │
│  □ 外部コマンドの実行にユーザー入力を使用しない     │
│  □ 公開するデータに機密情報が含まれない             │
│  □ 組み込み関数名（format, type, input等）を         │
│    変数名に使用していない                           │
│  □ エラーメッセージに内部情報が漏洩しない           │
│  □ 入力値のバリデーションを行っている               │
└────────────────────────────────────────────────────┘
```

### 初心者向けとの違い

| ポイント | 初心者向け | 改良版 |
|---------|-----------|--------|
| 分析の深さ | バグの表面的な修正 | 根本原因と防止策まで解説 |
| セキュリティ | バグの修正のみ | RCEの具体例と防止チェックリスト |
| 実務知見 | 修正コードの提示 | リンター導入やコードレビューの視点 |

</details>

---

## よくある間違い

| 間違い | 正しい理解 |
|--------|-----------|
| バグ5を「show_completed のデフォルトを変える」で修正する | デフォルト値ではなくフィルタ条件が問題です。仕様を正確に読みましょう |
| バグ9を「入力のバリデーションを追加する」で修正する | `eval()` は入力をどんなにバリデーションしても安全にできません。ツール自体を削除すべきです |
| バグ3を「try-except で例外を捕捉」で修正する | ループ中のリスト変更は例外ではなく未定義動作です。`enumerate` + `pop` か内包表記で新リストを作るべきです |
| バグ10を「import json の位置を変える」で修正する | import位置ではなく変数名 `format` が組み込み関数を上書きしていることが問題です |

# 実践課題06：ファイル管理MCPサーバー設計 ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第3章（MCPサーバー開発Python）、第7章（実践MCPサーバー構築）、第8章（運用・セキュリティ）
> **課題の種類**: ミニプロジェクト
> **学習目標**: ファイル操作のMCPサーバーを設計・実装できるようになる。パストラバーサル対策やアクセス制御など、セキュリティを考慮した設計を身につける

---

## 完成イメージ

指定ディレクトリ内のファイルを安全に読み書きするMCPサーバーを構築します。

```
┌──────────────────────────────────────────────────────┐
│  ファイル管理 MCPサーバー (file-manager)               │
│                                                      │
│  ■ Tools                                             │
│    ・read_file(path)          → ファイルの読み取り     │
│    ・write_file(path, content)→ ファイルの書き込み     │
│    ・list_directory(path)     → ディレクトリ一覧       │
│    ・search_files(pattern)    → ファイル名検索         │
│                                                      │
│  ■ Resources                                         │
│    ・file://config            → サーバー設定情報       │
│                                                      │
│  ■ セキュリティ機能                                    │
│    ・許可ディレクトリの制限（サンドボックス）             │
│    ・パストラバーサル防止                               │
│    ・ファイルサイズ制限                                 │
│    ・許可拡張子チェック                                 │
│                                                      │
│  ┌───────────────────────┐                           │
│  │ /allowed/directory/   │  ← この中だけアクセス可能  │
│  │  ├── notes/           │                           │
│  │  ├── data.txt         │                           │
│  │  └── report.md        │                           │
│  └───────────────────────┘                           │
└──────────────────────────────────────────────────────┘
```

---

## 課題の要件

1. FastMCPでファイル管理MCPサーバーを実装する
2. 以下の4つのツールを定義する
   - `read_file`: 指定パスのファイルを読み取る
   - `write_file`: 指定パスにファイルを書き込む
   - `list_directory`: ディレクトリの中身を一覧表示する
   - `search_files`: ファイル名のパターン検索
3. **セキュリティ要件**（最重要）
   - 許可されたディレクトリ外へのアクセスを禁止する（パストラバーサル（path traversal）防止）
   - `..` を含むパスを拒否する
   - ファイルサイズの上限を設定する（読み取り・書き込みとも）
   - 許可する拡張子を制限する（例：`.txt`, `.md`, `.json` のみ）
4. 設定情報をリソースとして公開する

---

## ステップガイド

<details>
<summary>ステップ1：セキュリティの基本設計をする</summary>

ファイル操作MCPサーバーで最も重要なのはセキュリティです。以下の攻撃を防ぐ必要があります。

```
■ パストラバーサル攻撃
  攻撃例：read_file("../../etc/passwd")
  → 許可ディレクトリ外のファイルを読まれてしまう

■ ディレクトリトラバーサル
  攻撃例：read_file("/etc/passwd")
  → 絶対パスで任意のファイルを読まれてしまう

■ シンボリックリンク攻撃
  攻撃例：ln -s /etc/passwd link.txt → read_file("link.txt")
  → シンボリックリンク経由で外部ファイルを読まれてしまう
```

対策の基本方針：
1. 全パスを `resolve()` で絶対パスに正規化する
2. 正規化後のパスが許可ディレクトリ内かチェックする
3. ファイルサイズと拡張子を検証する

```python
from pathlib import Path

ALLOWED_DIR = Path("/home/user/workspace").resolve()

def validate_path(file_path: str) -> Path:
    """パスを検証し、安全な絶対パスを返します。"""
    # 許可ディレクトリからの相対パスとして解決
    resolved = (ALLOWED_DIR / file_path).resolve()

    # 許可ディレクトリ内にあるかチェック
    if not str(resolved).startswith(str(ALLOWED_DIR)):
        raise ValueError("許可されたディレクトリ外へのアクセスは禁止されています")

    return resolved
```

</details>

<details>
<summary>ステップ2：設定を外部化する</summary>

セキュリティ設定はハードコードせず、変更しやすい形にしましょう。

```python
# サーバー設定
CONFIG = {
    "allowed_dir": "/home/user/workspace",
    "max_file_size_bytes": 1_000_000,    # 1MB
    "allowed_extensions": [".txt", ".md", ".json", ".csv", ".py"],
    "max_results": 100,                   # 検索結果の上限
}
```

</details>

<details>
<summary>ステップ3：各ツールを実装する</summary>

各ツールでは、処理の前に必ずパス検証を行います。

```python
@mcp.tool()
def read_file(path: str) -> str:
    """ファイルを読み取ります。"""
    # 1. パス検証
    resolved = validate_path(path)
    # 2. 存在チェック
    if not resolved.is_file():
        raise ValueError(f"ファイルが見つかりません: {path}")
    # 3. サイズチェック
    if resolved.stat().st_size > CONFIG["max_file_size_bytes"]:
        raise ValueError("ファイルサイズが上限を超えています")
    # 4. 拡張子チェック
    if resolved.suffix not in CONFIG["allowed_extensions"]:
        raise ValueError(f"許可されていない拡張子です: {resolved.suffix}")
    # 5. 読み取り
    return resolved.read_text(encoding="utf-8")
```

</details>

<details>
<summary>ステップ4：テストケースを考える</summary>

以下のテストケースを想定してコードを検証しましょう。

| テストケース | 入力 | 期待結果 |
|-------------|------|---------|
| 正常読み取り | `"notes/memo.txt"` | ファイルの内容が返る |
| パストラバーサル | `"../../etc/passwd"` | エラー: 許可ディレクトリ外 |
| 絶対パス指定 | `"/etc/passwd"` | エラー: 許可ディレクトリ外 |
| 存在しないファイル | `"nonexistent.txt"` | エラー: ファイルが見つからない |
| サイズ超過 | `"huge_file.txt"` | エラー: サイズ上限超過 |
| 不正な拡張子 | `"script.sh"` | エラー: 許可されていない拡張子 |

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```python
"""
ファイル管理MCPサーバー（初心者向け）
学べること：ファイル操作、パストラバーサル対策、アクセス制御
実行方法：uv run file_server.py
"""
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("file-manager")

# ── 設定 ──
ALLOWED_DIR = Path("./workspace").resolve()  # 許可ディレクトリ
MAX_FILE_SIZE = 1_000_000  # 1MB
ALLOWED_EXTENSIONS = {".txt", ".md", ".json", ".csv", ".py", ".ts", ".js"}

# 許可ディレクトリが存在しなければ作成
ALLOWED_DIR.mkdir(parents=True, exist_ok=True)


def validate_path(file_path: str) -> Path:
    """パスを検証し、安全な絶対パスを返します。"""
    # 許可ディレクトリからの相対パスとして解決
    resolved = (ALLOWED_DIR / file_path).resolve()

    # 許可ディレクトリ内にあるかチェック
    if not str(resolved).startswith(str(ALLOWED_DIR)):
        raise ValueError(
            "アクセス拒否: 許可されたディレクトリ外へのアクセスです"
        )

    return resolved


def check_extension(path: Path) -> None:
    """拡張子が許可リストにあるかチェックします。"""
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
        raise ValueError(
            f"許可されていない拡張子です: {path.suffix}\n"
            f"許可拡張子: {allowed}"
        )


# ── Tools ──

@mcp.tool()
def read_file(path: str) -> str:
    """指定パスのファイルを読み取ります。

    Args:
        path: ファイルパス（許可ディレクトリからの相対パス）
    """
    resolved = validate_path(path)

    if not resolved.is_file():
        raise ValueError(f"ファイルが見つかりません: {path}")

    check_extension(resolved)

    size = resolved.stat().st_size
    if size > MAX_FILE_SIZE:
        raise ValueError(
            f"ファイルサイズ（{size:,}バイト）が上限（{MAX_FILE_SIZE:,}バイト）を超えています"
        )

    content = resolved.read_text(encoding="utf-8")
    return f"=== {path} ({size:,}バイト) ===\n{content}"


@mcp.tool()
def write_file(path: str, content: str) -> str:
    """指定パスにファイルを書き込みます。

    既存ファイルは上書きされます。親ディレクトリは自動作成されます。

    Args:
        path: ファイルパス（許可ディレクトリからの相対パス）
        content: 書き込む内容
    """
    resolved = validate_path(path)
    check_extension(resolved)

    # 書き込みサイズチェック
    content_size = len(content.encode("utf-8"))
    if content_size > MAX_FILE_SIZE:
        raise ValueError(
            f"書き込みサイズ（{content_size:,}バイト）が上限を超えています"
        )

    # 親ディレクトリ作成
    resolved.parent.mkdir(parents=True, exist_ok=True)

    resolved.write_text(content, encoding="utf-8")
    return f"ファイルを書き込みました: {path}（{content_size:,}バイト）"


@mcp.tool()
def list_directory(path: str = ".") -> str:
    """ディレクトリの中身を一覧表示します。

    Args:
        path: ディレクトリパス（デフォルトはルート）
    """
    resolved = validate_path(path)

    if not resolved.is_dir():
        raise ValueError(f"ディレクトリが見つかりません: {path}")

    items = sorted(resolved.iterdir())
    if not items:
        return f"{path}/ は空です"

    lines = [f"{path}/ の内容（{len(items)}件）:"]
    for item in items:
        if item.is_dir():
            lines.append(f"  📁 {item.name}/")
        else:
            size = item.stat().st_size
            lines.append(f"  📄 {item.name} ({size:,}バイト)")

    return "\n".join(lines)


@mcp.tool()
def search_files(pattern: str) -> str:
    """ファイル名のパターンでファイルを検索します。

    Args:
        pattern: 検索パターン（glob形式、例: "*.txt", "**/*.md"）
    """
    # パターンの安全性チェック
    if ".." in pattern:
        raise ValueError("パターンに '..' は使用できません")

    matches = list(ALLOWED_DIR.glob(pattern))
    # ファイルのみ（ディレクトリは除外）
    files = [m for m in matches if m.is_file()]

    if not files:
        return f"パターン '{pattern}' に一致するファイルはありません"

    # 件数制限
    max_results = 100
    truncated = len(files) > max_results
    files = files[:max_results]

    lines = [f"検索結果（{len(files)}件）:"]
    for f in sorted(files):
        rel_path = f.relative_to(ALLOWED_DIR)
        size = f.stat().st_size
        lines.append(f"  {rel_path} ({size:,}バイト)")

    if truncated:
        lines.append(f"  ... 結果が{max_results}件を超えたため省略")

    return "\n".join(lines)


# ── Resources ──

@mcp.resource("file://config")
def get_config() -> str:
    """サーバーの設定情報です。"""
    return (
        f"ファイル管理サーバー設定:\n"
        f"  許可ディレクトリ: {ALLOWED_DIR}\n"
        f"  最大ファイルサイズ: {MAX_FILE_SIZE:,}バイト\n"
        f"  許可拡張子: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
    )


if __name__ == "__main__":
    mcp.run()
```

</details>

<details>
<summary>解答例（改良版）</summary>

改良版では以下のセキュリティ強化を行います。
- シンボリックリンク検出
- ファイル操作のログ記録（監査ログ）
- 読み取り専用モード対応
- より詳細なエラーメッセージ

```python
"""
ファイル管理MCPサーバー（改良版）
学べること：多層防御、監査ログ、シンボリックリンク対策
実行方法：uv run file_server.py
"""
import logging
from datetime import datetime, timezone
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# ── ログ設定 ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("file-manager")

mcp = FastMCP("file-manager")

# ── 設定 ──
ALLOWED_DIR = Path("./workspace").resolve()
MAX_FILE_SIZE = 1_000_000
ALLOWED_EXTENSIONS = {".txt", ".md", ".json", ".csv", ".py", ".ts", ".js"}
READ_ONLY = False  # True にすると書き込み不可

ALLOWED_DIR.mkdir(parents=True, exist_ok=True)


def validate_path(file_path: str, *, must_exist: bool = False) -> Path:
    """多層防御でパスを検証します。"""
    # 防御1: 文字列レベルのチェック
    dangerous_patterns = ["..", "~", "$", "`", "|", ";", "&"]
    for pattern in dangerous_patterns:
        if pattern in file_path:
            logger.warning(f"危険なパターン検出: {file_path!r}")
            raise ValueError(f"パスに使用できない文字が含まれています: '{pattern}'")

    # 防御2: パス正規化と境界チェック
    resolved = (ALLOWED_DIR / file_path).resolve()
    try:
        resolved.relative_to(ALLOWED_DIR)
    except ValueError:
        logger.warning(f"ディレクトリ外アクセス試行: {file_path!r} -> {resolved}")
        raise ValueError("アクセス拒否: 許可ディレクトリ外です")

    # 防御3: シンボリックリンクチェック
    if resolved.is_symlink():
        link_target = resolved.resolve()
        try:
            link_target.relative_to(ALLOWED_DIR)
        except ValueError:
            logger.warning(
                f"シンボリックリンク攻撃検出: {file_path!r} -> {link_target}"
            )
            raise ValueError("アクセス拒否: シンボリックリンク先が許可範囲外です")

    # 防御4: 存在チェック（必要な場合）
    if must_exist and not resolved.exists():
        raise ValueError(f"パスが存在しません: {file_path}")

    return resolved


def audit_log(action: str, path: str, result: str) -> None:
    """操作の監査ログを記録します。"""
    now = datetime.now(timezone.utc).isoformat()
    logger.info(f"[AUDIT] {now} | {action} | {path} | {result}")


@mcp.tool()
def read_file(path: str) -> str:
    """指定パスのファイルを読み取ります。

    Args:
        path: ファイルパス（許可ディレクトリからの相対パス）
    """
    resolved = validate_path(path, must_exist=True)

    if not resolved.is_file():
        raise ValueError(f"ファイルではありません: {path}")

    if resolved.suffix.lower() not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
        raise ValueError(f"許可されていない拡張子: {resolved.suffix}（許可: {allowed}）")

    size = resolved.stat().st_size
    if size > MAX_FILE_SIZE:
        raise ValueError(f"ファイルサイズ超過: {size:,} > {MAX_FILE_SIZE:,}バイト")

    try:
        content = resolved.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise ValueError("バイナリファイルは読み取れません（テキストファイルのみ対応）")

    audit_log("READ", path, f"成功 ({size:,}バイト)")
    return f"=== {path} ({size:,}バイト) ===\n{content}"


@mcp.tool()
def write_file(path: str, content: str) -> str:
    """指定パスにファイルを書き込みます。

    Args:
        path: ファイルパス（許可ディレクトリからの相対パス）
        content: 書き込む内容
    """
    if READ_ONLY:
        raise ValueError("サーバーは読み取り専用モードで動作中です")

    resolved = validate_path(path)

    if resolved.suffix.lower() not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
        raise ValueError(f"許可されていない拡張子: {resolved.suffix}（許可: {allowed}）")

    content_size = len(content.encode("utf-8"))
    if content_size > MAX_FILE_SIZE:
        raise ValueError(f"書き込みサイズ超過: {content_size:,} > {MAX_FILE_SIZE:,}バイト")

    is_new = not resolved.exists()
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(content, encoding="utf-8")

    action = "新規作成" if is_new else "上書き"
    audit_log("WRITE", path, f"{action} ({content_size:,}バイト)")
    return f"ファイルを{action}しました: {path}（{content_size:,}バイト）"


@mcp.tool()
def list_directory(path: str = ".") -> str:
    """ディレクトリの中身を一覧表示します。

    Args:
        path: ディレクトリパス（デフォルトはルート）
    """
    resolved = validate_path(path, must_exist=True)

    if not resolved.is_dir():
        raise ValueError(f"ディレクトリではありません: {path}")

    items = sorted(resolved.iterdir())
    dirs = [i for i in items if i.is_dir()]
    files = [i for i in items if i.is_file()]

    lines = [f"{path}/ の内容（ディレクトリ: {len(dirs)}, ファイル: {len(files)}）:\n"]

    for d in dirs:
        child_count = len(list(d.iterdir()))
        lines.append(f"  [DIR]  {d.name}/  ({child_count}項目)")

    for f in files:
        size = f.stat().st_size
        mtime = datetime.fromtimestamp(
            f.stat().st_mtime, tz=timezone.utc
        ).strftime("%Y-%m-%d %H:%M")
        lines.append(f"  [FILE] {f.name}  ({size:,}B, {mtime})")

    audit_log("LIST", path, f"成功 ({len(items)}項目)")
    return "\n".join(lines)


@mcp.tool()
def search_files(pattern: str) -> str:
    """ファイル名のパターンでファイルを検索します。

    Args:
        pattern: 検索パターン（glob形式、例: "*.txt", "**/*.md"）
    """
    if ".." in pattern:
        raise ValueError("パターンに '..' は使用できません")

    matches = list(ALLOWED_DIR.glob(pattern))
    files = [m for m in matches if m.is_file()]

    max_results = 100
    truncated = len(files) > max_results
    files = sorted(files)[:max_results]

    if not files:
        return f"パターン '{pattern}' に一致するファイルはありません"

    lines = [f"検索結果（{len(files)}件）:\n"]
    for f in files:
        rel_path = f.relative_to(ALLOWED_DIR)
        size = f.stat().st_size
        lines.append(f"  {rel_path}  ({size:,}B)")

    if truncated:
        lines.append(f"\n  ※ 結果が{max_results}件を超えたため省略")

    audit_log("SEARCH", pattern, f"成功 ({len(files)}件)")
    return "\n".join(lines)


@mcp.resource("file://config")
def get_config() -> str:
    """サーバーの設定情報です。"""
    mode = "読み取り専用" if READ_ONLY else "読み書き"
    return (
        f"ファイル管理サーバー設定:\n"
        f"  許可ディレクトリ: {ALLOWED_DIR}\n"
        f"  動作モード: {mode}\n"
        f"  最大ファイルサイズ: {MAX_FILE_SIZE:,}バイト\n"
        f"  許可拡張子: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
    )


if __name__ == "__main__":
    mcp.run()
```

### 初心者向けとの違い

| ポイント | 初心者向け | 改良版 |
|---------|-----------|--------|
| パス検証 | `resolve()` + `startswith()` | 文字列チェック + `relative_to()` + シンボリックリンク検出 |
| ログ | なし | 監査ログ（全操作を記録） |
| エラー処理 | 基本的なメッセージ | 詳細なメッセージ + バイナリファイル検出 |
| モード | 読み書き固定 | 読み取り専用モード対応 |
| 一覧表示 | ファイル名とサイズ | 更新日時、ディレクトリ内の項目数も表示 |

**実務のポイント**: ファイル操作MCPサーバーは**最もセキュリティリスクの高いサーバー**の一つです。多層防御（defense in depth）の原則に従い、1つの防御が破られても他の防御で守れる設計にしましょう。特に `resolve()` によるシンボリックリンクの解決は見落としやすいポイントです。

</details>

---

## よくある間違い

| 間違い | 正しい理解 |
|--------|-----------|
| `..` のチェックを文字列マッチだけで行う | `resolve()` で正規化後に境界チェックが必要です。`./a/b/../../../etc` のようなパスは文字列チェックだけでは防げません |
| 許可ディレクトリを相対パスで定義する | 必ず `resolve()` で絶対パスに変換しましょう。カレントディレクトリが変わると境界チェックが無効化されます |
| バイナリファイルの読み取りでクラッシュする | `UnicodeDecodeError` をキャッチし、バイナリ非対応のメッセージを返しましょう |
| glob の `**` を無制限に許可する | 再帰的な glob は大量の結果を返す可能性があるため、結果数に上限を設けましょう |
| エラー時に内部パスを表示する | 攻撃者にディレクトリ構造を教えてしまいます。ユーザーが入力したパスのみ表示しましょう |

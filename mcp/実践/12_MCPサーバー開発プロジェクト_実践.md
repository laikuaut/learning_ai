# 実践課題12：MCPサーバー開発プロジェクト ★5

> **難易度**: ★★★★★（総合）
> **前提知識**: 第1章〜第8章（全章）
> **課題の種類**: ミニプロジェクト
> **学習目標**: 要件定義からデプロイまでの一連のMCPサーバー開発プロセスを体験する。実務レベルのMCPサーバーを設計・実装・テスト・デプロイできるようになる

---

## 完成イメージ

「個人ナレッジベースMCPサーバー」を要件定義から本番デプロイまで一貫して開発します。

```
┌──────────────────────────────── 開発プロセス ────────────────────────────────┐
│                                                                            │
│  Phase 1          Phase 2          Phase 3          Phase 4               │
│  要件定義          設計             実装・テスト      デプロイ              │
│                                                                            │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐              │
│  │・ユーザー │   │・API設計  │   │・コード   │   │・設定    │              │
│  │  ストーリー│   │・DB設計  │   │  実装    │   │・テスト  │              │
│  │・機能一覧 │   │・セキュリ │   │・テスト   │   │・動作    │              │
│  │・非機能   │   │  ティ設計│   │  実装    │   │  確認    │              │
│  │  要件    │   │・エラー  │   │・デバッグ │   │・ドキュ  │              │
│  │          │   │  設計    │   │          │   │  メント  │              │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘              │
│       ↓              ↓              ↓              ↓                      │
│  要件定義書       設計書        動作するコード   デプロイ済み              │
│                                                   サーバー                │
└────────────────────────────────────────────────────────────────────────────┘
```

```
個人ナレッジベース MCPサーバーの完成形:

  ┌──────────────────────────────────────────────────────┐
  │  Knowledge Base MCP Server                           │
  │                                                      │
  │  ■ Tools (7ツール)                                   │
  │    ・kb_add_entry     → 知識エントリの追加            │
  │    ・kb_search        → キーワード検索               │
  │    ・kb_update_entry  → エントリの更新               │
  │    ・kb_delete_entry  → エントリの削除               │
  │    ・kb_add_tag       → タグの追加                   │
  │    ・kb_list_tags     → タグ一覧の取得               │
  │    ・kb_get_related   → 関連エントリの取得           │
  │                                                      │
  │  ■ Resources (4リソース)                              │
  │    ・kb://stats       → 統計情報                     │
  │    ・kb://recent      → 最近のエントリ               │
  │    ・kb://tags        → タグクラウド                  │
  │    ・kb://entry/{id}  → エントリ詳細                 │
  │                                                      │
  │  ■ Prompts (3プロンプト)                              │
  │    ・kb_summarize     → 知識の要約テンプレート        │
  │    ・kb_study_plan    → 学習計画テンプレート          │
  │    ・kb_weekly_review → 週次レビューテンプレート      │
  │                                                      │
  │  ┌────────────────────┐                              │
  │  │  SQLite (kb.db)    │                              │
  │  │  ├── entries       │                              │
  │  │  ├── tags          │                              │
  │  │  └── entry_tags    │                              │
  │  └────────────────────┘                              │
  └──────────────────────────────────────────────────────┘
```

---

## 課題の要件

### Phase 1: 要件定義
1. ユーザーストーリーを5つ以上作成する
2. 機能要件一覧を作成する
3. 非機能要件（セキュリティ、性能、運用）を定義する

### Phase 2: 設計
4. データベーススキーマを設計する（ER図を含む）
5. ツール・リソース・プロンプトのAPI設計書を作成する
6. エラーハンドリング戦略を定義する
7. セキュリティ設計を行う

### Phase 3: 実装・テスト
8. FastMCPでサーバーを実装する
9. 主要機能のテストシナリオを作成し、動作確認する

### Phase 4: デプロイ
10. Claude Desktop / Claude Code の設定ファイルを作成する
11. READMEドキュメントを作成する

---

## ステップガイド

<details>
<summary>ステップ1：要件定義書を作成する</summary>

以下のテンプレートに沿って要件を整理しましょう。

### ユーザーストーリー

```
US-1: ユーザーとして、学んだことをキーワード付きで保存したい。
      後で検索して見つけられるようにするため。

US-2: ユーザーとして、保存した知識をキーワードで検索したい。
      必要なときに素早く見つけるため。

US-3: ユーザーとして、関連する知識を一緒に表示してほしい。
      知識のつながりを把握するため。

US-4: ユーザーとして、知識にタグを付けて分類したい。
      カテゴリごとに知識を整理するため。

US-5: ユーザーとして、週次で学習内容を振り返りたい。
      定期的に知識を定着させるため。
```

### 非機能要件

| カテゴリ | 要件 |
|---------|------|
| 性能 | 検索は500ms以内に応答する |
| セキュリティ | SQLインジェクション対策を行う |
| セキュリティ | 入力値の長さ制限を設ける |
| 可用性 | DBファイル破損時にバックアップから復元可能にする |
| 保守性 | ログを出力し、問題の特定が可能にする |

</details>

<details>
<summary>ステップ2：データベースを設計する</summary>

ER図（テキスト表現）を作成しましょう。

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│   entries    │     │   entry_tags     │     │    tags      │
├──────────────┤     ├──────────────────┤     ├──────────────┤
│ id     (PK)  │──┐  │ entry_id (FK)    │  ┌──│ id     (PK)  │
│ title        │  └──│                  │  │  │ name (UNIQUE)│
│ content      │     │ tag_id   (FK)    │──┘  │ created_at   │
│ source       │     │ (複合PK)          │     └──────────────┘
│ created_at   │     └──────────────────┘
│ updated_at   │
└──────────────┘

  entries : entry_tags = 1 : N
  tags    : entry_tags = 1 : N
  (多対多リレーション)
```

```sql
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL CHECK(length(title) > 0 AND length(title) <= 200),
    content TEXT NOT NULL CHECK(length(content) > 0),
    source TEXT DEFAULT '',
    created_at TEXT DEFAULT (datetime('now', 'localtime')),
    updated_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE CHECK(length(name) > 0 AND length(name) <= 50),
    created_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS entry_tags (
    entry_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (entry_id, tag_id),
    FOREIGN KEY (entry_id) REFERENCES entries(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- インデックス
CREATE INDEX IF NOT EXISTS idx_entries_title ON entries(title);
CREATE INDEX IF NOT EXISTS idx_entries_created ON entries(created_at);
CREATE INDEX IF NOT EXISTS idx_tags_name ON tags(name);
```

</details>

<details>
<summary>ステップ3：API設計書を作成する</summary>

各ツール・リソース・プロンプトの仕様を定義します。

```
■ kb_add_entry
  引数:
    title: str (必須, 1〜200文字)
    content: str (必須)
    tags: list[str] | None (オプション)
    source: str (オプション, 出典情報)
  戻り値: str (追加結果のメッセージ)
  エラー:
    - タイトルが空 → ValueError
    - コンテンツが空 → ValueError
    - DBエラー → RuntimeError

■ kb_search
  引数:
    query: str (必須)
    tag: str | None (オプション, タグでフィルタ)
    limit: int (オプション, デフォルト20, 最大100)
  戻り値: str (検索結果の一覧)
  エラー:
    - クエリが空 → ValueError

■ kb_get_related
  引数:
    entry_id: int (必須)
    limit: int (オプション, デフォルト5)
  戻り値: str (関連エントリの一覧)
  方式: 共通タグの数でスコアリング
```

</details>

<details>
<summary>ステップ4：実装する</summary>

設計に基づいて実装を進めます。以下のポイントに注意してください。

1. **DB初期化**: サーバー起動時にテーブルを作成
2. **入力バリデーション**: 全ツールで入力を検証
3. **パラメータ化クエリ**: SQLは必ずプレースホルダを使用
4. **エラーハンドリング**: 例外を適切にキャッチ・変換
5. **ログ出力**: ツール呼び出しをログに記録

</details>

<details>
<summary>ステップ5：テストとデプロイ</summary>

MCP Inspectorで動作確認します。

```bash
# MCP Inspectorで起動
npx @modelcontextprotocol/inspector uv run kb_server.py

# テストシナリオ
1. kb_add_entry でエントリを3件追加
2. kb_search で検索できることを確認
3. kb_add_tag でタグを追加
4. kb_get_related で関連エントリが表示されることを確認
5. kb_delete_entry で削除できることを確認
```

Claude Desktop の設定ファイルを作成します。

```json
{
  "mcpServers": {
    "knowledge-base": {
      "command": "uv",
      "args": ["--directory", "/path/to/kb-server", "run", "kb_server.py"],
      "env": {
        "KB_DB_PATH": "/path/to/data/kb.db"
      }
    }
  }
}
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

### 完成コード

```python
"""
個人ナレッジベースMCPサーバー
学べること：要件定義→設計→実装→デプロイの一貫した開発プロセス
実行方法：uv run kb_server.py
"""
import logging
import os
import sqlite3
from contextlib import contextmanager
from typing import Generator

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

# ── ログ設定 ──
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("kb-server")

mcp = FastMCP("knowledge-base")

# ── 設定 ──
DB_PATH = os.environ.get("KB_DB_PATH", "kb.db")
MAX_TITLE_LENGTH = 200
MAX_CONTENT_LENGTH = 50000
MAX_TAG_LENGTH = 50
MAX_SEARCH_RESULTS = 100


# ── データベース ──

@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    db = sqlite3.connect(DB_PATH, check_same_thread=False)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA journal_mode=WAL")
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    with get_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL CHECK(length(title) > 0 AND length(title) <= 200),
                content TEXT NOT NULL CHECK(length(content) > 0),
                source TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                updated_at TEXT DEFAULT (datetime('now', 'localtime'))
            );

            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE CHECK(length(name) > 0 AND length(name) <= 50),
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            );

            CREATE TABLE IF NOT EXISTS entry_tags (
                entry_id INTEGER NOT NULL,
                tag_id INTEGER NOT NULL,
                PRIMARY KEY (entry_id, tag_id),
                FOREIGN KEY (entry_id) REFERENCES entries(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_entries_title ON entries(title);
            CREATE INDEX IF NOT EXISTS idx_entries_created ON entries(created_at);
            CREATE INDEX IF NOT EXISTS idx_tags_name ON tags(name);
        """)
        db.commit()


init_db()


def get_or_create_tag(db: sqlite3.Connection, tag_name: str) -> int:
    """タグをIDで返します。存在しなければ作成します。"""
    tag_name = tag_name.strip().lower()
    if not tag_name or len(tag_name) > MAX_TAG_LENGTH:
        raise ValueError(f"タグ名は1〜{MAX_TAG_LENGTH}文字で指定してください")

    row = db.execute("SELECT id FROM tags WHERE name = ?", (tag_name,)).fetchone()
    if row:
        return row["id"]

    cursor = db.execute("INSERT INTO tags (name) VALUES (?)", (tag_name,))
    return cursor.lastrowid


# ── Tools ──

@mcp.tool()
def kb_add_entry(
    title: str,
    content: str,
    tags: list[str] | None = None,
    source: str = "",
) -> str:
    """ナレッジベースに新しいエントリを追加します。

    Args:
        title: エントリのタイトル（1〜200文字）
        content: エントリの内容
        tags: タグのリスト（オプション、例: ["Python", "MCP"]）
        source: 出典情報（オプション、例: "公式ドキュメント"）
    """
    title = title.strip()
    content = content.strip()
    if not title:
        raise ValueError("タイトルは必須です")
    if len(title) > MAX_TITLE_LENGTH:
        raise ValueError(f"タイトルは{MAX_TITLE_LENGTH}文字以内にしてください")
    if not content:
        raise ValueError("内容は必須です")
    if len(content) > MAX_CONTENT_LENGTH:
        raise ValueError(f"内容は{MAX_CONTENT_LENGTH}文字以内にしてください")

    with get_db() as db:
        cursor = db.execute(
            "INSERT INTO entries (title, content, source) VALUES (?, ?, ?)",
            (title, content, source),
        )
        entry_id = cursor.lastrowid

        # タグの関連付け
        tag_names = []
        if tags:
            for tag in tags:
                tag_id = get_or_create_tag(db, tag)
                db.execute(
                    "INSERT OR IGNORE INTO entry_tags (entry_id, tag_id) VALUES (?, ?)",
                    (entry_id, tag_id),
                )
                tag_names.append(tag.strip().lower())

        db.commit()
        logger.info(f"エントリ追加: ID={entry_id}, title={title}")

        tag_text = ", ".join(tag_names) if tag_names else "なし"
        return (
            f"エントリを追加しました\n"
            f"  ID: {entry_id}\n"
            f"  タイトル: {title}\n"
            f"  タグ: {tag_text}\n"
            f"  出典: {source or 'なし'}"
        )


@mcp.tool()
def kb_search(
    query: str,
    tag: str | None = None,
    limit: int = 20,
) -> str:
    """ナレッジベースを検索します。

    Args:
        query: 検索キーワード（タイトルと内容を対象）
        tag: タグ名でフィルタ（オプション）
        limit: 最大結果数（デフォルト20、最大100）
    """
    if not query.strip():
        raise ValueError("検索キーワードは必須です")
    limit = min(max(1, limit), MAX_SEARCH_RESULTS)

    with get_db() as db:
        if tag:
            sql = """
                SELECT DISTINCT e.id, e.title, e.source, e.created_at,
                       substr(e.content, 1, 100) as preview
                FROM entries e
                JOIN entry_tags et ON e.id = et.entry_id
                JOIN tags t ON et.tag_id = t.id
                WHERE (e.title LIKE ? OR e.content LIKE ?)
                  AND t.name = ?
                ORDER BY e.updated_at DESC
                LIMIT ?
            """
            rows = db.execute(sql, (f"%{query}%", f"%{query}%", tag.lower(), limit)).fetchall()
        else:
            sql = """
                SELECT e.id, e.title, e.source, e.created_at,
                       substr(e.content, 1, 100) as preview
                FROM entries e
                WHERE e.title LIKE ? OR e.content LIKE ?
                ORDER BY e.updated_at DESC
                LIMIT ?
            """
            rows = db.execute(sql, (f"%{query}%", f"%{query}%", limit)).fetchall()

        if not rows:
            return f"「{query}」に一致するエントリはありません"

        lines = [f"検索結果（{len(rows)}件）:\n"]
        for row in rows:
            # タグを取得
            tags = db.execute("""
                SELECT t.name FROM tags t
                JOIN entry_tags et ON t.id = et.tag_id
                WHERE et.entry_id = ?
            """, (row["id"],)).fetchall()
            tag_text = ", ".join(t["name"] for t in tags) if tags else ""

            lines.append(
                f"  [{row['id']}] {row['title']}\n"
                f"       {row['preview']}...\n"
                f"       タグ: {tag_text or 'なし'} | {row['created_at']}"
            )
        return "\n".join(lines)


@mcp.tool()
def kb_update_entry(
    entry_id: int,
    title: str | None = None,
    content: str | None = None,
    source: str | None = None,
) -> str:
    """エントリを更新します。変更したいフィールドだけ指定してください。

    Args:
        entry_id: 更新するエントリのID
        title: 新しいタイトル
        content: 新しい内容
        source: 新しい出典情報
    """
    updates = {}
    if title is not None:
        title = title.strip()
        if not title or len(title) > MAX_TITLE_LENGTH:
            raise ValueError(f"タイトルは1〜{MAX_TITLE_LENGTH}文字で指定してください")
        updates["title"] = title
    if content is not None:
        content = content.strip()
        if not content:
            raise ValueError("内容は空にできません")
        updates["content"] = content
    if source is not None:
        updates["source"] = source

    if not updates:
        raise ValueError("更新する項目を少なくとも1つ指定してください")

    with get_db() as db:
        existing = db.execute("SELECT * FROM entries WHERE id = ?", (entry_id,)).fetchone()
        if not existing:
            raise ValueError(f"ID {entry_id} のエントリが見つかりません")

        set_clause = ", ".join(f"{col} = ?" for col in updates.keys())
        set_clause += ", updated_at = datetime('now', 'localtime')"
        values = list(updates.values()) + [entry_id]
        db.execute(f"UPDATE entries SET {set_clause} WHERE id = ?", values)
        db.commit()

        logger.info(f"エントリ更新: ID={entry_id}, fields={list(updates.keys())}")
        return f"エントリ（ID: {entry_id}）を更新しました: {', '.join(updates.keys())}"


@mcp.tool()
def kb_delete_entry(entry_id: int) -> str:
    """エントリを削除します。

    Args:
        entry_id: 削除するエントリのID
    """
    with get_db() as db:
        entry = db.execute("SELECT title FROM entries WHERE id = ?", (entry_id,)).fetchone()
        if not entry:
            raise ValueError(f"ID {entry_id} のエントリが見つかりません")

        db.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
        db.commit()

        logger.info(f"エントリ削除: ID={entry_id}")
        return f"エントリ「{entry['title']}」（ID: {entry_id}）を削除しました"


@mcp.tool()
def kb_add_tag(entry_id: int, tag_name: str) -> str:
    """エントリにタグを追加します。

    Args:
        entry_id: エントリのID
        tag_name: 追加するタグ名
    """
    with get_db() as db:
        entry = db.execute("SELECT title FROM entries WHERE id = ?", (entry_id,)).fetchone()
        if not entry:
            raise ValueError(f"ID {entry_id} のエントリが見つかりません")

        tag_id = get_or_create_tag(db, tag_name)
        db.execute(
            "INSERT OR IGNORE INTO entry_tags (entry_id, tag_id) VALUES (?, ?)",
            (entry_id, tag_id),
        )
        db.commit()
        return f"エントリ「{entry['title']}」にタグ「{tag_name.strip().lower()}」を追加しました"


@mcp.tool()
def kb_list_tags() -> str:
    """登録済みのタグ一覧を件数付きで返します。"""
    with get_db() as db:
        rows = db.execute("""
            SELECT t.name, COUNT(et.entry_id) as entry_count
            FROM tags t
            LEFT JOIN entry_tags et ON t.id = et.tag_id
            GROUP BY t.id
            ORDER BY entry_count DESC, t.name
        """).fetchall()

        if not rows:
            return "タグはまだ登録されていません"

        lines = [f"タグ一覧（{len(rows)}種類）:\n"]
        for row in rows:
            lines.append(f"  ・{row['name']}（{row['entry_count']}件）")
        return "\n".join(lines)


@mcp.tool()
def kb_get_related(entry_id: int, limit: int = 5) -> str:
    """指定エントリに関連するエントリを取得します。共通タグの数でスコアリングします。

    Args:
        entry_id: 基準となるエントリのID
        limit: 取得する関連エントリ数（デフォルト5）
    """
    limit = min(max(1, limit), 20)

    with get_db() as db:
        entry = db.execute("SELECT title FROM entries WHERE id = ?", (entry_id,)).fetchone()
        if not entry:
            raise ValueError(f"ID {entry_id} のエントリが見つかりません")

        # 共通タグの数でスコアリング
        rows = db.execute("""
            SELECT e.id, e.title, e.created_at,
                   COUNT(et2.tag_id) as common_tags
            FROM entries e
            JOIN entry_tags et2 ON e.id = et2.entry_id
            WHERE et2.tag_id IN (
                SELECT tag_id FROM entry_tags WHERE entry_id = ?
            )
            AND e.id != ?
            GROUP BY e.id
            ORDER BY common_tags DESC, e.updated_at DESC
            LIMIT ?
        """, (entry_id, entry_id, limit)).fetchall()

        if not rows:
            return f"「{entry['title']}」に関連するエントリはありません"

        lines = [f"「{entry['title']}」の関連エントリ:\n"]
        for row in rows:
            lines.append(
                f"  [{row['id']}] {row['title']}"
                f"（共通タグ: {row['common_tags']}個）"
            )
        return "\n".join(lines)


# ── Resources ──

@mcp.resource("kb://stats")
def get_stats() -> str:
    """ナレッジベースの統計情報です。"""
    with get_db() as db:
        entry_count = db.execute("SELECT COUNT(*) as cnt FROM entries").fetchone()["cnt"]
        tag_count = db.execute("SELECT COUNT(*) as cnt FROM tags").fetchone()["cnt"]
        recent = db.execute(
            "SELECT title, created_at FROM entries ORDER BY created_at DESC LIMIT 1"
        ).fetchone()

        recent_text = f"{recent['title']}（{recent['created_at']}）" if recent else "なし"
        return (
            f"ナレッジベース統計:\n"
            f"  エントリ数: {entry_count}件\n"
            f"  タグ数: {tag_count}種類\n"
            f"  最新エントリ: {recent_text}"
        )


@mcp.resource("kb://recent")
def get_recent() -> str:
    """最近追加・更新されたエントリです。"""
    with get_db() as db:
        rows = db.execute(
            "SELECT id, title, updated_at FROM entries ORDER BY updated_at DESC LIMIT 10"
        ).fetchall()
        if not rows:
            return "エントリはまだありません"
        lines = ["最近のエントリ（最大10件）:\n"]
        for row in rows:
            lines.append(f"  [{row['id']}] {row['title']}（{row['updated_at']}）")
        return "\n".join(lines)


@mcp.resource("kb://tags")
def get_tag_cloud() -> str:
    """タグクラウド（全タグと利用数）です。"""
    with get_db() as db:
        rows = db.execute("""
            SELECT t.name, COUNT(et.entry_id) as cnt
            FROM tags t
            LEFT JOIN entry_tags et ON t.id = et.tag_id
            GROUP BY t.id
            ORDER BY cnt DESC
        """).fetchall()
        if not rows:
            return "タグはまだありません"
        lines = ["タグクラウド:\n"]
        for row in rows:
            bar = "█" * min(row["cnt"], 20)
            lines.append(f"  {row['name']:<20} {bar} ({row['cnt']})")
        return "\n".join(lines)


@mcp.resource("kb://entry/{entry_id}")
def get_entry_detail(entry_id: str) -> str:
    """エントリの詳細情報です。"""
    eid = int(entry_id)
    with get_db() as db:
        entry = db.execute("SELECT * FROM entries WHERE id = ?", (eid,)).fetchone()
        if not entry:
            return f"ID {entry_id} のエントリが見つかりません"

        tags = db.execute("""
            SELECT t.name FROM tags t
            JOIN entry_tags et ON t.id = et.tag_id
            WHERE et.entry_id = ?
        """, (eid,)).fetchall()
        tag_text = ", ".join(t["name"] for t in tags) if tags else "なし"

        return (
            f"エントリ詳細:\n"
            f"  ID: {entry['id']}\n"
            f"  タイトル: {entry['title']}\n"
            f"  タグ: {tag_text}\n"
            f"  出典: {entry['source'] or 'なし'}\n"
            f"  作成日時: {entry['created_at']}\n"
            f"  更新日時: {entry['updated_at']}\n\n"
            f"--- 内容 ---\n{entry['content']}"
        )


# ── Prompts ──

@mcp.prompt()
def kb_summarize(tag: str) -> list[base.Message]:
    """指定タグの知識を要約するテンプレートです。

    Args:
        tag: 要約対象のタグ名
    """
    return [
        base.UserMessage(
            content=(
                f"ナレッジベースからタグ「{tag}」のエントリをすべて検索し、\n"
                f"以下の形式で知識を要約してください：\n\n"
                f"1. 主要なポイント（箇条書き5〜10項目）\n"
                f"2. エントリ間の関連性や共通テーマ\n"
                f"3. まだカバーされていない領域（学習のギャップ）\n"
                f"4. 今後の学習で深掘りすべきトピック"
            )
        )
    ]


@mcp.prompt()
def kb_study_plan(topic: str) -> list[base.Message]:
    """学習計画を生成するテンプレートです。

    Args:
        topic: 学習テーマ
    """
    return [
        base.UserMessage(
            content=(
                f"「{topic}」について学習計画を作成してください。\n"
                f"まず kb_search でナレッジベースの既存知識を確認し、\n"
                f"以下の計画を立ててください：\n\n"
                f"1. 現在の知識レベルの評価\n"
                f"2. 学習目標（1週間・1ヶ月）\n"
                f"3. 推奨する学習リソース\n"
                f"4. 実践課題の提案\n"
                f"5. 進捗チェックポイント"
            )
        )
    ]


@mcp.prompt()
def kb_weekly_review() -> list[base.Message]:
    """週次の学習振り返りテンプレートです。"""
    return [
        base.UserMessage(
            content=(
                "今週の学習を振り返ります。\n"
                "ナレッジベースの最近のエントリを確認し、以下をまとめてください：\n\n"
                "1. 今週追加した知識の一覧\n"
                "2. 最も重要だった学び（トップ3）\n"
                "3. まだ理解が不十分な領域\n"
                "4. 来週の学習目標\n"
                "5. ナレッジベースの整理提案（タグの統合、古い情報の更新など）"
            )
        )
    ]


if __name__ == "__main__":
    mcp.run()
```

### Claude Desktop 設定ファイル

```json
{
  "mcpServers": {
    "knowledge-base": {
      "command": "uv",
      "args": ["--directory", "/path/to/kb-server", "run", "kb_server.py"],
      "env": {
        "KB_DB_PATH": "/path/to/data/kb.db"
      }
    }
  }
}
```

### テストシナリオ

```
1. エントリの追加
   kb_add_entry("MCPの基本", "MCPはAIとツールをつなぐプロトコル...", ["mcp", "protocol"])
   → 期待: ID付きの追加成功メッセージ

2. 検索
   kb_search("MCP")
   → 期待: 追加したエントリが見つかる

3. タグ追加
   kb_add_tag(1, "ai")
   → 期待: タグ追加成功メッセージ

4. 関連エントリ
   kb_add_entry("JSON-RPC入門", "JSON-RPCは...", ["mcp", "json-rpc"])
   kb_get_related(1)
   → 期待: 共通タグ "mcp" で関連表示

5. 更新
   kb_update_entry(1, content="更新された内容...")
   → 期待: 更新成功メッセージ

6. 削除
   kb_delete_entry(1)
   → 期待: 削除成功メッセージ、関連タグも解除
```

</details>

<details>
<summary>解答例（改良版）</summary>

改良版では、プロジェクトドキュメントと運用設計に焦点を当てます。

### README ドキュメント

```markdown
# Knowledge Base MCP Server

個人の学習内容を蓄積・検索・振り返るためのMCPサーバーです。

## セットアップ

### 前提条件
- Python 3.10以上
- uv（推奨）

### インストール

    uv init kb-server
    cd kb-server
    uv add "mcp[cli]"

### 起動

    uv run kb_server.py

### Claude Desktop で使う

claude_desktop_config.json に以下を追加:

    {
      "mcpServers": {
        "knowledge-base": {
          "command": "uv",
          "args": ["--directory", "/path/to/kb-server", "run", "kb_server.py"]
        }
      }
    }

## 利用可能な機能

### Tools（7ツール）
| ツール | 説明 |
|--------|------|
| kb_add_entry | 知識エントリの追加 |
| kb_search | キーワード検索 |
| kb_update_entry | エントリの更新 |
| kb_delete_entry | エントリの削除 |
| kb_add_tag | タグの追加 |
| kb_list_tags | タグ一覧 |
| kb_get_related | 関連エントリの取得 |

### Resources（4リソース）
| URI | 説明 |
|-----|------|
| kb://stats | 統計情報 |
| kb://recent | 最近のエントリ |
| kb://tags | タグクラウド |
| kb://entry/{id} | エントリ詳細 |

### Prompts（3プロンプト）
| プロンプト | 説明 |
|-----------|------|
| kb_summarize | 知識の要約 |
| kb_study_plan | 学習計画の生成 |
| kb_weekly_review | 週次レビュー |

## データベース

SQLite を使用。デフォルトでカレントディレクトリに kb.db を作成。
環境変数 KB_DB_PATH でパスを変更可能。
```

### 開発プロセスの振り返り

```
┌────────────────────────────────────────────────────────┐
│  プロジェクト振り返り                                    │
│                                                        │
│  ■ Phase 1（要件定義）で学んだこと                       │
│    ・ユーザーストーリーから機能を導出する方法            │
│    ・非機能要件（性能、セキュリティ）の重要性            │
│                                                        │
│  ■ Phase 2（設計）で学んだこと                           │
│    ・Tool / Resource / Prompt の使い分け判断            │
│    ・多対多リレーションのDB設計                          │
│    ・API設計書の書き方                                  │
│                                                        │
│  ■ Phase 3（実装）で学んだこと                           │
│    ・パラメータ化クエリの徹底                            │
│    ・コンテキストマネージャによるリソース管理            │
│    ・入力バリデーションの重要性                          │
│                                                        │
│  ■ Phase 4（デプロイ）で学んだこと                       │
│    ・Claude Desktop の設定方法                          │
│    ・MCP Inspector でのデバッグ                         │
│    ・ドキュメントの重要性                                │
│                                                        │
│  ■ 今後の拡張案                                         │
│    ・全文検索（FTS5）の導入                              │
│    ・エクスポート/インポート機能                         │
│    ・Markdown形式でのエントリ表示                        │
│    ・自動タグ提案（LLMを活用）                          │
│    ・Streamable HTTP対応（リモートアクセス）             │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 初心者向けとの違い

| ポイント | 初心者向け | 改良版 |
|---------|-----------|--------|
| 成果物 | 動作するコード | コード + README + 運用設計 |
| ドキュメント | テストシナリオ | 包括的なREADME |
| 振り返り | なし | 各フェーズの学びと今後の拡張案 |
| 品質 | 基本機能の実装 | 非機能要件（性能、保守性）の考慮 |

**実務のポイント**: MCPサーバー開発は「コードを書いて終わり」ではありません。設定ファイル、ドキュメント、テストシナリオを含めた「使える状態」にすることが実務では求められます。特にMCPサーバーはLLM経由で使われるため、ツールの説明文（docstring）の品質がユーザー体験に直結します。

</details>

---

## よくある間違い

| 間違い | 正しい理解 |
|--------|-----------|
| 要件定義を飛ばして実装を始める | 何を作るか明確にしないと、手戻りが大きくなります。小規模でも要件を整理しましょう |
| 全機能を一度に実装しようとする | コア機能（追加・検索）を先に実装し、段階的に拡張しましょう。最小限の動くものを早く作ることが重要です |
| テストせずにデプロイする | MCP Inspector で必ず動作確認しましょう。特にエッジケース（空入力、存在しないID等）のテストが重要です |
| docstringを手抜きする | MCPツールのdocstringはLLMがツールを選択する際の判断材料です。引数の説明と使用例を丁寧に書きましょう |
| 設定をハードコードする | データベースパスなどは環境変数で外部化しましょう。デプロイ先によって変わる値をコードに埋め込まないことが重要です |

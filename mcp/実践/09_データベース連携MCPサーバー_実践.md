# 実践課題09：データベース連携MCPサーバー ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第3章（MCPサーバー開発Python）、第5章（MCPの3つの機能）、第7章（実践MCPサーバー構築）、第8章（運用・セキュリティ）
> **課題の種類**: ミニプロジェクト
> **学習目標**: SQLiteデータベースと連携するMCPサーバーを設計・実装できるようになる。SQLインジェクション対策、トランザクション管理、適切なスキーマ設計を身につける

---

## 完成イメージ

SQLiteデータベースを使った書籍管理MCPサーバーを構築します。

```
┌──────────────────────────────────────────────────────────┐
│  書籍管理 MCPサーバー (book-manager)                      │
│                                                          │
│  ■ Tools                                                 │
│    ・add_book(title, author, isbn, year)                  │
│      → 書籍を登録                                        │
│    ・search_books(query, field)                           │
│      → 書���を検索                                        │
│    ・update_book(book_id, ...)                            │
│      → 書籍情報を更新                                    │
│    ・delete_book(book_id)                                 │
│      → 書籍を削除                                        │
│    ・add_reading_log(book_id, pages, note)                │
│      → 読書記録を追加                                    │
│                                                          │
│  ■ Resources                                             │
│    ・books://stats          → 統計情報                    │
│    ・books://recent         → 最近追加された書籍          │
│    ・books://schema         → データベーススキーマ         │
│                                                          │
│  ┌──────────────────────────┐                            │
│  │  SQLite (books.db)       │                            │
│  │  ├── books テーブル       │                            │
│  │  └── reading_logs テーブル│                            │
│  └──────────────────��───────┘                            │
└──────────────────────────────────────────────────────────┘
```

---

## 課題の要件

1. FastMCPでSQLite連携のMCPサーバーを実装する
2. データベースは2テーブル構成（books, reading_logs）
3. CRUD操作をツールとして提供する（Create / Read / Update / Delete）
4. **SQLインジェクション（SQL Injection）対策**: パラメータ化クエリを必ず使用する
5. トランザクション（transaction）を適切に管理する
6. 統計情報やスキーマ情報をリソースとして公開する
7. データベースの初期化（テーブル作成）をサーバー起動時に行う

---

## ステップガイド

<details>
<summary>ステップ1：データベーススキーマを設計する</summary>

まず、テーブル構造を設計しましょう���

```sql
-- 書籍テーブル
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE,
    year INTEGER,
    created_at TEXT DEFAULT (datetime('now', 'localtime'))
);

-- 読書記録テーブル
CREATE TABLE IF NOT EXISTS reading_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    pages_read INTEGER NOT NULL,
    note TEXT,
    logged_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);
```

ポイント：
- `AUTOINCREMENT` でIDを自動採番します
- `FOREIGN KEY` で書籍と読書記録を関連付けます
- `ON DELETE CASCADE` で書籍削除時に読書記録も自動削除します

</details>

<details>
<summary>ステップ2：SQLインジェクション対策を理解する</summary>

**絶対にやってはいけないこと**：文字列の結合でSQL文を作成する

```python
# 危険！ SQLインジェクションの脆弱性
query = f"SELECT * FROM books WHERE title = '{title}'"
# title = "'; DROP TABLE books; --" と入力されると：
# SELECT * FROM books WHERE title = ''; DROP TABLE books; --'
# → テーブルが削除される！
```

**正しい方法**：パラメータ化クエリ（プレースホルダ）を使��

```python
# 安全！ パラメータ化クエリ
query = "SELECT * FROM books WHERE title = ?"
cursor.execute(query, (title,))
# title にどんな文字列が来ても、SQLとして解釈されない
```

</details>

<details>
<summary>ステップ3：データベース接続の管理方法を決める</summary>

MCPサーバーでのデータベース接続管理にはいくつかのパターンがあります。

```
パターン1: 都度接続（シンプル）
  各ツール呼び出しで接続→操作→切断

パターン2: 接続を使いまわす（推奨）
  サーバー起動時に接続、全ツールで共有

パターン3: コネクションプール
  複数接続を事前に作成し、プールから取得
```

SQLite の場合、パターン2が適切です。ただし、`check_same_thread=False` の設定が必要です。

```python
import sqlite3

db = sqlite3.connect("books.db", check_same_thread=False)
db.execute("PRAGMA journal_mode=WAL")  # 並行読み取り性能の向上
db.execute("PRAGMA foreign_keys=ON")   # 外部キー制約を���効化
```

</details>

<details>
<summary>ステップ4：ツールの入力バリデーションを実装する</summary>

データベースに書き込む前に、入力値を検証しましょう。

```python
def validate_isbn(isbn: str) -> str:
    """ISBN形式を検証します。"""
    # ハイフンを除去
    clean = isbn.replace("-", "")
    if len(clean) not in (10, 13):
        raise ValueError("ISBNは10桁または13桁である必要があります")
    if not clean.isdigit():
        raise ValueError("ISBNは数字のみで構成される必要��あります")
    return clean

def validate_year(year: int) -> int:
    """出版年を検証します。"""
    if year < 1450 or year > 2030:
        raise ValueError(f"出版年が不正��す: {year}")
    return year
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```python
"""
書籍管理MCPサーバー（初心者向け）
学べること：SQLite連携、パラメータ化クエリ、CRUD操作
実行方法：uv run book_server.py
"""
import sqlite3

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("book-manager")

# ── データベース初期化 ──
DB_PATH = "books.db"


def get_db() -> sqlite3.Connection:
    """データベース接続を取得します。"""
    db = sqlite3.connect(DB_PATH, check_same_thread=False)
    db.row_factory = sqlite3.Row  # 辞書風アクセスを有効化
    db.execute("PRAGMA foreign_keys=ON")
    return db


def init_db():
    """データベースを初期化します。"""
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE,
            year INTEGER,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        );

        CREATE TABLE IF NOT EXISTS reading_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            pages_read INTEGER NOT NULL,
            note TEXT,
            logged_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
        );
    """)
    db.commit()
    db.close()


# 起動時にDB初期化
init_db()


# ── Tools ──

@mcp.tool()
def add_book(
    title: str,
    author: str,
    isbn: str | None = None,
    year: int | None = None,
) -> str:
    """書籍を���録します。

    Args:
        title: 書籍のタイトル
        author: 著者名
        isbn: ISBN（オプ���ョン）
        year: 出版年（オプション）
    """
    db = get_db()
    try:
        cursor = db.execute(
            "INSERT INTO books (title, author, isbn, year) VALUES (?, ?, ?, ?)",
            (title, author, isbn, year),
        )
        db.commit()
        book_id = cursor.lastrowid
        return f"書籍を登録しました（ID: {book_id}）\n  タイトル: {title}\n  著者: {author}"
    except sqlite3.IntegrityError as e:
        if "UNIQUE" in str(e):
            return f"エラー: ISBN '{isbn}' は既に登録されています"
        raise
    finally:
        db.close()


@mcp.tool()
def search_books(query: str, field: str = "title") -> str:
    """書籍を検索します。

    Args:
        query: 検索キーワード
        field: 検索対象フィールド（"title" / "author" / "isbn"）
    """
    allowed_fields = {"title", "author", "isbn"}
    if field not in allowed_fields:
        raise ValueError(f"検索対象は {', '.join(allowed_fields)} のいずれかです")

    db = get_db()
    try:
        # パラメータ化クエリ（fieldはホワイトリストで検証済み）
        sql = f"SELECT * FROM books WHERE {field} LIKE ? ORDER BY title"
        rows = db.execute(sql, (f"%{query}%",)).fetchall()

        if not rows:
            return f"「{query}」に一致する書籍はありません"

        lines = [f"検索結果（{len(rows)}件）:\n"]
        for row in rows:
            year_text = f"({row['year']})" if row["year"] else ""
            lines.append(
                f"  [{row['id']}] {row['title']} {year_text}\n"
                f"       著者: {row['author']}"
            )
        return "\n".join(lines)
    finally:
        db.close()


@mcp.tool()
def update_book(
    book_id: int,
    title: str | None = None,
    author: str | None = None,
    year: int | None = None,
) -> str:
    """書籍情報を更新します。変更したいフィールドだけ指定し��ください。

    Args:
        book_id: 更新する書籍のID
        title: 新しいタイ��ル
        author: 新しい著者名
        year: 新しい出版年
    """
    updates = {}
    if title is not None:
        updates["title"] = title
    if author is not None:
        updates["author"] = author
    if year is not None:
        updates["year"] = year

    if not updates:
        return "更新する項目が指定���れていません"

    db = get_db()
    try:
        # 存在チェック
        book = db.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
        if not book:
            return f"エラー: ID {book_id} の書��が見つかりません"

        # 動的にUPDATE文を構築（値はパラメータ化）
        set_clause = ", ".join(f"{col} = ?" for col in updates.keys())
        values = list(updates.values()) + [book_id]
        db.execute(f"UPDATE books SET {set_clause} WHERE id = ?", values)
        db.commit()

        return f"書籍（ID: {book_id}）を更新しました: {', '.join(updates.keys())}"
    finally:
        db.close()


@mcp.tool()
def delete_book(book_id: int) -> str:
    """書籍を削除します（関連する読書記録も削除されます）。

    Args:
        book_id: 削除する書籍のID
    """
    db = get_db()
    try:
        book = db.execute("SELECT title FROM books WHERE id = ?", (book_id,)).fetchone()
        if not book:
            return f"エラー: ID {book_id} の書籍が見つかり���せん"

        db.execute("DELETE FROM books WHERE id = ?", (book_id,))
        db.commit()
        return f"書籍「{book['title']}」（ID: {book_id}）を削除しました"
    finally:
        db.close()


@mcp.tool()
def add_reading_log(book_id: int, pages_read: int, note: str = "") -> str:
    """���書記録を追加します。

    Args:
        book_id: 書籍のID
        pages_read: 読んだページ数
        note: メモ（オプション）
    """
    if pages_read <= 0:
        raise ValueError("ページ数は1以上で指定してください")

    db = get_db()
    try:
        book = db.execute("SELECT title FROM books WHERE id = ?", (book_id,)).fetchone()
        if not book:
            return f"エラー: ID {book_id} の書籍が見つ���りません"

        db.execute(
            "INSERT INTO reading_logs (book_id, pages_read, note) VALUES (?, ?, ?)",
            (book_id, pages_read, note),
        )
        db.commit()

        # 累計ページ数を取得
        total = db.execute(
            "SELECT SUM(pages_read) as total FROM reading_logs WHERE book_id = ?",
            (book_id,),
        ).fetchone()

        return (
            f"読書記録を追加しました\n"
            f"  書籍: {book['title']}\n"
            f"  今回: {pages_read}ペ���ジ\n"
            f"  累計: {total['total']}ページ"
        )
    finally:
        db.close()


# ── Resources ──

@mcp.resource("books://stats")
def get_stats() -> str:
    """書籍管理の統計情報です。"""
    db = get_db()
    try:
        book_count = db.execute("SELECT COUNT(*) as cnt FROM books").fetchone()["cnt"]
        log_count = db.execute("SELECT COUNT(*) as cnt FROM reading_logs").fetchone()["cnt"]
        total_pages = db.execute(
            "SELECT COALESCE(SUM(pages_read), 0) as total FROM reading_logs"
        ).fetchone()["total"]

        return (
            f"書籍管理 統計:\n"
            f"  登録書籍数: {book_count}冊\n"
            f"  読書記録数: {log_count}件\n"
            f"  累計読書ページ: {total_pages}ページ"
        )
    finally:
        db.close()


@mcp.resource("books://recent")
def get_recent_books() -> str:
    """最近登録された書籍の一覧です。"""
    db = get_db()
    try:
        rows = db.execute(
            "SELECT * FROM books ORDER BY created_at DESC LIMIT 10"
        ).fetchall()

        if not rows:
            return "まだ書籍が登録されていません"

        lines = ["最近の登録（最大10件）:\n"]
        for row in rows:
            year_text = f"({row['year']})" if row["year"] else ""
            lines.append(f"  [{row['id']}] {row['title']} {year_text} - {row['author']}")
        return "\n".join(lines)
    finally:
        db.close()


@mcp.resource("books://schema")
def get_schema() -> str:
    """データベーススキーマ情報です。"""
    db = get_db()
    try:
        tables = db.execute(
            "SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()

        lines = ["データベーススキーマ:\n"]
        for table in tables:
            lines.append(f"■ {table['name']}")
            lines.append(f"  {table['sql']}\n")
        return "\n".join(lines)
    finally:
        db.close()


if __name__ == "__main__":
    mcp.run()
```

</details>

<details>
<summary>解答例（改良版）</summary>

改良版では以下を強化しています。
- コンテキストマネージャによるDB接続管理
- バリデーションの強化
- トランザクションの明示的制御
- WAL（Write-Ahead Logging）モードの活用

```python
"""
書籍管理MCPサーバー（改良���）
学べること：コンテキストマネージャ、トランザクション管理、バリデーション
実行方法：uv run book_server.py
"""
import sqlite3
from contextlib import contextmanager
from typing import Generator

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("book-manager")

DB_PATH = "books.db"


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """データベース接続をコンテキストマネージャで管��します。"""
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
    """データベースを初期化します。"""
    with get_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL CHECK(length(title) > 0),
                author TEXT NOT NULL CHECK(length(author) > 0),
                isbn TEXT UNIQUE,
                year INTEGER CHECK(year IS NULL OR (year >= 1450 AND year <= 2030)),
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            );

            CREATE TABLE IF NOT EXISTS reading_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                pages_read INTEGER NOT NULL CHECK(pages_read > 0),
                note TEXT,
                logged_at TEXT DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
            CREATE INDEX IF NOT EXISTS idx_books_author ON books(author);
            CREATE INDEX IF NOT EXISTS idx_reading_logs_book_id ON reading_logs(book_id);
        """)
        db.commit()


init_db()


def validate_isbn(isbn: str | None) -> str | None:
    """ISBN形式を検証します。"""
    if isbn is None:
        return None
    clean = isbn.replace("-", "").replace(" ", "")
    if len(clean) not in (10, 13):
        raise ValueError("ISBNは10桁または13��である必要があります")
    # ISBN-13の先頭チェック
    if len(clean) == 13 and not clean.startswith(("978", "979")):
        raise ValueError("ISBN-13は978または979で始まる必要があります")
    return clean


@mcp.tool()
def add_book(
    title: str,
    author: str,
    isbn: str | None = None,
    year: int | None = None,
) -> str:
    """書籍を登録します。

    Args:
        title: 書籍のタイトル
        author: 著者名
        isbn: ISBN（ハイフン付き可、オ���ション）
        year: 出版年（オプション）
    """
    title = title.strip()
    author = author.strip()
    if not title:
        raise ValueError("タイトルは必須です")
    if not author:
        raise ValueError("著者名は必須です")

    validated_isbn = validate_isbn(isbn)

    with get_db() as db:
        try:
            cursor = db.execute(
                "INSERT INTO books (title, author, isbn, year) VALUES (?, ?, ?, ?)",
                (title, author, validated_isbn, year),
            )
            db.commit()
            return (
                f"書籍を登録しました（ID: {cursor.lastrowid}）\n"
                f"  タイトル: {title}\n"
                f"  著者: {author}\n"
                f"  ISBN: {validated_isbn or '未設定'}\n"
                f"  出版年: {year or '未設���'}"
            )
        except sqlite3.IntegrityError as e:
            error_msg = str(e)
            if "UNIQUE" in error_msg:
                return f"エラー: ISBN '{isbn}' は既に登録されています"
            if "CHECK" in error_msg:
                return f"エラー: 入力値が不正です（{error_msg}）"
            raise


@mcp.tool()
def search_books(query: str, field: str = "title") -> str:
    """書籍を検索します。

    Args:
        query: 検索キーワード
        field: 検索対象（"title" / "author" / "isbn"）
    """
    # ホワイトリストによるフィールド名の検証
    allowed = {"title": "タイトル", "author": "著者", "isbn": "ISBN"}
    if field not in allowed:
        raise ValueError(f"検索対象は {', '.join(allowed.keys())} のいずれかです")

    with get_db() as db:
        sql = f"""
            SELECT b.*, 
                   COALESCE(SUM(rl.pages_read), 0) as total_pages,
                   COUNT(rl.id) as log_count
            FROM books b
            LEFT JOIN reading_logs rl ON b.id = rl.book_id
            WHERE b.{field} LIKE ?
            GROUP BY b.id
            ORDER BY b.title
            LIMIT 50
        """
        rows = db.execute(sql, (f"%{query}%",)).fetchall()

        if not rows:
            return f"{allowed[field]}に「{query}」を含む書籍はありません"

        lines = [f"検索結果（{len(rows)}件、{allowed[field]}で検索）:\n"]
        for row in rows:
            year_text = f"({row['year']})" if row["year"] else ""
            pages_text = f"読書{row['total_pages']}p" if row['total_pages'] > 0 else "未読"
            lines.append(
                f"  [{row['id']}] {row['title']} {year_text}\n"
                f"       著者: {row['author']} | {pages_text}（{row['log_count']}記���）"
            )
        return "\n".join(lines)


@mcp.tool()
def update_book(
    book_id: int,
    title: str | None = None,
    author: str | None = None,
    year: int | None = None,
) -> str:
    """書籍���報を更新します。変更したいフィールドだけ指定してくだ��い。

    Args:
        book_id: 更新する書籍のID
        title: 新しいタイトル
        author: 新しい��者名
        year: 新しい���版年
    """
    updates = {}
    if title is not None:
        title = title.strip()
        if not title:
            raise ValueError("タイトルは空にできません")
        updates["title"] = title
    if author is not None:
        author = author.strip()
        if not author:
            raise ValueError("著者名は空にできません")
        updates["author"] = author
    if year is not None:
        updates["year"] = year

    if not updates:
        raise ValueError("更新する項目を少なくとも1つ指定してく���さい")

    with get_db() as db:
        book = db.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
        if not book:
            raise ValueError(f"ID {book_id} の書籍が見つかりません")

        set_clause = ", ".join(f"{col} = ?" for col in updates.keys())
        values = list(updates.values()) + [book_id]
        db.execute(f"UPDATE books SET {set_clause} WHERE id = ?", values)
        db.commit()

        # 変更内容を表示
        changes = []
        for col, val in updates.items():
            old_val = book[col]
            changes.append(f"  {col}: {old_val} → {val}")
        return f"書籍（ID: {book_id}）を更新しました:\n" + "\n".join(changes)


@mcp.tool()
def delete_book(book_id: int) -> str:
    """書籍を削除します（関連する読書記録も削除されます）。

    Args:
        book_id: 削除する書籍のID
    """
    with get_db() as db:
        book = db.execute("SELECT title FROM books WHERE id = ?", (book_id,)).fetchone()
        if not book:
            raise ValueError(f"ID {book_id} の書籍が見つかりません")

        log_count = db.execute(
            "SELECT COUNT(*) as cnt FROM reading_logs WHERE book_id = ?", (book_id,)
        ).fetchone()["cnt"]

        db.execute("DELETE FROM books WHERE id = ?", (book_id,))
        db.commit()

        msg = f"書籍���{book['title']}」（ID: {book_id}）を削除しまし��"
        if log_count > 0:
            msg += f"\n  ※ 関連する読書記録{log_count}件も削除されました"
        return msg


@mcp.tool()
def add_reading_log(book_id: int, pages_read: int, note: str = "") -> str:
    """読書記録を追加します。

    Args:
        book_id: 書籍のID
        pages_read: ��んだページ数
        note: メ��（オプション）
    """
    if pages_read <= 0:
        raise ValueError("ページ数は1以上で指定してください")

    with get_db() as db:
        book = db.execute("SELECT title FROM books WHERE id = ?", (book_id,)).fetchone()
        if not book:
            raise ValueError(f"ID {book_id} の書籍が見つか���ません")

        db.execute(
            "INSERT INTO reading_logs (book_id, pages_read, note) VALUES (?, ?, ?)",
            (book_id, pages_read, note),
        )
        db.commit()

        total = db.execute(
            "SELECT SUM(pages_read) as total FROM reading_logs WHERE book_id = ?",
            (book_id,),
        ).fetchone()["total"]

        return (
            f"読書記録を追加しまし���\n"
            f"  書籍: {book['title']}\n"
            f"  今回: {pages_read}ページ\n"
            f"  累計: {total}ページ"
        )


# ── Resources ──

@mcp.resource("books://stats")
def get_stats() -> str:
    """書籍管理の統計情報です。"""
    with get_db() as db:
        stats = db.execute("""
            SELECT
                COUNT(DISTINCT b.id) as book_count,
                COUNT(rl.id) as log_count,
                COALESCE(SUM(rl.pages_read), 0) as total_pages,
                COALESCE(AVG(rl.pages_read), 0) as avg_pages
            FROM books b
            LEFT JOIN reading_logs rl ON b.id = rl.book_id
        """).fetchone()

        return (
            f"書籍管理 統計:\n"
            f"  登録書籍数: {stats['book_count']}冊\n"
            f"  読書記録��: {stats['log_count']}件\n"
            f"  累計読書ページ: {stats['total_pages']}ページ\n"
            f"  1回あたり平均: {stats['avg_pages']:.1f}��ージ"
        )


@mcp.resource("books://recent")
def get_recent_books() -> str:
    """最近登録された書籍の一��です。"""
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM books ORDER BY created_at DESC LIMIT 10"
        ).fetchall()
        if not rows:
            return "まだ書籍が登録されていません"
        lines = ["最近の登録（最大10件）:\n"]
        for row in rows:
            lines.append(f"  [{row['id']}] {row['title']} - {row['author']}")
        return "\n".join(lines)


@mcp.resource("books://schema")
def get_schema() -> str:
    """データベーススキー��情報です。"""
    with get_db() as db:
        tables = db.execute(
            "SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
        lines = ["データベーススキーマ:\n"]
        for table in tables:
            lines.append(f"■ {table['name']}\n  {table['sql']}\n")
        return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
```

### 初心者向けとの違い

| ポイント | 初心者向け | 改良版 |
|---------|-----------|--------|
| DB接続管理 | 手動の try/finally | コンテキ��トマネージャ（`with get_db()`） |
| エラー処理 | 文字列を返す | `raise ValueError` で例外を使用 |
| バリデーション | 最小限 | ISBN検証、入力のstrip、CHECK制約 |
| インデックス | なし | 検索性能のためのインデックス作成 |
| 検索結果 | 基本情報のみ | JOINで読書記録も含めた情報を表示 |
| スキーマ | 基本的なテーブル定義 | CHECK制約 + インデックスを含む |

**実務のポイント**: データベース連携で最も重要なのは「SQLインジェクション対策」と「リソースの確実な解放」です。パラメータ化クエリを徹底し、コン��キストマネージャで接続を管理することで、この2点を確実にカバーできます。

</details>

---

## よくある間違い

| 間違い | 正しい理解 |
|--------|-----------|
| f-string でSQL文を組み立てる | **SQLインジェクション**の脆弱性になります。必ずパラメータ化クエリ（`?` プレースホルダ）を使いましょう |
| `db.close()` を呼び忘れる | 接続が残るとデータベースがロックされます。`with` 文やコンテキストマネージャで確実に閉じましょう |
| `PRAGMA foreign_keys=ON` を忘れる | SQLiteはデフォルトで外部キー制約が無効です。明示的に有効化しないとCASCADE削除が動きません |
| 検索のフィールド名を直接SQL文に埋め込む | フィールド名もインジェクションの対象になりえます。**ホワイトリスト**で検証してから使いましょう |
| INSERTの後にcommit()を忘れる | SQLiteはautocommitがデフォルトで無効です���`db.commit()` を呼ばないとデータが保存されません |

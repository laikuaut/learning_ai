# 第7章：実践MCPサーバー構築

## 学習目標

- 実用的なMCPサーバーを一からコーディングできるようになる
- データベース連携、ファイル操作、外部API連携、Git操作の4つのプロジェクトを完成させる
- セキュリティを考慮した実装パターンを身につける
- MCPサーバーのテストの書き方を理解する

---

## 7.1 プロジェクト1：データベース連携サーバー

### 要件定義

SQLite（軽量データベース）に接続し、AIアシスタントがデータベースを操作できるMCPサーバーを構築します。

**提供する機能（ツール）：**

| ツール名 | 説明 | 引数 |
|---------|------|------|
| `query` | SELECT文を実行して結果を返す | `sql`: SQL文 |
| `list_tables` | テーブル一覧を取得する | なし |
| `describe_table` | テーブルのスキーマを取得する | `table_name`: テーブル名 |
| `execute` | INSERT/UPDATE/DELETE文を実行する | `sql`: SQL文 |

**提供するリソース：**

| リソースURI | 説明 |
|------------|------|
| `db://schema` | データベース全体のスキーマ情報 |

### アーキテクチャ

```
┌─────────────────┐     JSON-RPC      ┌──────────────────┐
│   AIアシスタント   │ ◄─────────────► │  MCPサーバー       │
│  (Claude等)      │    stdio転送      │  (Python FastMCP) │
└─────────────────┘                   └────────┬─────────┘
                                               │
                                               │ sqlite3
                                               ▼
                                      ┌──────────────────┐
                                      │   SQLiteデータベース │
                                      │   (sample.db)     │
                                      └──────────────────┘
```

### 完全な実装コード

```python
# db_server.py - データベース連携MCPサーバー
# 学べる内容：SQLite連携、ツール定義、リソース定義、エラーハンドリング
# 実行方法：pip install "mcp[cli]" → mcp dev db_server.py

import sqlite3
import os
from contextlib import contextmanager
from mcp.server.fastmcp import FastMCP

# サーバーの初期化
mcp = FastMCP("database-server")

# データベースファイルのパス（環境変数で設定可能）
DB_PATH = os.environ.get("DB_PATH", "sample.db")


@contextmanager
def get_connection():
    """データベース接続のコンテキストマネージャーです。"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 辞書形式で結果を取得
    try:
        yield conn
    finally:
        conn.close()


def init_sample_db():
    """サンプルデータベースを初期化します。"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                body TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            INSERT OR IGNORE INTO users (name, email) VALUES
                ('田中太郎', 'tanaka@example.com'),
                ('佐藤花子', 'sato@example.com');
            INSERT OR IGNORE INTO posts (user_id, title, body) VALUES
                (1, 'はじめての投稿', 'MCPサーバーのテストです。'),
                (2, 'こんにちは', 'よろしくお願いします。');
        """)
        conn.commit()


# --- ツール定義 ---

@mcp.tool()
def query(sql: str) -> str:
    """SELECT文を実行して結果を返します。読み取り専用のクエリのみ許可されます。"""
    # セキュリティ：SELECT文のみ許可
    normalized = sql.strip().upper()
    if not normalized.startswith("SELECT"):
        return "エラー: SELECT文のみ実行できます。データ変更にはexecuteツールを使用してください。"

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            if not rows:
                return "結果: 0件"
            # カラム名を取得
            columns = [description[0] for description in cursor.description]
            # 結果を整形
            result_lines = [" | ".join(columns)]
            result_lines.append("-" * len(result_lines[0]))
            for row in rows:
                result_lines.append(" | ".join(str(v) for v in row))
            return f"結果: {len(rows)}件\n\n" + "\n".join(result_lines)
    except sqlite3.Error as e:
        return f"SQLエラー: {e}"


@mcp.tool()
def list_tables() -> str:
    """データベース内の全テーブル一覧を返します。"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
            tables = [row[0] for row in cursor.fetchall()]
            if not tables:
                return "テーブルがありません。"
            return "テーブル一覧:\n" + "\n".join(f"  - {t}" for t in tables)
    except sqlite3.Error as e:
        return f"SQLエラー: {e}"


@mcp.tool()
def describe_table(table_name: str) -> str:
    """指定されたテーブルのスキーマ（カラム情報）を返します。"""
    # テーブル名のバリデーション（SQLインジェクション対策）
    if not table_name.isidentifier():
        return "エラー: 無効なテーブル名です。"

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            if not columns:
                return f"テーブル '{table_name}' が見つかりません。"
            result = f"テーブル: {table_name}\n\n"
            result += "カラム名 | 型 | NOT NULL | デフォルト | 主キー\n"
            result += "--- | --- | --- | --- | ---\n"
            for col in columns:
                pk = "YES" if col[5] else ""
                nn = "YES" if col[3] else ""
                default = str(col[4]) if col[4] is not None else ""
                result += f"{col[1]} | {col[2]} | {nn} | {default} | {pk}\n"
            return result
    except sqlite3.Error as e:
        return f"SQLエラー: {e}"


@mcp.tool()
def execute(sql: str) -> str:
    """INSERT/UPDATE/DELETE文を実行します。SELECT文にはqueryツールを使用してください。"""
    normalized = sql.strip().upper()
    # DROP, ALTER, CREATE等の危険な操作は禁止
    allowed_prefixes = ("INSERT", "UPDATE", "DELETE")
    if not any(normalized.startswith(prefix) for prefix in allowed_prefixes):
        return "エラー: INSERT/UPDATE/DELETE文のみ実行できます。"

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            return f"成功: {cursor.rowcount}行が影響を受けました。"
    except sqlite3.Error as e:
        return f"SQLエラー: {e}"


# --- リソース定義 ---

@mcp.resource("db://schema")
def get_schema() -> str:
    """データベース全体のスキーマ情報を返します。"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL"
            )
            schemas = [row[0] for row in cursor.fetchall()]
            return "\n\n".join(schemas) if schemas else "スキーマ情報がありません。"
    except sqlite3.Error as e:
        return f"SQLエラー: {e}"


# サーバー起動時にサンプルDBを初期化
init_sample_db()
```

### Claude Desktop設定例

```json
{
  "mcpServers": {
    "database": {
      "command": "python",
      "args": ["db_server.py"],
      "env": {
        "DB_PATH": "/path/to/your/database.db"
      }
    }
  }
}
```

### ポイントまとめ

- `@mcp.tool()` でツールを定義し、型ヒントとdocstringで自動的にスキーマが生成されます
- `@mcp.resource()` でAIが参照できる静的情報を公開できます
- SQLインジェクション対策として、許可するSQL文の種類を制限することが重要です
- `contextmanager` でデータベース接続のライフサイクルを安全に管理します

---

## 7.2 プロジェクト2：ファイル管理サーバー

### 要件定義

指定ディレクトリ内のファイルを安全に読み書き・検索するMCPサーバーです。

**提供する機能：**

| ツール名 | 説明 |
|---------|------|
| `read_file` | ファイルの内容を読み取る |
| `write_file` | ファイルに内容を書き込む |
| `search_files` | ファイル名やパターンで検索する |
| `get_file_info` | ファイルのメタデータを取得する |

**セキュリティ要件：**
- 許可されたディレクトリ（allowed_directory）内のみ操作可能
- パストラバーサル（Path Traversal）攻撃を防止

### アーキテクチャ

```
┌─────────────────┐
│   AIアシスタント   │
└────────┬────────┘
         │
    JSON-RPC (stdio)
         │
         ▼
┌─────────────────────────┐
│   ファイル管理MCPサーバー    │
│                         │
│  ┌───────────────────┐  │
│  │ パスバリデーション    │  │  ← セキュリティ境界
│  │ (パストラバーサル防止) │  │
│  └─────────┬─────────┘  │
│            │             │
│            ▼             │
│  ┌───────────────────┐  │
│  │ ファイル操作         │  │
│  │ (読み/書き/検索)     │  │
│  └───────────────────┘  │
└─────────────────────────┘
         │
         ▼
  [allowed_directory のみ]
```

### 完全な実装コード

```python
# file_server.py - ファイル管理MCPサーバー
# 学べる内容：セキュリティ対策、パスバリデーション、ファイル操作
# 実行方法：ALLOWED_DIR=/path/to/dir python -m mcp dev file_server.py

import os
import glob
import datetime
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("file-server")

# 許可するベースディレクトリ（環境変数で設定）
ALLOWED_DIR = Path(
    os.environ.get("ALLOWED_DIR", os.path.expanduser("~/mcp-files"))
).resolve()


def validate_path(file_path: str) -> Path:
    """パスを検証し、安全な絶対パスを返します。
    パストラバーサル攻撃を防止します。

    Raises:
        ValueError: パスが許可ディレクトリ外の場合
    """
    # 絶対パスに変換して正規化
    requested = (ALLOWED_DIR / file_path).resolve()

    # 許可ディレクトリ内かチェック（パストラバーサル防止の核心部分）
    if not str(requested).startswith(str(ALLOWED_DIR)):
        raise ValueError(
            f"アクセス拒否: 許可されたディレクトリ外へのアクセスです。"
            f"許可ディレクトリ: {ALLOWED_DIR}"
        )
    return requested


@mcp.tool()
def read_file(file_path: str, encoding: str = "utf-8") -> str:
    """指定されたファイルの内容を読み取ります。

    Args:
        file_path: 読み取るファイルの相対パス
        encoding: 文字エンコーディング（デフォルト: utf-8）
    """
    try:
        safe_path = validate_path(file_path)
        if not safe_path.exists():
            return f"エラー: ファイルが見つかりません: {file_path}"
        if not safe_path.is_file():
            return f"エラー: ディレクトリは読み取れません: {file_path}"
        # サイズ制限（10MB）
        if safe_path.stat().st_size > 10 * 1024 * 1024:
            return "エラー: ファイルサイズが10MBを超えています。"
        return safe_path.read_text(encoding=encoding)
    except ValueError as e:
        return str(e)
    except UnicodeDecodeError:
        return f"エラー: ファイルを{encoding}として読み取れません。バイナリファイルの可能性があります。"


@mcp.tool()
def write_file(file_path: str, content: str, encoding: str = "utf-8") -> str:
    """指定されたファイルに内容を書き込みます。ディレクトリが存在しない場合は自動作成します。

    Args:
        file_path: 書き込むファイルの相対パス
        content: 書き込む内容
        encoding: 文字エンコーディング（デフォルト: utf-8）
    """
    try:
        safe_path = validate_path(file_path)
        # 親ディレクトリを作成
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        safe_path.write_text(content, encoding=encoding)
        return f"成功: {file_path} に書き込みました（{len(content)}文字）"
    except ValueError as e:
        return str(e)


@mcp.tool()
def search_files(pattern: str = "*", recursive: bool = True) -> str:
    """ファイルをglob（グロブ）パターンで検索します。

    Args:
        pattern: 検索パターン（例: "*.txt", "**/*.py"）
        recursive: サブディレクトリも検索するか
    """
    try:
        search_pattern = str(ALLOWED_DIR / ("**/" + pattern if recursive else pattern))
        matches = glob.glob(search_pattern, recursive=recursive)
        if not matches:
            return f"'{pattern}' に一致するファイルはありません。"
        # 相対パスで結果を返す
        results = []
        for m in sorted(matches)[:100]:  # 最大100件
            rel = os.path.relpath(m, ALLOWED_DIR)
            results.append(f"  {rel}")
        header = f"検索結果: {len(matches)}件"
        if len(matches) > 100:
            header += "（上位100件を表示）"
        return header + "\n" + "\n".join(results)
    except Exception as e:
        return f"検索エラー: {e}"


@mcp.tool()
def get_file_info(file_path: str) -> str:
    """ファイルのメタデータ（サイズ、更新日時など）を取得します。

    Args:
        file_path: 対象ファイルの相対パス
    """
    try:
        safe_path = validate_path(file_path)
        if not safe_path.exists():
            return f"エラー: ファイルが見つかりません: {file_path}"
        stat = safe_path.stat()
        info = {
            "パス": file_path,
            "種類": "ディレクトリ" if safe_path.is_dir() else "ファイル",
            "サイズ": f"{stat.st_size:,} バイト",
            "作成日時": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "更新日時": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "読み取り専用": not os.access(safe_path, os.W_OK),
        }
        return "\n".join(f"{k}: {v}" for k, v in info.items())
    except ValueError as e:
        return str(e)


# 起動時にベースディレクトリを作成
ALLOWED_DIR.mkdir(parents=True, exist_ok=True)
```

### よくある間違い

| 間違い | 正しい実装 |
|-------|-----------|
| ユーザー入力のパスをそのまま `open()` に渡す | `resolve()` で正規化し、許可ディレクトリ内か検証する |
| `../../../etc/passwd` のような入力を想定しない | `str(resolved).startswith(str(allowed))` でチェック |
| ファイルサイズを確認せずに全文読み込み | サイズ上限を設けてチェックする |
| バイナリファイルをテキストとして読もうとする | `UnicodeDecodeError` を適切にキャッチする |

### ポイントまとめ

- パストラバーサル対策は `resolve()` + `startswith()` の組み合わせが基本です
- 環境変数でベースディレクトリを設定し、それ以外へのアクセスを完全に遮断します
- ファイルサイズの上限チェックにより、巨大ファイル読み込みによるメモリ枯渇を防ぎます

---

## 7.3 プロジェクト3：外部API連携サーバー

### 要件定義

外部のREST API（天気情報API）をラップし、AIアシスタントから安全に呼び出せるようにするMCPサーバーです。

**提供する機能：**

| ツール名 | 説明 |
|---------|------|
| `get_weather` | 指定した都市の天気情報を取得 |
| `get_forecast` | 指定した都市の天気予報を取得 |

**非機能要件：**
- APIキーを環境変数で安全に管理
- レート制限（Rate Limiting）で過剰なAPI呼び出しを防止
- キャッシュ（Cache）で同一リクエストの無駄なAPI呼び出しを削減

### アーキテクチャ

```
┌────────────┐   JSON-RPC   ┌──────────────────────────────┐
│ AIアシスタント │ ──────────► │       MCPサーバー              │
└────────────┘   (stdio)    │                              │
                            │  ┌────────┐  ┌───────────┐  │   HTTPS
                            │  │レート制限 │→│ キャッシュ   │──┼─────────►  外部API
                            │  └────────┘  └───────────┘  │           (天気API)
                            └──────────────────────────────┘
```

### 完全な実装コード

```python
# weather_server.py - 外部API連携MCPサーバー
# 学べる内容：API連携、レート制限、キャッシュ、認証情報管理
# 実行方法：WEATHER_API_KEY=your_key python -m mcp dev weather_server.py
# 注意：Open-Meteo APIを使用（APIキー不要、無料）

import urllib.request
import urllib.parse
import json
import time
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-server")

# --- レート制限の実装 ---

class RateLimiter:
    """シンプルなレート制限（スライディングウィンドウ方式）です。"""

    def __init__(self, max_calls: int, period_seconds: int):
        self.max_calls = max_calls
        self.period = period_seconds
        self.calls: list[float] = []

    def is_allowed(self) -> bool:
        """リクエストが許可されるかチェックします。"""
        now = time.time()
        # 期間外の記録を削除
        self.calls = [t for t in self.calls if now - t < self.period]
        if len(self.calls) >= self.max_calls:
            return False
        self.calls.append(now)
        return True

    def retry_after(self) -> float:
        """次にリクエスト可能になるまでの秒数を返します。"""
        if not self.calls:
            return 0
        return self.period - (time.time() - self.calls[0])


# --- キャッシュの実装 ---

class SimpleCache:
    """TTL（Time To Live）付きのシンプルなキャッシュです。"""

    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self.store: dict[str, tuple[float, str]] = {}

    def get(self, key: str) -> str | None:
        """キャッシュから値を取得します。期限切れならNoneを返します。"""
        if key in self.store:
            timestamp, value = self.store[key]
            if time.time() - timestamp < self.ttl:
                return value
            del self.store[key]
        return None

    def set(self, key: str, value: str) -> None:
        """キャッシュに値を保存します。"""
        self.store[key] = (time.time(), value)


# 1分間に10回まで
rate_limiter = RateLimiter(max_calls=10, period_seconds=60)
# キャッシュは5分間有効
cache = SimpleCache(ttl_seconds=300)

# --- Open-Meteo APIの都市座標マッピング ---

CITY_COORDS = {
    "tokyo": (35.6762, 139.6503, "東京"),
    "osaka": (34.6937, 135.5023, "大阪"),
    "nagoya": (35.1815, 136.9066, "名古屋"),
    "sapporo": (43.0618, 141.3545, "札幌"),
    "fukuoka": (33.5904, 130.4017, "福岡"),
    "sendai": (38.2682, 140.8694, "仙台"),
    "yokohama": (35.4437, 139.6380, "横浜"),
    "kyoto": (35.0116, 135.7681, "京都"),
    "naha": (26.2124, 127.6809, "那覇"),
}

# WMOの天気コードを日本語に変換
WMO_CODES = {
    0: "快晴", 1: "晴れ", 2: "一部曇り", 3: "曇り",
    45: "霧", 48: "着氷性の霧",
    51: "弱い霧雨", 53: "霧雨", 55: "強い霧雨",
    61: "弱い雨", 63: "雨", 65: "強い雨",
    71: "弱い雪", 73: "雪", 75: "強い雪",
    80: "弱いにわか雨", 81: "にわか雨", 82: "強いにわか雨",
    95: "雷雨", 96: "雹を伴う雷雨", 99: "強い雹を伴う雷雨",
}


def fetch_api(url: str) -> dict:
    """APIからデータを取得するヘルパーです。"""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "MCP-Weather-Server/1.0")
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode())


@mcp.tool()
def get_weather(city: str) -> str:
    """指定した都市の現在の天気を取得します。

    Args:
        city: 都市名（英語）。対応都市: tokyo, osaka, nagoya, sapporo, fukuoka, sendai, yokohama, kyoto, naha
    """
    # レート制限チェック
    if not rate_limiter.is_allowed():
        wait = rate_limiter.retry_after()
        return f"レート制限中です。{wait:.0f}秒後に再試行してください。"

    city_lower = city.lower()
    if city_lower not in CITY_COORDS:
        available = ", ".join(CITY_COORDS.keys())
        return f"未対応の都市です。対応都市: {available}"

    # キャッシュチェック
    cache_key = f"weather_{city_lower}"
    cached = cache.get(cache_key)
    if cached:
        return cached + "\n\n（キャッシュから取得）"

    lat, lon, name_ja = CITY_COORDS[city_lower]
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
    )

    try:
        data = fetch_api(url)
        current = data["current"]
        weather_desc = WMO_CODES.get(current["weather_code"], "不明")
        result = (
            f"📍 {name_ja}の現在の天気\n\n"
            f"天気: {weather_desc}\n"
            f"気温: {current['temperature_2m']}°C\n"
            f"湿度: {current['relative_humidity_2m']}%\n"
            f"風速: {current['wind_speed_10m']} km/h"
        )
        cache.set(cache_key, result)
        return result
    except Exception as e:
        return f"API呼び出しエラー: {e}"


@mcp.tool()
def get_forecast(city: str, days: int = 3) -> str:
    """指定した都市の天気予報を取得します。

    Args:
        city: 都市名（英語）
        days: 予報日数（1-7、デフォルト3）
    """
    if not rate_limiter.is_allowed():
        wait = rate_limiter.retry_after()
        return f"レート制限中です。{wait:.0f}秒後に再試行してください。"

    city_lower = city.lower()
    if city_lower not in CITY_COORDS:
        available = ", ".join(CITY_COORDS.keys())
        return f"未対応の都市です。対応都市: {available}"

    days = max(1, min(7, days))  # 1-7日の範囲に制限

    cache_key = f"forecast_{city_lower}_{days}"
    cached = cache.get(cache_key)
    if cached:
        return cached + "\n\n（キャッシュから取得）"

    lat, lon, name_ja = CITY_COORDS[city_lower]
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=weather_code,temperature_2m_max,temperature_2m_min,"
        f"precipitation_probability_max"
        f"&forecast_days={days}"
    )

    try:
        data = fetch_api(url)
        daily = data["daily"]
        lines = [f"📍 {name_ja}の{days}日間の天気予報\n"]
        lines.append("日付 | 天気 | 最高気温 | 最低気温 | 降水確率")
        lines.append("--- | --- | --- | --- | ---")
        for i in range(len(daily["time"])):
            weather_desc = WMO_CODES.get(daily["weather_code"][i], "不明")
            lines.append(
                f"{daily['time'][i]} | {weather_desc} | "
                f"{daily['temperature_2m_max'][i]}°C | "
                f"{daily['temperature_2m_min'][i]}°C | "
                f"{daily['precipitation_probability_max'][i]}%"
            )
        result = "\n".join(lines)
        cache.set(cache_key, result)
        return result
    except Exception as e:
        return f"API呼び出しエラー: {e}"
```

### よくある間違い

| 間違い | 正しい対応 |
|-------|-----------|
| APIキーをソースコードに直接記載する | 環境変数 (`os.environ`) で管理する |
| レート制限を実装しない | `RateLimiter` クラスでAPI呼び出し頻度を制御する |
| 同じリクエストで何度もAPIを叩く | TTL付きキャッシュで重複リクエストを削減する |
| APIのタイムアウトを設定しない | `urlopen(url, timeout=10)` でタイムアウトを設定する |

### ポイントまとめ

- 外部APIキーは必ず環境変数で管理し、コードに含めないようにします
- レート制限とキャッシュで、APIの無駄な呼び出しを防ぎます
- タイムアウトを設定して、外部APIの応答遅延からサーバーを保護します
- Open-Meteo APIはAPIキー不要で学習に最適です

---

## 7.4 プロジェクト4：Git操作サーバー

### 要件定義

Gitリポジトリの情報を取得・操作するMCPサーバーです。

**提供する機能：**

| ツール名 | 説明 |
|---------|------|
| `git_status` | ワーキングツリーの変更状態を表示 |
| `git_log` | コミット履歴を表示 |
| `git_diff` | 差分を表示 |
| `git_commit` | 変更をコミット |

### 完全な実装コード

```python
# git_server.py - Git操作MCPサーバー
# 学べる内容：サブプロセス呼び出し、コマンドインジェクション対策
# 実行方法：GIT_REPO_PATH=/path/to/repo python -m mcp dev git_server.py

import subprocess
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("git-server")

# 操作対象のGitリポジトリパス
REPO_PATH = Path(
    os.environ.get("GIT_REPO_PATH", ".")
).resolve()


def run_git(*args: str) -> tuple[bool, str]:
    """Gitコマンドを安全に実行します。

    Returns:
        (成功したか, 出力テキスト)
    """
    try:
        result = subprocess.run(
            ["git"] + list(args),
            cwd=str(REPO_PATH),
            capture_output=True,
            text=True,
            timeout=30,  # 30秒でタイムアウト
        )
        output = result.stdout.strip()
        if result.returncode != 0:
            error = result.stderr.strip()
            return False, f"Gitエラー: {error}"
        return True, output
    except subprocess.TimeoutExpired:
        return False, "エラー: コマンドがタイムアウトしました（30秒）"
    except FileNotFoundError:
        return False, "エラー: gitコマンドが見つかりません。gitをインストールしてください。"


@mcp.tool()
def git_status() -> str:
    """現在のリポジトリのステータス（変更されたファイル一覧）を表示します。"""
    success, output = run_git("status", "--short")
    if not success:
        return output
    if not output:
        return "変更はありません（ワーキングツリーはクリーンです）。"
    return f"変更状態:\n{output}"


@mcp.tool()
def git_log(count: int = 10) -> str:
    """直近のコミット履歴を表示します。

    Args:
        count: 表示するコミット数（デフォルト10、最大50）
    """
    count = max(1, min(50, count))
    success, output = run_git(
        "log",
        f"-{count}",
        "--oneline",
        "--graph",
        "--decorate"
    )
    if not success:
        return output
    return f"直近{count}件のコミット:\n{output}"


@mcp.tool()
def git_diff(staged: bool = False, file_path: str = "") -> str:
    """差分（変更内容）を表示します。

    Args:
        staged: ステージ済みの差分を表示するか（デフォルト: False）
        file_path: 特定ファイルの差分のみ表示（省略時は全体）
    """
    args = ["diff"]
    if staged:
        args.append("--cached")
    if file_path:
        # パスバリデーション：../ を含むパスを拒否
        if ".." in file_path:
            return "エラー: 無効なファイルパスです。"
        args.append("--")
        args.append(file_path)

    success, output = run_git(*args)
    if not success:
        return output
    if not output:
        return "差分はありません。"
    # 差分が長すぎる場合は切り詰め
    lines = output.split("\n")
    if len(lines) > 200:
        output = "\n".join(lines[:200]) + f"\n\n... （残り{len(lines) - 200}行省略）"
    return output


@mcp.tool()
def git_commit(message: str) -> str:
    """ステージ済みの変更をコミットします。事前にgit addされたファイルのみ対象です。

    Args:
        message: コミットメッセージ
    """
    if not message.strip():
        return "エラー: コミットメッセージは空にできません。"
    if len(message) > 500:
        return "エラー: コミットメッセージが長すぎます（500文字以内）。"

    # まずステージ済みの変更があるか確認
    success, diff_output = run_git("diff", "--cached", "--stat")
    if not success:
        return diff_output
    if not diff_output:
        return "エラー: ステージ済みの変更がありません。先にgit addしてください。"

    # コミット実行
    # 注意：messageはリスト引数として渡すのでシェルインジェクションは発生しない
    success, output = run_git("commit", "-m", message)
    if not success:
        return output
    return f"コミット成功:\n{output}"
```

### よくある間違い

| 間違い | 正しい対応 |
|-------|-----------|
| `os.system(f"git {user_input}")` のようにシェルを経由する | `subprocess.run(["git", ...])` でリスト形式で引数を渡す |
| タイムアウトを設定しない | `timeout=30` で長時間ハングを防止する |
| 任意のgitコマンドを許可する | 許可するサブコマンドを限定する（`status`, `log`, `diff`, `commit`） |
| コミットメッセージの長さを制限しない | 上限を設けて異常な入力を防ぐ |

### ポイントまとめ

- `subprocess.run()` はリスト形式で引数を渡すことで、コマンドインジェクション（Command Injection）を防止します
- 実行可能な操作（サブコマンド）を限定し、`push` や `reset --hard` 等の危険な操作を提供しないことが重要です
- タイムアウト設定により、巨大リポジトリでの長時間ハングを防ぎます

---

## 7.5 テストの書き方

### MCPサーバーのテスト戦略

MCPサーバーのテストは3段階で行います。

```
┌───────────────────────────────────┐
│   1. ユニットテスト（Unit Test）     │  ← 個々の関数をテスト
├───────────────────────────────────┤
│   2. 統合テスト（Integration Test） │  ← MCPプロトコル経由でテスト
├───────────────────────────────────┤
│   3. 手動テスト（MCP Inspector）    │  ← ブラウザUIでテスト
└───────────────────────────────────┘
```

### ユニットテスト

各ツール関数を直接呼び出してテストします。

```python
# test_db_server.py - データベースサーバーのユニットテスト
# 実行方法：python -m pytest test_db_server.py -v

import os
import tempfile
import pytest

# テスト用の一時データベースを使用
@pytest.fixture(autouse=True)
def setup_test_db(tmp_path):
    """テスト用の一時データベースをセットアップします。"""
    test_db = str(tmp_path / "test.db")
    os.environ["DB_PATH"] = test_db
    # サーバーモジュールをインポート（環境変数設定後に行う）
    import importlib
    import db_server
    importlib.reload(db_server)
    db_server.DB_PATH = test_db
    db_server.init_sample_db()
    yield db_server
    # クリーンアップ
    if os.path.exists(test_db):
        os.remove(test_db)


def test_list_tables(setup_test_db):
    """テーブル一覧が正しく取得できることを検証します。"""
    result = setup_test_db.list_tables()
    assert "posts" in result
    assert "users" in result


def test_query_select(setup_test_db):
    """SELECT文が正常に実行できることを検証します。"""
    result = setup_test_db.query("SELECT name FROM users ORDER BY name")
    assert "田中太郎" in result
    assert "佐藤花子" in result


def test_query_rejects_non_select(setup_test_db):
    """SELECT以外のSQL文が拒否されることを検証します。"""
    result = setup_test_db.query("DROP TABLE users")
    assert "エラー" in result


def test_describe_table(setup_test_db):
    """テーブルスキーマが正しく取得できることを検証します。"""
    result = setup_test_db.describe_table("users")
    assert "name" in result
    assert "email" in result


def test_execute_insert(setup_test_db):
    """INSERT文が正常に実行できることを検証します。"""
    result = setup_test_db.execute(
        "INSERT INTO users (name, email) VALUES ('テスト', 'test@example.com')"
    )
    assert "成功" in result
```

### 統合テスト

MCPクライアントを使ってプロトコル経由でテストします。

```python
# test_integration.py - MCPプロトコル経由の統合テスト
# 実行方法：python -m pytest test_integration.py -v

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_SCRIPT = "db_server.py"


@pytest.fixture
async def mcp_session():
    """MCPセッションを作成するフィクスチャです。"""
    server_params = StdioServerParameters(
        command="python",
        args=[SERVER_SCRIPT],
        env={"DB_PATH": "test_integration.db"},
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


@pytest.mark.asyncio
async def test_list_tools(mcp_session):
    """サーバーが正しいツール一覧を返すことを検証します。"""
    tools = await mcp_session.list_tools()
    tool_names = [t.name for t in tools.tools]
    assert "query" in tool_names
    assert "list_tables" in tool_names
    assert "describe_table" in tool_names
    assert "execute" in tool_names


@pytest.mark.asyncio
async def test_call_tool(mcp_session):
    """ツール呼び出しが正常に動作することを検証します。"""
    result = await mcp_session.call_tool("list_tables", {})
    assert result.content[0].text
    assert "users" in result.content[0].text
```

### MCP Inspectorによる手動テスト

MCP Inspector（MCPインスペクター）はブラウザベースのテストツールです。

```bash
# MCP Inspectorの起動
npx @modelcontextprotocol/inspector python db_server.py

# 起動するとブラウザが開き、以下の操作が可能です：
# - 接続状態の確認
# - ツール一覧の確認
# - ツールの手動実行（引数を入力して呼び出し）
# - リソースの閲覧
# - レスポンスの確認
```

MCP Inspectorの主な画面構成：

```
┌─────────────────────────────────────────────┐
│  MCP Inspector                              │
├──────────────┬──────────────────────────────┤
│              │                              │
│  Tools       │  Tool: query                 │
│  ・query     │  ─────────────               │
│  ・list_..   │  sql: [SELECT * FROM users ] │
│  ・descri..  │                              │
│  ・execute   │  [▶ Run]                     │
│              │                              │
│  Resources   │  Response:                   │
│  ・db://..   │  結果: 2件                    │
│              │  name | email                │
│              │  田中太郎 | tanaka@...        │
│              │  佐藤花子 | sato@...          │
└──────────────┴──────────────────────────────┘
```

### ポイントまとめ

- ユニットテストでは各ツール関数を直接呼び出し、ロジックの正しさを確認します
- 統合テストではMCPプロトコル経由でツールを呼び出し、エンドツーエンドの動作を検証します
- MCP Inspectorはブラウザから手動でツールをテストできる強力なデバッグツールです
- テスト用の一時ファイルや一時データベースを使い、テスト間の独立性を確保します
- `pytest` の `fixture` を活用して、テストのセットアップとクリーンアップを自動化します

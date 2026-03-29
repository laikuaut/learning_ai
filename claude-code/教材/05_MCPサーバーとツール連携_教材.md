# 第5章：MCPサーバーとツール連携

## この章のゴール
- MCP（Model Context Protocol）の仕組みとClaude Codeとの統合方法を理解する
- MCPサーバーの設定方法（プロジェクトスコープ・ユーザースコープ）を習得する
- 代表的なMCPサーバー（GitHub、ファイルシステム、データベースなど）の活用法を学ぶ
- MCPツールをClaude Codeセッション内で実際に使えるようになる
- MCPサーバーの設定ファイル（`mcpServers`）の書き方をマスターする

---

## 5.1 MCPとは何か

### Model Context Protocolの概要

MCP（Model Context Protocol）は、Anthropic社が策定したオープンプロトコル（open protocol）です。AIアプリケーションと外部ツール・データソースを**標準化された方法**で接続するための仕組みです。

Claude Codeでは、MCPサーバーを通じてさまざまな外部サービスやローカルツールと連携できます。これにより、Claude Codeの能力を大幅に拡張できます。

### なぜClaude CodeでMCPが重要なのか

Claude Code単体でも強力なコーディング支援が可能ですが、MCPサーバーを追加することで以下のような拡張が実現します。

| 機能 | MCPなし | MCPあり |
|---|---|---|
| GitHub操作 | CLIコマンド経由のみ | 直接API操作が可能 |
| データベース操作 | SQLコマンド手動実行 | スキーマ取得・クエリ実行を直接支援 |
| ファイル検索 | 基本的なgrep/find | 高度な意味検索が可能 |
| 外部API連携 | curl等で手動実行 | ツールとして自然に利用 |

### MCPの3層アーキテクチャ

MCPは**ホスト（host）**、**クライアント（client）**、**サーバー（server）**の3層で構成されます。Claude Codeにおける対応関係を見てみましょう。

```
┌─────────────────────────────────────────────────┐
│  ホスト（Host）: Claude Code                      │
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │  MCPクライアント（Client）                    │ │
│  │  Claude Code内蔵のMCPクライアント機能         │ │
│  └──────┬──────────┬──────────┬────────────────┘ │
│         │          │          │                   │
└─────────┼──────────┼──────────┼───────────────────┘
          │          │          │
    ┌─────▼────┐ ┌──▼───────┐ ┌▼───────────┐
    │ MCPサーバー│ │MCPサーバー│ │MCPサーバー  │
    │ GitHub   │ │filesystem│ │ PostgreSQL │
    └─────┬────┘ └──┬───────┘ └┬───────────┘
          │          │          │
    ┌─────▼────┐ ┌──▼───────┐ ┌▼───────────┐
    │ GitHub   │ │ローカル   │ │ データベース│
    │ API      │ │ファイル   │ │            │
    └──────────┘ └──────────┘ └────────────┘
```

### MCPサーバーが提供する3つの機能

MCPサーバーは、以下の3つの機能（プリミティブ）を提供できます。

| 機能 | 英語名 | 説明 | Claude Codeでの使い方 |
|---|---|---|---|
| ツール | Tools | 実行可能なアクション | コマンドのように呼び出す |
| リソース | Resources | 読み取り可能なデータ | コンテキストとして参照 |
| プロンプト | Prompts | 再利用可能なテンプレート | 定型操作のショートカット |

Claude Codeで最も頻繁に使うのは**ツール（Tools）**です。MCPサーバーが提供するツールは、Claude Codeの組み込みツール（Bash、Read、Write、Editなど）と同様に利用できます。

### ポイントまとめ
- MCPはAIアプリと外部ツールをつなぐ標準プロトコルである
- Claude CodeはMCPホスト兼クライアントとして機能する
- MCPサーバーを追加することでClaude Codeの能力を大幅に拡張できる
- ツール・リソース・プロンプトの3つの機能が提供される

---

## 5.2 MCPサーバーの設定方法

### 設定ファイルの種類

Claude CodeでMCPサーバーを設定する方法は複数あります。設定のスコープ（scope：適用範囲）によって使い分けます。

| 設定ファイル | スコープ | 場所 | 用途 |
|---|---|---|---|
| `~/.claude/settings.json` | ユーザースコープ | ホームディレクトリ | 全プロジェクト共通のMCPサーバー |
| `.claude/settings.json` | プロジェクトスコープ | プロジェクトルート | 特定プロジェクト専用のMCPサーバー |
| `.claude/settings.local.json` | ローカルスコープ | プロジェクトルート | 個人環境固有の設定（Gitにコミットしない） |

### スコープの選び方

```
ユーザースコープ（~/.claude/settings.json）
  → 自分がどのプロジェクトでも使いたいMCPサーバー
  → 例：GitHub MCP、個人用ナレッジベース

プロジェクトスコープ（.claude/settings.json）
  → チーム全員で共有すべきMCPサーバー
  → 例：プロジェクト専用のDB接続、社内API連携
  → Gitにコミットしてチームで共有する

ローカルスコープ（.claude/settings.local.json）
  → 個人の環境に依存する設定（認証情報を含むもの等）
  → Gitにコミットしない（.gitignoreに追加推奨）
```

### mcpServers設定の基本フォーマット

MCPサーバーの設定は、`mcpServers`キーの下にサーバーごとの設定を記述します。

```json
{
  "mcpServers": {
    "サーバー名": {
      "command": "実行コマンド",
      "args": ["引数1", "引数2"],
      "env": {
        "環境変数名": "値"
      }
    }
  }
}
```

各フィールドの意味は以下の通りです。

| フィールド | 必須 | 説明 |
|---|---|---|
| `command` | はい | MCPサーバーを起動するコマンド |
| `args` | いいえ | コマンドに渡す引数の配列 |
| `env` | いいえ | MCPサーバーに渡す環境変数 |
| `cwd` | いいえ | サーバー起動時の作業ディレクトリ |

### CLIからMCPサーバーを追加する

`claude mcp add`コマンドを使うと、対話的にMCPサーバーを追加できます。

```bash
# 基本的な追加コマンド
claude mcp add <サーバー名> -- <コマンド> [引数...]

# ユーザースコープに追加（-s user）
claude mcp add -s user github -- npx -y @modelcontextprotocol/server-github

# プロジェクトスコープに追加（-s project）
claude mcp add -s project my-db -- npx -y @modelcontextprotocol/server-postgres postgresql://localhost/mydb

# 環境変数を指定して追加（-e オプション）
claude mcp add -s user github -e GITHUB_TOKEN=ghp_xxxxx -- npx -y @modelcontextprotocol/server-github
```

### MCPサーバーの管理コマンド

```bash
# 登録されているMCPサーバーの一覧表示
claude mcp list

# 特定のMCPサーバーの詳細表示
claude mcp get <サーバー名>

# MCPサーバーの削除
claude mcp remove <サーバー名>
```

### ポイントまとめ
- 設定ファイルはユーザー・プロジェクト・ローカルの3つのスコープがある
- `mcpServers`キーにサーバー名・コマンド・引数・環境変数を記述する
- `claude mcp add`コマンドで対話的に追加できる
- 認証情報を含む設定は`.claude/settings.local.json`に分離する

---

## 5.3 代表的なMCPサーバー

### GitHub MCPサーバー

GitHub MCPサーバーは、GitHubのAPIを直接操作できるツールを提供します。イシュー（issue）の操作、プルリクエスト（pull request）の管理、リポジトリの検索などが可能です。

**設定例：**

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

**提供される主なツール：**

| ツール名 | 機能 |
|---|---|
| `search_repositories` | リポジトリを検索 |
| `list_issues` | イシュー一覧を取得 |
| `create_issue` | 新しいイシューを作成 |
| `create_pull_request` | プルリクエストを作成 |
| `get_file_contents` | ファイル内容を取得 |
| `push_files` | ファイルをプッシュ |

**活用例：**

```
ユーザー: このリポジトリのオープンなイシューを一覧表示して

Claude Code: （GitHub MCPのlist_issuesツールを使用して一覧を取得・表示）
```

### ファイルシステムMCPサーバー

ローカルのファイルシステムに対して、通常のClaude Codeよりも広範な操作を提供します。特定のディレクトリへの安全なアクセスを制御できます。

**設定例：**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/user/documents",
        "/home/user/projects"
      ]
    }
  }
}
```

`args`の末尾にアクセスを許可するディレクトリパスを列挙します。指定されたディレクトリ外へのアクセスはブロックされます。

### PostgreSQL MCPサーバー

PostgreSQLデータベースに接続し、スキーマ（schema：データベースの構造定義）の確認やクエリ（query：問い合わせ）の実行ができます。

**設定例：**

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://user:password@localhost:5432/mydb"
      ]
    }
  }
}
```

**提供される主なツール：**

| ツール名 | 機能 |
|---|---|
| `query` | SQLクエリを実行 |
| `list_tables` | テーブル一覧を取得 |
| `describe_table` | テーブル構造を確認 |

### その他の代表的なMCPサーバー

| MCPサーバー | パッケージ名 | 主な用途 |
|---|---|---|
| Slack | `@modelcontextprotocol/server-slack` | Slackメッセージの送受信 |
| Google Drive | `@modelcontextprotocol/server-gdrive` | Googleドライブのファイル操作 |
| Puppeteer | `@modelcontextprotocol/server-puppeteer` | ブラウザ操作の自動化 |
| Memory | `@modelcontextprotocol/server-memory` | 知識グラフによる記憶管理 |
| Fetch | `@modelcontextprotocol/server-fetch` | Webページの取得 |
| SQLite | `@modelcontextprotocol/server-sqlite` | SQLiteデータベース操作 |

### MCPサーバーの全体像

```
┌──────────────────────────────────────────────┐
│              Claude Code                      │
│  ┌────────────────────────────────────────┐  │
│  │         MCPクライアント                  │  │
│  │                                        │  │
│  │  組み込みツール    MCPツール             │  │
│  │  ┌──────────┐   ┌──────────────────┐  │  │
│  │  │ Bash     │   │ github.*         │  │  │
│  │  │ Read     │   │ postgres.*       │  │  │
│  │  │ Write    │   │ filesystem.*     │  │  │
│  │  │ Edit     │   │ slack.*          │  │  │
│  │  │ Grep     │   │ memory.*         │  │  │
│  │  │ Glob     │   │ ...              │  │  │
│  │  └──────────┘   └──────────────────┘  │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

### ポイントまとめ
- GitHub MCPサーバーはイシュー・PR操作を直接実行できる
- ファイルシステムMCPサーバーはアクセス範囲を制御できる
- データベースMCPサーバーでスキーマ確認やクエリ実行が可能
- 公式・コミュニティ製の多種多様なMCPサーバーが存在する

---

## 5.4 MCPツールの使い方

### MCPツールの確認

MCPサーバーが正しく設定されると、そのサーバーが提供するツールがClaude Codeセッションで自動的に利用可能になります。

セッション開始時に、接続されたMCPサーバーとツールの情報が表示されます。

```
$ claude

Claude Code v1.x.x

> Connected MCP servers:
  - github (12 tools)
  - postgres (3 tools)
```

### MCPツールの呼び出し

MCPツールは自然言語で要求するだけでClaude Codeが適切なツールを選択して呼び出します。特別な構文は不要です。

```
ユーザー: GitHubのissue #42の内容を確認して

Claude Code: GitHub MCPサーバーの issue_read ツールを使用します。

  mcp__github__issue_read (repo: "myorg/myrepo", issue_number: 42)

  Issue #42: ログイン画面のバグ修正
  状態: open
  作成者: tanaka
  ...
```

### MCPツールの権限管理

MCPツールの使用にはユーザーの許可（permission）が必要です。初回呼び出し時に確認ダイアログが表示されます。

```
Claude Code wants to use: mcp__github__create_issue

  Allow?
  (y) Yes, once
  (a) Always allow this tool
  (n) No, deny
```

許可の設定は`allowedTools`で事前に構成することもできます。

```json
{
  "allowedTools": [
    "mcp__github__issue_read",
    "mcp__github__list_issues",
    "mcp__github__search_repositories"
  ]
}
```

ワイルドカード（wildcard：`*`を使ったパターンマッチ）も使用できます。

```json
{
  "allowedTools": [
    "mcp__github__*"
  ]
}
```

### 実践例：MCPツールを活用した開発ワークフロー

以下は、GitHub MCPサーバーとPostgreSQL MCPサーバーを組み合わせた実践的なワークフローです。

```
ステップ1: イシューの確認
ユーザー: 「優先度の高いオープンイシューを見せて」
  → GitHub MCP の list_issues を使用

ステップ2: データベース調査
ユーザー: 「このイシューに関連するusersテーブルの構造を確認して」
  → PostgreSQL MCP の describe_table を使用

ステップ3: コード修正
ユーザー: 「イシューの内容に基づいてバグを修正して」
  → Claude Code組み込みのRead/Edit/Writeを使用

ステップ4: PRの作成
ユーザー: 「修正内容でPRを作成して」
  → GitHub MCP の create_pull_request を使用
```

```
┌────────────┐    ┌────────────┐    ┌────────────┐
│  イシュー   │───→│  調査・修正  │───→│  PR作成     │
│  確認      │    │            │    │            │
│ (GitHub    │    │ (PostgreSQL│    │ (GitHub    │
│  MCP)      │    │  MCP +     │    │  MCP)      │
│            │    │  組み込み)  │    │            │
└────────────┘    └────────────┘    └────────────┘
```

### ポイントまとめ
- MCPツールは自然言語で要求するだけで自動的に呼び出される
- 初回使用時は権限の許可が必要である
- `allowedTools`で事前に権限を設定できる（ワイルドカード対応）
- 複数のMCPサーバーを組み合わせた高度なワークフローが構築できる

---

## 5.5 MCPサーバーの設定例（実践）

### プロジェクト全体の設定例

以下は、Web開発プロジェクトでよく使うMCPサーバーをまとめて設定した例です。

**`.claude/settings.json`（プロジェクトスコープ）：**

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://localhost:5432/myapp_dev"
      ]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/user/myproject/docs"
      ]
    }
  },
  "allowedTools": [
    "mcp__postgres__query",
    "mcp__postgres__list_tables",
    "mcp__postgres__describe_table",
    "mcp__filesystem__read_file",
    "mcp__filesystem__list_directory"
  ]
}
```

**`~/.claude/settings.json`（ユーザースコープ）：**

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxxxxxx"
      }
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

### 環境変数を活用した安全な設定

認証トークン（authentication token）をJSONファイルに直接記述するのはセキュリティ上望ましくありません。環境変数（environment variable）を活用しましょう。

**方法1：シェルの環境変数を参照**

まず、`.bashrc`や`.zshrc`に環境変数を設定します。

```bash
# ~/.bashrc に追加
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxx"
```

MCPサーバーの設定で環境変数を参照します。

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**方法2：settings.local.jsonを使用**

チーム共有の設定と個人の認証情報を分離します。

```json
// .claude/settings.local.json（Gitにコミットしない）
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

```gitignore
# .gitignore に追加
.claude/settings.local.json
```

### ポイントまとめ
- プロジェクト共通の設定はプロジェクトスコープに配置する
- 個人の認証情報はローカルスコープまたは環境変数で管理する
- `allowedTools`と組み合わせて利用可能なツールを明示的に制御する
- `settings.local.json`はGitにコミットしないこと

---

## 5.6 トラブルシューティング

### MCPサーバーが接続できない場合

MCPサーバーの接続に問題がある場合、以下の手順で原因を特定します。

**チェックリスト：**

```
1. サーバーのコマンドが存在するか確認
   $ which npx
   $ npx -y @modelcontextprotocol/server-github --version

2. 設定ファイルのJSON構文が正しいか確認
   $ cat .claude/settings.json | python3 -m json.tool

3. 環境変数が正しく設定されているか確認
   $ echo $GITHUB_TOKEN

4. ネットワーク接続を確認（外部APIを使うサーバーの場合）
   $ curl -s https://api.github.com/rate_limit
```

### よくある間違い

**間違い1：JSONの末尾カンマ**

```json
// NG：最後の要素の後にカンマがある
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],  // ← 末尾カンマ
    }
  }
}

// OK：末尾カンマなし
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

**間違い2：npxの`-y`フラグの付け忘れ**

```json
// NG：-y がないとインストール確認で止まる
{
  "command": "npx",
  "args": ["@modelcontextprotocol/server-github"]
}

// OK：-y でインストールを自動承認
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"]
}
```

**間違い3：認証トークンの設定漏れ**

```json
// NG：GITHUB_TOKENが未設定だとAPIアクセスに失敗する
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}

// OK：env で認証トークンを設定
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

**間違い4：プロジェクトスコープとユーザースコープの混同**

```
NG: 個人の認証トークンを .claude/settings.json に書いてコミット
    → チームメンバーにトークンが漏洩する

OK: 認証トークンは ~/.claude/settings.json または
    .claude/settings.local.json に記述する
```

### ポイントまとめ
- 接続できないときはコマンドの存在確認・JSON構文確認・環境変数確認の順にチェックする
- npxには`-y`フラグを忘れずに付ける
- 認証トークンはプロジェクトスコープの設定ファイルにコミットしない
- JSONの末尾カンマはよくあるエラーの原因である

---

## 5.7 まとめ

この章では、Claude CodeにおけるMCPサーバーの設定と活用方法を学びました。

### 章全体のポイントまとめ

1. **MCPの基本**: MCPはAIアプリと外部ツールを標準化された方法で接続するプロトコルである
2. **設定のスコープ**: ユーザー・プロジェクト・ローカルの3つのスコープを目的に応じて使い分ける
3. **設定フォーマット**: `mcpServers`キーにサーバー名・コマンド・引数・環境変数を記述する
4. **代表的なサーバー**: GitHub、ファイルシステム、PostgreSQL、Slackなど多種多様なMCPサーバーが利用可能
5. **ツールの利用**: MCPツールは自然言語で要求するだけで自動呼び出しされる
6. **権限管理**: `allowedTools`でツールの利用許可を事前設定できる
7. **セキュリティ**: 認証情報はローカルスコープまたは環境変数で管理する

### 次章の予告

次の第6章では、Claude Codeのフック（Hooks）システムとカスタマイズ方法を学びます。特定のイベントに応じて自動的にシェルコマンドを実行する仕組みを理解し、開発ワークフローをさらに効率化する方法を習得します。

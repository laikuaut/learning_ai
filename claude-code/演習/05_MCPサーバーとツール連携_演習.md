# 第5章 演習：MCPサーバーとツール連携

## 基本問題

### 問題5-1：MCPの基本概念（穴埋め）
以下の文章の空欄（ア）〜（オ）に当てはまる語句を答えてください。

> Claude Codeにおける MCP（Model Context Protocol）とは、（ア）が外部の（イ）やデータソースに接続するための仕組みです。
> MCPサーバーを設定すると、Claude Codeは（ウ）を通じてファイルシステム、データベース、外部APIなどにアクセスできます。
> MCPサーバーの設定は（エ）コマンドまたは設定ファイルの直接編集で行います。
> サーバーとの通信には（オ）という通信方式が使われます。

**期待される出力例：**
```
（ア）Claude Code（AIアシスタント）
（イ）ツール
（ウ）MCPクライアント
（エ）claude mcp add
（オ）stdio（標準入出力）
```

<details>
<summary>ヒント</summary>

- Claude Code自体がMCPのHostとして機能します
- MCPサーバーとの通信方式にはstdio（標準入出力）とSSE（Server-Sent Events）があります
- `claude mcp add` コマンドでサーバーを追加できます

</details>

<details>
<summary>解答例</summary>

```
（ア）Claude Code（AIアシスタント）
（イ）ツール
（ウ）MCPクライアント
（エ）claude mcp add
（オ）stdio（標準入出力）
```

**解説：**
- Claude CodeはMCPのHost兼Clientとして動作し、MCPサーバーと通信します
- stdioトランスポートはローカルプロセスとの通信に使われ、最も一般的です
- SSE（Server-Sent Events）はリモートサーバーとのHTTPベースの通信に使われます
- `claude mcp add` コマンドは対話的にサーバーの追加を案内してくれます

</details>

### 問題5-2：MCPサーバー管理コマンド
以下の操作に対応する Claude Code の MCPコマンドを答えてください。

1. 新しいMCPサーバーを追加する
2. 設定済みのMCPサーバー一覧を表示する
3. 特定のMCPサーバーを削除する
4. MCPサーバーの設定を取得（表示）する
5. プロジェクトスコープでMCPサーバーを追加する

**期待される出力例：**
```
1. claude mcp add <サーバー名>
2. claude mcp list
3. claude mcp remove <サーバー名>
4. claude mcp get <サーバー名>
5. claude mcp add --scope project <サーバー名>
```

<details>
<summary>ヒント</summary>

- MCPサーバーの管理は `claude mcp` サブコマンドで行います
- スコープを指定するには `--scope` フラグを使用します
- `list` コマンドで現在の設定状況を確認できます

</details>

<details>
<summary>解答例</summary>

```
1. claude mcp add <サーバー名>
   # 例: claude mcp add my-server -t stdio -- npx my-mcp-server
2. claude mcp list
   # 設定済みの全MCPサーバーを一覧表示します
3. claude mcp remove <サーバー名>
   # 指定したサーバーの設定を削除します
4. claude mcp get <サーバー名>
   # 指定したサーバーの設定詳細を表示します
5. claude mcp add --scope project <サーバー名>
   # プロジェクトスコープ（.claude/settings.json）に保存されます
```

**補足：**
- `--scope` には `project`（プロジェクト）と `user`（ユーザー）があります
- プロジェクトスコープの設定はチーム全体で共有できます
- ユーザースコープの設定は `~/.claude/settings.json` に保存されます

</details>

### 問題5-3：スコープの使い分け
以下のMCPサーバーの設定シナリオについて、「project（プロジェクトスコープ）」と「user（ユーザースコープ）」のどちらが適切か答えてください。

1. チーム全員が使うGitHub MCPサーバーをプロジェクトに追加する
2. 個人のNotion MCPサーバーを自分だけの環境に追加する
3. プロジェクトのデータベースに接続するMCPサーバーを追加する
4. 個人的なメモアプリのMCPサーバーを追加する
5. CI/CDパイプラインで使うMCPサーバーを追加する
6. 個人のAPIキーを使うMCPサーバーを追加する

**期待される出力例：**
```
1. project
2. user
3. project
4. user
5. project
6. user
```

<details>
<summary>ヒント</summary>

- プロジェクトスコープは `.claude/settings.json` に保存され、Gitリポジトリに含めてチーム共有できます
- ユーザースコープは `~/.claude/settings.json` に保存され、そのマシンのユーザー固有です
- 個人のAPIキーや認証情報を含む設定はユーザースコープが適切です
- チーム全体で使う共有設定はプロジェクトスコープが適切です

</details>

<details>
<summary>解答例</summary>

```
1. project  ← チーム共有のツールはプロジェクトスコープに置きます
2. user     ← 個人のサービスはユーザースコープに置きます
3. project  ← プロジェクト固有のDBはプロジェクトスコープが適切です
4. user     ← 個人ツールはユーザースコープに置きます
5. project  ← CI/CD関連はプロジェクト設定として共有します
6. user     ← 個人のAPIキーはユーザースコープで管理します
```

**判断基準のまとめ：**
```
┌─────────────────────────────────────────┐
│  スコープ選択の判断フロー               │
│                                          │
│  チーム全員が使う？                      │
│    ├─ Yes → project スコープ             │
│    └─ No                                 │
│         個人の認証情報を含む？           │
│           ├─ Yes → user スコープ         │
│           └─ No → どちらでも可           │
│                 （通常は user）           │
└─────────────────────────────────────────┘
```

</details>

### 問題5-4：MCPサーバー設定の読解
以下のJSON設定を読み、各問いに答えてください。

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/project"],
      "type": "stdio"
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "type": "stdio",
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    }
  }
}
```

(1) この設定にはいくつのMCPサーバーが定義されていますか。それぞれの名前を答えてください。
(2) `filesystem` サーバーがアクセスできるディレクトリはどこですか。
(3) `github` サーバーの認証はどのように行われていますか。
(4) 両方のサーバーの通信方式は何ですか。
(5) この設定ファイルがセキュリティ上問題がある点を1つ指摘してください。

**期待される出力例：**
```
(1) 2つ：filesystem と github
(2) /home/user/project
(3) 環境変数 GITHUB_PERSONAL_ACCESS_TOKEN にパーソナルアクセストークンを設定
(4) stdio（標準入出力）
(5) GitHubのアクセストークンが平文で設定ファイルに記載されている
```

<details>
<summary>ヒント</summary>

- `mcpServers` オブジェクトのキーがサーバー名です
- `args` 配列の最後の要素がファイルシステムのパスになっています
- `env` フィールドで環境変数を設定できます
- 認証情報の管理方法に注意しましょう

</details>

<details>
<summary>解答例</summary>

```
(1) 2つのMCPサーバーが定義されています
    - filesystem（ファイルシステムサーバー）
    - github（GitHubサーバー）

(2) /home/user/project ディレクトリ
    args配列の最後の要素がアクセス対象のパスです

(3) 環境変数 GITHUB_PERSONAL_ACCESS_TOKEN にパーソナルアクセストークンを設定して認証
    env フィールドでトークンを渡しています

(4) stdio（標準入出力）
    両方とも "type": "stdio" が指定されています

(5) GitHubのパーソナルアクセストークン（ghp_xxxxxxxxxxxx）が平文で
    設定ファイルに記載されており、セキュリティリスクがあります
```

**セキュリティのベストプラクティス：**
- トークンは環境変数やシークレット管理ツールで管理すべきです
- 設定ファイルをGitにコミットする際はトークンを含めないようにします
- ユーザースコープの設定に個人トークンを置き、プロジェクトスコープには含めないようにします

</details>

---

## 応用問題

### 問題5-5：MCPサーバー設定の作成
以下の要件を満たすMCPサーバーの設定JSONを作成してください。

**要件：**
- サーバー名：`postgres-db`
- 実行コマンド：`npx`
- パッケージ：`@modelcontextprotocol/server-postgres`
- 接続先：`postgresql://localhost:5432/myapp_dev`
- 通信方式：stdio

**期待される出力例：**
```json
{
  "mcpServers": {
    "postgres-db": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost:5432/myapp_dev"],
      "type": "stdio"
    }
  }
}
```

<details>
<summary>ヒント</summary>

- `npx` コマンドで実行する場合、`-y` フラグを付けるとインストール確認をスキップできます
- 接続文字列は `args` の最後の要素として渡します
- `type` は通信方式を指定します

</details>

<details>
<summary>解答例</summary>

```json
{
  "mcpServers": {
    "postgres-db": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost:5432/myapp_dev"],
      "type": "stdio"
    }
  }
}
```

**CLIで追加する場合のコマンド：**
```bash
claude mcp add postgres-db \
  -t stdio \
  -- npx -y @modelcontextprotocol/server-postgres \
  postgresql://localhost:5432/myapp_dev
```

**注意事項：**
- 本番環境のデータベース接続文字列を設定ファイルに直接記載することは避けましょう
- 開発環境用の設定としてはこの方法で問題ありません
- 本番環境では環境変数経由でURLを渡すのがベストプラクティスです：
```json
{
  "mcpServers": {
    "postgres-db": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "type": "stdio",
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

</details>

### 問題5-6：人気のMCPサーバーの用途マッチング
以下のMCPサーバーと、その主な用途を正しく組み合わせてください。

**MCPサーバー：**
- (A) @modelcontextprotocol/server-filesystem
- (B) @modelcontextprotocol/server-github
- (C) @modelcontextprotocol/server-postgres
- (D) @modelcontextprotocol/server-memory
- (E) @modelcontextprotocol/server-puppeteer

**用途：**
1. ブラウザの自動操作、スクリーンショット取得、Webスクレイピング
2. ローカルファイルの読み書き、ディレクトリ操作
3. PostgreSQLデータベースへのクエリ実行とスキーマ参照
4. 会話間での知識・コンテキストの永続化
5. リポジトリの操作、Issue管理、PR作成

**期待される出力例：**
```
(A) - 2
(B) - 5
(C) - 3
(D) - 4
(E) - 1
```

<details>
<summary>ヒント</summary>

- サーバー名にはその機能を表すキーワードが含まれています
- `filesystem` はファイル操作、`memory` は記憶に関連します
- `puppeteer` はGoogleが開発したブラウザ自動化ライブラリです

</details>

<details>
<summary>解答例</summary>

```
(A) - 2  filesystem  → ローカルファイルの読み書き、ディレクトリ操作
(B) - 5  github      → リポジトリ操作、Issue管理、PR作成
(C) - 3  postgres    → PostgreSQLへのクエリ実行とスキーマ参照
(D) - 4  memory      → 会話間での知識・コンテキストの永続化
(E) - 1  puppeteer   → ブラウザ自動操作、スクリーンショット、スクレイピング
```

**各サーバーの補足：**

| サーバー | 主な提供機能 | 使い所 |
|---|---|---|
| filesystem | ファイル読み書き、検索、メタデータ取得 | プロジェクトのファイル操作全般 |
| github | Issue/PR操作、コード検索、ブランチ管理 | GitHub連携の開発ワークフロー |
| postgres | SQL実行、テーブル一覧、スキーマ情報 | データベース操作・分析 |
| memory | ナレッジグラフへのエンティティ保存・検索 | 長期的なコンテキスト保持 |
| puppeteer | ページ遷移、クリック、入力、スクリーンショット | E2Eテスト、Web操作自動化 |

</details>

---

## チャレンジ問題

### 問題5-7：MCPサーバーのトラブルシューティング
以下の各シナリオでMCPサーバーが正しく動作しません。原因と対処方法を答えてください。

**シナリオ1：**
```bash
$ claude mcp add my-server -t stdio -- npx @modelcontextprotocol/server-filesystem /tmp
# サーバーは追加できたが、Claude Code内でツールが表示されない
```

**シナリオ2：**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "type": "stdio"
    }
  }
}
```
```
エラー：Authentication failed. GITHUB_PERSONAL_ACCESS_TOKEN is not set.
```

**シナリオ3：**
```bash
$ claude mcp add db-server -t stdio -- python3 /path/to/my_mcp_server.py
# エラー：spawn python3 ENOENT
```

**期待される出力例：**
```
シナリオ1：
  原因：npxコマンドに -y フラグがないため、パッケージのインストール確認で止まっている
  対処：args に "-y" を追加する

シナリオ2：
  原因：GitHubの認証トークンが設定されていない
  対処：env フィールドに GITHUB_PERSONAL_ACCESS_TOKEN を追加する

シナリオ3：
  原因：python3 コマンドがPATHに存在しない
  対処：python3 のフルパスを指定する、またはPATHを確認する
```

<details>
<summary>ヒント</summary>

- シナリオ1：`npx` でパッケージを初回実行する際、確認プロンプトが表示されることがあります
- シナリオ2：GitHub APIは認証が必要です。環境変数でトークンを渡す必要があります
- シナリオ3：`ENOENT` は「ファイルが見つからない」を意味するNode.jsのエラーです

</details>

<details>
<summary>解答例</summary>

**シナリオ1：npxの -y フラグ不足**
```
原因：npx で未インストールのパッケージを実行する際、-y フラグがないと
      インストール確認プロンプトが表示され、stdioトランスポートが正しく
      初期化されません。
対処：args に "-y" を追加します。

修正後のコマンド：
claude mcp add my-server -t stdio -- npx -y @modelcontextprotocol/server-filesystem /tmp
```

**シナリオ2：認証トークン未設定**
```
原因：GitHub MCPサーバーはAPIアクセスにパーソナルアクセストークンが必要ですが、
      env フィールドが設定されていません。
対処：env フィールドでトークンを設定します。

修正後の設定：
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "type": "stdio",
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    }
  }
}
```

**シナリオ3：コマンドが見つからない**
```
原因：python3 コマンドがシステムのPATHに存在しないか、
      Claude Codeの実行環境でPATHが異なっています。
対処：以下のいずれかで対応します。
  (a) python3 のフルパスを指定する：
      claude mcp add db-server -t stdio -- /usr/bin/python3 /path/to/my_mcp_server.py
  (b) コマンドが存在するか確認する：
      which python3
  (c) 仮想環境を使っている場合は、仮想環境内のpythonパスを指定する
```

**トラブルシューティングの一般的な手順：**
```
1. claude mcp list でサーバーの登録状況を確認
2. 設定ファイルの JSON 構文を確認（カンマ漏れ等）
3. コマンドが直接実行できるかターミナルで確認
4. 環境変数が正しく設定されているか確認
5. ネットワーク接続を確認（リモートサーバーの場合）
```

</details>

### 問題5-8：プロジェクト向けMCPサーバー構成の設計
以下の要件を持つWebアプリケーション開発プロジェクトに、最適なMCPサーバー構成を設計してください。

**プロジェクト概要：**
- React + Node.js + PostgreSQLのWebアプリケーション
- GitHubでソースコード管理
- チーム5人で開発
- ローカル開発環境とステージング環境がある

**要件：**
(1) 必要なMCPサーバーを3つ以上選定し、その理由を述べてください
(2) 各サーバーの設定JSONを作成してください
(3) プロジェクトスコープとユーザースコープの使い分けを説明してください
(4) セキュリティに関する考慮事項を2つ以上挙げてください

**期待される出力例（一部）：**
```
(1) 選定するMCPサーバー：
    - filesystem: プロジェクトファイルの読み書きに使用
    - github: PR作成、コードレビュー支援に使用
    - postgres: 開発用DBのスキーマ確認・クエリ実行に使用
    理由：...

(2) 設定JSON：
    ...
```

<details>
<summary>ヒント</summary>

- プロジェクトで共有すべき設定と、個人で管理すべき設定を分けて考えましょう
- 認証トークンはプロジェクトスコープに含めてはいけません
- `.claude/settings.json`（プロジェクト）と `~/.claude/settings.json`（ユーザー）を使い分けます
- ステージング環境への接続は本番環境ほどではないですが、注意が必要です

</details>

<details>
<summary>解答例</summary>

**(1) 選定するMCPサーバー：**

| サーバー | 選定理由 |
|---|---|
| filesystem | プロジェクトのソースコード、設定ファイルの読み書きに必要 |
| github | PR作成、Issue管理、コードレビュー支援で開発効率を向上 |
| postgres | 開発用DBのスキーマ確認、テストデータ投入、クエリ検証に使用 |
| puppeteer | フロントエンドのE2Eテスト、UIの動作確認に活用 |

**(2) プロジェクトスコープの設定（`.claude/settings.json`）：**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./"],
      "type": "stdio"
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost:5432/myapp_dev"],
      "type": "stdio"
    }
  }
}
```

**ユーザースコープの設定（`~/.claude/settings.json`）：**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "type": "stdio",
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    }
  }
}
```

**(3) スコープの使い分け：**

| 設定内容 | スコープ | 理由 |
|---|---|---|
| filesystem サーバー | project | チーム全員が同じパスでアクセスするため |
| postgres（開発DB）サーバー | project | 開発用DB接続情報はチーム共通のため |
| github サーバー | user | 個人のアクセストークンを含むため |
| puppeteer サーバー | project | テスト設定はチーム共有のため |

**(4) セキュリティの考慮事項：**

1. **認証トークンの管理**
   - GitHubトークンなどの認証情報はユーザースコープに置き、Gitリポジトリにコミットしない
   - `.gitignore` に個人設定ファイルを追加する

2. **ファイルシステムのアクセス範囲**
   - filesystem サーバーのアクセスパスはプロジェクトディレクトリに限定する
   - `/` や `~` など広範囲のパスを指定しない

3. **データベース接続の分離**
   - 本番環境のDB接続情報は絶対にMCP設定に含めない
   - 開発用DBのみを設定対象とする

4. **チームメンバーへの周知**
   - MCPサーバーの権限範囲をチーム全員が理解していることを確認する
   - 新しいサーバー追加時はチームレビューを行う

</details>

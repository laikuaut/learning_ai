#!/bin/bash
# ============================================================
# Claude Code MCP設定デモ
# ============================================================
#
# 学べる内容:
#   - MCP（Model Context Protocol）サーバーの基本概念
#   - Claude Code での MCP サーバー設定方法
#   - プロジェクトレベル・ユーザーレベルの設定
#   - 人気のある MCP サーバーの設定例
#   - MCP サーバーの動作確認方法
#
# 実行方法:
#   chmod +x 04_MCP設定デモ.sh
#   ./04_MCP設定デモ.sh
#
# 注意:
#   このスクリプトはMCP設定ファイルのサンプルを作成するデモです。
#   実際のMCPサーバーの動作にはNode.jsや各MCPサーバーパッケージが必要です。
# ============================================================

# デモ用ディレクトリ
DEMO_DIR="/tmp/claude-mcp-demo"

echo "============================================================"
echo " Claude Code MCP設定デモ"
echo "============================================================"
echo ""

# ----------------------------------------------------------
# 1. MCP の概要説明
# ----------------------------------------------------------
echo "【1】MCP（Model Context Protocol）とは"
echo "------------------------------------------------------------"
echo ""
echo "  MCP は、AIアシスタントに外部ツールやデータソースを"
echo "  接続するための標準プロトコルです。"
echo ""
echo "  Claude Code では MCP サーバーを設定することで、"
echo "  以下のような外部サービスと連携できます:"
echo ""
echo "    - GitHub（Issue、PR操作）"
echo "    - ファイルシステム（指定ディレクトリへのアクセス）"
echo "    - データベース（PostgreSQL、SQLite等）"
echo "    - Slack（メッセージの送受信）"
echo "    - その他のカスタムツール"
echo ""

# ----------------------------------------------------------
# 2. デモ環境の準備
# ----------------------------------------------------------
echo "【2】デモ環境を準備します"
echo "------------------------------------------------------------"

rm -rf "$DEMO_DIR"
mkdir -p "$DEMO_DIR/.claude"
cd "$DEMO_DIR" || exit 1
git init --quiet
echo "デモディレクトリ: $DEMO_DIR"
echo ""

# ----------------------------------------------------------
# 3. プロジェクトレベルの MCP 設定
# ----------------------------------------------------------
# .claude/settings.json にMCPサーバーを設定する
# この設定はチーム全体で共有される
echo "【3】プロジェクトレベルの MCP 設定"
echo "------------------------------------------------------------"
echo ""
echo "設定ファイル: .claude/settings.json"
echo ""

cat > "$DEMO_DIR/.claude/settings.json" << 'SETTINGS_EOF'
{
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Bash(git:*)"
    ]
  },
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/user/projects",
        "/home/user/documents"
      ]
    }
  }
}
SETTINGS_EOF

echo "--- .claude/settings.json ---"
cat "$DEMO_DIR/.claude/settings.json"
echo ""
echo ""

# ----------------------------------------------------------
# 4. ユーザーレベルの MCP 設定
# ----------------------------------------------------------
# ~/.claude/settings.json にグローバルMCPサーバーを設定する
# 全プロジェクトで共通して使いたいMCPサーバーを設定
echo "【4】ユーザーレベル（グローバル）の MCP 設定"
echo "------------------------------------------------------------"
echo ""
echo "設定ファイル: ~/.claude/settings.json"
echo ""

# デモ用にローカルファイルとして作成（実際は ~/.claude/ に置く）
cat > "$DEMO_DIR/global-settings-example.json" << 'GLOBAL_EOF'
{
  "permissions": {
    "allow": [
      "Read",
      "Write"
    ]
  },
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic/mcp-server-slack"
      ],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://localhost:5432/mydb"
      ]
    }
  }
}
GLOBAL_EOF

echo "--- グローバル設定の例 ---"
cat "$DEMO_DIR/global-settings-example.json"
echo ""
echo ""

# ----------------------------------------------------------
# 5. claude mcp コマンドによる設定
# ----------------------------------------------------------
# CLIコマンドを使ってMCPサーバーを追加・管理する方法
echo "【5】claude mcp コマンドによる設定管理"
echo "------------------------------------------------------------"
echo ""

echo "● MCPサーバーの追加（JSONファイルを編集せずにコマンドで設定）:"
echo ""
echo "  # GitHub MCPサーバーを追加"
echo "  $ claude mcp add github \\"
echo "      -e GITHUB_TOKEN=ghp_xxxx \\"
echo "      -- npx -y @modelcontextprotocol/server-github"
echo ""
echo "  # ファイルシステム MCPサーバーを追加"
echo "  $ claude mcp add filesystem \\"
echo "      -- npx -y @modelcontextprotocol/server-filesystem /path/to/dir"
echo ""
echo "  # スコープを指定して追加（user = グローバル、project = プロジェクト）"
echo "  $ claude mcp add --scope user slack \\"
echo "      -e SLACK_BOT_TOKEN=xoxb-xxxx \\"
echo "      -- npx -y @anthropic/mcp-server-slack"
echo ""

echo "● MCPサーバーの一覧表示:"
echo "  $ claude mcp list"
echo ""

echo "● MCPサーバーの削除:"
echo "  $ claude mcp remove github"
echo ""

echo "● MCPサーバーの詳細確認:"
echo "  $ claude mcp get github"
echo ""

# ----------------------------------------------------------
# 6. 各 MCP サーバーの設定例
# ----------------------------------------------------------
echo "【6】人気のあるMCPサーバーの設定例"
echo "============================================================"
echo ""

# GitHub MCP サーバー
echo "--- (a) GitHub MCPサーバー ---"
echo "用途: Issue作成、PR操作、リポジトリ検索"
echo ""
cat << 'GITHUB_MCP'
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
  }
}
GITHUB_MCP
echo ""

# ファイルシステム MCP サーバー
echo "--- (b) ファイルシステム MCPサーバー ---"
echo "用途: 指定ディレクトリへの安全なファイルアクセス"
echo ""
cat << 'FS_MCP'
"filesystem": {
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "/allowed/path/1",
    "/allowed/path/2"
  ]
}
FS_MCP
echo ""

# PostgreSQL MCP サーバー
echo "--- (c) PostgreSQL MCPサーバー ---"
echo "用途: データベースのクエリ実行、スキーマ確認"
echo ""
cat << 'PG_MCP'
"postgres": {
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-postgres",
    "postgresql://user:pass@localhost:5432/dbname"
  ]
}
PG_MCP
echo ""

# Slack MCP サーバー
echo "--- (d) Slack MCPサーバー ---"
echo "用途: Slackメッセージの送受信、チャンネル管理"
echo ""
cat << 'SLACK_MCP'
"slack": {
  "command": "npx",
  "args": ["-y", "@anthropic/mcp-server-slack"],
  "env": {
    "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"
  }
}
SLACK_MCP
echo ""

# ----------------------------------------------------------
# 7. MCP 設定のベストプラクティス
# ----------------------------------------------------------
echo "【7】MCP設定のベストプラクティス"
echo "============================================================"
echo ""
echo "  1. 機密情報は環境変数を使う"
echo "     - トークンやパスワードは直接書かず \${VAR} 形式を使う"
echo "     - .env ファイルや OS の環境変数で管理する"
echo ""
echo "  2. スコープを適切に使い分ける"
echo "     - user: 全プロジェクト共通（Slack、個人GitHub等）"
echo "     - project: 特定プロジェクト用（DB接続等）"
echo ""
echo "  3. 最小権限の原則"
echo "     - ファイルシステムは必要なパスだけ許可する"
echo "     - DBは読み取り専用ユーザーを使う"
echo ""
echo "  4. チーム共有設定"
echo "     - .claude/settings.json はリポジトリにコミットする"
echo "     - 秘密情報を含む設定は .claude/settings.local.json に"
echo ""

# ----------------------------------------------------------
# 8. 作成したファイルの確認
# ----------------------------------------------------------
echo "【8】作成したファイル一覧"
echo "------------------------------------------------------------"
echo ""
find "$DEMO_DIR" -name ".git" -prune -o -type f -print | sort | while read -r file; do
    echo "  ${file#$DEMO_DIR/}"
done
echo ""

echo "============================================================"
echo " デモ完了 - デモファイルは $DEMO_DIR に作成されました"
echo "============================================================"

#!/bin/bash
# ============================================================
# Claude Code プロジェクト初期設定デモ
# ============================================================
#
# 学べる内容:
#   - CLAUDE.md ファイルの作成と活用法
#   - .claude/settings.json の設定方法
#   - 許可ツールとパーミッションの管理
#   - プロジェクトワークスペースの初期化
#   - 設定ファイルの階層構造（グローバル/プロジェクト/ローカル）
#
# 実行方法:
#   chmod +x 02_プロジェクト初期設定デモ.sh
#   ./02_プロジェクト初期設定デモ.sh
#
# 注意:
#   このスクリプトは /tmp/claude-code-demo ディレクトリに
#   デモ用のプロジェクトを作成します。
#   既存のプロジェクトには影響しません。
# ============================================================

# デモ用ディレクトリ
DEMO_DIR="/tmp/claude-code-demo"

echo "============================================================"
echo " Claude Code プロジェクト初期設定デモ"
echo "============================================================"
echo ""

# ----------------------------------------------------------
# 1. デモ用プロジェクトディレクトリの作成
# ----------------------------------------------------------
echo "【1】デモ用プロジェクトディレクトリを作成します"
echo "------------------------------------------------------------"

# 既存のデモディレクトリがあれば削除
if [ -d "$DEMO_DIR" ]; then
    echo "既存のデモディレクトリを削除します..."
    rm -rf "$DEMO_DIR"
fi

# プロジェクトディレクトリを作成
mkdir -p "$DEMO_DIR"
cd "$DEMO_DIR" || exit 1

# Gitリポジトリとして初期化（Claude Codeはgitリポジトリで最も効果的）
git init
echo "プロジェクトディレクトリ: $DEMO_DIR"
echo ""

# ----------------------------------------------------------
# 2. CLAUDE.md の作成
# ----------------------------------------------------------
# CLAUDE.md はプロジェクトのルートに配置する設定ファイル
# Claude Codeが会話開始時に自動的に読み込む
# プロジェクト固有のルールや知識を記述する
echo "【2】CLAUDE.md を作成します"
echo "------------------------------------------------------------"

cat > "$DEMO_DIR/CLAUDE.md" << 'CLAUDE_EOF'
# プロジェクト概要

このプロジェクトはWebアプリケーションのバックエンドAPIです。

## 技術スタック
- 言語: Python 3.12
- フレームワーク: FastAPI
- データベース: PostgreSQL
- ORM: SQLAlchemy

## コーディング規約
- PEP 8 に準拠すること
- 型ヒント（type hints）を必ず使用すること
- docstring は Google スタイルで記述すること
- テストは pytest で書くこと

## ディレクトリ構造
```
src/
├── api/          # APIエンドポイント
├── models/       # データベースモデル
├── services/     # ビジネスロジック
├── schemas/      # Pydanticスキーマ
└── utils/        # ユーティリティ
tests/
├── unit/         # ユニットテスト
└── integration/  # 統合テスト
```

## 重要なルール
- APIレスポンスは必ず統一フォーマットで返す
- 環境変数は .env ファイルで管理（コミットしない）
- マイグレーションは Alembic を使用する
- エラーハンドリングは集約ハンドラで行う

## よく使うコマンド
- テスト実行: `pytest`
- リンター: `ruff check .`
- フォーマッター: `ruff format .`
- サーバー起動: `uvicorn src.main:app --reload`
CLAUDE_EOF

echo "CLAUDE.md を作成しました"
echo ""
# CLAUDE.md の内容を確認
echo "--- CLAUDE.md の内容（先頭10行） ---"
head -10 "$DEMO_DIR/CLAUDE.md"
echo "..."
echo ""

# ----------------------------------------------------------
# 3. .claude/settings.json の作成
# ----------------------------------------------------------
# プロジェクトレベルの設定ファイル
# チームで共有する設定はこのファイルに記述する
echo "【3】.claude/settings.json を作成します"
echo "------------------------------------------------------------"

mkdir -p "$DEMO_DIR/.claude"

cat > "$DEMO_DIR/.claude/settings.json" << 'SETTINGS_EOF'
{
  "permissions": {
    "allow": [
      "Bash(pytest:*)",
      "Bash(ruff:*)",
      "Bash(python:*)",
      "Bash(uvicorn:*)",
      "Bash(pip install:*)",
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Read",
      "Write",
      "Edit"
    ],
    "deny": [
      "Bash(rm -rf /)",
      "Bash(git push --force:*)",
      "Bash(curl:*)",
      "Bash(wget:*)"
    ]
  }
}
SETTINGS_EOF

echo ".claude/settings.json を作成しました"
echo ""
echo "--- settings.json の内容 ---"
cat "$DEMO_DIR/.claude/settings.json"
echo ""
echo ""

# ----------------------------------------------------------
# 4. .claude/settings.local.json の作成
# ----------------------------------------------------------
# ローカル（個人）設定ファイル
# .gitignore に追加して、個人の環境固有の設定を管理する
echo "【4】.claude/settings.local.json を作成します"
echo "------------------------------------------------------------"
echo "※ このファイルは個人の環境固有の設定です"
echo "※ .gitignore に追加してリポジトリにはコミットしません"

cat > "$DEMO_DIR/.claude/settings.local.json" << 'LOCAL_SETTINGS_EOF'
{
  "permissions": {
    "allow": [
      "Bash(docker compose:*)",
      "Bash(make:*)"
    ]
  },
  "env": {
    "DATABASE_URL": "postgresql://localhost:5432/myapp_dev",
    "DEBUG": "true"
  }
}
LOCAL_SETTINGS_EOF

echo ".claude/settings.local.json を作成しました"
echo ""

# ----------------------------------------------------------
# 5. .gitignore の設定
# ----------------------------------------------------------
# Claude Code関連で無視すべきファイルを設定
echo "【5】.gitignore を設定します"
echo "------------------------------------------------------------"

cat > "$DEMO_DIR/.gitignore" << 'GITIGNORE_EOF'
# Claude Code ローカル設定（個人環境固有）
.claude/settings.local.json

# 環境変数ファイル
.env
.env.local

# Python
__pycache__/
*.pyc
.venv/

# IDE
.vscode/
.idea/
GITIGNORE_EOF

echo ".gitignore を作成しました"
echo ""

# ----------------------------------------------------------
# 6. 設定ファイルの階層構造の説明
# ----------------------------------------------------------
echo "【6】設定ファイルの階層構造"
echo "============================================================"
echo ""
echo "  Claude Code の設定は以下の優先順位で読み込まれます:"
echo ""
echo "  1. エンタープライズポリシー（最優先）"
echo "     ~/.claude/enterprise-settings.json"
echo ""
echo "  2. ユーザー設定（グローバル）"
echo "     ~/.claude/settings.json"
echo ""
echo "  3. プロジェクト設定（チーム共有）"
echo "     .claude/settings.json"
echo ""
echo "  4. プロジェクトローカル設定（個人用）"
echo "     .claude/settings.local.json"
echo ""
echo "  ※ CLAUDE.md も同様に階層化できます:"
echo "     ~/.claude/CLAUDE.md      - グローバル"
echo "     ./CLAUDE.md              - プロジェクトルート"
echo "     ./src/CLAUDE.md          - サブディレクトリ"
echo ""

# ----------------------------------------------------------
# 7. 作成したファイルの確認
# ----------------------------------------------------------
echo "【7】作成したファイル一覧"
echo "------------------------------------------------------------"
echo ""
echo "プロジェクト構成:"
# tree コマンドがなくても動くように find を使用
find "$DEMO_DIR" -name ".git" -prune -o -type f -print | sort | while read -r file; do
    # プロジェクトディレクトリからの相対パスを表示
    echo "  ${file#$DEMO_DIR/}"
done
echo ""

# ----------------------------------------------------------
# 8. Claude Code の起動方法
# ----------------------------------------------------------
echo "【8】プロジェクトでの Claude Code 起動方法"
echo "============================================================"
echo ""
echo "  # プロジェクトディレクトリに移動して起動"
echo "  cd $DEMO_DIR"
echo "  claude"
echo ""
echo "  # Claude Code は起動時に以下を自動的に読み込みます:"
echo "  #   - CLAUDE.md（プロジェクトのコンテキスト）"
echo "  #   - .claude/settings.json（許可設定）"
echo "  #   - .git（リポジトリ情報）"
echo ""
echo "============================================================"
echo " デモ完了 - デモファイルは $DEMO_DIR に作成されました"
echo "============================================================"

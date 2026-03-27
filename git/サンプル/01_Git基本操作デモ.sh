#!/bin/bash
# ============================================================
# Git基本操作デモスクリプト
# ============================================================
# 学べる内容: git init, add, commit, status, log, diff の基本操作
# 実行方法: chmod +x 01_Git基本操作デモ.sh && ./01_Git基本操作デモ.sh
# 前提条件: Git がインストールされていること
# ============================================================

set -e

# --- 色の定義 ---
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RESET='\033[0m'

# --- ヘルパー関数 ---
section() {
    echo ""
    echo -e "${GREEN}========================================${RESET}"
    echo -e "${GREEN}  $1${RESET}"
    echo -e "${GREEN}========================================${RESET}"
    echo ""
}

info() {
    echo -e "${CYAN}[説明] $1${RESET}"
}

run_cmd() {
    echo -e "${YELLOW}\$ $1${RESET}"
    eval "$1"
    echo ""
}

pause() {
    echo "--- Enterキーで次のステップへ ---"
    read -r
}

# --- 作業用ディレクトリの準備 ---
WORK_DIR=$(mktemp -d /tmp/git-demo-XXXXXX)
echo "作業ディレクトリ: $WORK_DIR"
cd "$WORK_DIR"

# クリーンアップ処理（終了時に自動実行）
cleanup() {
    echo ""
    echo "作業ディレクトリを削除しています: $WORK_DIR"
    rm -rf "$WORK_DIR"
    echo "クリーンアップ完了。お疲れさまでした！"
}
trap cleanup EXIT

# ============================================================
# ステップ1: リポジトリの初期化
# ============================================================
section "ステップ1: git init - リポジトリの初期化"
info "git init でカレントディレクトリをGitリポジトリとして初期化します。"
info ".git ディレクトリが作成され、バージョン管理が始まります。"
run_cmd "git init"
run_cmd "ls -la .git/"
pause

# ============================================================
# ステップ2: Gitの初期設定（デモ用）
# ============================================================
section "ステップ2: ユーザー設定"
info "コミットに記録される名前とメールアドレスを設定します。"
info "--local を使うとこのリポジトリだけに適用されます。"
run_cmd "git config --local user.name 'デモユーザー'"
run_cmd "git config --local user.email 'demo@example.com'"
pause

# ============================================================
# ステップ3: ファイルの作成とステータス確認
# ============================================================
section "ステップ3: ファイル作成と git status"
info "新しいファイルを作成し、Gitがどう認識するか確認します。"

cat > hello.py << 'PYEOF'
# はじめてのPythonスクリプト
def greet(name):
    return f"こんにちは、{name}さん！"

if __name__ == "__main__":
    print(greet("世界"))
PYEOF

echo "hello.py を作成しました。"
echo ""
info "git status で現在の状態を確認します。"
info "まだ add していないので「Untracked files」として表示されます。"
run_cmd "git status"
pause

# ============================================================
# ステップ4: ステージングエリアへの追加
# ============================================================
section "ステップ4: git add - ステージングエリアへ追加"
info "git add でファイルをステージングエリア（インデックス）に追加します。"
info "ステージングエリアは「次のコミットに含める変更」を管理する場所です。"
run_cmd "git add hello.py"
run_cmd "git status"
pause

# ============================================================
# ステップ5: 最初のコミット
# ============================================================
section "ステップ5: git commit - 最初のコミット"
info "git commit でステージングエリアの内容を記録します。"
info "-m オプションでコミットメッセージを指定します。"
run_cmd "git commit -m 'feat: 挨拶スクリプトを追加'"
info "git log でコミット履歴を確認します。"
run_cmd "git log --oneline"
pause

# ============================================================
# ステップ6: ファイルの変更と差分確認
# ============================================================
section "ステップ6: ファイル変更と git diff"
info "ファイルを編集して、git diff で変更内容を確認します。"

cat > hello.py << 'PYEOF'
# はじめてのPythonスクリプト
import sys

def greet(name):
    return f"こんにちは、{name}さん！"

def farewell(name):
    return f"さようなら、{name}さん！"

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "世界"
    print(greet(name))
    print(farewell(name))
PYEOF

echo "hello.py を編集しました。"
echo ""
info "git diff でワーキングツリーとインデックスの差分を表示します。"
info "緑（+）が追加行、赤（-）が削除行です。"
run_cmd "git diff"
pause

# ============================================================
# ステップ7: 変更をコミット
# ============================================================
section "ステップ7: 変更のステージングとコミット"
info "git add で変更をステージングし、コミットします。"
run_cmd "git add hello.py"
info "git diff --staged でステージ済みの差分を確認できます。"
run_cmd "git diff --staged"
run_cmd "git commit -m 'feat: お別れ機能とコマンドライン引数対応を追加'"
pause

# ============================================================
# ステップ8: 複数ファイルの操作
# ============================================================
section "ステップ8: 複数ファイルの操作"
info "複数ファイルを作成し、選択的にステージングします。"

echo "# Git基本操作デモ" > README.md
echo "*.pyc" > .gitignore

info "2つのファイルを作成しました。個別に add できます。"
run_cmd "git status"
run_cmd "git add README.md .gitignore"
run_cmd "git commit -m 'docs: READMEと.gitignoreを追加'"
pause

# ============================================================
# ステップ9: コミット履歴の確認
# ============================================================
section "ステップ9: git log - 履歴の確認"
info "git log のさまざまなオプションを試します。"
echo ""
info "--- 通常のログ ---"
run_cmd "git log"
info "--- 1行表示 ---"
run_cmd "git log --oneline"
info "--- 変更されたファイル一覧付き ---"
run_cmd "git log --oneline --stat"

echo ""
echo -e "${GREEN}=== デモ完了 ===${RESET}"
echo "Git の基本操作（init, add, commit, status, log, diff）を体験しました。"
echo "次は02_ブランチ操作デモ.sh でブランチ操作を学びましょう！"

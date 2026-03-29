#!/bin/bash
# ============================================================
# ブランチ操作デモスクリプト
# ============================================================
# 学べる内容: branch, switch, merge の操作とブランチの視覚化
# 実行方法: chmod +x 02_ブランチ操作デモ.sh && ./02_ブランチ操作デモ.sh
# 前提条件: Git がインストールされていること
# ============================================================

set -e

# --- 色の定義 ---
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
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
WORK_DIR=$(mktemp -d /tmp/git-branch-demo-XXXXXX)
echo "作業ディレクトリ: $WORK_DIR"
cd "$WORK_DIR"

cleanup() {
    echo ""
    echo "作業ディレクトリを削除しています: $WORK_DIR"
    rm -rf "$WORK_DIR"
    echo "クリーンアップ完了。お疲れさまでした！"
}
trap cleanup EXIT

# --- リポジトリの初期化と初期コミット ---
git init -q
git config --local user.name "デモユーザー"
git config --local user.email "demo@example.com"

# 初期ファイルを作成
cat > app.py << 'PYEOF'
# シンプルな計算アプリ
def add(a, b):
    return a + b

if __name__ == "__main__":
    print(f"1 + 2 = {add(1, 2)}")
PYEOF

git add app.py
git commit -q -m "feat: 計算アプリの初期バージョン"

echo "初期リポジトリを準備しました。"

# ============================================================
# ステップ1: ブランチの一覧と作成
# ============================================================
section "ステップ1: ブランチの一覧確認と作成"
info "git branch でブランチの一覧を確認します。"
info "* がついているのが現在のブランチです。"
run_cmd "git branch"

info "git branch <名前> で新しいブランチを作成します。"
run_cmd "git branch feature/subtract"
run_cmd "git branch"
pause

# ============================================================
# ステップ2: ブランチの切り替え
# ============================================================
section "ステップ2: git switch - ブランチの切り替え"
info "git switch でブランチを切り替えます。"
info "（git checkout でも可能ですが、switch がモダンな方法です）"
run_cmd "git switch feature/subtract"
run_cmd "git branch"

info "feature/subtract ブランチでファイルを編集します。"

cat > app.py << 'PYEOF'
# シンプルな計算アプリ
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

if __name__ == "__main__":
    print(f"1 + 2 = {add(1, 2)}")
    print(f"5 - 3 = {subtract(5, 3)}")
PYEOF

git add app.py
git commit -q -m "feat: 引き算機能を追加"
run_cmd "git log --oneline"
pause

# ============================================================
# ステップ3: Fast-forward マージ
# ============================================================
section "ステップ3: Fast-forward マージ"
info "mainブランチに戻って、feature/subtract をマージします。"
info "mainブランチに追加コミットがないため、Fast-forwardマージになります。"
info "（ブランチポインタを前に進めるだけの単純なマージ）"

run_cmd "git switch main"
info "マージ前のmainブランチの状態:"
run_cmd "git log --oneline"

run_cmd "git merge feature/subtract"
info "マージ後のmainブランチの状態:"
run_cmd "git log --oneline"
pause

# ============================================================
# ステップ4: 3-way マージの準備
# ============================================================
section "ステップ4: 3-way マージの準備"
info "両方のブランチにコミットがある場合、3-wayマージになります。"
info "2つのブランチを並行して開発する状況を作ります。"

# feature/multiply ブランチを作成して作業
run_cmd "git switch -c feature/multiply"

cat > app.py << 'PYEOF'
# シンプルな計算アプリ
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

if __name__ == "__main__":
    print(f"1 + 2 = {add(1, 2)}")
    print(f"5 - 3 = {subtract(5, 3)}")
    print(f"3 * 4 = {multiply(3, 4)}")
PYEOF

git add app.py
git commit -q -m "feat: 掛け算機能を追加"

# mainブランチに戻って別の変更を加える
git switch -q main
echo "# 計算アプリ" > README.md
echo "四則演算を行うシンプルなアプリです。" >> README.md
git add README.md
git commit -q -m "docs: READMEを追加"

info "mainブランチにはREADME追加のコミットがあります:"
run_cmd "git log --oneline"

info "feature/multiply ブランチには掛け算追加のコミットがあります:"
run_cmd "git log --oneline feature/multiply"
pause

# ============================================================
# ステップ5: 3-way マージの実行
# ============================================================
section "ステップ5: 3-way マージの実行"
info "両ブランチにコミットがあるため、マージコミットが作成されます。"

run_cmd "git merge feature/multiply -m 'merge: feature/multiply を統合'"

info "マージ後のログをグラフで表示します:"
run_cmd "git log --oneline --graph --all"
pause

# ============================================================
# ステップ6: ブランチの削除と整理
# ============================================================
section "ステップ6: ブランチの削除と整理"
info "マージ済みのブランチは削除して整理しましょう。"
info "git branch -d でマージ済みブランチを安全に削除できます。"

run_cmd "git branch"
run_cmd "git branch -d feature/subtract"
run_cmd "git branch -d feature/multiply"
run_cmd "git branch"
pause

# ============================================================
# ステップ7: ブランチの全体像を視覚化
# ============================================================
section "ステップ7: コミット履歴の視覚化"
info "git log --graph でブランチの分岐・統合を視覚的に確認できます。"

run_cmd "git log --oneline --graph --all --decorate"

echo ""
echo -e "${GREEN}=== デモ完了 ===${RESET}"
echo ""
echo "ブランチ操作のまとめ:"
echo "  git branch <名前>       ... ブランチ作成"
echo "  git switch <名前>       ... ブランチ切り替え"
echo "  git switch -c <名前>    ... 作成と切り替えを同時に"
echo "  git merge <名前>        ... 現在のブランチに統合"
echo "  git branch -d <名前>    ... マージ済みブランチの削除"
echo ""
echo "次は03_コミット履歴解析ツール.sh で履歴の分析を学びましょう！"

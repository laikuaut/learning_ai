#!/bin/bash
# ============================================================
# Gitフック設定ツール
# ============================================================
# 学べる内容: Git Hooks の仕組みと設定方法
#   - pre-commit フックによるコミット前の自動チェック
#   - commit-msg フックによるメッセージ形式の検証
#   - フックのインストール・アンインストール方法
#
# 実行方法:
#   chmod +x 04_Gitフック設定ツール.sh
#   cd <Gitリポジトリ>
#   bash /path/to/04_Gitフック設定ツール.sh
#
# 注意: Gitリポジトリ内で実行してください
# ============================================================

# --- 色の定義 ---
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
BOLD='\033[1m'
RESET='\033[0m'

# --- メッセージ表示用関数 ---
info()    { echo -e "${CYAN}[情報] $1${RESET}"; }
success() { echo -e "${GREEN}[成功] $1${RESET}"; }
warn()    { echo -e "${YELLOW}[警告] $1${RESET}"; }
error()   { echo -e "${RED}[エラー] $1${RESET}"; }

# --- Gitリポジトリの確認 ---
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    error "Gitリポジトリ内で実行してください。"
    exit 1
fi

REPO_ROOT=$(git rev-parse --show-toplevel)
HOOKS_DIR="$REPO_ROOT/.git/hooks"

# --- pre-commit フックの内容を生成する関数 ---
generate_pre_commit() {
    cat << 'HOOKEOF'
#!/bin/bash
# pre-commit フック: デバッグ文と末尾空白をチェックする
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RESET='\033[0m'
errors=0
echo "pre-commit チェックを実行中..."
# デバッグ文の検出（console.log, print, debugger）
echo -n "  デバッグ文のチェック... "
debug_files=$(git diff --cached --name-only --diff-filter=ACM | \
    xargs grep -l "console\.log\|debugger\|print(" 2>/dev/null || true)
if [ -n "$debug_files" ]; then
    echo -e "${RED}検出！${RESET}"
    echo "$debug_files" | while read -r f; do echo "    - $f"; done
    errors=1
else
    echo -e "${GREEN}OK${RESET}"
fi
# 末尾の空白文字チェック
echo -n "  末尾の空白文字チェック... "
ws=$(git diff --cached --check 2>&1 | grep "trailing whitespace" || true)
if [ -n "$ws" ]; then
    echo -e "${YELLOW}警告（末尾に空白あり）${RESET}"
else
    echo -e "${GREEN}OK${RESET}"
fi
if [ $errors -ne 0 ]; then
    echo -e "${RED}問題が検出されました。コミットを中止します。${RESET}"
    echo "  スキップするには: git commit --no-verify"
    exit 1
fi
echo -e "${GREEN}すべてのチェックをパスしました。${RESET}"
HOOKEOF
}

# --- commit-msg フックの内容を生成する関数 ---
generate_commit_msg() {
    cat << 'HOOKEOF'
#!/bin/bash
# commit-msg フック: Conventional Commits 形式を検証する
RED='\033[0;31m'; GREEN='\033[0;32m'; RESET='\033[0m'
MSG=$(head -1 "$1")
TYPES="feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert"
if echo "$MSG" | grep -qE "^($TYPES)(\(.+\))?: .+$"; then
    echo -e "${GREEN}コミットメッセージの形式: OK${RESET}"
else
    echo -e "${RED}Conventional Commits 形式で記述してください。${RESET}"
    echo "  形式: <type>: <description>"
    echo "  例: feat: ユーザー認証機能を追加"
    echo "  例: fix: ログインエラーを修正"
    echo "  使用可能: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert"
    exit 1
fi
HOOKEOF
}

# --- フックのインストール ---
install_hook() {
    local hook_name="$1" hook_path="$HOOKS_DIR/$hook_name"
    # 既存フックがあればバックアップする
    if [ -f "$hook_path" ] && [ ! -f "${hook_path}.backup" ]; then
        cp "$hook_path" "${hook_path}.backup"
        info "既存の ${hook_name} をバックアップしました。"
    fi
    # フック生成関数を呼び出して書き込む
    case "$hook_name" in
        pre-commit) generate_pre_commit > "$hook_path" ;;
        commit-msg) generate_commit_msg > "$hook_path" ;;
    esac
    chmod +x "$hook_path"
    success "${hook_name} フックをインストールしました。"
}

# --- フックのアンインストール ---
uninstall_hook() {
    local hook_name="$1" hook_path="$HOOKS_DIR/$hook_name"
    if [ -f "$hook_path" ]; then
        rm "$hook_path"
        success "${hook_name} フックを削除しました。"
        # バックアップがあれば復元する
        if [ -f "${hook_path}.backup" ]; then
            mv "${hook_path}.backup" "$hook_path"
            info "バックアップから復元しました。"
        fi
    else
        warn "${hook_name} フックは存在しません。"
    fi
}

# --- フックの状態表示 ---
show_hooks() {
    echo ""
    echo -e "${BOLD}現在のフック状態:${RESET}"
    for hook in pre-commit commit-msg; do
        if [ -f "$HOOKS_DIR/$hook" ] && [ -x "$HOOKS_DIR/$hook" ]; then
            echo -e "  ${hook}: ${GREEN}インストール済み${RESET}"
        else
            echo -e "  ${hook}: ${YELLOW}未インストール${RESET}"
        fi
    done
    echo ""
}

# --- メインメニューのループ ---
while true; do
    echo ""
    echo -e "${GREEN}========== Gitフック設定ツール ==========${RESET}"
    echo "  リポジトリ: $REPO_ROOT"
    show_hooks
    echo "  1) pre-commit フックをインストール"
    echo "  2) commit-msg フックをインストール"
    echo "  3) フックをアンインストール"
    echo "  4) フックの状態を表示"
    echo "  0) 終了"
    echo ""
    read -r -p "  選択 [0-4]: " choice
    case "$choice" in
        1) install_hook "pre-commit" ;;
        2) install_hook "commit-msg" ;;
        3) uninstall_hook "pre-commit"; uninstall_hook "commit-msg" ;;
        4) show_hooks ;;
        0) echo "終了します。"; exit 0 ;;
        *) warn "無効な選択です。0-4 を入力してください。" ;;
    esac
done

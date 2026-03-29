#!/bin/bash
# =============================================================================
# リポジトリ管理ダッシュボード
# =============================================================================
# 学べる内容: Gitの様々な情報表示コマンドの組み合わせ
#   - git status / git log / git branch などの基本コマンド
#   - git stash list / git tag / git remote の活用
#   - ANSIエスケープコードによるターミナル出力の装飾
#
# 実行方法:
#   chmod +x 05_リポジトリ管理ダッシュボード.sh
#   cd <Gitリポジトリ>
#   bash /path/to/05_リポジトリ管理ダッシュボード.sh
#
# 注意: Gitリポジトリ内で実行してください
# =============================================================================

# --- 色とスタイルの定義 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
RESET='\033[0m'

# --- ユーティリティ関数 ---
# セクションヘッダーを色付きで表示する
section() {
    echo ""
    echo -e "${1}${BOLD}══════════════════════════════════════════${RESET}"
    echo -e "${1}${BOLD}  $2${RESET}"
    echo -e "${1}${BOLD}══════════════════════════════════════════${RESET}"
}

# --- Gitリポジトリの確認 ---
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo -e "${RED}[エラー] Gitリポジトリ内で実行してください。${RESET}"
    exit 1
fi

# --- タイトル表示 ---
echo ""
echo -e "${BLUE}${BOLD}  ╔══════════════════════════════════════════╗${RESET}"
echo -e "${BLUE}${BOLD}  ║   Git リポジトリ管理ダッシュボード      ║${RESET}"
echo -e "${BLUE}${BOLD}  ╚══════════════════════════════════════════╝${RESET}"
echo -e "  ${DIM}実行日時: $(date '+%Y-%m-%d %H:%M:%S')${RESET}"

# === セクション1: 現在のブランチとステータス ===
section "$GREEN" "現在のブランチとステータス"

# ブランチ名を取得する
current_branch=$(git branch --show-current 2>/dev/null)
[ -z "$current_branch" ] && current_branch="(デタッチドHEAD)"
echo -e "  ${BOLD}ブランチ:${RESET} ${GREEN}${current_branch}${RESET}"
echo -e "  ${BOLD}HEAD:${RESET}    $(git rev-parse --short HEAD 2>/dev/null)"

# ファイルの状態を集計して表示する
staged=$(git diff --cached --name-only 2>/dev/null | wc -l)
modified=$(git diff --name-only 2>/dev/null | wc -l)
untracked=$(git ls-files --others --exclude-standard 2>/dev/null | wc -l)
echo -e "  ${GREEN}ステージ済み: ${staged}${RESET} | ${YELLOW}変更あり: ${modified}${RESET} | ${RED}未追跡: ${untracked}${RESET}"

# === セクション2: 最近のコミット（直近5件） ===
section "$MAGENTA" "最近のコミット（直近5件）"

if git log --oneline -1 > /dev/null 2>&1; then
    git log --oneline --graph --decorate -5 2>/dev/null | while IFS= read -r line; do
        echo "  ${line}"
    done
    total=$(git rev-list --count HEAD 2>/dev/null)
    echo -e "  ${DIM}(全 ${total} コミット)${RESET}"
else
    echo -e "  ${DIM}コミット履歴がありません${RESET}"
fi

# === セクション3: ブランチ一覧（ローカル＋リモート） ===
section "$CYAN" "ブランチ一覧"

echo -e "  ${YELLOW}[ローカル]${RESET}"
git branch 2>/dev/null | while IFS= read -r branch; do
    if echo "$branch" | grep -q '^\*'; then
        echo -e "  ${GREEN}${BOLD}${branch}${RESET}"
    else
        echo "  ${branch}"
    fi
done

echo -e "  ${YELLOW}[リモート]${RESET}"
remote_branches=$(git branch -r 2>/dev/null)
if [ -n "$remote_branches" ]; then
    echo "$remote_branches" | while IFS= read -r branch; do
        echo -e "  ${DIM}${branch}${RESET}"
    done
else
    echo -e "  ${DIM}リモートブランチがありません${RESET}"
fi

# === セクション4: スタッシュ一覧 ===
section "$YELLOW" "スタッシュ一覧"

stash_list=$(git stash list 2>/dev/null)
if [ -n "$stash_list" ]; then
    echo "$stash_list" | while IFS= read -r entry; do
        echo -e "  ${YELLOW}${entry}${RESET}"
    done
else
    echo -e "  ${DIM}スタッシュはありません${RESET}"
fi

# === セクション5: タグ一覧 ===
section "$RED" "タグ一覧"

tags=$(git tag --sort=-version:refname 2>/dev/null | head -10)
if [ -n "$tags" ]; then
    echo "$tags" | while IFS= read -r tag; do
        tag_info=$(git log -1 --format="%h %s" "$tag" 2>/dev/null)
        echo -e "  ${RED}${tag}${RESET} ${DIM}-> ${tag_info}${RESET}"
    done
    total_tags=$(git tag 2>/dev/null | wc -l)
    [ "$total_tags" -gt 10 ] && echo -e "  ${DIM}... 他 $((total_tags - 10)) 件${RESET}"
else
    echo -e "  ${DIM}タグはありません${RESET}"
fi

# === セクション6: リモートリポジトリ情報 ===
section "$BLUE" "リモートリポジトリ"

remotes=$(git remote 2>/dev/null)
if [ -n "$remotes" ]; then
    echo "$remotes" | while IFS= read -r name; do
        url=$(git remote get-url "$name" 2>/dev/null)
        echo -e "  ${BOLD}${name}${RESET}: ${url}"
    done
else
    echo -e "  ${DIM}リモートが設定されていません${RESET}"
fi

# --- フッター ---
echo ""
echo -e "${DIM}══════════════════════════════════════════${RESET}"
echo -e "${DIM}  ダッシュボードの表示が完了しました${RESET}"
echo -e "${DIM}══════════════════════════════════════════${RESET}"
echo ""

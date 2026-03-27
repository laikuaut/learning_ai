#!/bin/bash
# ============================================================
# コミット履歴解析ツール
# ============================================================
# 学べる内容: git log のオプション活用、シェルスクリプトでの集計処理
# 実行方法: chmod +x 03_コミット履歴解析ツール.sh && ./03_コミット履歴解析ツール.sh
#           引数でリポジトリのパスを指定可能:
#           ./03_コミット履歴解析ツール.sh /path/to/repo
# 前提条件: Git がインストールされていること、Gitリポジトリ内で実行
# ============================================================

# --- 色の定義 ---
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
BOLD='\033[1m'
RESET='\033[0m'

# --- ヘルパー関数 ---
header() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════╗${RESET}"
    echo -e "${GREEN}║  $1${RESET}"
    echo -e "${GREEN}╚══════════════════════════════════════════╝${RESET}"
    echo ""
}

sub_header() {
    echo -e "${CYAN}── $1 ──${RESET}"
}

# --- リポジトリの確認 ---
REPO_PATH="${1:-.}"

if ! git -C "$REPO_PATH" rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo -e "${RED}エラー: $REPO_PATH はGitリポジトリではありません。${RESET}"
    echo "使い方: $0 [リポジトリのパス]"
    echo "  パスを省略するとカレントディレクトリを解析します。"
    exit 1
fi

# リポジトリのルートディレクトリを取得
REPO_ROOT=$(git -C "$REPO_PATH" rev-parse --show-toplevel)
REPO_NAME=$(basename "$REPO_ROOT")

header "Git リポジトリ解析: $REPO_NAME"
echo -e "  リポジトリパス: ${BOLD}$REPO_ROOT${RESET}"
echo ""

# ============================================================
# 1. 基本統計
# ============================================================
sub_header "1. 基本統計"

# コミット総数
TOTAL_COMMITS=$(git -C "$REPO_ROOT" rev-list --count HEAD 2>/dev/null || echo "0")
echo "  コミット総数: $TOTAL_COMMITS"

# ブランチ数
LOCAL_BRANCHES=$(git -C "$REPO_ROOT" branch | wc -l | tr -d ' ')
echo "  ローカルブランチ数: $LOCAL_BRANCHES"

# タグ数
TAG_COUNT=$(git -C "$REPO_ROOT" tag | wc -l | tr -d ' ')
echo "  タグ数: $TAG_COUNT"

# 最初のコミット日
FIRST_COMMIT=$(git -C "$REPO_ROOT" log --reverse --format="%ai" 2>/dev/null | head -1)
if [ -n "$FIRST_COMMIT" ]; then
    echo "  最初のコミット: $FIRST_COMMIT"
fi

# 最新のコミット日
LATEST_COMMIT=$(git -C "$REPO_ROOT" log -1 --format="%ai" 2>/dev/null)
if [ -n "$LATEST_COMMIT" ]; then
    echo "  最新のコミット: $LATEST_COMMIT"
fi

# 現在のブランチ
CURRENT_BRANCH=$(git -C "$REPO_ROOT" branch --show-current 2>/dev/null)
echo "  現在のブランチ: $CURRENT_BRANCH"
echo ""

# ============================================================
# 2. コントリビューター分析
# ============================================================
sub_header "2. コントリビューター別コミット数（上位10名）"

git -C "$REPO_ROOT" log --format="%aN" 2>/dev/null | \
    sort | uniq -c | sort -rn | head -10 | \
    while read -r count name; do
        # 簡易バーグラフを生成
        bar=""
        bar_len=$((count * 40 / TOTAL_COMMITS))
        if [ "$bar_len" -eq 0 ]; then
            bar_len=1
        fi
        for ((i=0; i<bar_len; i++)); do
            bar="${bar}█"
        done
        printf "  %-20s %4d件 %s\n" "$name" "$count" "$bar"
    done
echo ""

# ============================================================
# 3. 曜日別コミット分布
# ============================================================
sub_header "3. 曜日別コミット分布"

# 曜日名の配列（日本語）
declare -A DAY_NAMES
DAY_NAMES=([Mon]="月曜" [Tue]="火曜" [Wed]="水曜" [Thu]="木曜" [Fri]="金曜" [Sat]="土曜" [Sun]="日曜")

# 曜日の表示順
DAY_ORDER=("Mon" "Tue" "Wed" "Thu" "Fri" "Sat" "Sun")

# 曜日別の集計を連想配列に格納
declare -A DAY_COUNTS
for day in "${DAY_ORDER[@]}"; do
    DAY_COUNTS[$day]=0
done

while IFS= read -r day; do
    if [ -n "$day" ]; then
        current=${DAY_COUNTS[$day]:-0}
        DAY_COUNTS[$day]=$((current + 1))
    fi
done < <(git -C "$REPO_ROOT" log --format="%ad" --date=format:"%a" 2>/dev/null)

for day in "${DAY_ORDER[@]}"; do
    count=${DAY_COUNTS[$day]:-0}
    bar=""
    if [ "$TOTAL_COMMITS" -gt 0 ]; then
        bar_len=$((count * 30 / TOTAL_COMMITS))
        [ "$bar_len" -eq 0 ] && [ "$count" -gt 0 ] && bar_len=1
        for ((i=0; i<bar_len; i++)); do
            bar="${bar}▓"
        done
    fi
    printf "  %s: %4d件 %s\n" "${DAY_NAMES[$day]}" "$count" "$bar"
done
echo ""

# ============================================================
# 4. 時間帯別コミット分布
# ============================================================
sub_header "4. 時間帯別コミット分布"

declare -A HOUR_COUNTS
for ((h=0; h<24; h++)); do
    HOUR_COUNTS[$h]=0
done

while IFS= read -r hour; do
    if [ -n "$hour" ]; then
        # 先頭のゼロを除去して数値として扱う
        h=$((10#$hour))
        current=${HOUR_COUNTS[$h]:-0}
        HOUR_COUNTS[$h]=$((current + 1))
    fi
done < <(git -C "$REPO_ROOT" log --format="%ad" --date=format:"%H" 2>/dev/null)

for ((h=0; h<24; h++)); do
    count=${HOUR_COUNTS[$h]:-0}
    bar=""
    if [ "$TOTAL_COMMITS" -gt 0 ] && [ "$count" -gt 0 ]; then
        bar_len=$((count * 30 / TOTAL_COMMITS))
        [ "$bar_len" -eq 0 ] && bar_len=1
        for ((i=0; i<bar_len; i++)); do
            bar="${bar}░"
        done
    fi
    printf "  %02d時: %4d件 %s\n" "$h" "$count" "$bar"
done
echo ""

# ============================================================
# 5. 変更が多いファイル（上位10件）
# ============================================================
sub_header "5. 変更頻度が高いファイル（上位10件）"

git -C "$REPO_ROOT" log --pretty=format: --name-only 2>/dev/null | \
    sed '/^$/d' | sort | uniq -c | sort -rn | head -10 | \
    while read -r count filepath; do
        printf "  %4d回変更: %s\n" "$count" "$filepath"
    done
echo ""

# ============================================================
# 6. 直近のコミット
# ============================================================
sub_header "6. 直近のコミット（最新5件）"

git -C "$REPO_ROOT" log --oneline --format="  %C(yellow)%h%C(reset) %C(green)%ad%C(reset) %s (%an)" \
    --date=format:"%Y-%m-%d %H:%M" -5 2>/dev/null
echo ""

# --- フッター ---
echo -e "${GREEN}╔══════════════════════════════════════════╗${RESET}"
echo -e "${GREEN}║  解析完了                                ║${RESET}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${RESET}"
echo ""
echo "ヒント: 特定の期間を解析するには git log に --since/--until を使います"
echo "  例: git log --since='2024-01-01' --until='2024-12-31' --oneline"

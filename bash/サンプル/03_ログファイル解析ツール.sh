#!/usr/bin/env bash
# ============================================================
# ログファイル解析ツール
# ============================================================
# 【学べる内容】
#   - テキスト処理（grep, awk, sort, uniq, cut）
#   - 連想配列（declare -A）の使い方
#   - ループ（for, while）によるデータ集計
#   - パイプラインを使った複雑なデータ処理
#   - ヒアドキュメントによるサンプルデータ生成
#
# 【実行方法】
#   chmod +x 03_ログファイル解析ツール.sh
#   ./03_ログファイル解析ツール.sh            # サンプルデータで実行
#   ./03_ログファイル解析ツール.sh access.log  # 既存ログを解析
# ============================================================
set -euo pipefail

# --- 色の定義 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

LOG_FILE=""
TEMP_LOG=""

# 区切り線を出力する
separator() {
    printf '%60s\n' '' | tr ' ' '-'
}

# サンプルのアクセスログを生成する
generate_sample_log() {
    TEMP_LOG=$(mktemp /tmp/sample_access_log.XXXXXX)
    # クリーンアップ用トラップを設定する
    trap 'rm -f "$TEMP_LOG"' EXIT

    echo -e "${CYAN}サンプルログを生成しています...${RESET}"

    local ips=("192.168.1.10" "192.168.1.20" "10.0.0.5" "172.16.0.100" "203.0.113.50" "198.51.100.25")
    local paths=("/" "/index.html" "/about" "/api/users" "/api/products" "/login" "/dashboard" "/images/logo.png" "/css/style.css" "/js/app.js")
    local codes=("200" "200" "200" "200" "200" "301" "304" "403" "404" "404" "500")
    local hours=("08" "09" "09" "10" "10" "10" "11" "11" "12" "13" "13" "14" "14" "14" "15" "15" "16" "17" "18" "19")

    for i in $(seq 1 100); do
        local ip="${ips[$((RANDOM % ${#ips[@]}))]}"
        local path="${paths[$((RANDOM % ${#paths[@]}))]}"
        local code="${codes[$((RANDOM % ${#codes[@]}))]}"
        local hour="${hours[$((RANDOM % ${#hours[@]}))]}"
        local minute=$(printf '%02d' $((RANDOM % 60)))
        local second=$(printf '%02d' $((RANDOM % 60)))
        local size=$((RANDOM % 50000 + 100))
        # Apache Combined Log Format 風の出力
        echo "${ip} - - [15/Mar/2026:${hour}:${minute}:${second} +0900] \"GET ${path} HTTP/1.1\" ${code} ${size}"
    done > "$TEMP_LOG"

    LOG_FILE="$TEMP_LOG"
    echo -e "${GREEN}100件のサンプルログを生成しました。${RESET}"
}

# 基本統計を表示する
analyze_basic() {
    echo ""
    echo -e "${BOLD}${CYAN}[1] 基本統計${RESET}"
    separator

    local total
    total=$(wc -l < "$LOG_FILE")
    printf "  %-25s : %s 件\n" "総リクエスト数" "$total"

    local unique_ips
    unique_ips=$(awk '{print $1}' "$LOG_FILE" | sort -u | wc -l)
    printf "  %-25s : %s\n" "ユニークIPアドレス数" "$unique_ips"

    local unique_paths
    unique_paths=$(awk '{print $7}' "$LOG_FILE" | sort -u | wc -l)
    printf "  %-25s : %s\n" "ユニークURL数" "$unique_paths"
}

# ステータスコード別集計を表示する
analyze_status_codes() {
    echo ""
    echo -e "${BOLD}${CYAN}[2] ステータスコード別集計${RESET}"
    separator

    local total
    total=$(wc -l < "$LOG_FILE")

    printf "  %-12s  %-8s  %-8s  %s\n" "ステータス" "件数" "割合" "状態"
    printf "  %-12s  %-8s  %-8s  %s\n" "------------" "--------" "--------" "--------"

    awk '{print $9}' "$LOG_FILE" | sort | uniq -c | sort -rn | while read -r count code; do
        local pct=$(( count * 100 / total ))
        local status_text=""
        case "$code" in
            200) status_text="OK" ;;
            301) status_text="リダイレクト" ;;
            304) status_text="キャッシュ" ;;
            403) status_text="アクセス拒否" ;;
            404) status_text="未検出" ;;
            500) status_text="サーバーエラー" ;;
            *)   status_text="その他" ;;
        esac
        printf "  %-12s  %-8s  %-7s%%  %s\n" "$code" "$count" "$pct" "$status_text"
    done

    # エラー率を計算する（4xx + 5xx）
    local errors
    errors=$(awk '$9 ~ /^[45]/' "$LOG_FILE" | wc -l)
    local error_rate=$(( errors * 100 / total ))
    echo ""
    if [[ $error_rate -gt 10 ]]; then
        echo -e "  ${RED}エラー率: ${error_rate}% (${errors}/${total}) ⚠ 要確認${RESET}"
    else
        echo -e "  ${GREEN}エラー率: ${error_rate}% (${errors}/${total})${RESET}"
    fi
}

# IPアドレス別アクセスランキングを表示する
analyze_ip_ranking() {
    echo ""
    echo -e "${BOLD}${CYAN}[3] IPアドレス別アクセス数 Top5${RESET}"
    separator

    printf "  %-5s  %-20s  %s\n" "順位" "IPアドレス" "アクセス数"
    printf "  %-5s  %-20s  %s\n" "-----" "--------------------" "----------"

    local rank=1
    awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -5 | while read -r count ip; do
        printf "  %-5s  %-20s  %s 件\n" "${rank}." "$ip" "$count"
        ((rank++))
    done
}

# URL 別アクセスランキングを表示する
analyze_url_ranking() {
    echo ""
    echo -e "${BOLD}${CYAN}[4] URL別アクセス数 Top5${RESET}"
    separator

    printf "  %-5s  %-30s  %s\n" "順位" "URL" "アクセス数"
    printf "  %-5s  %-30s  %s\n" "-----" "------------------------------" "----------"

    local rank=1
    awk '{print $7}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -5 | while read -r count url; do
        printf "  %-5s  %-30s  %s 件\n" "${rank}." "$url" "$count"
        ((rank++))
    done
}

# 時間帯別アクセス数を表示する
analyze_hourly() {
    echo ""
    echo -e "${BOLD}${CYAN}[5] 時間帯別アクセス数${RESET}"
    separator

    # 時間帯ごとのアクセス数を集計する
    declare -A hourly_counts
    for h in $(seq -w 0 23); do
        hourly_counts[$h]=0
    done

    while IFS= read -r line; do
        local hour
        hour=$(echo "$line" | grep -oP '\d{2}:\d{2}:\d{2}' | head -1 | cut -d':' -f1)
        if [[ -n "$hour" ]]; then
            hourly_counts[$hour]=$(( ${hourly_counts[$hour]:-0} + 1 ))
        fi
    done < "$LOG_FILE"

    local max_count=1
    for h in "${!hourly_counts[@]}"; do
        if [[ ${hourly_counts[$h]} -gt $max_count ]]; then
            max_count=${hourly_counts[$h]}
        fi
    done

    for h in $(seq -w 0 23); do
        local count=${hourly_counts[$h]:-0}
        local bar_len=$(( count * 30 / max_count ))
        local bar=""
        for ((i = 0; i < bar_len; i++)); do
            bar+="█"
        done
        printf "  %s時  %3d件  %s\n" "$h" "$count" "$bar"
    done
}

# --- メイン処理 ---
echo -e "${BOLD}${CYAN}"
echo "  ╔══════════════════════════════════╗"
echo "  ║     ログファイル解析ツール       ║"
echo "  ╚══════════════════════════════════╝"
echo -e "${RESET}"

if [[ $# -ge 1 && -f "$1" ]]; then
    LOG_FILE="$1"
    echo -e "${GREEN}ログファイルを読み込みました: ${LOG_FILE}${RESET}"
else
    if [[ $# -ge 1 ]]; then
        echo -e "${YELLOW}ファイルが見つかりません: $1${RESET}"
        echo -e "${YELLOW}サンプルデータで実行します。${RESET}"
    fi
    generate_sample_log
fi

analyze_basic
analyze_status_codes
analyze_ip_ranking
analyze_url_ranking
analyze_hourly

echo ""
echo -e "${GREEN}解析が完了しました。${RESET}"

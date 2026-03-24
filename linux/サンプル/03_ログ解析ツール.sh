#!/bin/bash
# ============================================================================
# 03_ログ解析ツール.sh
# ============================================================================
# 学べる内容:
#   - awk, sort, uniq, head を組み合わせたテキスト処理
#   - Apache/nginx のアクセスログの構造と解析方法
#   - case 文を使ったメニュー形式のスクリプト
#   - 関数の分割と再利用
#   - ログ解析の実務テクニック
#
# 実行方法:
#   1. chmod +x 03_ログ解析ツール.sh
#   2. ./03_ログ解析ツール.sh [ログファイルパス]
#      例: ./03_ログ解析ツール.sh /var/log/nginx/access.log
#
#   ※ テスト用のサンプルログを自動生成する機能もあります
#      ./03_ログ解析ツール.sh --generate-sample
#
# 動作説明:
#   Apache/nginx の Combined Log Format のアクセスログを解析し、
#   IPアドレス別アクセス数、ステータスコード集計、人気URL等を表示します。
# ============================================================================

set -euo pipefail

# --- サンプルログの生成 ---
generate_sample_log() {
    local sample_file="sample_access.log"

    echo "サンプルログファイルを生成しています: $sample_file"

    # サンプルデータの生成
    cat << 'SAMPLEEOF' > "$sample_file"
192.168.1.50 - - [20/Mar/2024:10:15:23 +0900] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
203.0.113.100 - - [20/Mar/2024:10:15:24 +0900] "GET /about.html HTTP/1.1" 200 5678 "-" "Mozilla/5.0"
192.168.1.50 - - [20/Mar/2024:10:15:25 +0900] "POST /api/users HTTP/1.1" 201 89 "-" "curl/7.68.0"
198.51.100.25 - - [20/Mar/2024:10:15:26 +0900] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
192.168.1.50 - - [20/Mar/2024:10:15:27 +0900] "GET /style.css HTTP/1.1" 200 456 "-" "Mozilla/5.0"
203.0.113.100 - - [20/Mar/2024:10:15:28 +0900] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
10.0.0.5 - - [20/Mar/2024:10:16:00 +0900] "GET /admin/login HTTP/1.1" 302 0 "-" "Mozilla/5.0"
192.168.1.50 - - [20/Mar/2024:10:16:01 +0900] "GET /images/logo.png HTTP/1.1" 200 8901 "-" "Mozilla/5.0"
203.0.113.100 - - [20/Mar/2024:10:16:02 +0900] "GET /api/data HTTP/1.1" 200 2345 "-" "curl/7.68.0"
198.51.100.25 - - [20/Mar/2024:10:16:03 +0900] "GET /nonexistent HTTP/1.1" 404 178 "-" "Mozilla/5.0"
192.168.1.50 - - [20/Mar/2024:10:16:04 +0900] "GET /about.html HTTP/1.1" 200 5678 "-" "Mozilla/5.0"
10.0.0.5 - - [20/Mar/2024:10:16:05 +0900] "POST /api/login HTTP/1.1" 200 345 "-" "Mozilla/5.0"
203.0.113.100 - - [20/Mar/2024:10:16:06 +0900] "GET /style.css HTTP/1.1" 304 0 "-" "Mozilla/5.0"
192.168.1.50 - - [20/Mar/2024:10:16:07 +0900] "DELETE /api/users/5 HTTP/1.1" 403 67 "-" "curl/7.68.0"
198.51.100.25 - - [20/Mar/2024:10:16:08 +0900] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
10.0.0.5 - - [20/Mar/2024:10:17:00 +0900] "GET /dashboard HTTP/1.1" 200 3456 "-" "Mozilla/5.0"
192.168.1.50 - - [20/Mar/2024:10:17:01 +0900] "GET /api/status HTTP/1.1" 500 123 "-" "curl/7.68.0"
203.0.113.100 - - [20/Mar/2024:10:17:02 +0900] "GET /contact.html HTTP/1.1" 200 4567 "-" "Mozilla/5.0"
10.0.0.5 - - [20/Mar/2024:10:17:03 +0900] "PUT /api/settings HTTP/1.1" 200 89 "-" "curl/7.68.0"
192.168.1.50 - - [20/Mar/2024:10:17:04 +0900] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
SAMPLEEOF

    echo "サンプルログを生成しました: $sample_file ($(wc -l < "$sample_file") 行)"
    echo ""
    echo "解析するには: $0 $sample_file"
}

# --- 解析関数 ---

# セクションヘッダー
print_section() {
    echo ""
    echo "=========================================="
    echo "  $1"
    echo "=========================================="
}

# 基本統計
analyze_basic_stats() {
    local logfile="$1"
    print_section "基本統計"

    local total_requests
    total_requests=$(wc -l < "$logfile")
    echo "  総リクエスト数: $total_requests"

    local unique_ips
    unique_ips=$(awk '{print $1}' "$logfile" | sort -u | wc -l)
    echo "  ユニークIP数: $unique_ips"

    local unique_urls
    unique_urls=$(awk '{print $7}' "$logfile" | sort -u | wc -l)
    echo "  ユニークURL数: $unique_urls"

    # 合計転送量
    local total_bytes
    total_bytes=$(awk '{sum += $10} END {print sum}' "$logfile" 2>/dev/null || echo "0")
    if [ "$total_bytes" -gt 1048576 ]; then
        echo "  合計転送量: $((total_bytes / 1048576)) MB"
    elif [ "$total_bytes" -gt 1024 ]; then
        echo "  合計転送量: $((total_bytes / 1024)) KB"
    else
        echo "  合計転送量: $total_bytes bytes"
    fi
}

# IPアドレス別アクセスランキング
analyze_top_ips() {
    local logfile="$1"
    local top_n="${2:-10}"
    print_section "IPアドレス別アクセス数 (トップ $top_n)"

    printf "  %-8s  %-18s\n" "件数" "IPアドレス"
    printf "  %-8s  %-18s\n" "--------" "------------------"
    awk '{print $1}' "$logfile" | sort | uniq -c | sort -rn | head -n "$top_n" | \
        awk '{printf "  %-8s  %-18s\n", $1, $2}'
}

# ステータスコード集計
analyze_status_codes() {
    local logfile="$1"
    print_section "ステータスコード別集計"

    printf "  %-8s  %-6s  %-20s\n" "件数" "コード" "意味"
    printf "  %-8s  %-6s  %-20s\n" "--------" "------" "--------------------"

    awk '{print $9}' "$logfile" | sort | uniq -c | sort -rn | while read -r count code; do
        local meaning
        case "$code" in
            200) meaning="OK（成功）" ;;
            201) meaning="Created（作成成功）" ;;
            301) meaning="Moved Permanently（恒久的転送）" ;;
            302) meaning="Found（一時的転送）" ;;
            304) meaning="Not Modified（未変更）" ;;
            400) meaning="Bad Request（不正なリクエスト）" ;;
            401) meaning="Unauthorized（認証エラー）" ;;
            403) meaning="Forbidden（アクセス拒否）" ;;
            404) meaning="Not Found（未発見）" ;;
            500) meaning="Internal Server Error（サーバーエラー）" ;;
            502) meaning="Bad Gateway" ;;
            503) meaning="Service Unavailable" ;;
            *) meaning="その他" ;;
        esac
        printf "  %-8s  %-6s  %-20s\n" "$count" "$code" "$meaning"
    done
}

# 人気URL ランキング
analyze_top_urls() {
    local logfile="$1"
    local top_n="${2:-10}"
    print_section "人気URL ランキング (トップ $top_n)"

    printf "  %-8s  %s\n" "件数" "URL"
    printf "  %-8s  %s\n" "--------" "--------------------"
    awk '{print $7}' "$logfile" | sort | uniq -c | sort -rn | head -n "$top_n" | \
        awk '{printf "  %-8s  %s\n", $1, $2}'
}

# エラー分析（4xx, 5xx）
analyze_errors() {
    local logfile="$1"
    print_section "エラー分析 (4xx/5xx)"

    local error_count
    error_count=$(awk '$9 >= 400' "$logfile" | wc -l)
    local total_count
    total_count=$(wc -l < "$logfile")

    echo "  エラー件数: $error_count / $total_count ($(( error_count * 100 / total_count ))%)"
    echo ""

    if [ "$error_count" -gt 0 ]; then
        echo "  [エラー発生URL]"
        printf "  %-6s  %-8s  %s\n" "コード" "件数" "URL"
        printf "  %-6s  %-8s  %s\n" "------" "--------" "--------------------"
        awk '$9 >= 400 {print $9, $7}' "$logfile" | sort | uniq -c | sort -rn | \
            awk '{printf "  %-6s  %-8s  %s\n", $2, $1, $3}'
    else
        echo "  エラーはありません"
    fi
}

# HTTPメソッド別集計
analyze_methods() {
    local logfile="$1"
    print_section "HTTPメソッド別集計"

    printf "  %-8s  %s\n" "件数" "メソッド"
    printf "  %-8s  %s\n" "--------" "----------"
    awk '{
        # "GET のようにクォートがついているので除去
        method = $6
        gsub(/"/, "", method)
        print method
    }' "$logfile" | sort | uniq -c | sort -rn | \
        awk '{printf "  %-8s  %s\n", $1, $2}'
}

# --- メイン処理 ---
main() {
    # 引数チェック
    if [ $# -eq 0 ]; then
        echo "使い方: $0 <ログファイルパス>"
        echo "        $0 --generate-sample  (サンプルログを生成)"
        exit 1
    fi

    # サンプルログ生成モード
    if [ "$1" = "--generate-sample" ]; then
        generate_sample_log
        exit 0
    fi

    local logfile="$1"

    # ファイルの存在確認
    if [ ! -f "$logfile" ]; then
        echo "エラー: ファイルが見つかりません: $logfile" >&2
        exit 1
    fi

    echo "╔══════════════════════════════════════════╗"
    echo "║         アクセスログ解析レポート           ║"
    echo "║   $(date '+%Y-%m-%d %H:%M:%S')              ║"
    echo "╚══════════════════════════════════════════╝"
    echo "  対象ファイル: $logfile"

    # 各解析を実行
    analyze_basic_stats "$logfile"
    analyze_top_ips "$logfile" 10
    analyze_status_codes "$logfile"
    analyze_top_urls "$logfile" 10
    analyze_errors "$logfile"
    analyze_methods "$logfile"

    echo ""
    echo "=========================================="
    echo "  解析完了"
    echo "=========================================="
}

main "$@"

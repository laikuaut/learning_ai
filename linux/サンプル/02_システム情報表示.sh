#!/bin/bash
# ============================================================================
# 02_システム情報表示.sh
# ============================================================================
# 学べる内容:
#   - システム情報を取得する各種コマンドの使い方
#     (uname, hostname, uptime, free, df, lscpu, nproc)
#   - 関数の定義と呼び出し
#   - printf によるフォーマット出力
#   - コマンドの出力を変数に格納する方法
#   - awk を使ったテキスト処理
#
# 実行方法:
#   1. chmod +x 02_システム情報表示.sh
#   2. ./02_システム情報表示.sh
#
# 動作説明:
#   CPU、メモリ、ディスク、ネットワーク、OS の情報を一覧表示します。
#   サーバーの状態を素早く確認したいときに便利なスクリプトです。
# ============================================================================

set -euo pipefail

# --- 表示用の関数 ---

# セクションヘッダーを表示
print_header() {
    local title="$1"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  $title"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# キーと値のペアを表示
print_item() {
    printf "  %-20s : %s\n" "$1" "$2"
}

# --- 各情報の取得関数 ---

# OS情報を表示
show_os_info() {
    print_header "OS 情報"

    # OS名の取得
    if [ -f /etc/os-release ]; then
        local os_name
        os_name=$(grep "^PRETTY_NAME" /etc/os-release | cut -d'"' -f2)
        print_item "OS" "$os_name"
    fi

    print_item "カーネル" "$(uname -r)"
    print_item "アーキテクチャ" "$(uname -m)"
    print_item "ホスト名" "$(hostname)"
    print_item "現在の日時" "$(date '+%Y-%m-%d %H:%M:%S %Z')"

    # 稼働時間
    local uptime_info
    uptime_info=$(uptime -p 2>/dev/null || uptime)
    print_item "稼働時間" "$uptime_info"
}

# CPU情報を表示
show_cpu_info() {
    print_header "CPU 情報"

    # CPU名の取得
    if [ -f /proc/cpuinfo ]; then
        local cpu_model
        cpu_model=$(grep "model name" /proc/cpuinfo | head -1 | cut -d':' -f2 | sed 's/^ *//')
        print_item "モデル" "$cpu_model"
    fi

    print_item "コア数" "$(nproc)"

    # ロードアベレージ
    local load_avg
    load_avg=$(uptime | awk -F'load average:' '{print $2}' | sed 's/^ *//')
    print_item "ロードアベレージ" "$load_avg"

    # CPU使用率（簡易版）
    if command -v top > /dev/null 2>&1; then
        local cpu_usage
        cpu_usage=$(top -bn1 2>/dev/null | grep "Cpu(s)" | awk '{print $2}' || echo "取得不可")
        print_item "CPU使用率" "${cpu_usage}%"
    fi
}

# メモリ情報を表示
show_memory_info() {
    print_header "メモリ情報"

    if command -v free > /dev/null 2>&1; then
        # free コマンドの出力を解析
        local mem_total mem_used mem_available mem_usage_pct
        mem_total=$(free -h | awk '/^Mem:/ {print $2}')
        mem_used=$(free -h | awk '/^Mem:/ {print $3}')
        mem_available=$(free -h | awk '/^Mem:/ {print $7}')

        # 使用率の計算（バイト単位で取得して計算）
        local total_kb used_kb
        total_kb=$(free | awk '/^Mem:/ {print $2}')
        used_kb=$(free | awk '/^Mem:/ {print $3}')
        if [ "$total_kb" -gt 0 ]; then
            mem_usage_pct=$((used_kb * 100 / total_kb))
        else
            mem_usage_pct=0
        fi

        print_item "合計" "$mem_total"
        print_item "使用中" "$mem_used"
        print_item "利用可能" "$mem_available"
        print_item "使用率" "${mem_usage_pct}%"

        # Swap情報
        local swap_total swap_used
        swap_total=$(free -h | awk '/^Swap:/ {print $2}')
        swap_used=$(free -h | awk '/^Swap:/ {print $3}')
        print_item "Swap合計" "$swap_total"
        print_item "Swap使用中" "$swap_used"
    else
        print_item "メモリ情報" "free コマンドが利用できません"
    fi
}

# ディスク情報を表示
show_disk_info() {
    print_header "ディスク情報"

    echo ""
    printf "  %-20s %-8s %-8s %-8s %-6s\n" "マウントポイント" "合計" "使用済" "空き" "使用率"
    printf "  %-20s %-8s %-8s %-8s %-6s\n" "--------------------" "--------" "--------" "--------" "------"

    df -h | awk 'NR>1 && $1 !~ /^tmpfs/ && $1 !~ /^devtmpfs/ && $1 !~ /^udev/ {
        printf "  %-20s %-8s %-8s %-8s %-6s", $6, $2, $3, $4, $5
        # 使用率が80%以上なら警告マークを付ける
        usage = $5 + 0
        if (usage >= 80) {
            printf "  [!警告!]"
        }
        printf "\n"
    }'
}

# ネットワーク情報を表示
show_network_info() {
    print_header "ネットワーク情報"

    # IPアドレスの取得
    if command -v ip > /dev/null 2>&1; then
        ip -4 addr show | awk '/inet / && !/127.0.0.1/ {
            split($2, addr, "/")
            printf "  %-20s : %s\n", $NF, addr[1]
        }'
    fi

    # デフォルトゲートウェイ
    if command -v ip > /dev/null 2>&1; then
        local gateway
        gateway=$(ip route show default 2>/dev/null | awk '{print $3}' | head -1)
        if [ -n "$gateway" ]; then
            print_item "デフォルトGW" "$gateway"
        fi
    fi

    # DNSサーバー
    if [ -f /etc/resolv.conf ]; then
        local dns_servers
        dns_servers=$(grep "^nameserver" /etc/resolv.conf | awk '{print $2}' | tr '\n' ', ' | sed 's/,$//')
        if [ -n "$dns_servers" ]; then
            print_item "DNSサーバー" "$dns_servers"
        fi
    fi
}

# ログイン中のユーザーを表示
show_user_info() {
    print_header "ログインユーザー"

    if command -v who > /dev/null 2>&1; then
        local user_count
        user_count=$(who | wc -l)
        print_item "ログイン数" "${user_count} セッション"
        echo ""
        who | awk '{printf "  %-12s %-8s %s %s\n", $1, $2, $3, $4}'
    fi
}

# --- メイン処理 ---
main() {
    echo "╔══════════════════════════════════════════╗"
    echo "║         システム情報レポート              ║"
    echo "║   $(date '+%Y-%m-%d %H:%M:%S')              ║"
    echo "╚══════════════════════════════════════════╝"

    show_os_info
    show_cpu_info
    show_memory_info
    show_disk_info
    show_network_info
    show_user_info

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  レポート生成完了"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

main

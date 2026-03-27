#!/usr/bin/env bash
# ============================================================
# システム情報レポート生成ツール
# ============================================================
# 【学べる内容】
#   - コマンド置換 $() による値の取得
#   - パイプ（|）を使ったコマンド連携
#   - 関数によるコードの整理
#   - リダイレクト（>、>>、tee）によるファイル出力
#   - printf による整形出力
#
# 【実行方法】
#   chmod +x 02_システム情報レポート.sh
#   ./02_システム情報レポート.sh            # 画面に表示
#   ./02_システム情報レポート.sh -o report.txt  # ファイルにも保存
#   ./02_システム情報レポート.sh -h          # ヘルプ表示
# ============================================================
set -euo pipefail

# --- 色の定義 ---
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
RESET='\033[0m'

OUTPUT_FILE=""

# ヘルプを表示する
show_help() {
    echo "使い方: $0 [オプション]"
    echo ""
    echo "オプション:"
    echo "  -o <ファイル>  レポートをファイルに保存する"
    echo "  -h             このヘルプを表示する"
}

# 区切り線を出力する
separator() {
    printf '%60s\n' '' | tr ' ' '='
}

# セクションヘッダーを出力する
section() {
    local title="$1"
    echo ""
    separator
    printf "  %s\n" "$title"
    separator
}

# OS 情報を表示する
report_os() {
    section "OS 情報"
    printf "  %-20s : %s\n" "ホスト名" "$(hostname)"
    printf "  %-20s : %s\n" "カーネル" "$(uname -r)"
    printf "  %-20s : %s\n" "アーキテクチャ" "$(uname -m)"
    printf "  %-20s : %s\n" "OS" "$(uname -o)"
    if [[ -f /etc/os-release ]]; then
        local pretty_name
        pretty_name=$(grep '^PRETTY_NAME=' /etc/os-release | cut -d'"' -f2)
        printf "  %-20s : %s\n" "ディストリビューション" "${pretty_name:-不明}"
    fi
    printf "  %-20s : %s\n" "現在時刻" "$(date '+%Y-%m-%d %H:%M:%S')"
    printf "  %-20s : %s\n" "稼働時間" "$(uptime -p 2>/dev/null || uptime | sed 's/.*up //' | sed 's/,.*//')"
}

# CPU 情報を表示する
report_cpu() {
    section "CPU 情報"
    if [[ -f /proc/cpuinfo ]]; then
        local model
        model=$(grep 'model name' /proc/cpuinfo | head -1 | cut -d':' -f2 | xargs)
        local cores
        cores=$(grep -c '^processor' /proc/cpuinfo)
        printf "  %-20s : %s\n" "モデル" "${model:-不明}"
        printf "  %-20s : %s\n" "コア数" "${cores}"
    else
        printf "  %-20s : %s\n" "情報" "取得できませんでした"
    fi
    # ロードアベレージを表示する
    local loadavg
    loadavg=$(cat /proc/loadavg 2>/dev/null | cut -d' ' -f1-3 || echo "不明")
    printf "  %-20s : %s\n" "ロードアベレージ" "${loadavg}"
}

# メモリ情報を表示する
report_memory() {
    section "メモリ情報"
    if command -v free &>/dev/null; then
        echo ""
        # free コマンドの出力を整形して表示する
        free -h | while IFS= read -r line; do
            printf "    %s\n" "$line"
        done
        echo ""
        # 使用率を計算して表示する
        local total used
        total=$(free | awk '/^Mem:/ {print $2}')
        used=$(free | awk '/^Mem:/ {print $3}')
        if [[ "$total" -gt 0 ]]; then
            local pct=$(( used * 100 / total ))
            printf "  %-20s : %d%%\n" "メモリ使用率" "$pct"
            # 使用率のバーグラフを表示する
            local bar=""
            local filled=$(( pct / 5 ))
            for ((i = 0; i < 20; i++)); do
                if [[ $i -lt $filled ]]; then
                    bar+="█"
                else
                    bar+="░"
                fi
            done
            printf "  %-20s : [%s] %d%%\n" "使用状況" "$bar" "$pct"
        fi
    else
        printf "  %-20s\n" "free コマンドが見つかりません"
    fi
}

# ディスク使用量を表示する
report_disk() {
    section "ディスク使用量"
    echo ""
    printf "    %-30s %6s %6s %6s %6s\n" "マウントポイント" "容量" "使用" "空き" "使用率"
    printf "    %-30s %6s %6s %6s %6s\n" "------------------------------" "------" "------" "------" "------"
    # 物理ディスクのみ表示する（tmpfs 等を除外）
    df -h --type=ext4 --type=xfs --type=btrfs --type=overlay 2>/dev/null | tail -n +2 | while read -r fs size used avail pct mount; do
        printf "    %-30s %6s %6s %6s %6s\n" "$mount" "$size" "$used" "$avail" "$pct"
    done
    # 上記で何も出力されない場合のフォールバック
    if ! df -h --type=ext4 --type=xfs --type=btrfs --type=overlay &>/dev/null; then
        df -h 2>/dev/null | grep '^/' | while read -r fs size used avail pct mount; do
            printf "    %-30s %6s %6s %6s %6s\n" "$mount" "$size" "$used" "$avail" "$pct"
        done
    fi
}

# ネットワーク情報を表示する
report_network() {
    section "ネットワーク情報"
    # IP アドレスを表示する
    if command -v ip &>/dev/null; then
        ip -4 addr show 2>/dev/null | grep 'inet ' | while read -r _ addr _ _ _ iface; do
            printf "  %-20s : %s\n" "$iface" "$addr"
        done
    elif command -v hostname &>/dev/null; then
        printf "  %-20s : %s\n" "IPアドレス" "$(hostname -I 2>/dev/null || echo '不明')"
    fi
    # DNS サーバーを表示する
    if [[ -f /etc/resolv.conf ]]; then
        local dns
        dns=$(grep '^nameserver' /etc/resolv.conf | head -1 | awk '{print $2}')
        printf "  %-20s : %s\n" "DNSサーバー" "${dns:-不明}"
    fi
}

# レポートのヘッダーを出力する
report_header() {
    echo ""
    echo -e "${BOLD}${CYAN}  システム情報レポート${RESET}"
    echo -e "  生成日時: $(date '+%Y-%m-%d %H:%M:%S')"
}

# --- オプション解析 ---
while getopts ":o:h" opt; do
    case "$opt" in
        o) OUTPUT_FILE="$OPTARG" ;;
        h) show_help; exit 0 ;;
        *) echo "不明なオプション: -${OPTARG}"; show_help; exit 1 ;;
    esac
done

# --- メイン処理 ---
generate_report() {
    report_header
    report_os
    report_cpu
    report_memory
    report_disk
    report_network
    echo ""
    separator
    echo "  レポート終了"
    separator
    echo ""
}

if [[ -n "$OUTPUT_FILE" ]]; then
    # ファイルにも保存する（tee で画面とファイルの両方に出力）
    generate_report | tee "$OUTPUT_FILE"
    echo -e "${GREEN}レポートを保存しました: ${OUTPUT_FILE}${RESET}"
else
    generate_report
fi

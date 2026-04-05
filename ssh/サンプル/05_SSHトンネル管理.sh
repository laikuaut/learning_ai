#!/bin/bash
# ============================================================================
# 05_SSHトンネル管理.sh
# ============================================================================
# 学べる内容:
#   - SSHポートフォワーディング（ローカル/リモート/ダイナミック）
#   - バックグラウンドプロセスの管理
#   - PIDファイルによるプロセス管理パターン
#   - シェルスクリプトでの配列操作
#
# 実行方法:
#   1. chmod +x 05_SSHトンネル管理.sh
#   2. ./05_SSHトンネル管理.sh
#
# 動作説明:
#   SSHトンネル（ポートフォワーディング）の作成・一覧表示・停止を
#   対話的に管理できるツールです。
# ============================================================================

set -euo pipefail

# --- 定数 ---
PID_DIR="$HOME/.ssh/tunnels"

# --- 色の定義 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# --- ユーティリティ ---
print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}[OK] $1${NC}"
}

print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

# --- PIDディレクトリの確認 ---
ensure_pid_dir() {
    if [ ! -d "$PID_DIR" ]; then
        mkdir -p "$PID_DIR"
        chmod 700 "$PID_DIR"
    fi
}

# --- ローカルポートフォワーディングの作成 ---
create_local_tunnel() {
    print_header "ローカルポートフォワーディング（-L）"

    echo "リモートのサービスにローカルからアクセスするトンネルを作成します"
    echo ""
    echo "  ローカルPC:ローカルポート ===SSH===> SSHサーバー → リモートホスト:リモートポート"
    echo ""

    # 入力
    read -rp "SSHサーバー (例: user@bastion.example.com): " ssh_server
    [ -z "$ssh_server" ] && return

    read -rp "ローカルポート (例: 8080): " local_port
    [ -z "$local_port" ] && return

    read -rp "リモートホスト (例: localhost, internal-web): " remote_host
    remote_host=${remote_host:-localhost}

    read -rp "リモートポート (例: 80, 5432): " remote_port
    [ -z "$remote_port" ] && return

    # 確認
    echo ""
    echo -e "${BLUE}作成するトンネル:${NC}"
    echo "  localhost:$local_port → $remote_host:$remote_port (via $ssh_server)"
    echo ""
    read -rp "作成しますか? (Y/n): " confirm
    [[ "$confirm" =~ ^[Nn]$ ]] && return

    # ポートが使用されていないか確認
    if lsof -i ":$local_port" > /dev/null 2>&1; then
        print_error "ポート $local_port は既に使用されています"
        return
    fi

    # トンネル作成
    ensure_pid_dir
    local pid_file="$PID_DIR/L_${local_port}_${remote_host}_${remote_port}.pid"

    ssh -f -N -L "${local_port}:${remote_host}:${remote_port}" "$ssh_server"

    # PIDを取得して保存
    local pid
    pid=$(pgrep -f "ssh.*-L.*${local_port}:${remote_host}:${remote_port}.*${ssh_server}" | tail -1 || echo "")

    if [ -n "$pid" ]; then
        echo "$pid" > "$pid_file"
        print_success "トンネルを作成しました (PID: $pid)"
        echo ""
        echo "接続方法:"
        case $remote_port in
            80|443|3000|8080|8443)
                echo "  ブラウザ: http://localhost:$local_port"
                ;;
            5432)
                echo "  PostgreSQL: psql -h localhost -p $local_port -U ユーザー名 DB名"
                ;;
            3306)
                echo "  MySQL: mysql -h 127.0.0.1 -P $local_port -u ユーザー名 DB名"
                ;;
            6379)
                echo "  Redis: redis-cli -h localhost -p $local_port"
                ;;
            *)
                echo "  localhost:$local_port に接続してください"
                ;;
        esac
    else
        print_error "トンネルの作成に失敗しました"
    fi
}

# --- リモートポートフォワーディングの作成 ---
create_remote_tunnel() {
    print_header "リモートポートフォワーディング（-R）"

    echo "ローカルのサービスをリモートに公開するトンネルを作成します"
    echo ""
    echo "  外部 → リモートサーバー:リモートポート ===SSH===> ローカルPC:ローカルポート"
    echo ""

    # 入力
    read -rp "SSHサーバー (例: user@vps.example.com): " ssh_server
    [ -z "$ssh_server" ] && return

    read -rp "リモートポート (例: 8080): " remote_port
    [ -z "$remote_port" ] && return

    read -rp "ローカルホスト [localhost]: " local_host
    local_host=${local_host:-localhost}

    read -rp "ローカルポート (例: 3000): " local_port
    [ -z "$local_port" ] && return

    # 確認
    echo ""
    echo -e "${BLUE}作成するトンネル:${NC}"
    echo "  リモート:$remote_port → $local_host:$local_port (via $ssh_server)"
    echo ""
    read -rp "作成しますか? (Y/n): " confirm
    [[ "$confirm" =~ ^[Nn]$ ]] && return

    # トンネル作成
    ensure_pid_dir
    local pid_file="$PID_DIR/R_${remote_port}_${local_host}_${local_port}.pid"

    ssh -f -N -R "${remote_port}:${local_host}:${local_port}" "$ssh_server"

    local pid
    pid=$(pgrep -f "ssh.*-R.*${remote_port}:${local_host}:${local_port}.*${ssh_server}" | tail -1 || echo "")

    if [ -n "$pid" ]; then
        echo "$pid" > "$pid_file"
        print_success "トンネルを作成しました (PID: $pid)"
    else
        print_error "トンネルの作成に失敗しました"
    fi
}

# --- ダイナミックフォワーディングの作成 ---
create_dynamic_tunnel() {
    print_header "ダイナミックフォワーディング（-D）"

    echo "SOCKSプロキシを作成します"
    echo ""
    echo "  ブラウザ → localhost:ポート (SOCKS5) ===SSH===> SSHサーバー → インターネット"
    echo ""

    read -rp "SSHサーバー (例: user@proxy-server.example.com): " ssh_server
    [ -z "$ssh_server" ] && return

    read -rp "ローカルポート [1080]: " local_port
    local_port=${local_port:-1080}

    # ポート確認
    if lsof -i ":$local_port" > /dev/null 2>&1; then
        print_error "ポート $local_port は既に使用されています"
        return
    fi

    # 確認
    echo ""
    echo -e "${BLUE}作成するSOCKSプロキシ:${NC}"
    echo "  localhost:$local_port (SOCKS5) via $ssh_server"
    echo ""
    read -rp "作成しますか? (Y/n): " confirm
    [[ "$confirm" =~ ^[Nn]$ ]] && return

    # トンネル作成
    ensure_pid_dir
    local pid_file="$PID_DIR/D_${local_port}.pid"

    ssh -f -N -D "$local_port" "$ssh_server"

    local pid
    pid=$(pgrep -f "ssh.*-D.*${local_port}.*${ssh_server}" | tail -1 || echo "")

    if [ -n "$pid" ]; then
        echo "$pid" > "$pid_file"
        print_success "SOCKSプロキシを作成しました (PID: $pid)"
        echo ""
        echo "使い方:"
        echo "  ブラウザ: プロキシ設定 → SOCKS5 localhost:$local_port"
        echo "  curl:     curl --socks5-hostname localhost:$local_port https://example.com"
    else
        print_error "トンネルの作成に失敗しました"
    fi
}

# --- アクティブなトンネル一覧 ---
list_tunnels() {
    print_header "アクティブなSSHトンネル"

    # 方法1: PIDファイルから確認
    ensure_pid_dir
    local found=0

    for pid_file in "$PID_DIR"/*.pid; do
        [ -f "$pid_file" ] || continue

        local pid
        pid=$(cat "$pid_file")
        local name
        name=$(basename "$pid_file" .pid)

        if kill -0 "$pid" 2>/dev/null; then
            found=1
            local type local_p remote_info

            # ファイル名からトンネル情報を抽出
            case "$name" in
                L_*)
                    type="ローカル(-L)"
                    ;;
                R_*)
                    type="リモート(-R)"
                    ;;
                D_*)
                    type="ダイナミック(-D)"
                    ;;
                *)
                    type="不明"
                    ;;
            esac

            echo -e "  ${GREEN}[ACTIVE]${NC} PID=$pid  タイプ=$type  名前=$name"
        else
            # プロセスが存在しない → PIDファイルを削除
            rm -f "$pid_file"
        fi
    done

    # 方法2: プロセスから直接確認
    echo ""
    echo -e "${BLUE}--- ssh プロセス一覧（フォワーディング関連） ---${NC}"
    if ps aux | grep -E "ssh.*-[LRD]" | grep -v grep; then
        :
    else
        echo "  アクティブなSSHトンネルはありません"
    fi

    if [ $found -eq 0 ]; then
        echo ""
        echo "  管理対象のトンネルはありません"
    fi
}

# --- トンネルの停止 ---
stop_tunnel() {
    print_header "トンネルの停止"

    ensure_pid_dir

    # アクティブなトンネルを取得
    local i=0
    local pids=()
    local names=()

    for pid_file in "$PID_DIR"/*.pid; do
        [ -f "$pid_file" ] || continue

        local pid
        pid=$(cat "$pid_file")

        if kill -0 "$pid" 2>/dev/null; then
            i=$((i + 1))
            pids+=("$pid")
            names+=("$(basename "$pid_file" .pid)")
            echo "  $i) ${names[$((i-1))]} (PID: $pid)"
        else
            rm -f "$pid_file"
        fi
    done

    if [ $i -eq 0 ]; then
        echo "  停止するトンネルがありません"
        return
    fi

    echo "  a) すべて停止"
    echo ""
    read -rp "停止するトンネルの番号（またはa）: " choice

    if [ "$choice" = "a" ] || [ "$choice" = "A" ]; then
        for pid in "${pids[@]}"; do
            kill "$pid" 2>/dev/null && print_success "PID $pid を停止しました"
        done
        rm -f "$PID_DIR"/*.pid
    elif [ -n "$choice" ] && [ "$choice" -ge 1 ] && [ "$choice" -le $i ] 2>/dev/null; then
        local target_pid="${pids[$((choice-1))]}"
        local target_name="${names[$((choice-1))]}"
        kill "$target_pid" 2>/dev/null && print_success "$target_name (PID: $target_pid) を停止しました"
        rm -f "$PID_DIR/${target_name}.pid"
    else
        echo "無効な選択です"
    fi
}

# --- よく使うトンネルのプリセット ---
preset_tunnels() {
    print_header "プリセットトンネル"

    echo "よく使うトンネルパターン:"
    echo "  1) Web開発 (-L 8080:localhost:80)"
    echo "  2) PostgreSQL (-L 5432:localhost:5432)"
    echo "  3) MySQL (-L 3306:localhost:3306)"
    echo "  4) Redis (-L 6379:localhost:6379)"
    echo "  5) SOCKSプロキシ (-D 1080)"
    echo ""

    read -rp "番号を選択: " preset
    read -rp "SSHサーバー: " ssh_server
    [ -z "$ssh_server" ] && return

    ensure_pid_dir
    local tunnel_cmd=""
    local pid_name=""

    case $preset in
        1) tunnel_cmd="-L 8080:localhost:80"; pid_name="L_8080_localhost_80" ;;
        2) tunnel_cmd="-L 5432:localhost:5432"; pid_name="L_5432_localhost_5432" ;;
        3) tunnel_cmd="-L 3306:localhost:3306"; pid_name="L_3306_localhost_3306" ;;
        4) tunnel_cmd="-L 6379:localhost:6379"; pid_name="L_6379_localhost_6379" ;;
        5) tunnel_cmd="-D 1080"; pid_name="D_1080" ;;
        *) echo "無効な選択です"; return ;;
    esac

    # shellcheck disable=SC2086
    ssh -f -N $tunnel_cmd "$ssh_server"

    local pid
    pid=$(pgrep -f "ssh.*${tunnel_cmd}.*${ssh_server}" | tail -1 || echo "")

    if [ -n "$pid" ]; then
        echo "$pid" > "$PID_DIR/${pid_name}.pid"
        print_success "トンネルを作成しました (PID: $pid)"
    else
        print_error "トンネルの作成に失敗しました"
    fi
}

# --- メインメニュー ---
main_menu() {
    while true; do
        print_header "SSHトンネル管理ツール"
        echo "  1) ローカルフォワーディング (-L) を作成"
        echo "  2) リモートフォワーディング (-R) を作成"
        echo "  3) ダイナミックフォワーディング (-D) を作成"
        echo "  4) プリセットから作成"
        echo "  5) アクティブなトンネル一覧"
        echo "  6) トンネルを停止"
        echo "  q) 終了"
        echo ""
        read -rp "選択: " choice

        case $choice in
            1) create_local_tunnel ;;
            2) create_remote_tunnel ;;
            3) create_dynamic_tunnel ;;
            4) preset_tunnels ;;
            5) list_tunnels ;;
            6) stop_tunnel ;;
            q|Q) echo "終了します"; exit 0 ;;
            *) echo "無効な選択です" ;;
        esac

        echo ""
        read -rp "Enter で続行..."
    done
}

# --- メイン処理 ---
main_menu

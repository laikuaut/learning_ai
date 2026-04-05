#!/bin/bash
# ============================================================================
# 04_SSH接続テスト.sh
# ============================================================================
# 学べる内容:
#   - SSH接続の自動テスト
#   - ~/.ssh/config からのホスト情報読み取り
#   - ネットワーク診断コマンド（nc, ssh -G）
#   - シェルスクリプトでのエラーハンドリング
#   - タイムアウトの設定と処理
#
# 実行方法:
#   1. chmod +x 04_SSH接続テスト.sh
#   2. ./04_SSH接続テスト.sh [ホスト名]
#   ※ 引数なしで実行するとすべての設定済みホストをテスト
#
# 動作説明:
#   ~/.ssh/config に登録されているホストへのSSH接続をテストし、
#   接続状況のレポートを出力します。
# ============================================================================

set -euo pipefail

# --- 定数 ---
SSH_DIR="$HOME/.ssh"
CONFIG_FILE="$SSH_DIR/config"
TIMEOUT=10  # 接続タイムアウト（秒）

# --- 色の定義 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# --- ユーティリティ ---
print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

# --- ホスト一覧の取得 ---
get_hosts() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo ""
        return
    fi

    # Host * と Host *.xxx は除外
    grep -E "^Host " "$CONFIG_FILE" | awk '{print $2}' | grep -v '[*?]' || true
}

# --- ホスト情報の表示 ---
show_host_info() {
    local host="$1"

    echo -e "${CYAN}--- ホスト情報: $host ---${NC}"

    # ssh -G で実効設定を取得
    local hostname user port identity_file proxy_jump
    hostname=$(ssh -G "$host" 2>/dev/null | grep "^hostname " | awk '{print $2}' || echo "不明")
    user=$(ssh -G "$host" 2>/dev/null | grep "^user " | awk '{print $2}' || echo "不明")
    port=$(ssh -G "$host" 2>/dev/null | grep "^port " | awk '{print $2}' || echo "22")
    identity_file=$(ssh -G "$host" 2>/dev/null | grep "^identityfile " | head -1 | awk '{print $2}' || echo "デフォルト")
    proxy_jump=$(ssh -G "$host" 2>/dev/null | grep "^proxyjump " | awk '{print $2}' || echo "なし")

    echo "  ホスト名:    $hostname"
    echo "  ユーザー:    $user"
    echo "  ポート:      $port"
    echo "  秘密鍵:      $identity_file"
    [ "$proxy_jump" != "なし" ] && echo "  踏み台:      $proxy_jump"
}

# --- 接続テストの実行 ---
test_host() {
    local host="$1"
    local hostname port

    hostname=$(ssh -G "$host" 2>/dev/null | grep "^hostname " | awk '{print $2}' || echo "$host")
    port=$(ssh -G "$host" 2>/dev/null | grep "^port " | awk '{print $2}' || echo "22")

    echo ""
    show_host_info "$host"
    echo ""

    # テスト1: ポートの疎通確認
    echo -n "  [1/3] ポート疎通確認 ($hostname:$port)... "
    if nc -z -w "$TIMEOUT" "$hostname" "$port" 2>/dev/null; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${RED}FAIL${NC}"
        echo -e "  ${RED}→ ポート $port に接続できません（サーバー停止/ファイアウォール）${NC}"
        return 1
    fi

    # テスト2: SSHプロトコルの確認
    echo -n "  [2/3] SSHプロトコル確認... "
    local banner
    banner=$(echo "" | nc -w "$TIMEOUT" "$hostname" "$port" 2>/dev/null | head -1 || echo "")
    if [[ "$banner" == SSH-* ]]; then
        echo -e "${GREEN}OK${NC} ($banner)"
    else
        echo -e "${YELLOW}WARN${NC} (バナーを取得できません)"
    fi

    # テスト3: SSH認証テスト
    echo -n "  [3/3] SSH認証テスト... "
    local ssh_result
    ssh_result=$(ssh -o ConnectTimeout="$TIMEOUT" \
                     -o BatchMode=yes \
                     -o StrictHostKeyChecking=accept-new \
                     "$host" "echo OK" 2>&1) && true
    local exit_code=$?

    if [ $exit_code -eq 0 ] && [ "$ssh_result" = "OK" ]; then
        echo -e "${GREEN}OK${NC} (認証成功)"
        return 0
    elif echo "$ssh_result" | grep -q "Permission denied"; then
        echo -e "${RED}FAIL${NC} (認証失敗)"
        echo -e "  ${RED}→ 公開鍵が登録されていないか、秘密鍵が正しくありません${NC}"
        return 1
    elif echo "$ssh_result" | grep -q "Connection timed out"; then
        echo -e "${RED}FAIL${NC} (タイムアウト)"
        echo -e "  ${RED}→ ネットワーク的に到達できません${NC}"
        return 1
    elif echo "$ssh_result" | grep -q "Host key verification failed"; then
        echo -e "${YELLOW}WARN${NC} (ホスト鍵の検証失敗)"
        echo -e "  ${YELLOW}→ known_hosts のホスト鍵が変更されています${NC}"
        return 1
    else
        echo -e "${YELLOW}WARN${NC} (その他のエラー)"
        echo "  → $ssh_result" | head -3
        return 1
    fi
}

# --- 全ホストのテスト ---
test_all_hosts() {
    print_header "SSH接続テスト（全ホスト）"

    local hosts
    hosts=$(get_hosts)

    if [ -z "$hosts" ]; then
        echo -e "${YELLOW}設定済みのホストがありません${NC}"
        echo "~/.ssh/config にホストを追加してください"
        return
    fi

    local total=0
    local success=0
    local fail=0

    while IFS= read -r host; do
        [ -z "$host" ] && continue
        total=$((total + 1))

        if test_host "$host"; then
            success=$((success + 1))
        else
            fail=$((fail + 1))
        fi
    done <<< "$hosts"

    # サマリー
    echo ""
    echo -e "${BLUE}━━━ テスト結果サマリー ━━━${NC}"
    echo ""
    echo "  テスト対象: $total ホスト"
    echo -e "  ${GREEN}成功: $success${NC}"
    echo -e "  ${RED}失敗: $fail${NC}"
    echo ""
}

# --- 詳細診断 ---
diagnose_host() {
    local host="$1"

    print_header "詳細診断: $host"

    show_host_info "$host"

    local hostname port identity_file
    hostname=$(ssh -G "$host" 2>/dev/null | grep "^hostname " | awk '{print $2}' || echo "$host")
    port=$(ssh -G "$host" 2>/dev/null | grep "^port " | awk '{print $2}' || echo "22")
    identity_file=$(ssh -G "$host" 2>/dev/null | grep "^identityfile " | head -1 | awk '{print $2}' || echo "")

    echo ""
    echo -e "${CYAN}--- 診断開始 ---${NC}"

    # 1. DNS解決
    echo ""
    echo -n "  DNS解決... "
    if host "$hostname" > /dev/null 2>&1; then
        local ip
        ip=$(host "$hostname" 2>/dev/null | grep "has address" | head -1 | awk '{print $NF}')
        echo -e "${GREEN}OK${NC} ($ip)"
    elif [[ "$hostname" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo -e "${GREEN}OK${NC} (IPアドレス直指定)"
    else
        echo -e "${RED}FAIL${NC} (DNS解決できません)"
    fi

    # 2. ポート疎通
    echo -n "  ポート疎通 ($hostname:$port)... "
    if nc -z -w "$TIMEOUT" "$hostname" "$port" 2>/dev/null; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${RED}FAIL${NC}"
    fi

    # 3. 秘密鍵の確認
    if [ -n "$identity_file" ]; then
        # チルダを展開
        local expanded_path
        expanded_path=$(eval echo "$identity_file")

        echo -n "  秘密鍵の存在 ($identity_file)... "
        if [ -f "$expanded_path" ]; then
            local perm
            perm=$(stat -c "%a" "$expanded_path" 2>/dev/null || stat -f "%Lp" "$expanded_path" 2>/dev/null)
            if [ "$perm" = "600" ]; then
                echo -e "${GREEN}OK${NC} (パーミッ���ョン: $perm)"
            else
                echo -e "${YELLOW}WARN${NC} (パーミッション: $perm → 600 に修正してください)"
            fi
        else
            echo -e "${RED}FAIL${NC} (ファイルが存在しません)"
        fi
    fi

    # 4. SSH詳細ログ
    echo ""
    echo -e "${CYAN}--- SSH接続の詳細ログ（抜粋） ---${NC}"
    ssh -v -o ConnectTimeout="$TIMEOUT" \
           -o BatchMode=yes \
           "$host" "exit" 2>&1 | grep -E "(Connecting|Authentication|Offering|debug1: identity)" | head -10 || true

    echo ""
}

# --- メイン処理 ---
main() {
    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║    SSH 接続テストツール                ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════╝${NC}"
    echo ""
    echo "日時: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "タイムアウト: ${TIMEOUT}秒"

    if [ $# -eq 0 ]; then
        # 引数なし → メニュー表示
        echo ""
        echo "  1) 全ホストの接続テスト"
        echo "  2) 特定ホストの詳細診断"
        echo "  3) 設定済みホスト一覧"
        echo "  q) 終了"
        echo ""
        read -rp "選択: " choice

        case $choice in
            1) test_all_hosts ;;
            2)
                read -rp "ホスト名: " target
                [ -n "$target" ] && diagnose_host "$target"
                ;;
            3)
                print_header "設定済みホスト一覧"
                local hosts
                hosts=$(get_hosts)
                if [ -n "$hosts" ]; then
                    echo "$hosts" | while IFS= read -r h; do
                        echo "  - $h"
                    done
                else
                    echo "  (なし)"
                fi
                ;;
            q|Q) exit 0 ;;
            *) echo "無効な選択です" ;;
        esac
    else
        # 引数あり → そのホストをテスト
        diagnose_host "$1"
    fi
}

main "$@"

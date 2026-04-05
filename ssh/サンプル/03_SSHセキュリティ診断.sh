#!/bin/bash
# ============================================================================
# 03_SSHセキュリティ診断.sh
# ============================================================================
# 学べる内容:
#   - SSH設定のセキュリティ監査
#   - パーミッションチェックの自動化
#   - sshd_config の安全性評価
#   - シェルスクリプトでの条件分岐とレポート生成
#
# 実行方法:
#   1. chmod +x 03_SSHセキュリティ診断.sh
#   2. ./03_SSHセキュリティ診断.sh
#   ※ サーバー設定の診断には root 権限が必要な項目があります
#
# 動作説明:
#   ローカルのSSH設定とサーバー設定のセキュリティを診断し、
#   改善点をレポートとして出力します。
# ============================================================================

set -euo pipefail

# --- 定数 ---
SSH_DIR="$HOME/.ssh"
SSHD_CONFIG="/etc/ssh/sshd_config"

# --- 色の定義 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# --- カウンター ---
PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

# --- 結果の記録 ---
check_pass() {
    echo -e "  ${GREEN}[PASS]${NC} $1"
    PASS_COUNT=$((PASS_COUNT + 1))
}

check_warn() {
    echo -e "  ${YELLOW}[WARN]${NC} $1"
    WARN_COUNT=$((WARN_COUNT + 1))
}

check_fail() {
    echo -e "  ${RED}[FAIL]${NC} $1"
    FAIL_COUNT=$((FAIL_COUNT + 1))
}

print_section() {
    echo ""
    echo -e "${BLUE}━━━ $1 ━━━${NC}"
}

# --- 1. クライアント側の診断 ---
check_client() {
    print_section "クライアント設定の診断"

    # .ssh ディレクトリのパーミッション
    echo ""
    echo "■ ディレクトリ・ファイルのパーミッション"

    if [ -d "$SSH_DIR" ]; then
        local dir_perm
        dir_perm=$(stat -c "%a" "$SSH_DIR" 2>/dev/null || stat -f "%Lp" "$SSH_DIR" 2>/dev/null)

        if [ "$dir_perm" = "700" ]; then
            check_pass ".ssh ディレクトリ: $dir_perm"
        else
            check_fail ".ssh ディレクトリ: $dir_perm (700 であるべき)"
        fi
    else
        check_warn ".ssh ディレクトリが存在しません"
    fi

    # 秘密鍵のパーミッション
    for key_file in "$SSH_DIR"/id_*; do
        [[ "$key_file" == *.pub ]] && continue
        [ -f "$key_file" ] || continue

        local perm
        perm=$(stat -c "%a" "$key_file" 2>/dev/null || stat -f "%Lp" "$key_file" 2>/dev/null)

        if [ "$perm" = "600" ]; then
            check_pass "$(basename "$key_file"): $perm"
        else
            check_fail "$(basename "$key_file"): $perm (600 であるべき)"
        fi
    done

    # config のパーミッション
    if [ -f "$SSH_DIR/config" ]; then
        local config_perm
        config_perm=$(stat -c "%a" "$SSH_DIR/config" 2>/dev/null || stat -f "%Lp" "$SSH_DIR/config" 2>/dev/null)

        if [ "$config_perm" = "600" ] || [ "$config_perm" = "644" ]; then
            check_pass "config: $config_perm"
        else
            check_fail "config: $config_perm (600 であるべき)"
        fi
    fi

    # authorized_keys のパーミッション
    if [ -f "$SSH_DIR/authorized_keys" ]; then
        local ak_perm
        ak_perm=$(stat -c "%a" "$SSH_DIR/authorized_keys" 2>/dev/null || stat -f "%Lp" "$SSH_DIR/authorized_keys" 2>/dev/null)

        if [ "$ak_perm" = "600" ]; then
            check_pass "authorized_keys: $ak_perm"
        else
            check_fail "authorized_keys: $ak_perm (600 であるべき)"
        fi
    fi

    # 鍵のアルゴリズム
    echo ""
    echo "■ 鍵のアルゴリズム"

    for pub_file in "$SSH_DIR"/id_*.pub; do
        [ -f "$pub_file" ] || continue

        local key_info
        key_info=$(ssh-keygen -l -f "$pub_file" 2>/dev/null || echo "")
        if [ -z "$key_info" ]; then
            continue
        fi

        local key_type
        key_type=$(echo "$key_info" | awk '{print $NF}' | tr -d '()')
        local key_bits
        key_bits=$(echo "$key_info" | awk '{print $1}')

        case "$key_type" in
            ED25519)
                check_pass "$(basename "$pub_file"): Ed25519 (推奨)"
                ;;
            RSA)
                if [ "$key_bits" -ge 3072 ] 2>/dev/null; then
                    check_pass "$(basename "$pub_file"): RSA ${key_bits}bit"
                elif [ "$key_bits" -ge 2048 ] 2>/dev/null; then
                    check_warn "$(basename "$pub_file"): RSA ${key_bits}bit (3072bit以上を推奨)"
                else
                    check_fail "$(basename "$pub_file"): RSA ${key_bits}bit (鍵長が不十分)"
                fi
                ;;
            DSA)
                check_fail "$(basename "$pub_file"): DSA (非推奨、使用禁止)"
                ;;
            ECDSA)
                check_warn "$(basename "$pub_file"): ECDSA (Ed25519 を推奨)"
                ;;
            *)
                check_warn "$(basename "$pub_file"): $key_type (不明なアルゴリズム)"
                ;;
        esac
    done

    # config の設定チェック
    echo ""
    echo "■ クライアント設定（~/.ssh/config）"

    if [ -f "$SSH_DIR/config" ]; then
        # IdentitiesOnly
        if grep -q "IdentitiesOnly yes" "$SSH_DIR/config" 2>/dev/null; then
            check_pass "IdentitiesOnly yes が設定されています"
        else
            check_warn "IdentitiesOnly yes の設定を推奨します"
        fi

        # ServerAliveInterval
        if grep -q "ServerAliveInterval" "$SSH_DIR/config" 2>/dev/null; then
            check_pass "ServerAliveInterval が設定されています"
        else
            check_warn "ServerAliveInterval の設定を推奨します"
        fi

        # ForwardAgent（セキュリティリスク）
        if grep -qi "ForwardAgent yes" "$SSH_DIR/config" 2>/dev/null; then
            check_warn "ForwardAgent yes が設定されています（ProxyJump を推奨）"
        else
            check_pass "ForwardAgent はデフォルト（無効）です"
        fi
    else
        check_warn "~/.ssh/config が存在しません"
    fi
}

# --- 2. サーバー側の診断 ---
check_server() {
    print_section "サーバー設定の診断（sshd_config）"

    if [ ! -f "$SSHD_CONFIG" ]; then
        check_warn "sshd_config が見つかりません（$SSHD_CONFIG）"
        echo "  → サーバー設定の診断をスキップします"
        return
    fi

    if [ ! -r "$SSHD_CONFIG" ]; then
        check_warn "sshd_config を読み取れません（root権限が必要です）"
        echo "  → sudo で再実行してください"
        return
    fi

    echo ""
    echo "■ 認証設定"

    # PermitRootLogin
    local root_login
    root_login=$(grep -E "^PermitRootLogin" "$SSHD_CONFIG" | awk '{print $2}' || echo "")
    if [ "$root_login" = "no" ]; then
        check_pass "PermitRootLogin no"
    elif [ -z "$root_login" ]; then
        check_warn "PermitRootLogin が明示されていません（デフォルト: prohibit-password）"
    else
        check_fail "PermitRootLogin $root_login (no を推奨)"
    fi

    # PasswordAuthentication
    local pass_auth
    pass_auth=$(grep -E "^PasswordAuthentication" "$SSHD_CONFIG" | awk '{print $2}' || echo "")
    if [ "$pass_auth" = "no" ]; then
        check_pass "PasswordAuthentication no"
    elif [ -z "$pass_auth" ]; then
        check_warn "PasswordAuthentication が明示されていません（デフォルト: yes）"
    else
        check_fail "PasswordAuthentication $pass_auth (no を推奨)"
    fi

    # PermitEmptyPasswords
    local empty_pass
    empty_pass=$(grep -E "^PermitEmptyPasswords" "$SSHD_CONFIG" | awk '{print $2}' || echo "")
    if [ "$empty_pass" = "no" ] || [ -z "$empty_pass" ]; then
        check_pass "PermitEmptyPasswords: ${empty_pass:-no (default)}"
    else
        check_fail "PermitEmptyPasswords $empty_pass (no であるべき)"
    fi

    # MaxAuthTries
    local max_tries
    max_tries=$(grep -E "^MaxAuthTries" "$SSHD_CONFIG" | awk '{print $2}' || echo "")
    if [ -n "$max_tries" ] && [ "$max_tries" -le 5 ] 2>/dev/null; then
        check_pass "MaxAuthTries $max_tries"
    elif [ -z "$max_tries" ]; then
        check_warn "MaxAuthTries が明示されていません（デフォルト: 6）"
    else
        check_warn "MaxAuthTries $max_tries (3〜5 を推奨)"
    fi

    echo ""
    echo "■ その他の設定"

    # X11Forwarding
    local x11
    x11=$(grep -E "^X11Forwarding" "$SSHD_CONFIG" | awk '{print $2}' || echo "")
    if [ "$x11" = "no" ]; then
        check_pass "X11Forwarding no"
    else
        check_warn "X11Forwarding ${x11:-yes (default)} (不要なら no を推奨)"
    fi

    # LogLevel
    local log_level
    log_level=$(grep -E "^LogLevel" "$SSHD_CONFIG" | awk '{print $2}' || echo "")
    if [ "$log_level" = "VERBOSE" ] || [ "$log_level" = "INFO" ]; then
        check_pass "LogLevel $log_level"
    else
        check_warn "LogLevel ${log_level:-INFO (default)} (VERBOSE を推奨)"
    fi

    # AllowUsers / AllowGroups
    if grep -qE "^(AllowUsers|AllowGroups)" "$SSHD_CONFIG"; then
        check_pass "AllowUsers/AllowGroups が設定されています"
    else
        check_warn "AllowUsers/AllowGroups の設定を推奨します"
    fi
}

# --- 3. known_hosts の診断 ---
check_known_hosts() {
    print_section "known_hosts の診断"

    local kh_file="$SSH_DIR/known_hosts"

    if [ ! -f "$kh_file" ]; then
        check_warn "known_hosts が存在しません"
        return
    fi

    # エントリ数
    local entry_count
    entry_count=$(wc -l < "$kh_file")
    echo "  登録済みホスト数: $entry_count"

    # ハッシュ化されているか
    if head -1 "$kh_file" | grep -q "^|1|"; then
        check_pass "ホスト名がハッシュ化されています"
    else
        check_warn "ホスト名がハッシュ化されていません（HashKnownHosts yes を推奨）"
    fi
}

# --- レポートのサマリー ---
print_summary() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  診断結果サマリー${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "  ${GREEN}PASS: $PASS_COUNT${NC}"
    echo -e "  ${YELLOW}WARN: $WARN_COUNT${NC}"
    echo -e "  ${RED}FAIL: $FAIL_COUNT${NC}"
    echo ""

    if [ $FAIL_COUNT -eq 0 ] && [ $WARN_COUNT -eq 0 ]; then
        echo -e "  ${GREEN}すべてのチェックに合格しました！${NC}"
    elif [ $FAIL_COUNT -eq 0 ]; then
        echo -e "  ${YELLOW}重大な問題はありませんが、改善の余地があります${NC}"
    else
        echo -e "  ${RED}セキュリティ上の問題が見つかりました。FAIL の項目を修正してください${NC}"
    fi
    echo ""
}

# --- メイン処理 ---
echo ""
echo -e "${BLUE}╔═══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║    SSH セキュリティ診断ツール          ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════╝${NC}"
echo ""
echo "診断日時: $(date '+%Y-%m-%d %H:%M:%S')"
echo "ユーザー: $(whoami)"
echo "ホスト名: $(hostname)"

check_client
check_server
check_known_hosts
print_summary

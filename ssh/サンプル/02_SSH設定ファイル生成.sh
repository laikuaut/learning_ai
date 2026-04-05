#!/bin/bash
# ============================================================================
# 02_SSH設定ファイル生成.sh
# ============================================================================
# 学べる内容:
#   - ~/.ssh/config の構造と書き方
#   - シェルスクリプトでの設定ファイル生成
#   - ヒアドキュメントの使い方
#   - ファイルのバックアップと安全な書き込み
#
# 実行方法:
#   1. chmod +x 02_SSH設定ファイル生成.sh
#   2. ./02_SSH設定ファイル生成.sh
#
# 動作説明:
#   対話的に接続先情報を入力し、~/.ssh/config に追記します。
#   既存の設定のバックアップも自動で行います。
# ============================================================================

set -euo pipefail

# --- 定数 ---
SSH_DIR="$HOME/.ssh"
CONFIG_FILE="$SSH_DIR/config"

# --- 色の定義 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# --- ユーティリティ関数 ---
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

print_warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# --- .ssh ディレクトリの確認 ---
ensure_ssh_dir() {
    if [ ! -d "$SSH_DIR" ]; then
        mkdir -p "$SSH_DIR"
        chmod 700 "$SSH_DIR"
    fi
}

# --- 現在の設定を表示 ---
show_config() {
    print_header "現在の SSH 設定"

    if [ ! -f "$CONFIG_FILE" ]; then
        print_warning "設定ファイルが存在しません: $CONFIG_FILE"
        return
    fi

    echo -e "${BLUE}--- $CONFIG_FILE ---${NC}"
    cat "$CONFIG_FILE"
    echo -e "${BLUE}--- ここまで ---${NC}"

    # Host の一覧を抽出
    echo ""
    echo -e "${GREEN}登録済みホスト:${NC}"
    grep -E "^Host " "$CONFIG_FILE" | sed 's/Host /  /' || echo "  (なし)"
}

# --- ホスト設定を追加 ---
add_host() {
    print_header "新しいホスト設定を追加"

    ensure_ssh_dir

    # エイリアス名
    read -rp "エイリアス名 (例: dev, staging, github): " alias_name
    if [ -z "$alias_name" ]; then
        echo "キャンセルしました"
        return
    fi

    # 既存チェック
    if [ -f "$CONFIG_FILE" ] && grep -q "^Host $alias_name$" "$CONFIG_FILE"; then
        print_warning "エイリアス '$alias_name' は既に存在します"
        read -rp "続行しますか? (y/N): " cont
        [[ "$cont" =~ ^[Yy]$ ]] || return
    fi

    # ホスト名
    read -rp "ホスト名またはIP (例: dev.example.com): " hostname
    [ -z "$hostname" ] && hostname="$alias_name"

    # ユーザー名
    read -rp "ユーザー名 (例: deploy) [$(whoami)]: " username
    username=${username:-$(whoami)}

    # ポート
    read -rp "ポート番号 [22]: " port
    port=${port:-22}

    # 秘密鍵
    echo ""
    echo "利用可能な鍵:"
    local i=0
    local keys=()
    for key_file in "$SSH_DIR"/id_*; do
        [[ "$key_file" == *.pub ]] && continue
        [ -f "$key_file" ] || continue
        i=$((i + 1))
        keys+=("$key_file")
        echo "  $i) $(basename "$key_file")"
    done
    echo "  0) 指定しない"

    local identity_file=""
    if [ $i -gt 0 ]; then
        read -rp "鍵を選択 [0]: " key_choice
        key_choice=${key_choice:-0}
        if [ "$key_choice" -gt 0 ] && [ "$key_choice" -le $i ] 2>/dev/null; then
            identity_file="${keys[$((key_choice - 1))]}"
        fi
    fi

    # ProxyJump（踏み台）
    read -rp "踏み台サーバー (空欄でなし): " proxy_jump

    # 確認
    echo ""
    echo -e "${BLUE}--- 追加する設定 ---${NC}"
    echo "Host $alias_name"
    echo "    HostName $hostname"
    echo "    User $username"
    [ "$port" != "22" ] && echo "    Port $port"
    [ -n "$identity_file" ] && echo "    IdentityFile $identity_file"
    [ -n "$proxy_jump" ] && echo "    ProxyJump $proxy_jump"
    echo -e "${BLUE}--------------------${NC}"
    echo ""

    read -rp "この設定を追加しますか? (Y/n): " confirm
    if [[ "$confirm" =~ ^[Nn]$ ]]; then
        echo "キャンセルしました"
        return
    fi

    # バックアップ
    if [ -f "$CONFIG_FILE" ]; then
        cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
        print_success "バックアップを作成: ${CONFIG_FILE}.bak"
    fi

    # 設定を追記
    {
        echo ""
        echo "# --- $alias_name ---"
        echo "Host $alias_name"
        echo "    HostName $hostname"
        echo "    User $username"
        [ "$port" != "22" ] && echo "    Port $port"
        [ -n "$identity_file" ] && echo "    IdentityFile $identity_file"
        [ -n "$proxy_jump" ] && echo "    ProxyJump $proxy_jump"
    } >> "$CONFIG_FILE"

    chmod 600 "$CONFIG_FILE"
    print_success "設定を追加しました: Host $alias_name"
    echo ""
    echo "接続コマンド: ssh $alias_name"
}

# --- 共通設定を追加 ---
add_common_settings() {
    print_header "共通設定（Host *）を追加"

    ensure_ssh_dir

    if [ -f "$CONFIG_FILE" ] && grep -q "^Host \*$" "$CONFIG_FILE"; then
        print_warning "Host * の設定は既に存在します"
        read -rp "追記しますか? (y/N): " cont
        [[ "$cont" =~ ^[Yy]$ ]] || return
    fi

    echo "追加する共通設定を選択してください（複数選択可）:"
    echo "  1) キープアライブ（接続維持）"
    echo "  2) IdentitiesOnly（指定した鍵のみ使用）"
    echo "  3) AddKeysToAgent（ssh-agent に自動追加）"
    echo "  4) HashKnownHosts（known_hosts のハッシュ化）"
    echo "  5) すべて"
    read -rp "選択（カンマ区切り）[5]: " selections
    selections=${selections:-5}

    # バックアップ
    if [ -f "$CONFIG_FILE" ]; then
        cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
    fi

    local config_lines=()
    config_lines+=("")
    config_lines+=("# --- 共通設定 ---")
    config_lines+=("Host *")

    if [[ "$selections" == *"1"* ]] || [[ "$selections" == *"5"* ]]; then
        config_lines+=("    ServerAliveInterval 60")
        config_lines+=("    ServerAliveCountMax 3")
    fi
    if [[ "$selections" == *"2"* ]] || [[ "$selections" == *"5"* ]]; then
        config_lines+=("    IdentitiesOnly yes")
    fi
    if [[ "$selections" == *"3"* ]] || [[ "$selections" == *"5"* ]]; then
        config_lines+=("    AddKeysToAgent yes")
    fi
    if [[ "$selections" == *"4"* ]] || [[ "$selections" == *"5"* ]]; then
        config_lines+=("    HashKnownHosts yes")
    fi

    # 設定を追記
    printf '%s\n' "${config_lines[@]}" >> "$CONFIG_FILE"
    chmod 600 "$CONFIG_FILE"

    print_success "共通設定を追加しました"
}

# --- GitHub用設定を追加 ---
add_github() {
    print_header "GitHub SSH設定を追加"

    ensure_ssh_dir

    # GitHub用の鍵を探す
    local github_key=""
    for key_file in "$SSH_DIR"/id_*github* "$SSH_DIR"/id_ed25519 "$SSH_DIR"/id_rsa; do
        [[ "$key_file" == *.pub ]] && continue
        if [ -f "$key_file" ]; then
            github_key="$key_file"
            break
        fi
    done

    if [ -z "$github_key" ]; then
        print_warning "SSH鍵が見つかりません。先に鍵を生成してください。"
        return
    fi

    echo "使用する鍵: $github_key"
    read -rp "この鍵を使用しますか? (Y/n): " confirm
    [[ "$confirm" =~ ^[Nn]$ ]] && return

    # バックアップ
    if [ -f "$CONFIG_FILE" ]; then
        cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
    fi

    # 設定を追記
    {
        echo ""
        echo "# --- GitHub ---"
        echo "Host github.com"
        echo "    HostName github.com"
        echo "    User git"
        echo "    IdentityFile $github_key"
        echo "    IdentitiesOnly yes"
    } >> "$CONFIG_FILE"

    chmod 600 "$CONFIG_FILE"
    print_success "GitHub SSH設定を追加しました"
    echo ""
    echo "接続テスト: ssh -T git@github.com"
}

# --- 設定の有効性確認 ---
validate_config() {
    print_header "設定の有効性確認"

    if [ ! -f "$CONFIG_FILE" ]; then
        print_warning "設定ファイルが存在しません"
        return
    fi

    echo "登録されているホストの実効設定を確認:"
    echo ""

    # 各ホストの実効設定を表示
    while IFS= read -r line; do
        local host
        host=$(echo "$line" | sed 's/Host //')
        [ "$host" = "*" ] && continue

        echo -e "${GREEN}[$host]${NC}"
        ssh -G "$host" 2>/dev/null | grep -E "^(hostname|user|port|identityfile|proxyjump) " | while IFS= read -r setting; do
            echo "  $setting"
        done
        echo ""
    done < <(grep "^Host " "$CONFIG_FILE")
}

# --- メインメニュー ---
main_menu() {
    while true; do
        print_header "SSH設定ファイル生成ツール"
        echo "  1) 現在の設定を表示"
        echo "  2) 新しいホスト設定を追加"
        echo "  3) 共通設定（Host *）を追加"
        echo "  4) GitHub SSH設定を追加"
        echo "  5) 設定の有効性確認"
        echo "  q) 終了"
        echo ""
        read -rp "選択: " choice

        case $choice in
            1) show_config ;;
            2) add_host ;;
            3) add_common_settings ;;
            4) add_github ;;
            5) validate_config ;;
            q|Q) echo "終了します"; exit 0 ;;
            *) echo "無効な選択です" ;;
        esac

        echo ""
        read -rp "Enter で続行..."
    done
}

# --- メイン処理 ---
main_menu

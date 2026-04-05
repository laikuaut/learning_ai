#!/bin/bash
# ============================================================================
# 01_SSH鍵管理ツール.sh
# ============================================================================
# 学べる内容:
#   - SSH鍵ペアの生成（Ed25519 / RSA）
#   - 鍵のフィンガープリント確認
#   - ssh-agentへの鍵の登録・管理
#   - パーミッションの自動修正
#   - シェルスクリプトでの対話的メニュー
#
# 実行方法:
#   1. chmod +x 01_SSH鍵管理ツール.sh
#   2. ./01_SSH鍵管理ツール.sh
#
# 動作説明:
#   SSH鍵の生成・一覧表示・パーミッション修正などを
#   対話的なメニューから操作できるツールです。
# ============================================================================

set -euo pipefail

# --- 定数 ---
SSH_DIR="$HOME/.ssh"
DEFAULT_KEY_TYPE="ed25519"

# --- 色の定義 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

# --- .ssh ディレクトリの確認・作成 ---
ensure_ssh_dir() {
    if [ ! -d "$SSH_DIR" ]; then
        mkdir -p "$SSH_DIR"
        chmod 700 "$SSH_DIR"
        print_success ".ssh ディレクトリを作成しました: $SSH_DIR"
    fi
}

# --- 鍵一覧の表示 ---
list_keys() {
    print_header "SSH鍵の一覧"

    if [ ! -d "$SSH_DIR" ]; then
        print_warning ".ssh ディレクトリが存在しません"
        return
    fi

    local found=0

    # 秘密鍵を検索（.pub でないファイル）
    for key_file in "$SSH_DIR"/id_*; do
        # .pub ファイルはスキップ
        if [[ "$key_file" == *.pub ]]; then
            continue
        fi

        if [ -f "$key_file" ]; then
            found=1
            local pub_file="${key_file}.pub"

            echo -e "${GREEN}鍵ファイル:${NC} $(basename "$key_file")"

            if [ -f "$pub_file" ]; then
                # フィンガープリントを表示
                local fingerprint
                fingerprint=$(ssh-keygen -l -f "$pub_file" 2>/dev/null || echo "取得できません")
                echo "  フィンガープリント: $fingerprint"
            fi

            # パーミッション確認
            local perm
            perm=$(stat -c "%a" "$key_file" 2>/dev/null || stat -f "%Lp" "$key_file" 2>/dev/null)
            if [ "$perm" = "600" ]; then
                echo -e "  パーミッション: ${GREEN}${perm} (OK)${NC}"
            else
                echo -e "  パーミッション: ${RED}${perm} (要修正 → 600)${NC}"
            fi
            echo ""
        fi
    done

    if [ $found -eq 0 ]; then
        print_warning "SSH鍵が見つかりません"
    fi

    # ssh-agent に登録されている鍵
    echo -e "${BLUE}--- ssh-agent に登録されている鍵 ---${NC}"
    if ssh-add -l 2>/dev/null; then
        :
    else
        echo "  ssh-agent に鍵が登録されていません（またはagentが起動していません）"
    fi
}

# --- 鍵ペアの生成 ---
generate_key() {
    print_header "SSH鍵ペアの生成"

    ensure_ssh_dir

    # 鍵の種類を選択
    echo "鍵の種類を選択してください:"
    echo "  1) Ed25519 (推奨)"
    echo "  2) RSA 4096bit"
    read -rp "選択 [1]: " key_choice
    key_choice=${key_choice:-1}

    local key_type
    local key_bits=""
    case $key_choice in
        1) key_type="ed25519" ;;
        2) key_type="rsa"; key_bits="-b 4096" ;;
        *) print_error "無効な選択です"; return ;;
    esac

    # ファイル名を入力
    read -rp "鍵ファイル名 (例: id_ed25519_github): " key_name
    if [ -z "$key_name" ]; then
        key_name="id_${key_type}"
    fi

    local key_path="$SSH_DIR/$key_name"

    # 既存ファイルの確認
    if [ -f "$key_path" ]; then
        print_warning "ファイルが既に存在します: $key_path"
        read -rp "上書きしますか? (y/N): " overwrite
        if [[ ! "$overwrite" =~ ^[Yy]$ ]]; then
            echo "キャンセルしました"
            return
        fi
    fi

    # コメントを入力
    read -rp "コメント (例: user@example.com): " comment
    comment=${comment:-"$(whoami)@$(hostname)"}

    # 鍵を生成
    echo ""
    echo "生成中..."
    # shellcheck disable=SC2086
    ssh-keygen -t "$key_type" $key_bits -C "$comment" -f "$key_path"

    echo ""
    print_success "鍵ペアを生成しました"
    echo "  秘密鍵: $key_path"
    echo "  公開鍵: ${key_path}.pub"
    echo ""

    # 公開鍵を表示
    echo -e "${BLUE}公開鍵の内容（サーバーやGitHubに登録する文字列）:${NC}"
    echo "---"
    cat "${key_path}.pub"
    echo "---"
}

# --- パーミッションの修正 ---
fix_permissions() {
    print_header "パーミッションの修正"

    ensure_ssh_dir

    local fixed=0

    # .ssh ディレクトリ
    local dir_perm
    dir_perm=$(stat -c "%a" "$SSH_DIR" 2>/dev/null || stat -f "%Lp" "$SSH_DIR" 2>/dev/null)
    if [ "$dir_perm" != "700" ]; then
        chmod 700 "$SSH_DIR"
        print_success ".ssh ディレクトリ: $dir_perm → 700"
        fixed=1
    fi

    # 各ファイルのパーミッション
    for file in "$SSH_DIR"/*; do
        [ -f "$file" ] || continue

        local current_perm expected_perm
        current_perm=$(stat -c "%a" "$file" 2>/dev/null || stat -f "%Lp" "$file" 2>/dev/null)

        case "$(basename "$file")" in
            *.pub)
                expected_perm="644"
                ;;
            known_hosts|known_hosts.old)
                expected_perm="644"
                ;;
            *)
                expected_perm="600"
                ;;
        esac

        if [ "$current_perm" != "$expected_perm" ]; then
            chmod "$expected_perm" "$file"
            print_success "$(basename "$file"): $current_perm → $expected_perm"
            fixed=1
        fi
    done

    if [ $fixed -eq 0 ]; then
        print_success "すべてのパーミッションは正しく設定されています"
    fi
}

# --- ssh-agent に鍵を登録 ---
add_to_agent() {
    print_header "ssh-agent に鍵を登録"

    # ssh-agent が起動しているか確認
    if [ -z "${SSH_AUTH_SOCK:-}" ]; then
        print_warning "ssh-agent が起動していません"
        echo "以下のコマンドで起動してください:"
        echo '  eval "$(ssh-agent -s)"'
        return
    fi

    # 鍵ファイルの一覧を表示
    echo "登録可能な秘密鍵:"
    local i=0
    local keys=()
    for key_file in "$SSH_DIR"/id_*; do
        [[ "$key_file" == *.pub ]] && continue
        [ -f "$key_file" ] || continue
        i=$((i + 1))
        keys+=("$key_file")
        echo "  $i) $(basename "$key_file")"
    done

    if [ $i -eq 0 ]; then
        print_warning "秘密鍵が見つかりません"
        return
    fi

    read -rp "登録する鍵の番号を選択: " selection
    if [ -z "$selection" ] || [ "$selection" -lt 1 ] || [ "$selection" -gt $i ] 2>/dev/null; then
        print_error "無効な選択です"
        return
    fi

    local selected_key="${keys[$((selection - 1))]}"

    # 有効期限を設定するか
    read -rp "有効期限を設定しますか? (秒数を入力、空欄でなし): " lifetime
    if [ -n "$lifetime" ]; then
        ssh-add -t "$lifetime" "$selected_key"
    else
        ssh-add "$selected_key"
    fi

    echo ""
    print_success "鍵を登録しました"

    # 登録確認
    echo ""
    echo "現在登録されている鍵:"
    ssh-add -l
}

# --- SSH接続テスト ---
test_connection() {
    print_header "SSH接続テスト"

    read -rp "接続先 (例: user@example.com): " target
    if [ -z "$target" ]; then
        print_error "接続先を入力してください"
        return
    fi

    echo ""
    echo "接続テスト中... ($target)"
    echo ""

    # -v で詳細情報を表示、タイムアウト10秒
    if ssh -v -o ConnectTimeout=10 -o BatchMode=yes "$target" "echo '接続成功！'" 2>&1; then
        echo ""
        print_success "接続テスト成功"
    else
        echo ""
        print_error "接続テスト失敗（上記のデバッグ情報を確認してください）"
    fi
}

# --- メインメニュー ---
main_menu() {
    while true; do
        print_header "SSH鍵管理ツール"
        echo "  1) 鍵の一覧表示"
        echo "  2) 新しい鍵ペアを生成"
        echo "  3) パーミッションを修正"
        echo "  4) ssh-agent に鍵を登録"
        echo "  5) SSH接続テスト"
        echo "  q) 終了"
        echo ""
        read -rp "選択: " choice

        case $choice in
            1) list_keys ;;
            2) generate_key ;;
            3) fix_permissions ;;
            4) add_to_agent ;;
            5) test_connection ;;
            q|Q) echo "終了します"; exit 0 ;;
            *) print_error "無効な選択です" ;;
        esac

        echo ""
        read -rp "Enter で続行..."
    done
}

# --- メイン処理 ---
main_menu

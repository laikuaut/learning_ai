# 実践課題12：総合演習 ─ セキュアSSH環境構築 ★5

> **難易度**: ★★★★★（総合）
> **前提知識**: 第1章〜第8章（SSH全般）
> **課題の種類**: 設計課題 / ミニプロジェクト
> **学習目標**: 企業レベルのSSH環境を一から設計・構築し、鍵管理・アクセス制御・監視・自動化を統合した実務レベルの環境をプロジェクトとして完成させる

---

## 課題の説明

あなたは新しいプロジェクトのインフラ担当者です。以下の要件を満たすSSH環境を設計・構築してください。

### プロジェクト要件

```
【チーム構成】
- 開発者: 5名（dev1〜dev5）
- 運用担当: 2名（ops1, ops2）
- SFTPユーザー: 1名（sftp1）

【サーバー構成】
+------------------+
|  インターネット   |
+--------+---------+
         |
+--------+---------+
|  踏み台サーバー   |  bastion.example.com
|  (DMZ)           |  Port: 2222
+--------+---------+
         |
+--------+---------+-------+---------+
|                  |                  |
+--------+---------+ +------+---------+ +------+---------+
|  Webサーバー     | |  APIサーバー   | |  DBサーバー    |
|  10.0.1.10       | |  10.0.1.20    | |  10.0.1.30    |
+------------------+ +---------------+ +---------------+

【要件】
1. 全ユーザーが公開鍵認証のみでログインできること
2. 踏み台サーバー経由でのみ内部サーバーにアクセスできること
3. 開発者はWeb・APIサーバーにアクセス可能、DBサーバーにはアクセス不可
4. 運用担当は全サーバーにアクセス可能
5. SFTPユーザーはWebサーバーのみにSFTP接続可能（シェル不可）
6. ローカルポートフォワーディングでDBに接続する経路を確保
7. 全接続のログを取得すること
8. 鍵の管理・配布を自動化すること
```

---

## 完成イメージ

```bash
# 開発者が1コマンドで環境セットアップ
$ ./setup_ssh_env.sh dev1
[OK] 鍵ペアを生成しました: id_ed25519_dev1
[OK] SSH設定ファイルを作成しました
[OK] 接続テスト: bastion → 成功
[OK] 接続テスト: web → 成功
[OK] 接続テスト: api → 成功
[情報] db → アクセス権限がありません

# ワンコマンドで接続
$ ssh web
dev1@web-server:~$

# DBへのポートフォワーディング（運用担当のみ）
$ ssh db-tunnel
# 別ターミナルで
$ mysql -h 127.0.0.1 -P 13306 -u appuser -p
```

---

## 課題の構成

この課題は5つのパートに分かれています。すべて完成させてください。

### パート1：SSH設定ファイルの設計
### パート2：鍵管理の自動化スクリプト
### パート3：サーバー側のsshd_config設計
### パート4：接続テストと監視スクリプト
### パート5：ドキュメント（運用手順書）の作成

---

## ステップガイド

<details>
<summary>パート1のヒント：SSH設定ファイルの設計</summary>

ロール（役割）ごとに異なる設定テンプレートを用意します。

```
# 開発者向けテンプレート
# - bastion, web, api にアクセス可能
# - db にはアクセス不可
# - ポートフォワーディング不可

# 運用担当向けテンプレート
# - 全サーバーにアクセス可能
# - DBへのポートフォワーディング設定付き
# - ControlMaster で接続を効率化
```

</details>

<details>
<summary>パート2のヒント：鍵管理の自動化</summary>

以下の機能を持つスクリプトを作成します。

1. ユーザー名とロールを指定して鍵ペアを生成
2. 公開鍵をサーバーに配布
3. SSH設定ファイルをロールに応じて生成
4. 接続テストを実行

```bash
./manage_ssh_keys.sh create dev1 developer
./manage_ssh_keys.sh create ops1 operator
./manage_ssh_keys.sh distribute dev1
./manage_ssh_keys.sh revoke dev1  # 退職時
```

</details>

<details>
<summary>パート3のヒント：sshd_configの設計</summary>

各サーバーのsshd_configで、ロールに応じたアクセス制御を行います。

```bash
# 踏み台サーバー
# - 全ユーザーが接続可能
# - コマンド実行は制限

# Webサーバー
# - 開発者、運用担当、SFTPユーザーが接続可能
# - SFTPユーザーはchrootで制限

# DBサーバー
# - 運用担当のみ接続可能
```

</details>

---

## 解答例

<details>
<summary>パート1の解答：SSH設定ファイルの設計</summary>

**開発者向け設定テンプレート（config_developer.template）:**

```
# ============================================
# SSH設定ファイル（開発者用）
# ユーザー: USERNAME
# 生成日: GENERATED_DATE
# ============================================

# --- 踏み台サーバー ---
Host bastion
    HostName bastion.example.com
    User USERNAME
    Port 2222
    IdentityFile ~/.ssh/id_ed25519_USERNAME
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600

# --- Webサーバー ---
Host web
    HostName 10.0.1.10
    User USERNAME
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_USERNAME
    IdentitiesOnly yes

# --- APIサーバー ---
Host api
    HostName 10.0.1.20
    User USERNAME
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_USERNAME
    IdentitiesOnly yes

# --- 共通設定 ---
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    AddKeysToAgent yes
    HashKnownHosts yes
```

**運用担当向け設定テンプレート（config_operator.template）:**

```
# ============================================
# SSH設定ファイル（運用担当用）
# ユーザー: USERNAME
# 生成日: GENERATED_DATE
# ============================================

# --- 踏み台サーバー ---
Host bastion
    HostName bastion.example.com
    User USERNAME
    Port 2222
    IdentityFile ~/.ssh/id_ed25519_USERNAME
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600

# --- Webサーバー ---
Host web
    HostName 10.0.1.10
    User USERNAME
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_USERNAME
    IdentitiesOnly yes

# --- APIサーバー ---
Host api
    HostName 10.0.1.20
    User USERNAME
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_USERNAME
    IdentitiesOnly yes

# --- DBサーバー ---
Host db
    HostName 10.0.1.30
    User USERNAME
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_USERNAME
    IdentitiesOnly yes

# --- DBポートフォワーディング ---
Host db-tunnel
    HostName 10.0.1.30
    User USERNAME
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_USERNAME
    LocalForward 13306 localhost:3306
    LocalForward 15432 localhost:5432
    RequestTTY no

# --- 共通設定 ---
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    AddKeysToAgent yes
    HashKnownHosts yes
```

</details>

<details>
<summary>パート2の解答：鍵管理の自動化スクリプト</summary>

```bash
#!/bin/bash
# SSH鍵管理・環境セットアップスクリプト
# 学べる内容：鍵の自動生成・配布・失効、ロールベースの設定管理
# 実行方法：bash manage_ssh_env.sh [create|distribute|revoke|test] <ユーザー名> <ロール>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SSH_DIR="$HOME/.ssh"
TEMPLATE_DIR="$SCRIPT_DIR/templates"
LOG_FILE="$SCRIPT_DIR/ssh_management.log"

# サーバー定義
BASTION="bastion.example.com"
BASTION_PORT="2222"
declare -A SERVERS=(
    ["web"]="10.0.1.10"
    ["api"]="10.0.1.20"
    ["db"]="10.0.1.30"
)

# ロールごとのアクセス権
declare -A ROLE_ACCESS=(
    ["developer"]="bastion web api"
    ["operator"]="bastion web api db"
    ["sftp"]="bastion web"
)

# === ログ関数 ===

log() {
    local timestamp
    timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] $1" >> "$LOG_FILE"
    echo "$1"
}

# === 鍵の生成 ===

create_user() {
    local username="$1"
    local role="$2"
    local key_name="id_ed25519_${username}"
    local key_path="$SSH_DIR/$key_name"

    log "--- ユーザー作成: $username (ロール: $role) ---"

    # ロールの確認
    if [ -z "${ROLE_ACCESS[$role]:-}" ]; then
        log "[エラー] 不明なロール: $role"
        log "有効なロール: developer, operator, sftp"
        return 1
    fi

    # ディレクトリ準備
    mkdir -p "$SSH_DIR/sockets"
    chmod 700 "$SSH_DIR"

    # 鍵ペアの生成
    if [ -f "$key_path" ]; then
        log "[スキップ] 鍵は既に存在します: $key_path"
    else
        ssh-keygen -t ed25519 \
            -C "${username}@project-$(date +%Y%m%d)" \
            -f "$key_path" \
            -N ""
        chmod 600 "$key_path"
        chmod 644 "${key_path}.pub"
        log "[OK] 鍵ペアを生成しました: $key_name"
    fi

    # SSH設定ファイルの生成
    generate_config "$username" "$role"

    log "[OK] ユーザー $username ($role) の作成が完了しました"
    log ""
    log "次のステップ:"
    log "  1. 公開鍵をサーバー管理者に送付: $key_path.pub"
    log "  2. 配布完了後にテスト: $0 test $username $role"
}

# === 設定ファイル生成 ===

generate_config() {
    local username="$1"
    local role="$2"
    local config_file="$SSH_DIR/config"
    local access_servers="${ROLE_ACCESS[$role]}"

    # バックアップ
    if [ -f "$config_file" ]; then
        cp "$config_file" "${config_file}.backup.$(date +%Y%m%d%H%M%S)"
    fi

    # ヘッダー
    cat > "$config_file" << EOF
# ============================================
# SSH設定ファイル
# ユーザー: $username
# ロール: $role
# 生成日: $(date '+%Y-%m-%d %H:%M:%S')
# ============================================

EOF

    # 踏み台サーバー
    cat >> "$config_file" << EOF
# --- 踏み台サーバー ---
Host bastion
    HostName $BASTION
    User $username
    Port $BASTION_PORT
    IdentityFile ~/.ssh/id_ed25519_${username}
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600

EOF

    # アクセス可能なサーバーの設定を追加
    for server_name in web api db; do
        local server_ip="${SERVERS[$server_name]}"

        if echo "$access_servers" | grep -qw "$server_name"; then
            # SFTPユーザーの場合はWebのみ特別設定
            if [ "$role" = "sftp" ] && [ "$server_name" = "web" ]; then
                cat >> "$config_file" << EOF
# --- Webサーバー（SFTPのみ） ---
Host web
    HostName $server_ip
    User $username
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_${username}
    IdentitiesOnly yes
    # SFTPのみ使用（シェル接続は不可）

EOF
            else
                cat >> "$config_file" << EOF
# --- ${server_name}サーバー ---
Host $server_name
    HostName $server_ip
    User $username
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_${username}
    IdentitiesOnly yes

EOF
            fi

            # 運用担当のDB接続にはポートフォワーディング追加
            if [ "$role" = "operator" ] && [ "$server_name" = "db" ]; then
                cat >> "$config_file" << EOF
# --- DBポートフォワーディング ---
Host db-tunnel
    HostName $server_ip
    User $username
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_${username}
    IdentitiesOnly yes
    LocalForward 13306 localhost:3306
    LocalForward 15432 localhost:5432
    RequestTTY no

EOF
            fi
        fi
    done

    # 共通設定
    cat >> "$config_file" << 'EOF'
# --- 共通設定 ---
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    AddKeysToAgent yes
    HashKnownHosts yes
EOF

    chmod 600 "$config_file"
    log "[OK] SSH設定ファイルを生成しました: $config_file"
}

# === 公開鍵の配布 ===

distribute_key() {
    local username="$1"
    local role="$2"
    local key_path="$SSH_DIR/id_ed25519_${username}.pub"
    local access_servers="${ROLE_ACCESS[$role]}"

    log "--- 公開鍵の配布: $username ---"

    if [ ! -f "$key_path" ]; then
        log "[エラー] 公開鍵が見つかりません: $key_path"
        return 1
    fi

    local pub_key
    pub_key=$(cat "$key_path")

    # 踏み台サーバーに配布
    log "踏み台サーバーに公開鍵を配布中..."
    ssh -p "$BASTION_PORT" "admin@$BASTION" << EOF
sudo mkdir -p /home/$username/.ssh
echo '$pub_key' | sudo tee -a /home/$username/.ssh/authorized_keys
sudo chmod 700 /home/$username/.ssh
sudo chmod 600 /home/$username/.ssh/authorized_keys
sudo chown -R $username:$username /home/$username/.ssh
EOF
    log "[OK] 踏み台サーバーへの配布完了"

    # 内部サーバーに配布
    for server_name in web api db; do
        if echo "$access_servers" | grep -qw "$server_name"; then
            local server_ip="${SERVERS[$server_name]}"
            log "${server_name}サーバー ($server_ip) に配布中..."
            ssh -J "admin@$BASTION:$BASTION_PORT" "admin@$server_ip" << EOF
sudo mkdir -p /home/$username/.ssh
echo '$pub_key' | sudo tee -a /home/$username/.ssh/authorized_keys
sudo chmod 700 /home/$username/.ssh
sudo chmod 600 /home/$username/.ssh/authorized_keys
sudo chown -R $username:$username /home/$username/.ssh
EOF
            log "[OK] ${server_name}サーバーへの配布完了"
        fi
    done

    log "[OK] 公開鍵の配布が完了しました"
}

# === 鍵の失効（退職時等） ===

revoke_user() {
    local username="$1"
    local role="$2"
    local access_servers="${ROLE_ACCESS[$role]}"

    log "--- ユーザー失効: $username ---"
    log "[警告] $username の全サーバーからのアクセスを無効化します"

    # 踏み台サーバーから削除
    log "踏み台サーバーから鍵を削除中..."
    ssh -p "$BASTION_PORT" "admin@$BASTION" \
        "sudo sed -i '/${username}/d' /home/$username/.ssh/authorized_keys 2>/dev/null; echo 'done'" || true
    log "[OK] 踏み台サーバーから削除"

    # 内部サーバーから削除
    for server_name in web api db; do
        if echo "$access_servers" | grep -qw "$server_name"; then
            local server_ip="${SERVERS[$server_name]}"
            log "${server_name}サーバーから鍵を削除中..."
            ssh -J "admin@$BASTION:$BASTION_PORT" "admin@$server_ip" \
                "sudo sed -i '/${username}/d' /home/$username/.ssh/authorized_keys 2>/dev/null; echo 'done'" || true
            log "[OK] ${server_name}サーバーから削除"
        fi
    done

    # ローカルの鍵を無効化（削除はしない）
    local key_path="$SSH_DIR/id_ed25519_${username}"
    if [ -f "$key_path" ]; then
        mv "$key_path" "${key_path}.revoked.$(date +%Y%m%d)"
        mv "${key_path}.pub" "${key_path}.pub.revoked.$(date +%Y%m%d)"
        log "[OK] ローカル鍵を .revoked に名前変更しました"
    fi

    log "[OK] ユーザー $username の失効処理が完了しました"
}

# === 接続テスト ===

test_connection() {
    local username="$1"
    local role="$2"
    local access_servers="${ROLE_ACCESS[$role]}"

    log "--- 接続テスト: $username ($role) ---"

    # 踏み台サーバー
    echo -n "  bastion: "
    if ssh -o ConnectTimeout=5 -o BatchMode=yes bastion "echo OK" 2>/dev/null; then
        log "[OK] bastion 接続成功"
    else
        log "[NG] bastion 接続失敗"
    fi

    # 内部サーバー
    for server_name in web api db; do
        echo -n "  $server_name: "
        if echo "$access_servers" | grep -qw "$server_name"; then
            if ssh -o ConnectTimeout=10 -o BatchMode=yes "$server_name" "echo OK" 2>/dev/null; then
                log "[OK] $server_name 接続成功"
            else
                log "[NG] $server_name 接続失敗"
            fi
        else
            echo "アクセス権限なし（正常）"
            log "[情報] $server_name アクセス権限なし"
        fi
    done
}

# === メイン処理 ===

ACTION="${1:-help}"
USERNAME="${2:-}"
ROLE="${3:-developer}"

case "$ACTION" in
    create)
        if [ -z "$USERNAME" ]; then
            echo "使い方: $0 create <ユーザー名> [ロール]"
            echo "ロール: developer（デフォルト）, operator, sftp"
            exit 1
        fi
        create_user "$USERNAME" "$ROLE"
        ;;
    distribute)
        if [ -z "$USERNAME" ]; then
            echo "使い方: $0 distribute <ユーザー名> <ロール>"
            exit 1
        fi
        distribute_key "$USERNAME" "$ROLE"
        ;;
    revoke)
        if [ -z "$USERNAME" ]; then
            echo "使い方: $0 revoke <ユーザー名> <ロール>"
            exit 1
        fi
        revoke_user "$USERNAME" "$ROLE"
        ;;
    test)
        if [ -z "$USERNAME" ]; then
            echo "使い方: $0 test <ユーザー名> [ロール]"
            exit 1
        fi
        test_connection "$USERNAME" "$ROLE"
        ;;
    help|*)
        echo "===== SSH環境管理ツール ====="
        echo ""
        echo "使い方: $0 [コマンド] <ユーザー名> [ロール]"
        echo ""
        echo "コマンド:"
        echo "  create      鍵ペア生成 + SSH設定ファイル生成"
        echo "  distribute  公開鍵をサーバーに配布"
        echo "  revoke      ユーザーのアクセスを失効"
        echo "  test        接続テスト"
        echo ""
        echo "ロール:"
        echo "  developer   開発者（web, api にアクセス可能）"
        echo "  operator    運用担当（全サーバー + DB転送設定）"
        echo "  sftp        SFTPユーザー（web にSFTPのみ）"
        echo ""
        echo "例:"
        echo "  $0 create dev1 developer"
        echo "  $0 create ops1 operator"
        echo "  $0 distribute dev1 developer"
        echo "  $0 test dev1 developer"
        echo "  $0 revoke dev1 developer"
        ;;
esac
```

</details>

<details>
<summary>パート3の解答：サーバー側のsshd_config設計</summary>

**踏み台サーバー（bastion）の sshd_config:**

```bash
# /etc/ssh/sshd_config - 踏み台サーバー

Port 2222
AddressFamily inet
ListenAddress 0.0.0.0

# 認証
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no
MaxAuthTries 3
LoginGraceTime 30

# アクセス制御
AllowGroups sshusers
DenyUsers root

# セキュリティ強化
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

# ログ
SyslogFacility AUTH
LogLevel VERBOSE

# セッション
X11Forwarding no
AllowTcpForwarding yes
GatewayPorts no
ClientAliveInterval 300
ClientAliveCountMax 2
MaxSessions 10

Banner /etc/ssh/banner.txt
```

**Webサーバーの sshd_config:**

```bash
# /etc/ssh/sshd_config - Webサーバー

Port 22
ListenAddress 10.0.1.10

PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
MaxAuthTries 3

AllowGroups developers operators sftpusers
DenyUsers root

SyslogFacility AUTH
LogLevel VERBOSE

X11Forwarding no
AllowTcpForwarding no
ClientAliveInterval 300
ClientAliveCountMax 2

Subsystem sftp internal-sftp

# SFTPユーザーの制限
Match Group sftpusers
    ChrootDirectory /home/%u
    ForceCommand internal-sftp
    AllowTcpForwarding no
    PermitTunnel no

# 開発者の設定
Match Group developers
    AllowTcpForwarding no
    MaxSessions 5
```

**DBサーバーの sshd_config:**

```bash
# /etc/ssh/sshd_config - DBサーバー

Port 22
ListenAddress 10.0.1.30

PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
MaxAuthTries 3

# 運用担当のみアクセス可能
AllowGroups operators
DenyUsers root

SyslogFacility AUTH
LogLevel VERBOSE

X11Forwarding no
AllowTcpForwarding no
ClientAliveInterval 300
ClientAliveCountMax 2

# 運用担当にはポートフォワーディングを許可
Match Group operators
    AllowTcpForwarding yes
    MaxSessions 5
```

</details>

<details>
<summary>パート4の解答：接続テストと監視スクリプト</summary>

```bash
#!/bin/bash
# SSH接続監視スクリプト
# 学べる内容：定期的な接続テスト、ログ監視、アラート
# 実行方法：bash ssh_monitor.sh [test|audit|report]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$SCRIPT_DIR/monitor_logs"
REPORT_FILE="$LOG_DIR/report_$(date +%Y%m%d).txt"

mkdir -p "$LOG_DIR"

# サーバー定義
declare -A SERVERS=(
    ["bastion"]="bastion"
    ["web"]="web"
    ["api"]="api"
    ["db"]="db"
)

# === 接続テスト ===

do_test() {
    echo "===== SSH接続テスト ====="
    echo "日時: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    local pass=0 fail=0

    for name in bastion web api db; do
        echo -n "  $name: "
        local start_time end_time elapsed

        start_time=$(date +%s%N)
        if ssh -o ConnectTimeout=5 -o BatchMode=yes "$name" "echo OK" 2>/dev/null; then
            end_time=$(date +%s%N)
            elapsed=$(( (end_time - start_time) / 1000000 ))
            echo " (${elapsed}ms)"
            pass=$((pass + 1))
        else
            echo "失敗"
            fail=$((fail + 1))
        fi
    done

    echo ""
    echo "結果: 成功=$pass, 失敗=$fail"

    if [ "$fail" -gt 0 ]; then
        echo "[警告] 一部のサーバーに接続できません"
        return 1
    fi
}

# === セキュリティ監査 ===

do_audit() {
    echo "===== SSHセキュリティ監査 ====="
    echo "日時: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    # ローカルの鍵ファイル監査
    echo "--- ローカル鍵ファイルの監査 ---"
    local issues=0

    for key_file in ~/.ssh/id_*; do
        [[ "$key_file" == *.pub ]] && continue
        [[ "$key_file" == *.revoked.* ]] && continue
        [ ! -f "$key_file" ] && continue

        local perm
        perm=$(stat -c '%a' "$key_file" 2>/dev/null || stat -f '%Lp' "$key_file" 2>/dev/null)

        if [ "$perm" != "600" ]; then
            echo "  [NG] $key_file: パーミッション=$perm (期待: 600)"
            issues=$((issues + 1))
        else
            echo "  [OK] $key_file: パーミッション=$perm"
        fi
    done

    # ~/.ssh/config の監査
    echo ""
    echo "--- SSH設定ファイルの監査 ---"

    if [ -f ~/.ssh/config ]; then
        local config_perm
        config_perm=$(stat -c '%a' ~/.ssh/config 2>/dev/null || stat -f '%Lp' ~/.ssh/config 2>/dev/null)

        if [ "$config_perm" != "600" ]; then
            echo "  [NG] ~/.ssh/config: パーミッション=$config_perm (期待: 600)"
            issues=$((issues + 1))
        else
            echo "  [OK] ~/.ssh/config: パーミッション=$config_perm"
        fi

        # パスワード認証が有効な設定がないか確認
        if grep -qi "PasswordAuthentication yes" ~/.ssh/config 2>/dev/null; then
            echo "  [警告] パスワード認証が有効な設定があります"
            issues=$((issues + 1))
        fi

        # ForwardAgent が有効な設定を確認
        if grep -qi "ForwardAgent yes" ~/.ssh/config 2>/dev/null; then
            echo "  [注意] エージェントフォワーディングが有効な設定があります"
        fi
    fi

    # known_hosts の確認
    echo ""
    echo "--- known_hosts の監査 ---"
    if [ -f ~/.ssh/known_hosts ]; then
        local host_count
        host_count=$(wc -l < ~/.ssh/known_hosts)
        echo "  登録ホスト数: $host_count"

        # ハッシュ化されているか確認
        if head -1 ~/.ssh/known_hosts | grep -q "^|1|"; then
            echo "  [OK] ホスト名がハッシュ化されています"
        else
            echo "  [注意] ホスト名がハッシュ化されていません"
            echo "       ssh-keygen -H で一括ハッシュ化できます"
        fi
    fi

    echo ""
    if [ "$issues" -eq 0 ]; then
        echo "監査結果: 問題なし"
    else
        echo "監査結果: ${issues}件の問題が見つかりました"
    fi
}

# === レポート生成 ===

do_report() {
    echo "===== SSH環境レポート ====="

    {
        echo "SSH環境レポート"
        echo "生成日時: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "========================================="
        echo ""

        echo "[鍵ファイル一覧]"
        ls -la ~/.ssh/id_* 2>/dev/null | grep -v ".pub$" | while read -r line; do
            echo "  $line"
        done
        echo ""

        echo "[SSH設定のホストエントリ]"
        grep "^Host " ~/.ssh/config 2>/dev/null | while read -r line; do
            echo "  $line"
        done
        echo ""

        echo "[known_hosts の統計]"
        if [ -f ~/.ssh/known_hosts ]; then
            echo "  ホスト数: $(wc -l < ~/.ssh/known_hosts)"
        else
            echo "  ファイルなし"
        fi
        echo ""

        echo "[ssh-agent の状態]"
        if [ -n "${SSH_AGENT_PID:-}" ] && kill -0 "$SSH_AGENT_PID" 2>/dev/null; then
            echo "  稼働中 (PID: $SSH_AGENT_PID)"
            echo "  登録済み鍵:"
            ssh-add -l 2>/dev/null | while read -r line; do
                echo "    $line"
            done
        else
            echo "  未起動"
        fi
    } | tee "$REPORT_FILE"

    echo ""
    echo "レポートを保存しました: $REPORT_FILE"
}

# === メイン処理 ===

ACTION="${1:-help}"

case "$ACTION" in
    test)    do_test ;;
    audit)   do_audit ;;
    report)  do_report ;;
    *)
        echo "使い方: $0 [test|audit|report]"
        echo ""
        echo "  test    全サーバーへの接続テスト"
        echo "  audit   セキュリティ監査"
        echo "  report  環境レポート生成"
        ;;
esac
```

</details>

<details>
<summary>パート5の解答：運用手順書の要点</summary>

以下の内容を運用手順書としてまとめます。

### 1. 新規ユーザー追加手順

```
1. 管理者が manage_ssh_env.sh create <ユーザー名> <ロール> を実行
2. 生成された公開鍵をサーバー管理者に送付
3. サーバー管理者が manage_ssh_env.sh distribute <ユーザー名> <ロール> を実行
4. ユーザーに SSH設定ファイル と 秘密鍵 を安全に渡す
5. ユーザーが manage_ssh_env.sh test <ユーザー名> <ロール> で接続確認
```

### 2. ユーザー退職・異動時の手順

```
1. 管理者が manage_ssh_env.sh revoke <ユーザー名> <ロール> を実行
2. 全サーバーの authorized_keys からユーザーの鍵が削除されたことを確認
3. 必要に応じてサーバーのユーザーアカウントも無効化
4. 監査ログで最終ログイン日時を記録
```

### 3. 定期的なセキュリティ確認

```
- 毎日: ssh_monitor.sh test で全サーバーの接続テスト
- 毎週: ssh_monitor.sh audit でセキュリティ監査
- 毎月: ssh_monitor.sh report で環境レポート生成
- 四半期: 全鍵のローテーション（新しい鍵の生成と配布）
```

### 4. トラブルシューティングの基本手順

```
1. ssh -vvv <ホスト名> で詳細ログを確認
2. サーバー側の /var/log/auth.log を確認
3. パーミッションの確認（~/.ssh: 700, 秘密鍵: 600, authorized_keys: 600）
4. 鍵のフィンガープリントが一致するか確認
5. ControlMaster のソケットが残っている場合は削除: rm ~/.ssh/sockets/*
```

</details>

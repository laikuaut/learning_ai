# 実践課題11：リファクタリング ─ SSH運用スクリプト改善 ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第3章（公開鍵認証の設定）、第4章（SSH設定ファイル）、第5章（ファイル転送）、第8章（SSHのセキュリティと運用）
> **課題の種類**: リファクタリング
> **学習目標**: 「動くが保守性が低い」SSH運用スクリプトを段階的に改善し、安全で再利用しやすい構造にリファクタリングする力を養う

---

## 課題の説明

以下は、チーム内で使われている「SSH一括操作スクリプト」の全コードです。**正しく動作します**が、以下の問題を抱えています。

- サーバー情報がスクリプト内にハードコードされている
- エラーハンドリングがない
- パスワードがスクリプト内に平文で書かれている
- 同じパターンのコードが繰り返されている
- ログ出力がない
- 設定とロジックが分離されていない

**このスクリプトを段階的にリファクタリングしてください。**

### ゴール

1. **ステップ1**: ハードコードされた値を外部設定ファイルに分離する
2. **ステップ2**: 繰り返し処理を関数に切り出す
3. **ステップ3**: エラーハンドリングとログ出力を追加する

---

## リファクタリング対象のスクリプト

以下を `ssh_batch_legacy.sh` として保存してください。

```bash
#!/bin/bash
# サーバー一括操作スクリプト（レガシー版）
# 動作するが保守性が低いコード。リファクタリングしてください。

# サーバー情報（ハードコード）
SERVER1="192.168.1.101"
SERVER2="192.168.1.102"
SERVER3="192.168.1.103"
USER="deploy"
KEY="/home/deploy/.ssh/id_rsa"

echo "===== デプロイ開始 ====="
echo "日時: $(date)"

# サーバー1のディスク確認
echo "--- サーバー1のディスク確認 ---"
ssh -i $KEY $USER@$SERVER1 "df -h / | tail -1"

# サーバー2のディスク確認
echo "--- サーバー2のディスク確認 ---"
ssh -i $KEY $USER@$SERVER2 "df -h / | tail -1"

# サーバー3のディスク確認
echo "--- サーバー3のディスク確認 ---"
ssh -i $KEY $USER@$SERVER3 "df -h / | tail -1"

# サーバー1にファイルをコピー
echo "--- サーバー1にデプロイ ---"
scp -i $KEY ./app.tar.gz $USER@$SERVER1:/tmp/
ssh -i $KEY $USER@$SERVER1 "cd /var/www/app && tar xzf /tmp/app.tar.gz && sudo systemctl restart app"
echo "サーバー1完了"

# サーバー2にファイルをコピー
echo "--- サーバー2にデプロイ ---"
scp -i $KEY ./app.tar.gz $USER@$SERVER2:/tmp/
ssh -i $KEY $USER@$SERVER2 "cd /var/www/app && tar xzf /tmp/app.tar.gz && sudo systemctl restart app"
echo "サーバー2完了"

# サーバー3にファイルをコピー
echo "--- サーバー3にデプロイ ---"
scp -i $KEY ./app.tar.gz $USER@$SERVER3:/tmp/
ssh -i $KEY $USER@$SERVER3 "cd /var/www/app && tar xzf /tmp/app.tar.gz && sudo systemctl restart app"
echo "サーバー3完了"

# ヘルスチェック
echo "--- ヘルスチェック ---"
ssh -i $KEY $USER@$SERVER1 "curl -s http://localhost:8080/health"
echo ""
ssh -i $KEY $USER@$SERVER2 "curl -s http://localhost:8080/health"
echo ""
ssh -i $KEY $USER@$SERVER3 "curl -s http://localhost:8080/health"
echo ""

echo "===== デプロイ完了 ====="
```

---

## ステップガイド

<details>
<summary>ステップ1：設定の外部化</summary>

ハードコードされたサーバー情報を外部の設定ファイルに移動します。

```bash
# servers.conf（設定ファイルの例）
# 形式: サーバー名 IPアドレス
web1 192.168.1.101
web2 192.168.1.102
web3 192.168.1.103
```

スクリプトから設定ファイルを読み込む方法：
```bash
while read -r name ip; do
    [[ "$name" =~ ^#.*$ ]] && continue  # コメント行スキップ
    [ -z "$name" ] && continue          # 空行スキップ
    echo "サーバー: $name ($ip)"
done < servers.conf
```

</details>

<details>
<summary>ステップ2：関数化</summary>

繰り返されている処理を関数に切り出します。

```bash
# リモートコマンド実行の関数
run_remote() {
    local server="$1"
    local command="$2"
    ssh -i "$KEY" "$USER@$server" "$command"
}

# ファイル転送の関数
transfer_file() {
    local server="$1"
    local local_path="$2"
    local remote_path="$3"
    scp -i "$KEY" "$local_path" "$USER@$server:$remote_path"
}
```

</details>

<details>
<summary>ステップ3：エラーハンドリングとログ</summary>

各操作の成否を判定し、ログファイルに記録します。

```bash
LOG_FILE="deploy_$(date +%Y%m%d_%H%M%S).log"

log() {
    local message="$1"
    local timestamp
    timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

run_remote() {
    local server="$1"
    local command="$2"
    if ssh -i "$KEY" "$USER@$server" "$command"; then
        log "[OK] $server: $command"
    else
        log "[NG] $server: $command (終了コード: $?)"
        return 1
    fi
}
```

</details>

---

## 解答例

<details>
<summary>解答例（ステップ1：設定の外部化）</summary>

**設定ファイル（servers.conf）:**

```bash
# サーバー一覧
# 形式: 名前 IPアドレス 役割
web1 192.168.1.101 web
web2 192.168.1.102 web
web3 192.168.1.103 web
```

**設定ファイル（deploy.conf）:**

```bash
# デプロイ設定
DEPLOY_USER="deploy"
DEPLOY_KEY="$HOME/.ssh/id_ed25519_work"
APP_ARCHIVE="./app.tar.gz"
REMOTE_TMP="/tmp"
APP_DIR="/var/www/app"
APP_SERVICE="app"
HEALTH_URL="http://localhost:8080/health"
```

**スクリプト（改善版 ステップ1）:**

```bash
#!/bin/bash
# サーバー一括操作スクリプト（ステップ1：設定の外部化）

# 設定ファイルの読み込み
source ./deploy.conf

echo "===== デプロイ開始 ====="
echo "日時: $(date)"

# サーバー一覧を読み込んでループ処理
while read -r name ip role; do
    [[ "$name" =~ ^#.*$ ]] && continue
    [ -z "$name" ] && continue

    echo ""
    echo "--- $name ($ip) のディスク確認 ---"
    ssh -i "$DEPLOY_KEY" "$DEPLOY_USER@$ip" "df -h / | tail -1"

    echo "--- $name ($ip) にデプロイ ---"
    scp -i "$DEPLOY_KEY" "$APP_ARCHIVE" "$DEPLOY_USER@$ip:$REMOTE_TMP/"
    ssh -i "$DEPLOY_KEY" "$DEPLOY_USER@$ip" "cd $APP_DIR && tar xzf $REMOTE_TMP/$(basename $APP_ARCHIVE) && sudo systemctl restart $APP_SERVICE"
    echo "$name 完了"
done < servers.conf

echo ""
echo "--- ヘルスチェック ---"
while read -r name ip role; do
    [[ "$name" =~ ^#.*$ ]] && continue
    [ -z "$name" ] && continue
    echo -n "$name: "
    ssh -i "$DEPLOY_KEY" "$DEPLOY_USER@$ip" "curl -s $HEALTH_URL"
    echo ""
done < servers.conf

echo ""
echo "===== デプロイ完了 ====="
```

</details>

<details>
<summary>解答例（ステップ2+3：関数化 + エラーハンドリング ─ 完成版）</summary>

**設定ファイル（servers.conf）:**

```bash
# サーバー一覧
# 形式: 名前 IPアドレス 役割
web1 192.168.1.101 web
web2 192.168.1.102 web
web3 192.168.1.103 web
```

**設定ファイル（deploy.conf）:**

```bash
# デプロイ設定
DEPLOY_USER="deploy"
DEPLOY_KEY="$HOME/.ssh/id_ed25519_work"
APP_ARCHIVE="./app.tar.gz"
REMOTE_TMP="/tmp"
APP_DIR="/var/www/app"
APP_SERVICE="app"
HEALTH_URL="http://localhost:8080/health"
HEALTH_TIMEOUT=10
SSH_TIMEOUT=10
```

**スクリプト（完成版）:**

```bash
#!/bin/bash
# サーバー一括デプロイスクリプト（リファクタリング完成版）
# 学べる内容：設定分離、関数化、エラーハンドリング、ログ管理
# 実行方法：bash ssh_batch_deploy.sh [check|deploy|health|rollback]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVERS_FILE="$SCRIPT_DIR/servers.conf"
CONFIG_FILE="$SCRIPT_DIR/deploy.conf"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/deploy_$(date +%Y%m%d_%H%M%S).log"

# === 設定の読み込み ===

if [ ! -f "$CONFIG_FILE" ]; then
    echo "[エラー] 設定ファイルが見つかりません: $CONFIG_FILE"
    exit 1
fi
source "$CONFIG_FILE"

if [ ! -f "$SERVERS_FILE" ]; then
    echo "[エラー] サーバー一覧が見つかりません: $SERVERS_FILE"
    exit 1
fi

mkdir -p "$LOG_DIR"

# === ログ関数 ===

log() {
    local level="$1"
    local message="$2"
    local timestamp
    timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

log_info()  { log "INFO"  "$1"; }
log_ok()    { log " OK "  "$1"; }
log_error() { log "ERROR" "$1"; }
log_warn()  { log "WARN"  "$1"; }

# === SSH操作関数 ===

run_remote() {
    local name="$1"
    local ip="$2"
    local command="$3"
    local description="${4:-コマンド実行}"

    if ssh -i "$DEPLOY_KEY" \
           -o ConnectTimeout="$SSH_TIMEOUT" \
           -o BatchMode=yes \
           -o StrictHostKeyChecking=accept-new \
           "$DEPLOY_USER@$ip" "$command" 2>>"$LOG_FILE"; then
        log_ok "$name: $description"
        return 0
    else
        log_error "$name: $description (終了コード: $?)"
        return 1
    fi
}

transfer_file() {
    local name="$1"
    local ip="$2"
    local local_path="$3"
    local remote_path="$4"

    if scp -i "$DEPLOY_KEY" \
           -o ConnectTimeout="$SSH_TIMEOUT" \
           -o BatchMode=yes \
           "$local_path" "$DEPLOY_USER@$ip:$remote_path" 2>>"$LOG_FILE"; then
        log_ok "$name: ファイル転送 $(basename "$local_path")"
        return 0
    else
        log_error "$name: ファイル転送失敗 $(basename "$local_path")"
        return 1
    fi
}

# === サーバー一覧の読み込み ===

read_servers() {
    local callback="$1"
    local success=0
    local fail=0

    while read -r name ip role; do
        [[ "$name" =~ ^#.*$ ]] && continue
        [ -z "$name" ] && continue

        if "$callback" "$name" "$ip" "$role"; then
            success=$((success + 1))
        else
            fail=$((fail + 1))
        fi
    done < "$SERVERS_FILE"

    log_info "結果: 成功=$success, 失敗=$fail"
    [ "$fail" -eq 0 ]
}

# === 操作関数 ===

do_check() {
    log_info "--- ディスク＆メモリ確認 ---"

    check_server() {
        local name="$1" ip="$2" role="$3"
        echo ""
        echo "[$name ($ip)]"
        run_remote "$name" "$ip" "echo 'ディスク:' && df -h / | tail -1 && echo 'メモリ:' && free -h | grep Mem" "システム情報取得"
    }

    read_servers check_server
}

do_deploy() {
    log_info "===== デプロイ開始 ====="

    # デプロイ対象の確認
    if [ ! -f "$APP_ARCHIVE" ]; then
        log_error "デプロイ対象が見つかりません: $APP_ARCHIVE"
        return 1
    fi

    local archive_name
    archive_name=$(basename "$APP_ARCHIVE")
    log_info "デプロイ対象: $archive_name ($(du -h "$APP_ARCHIVE" | awk '{print $1}'))"

    deploy_server() {
        local name="$1" ip="$2" role="$3"
        echo ""
        log_info "$name ($ip): デプロイ開始"

        # ディスク空き容量の事前確認
        local avail
        avail=$(ssh -i "$DEPLOY_KEY" -o ConnectTimeout="$SSH_TIMEOUT" -o BatchMode=yes \
            "$DEPLOY_USER@$ip" "df / | tail -1 | awk '{print \$4}'" 2>/dev/null)
        if [ -n "$avail" ] && [ "$avail" -lt 1048576 ] 2>/dev/null; then
            log_warn "$name: ディスク空き容量が1GB未満です"
        fi

        # バックアップ作成
        run_remote "$name" "$ip" \
            "[ -d '$APP_DIR' ] && sudo tar czf '$REMOTE_TMP/app_backup_\$(date +%Y%m%d_%H%M%S).tar.gz' -C '$APP_DIR' . || true" \
            "バックアップ作成" || true

        # ファイル転送
        transfer_file "$name" "$ip" "$APP_ARCHIVE" "$REMOTE_TMP/" || return 1

        # デプロイ（展開とサービス再起動）
        run_remote "$name" "$ip" \
            "cd '$APP_DIR' && sudo tar xzf '$REMOTE_TMP/$archive_name' && sudo systemctl restart '$APP_SERVICE'" \
            "デプロイ実行" || return 1

        # 一時ファイルの削除
        run_remote "$name" "$ip" "rm -f '$REMOTE_TMP/$archive_name'" "一時ファイル削除" || true

        log_ok "$name: デプロイ完了"
    }

    read_servers deploy_server
}

do_health() {
    log_info "--- ヘルスチェック ---"

    health_check() {
        local name="$1" ip="$2" role="$3"
        local result
        result=$(ssh -i "$DEPLOY_KEY" -o ConnectTimeout="$SSH_TIMEOUT" -o BatchMode=yes \
            "$DEPLOY_USER@$ip" "curl -sf --max-time $HEALTH_TIMEOUT '$HEALTH_URL'" 2>/dev/null)

        if [ $? -eq 0 ]; then
            log_ok "$name: ヘルスチェック OK ($result)"
        else
            log_error "$name: ヘルスチェック NG"
            return 1
        fi
    }

    read_servers health_check
}

do_rollback() {
    log_info "===== ロールバック開始 ====="

    rollback_server() {
        local name="$1" ip="$2" role="$3"
        log_info "$name: ロールバック"

        # 最新のバックアップを取得
        local backup
        backup=$(ssh -i "$DEPLOY_KEY" -o ConnectTimeout="$SSH_TIMEOUT" -o BatchMode=yes \
            "$DEPLOY_USER@$ip" "ls -t '$REMOTE_TMP'/app_backup_*.tar.gz 2>/dev/null | head -1")

        if [ -z "$backup" ]; then
            log_error "$name: バックアップが見つかりません"
            return 1
        fi

        run_remote "$name" "$ip" \
            "cd '$APP_DIR' && sudo tar xzf '$backup' && sudo systemctl restart '$APP_SERVICE'" \
            "ロールバック実行"
    }

    read_servers rollback_server
}

# === メイン処理 ===

ACTION="${1:-help}"

log_info "コマンド: $ACTION"

case "$ACTION" in
    check)    do_check ;;
    deploy)   do_deploy && do_health ;;
    health)   do_health ;;
    rollback) do_rollback && do_health ;;
    *)
        echo "===== サーバー一括デプロイツール ====="
        echo ""
        echo "使い方: $0 [コマンド]"
        echo ""
        echo "コマンド:"
        echo "  check     全サーバーのディスク・メモリ確認"
        echo "  deploy    デプロイ実行（ヘルスチェック付き）"
        echo "  health    ヘルスチェックのみ実行"
        echo "  rollback  直前のバックアップにロールバック"
        echo ""
        echo "設定ファイル:"
        echo "  $CONFIG_FILE   デプロイ設定"
        echo "  $SERVERS_FILE  サーバー一覧"
        echo "  $LOG_DIR/      ログファイル"
        ;;
esac

log_info "===== 完了 ====="
```

**レガシー版からの改善点:**

| 項目 | レガシー版 | リファクタリング版 |
|------|----------|-----------------|
| サーバー情報 | ハードコード | 外部ファイル（servers.conf） |
| 設定値 | スクリプト内に散在 | 外部ファイル（deploy.conf） |
| 繰り返し | コピー&ペースト | 関数 + コールバック |
| エラー処理 | なし | 全操作で成否判定 |
| ログ | echoのみ | タイムスタンプ付きログファイル |
| バックアップ | なし | デプロイ前に自動作成 |
| ロールバック | なし | ロールバック機能追加 |
| ディスク確認 | 表示のみ | 不足時に警告 |
| SSH接続 | タイムアウトなし | ConnectTimeout設定 |

</details>

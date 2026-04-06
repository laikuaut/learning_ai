# 実践課題08：多段SSH接続と踏み台サーバー ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第4章（SSH設定ファイル）、第7章（SSHエージェントと多段接続）
> **課題の種類**: ミニプロジェクト
> **学習目標**: 踏み台サーバー（bastion host）を経由した多段SSH接続を設定し、ProxyJumpや多段SCPなど実務で必須のテクニックを習得する

---

## 完成イメージ

```
ネットワーク構成:

+----------+          +----------+          +----------+
| ローカル  |   SSH    | 踏み台    |   SSH    | 内部サーバー|
| PC       |=========>| bastion  |=========>| internal |
| (自宅)   |  インター  | (DMZ)    |  社内     | (社内LAN) |
|          |  ネット   |          |  ネット   |          |
+----------+          +----------+          +----------+

# ProxyJump で一発接続
$ ssh internal
user@internal:~$   ← 踏み台を意識せず直接接続！

# 多段SCP
$ scp -J bastion localfile.txt internal:/tmp/
```

```
# ~/.ssh/config の設定
Host bastion
    HostName bastion.example.com
    User jumpuser
    IdentityFile ~/.ssh/id_ed25519_work

Host internal
    HostName 10.0.1.50
    User appuser
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work
```

---

## 課題の要件

1. 踏み台サーバー（bastion）の設定を `~/.ssh/config` に記述する
2. `ProxyJump` を使って内部サーバーに直接接続する
3. 多段SCPでファイルを転送する
4. エージェントフォワーディング（agent forwarding）の設定と注意点を理解する
5. 複数の内部サーバーへの接続設定をまとめる

---

## ステップガイド

<details>
<summary>ステップ1：踏み台サーバーの設定を書く</summary>

```bash
# ~/.ssh/config に追記

# 踏み台サーバー
Host bastion
    HostName bastion.example.com
    User jumpuser
    Port 22
    IdentityFile ~/.ssh/id_ed25519_work
    # 踏み台はコマンド実行不要なのでシェルを割り当てない
    # RequestTTY no  ← 踏み台としてのみ使う場合
```

</details>

<details>
<summary>ステップ2：ProxyJumpで内部サーバーに接続する</summary>

```bash
# コマンドラインで指定する方法
$ ssh -J bastion appuser@10.0.1.50

# ~/.ssh/config に記述する方法（推奨）
Host internal-web
    HostName 10.0.1.50
    User appuser
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work

Host internal-db
    HostName 10.0.1.51
    User dbadmin
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work

# 使い方
$ ssh internal-web
$ ssh internal-db
```

</details>

<details>
<summary>ステップ3：多段ファイル転送</summary>

```bash
# ProxyJump経由でSCP
$ scp -J bastion localfile.txt internal-web:/tmp/

# ProxyJump経由でrsync
$ rsync -avz -e "ssh -J bastion" ./project/ internal-web:/home/appuser/project/

# ~/.ssh/config に ProxyJump が設定済みなら直接指定可能
$ scp localfile.txt internal-web:/tmp/
$ rsync -avz ./project/ internal-web:/home/appuser/project/
```

</details>

<details>
<summary>ステップ4：エージェントフォワーディングの設定</summary>

エージェントフォワーディングを使うと、踏み台サーバー上でもローカルの鍵を利用できます。

```bash
# ~/.ssh/config に追記
Host bastion
    HostName bastion.example.com
    User jumpuser
    ForwardAgent yes   # エージェントフォワーディングを有効化
```

**注意:** エージェントフォワーディングにはセキュリティリスクがあります。
踏み台サーバーの管理者が悪意を持っている場合、あなたの鍵を不正に利用される可能性があります。
信頼できるサーバーに対してのみ有効にしてください。

`ProxyJump` を使う場合はエージェントフォワーディングが不要なケースが多いです。

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）─ 基本的な多段接続設定</summary>

```bash
#!/bin/bash
# 多段SSH接続セットアップスクリプト
# 学べる内容：ProxyJump、踏み台サーバー、多段SCP
# 実行方法：bash setup_proxy_jump.sh

CONFIG_FILE="$HOME/.ssh/config"

echo "===== 多段SSH接続セットアップ ====="

# バックアップ
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "${CONFIG_FILE}.backup.$(date +%Y%m%d%H%M%S)"
    echo "既存の設定をバックアップしました。"
fi

# 設定を追記
cat >> "$CONFIG_FILE" << 'EOF'

# ============================================
# 踏み台サーバー経由の接続設定
# ============================================

# --- 踏み台サーバー ---
Host bastion
    HostName bastion.example.com
    User jumpuser
    Port 22
    IdentityFile ~/.ssh/id_ed25519_work
    ServerAliveInterval 30
    ServerAliveCountMax 3

# --- 内部Webサーバー ---
Host internal-web
    HostName 10.0.1.50
    User appuser
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work

# --- 内部DBサーバー ---
Host internal-db
    HostName 10.0.1.51
    User dbadmin
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work

# --- 内部バッチサーバー ---
Host internal-batch
    HostName 10.0.1.52
    User batch
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work
EOF

chmod 600 "$CONFIG_FILE"

echo ""
echo "設定を追記しました。"
echo ""
echo "--- 追加された接続先 ---"
echo "  ssh bastion        → 踏み台サーバーに直接接続"
echo "  ssh internal-web   → 踏み台経由でWebサーバーに接続"
echo "  ssh internal-db    → 踏み台経由でDBサーバーに接続"
echo "  ssh internal-batch → 踏み台経由でバッチサーバーに接続"
echo ""
echo "--- 多段ファイル転送 ---"
echo "  scp file.txt internal-web:/tmp/"
echo "  rsync -avz ./dir/ internal-web:/home/appuser/dir/"

echo ""
echo "===== 完了 ====="
```

</details>

<details>
<summary>解答例（改良版）─ 動的な踏み台設定と接続テスト付き</summary>

```bash
#!/bin/bash
# 多段SSH接続管理ツール（改良版）
# 学べる内容：ワイルドカード設定、接続テスト、多段SCP/rsync
# 実行方法：bash proxy_jump_manager.sh [setup|test|transfer]

set -euo pipefail

CONFIG_FILE="$HOME/.ssh/config"
BASTION_HOST="${BASTION_HOST:-bastion.example.com}"
BASTION_USER="${BASTION_USER:-jumpuser}"

# === ユーティリティ関数 ===

test_connection() {
    local host="$1"
    local timeout="${2:-5}"

    echo -n "  $host: "
    if ssh -o ConnectTimeout="$timeout" -o BatchMode=yes "$host" "echo OK" 2>/dev/null; then
        echo ""  # OKは既に出力済み
    else
        echo "失敗"
        echo "    詳細確認: ssh -vvv $host"
    fi
}

# === セットアップ ===

do_setup() {
    echo "--- 多段SSH接続のセットアップ ---"

    # バックアップ
    if [ -f "$CONFIG_FILE" ]; then
        local backup="${CONFIG_FILE}.backup.$(date +%Y%m%d%H%M%S)"
        cp "$CONFIG_FILE" "$backup"
        echo "バックアップ: $backup"
    fi

    # 踏み台設定が既に存在するか確認
    if grep -q "^Host bastion$" "$CONFIG_FILE" 2>/dev/null; then
        echo "踏み台の設定は既に存在します。上書きしません。"
        echo "手動で編集してください: $CONFIG_FILE"
        return
    fi

    cat >> "$CONFIG_FILE" << EOF

# ============================================
# 多段SSH接続設定（$(date +%Y-%m-%d) 生成）
# ============================================

# --- 踏み台サーバー ---
Host bastion
    HostName $BASTION_HOST
    User $BASTION_USER
    Port 22
    IdentityFile ~/.ssh/id_ed25519_work
    ServerAliveInterval 30
    ServerAliveCountMax 3
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600

# --- 内部サーバー（ワイルドカード設定） ---
# 10.0.1.* のサーバーはすべて踏み台経由
Host 10.0.1.*
    ProxyJump bastion
    User appuser
    IdentityFile ~/.ssh/id_ed25519_work
    ServerAliveInterval 30

# --- 個別の内部サーバー（エイリアス） ---
Host internal-web
    HostName 10.0.1.50
    User appuser
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work

Host internal-db
    HostName 10.0.1.51
    User dbadmin
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work

Host internal-batch
    HostName 10.0.1.52
    User batch
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work

# --- 多段踏み台（3段以上の接続） ---
# bastion → internal-jumpbox → deep-internal
Host internal-jumpbox
    HostName 10.0.1.100
    User jumpuser
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work

Host deep-internal
    HostName 172.16.0.10
    User deepuser
    ProxyJump internal-jumpbox
    IdentityFile ~/.ssh/id_ed25519_work
EOF

    # ControlPath用ディレクトリ作成
    mkdir -p "$HOME/.ssh/sockets"

    chmod 600 "$CONFIG_FILE"
    echo ""
    echo "設定を追加しました。"
}

# === 接続テスト ===

do_test() {
    echo "--- 接続テスト ---"
    echo ""

    echo "[踏み台サーバー]"
    test_connection "bastion"

    echo ""
    echo "[踏み台経由の内部サーバー]"
    test_connection "internal-web"
    test_connection "internal-db"
    test_connection "internal-batch"

    echo ""
    echo "[ControlMaster の状態]"
    ssh -O check bastion 2>&1 || echo "  ControlMaster は起動していません"
}

# === ファイル転送 ===

do_transfer() {
    local action="${1:-help}"
    local src="${2:-}"
    local dest="${3:-}"

    case "$action" in
        upload)
            if [ -z "$src" ] || [ -z "$dest" ]; then
                echo "使い方: $0 transfer upload <ローカルパス> <ホスト:リモートパス>"
                return 1
            fi
            echo "アップロード: $src → $dest"
            # ProxyJumpが設定済みなら直接指定可能
            if [ -d "$src" ]; then
                rsync -avz --progress "$src/" "$dest/"
            else
                scp "$src" "$dest"
            fi
            ;;
        download)
            if [ -z "$src" ] || [ -z "$dest" ]; then
                echo "使い方: $0 transfer download <ホスト:リモートパス> <ローカルパス>"
                return 1
            fi
            echo "ダウンロード: $src → $dest"
            if ssh "${src%%:*}" "test -d '${src#*:}'" 2>/dev/null; then
                rsync -avz --progress "$src/" "$dest/"
            else
                scp "$src" "$dest"
            fi
            ;;
        *)
            echo "使い方:"
            echo "  $0 transfer upload <ローカルパス> <ホスト:リモートパス>"
            echo "  $0 transfer download <ホスト:リモートパス> <ローカルパス>"
            echo ""
            echo "例:"
            echo "  $0 transfer upload ./report.txt internal-web:/tmp/"
            echo "  $0 transfer download internal-db:/var/log/app.log ./logs/"
            ;;
    esac
}

# === メイン処理 ===

ACTION="${1:-help}"
shift 2>/dev/null || true

case "$ACTION" in
    setup)
        echo "===== 多段SSH接続管理ツール ====="
        do_setup
        ;;
    test)
        echo "===== 多段SSH接続テスト ====="
        do_test
        ;;
    transfer)
        echo "===== 多段ファイル転送 ====="
        do_transfer "$@"
        ;;
    help|*)
        echo "===== 多段SSH接続管理ツール ====="
        echo ""
        echo "使い方: $0 [コマンド]"
        echo ""
        echo "コマンド:"
        echo "  setup                 設定ファイルに踏み台設定を追加"
        echo "  test                  全接続先への接続テスト"
        echo "  transfer [up|down]    踏み台経由のファイル転送"
        echo ""
        echo "環境変数:"
        echo "  BASTION_HOST  踏み台のホスト名 (デフォルト: $BASTION_HOST)"
        echo "  BASTION_USER  踏み台のユーザー名 (デフォルト: $BASTION_USER)"
        ;;
esac

echo ""
echo "===== 完了 ====="
```

**初心者向けとの違い:**
- ワイルドカード設定（`Host 10.0.1.*`）で内部サーバーを一括設定 → サーバー追加のたびにconfigを編集する手間を削減
- `ControlMaster` で接続を多重化 → 踏み台経由でも2回目以降の接続が高速
- 3段以上の多段接続にも対応 → より複雑なネットワーク構成に対応
- 接続テスト機能で全サーバーの到達性を一括確認 → トラブル時の切り分けが容易
- 環境変数で踏み台のホスト名を差し替え可能 → 環境ごとに使い回せる

</details>

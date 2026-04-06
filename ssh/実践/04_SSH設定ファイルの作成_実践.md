# 実践課題04：SSH設定ファイルの作成 ★2

> **難易度**: ★★☆☆☆（基礎）
> **前提知識**: 第3章（公開鍵認証の設定）、第4章（SSH設定ファイル）
> **課題の種類**: ミニプロジェクト
> **学習目標**: `~/.ssh/config` を作成して複数サーバーへの接続を効率化し、設定ファイルの書き方と各項目の意味を理解する

---

## 完成イメージ

```
# 設定前：毎回長いコマンドが必要
$ ssh -i ~/.ssh/id_ed25519_work -p 2222 deploy@dev-server.example.com

# 設定後：エイリアスだけで接続
$ ssh dev
deploy@dev-server:~$
```

```
# 設定ファイルの内容
$ cat ~/.ssh/config
Host dev
    HostName dev-server.example.com
    User deploy
    Port 2222
    IdentityFile ~/.ssh/id_ed25519_work

Host staging
    HostName staging.example.com
    User deploy
    IdentityFile ~/.ssh/id_ed25519_work

Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github
    IdentitiesOnly yes
```

---

## 課題の要件

1. 以下の接続先を `~/.ssh/config` に設定する
   - 開発サーバー（エイリアス: `dev`）
   - ステージングサーバー（エイリアス: `staging`）
   - 本番サーバー（エイリアス: `prod`）
   - GitHub（エイリアス: `github.com`）
2. 共通設定をワイルドカード（`Host *`）で定義する
3. 接続維持の設定（`ServerAliveInterval`）を追加する
4. 設定ファイルのパーミッションを正しく設定する
5. 設定が正しく反映されるか確認する

---

## ステップガイド

<details>
<summary>ステップ1：設定ファイルを作成する</summary>

`~/.ssh/config` をテキストエディタで作成します。

```bash
# エディタで開く（好みのエディタを使用）
$ vim ~/.ssh/config
# または
$ nano ~/.ssh/config
```

基本的な構文：
```
Host エイリアス名
    設定項目 値
    設定項目 値
```

インデント（字下げ）はスペース4つが一般的ですが、タブでも動作します。

</details>

<details>
<summary>ステップ2：共通設定を書く</summary>

`Host *` はすべての接続先に適用される共通設定です。ファイルの末尾に書くのが一般的です。

```
# すべてのホストに共通する設定
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    AddKeysToAgent yes
    IdentitiesOnly yes
```

- `ServerAliveInterval 60` : 60秒ごとにキープアライブ信号を送信
- `ServerAliveCountMax 3` : 3回応答がなければ切断
- `AddKeysToAgent yes` : 使用した鍵を自動でssh-agentに追加
- `IdentitiesOnly yes` : 指定した鍵のみ使用（余計な鍵を送らない）

</details>

<details>
<summary>ステップ3：接続確認</summary>

```bash
# -G オプションで実際の接続設定を確認（接続はしない）
$ ssh -G dev

# 出力例
# hostname dev-server.example.com
# user deploy
# port 2222
# identityfile /home/user/.ssh/id_ed25519_work
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）─ 基本的な設定ファイル</summary>

```bash
#!/bin/bash
# SSH設定ファイル作成スクリプト
# 学べる内容：~/.ssh/config の作成、エイリアス設定
# 実行方法：bash create_ssh_config.sh

CONFIG_FILE="$HOME/.ssh/config"

echo "===== SSH設定ファイルの作成 ====="

# バックアップ
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "${CONFIG_FILE}.backup.$(date +%Y%m%d%H%M%S)"
    echo "既存の設定ファイルをバックアップしました。"
fi

# 設定ファイルを作成
cat > "$CONFIG_FILE" << 'EOF'
# ============================================
# SSH クライアント設定ファイル
# ============================================

# --- 開発サーバー ---
Host dev
    HostName dev-server.example.com
    User deploy
    Port 2222
    IdentityFile ~/.ssh/id_ed25519_work

# --- ステージングサーバー ---
Host staging
    HostName staging.example.com
    User deploy
    IdentityFile ~/.ssh/id_ed25519_work

# --- 本番サーバー ---
Host prod
    HostName production.example.com
    User deploy
    IdentityFile ~/.ssh/id_ed25519_work
    # 本番は誤操作防止のため確認メッセージを表示
    # （接続後にシェルのPS1やmotdで工夫する）

# --- GitHub ---
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github
    IdentitiesOnly yes

# --- 共通設定（すべてのホストに適用） ---
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    AddKeysToAgent yes
    IdentitiesOnly yes
EOF

# パーミッション設定
chmod 600 "$CONFIG_FILE"

echo ""
echo "設定ファイルを作成しました: $CONFIG_FILE"
echo ""

# 内容を表示
echo "--- 設定内容 ---"
cat "$CONFIG_FILE"

echo ""
echo "--- 設定の確認（dev の例） ---"
ssh -G dev 2>/dev/null | grep -E "^(hostname|user|port|identityfile)" || echo "（ssh -G が利用できない環境です）"

echo ""
echo "===== 完了 ====="
```

</details>

<details>
<summary>解答例（改良版）─ 対話式設定ジェネレータ</summary>

```bash
#!/bin/bash
# SSH設定ファイルジェネレータ（改良版）
# 学べる内容：対話式入力、設定の検証、テンプレート管理
# 実行方法：bash ssh_config_generator.sh

set -euo pipefail

CONFIG_FILE="$HOME/.ssh/config"
TEMP_CONFIG=$(mktemp)
trap 'rm -f "$TEMP_CONFIG"' EXIT

# === ユーティリティ関数 ===

add_host_entry() {
    local alias="$1"
    local hostname="$2"
    local user="$3"
    local port="${4:-22}"
    local keyfile="${5:-~/.ssh/id_ed25519}"

    cat >> "$TEMP_CONFIG" << EOF
# --- $alias ---
Host $alias
    HostName $hostname
    User $user
    Port $port
    IdentityFile $keyfile

EOF
    echo "  追加: $alias → ${user}@${hostname}:${port}"
}

validate_config() {
    local config="$1"
    echo "--- 設定の検証 ---"

    # Host エントリの数を数える
    local count
    count=$(grep -c "^Host " "$config" || true)
    echo "  Host エントリ数: $count"

    # 各エイリアスを表示
    echo "  エイリアス一覧:"
    grep "^Host " "$config" | while read -r line; do
        local alias="${line#Host }"
        if [ "$alias" != "*" ]; then
            echo "    - $alias"
        fi
    done

    # パーミッション確認
    if [ -f "$config" ]; then
        local perm
        perm=$(stat -c '%a' "$config" 2>/dev/null || stat -f '%Lp' "$config" 2>/dev/null)
        if [ "$perm" = "600" ]; then
            echo "  パーミッション: $perm [OK]"
        else
            echo "  パーミッション: $perm [要修正 → 600]"
        fi
    fi
}

# === メイン処理 ===

echo "===== SSH設定ファイルジェネレータ ====="

# バックアップ
if [ -f "$CONFIG_FILE" ]; then
    BACKUP="${CONFIG_FILE}.backup.$(date +%Y%m%d%H%M%S)"
    cp "$CONFIG_FILE" "$BACKUP"
    echo "バックアップを作成しました: $BACKUP"
fi

# ヘッダーを書き込み
cat > "$TEMP_CONFIG" << 'EOF'
# ============================================
# SSH クライアント設定ファイル
# 生成日時: GENERATED_DATE
# ============================================

EOF

# 日時を挿入
sed -i "s/GENERATED_DATE/$(date '+%Y-%m-%d %H:%M:%S')/" "$TEMP_CONFIG" 2>/dev/null || \
    sed -i '' "s/GENERATED_DATE/$(date '+%Y-%m-%d %H:%M:%S')/" "$TEMP_CONFIG"

echo ""
echo "--- サーバー設定を追加 ---"

# プリセットの設定を追加
add_host_entry "dev"     "dev-server.example.com"    "deploy" "2222" "~/.ssh/id_ed25519_work"
add_host_entry "staging" "staging.example.com"        "deploy" "22"   "~/.ssh/id_ed25519_work"
add_host_entry "prod"    "production.example.com"     "deploy" "22"   "~/.ssh/id_ed25519_work"

# GitHub の設定を追加
cat >> "$TEMP_CONFIG" << 'EOF'
# --- GitHub ---
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github
    IdentitiesOnly yes

# --- GitLab ---
Host gitlab.com
    HostName gitlab.com
    User git
    IdentityFile ~/.ssh/id_ed25519_gitlab
    IdentitiesOnly yes

EOF
echo "  追加: github.com → git@github.com"
echo "  追加: gitlab.com → git@gitlab.com"

# 共通設定を追加
cat >> "$TEMP_CONFIG" << 'EOF'
# ============================================
# 共通設定（すべてのホストに適用）
# ファイル末尾に配置すること
# ============================================
Host *
    # 接続維持（60秒間隔でキープアライブ、3回失敗で切断）
    ServerAliveInterval 60
    ServerAliveCountMax 3

    # ssh-agent に鍵を自動追加
    AddKeysToAgent yes

    # 指定した鍵のみ使用（セキュリティ向上）
    IdentitiesOnly yes

    # ホスト鍵のハッシュ化（known_hostsの保護）
    HashKnownHosts yes

    # 接続の多重化（同じホストへの2回目以降の接続を高速化）
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600
EOF

# ControlPath 用ディレクトリ作成
mkdir -p "$HOME/.ssh/sockets"

# 設定ファイルを配置
cp "$TEMP_CONFIG" "$CONFIG_FILE"
chmod 600 "$CONFIG_FILE"

echo ""
validate_config "$CONFIG_FILE"

echo ""
echo "--- 生成された設定ファイル ---"
cat "$CONFIG_FILE"

echo ""
echo "===== 完了 ====="
echo ""
echo "使い方の例:"
echo "  ssh dev        → 開発サーバーに接続"
echo "  ssh staging    → ステージングサーバーに接続"
echo "  ssh prod       → 本番サーバーに接続"
echo "  ssh -G dev     → dev の接続設定を確認（接続しない）"
```

**初心者向けとの違い:**
- 関数化により、サーバー追加が1行で可能 → チーム内で設定を共有しやすい
- 設定の検証機能付き → 設定ミスに気づきやすい
- `ControlMaster` による接続多重化設定 → 同じサーバーへの再接続が高速化
- `HashKnownHosts` でknown_hostsのセキュリティ向上 → ホスト名が漏れにくい
- 一時ファイルとtrapで安全な書き込み → 途中で失敗しても元のファイルが壊れない

</details>

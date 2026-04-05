# 第4章：SSH設定ファイル

## この章のゴール
- ~/.ssh/config の書き方を理解し、接続を効率化できるようになる
- sshd_config（サーバー設定）の主要項目を理解する
- セキュリティを考慮した設定ができるようになる

---

## 4.1 クライアント設定ファイル（~/.ssh/config）

### 設定ファイルがない場合の接続

```bash
# 毎回長いコマンドを入力する必要がある
$ ssh -i ~/.ssh/id_ed25519_work -p 2222 myuser@dev-server.example.com
```

### 設定ファイルを使った接続

```bash
# ~/.ssh/config に設定を書くと...
$ ssh dev
# これだけで接続できる！
```

---

## 4.2 ~/.ssh/config の基本構文

```
Host <エイリアス名>
    <設定項目> <値>
    <設定項目> <値>
    ...
```

### 基本的な設定例

```
# 開発サーバー
Host dev
    HostName dev-server.example.com
    User myuser
    Port 2222
    IdentityFile ~/.ssh/id_ed25519_work

# ステージングサーバー
Host staging
    HostName staging.example.com
    User deploy
    IdentityFile ~/.ssh/id_ed25519_work

# 本番サーバー
Host production
    HostName prod.example.com
    User deploy
    IdentityFile ~/.ssh/id_ed25519_work
    # 本番は注意が必要なので色を変える視覚的リマインダーなし
    # → シェルのPS1で工夫する

# GitHub
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github

# GitLab
Host gitlab.com
    HostName gitlab.com
    User git
    IdentityFile ~/.ssh/id_ed25519_gitlab
```

---

## 4.3 主要な設定項目

### 接続先の指定

| 設定項目 | 説明 | 例 |
|---------|------|-----|
| `Host` | エイリアス名（パターン可） | `Host dev` |
| `HostName` | 実際のホスト名またはIP | `HostName 192.168.1.100` |
| `User` | ログインユーザー名 | `User myuser` |
| `Port` | ポート番号 | `Port 2222` |

### 認証の設定

| 設定項目 | 説明 | 例 |
|---------|------|-----|
| `IdentityFile` | 秘密鍵のパス | `IdentityFile ~/.ssh/id_ed25519` |
| `IdentitiesOnly` | 指定した鍵のみ使用 | `IdentitiesOnly yes` |
| `PreferredAuthentications` | 認証方式の優先順位 | `PreferredAuthentications publickey` |
| `PubkeyAuthentication` | 公開鍵認証の有効/無効 | `PubkeyAuthentication yes` |

### 接続維持の設定

| 設定項目 | 説明 | 例 |
|---------|------|-----|
| `ServerAliveInterval` | キープアライブの送信間隔（秒） | `ServerAliveInterval 60` |
| `ServerAliveCountMax` | 無応答時の最大再試行回数 | `ServerAliveCountMax 3` |
| `ConnectTimeout` | 接続タイムアウト（秒） | `ConnectTimeout 10` |
| `ConnectionAttempts` | 接続試行回数 | `ConnectionAttempts 3` |

### 多段接続・プロキシ

| 設定項目 | 説明 | 例 |
|---------|------|-----|
| `ProxyJump` | 踏み台サーバー経由の接続 | `ProxyJump bastion` |
| `ProxyCommand` | プロキシコマンド（高度な用途） | `ProxyCommand ssh -W %h:%p bastion` |

---

## 4.4 ワイルドカードとパターンマッチ

`Host` にはワイルドカードを使ってパターンマッチができます。

```
# すべてのホストに適用する共通設定
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    AddKeysToAgent yes
    IdentitiesOnly yes

# example.com ドメインのすべてのサーバー
Host *.example.com
    User myuser
    IdentityFile ~/.ssh/id_ed25519_work

# dev- で始まるすべてのホスト
Host dev-*
    User developer
    Port 2222

# 特定のホストを除外
Host * !production
    LogLevel VERBOSE
```

### 設定の適用順序

```
設定は上から順に読み込まれ、最初にマッチした値が使用されます。

例:
Host dev
    User devuser        ← dev で接続するときはこの User が使われる

Host *
    User defaultuser    ← dev 以外のホストではこの User が使われる

※ 具体的な設定を上に、一般的な設定（Host *）を下に書くのがポイント
```

---

## 4.5 実践的な設定例

### 完全な設定ファイルの例

```
# ==============================================
# SSH Config - ~/.ssh/config
# ==============================================

# --- 共通設定 ---
Host *
    # 接続維持
    ServerAliveInterval 60
    ServerAliveCountMax 3
    
    # ssh-agent に鍵を自動追加
    AddKeysToAgent yes
    
    # 指定した鍵のみ使用（鍵の過剰送信を防止）
    IdentitiesOnly yes
    
    # ホスト鍵のハッシュ化
    HashKnownHosts yes

# --- GitHub ---
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github

# --- 踏み台サーバー ---
Host bastion
    HostName bastion.example.com
    User admin
    Port 22
    IdentityFile ~/.ssh/id_ed25519_work

# --- 内部サーバー（踏み台経由） ---
Host internal-web
    HostName 10.0.1.10
    User webapp
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work

Host internal-db
    HostName 10.0.1.20
    User dbadmin
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work

# --- 開発環境 ---
Host dev
    HostName dev.example.com
    User developer
    IdentityFile ~/.ssh/id_ed25519_work
    LocalForward 3000 localhost:3000
    LocalForward 5432 localhost:5432

# --- AWS EC2 ---
Host aws-web
    HostName ec2-xx-xx-xx-xx.ap-northeast-1.compute.amazonaws.com
    User ec2-user
    IdentityFile ~/.ssh/aws-keypair.pem
```

### 接続コマンド

```bash
# 設定ファイルを使った簡潔な接続
$ ssh dev              # 開発サーバーに接続
$ ssh bastion          # 踏み台に接続
$ ssh internal-web     # 踏み台経由で内部Webサーバーに接続
$ ssh aws-web          # AWS EC2に接続

# Git操作も設定ファイルの恩恵を受ける
$ git clone git@github.com:user/repo.git
```

---

## 4.6 Match ブロック

条件に応じて設定を切り替える高度な設定方法です。

```
# 特定のネットワークからの接続時のみ適用
Match host *.internal.example.com exec "ip route | grep -q '10.0.0.0/8'"
    ProxyJump none

# 特定のユーザーでの接続時のみ適用
Match user root
    IdentityFile ~/.ssh/id_ed25519_root

# 特定のホストかつ特定のユーザー
Match host production user deploy
    IdentityFile ~/.ssh/id_ed25519_deploy
    RequestTTY no
```

---

## 4.7 サーバー設定ファイル（sshd_config）

SSHサーバーの設定ファイルは `/etc/ssh/sshd_config` です。

### セキュリティ推奨設定

```bash
# /etc/ssh/sshd_config

# --- 基本設定 ---
Port 22                          # ポート番号（変更する場合は運用と相談）
Protocol 2                       # SSH-2のみ使用
AddressFamily any                # IPv4/IPv6両方
ListenAddress 0.0.0.0            # リッスンするアドレス

# --- 認証設定 ---
PermitRootLogin no               # rootの直接ログインを禁止
PubkeyAuthentication yes         # 公開鍵認証を有効
PasswordAuthentication no        # パスワード認証を無効（鍵認証のみにする）
PermitEmptyPasswords no          # 空パスワードを禁止
ChallengeResponseAuthentication no
MaxAuthTries 3                   # 認証試行回数の制限
LoginGraceTime 30                # ログイン猶予時間（秒）

# --- セッション設定 ---
MaxSessions 5                    # 1接続あたりの最大セッション数
ClientAliveInterval 300          # クライアントへのキープアライブ間隔（秒）
ClientAliveCountMax 2            # 無応答時の最大再試行回数

# --- アクセス制御 ---
AllowUsers deploy admin          # 許可するユーザー
# AllowGroups ssh-users          # 許可するグループ
# DenyUsers guest                # 拒否するユーザー

# --- その他のセキュリティ ---
X11Forwarding no                 # X11フォワーディングを無効
AllowTcpForwarding yes           # TCPフォワーディング
PermitTunnel no                  # トンネリングを無効
UseDNS no                        # DNS逆引きを無効（接続速度向上）

# --- ログ ---
LogLevel VERBOSE                 # 詳細なログ出力
SyslogFacility AUTH              # ログファシリティ

# --- 暗号設定（強い暗号のみ使用） ---
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com
```

### sshd_config の操作

```bash
# 設定ファイルの文法チェック
$ sudo sshd -t
# エラーがなければ何も表示されない

# 設定ファイルのテスト（詳細）
$ sudo sshd -T

# SSHサーバーの再起動（設定を反映）
# systemd の場合
$ sudo systemctl restart sshd

# 再起動ではなくリロード（既存接続を切断しない）
$ sudo systemctl reload sshd
```

> **よくある間違い**: `sshd_config` を変更した後、再起動する前に**必ず文法チェック**（`sshd -t`）を行いましょう。設定ミスでSSHサーバーが起動しなくなると、リモートからのアクセス手段を失う可能性があります。また、変更前の接続は切断せず残しておくと、問題があった場合に復旧できます。

---

## 4.8 設定の優先順位

SSH接続時の設定は以下の順に優先されます（上が最優先）。

```
1. コマンドラインオプション   (ssh -p 2222 ...)
2. ~/.ssh/config              (ユーザー設定)
3. /etc/ssh/ssh_config        (システム全体の設定)
4. SSHのデフォルト値

例:
~/.ssh/config に Port 2222 と書いて、
コマンドで ssh -p 3333 host と実行すると、
ポート 3333 が使われます（コマンドラインが最優先）。
```

---

## 4.9 設定のデバッグ

```bash
# 特定のホストに対する実効設定を確認
$ ssh -G dev
user myuser
hostname dev-server.example.com
port 2222
identityfile ~/.ssh/id_ed25519_work
...

# 接続時の詳細ログで設定の適用を確認
$ ssh -v dev 2>&1 | grep -E "Reading|Applying|config"
debug1: Reading configuration data /home/user/.ssh/config
debug1: /home/user/.ssh/config line 1: Applying options for dev
debug1: /home/user/.ssh/config line 20: Applying options for *
debug1: Reading configuration data /etc/ssh/ssh_config
```

---

## ポイントまとめ

```
1. ~/.ssh/config で接続先を定義すれば ssh エイリアス名 だけで接続可能
2. 具体的なHost設定を上に、Host * を最後に書く（適用順序に注意）
3. IdentitiesOnly yes で不要な鍵の送信を防止
4. ServerAliveInterval で接続断を防止
5. sshd_config でパスワード認証を無効化し公開鍵認証のみにするのが基本
6. sshd_config 変更前に必ず sshd -t で文法チェック
7. ssh -G でホストに適用される実効設定を確認できる
```

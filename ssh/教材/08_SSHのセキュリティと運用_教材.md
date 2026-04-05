# 第8章：SSHのセキュリティと運用

## この章のゴール
- SSHサーバーのセキュリティ強化手法を理解する
- 一般的な攻撃手法とその対策を知る
- SSHに関するトラブルシューティングができるようになる
- 実運用でのベストプラクティスを身につける

---

## 8.1 SSHへの一般的な攻撃

### ブルートフォース攻撃

```
攻撃者が大量のユーザー名・パスワードの組み合わせを試行:

攻撃者 → ssh root@target  password: admin      → 失敗
攻撃者 → ssh root@target  password: password   → 失敗
攻撃者 → ssh root@target  password: 123456     → 失敗
攻撃者 → ssh admin@target password: admin123   → 失敗
... 数千〜数百万回試行 ...

対策:
1. パスワード認証を無効化（公開鍵認証のみ）← 最も効果的
2. fail2ban で一定回数失敗したIPをブロック
3. MaxAuthTries で試行回数を制限
4. AllowUsers/AllowGroups で接続可能なユーザーを制限
```

### 中間者攻撃（MITM）

```
正常な通信:
クライアント ──────────────────→ サーバー

中間者攻撃:
クライアント ──→ 攻撃者 ──→ サーバー
              （通信を傍受・改ざん）

対策:
1. ホスト鍵フィンガープリントの検証（初回接続時に確認）
2. known_hosts の適切な管理
3. ホスト鍵が変わった場合の警告を無視しない
4. SSH証明書認証の導入
```

---

## 8.2 サーバーのセキュリティ強化

### 基本的なセキュリティ設定（/etc/ssh/sshd_config）

```bash
# ====================
# 必須のセキュリティ設定
# ====================

# rootログインの禁止
PermitRootLogin no

# パスワード認証の無効化（公開鍵認証のみ）
PasswordAuthentication no
ChallengeResponseAuthentication no

# 空パスワードの禁止
PermitEmptyPasswords no

# 認証試行回数の制限
MaxAuthTries 3

# ログイン猶予時間の短縮
LoginGraceTime 30

# 接続可能なユーザーを制限
AllowUsers deploy admin

# ====================
# 推奨のセキュリティ設定
# ====================

# X11フォワーディングの無効化（不要な場合）
X11Forwarding no

# 使用する暗号アルゴリズムを限定
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com

# ホスト鍵の種類を限定
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key

# SSH バナーの設定（法的警告等）
Banner /etc/ssh/banner.txt

# ログレベルを上げる
LogLevel VERBOSE
```

### 設定変更の安全な手順

```bash
# 1. 現在の接続を維持したまま作業する（切断しない！）

# 2. 設定ファイルのバックアップ
$ sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

# 3. 設定を編集
$ sudo vim /etc/ssh/sshd_config

# 4. 文法チェック
$ sudo sshd -t
# エラーがなければ何も表示されない

# 5. 設定をリロード（既存接続は切断されない）
$ sudo systemctl reload sshd

# 6. 別のターミナルから新しい接続をテスト
$ ssh user@server
# 成功したら完了

# 7. 失敗した場合、バックアップから復元
$ sudo cp /etc/ssh/sshd_config.bak /etc/ssh/sshd_config
$ sudo systemctl reload sshd
```

> **よくある間違い**: SSHの設定変更をして再起動した後、**既存の接続を閉じてから**テストすると、設定ミスがあった場合にサーバーにアクセスできなくなります。必ず既存の接続を維持した状態でテストしましょう。

---

## 8.3 fail2ban の導入

fail2ban は、認証失敗を監視し、攻撃元のIPアドレスを自動的にブロックするツールです。

### インストールと設定

```bash
# インストール（Ubuntu/Debian）
$ sudo apt install fail2ban

# 設定ファイルの作成（デフォルト設定を上書き）
$ sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
$ sudo vim /etc/fail2ban/jail.local
```

### SSH用の設定

```ini
# /etc/fail2ban/jail.local

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3          # 3回失敗でBAN
findtime = 600        # 600秒（10分）以内に
bantime = 3600        # 3600秒（1時間）BAN
```

### 操作コマンド

```bash
# サービスの起動
$ sudo systemctl enable fail2ban
$ sudo systemctl start fail2ban

# ステータス確認
$ sudo fail2ban-client status
Status
|- Number of jail:      1
`- Jail list:   sshd

# SSH jail の詳細
$ sudo fail2ban-client status sshd
Status for the jail: sshd
|- Filter
|  |- Currently failed: 2
|  |- Total failed:     15
|  `- File list:        /var/log/auth.log
`- Actions
   |- Currently banned: 1
   |- Total banned:     3
   `- Banned IP list:   203.0.113.50

# 手動でIPをBAN解除
$ sudo fail2ban-client set sshd unbanip 203.0.113.50
```

---

## 8.4 ファイアウォールとの連携

### UFW（Ubuntu）

```bash
# SSH を許可
$ sudo ufw allow ssh
# または
$ sudo ufw allow 22/tcp

# 特定のIPからのみSSHを許可
$ sudo ufw allow from 192.168.1.0/24 to any port 22

# ファイアウォールを有効化
$ sudo ufw enable

# ルールの確認
$ sudo ufw status verbose
```

### firewalld（CentOS/Rocky Linux）

```bash
# SSH を許可（デフォルトで許可済み）
$ sudo firewall-cmd --permanent --add-service=ssh

# 特定のIPからのみ許可（リッチルール）
$ sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" service name="ssh" accept'

# 変更を反映
$ sudo firewall-cmd --reload
```

---

## 8.5 SSH証明書認証

大規模環境では、公開鍵の代わりに**SSH証明書**を使う方法があります。

### 従来の公開鍵認証の課題

```
サーバーが100台、ユーザーが50人の場合:
  各サーバーの authorized_keys に各ユーザーの公開鍵を登録
  → 100 × 50 = 5,000 のエントリ管理が必要！

ユーザーの追加・削除のたびに全サーバーを更新...
```

### SSH証明書の仕組み

```
+----------+                    +----------+
|   CA     | --- 署名 -------→ | ユーザー   |
| (認証局)  |                    | 証明書    |
+----------+                    +----------+
     |
     | CA公開鍵を
     | 全サーバーに登録
     | (1回だけ)
     ↓
+----------+
| サーバー  |  CA公開鍵で証明書を検証 → 認証OK
+----------+

メリット:
- サーバーにはCA公開鍵を1つ登録するだけ
- ユーザー追加はCAが証明書を発行するだけ
- 証明書に有効期限を設定できる
```

### 基本的な手順

```bash
# 1. CA鍵ペアの作成
$ ssh-keygen -t ed25519 -f ca_key -C "SSH CA"

# 2. ユーザー鍵に署名して証明書を作成
$ ssh-keygen -s ca_key -I "user-cert" -n username -V +365d ~/.ssh/id_ed25519.pub
# -s: CA秘密鍵
# -I: 証明書ID（識別用）
# -n: 許可するユーザー名
# -V: 有効期限

# 3. 証明書の確認
$ ssh-keygen -L -f ~/.ssh/id_ed25519-cert.pub
        Type: ssh-ed25519-cert-v01@openssh.com user certificate
        Public key: ED25519-CERT ...
        Signing CA: ED25519 ...
        Key ID: "user-cert"
        Serial: 0
        Valid: from 2024-01-01T00:00:00 to 2025-01-01T00:00:00
        Principals:
                username
        ...

# 4. サーバーにCA公開鍵を登録（/etc/ssh/sshd_config）
# TrustedUserCAKeys /etc/ssh/ca_key.pub
```

---

## 8.6 認証ログの監視

### ログの確認

```bash
# Ubuntu/Debian のSSH認証ログ
$ sudo tail -f /var/log/auth.log

# CentOS/Rocky Linux のSSH認証ログ
$ sudo tail -f /var/log/secure

# systemd journal でSSHログを確認
$ sudo journalctl -u sshd -f

# 認証失敗のみ抽出
$ sudo grep "Failed password" /var/log/auth.log
Jan 15 10:23:45 server sshd[12345]: Failed password for invalid user admin from 203.0.113.50 port 54321 ssh2

# 認証成功のみ抽出
$ sudo grep "Accepted" /var/log/auth.log
Jan 15 10:30:12 server sshd[12346]: Accepted publickey for user from 198.51.100.10 port 54322 ssh2

# 不正なユーザー名での試行を抽出
$ sudo grep "Invalid user" /var/log/auth.log | awk '{print $8}' | sort | uniq -c | sort -rn | head
    152 admin
     89 root
     45 test
     23 oracle
```

---

## 8.7 トラブルシューティング

### よくある問題と解決方法

#### 問題1: "Connection refused"

```bash
$ ssh user@example.com
ssh: connect to host example.com port 22: Connection refused

# 原因と対処:
# 1. SSHサーバーが起動していない
$ sudo systemctl status sshd
$ sudo systemctl start sshd

# 2. ファイアウォールでブロックされている
$ sudo ufw status
$ sudo ufw allow ssh

# 3. ポート番号が異なる
$ ssh -p 2222 user@example.com
```

#### 問題2: "Permission denied (publickey)"

```bash
$ ssh user@example.com
Permission denied (publickey).

# 原因と対処:
# 1. 正しい鍵が使われているか確認
$ ssh -v user@example.com 2>&1 | grep "Offering"
debug1: Offering public key: /home/user/.ssh/id_ed25519

# 2. サーバー側の authorized_keys を確認
# パスワード認証が有効な場合:
$ ssh -o PreferredAuthentications=password user@example.com
$ cat ~/.ssh/authorized_keys

# 3. パーミッションを確認
$ ls -la ~/.ssh/
$ ls -la ~/.ssh/authorized_keys
# → 秘密鍵: 600, .ssh: 700, authorized_keys: 600

# 4. SELinux のコンテキストを確認（RHEL系）
$ restorecon -Rv ~/.ssh/
```

#### 問題3: "Connection timed out"

```bash
$ ssh user@example.com
ssh: connect to host example.com port 22: Connection timed out

# 原因と対処:
# 1. ネットワークの疎通確認
$ ping example.com
$ traceroute example.com

# 2. ポートの疎通確認
$ nc -zv example.com 22
$ nmap -p 22 example.com

# 3. DNS解決の確認
$ nslookup example.com
$ dig example.com
```

#### 問題4: "Host key verification failed"

```bash
$ ssh user@example.com
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# 原因: サーバーが再構築された等でホスト鍵が変わった

# 対処（サーバー再構築を確認した上で）:
$ ssh-keygen -R example.com
$ ssh user@example.com  # 新しいホスト鍵を受け入れる
```

#### 問題5: 接続が途中で切れる

```bash
# 原因: NAT/ファイアウォールがアイドル接続を切断

# 対処: ~/.ssh/config にキープアライブを設定
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    TCPKeepAlive yes
```

### デバッグの手順

```bash
# ステップ1: クライアント側のデバッグ
$ ssh -vvv user@example.com 2>&1 | tee ssh_debug.log

# ステップ2: サーバー側のログ確認
$ sudo journalctl -u sshd -n 50

# ステップ3: SSHDをデバッグモードで起動（別ポートで）
$ sudo /usr/sbin/sshd -d -p 2222
# 別のターミナルから接続
$ ssh -p 2222 -v user@example.com
```

---

## 8.8 運用のベストプラクティス

### セキュリティチェックリスト

```
基本設定:
□ パスワード認証を無効化
□ rootログインを禁止
□ 公開鍵認証のみを使用
□ Ed25519 鍵を使用
□ パスフレーズ付き鍵を使用

アクセス制御:
□ AllowUsers/AllowGroups で接続可能なユーザーを制限
□ fail2ban を導入
□ ファイアウォールでSSHポートへのアクセスを制限
□ MaxAuthTries を制限（3回程度）

鍵管理:
□ 用途ごとに鍵を分ける
□ 不要になった公開鍵はサーバーから削除
□ 鍵のローテーション（定期的な更新）を行う
□ 秘密鍵のパーミッションは 600

運用:
□ SSH設定変更時は既存接続を維持してテスト
□ 認証ログを定期的に監視
□ OpenSSHを最新バージョンに保つ
□ 暗号アルゴリズムを定期的に見直す
```

### 鍵のローテーション手順

```bash
# 1. 新しい鍵ペアを生成
$ ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_new -C "user@host-$(date +%Y%m)"

# 2. 新しい公開鍵をサーバーに追加（古い鍵で接続して追加）
$ ssh-copy-id -i ~/.ssh/id_ed25519_new.pub user@example.com

# 3. 新しい鍵で接続テスト
$ ssh -i ~/.ssh/id_ed25519_new user@example.com

# 4. 問題なければ ~/.ssh/config を更新
# IdentityFile ~/.ssh/id_ed25519_new

# 5. 古い公開鍵をサーバーから削除
$ ssh user@example.com
$ vim ~/.ssh/authorized_keys  # 古い鍵の行を削除

# 6. 古い鍵ファイルを削除
$ rm ~/.ssh/id_ed25519_old ~/.ssh/id_ed25519_old.pub
```

---

## 8.9 SSH のモダンな活用

### SSHとコンテナ

```bash
# Docker コンテナへのSSH（開発時の一時的なアクセス）
$ docker exec -it container_name bash  # SSH より推奨

# Kubernetes Pod へのアクセス
$ kubectl exec -it pod-name -- bash    # SSH より推奨

# ※ コンテナ環境では SSH よりも exec を使うのが現代的
```

### GitHub Actions でのSSHデプロイ

```yaml
# .github/workflows/deploy.yml
- name: Deploy via SSH
  uses: appleboy/ssh-action@v1
  with:
    host: ${{ secrets.HOST }}
    username: ${{ secrets.USERNAME }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    script: |
      cd /var/www/app
      git pull origin main
      npm install
      npm run build
      pm2 restart app
```

### VS Code Remote SSH

```
VS Code から SSH経由でリモートサーバー上のファイルを直接編集:

1. 拡張機能「Remote - SSH」をインストール
2. コマンドパレット → "Remote-SSH: Connect to Host"
3. ~/.ssh/config のホストが一覧に表示される
4. 選択して接続 → リモートのファイルをローカルのように編集
```

---

## ポイントまとめ

```
1. パスワード認証の無効化が最も効果的なセキュリティ対策
2. fail2ban でブルートフォース攻撃を自動ブロック
3. ホスト鍵の警告は安易に無視しない（MITM攻撃の可能性）
4. SSH設定変更時は既存接続を維持してテスト
5. -v オプションでのデバッグがトラブルシューティングの基本
6. 鍵のローテーションを定期的に行う
7. コンテナ環境ではSSHより exec を使うのが現代的
8. 大規模環境ではSSH証明書認証の導入を検討
```

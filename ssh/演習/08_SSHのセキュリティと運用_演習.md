# 第8章 演習：SSHのセキュリティと運用

---

## 基本問題

### 問題1: 基本的なセキュリティ設定
以下の `sshd_config` の設定項目について、セキュリティ上推奨される値を答えてください。

1. `PermitRootLogin`
2. `PasswordAuthentication`
3. `PermitEmptyPasswords`
4. `MaxAuthTries`
5. `PubkeyAuthentication`

<details>
<summary>解答</summary>

```
1. PermitRootLogin no           ← rootの直接ログインを禁止
2. PasswordAuthentication no    ← パスワード認証を無効化
3. PermitEmptyPasswords no      ← 空パスワードを禁止
4. MaxAuthTries 3               ← 認証試行回数を3回に制限
5. PubkeyAuthentication yes     ← 公開鍵認証を有効化
```

</details>

---

### 問題2: ブルートフォース攻撃の対策
SSHへのブルートフォース攻撃に対する対策を4つ挙げてください。

<details>
<summary>解答</summary>

```
1. パスワード認証を無効化し、公開鍵認証のみにする（最も効果的）
   → PasswordAuthentication no

2. fail2ban を導入し、一定回数の認証失敗でIPをブロック
   → 例: 3回失敗で1時間BAN

3. MaxAuthTries で認証試行回数を制限
   → MaxAuthTries 3

4. AllowUsers/AllowGroups で接続可能なユーザーを制限
   → AllowUsers deploy admin

その他:
- ファイアウォールでSSHポートへのアクセスを制限
- 特定のIPアドレスからのみSSHを許可
```

</details>

---

### 問題3: エラーメッセージの診断
以下の各エラーメッセージの原因を答えてください。

**エラー1:**
```
ssh: connect to host example.com port 22: Connection refused
```

**エラー2:**
```
Permission denied (publickey).
```

**エラー3:**
```
ssh: connect to host example.com port 22: Connection timed out
```

<details>
<summary>解答</summary>

```
エラー1: Connection refused
原因:
- SSHサーバー（sshd）が起動していない
- ファイアウォールでポート22がブロックされている
- SSHサーバーが別のポートで動作している

エラー2: Permission denied (publickey)
原因:
- サーバーに公開鍵が登録されていない
- 正しい秘密鍵が使われていない
- サーバー側の ~/.ssh/ やauthorized_keysのパーミッションが不正
- サーバーでパスワード認証が無効で、鍵認証に失敗した

エラー3: Connection timed out
原因:
- ネットワーク的にサーバーに到達できない
- ファイアウォールがパケットをドロップしている（rejectではなくdrop）
- サーバーがダウンしている
- DNS解決に問題がある
```

</details>

---

### 問題4: fail2banの基本操作
以下の操作のコマンドを書いてください。

1. fail2banのSSH jailのステータスを確認する
2. BANされたIPアドレス `203.0.113.50` を解除する
3. fail2banサービスを起動する

<details>
<summary>解答</summary>

```bash
# 1. SSH jailのステータス確認
$ sudo fail2ban-client status sshd

# 2. IPのBAN解除
$ sudo fail2ban-client set sshd unbanip 203.0.113.50

# 3. サービス起動
$ sudo systemctl start fail2ban
```

</details>

---

## 応用問題

### 問題5: ログの解析
以下のSSH認証ログから読み取れる情報を説明してください。

```
Jan 15 10:23:45 server sshd[12345]: Failed password for invalid user admin from 203.0.113.50 port 54321 ssh2
Jan 15 10:23:47 server sshd[12346]: Failed password for invalid user admin from 203.0.113.50 port 54322 ssh2
Jan 15 10:23:49 server sshd[12347]: Failed password for invalid user root from 203.0.113.50 port 54323 ssh2
Jan 15 10:30:12 server sshd[12350]: Accepted publickey for deploy from 198.51.100.10 port 55000 ssh2
```

<details>
<summary>解答</summary>

```
1行目〜3行目:
- 203.0.113.50 から「admin」「root」というユーザー名でパスワード認証の
  ブルートフォース攻撃を受けている
- "invalid user" は、サーバーに存在しないユーザー名での試行
- 約2秒間隔で連続試行しており、自動化されたツールによる攻撃と推測される
- パスワード認証が有効になっている（セキュリティ上の懸念）

4行目:
- 198.51.100.10 から「deploy」ユーザーが公開鍵認証で正常にログインした
- "Accepted publickey" は認証成功

対策:
- PasswordAuthentication no でパスワード認証を無効化
- fail2ban で 203.0.113.50 をブロック
- AllowUsers deploy で接続可能ユーザーを制限
```

</details>

---

### 問題6: ホスト鍵の警告への対応
以下の警告が表示されました。取るべき行動を手順で説明してください。

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```

<details>
<summary>解答</summary>

```
正しい対応手順:

1. まず疑う
   → 中間者攻撃（MITM）の可能性を考慮する
   → 安易にknown_hostsから削除しない

2. サーバー管理者に確認
   → サーバーの再構築、OS再インストール、SSH鍵の再生成があったか確認
   → 正当な理由でホスト鍵が変わったのか確認

3. 正当な理由が確認できたら
   → 古いホスト鍵を削除
   $ ssh-keygen -R example.com

   → 再接続して新しいホスト鍵を確認・登録
   $ ssh user@example.com
   → フィンガープリントが管理者から通知されたものと一致するか確認
   → yes で登録

4. 正当な理由が確認できない場合
   → 接続しない
   → セキュリティチームに報告
   → ネットワーク経路を調査
```

</details>

---

### 問題7: デバッグ手順
SSHで接続できない場合の体系的なデバッグ手順を説明してください。

<details>
<summary>解答</summary>

```bash
# ステップ1: クライアント側のデバッグ出力を確認
$ ssh -vvv user@server
# → 接続のどの段階で失敗しているか特定

# ステップ2: ネットワーク疎通を確認
$ ping server                    # ICMPの疎通
$ nc -zv server 22               # ポート22への接続
$ traceroute server              # 経路の確認

# ステップ3: DNS解決を確認
$ nslookup server
$ dig server

# ステップ4: 認証関連の確認
$ ssh -v user@server 2>&1 | grep "Offering"      # 使用される鍵
$ ssh -v user@server 2>&1 | grep "Authentication"  # 認証方式

# ステップ5: サーバー側の確認（別の方法でアクセスできる場合）
$ sudo systemctl status sshd     # SSHDの状態
$ sudo journalctl -u sshd -n 50  # SSHDのログ
$ sudo sshd -t                   # 設定ファイルの文法チェック

# ステップ6: パーミッションの確認
$ ls -la ~/.ssh/                 # ローカル
$ ls -ld ~ ~/.ssh ~/.ssh/authorized_keys  # リモート（可能なら）
```

</details>

---

### 問題8: セキュリティチェックリスト
以下のセキュリティチェック項目について、それぞれ「設定済み」か「未設定」かを確認するコマンドを書いてください。

1. パスワード認証が無効化されているか
2. rootログインが禁止されているか
3. 使用中のSSHの暗号アルゴリズム

<details>
<summary>解答</summary>

```bash
# 1. パスワード認証の確認
$ sudo grep "^PasswordAuthentication" /etc/ssh/sshd_config
# 期待: PasswordAuthentication no

# 2. rootログインの確認
$ sudo grep "^PermitRootLogin" /etc/ssh/sshd_config
# 期待: PermitRootLogin no

# 3. 使用中の暗号アルゴリズム
$ ssh -v user@server 2>&1 | grep "kex:" 
# 鍵交換アルゴリズムを確認
$ ssh -v user@server 2>&1 | grep "cipher:"
# 暗号方式を確認

# 一括確認（sshd -T でテスト表示）
$ sudo sshd -T | grep -E "^(passwordauthentication|permitrootlogin|ciphers|kexalgorithms)"
```

</details>

---

## チャレンジ問題

### 問題9: 鍵のローテーション
現在使用中の Ed25519 鍵を新しい鍵に安全にローテーションする手順を書いてください。サーバーへのアクセスが途切れないことを保証する手順にしてください。

<details>
<summary>解答</summary>

```bash
# 1. 新しい鍵ペアを生成
$ ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_new -C "user@host-$(date +%Y%m)"

# 2. 新しい公開鍵をサーバーに追加（古い鍵で接続して）
# ※ 古い鍵の行は削除しない（新しい鍵を追加するだけ）
$ ssh-copy-id -i ~/.ssh/id_ed25519_new.pub user@server

# 3. 新しい鍵で接続テスト
$ ssh -i ~/.ssh/id_ed25519_new user@server
# → 成功することを確認

# 4. ~/.ssh/config を更新
# IdentityFile ~/.ssh/id_ed25519_new

# 5. 設定変更後の接続テスト
$ ssh server
# → 新しい鍵で接続できることを確認

# 6. サーバーから古い公開鍵を削除
$ ssh server
$ vim ~/.ssh/authorized_keys
# 古い鍵の行を削除

# 7. 古い鍵で接続できないことを確認
$ ssh -i ~/.ssh/id_ed25519_old server
# → Permission denied になることを確認

# 8. ローカルの古い鍵ファイルを削除
$ rm ~/.ssh/id_ed25519_old ~/.ssh/id_ed25519_old.pub

重要なポイント:
- 新しい鍵を追加してから古い鍵を削除する（順番が逆だとアクセス不能に）
- 各ステップで接続テストを行う
- 古い鍵を削除する前に新しい鍵での接続を確認する
```

</details>

---

### 問題10: 総合セキュリティ設計
新しいサーバーをセットアップする際の、SSH セキュリティの設定手順を最初から最後まで書いてください。鍵の生成から sshd_config の設定、fail2ban の導入までを含めてください。

<details>
<summary>解答</summary>

```bash
# ========== ローカルPC側 ==========

# 1. 鍵ペアの生成
$ ssh-keygen -t ed25519 -C "admin@server" -f ~/.ssh/id_ed25519_server
# パスフレーズを設定

# 2. 公開鍵をサーバーに登録（初回はパスワードで接続）
$ ssh-copy-id -i ~/.ssh/id_ed25519_server.pub admin@server

# 3. 鍵認証での接続テスト
$ ssh -i ~/.ssh/id_ed25519_server admin@server

# ========== サーバー側 ==========

# 4. sshd_config のバックアップ
$ sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

# 5. sshd_config の編集
$ sudo vim /etc/ssh/sshd_config

# 設定内容:
PermitRootLogin no
PasswordAuthentication no
ChallengeResponseAuthentication no
PermitEmptyPasswords no
PubkeyAuthentication yes
MaxAuthTries 3
LoginGraceTime 30
AllowUsers admin
X11Forwarding no
LogLevel VERBOSE
ClientAliveInterval 300
ClientAliveCountMax 2

# 6. 文法チェック
$ sudo sshd -t

# 7. SSHDリロード（既存接続は維持！）
$ sudo systemctl reload sshd

# 8. 別ターミナルから接続テスト
$ ssh admin@server

# 9. fail2ban のインストールと設定
$ sudo apt install fail2ban
$ sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
$ sudo vim /etc/fail2ban/jail.local

# [sshd]
# enabled = true
# maxretry = 3
# findtime = 600
# bantime = 3600

$ sudo systemctl enable fail2ban
$ sudo systemctl start fail2ban

# 10. ファイアウォールの設定
$ sudo ufw allow ssh
$ sudo ufw enable

# 11. 動作確認
$ sudo fail2ban-client status sshd
$ sudo ufw status
```

</details>

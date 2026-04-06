# 実践課題09：デバッグ演習 ─ SSH接続トラブルシューティング ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第1章〜第8章（SSH全般）
> **課題の種類**: デバッグ
> **学習目標**: SSHの接続エラーに対するトラブルシューティング手順を身につけ、エラーメッセージから原因を特定・修正する力を養う

---

## 課題の説明

以下の **10個のSSH設定・操作のバグ** を含むシナリオが提示されます。
各シナリオのエラーメッセージや設定内容を読み解き、原因を特定して修正してください。

### 進め方

1. 各シナリオのエラーメッセージまたは設定内容を確認する
2. 原因を推測する
3. 修正方法を考える
4. 解答を確認する

---

## シナリオ一覧

### シナリオ1：パーミッションエラーで接続できない

```
$ ssh -i ~/.ssh/id_ed25519_work user@server
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for '/home/user/.ssh/id_ed25519_work' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "/home/user/.ssh/id_ed25519_work": bad permissions
user@server: Permission denied (publickey).
```

### シナリオ2：ホスト鍵が変わった警告

```
$ ssh user@server
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ED25519 key sent by the remote host is
SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
Please contact your system administrator.
Add correct host key in /home/user/.ssh/known_hosts:5.
Offending ED25519 key in /home/user/.ssh/known_hosts:5
Host key for server has changed and you have requested strict checking.
Host key verification failed.
```

### シナリオ3：設定ファイルが効かない

```
# ~/.ssh/config の内容
Host dev
HostName dev-server.example.com
User deploy
Port 2222
IdentityFile ~/.ssh/id_ed25519_work

# 接続しようとすると...
$ ssh dev
ssh: Could not resolve hostname dev: Name or service not known
```

### シナリオ4：公開鍵認証が通らない

```
$ ssh -vvv user@server 2>&1 | grep -A2 "Offering"
debug1: Offering public key: /home/user/.ssh/id_ed25519_work ED25519 ...
debug1: Authentications that can continue: publickey
debug1: No more authentication methods to try.
user@server: Permission denied (publickey).
```

サーバー側の設定:
```bash
$ ls -la /home/user/.ssh/
drwxrwxrwx 2 user user 4096 ... .ssh/
-rw-rw-r-- 1 user user  104 ... authorized_keys
```

### シナリオ5：ポートフォワーディングが動かない

```
$ ssh -L 8080:localhost:80 user@server -N
bind: Address already in use
channel_setup_fwd_listener_tcpip: cannot listen to port: 8080
Could not request local forwarding.
```

### シナリオ6：ssh-agent に鍵が登録できない

```
$ ssh-add ~/.ssh/id_ed25519_work
Could not open a connection to your authentication agent.
```

### シナリオ7：ProxyJump で内部サーバーに接続できない

```
# ~/.ssh/config
Host bastion
    HostName bastion.example.com
    User jumpuser
    IdentityFile ~/.ssh/id_ed25519_work

Host internal
    HostName 10.0.1.50
    User appuser
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_bastion  # ← 踏み台上の鍵を指定

$ ssh internal
Permission denied (publickey).
```

### シナリオ8：SCP転送でファイルが見つからない

```
$ scp user@server:~/documents/report 2024.pdf ./
scp: /home/user/documents/report: No such file or directory
scp: 2024.pdf: No such file or directory
```

### シナリオ9：接続がすぐ切れる

```
$ ssh user@server
Last login: Mon Apr  6 10:00:00 2026
Connection to server closed.
```

サーバー側の `/etc/ssh/sshd_config`:
```
ClientAliveInterval 10
ClientAliveCountMax 0
```

### シナリオ10：~/.ssh/config で意図しない設定が適用される

```
# ~/.ssh/config
Host *
    User admin
    Port 2222
    IdentityFile ~/.ssh/id_rsa

Host dev
    HostName dev-server.example.com
    User deploy
    Port 22

# 確認
$ ssh -G dev | grep -E "^(user|port|identityfile)"
user deploy
port 22
identityfile /home/user/.ssh/id_rsa    # ← id_rsa ではなく別の鍵を使いたい
```

---

## バグの種類（ヒントレベル別）

<details>
<summary>ヒント（軽め）：バグの分類</summary>

| # | カテゴリ |
|---|---------|
| 1 | パーミッション設定ミス |
| 2 | ホスト鍵の変更対応 |
| 3 | 設定ファイルの構文エラー |
| 4 | サーバー側のパーミッション |
| 5 | ポート競合 |
| 6 | ssh-agent 未起動 |
| 7 | 鍵のパス解決ミス |
| 8 | ファイル名のスペース |
| 9 | サーバー設定ミス |
| 10 | config の優先順位 |

</details>

<details>
<summary>ヒント（詳細）：各バグの場所と手がかり</summary>

| # | 手がかり |
|---|---------|
| 1 | 秘密鍵のパーミッションが `0644`（公開されすぎ） |
| 2 | サーバーの再構築やIPの変更でホスト鍵が変わった |
| 3 | Hostブロック内の設定にインデントがない |
| 4 | `.ssh/` と `authorized_keys` のパーミッションが緩すぎる |
| 5 | ローカルの8080番ポートが他のプロセスで使用中 |
| 6 | `ssh-agent` が起動していない（`eval` が必要） |
| 7 | `IdentityFile` のパスは接続元（ローカル）から見たパス |
| 8 | ファイル名にスペースが含まれている |
| 9 | `ClientAliveCountMax 0` は即座に切断される設定 |
| 10 | `Host *` の `IdentityFile` が適用されている |

</details>

---

## 解答例

<details>
<summary>全10個のバグと修正方法</summary>

### シナリオ1：秘密鍵のパーミッションが緩すぎる

秘密鍵のパーミッションが `0644`（他人が読める）になっています。

```bash
# 修正：パーミッションを600に変更
$ chmod 600 ~/.ssh/id_ed25519_work

# 確認
$ ls -la ~/.ssh/id_ed25519_work
-rw------- 1 user user 464 ... /home/user/.ssh/id_ed25519_work
```

**ポイント:** SSHは秘密鍵のパーミッションが緩いと使用を拒否します。秘密鍵は必ず `600`（所有者のみ読み書き）にしてください。

---

### シナリオ2：ホスト鍵が変わった

サーバーの再構築やOS再インストールでホスト鍵が変更されたケースです。

```bash
# 修正：古いホスト鍵を削除
$ ssh-keygen -R server

# または特定の行を削除
$ sed -i '5d' ~/.ssh/known_hosts

# 再接続（新しいホスト鍵を確認して受け入れる）
$ ssh user@server
```

**注意:** 本当に中間者攻撃の可能性がある場合もあります。サーバー管理者にホスト鍵のフィンガープリントを確認してから受け入れてください。

---

### シナリオ3：設定ファイルのインデント不足

`Host` ブロック内の設定項目にインデント（字下げ）がありません。

```
# 修正前（インデントなし → 設定が効かない）
Host dev
HostName dev-server.example.com
User deploy

# 修正後（インデントあり）
Host dev
    HostName dev-server.example.com
    User deploy
    Port 2222
    IdentityFile ~/.ssh/id_ed25519_work
```

**ポイント:** SSH設定ファイルでは、`Host` 行の下の設定項目にはスペースまたはタブでインデントが必要です。インデントがないと別のHostブロック（またはグローバル設定）として解釈されます。

---

### シナリオ4：サーバー側のパーミッションが緩すぎる

サーバー側の `~/.ssh/` が `777`、`authorized_keys` が `664` になっています。

```bash
# サーバー側で修正
$ chmod 700 ~/.ssh
$ chmod 600 ~/.ssh/authorized_keys

# ホームディレクトリも確認
$ chmod 755 ~
```

**ポイント:** SSHサーバーは、`~/.ssh/` や `authorized_keys` のパーミッションが緩いと公開鍵認証を拒否します（`StrictModes yes` がデフォルト）。

---

### シナリオ5：ポートが既に使用中

ローカルの8080番ポートが他のプロセスで使われています。

```bash
# 使用中のプロセスを確認
$ lsof -i :8080
# または
$ ss -tlnp | grep 8080

# 修正方法1：別のポートを使う
$ ssh -L 18080:localhost:80 user@server -N

# 修正方法2：既存のプロセスを終了する
$ kill $(lsof -ti :8080)
```

---

### シナリオ6：ssh-agent が起動していない

`ssh-add` の前に `ssh-agent` を起動する必要があります。

```bash
# 修正：ssh-agent を起動
$ eval "$(ssh-agent -s)"
Agent pid 12345

# 鍵を登録
$ ssh-add ~/.ssh/id_ed25519_work
```

**ポイント:** `ssh-agent -s` だけでは環境変数がシェルに設定されません。`eval` で囲む必要があります。

---

### シナリオ7：IdentityFileのパス解決

`ProxyJump` を使う場合、`IdentityFile` はローカルPCから見たパスで指定する必要があります。踏み台上のパスではありません。

```
# 修正前（踏み台上のパスを指定 → エラー）
Host internal
    IdentityFile ~/.ssh/id_ed25519_bastion  # 踏み台上の鍵

# 修正後（ローカルの鍵パスを指定）
Host internal
    HostName 10.0.1.50
    User appuser
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work  # ローカルの鍵
```

**ポイント:** `ProxyJump` では、SSHクライアントがローカルから直接内部サーバーに接続します（トンネル経由）。鍵もローカルのものを使います。

---

### シナリオ8：ファイル名のスペース

ファイル名が `report 2024.pdf`（スペース含む）のため、SCPが2つの引数として解釈しています。

```bash
# 修正前（スペースが引数区切りとして解釈される）
$ scp user@server:~/documents/report 2024.pdf ./

# 修正方法1：クォートで囲む
$ scp "user@server:~/documents/report 2024.pdf" ./

# 修正方法2：バックスラッシュでエスケープ
$ scp user@server:~/documents/report\ 2024.pdf ./
```

---

### シナリオ9：ClientAliveCountMax が0で即切断

`ClientAliveCountMax 0` は「キープアライブの失敗を0回まで許容」、つまり最初のチェックで即切断されます。

```bash
# 修正前（/etc/ssh/sshd_config）
ClientAliveInterval 10
ClientAliveCountMax 0    # ← 0回で切断 = 即切断

# 修正後
ClientAliveInterval 60   # 60秒間隔でチェック
ClientAliveCountMax 3    # 3回失敗で切断（180秒の無応答で切断）

# 設定反映
$ sudo systemctl restart sshd
```

---

### シナリオ10：Host * の設定が意図せず適用

`Host *` で `IdentityFile` を指定しているため、`dev` にも `id_rsa` が適用されています。

```
# 修正方法1：dev に明示的に IdentityFile を指定
Host dev
    HostName dev-server.example.com
    User deploy
    Port 22
    IdentityFile ~/.ssh/id_ed25519_work  # ← 明示的に指定

# 修正方法2：Host * から IdentityFile を削除し、個別に指定
Host *
    User admin
    Port 2222
    # IdentityFile は各Hostで個別に指定する
```

**ポイント:** SSH設定ファイルでは、最初にマッチした値が優先されます。ただし、`Host *` は常にマッチするため、個別のHostで指定がない項目は `Host *` の値が使われます。`IdentityFile` は複数指定可能な項目なので、`Host *` の値が追加される形になります。

</details>

# 第7章：SSHエージェントと多段接続

## この章のゴール
- ssh-agentの仕組みと使い方を理解する
- パスフレーズ付き鍵を便利に運用できるようになる
- 踏み台サーバー（多段SSH）の設定をマスターする
- エージェントフォワーディングの利点とリスクを理解する

---

## 7.1 ssh-agent とは

**ssh-agent** は、SSH秘密鍵をメモリ上に保持し、パスフレーズの入力を省略するためのプログラムです。

### ssh-agent がない場合

```
1回目の接続: パスフレーズ入力 → 接続
2回目の接続: パスフレーズ入力 → 接続  ← 毎回入力が必要！
3回目の接続: パスフレーズ入力 → 接続
```

### ssh-agent がある場合

```
起動時: パスフレーズ入力 → 鍵をエージェントに登録

1回目の接続: エージェントが自動応答 → 接続  ← 入力不要！
2回目の接続: エージェントが自動応答 → 接続
3回目の接続: エージェントが自動応答 → 接続
```

---

## 7.2 ssh-agent の起動と鍵の登録

### ssh-agent の起動

```bash
# ssh-agent を起動してシェルに環境変数を設定
$ eval "$(ssh-agent -s)"
Agent pid 12345

# 確認
$ echo $SSH_AUTH_SOCK
/tmp/ssh-XXXXXX/agent.12344

$ echo $SSH_AGENT_PID
12345
```

### 鍵の登録（ssh-add）

```bash
# デフォルトの鍵を追加（~/.ssh/id_ed25519 等）
$ ssh-add
Enter passphrase for /home/user/.ssh/id_ed25519:   # パスフレーズを入力
Identity added: /home/user/.ssh/id_ed25519 (user@host)

# 特定の鍵を追加
$ ssh-add ~/.ssh/id_ed25519_github
$ ssh-add ~/.ssh/id_ed25519_work

# 登録されている鍵の一覧
$ ssh-add -l
256 SHA256:xxxxx... user@host (ED25519)
256 SHA256:yyyyy... github (ED25519)

# 登録されている公開鍵を表示
$ ssh-add -L
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@host
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... github

# すべての鍵をエージェントから削除
$ ssh-add -D
All identities removed.

# 特定の鍵を削除
$ ssh-add -d ~/.ssh/id_ed25519_github
```

### ssh-add のオプション

| オプション | 説明 |
|-----------|------|
| `-l` | 登録されている鍵のフィンガープリントを表示 |
| `-L` | 登録されている公開鍵を表示 |
| `-d <鍵>` | 特定の鍵を削除 |
| `-D` | すべての鍵を削除 |
| `-t <秒>` | 鍵の有効期限を設定 |
| `-x` | エージェントをロック（パスワード設定） |
| `-X` | エージェントのロックを解除 |

---

## 7.3 ssh-agent の自動起動

### シェルの設定ファイルに追加

```bash
# ~/.bashrc または ~/.zshrc に追加

# ssh-agent が起動していなければ起動する
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval "$(ssh-agent -s)" > /dev/null
    ssh-add ~/.ssh/id_ed25519 2>/dev/null
fi
```

### macOS の場合（キーチェーン連携）

```bash
# macOS ではキーチェーンと連携できる
$ ssh-add --apple-use-keychain ~/.ssh/id_ed25519

# ~/.ssh/config に追加
Host *
    AddKeysToAgent yes
    UseKeychain yes  # macOS のみ
```

### Windows（OpenSSH Agent Service）

```powershell
# サービスの状態確認
> Get-Service ssh-agent

# サービスを有効化して起動
> Set-Service ssh-agent -StartupType Automatic
> Start-Service ssh-agent

# 鍵を追加
> ssh-add $env:USERPROFILE\.ssh\id_ed25519
```

### ~/.ssh/config での自動追加

```
Host *
    AddKeysToAgent yes    # SSH接続時に自動的にエージェントに鍵を追加
```

---

## 7.4 鍵の有効期限設定

セキュリティのために、エージェントに登録した鍵に有効期限を設定できます。

```bash
# 1時間後に自動削除
$ ssh-add -t 3600 ~/.ssh/id_ed25519

# 30分後に自動削除
$ ssh-add -t 1800 ~/.ssh/id_ed25519

# エージェントをロック（離席時）
$ ssh-add -x
Enter lock password:
Agent locked.

# ロック解除
$ ssh-add -X
Enter lock password:
Agent unlocked.
```

---

## 7.5 エージェントフォワーディング

踏み台サーバー（bastion）経由で内部サーバーに接続する際、ローカルのssh-agentを踏み台サーバー上でも使えるようにする機能です。

### エージェントフォワーディングの仕組み

```
【フォワーディングなし】
ローカル → 踏み台 → 内部サーバー
  鍵あり    鍵なし!   接続失敗

【フォワーディングあり】
ローカル → 踏み台 → 内部サーバー
  鍵あり    ローカルの    接続成功!
            エージェント
            を転送
```

```
+----------+          +----------+          +----------+
| ローカル  |   SSH    |  踏み台   |   SSH    | 内部      |
| PC       |=========>| (bastion)|=========>| サーバー   |
|          | Agent    |          | Agent    |          |
| ssh-agent| Forward  |←認証要求 →| Forward  | 認証要求→ |
| 秘密鍵   |          | 踏み台に  |          |          |
|          |          | 鍵は不要！ |          |          |
+----------+          +----------+          +----------+
```

### 設定方法

```bash
# コマンドラインで有効化（-A オプション）
$ ssh -A user@bastion.example.com

# 踏み台上でそのまま内部サーバーに接続
user@bastion:~$ ssh internal-server
# ローカルの鍵が使われて接続成功！

# ~/.ssh/config での設定
Host bastion
    HostName bastion.example.com
    User admin
    ForwardAgent yes     # エージェントフォワーディングを有効化
```

### セキュリティ上の注意

> **重要**: エージェントフォワーディングにはセキュリティリスクがあります。踏み台サーバーの管理者（root）は、フォワードされたエージェントソケットを通じて、あなたの鍵で他のサーバーに接続できてしまいます。**信頼できるサーバーにのみ使用**してください。

```
リスク:
踏み台の root が SSH_AUTH_SOCK を利用して、
あなたの鍵で他のサーバーにアクセスする可能性がある

対策:
1. 信頼できるサーバーにのみ ForwardAgent yes を設定
2. ProxyJump（-J）を使う方がより安全（推奨）
3. ssh-add -c で鍵使用時に確認プロンプトを表示
```

---

## 7.6 多段SSH接続（ProxyJump）

踏み台サーバー経由で内部サーバーに接続する最も安全で簡潔な方法です。

### ProxyJump（-J オプション）

```bash
# 踏み台経由で内部サーバーに接続
$ ssh -J user@bastion.example.com user@internal-server

# 複数の踏み台を経由
$ ssh -J user@bastion1,user@bastion2 user@target-server

# ポートを指定
$ ssh -J user@bastion:2222 user@internal-server
```

### ProxyJump の仕組み

```
+----------+          +----------+          +----------+
| ローカル  |   SSH    |  踏み台   |   SSH    | 内部      |
| PC       |=========>| (bastion)|=========>| サーバー   |
|          | トンネル  |          | 転送     |          |
+----------+          +----------+          +----------+

ProxyJump は踏み台サーバーを通るSSHトンネルを作成し、
そのトンネル上に内部サーバーへのSSH接続を確立します。

エージェントフォワーディングとの違い:
- ProxyJump: 踏み台上に秘密鍵が露出しない（より安全）
- Agent Forward: 踏み台上でエージェントソケットが利用可能（リスクあり）
```

### ~/.ssh/config での設定（推奨）

```
# 踏み台サーバー
Host bastion
    HostName bastion.example.com
    User admin
    IdentityFile ~/.ssh/id_ed25519_work

# 内部サーバー（踏み台経由）
Host internal-*
    User appuser
    IdentityFile ~/.ssh/id_ed25519_work
    ProxyJump bastion

# 個別の内部サーバー
Host internal-web
    HostName 10.0.1.10

Host internal-db
    HostName 10.0.1.20

Host internal-app
    HostName 10.0.1.30
```

```bash
# これだけで踏み台経由で接続される
$ ssh internal-web
$ ssh internal-db
$ ssh internal-app

# SCP も透過的に動作
$ scp myfile.txt internal-web:~/

# rsync も透過的に動作
$ rsync -avz ./deploy/ internal-web:~/app/
```

---

## 7.7 ProxyCommand（高度な用途）

ProxyJump でカバーできない複雑なケースでは ProxyCommand を使います。

```
# ProxyJump と同等の設定
Host internal
    HostName 10.0.1.10
    ProxyCommand ssh -W %h:%p bastion

# ネットキャット経由（古い環境向け）
Host internal
    HostName 10.0.1.10
    ProxyCommand ssh bastion nc %h %p

# 条件付きプロキシ（社内ネットワークでは直接、外部では踏み台経由）
Host internal
    HostName 10.0.1.10
    ProxyCommand bash -c 'if ping -c1 -W1 10.0.1.10 &>/dev/null; then nc %h %p; else ssh -W %h:%p bastion; fi'
```

---

## 7.8 多段接続のトラブルシューティング

```bash
# 各段の接続を個別にテスト
# 1. 踏み台への接続
$ ssh -v bastion

# 2. 踏み台上から内部サーバーへの接続
$ ssh bastion
bastion$ ssh -v internal-web

# 3. ProxyJump の詳細ログ
$ ssh -vvv -J bastion internal-web

# よくある問題と対処
# 問題: 踏み台で "Permission denied"
# → 踏み台上の ~/.ssh/authorized_keys を確認

# 問題: 内部サーバーで "Connection refused"
# → 踏み台から内部サーバーの22番ポートに到達できるか確認
# bastion$ nc -zv 10.0.1.10 22

# 問題: "channel 0: open failed: connect failed"
# → 踏み台から内部ホストへのネットワーク接続を確認
```

---

## 7.9 ControlMaster（接続の多重化）

既存のSSH接続を再利用して、2回目以降の接続を高速化する機能です。

```
# ~/.ssh/config
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600    # 接続を600秒（10分）維持
```

```bash
# ソケット用ディレクトリを作成
$ mkdir -p ~/.ssh/sockets
$ chmod 700 ~/.ssh/sockets

# 1回目の接続（通常通り認証が行われる）
$ ssh dev
# 認証完了、マスター接続が確立

# 2回目以降の接続（瞬時に接続、認証不要）
$ ssh dev
# マスター接続を再利用 → ほぼ遅延なし！

# 接続状況の確認
$ ssh -O check dev
Master running (pid=12345)

# マスター接続を終了
$ ssh -O exit dev
Exit request sent.
```

### ControlMaster のメリット

```
1. 2回目以降のSSH接続が瞬時（TCP接続と認証をスキップ）
2. SCP/SFTP/rsync も高速化される
3. 多段接続（ProxyJump）のオーバーヘッドを削減
```

---

## ポイントまとめ

```
1. ssh-agent はパスフレーズ付き鍵を便利に運用するための仕組み
2. ssh-add で鍵をエージェントに登録、-t で有効期限を設定
3. AddKeysToAgent yes で接続時に自動登録
4. ProxyJump(-J) は踏み台経由の接続で最も安全な方法（推奨）
5. エージェントフォワーディングはセキュリティリスクがある → 信頼できるサーバーのみ
6. ControlMaster で既存接続を再利用して高速化
7. ~/.ssh/config にまとめて設定すれば運用が大幅に楽になる
```

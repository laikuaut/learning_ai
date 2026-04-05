# 第2章：SSHクライアントの基本操作

## この章のゴール
- sshコマンドの基本的な使い方をマスターする
- リモートサーバーへの接続と切断ができるようになる
- リモートコマンド実行の方法を理解する
- 接続時のオプションを使いこなせるようになる

---

## 2.1 sshコマンドの基本構文

```bash
ssh [オプション] [ユーザー名@]ホスト名 [コマンド]
```

### 最もシンプルな接続

```bash
# ユーザー名を指定して接続
$ ssh user@192.168.1.100

# ホスト名（FQDN）で接続
$ ssh user@example.com

# ユーザー名を省略（ローカルのユーザー名が使われる）
$ ssh 192.168.1.100

# ユーザー名を -l オプションで指定
$ ssh -l user 192.168.1.100
```

### 接続から切断までの流れ

```bash
# 1. 接続
$ ssh user@example.com
user@example.com's password:     # パスワードを入力（画面に表示されない）

# 2. リモートサーバー上で作業
user@server:~$ whoami
user
user@server:~$ hostname
server.example.com

# 3. 切断
user@server:~$ exit
logout
Connection to example.com closed.

# exit の代わりに Ctrl+D でも切断できます
```

---

## 2.2 ポート番号の指定

SSHサーバーがデフォルトの22番以外のポートで動作している場合、`-p` オプションで指定します。

```bash
# ポート2222で接続
$ ssh -p 2222 user@example.com

# ポート番号は URI 形式でも指定可能
$ ssh ssh://user@example.com:2222
```

---

## 2.3 リモートコマンド実行

対話的なシェルを開かずに、コマンドだけを実行して結果を受け取ることができます。

```bash
# リモートサーバーのディスク使用量を確認
$ ssh user@example.com df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   15G   33G  31% /

# リモートサーバーの稼働時間を確認
$ ssh user@example.com uptime
 10:23:45 up 120 days,  3:45,  2 users,  load average: 0.15, 0.10, 0.05

# 複数コマンドを実行（クォートで囲む）
$ ssh user@example.com "hostname && uptime && free -h"
server.example.com
 10:23:45 up 120 days,  3:45,  2 users,  load average: 0.15, 0.10, 0.05
              total        used        free      shared  buff/cache   available
Mem:          7.8Gi       2.1Gi       4.2Gi       256Mi       1.5Gi       5.3Gi

# パイプとリダイレクトの組み合わせ
$ ssh user@example.com "cat /var/log/syslog | grep error | tail -5" > local_errors.txt
```

### ローカルとリモートの区別

```bash
# リモートで実行される（リモートのファイルが表示される）
$ ssh user@example.com "cat /etc/hostname"

# パイプの左側はリモート、右側はローカルで処理
$ ssh user@example.com "cat /var/log/syslog" | grep error

# リモート側でパイプを使うにはクォートで囲む
$ ssh user@example.com "cat /var/log/syslog | grep error"
```

> **ポイント**: クォートなしだとローカルのシェルがパイプを解釈します。リモートで完結させたい処理はクォートで囲みましょう。

---

## 2.4 よく使うオプション

### 接続関連

```bash
# -v: 詳細なデバッグ情報を表示（トラブルシューティング時に重要）
$ ssh -v user@example.com
debug1: Connecting to example.com [93.184.216.34] port 22.
debug1: Connection established.
debug1: identity file /home/user/.ssh/id_ed25519 type 3
...

# -vv: さらに詳細な情報
$ ssh -vv user@example.com

# -vvv: 最も詳細な情報
$ ssh -vvv user@example.com
```

### 認証関連

```bash
# -i: 使用する秘密鍵ファイルを指定
$ ssh -i ~/.ssh/my_key user@example.com

# -o: SSHオプションを直接指定
$ ssh -o "IdentityFile=~/.ssh/my_key" user@example.com

# パスワード認証を強制（鍵認証をスキップ）
$ ssh -o "PreferredAuthentications=password" user@example.com

# 公開鍵認証を強制
$ ssh -o "PreferredAuthentications=publickey" user@example.com
```

### その他の便利なオプション

```bash
# -N: リモートコマンドを実行しない（ポートフォワーディング時に使用）
$ ssh -N -L 8080:localhost:80 user@example.com

# -f: バックグラウンドで実行
$ ssh -f -N -L 8080:localhost:80 user@example.com

# -t: 疑似端末を強制的に割り当て（sudoなど対話コマンドの実行時）
$ ssh -t user@example.com sudo apt update

# -C: 通信を圧縮（低速回線で有効）
$ ssh -C user@example.com

# -q: 警告メッセージを抑制
$ ssh -q user@example.com

# -4: IPv4 を強制
$ ssh -4 user@example.com

# -6: IPv6 を強制
$ ssh -6 user@example.com
```

---

## 2.5 主要オプション一覧

| オプション | 説明 | 使用例 |
|-----------|------|--------|
| `-p` | ポート番号を指定 | `ssh -p 2222 user@host` |
| `-i` | 秘密鍵ファイルを指定 | `ssh -i ~/.ssh/mykey user@host` |
| `-l` | ユーザー名を指定 | `ssh -l user host` |
| `-v` | デバッグモード（詳細表示） | `ssh -v user@host` |
| `-N` | リモートコマンドを実行しない | `ssh -N -L ...` |
| `-f` | バックグラウンドで実行 | `ssh -f -N -L ...` |
| `-t` | 疑似端末を強制割り当て | `ssh -t user@host sudo cmd` |
| `-C` | 通信を圧縮 | `ssh -C user@host` |
| `-q` | 静粛モード | `ssh -q user@host` |
| `-o` | SSH設定オプションを指定 | `ssh -o "Option=value"` |
| `-J` | ジャンプホスト経由で接続 | `ssh -J jump@bastion user@host` |
| `-X` | X11フォワーディング有効 | `ssh -X user@host` |
| `-D` | ダイナミックポートフォワーディング | `ssh -D 1080 user@host` |
| `-L` | ローカルポートフォワーディング | `ssh -L 8080:host:80 user@host` |
| `-R` | リモートポートフォワーディング | `ssh -R 8080:host:80 user@host` |

---

## 2.6 エスケープシーケンス

SSH接続中に特別な操作を行うためのキーシーケンスです。`~` （チルダ）をエスケープ文字として使用します。

> **重要**: エスケープシーケンスは**行頭**（Enter直後）で入力する必要があります。

```bash
# 主なエスケープシーケンス
~.     接続を強制切断（応答がなくなった時に有効）
~?     エスケープシーケンスのヘルプを表示
~~     チルダ文字をそのまま送信
~#     転送されたコネクションの一覧を表示
~C     SSHコマンドラインを開く（動的にポートフォワーディングを追加）
~^Z    SSHをバックグラウンドに移す（fg で復帰）
```

### 実践例：接続が固まった場合

```bash
# サーバーが応答しなくなった場合
user@server:~$ （応答なし、Ctrl+C も効かない）

# Enter キーを押してから ~. を入力
[Enter]
~.
Connection to example.com closed.
$
```

---

## 2.7 known_hostsの管理

`~/.ssh/known_hosts` ファイルには、過去に接続したサーバーのホスト鍵が記録されています。

### ホスト鍵の警告

サーバーのホスト鍵が変わった場合（サーバー再構築など）、以下の警告が出ます。

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
...
Host key verification failed.
```

### known_hostsの操作

```bash
# 特定ホストの鍵を削除
$ ssh-keygen -R example.com
# Host example.com found: line 5
/home/user/.ssh/known_hosts updated.

# 特定ホストの鍵を確認
$ ssh-keygen -F example.com
# Host example.com found: line 5
example.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA...

# サーバーのホスト鍵を事前に取得
$ ssh-keyscan example.com
# example.com:22 SSH-2.0-OpenSSH_9.6
example.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA...
example.com ssh-rsa AAAAB3NzaC1yc2EAAAA...

# 取得した鍵をknown_hostsに追加
$ ssh-keyscan example.com >> ~/.ssh/known_hosts
```

> **よくある間違い**: ホスト鍵の警告を見たら、安易に `known_hosts` から削除せず、まずサーバー管理者に鍵が本当に変更されたか確認しましょう。中間者攻撃（MITM）の可能性もあります。

---

## 2.8 接続のタイムアウト設定

接続の維持に関する設定です。

```bash
# 接続タイムアウト（秒）を指定
$ ssh -o "ConnectTimeout=10" user@example.com

# 接続維持（キープアライブ）設定
$ ssh -o "ServerAliveInterval=60" -o "ServerAliveCountMax=3" user@example.com
# 60秒ごとにキープアライブを送信、3回応答がなければ切断

# TCPキープアライブの無効化（通常は有効のまま）
$ ssh -o "TCPKeepAlive=yes" user@example.com
```

---

## ポイントまとめ

```
1. 基本構文: ssh [オプション] ユーザー名@ホスト名 [コマンド]
2. リモートコマンド実行はクォートで囲んでパイプの扱いに注意
3. -v オプションはトラブルシューティングの最初の一手
4. エスケープシーケンス ~. で固まった接続を強制切断できる
5. known_hosts はセキュリティ上重要 → 警告を安易に無視しない
6. -i で秘密鍵、-p でポート番号を指定
7. -t はリモートで sudo 等の対話コマンドを実行する時に必要
```

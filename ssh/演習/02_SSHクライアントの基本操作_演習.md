# 第2章 演習：SSHクライアントの基本操作

---

## 基本問題

### 問題1: 基本的な接続コマンド
以下の条件でSSH接続するコマンドを書いてください。

1. ホスト `192.168.1.100` にユーザー `admin` で接続
2. ホスト `example.com` にポート `2222` で接続（ユーザー名は `deploy`）
3. ホスト `server.example.com` に秘密鍵 `~/.ssh/id_ed25519_work` を使って接続（ユーザー名は `user`）

<details>
<summary>解答</summary>

```bash
# 1.
$ ssh admin@192.168.1.100

# 2.
$ ssh -p 2222 deploy@example.com

# 3.
$ ssh -i ~/.ssh/id_ed25519_work user@server.example.com
```

</details>

---

### 問題2: リモートコマンド実行
以下のそれぞれの操作を1行のコマンドで実行してください。

1. リモートサーバー `server` でディスク使用量を確認する
2. リモートサーバー `server` で `hostname` と `uptime` を連続実行する
3. リモートサーバー `server` の `/var/log/syslog` から "error" を含む行を抽出する（リモート側でフィルタリング）

<details>
<summary>解答</summary>

```bash
# 1.
$ ssh user@server df -h

# 2.
$ ssh user@server "hostname && uptime"

# 3.
$ ssh user@server "grep error /var/log/syslog"
# または
$ ssh user@server "cat /var/log/syslog | grep error"
```

</details>

---

### 問題3: ローカルとリモートの区別
以下の2つのコマンドの違いを説明してください。

```bash
# コマンドA
$ ssh user@server "cat /var/log/syslog | grep error"

# コマンドB
$ ssh user@server cat /var/log/syslog | grep error
```

<details>
<summary>解答</summary>

```
コマンドA: クォートで囲まれているため、cat と grep の両方がリモートで実行されます。
         リモートでフィルタリングされた結果のみが転送されるため、ネットワーク転送量が少なくなります。

コマンドB: grep はクォートの外にあるため、ローカルで実行されます。
         リモートの syslog 全体がネットワーク経由で転送され、ローカルの grep でフィルタリングされます。

結果は同じですが、コマンドAの方がネットワーク効率が良いです。
大きなファイルの場合はコマンドAを推奨します。
```

</details>

---

### 問題4: オプションの意味
以下の各オプションの意味を答えてください。

1. `ssh -v`
2. `ssh -N`
3. `ssh -t`
4. `ssh -C`
5. `ssh -J`

<details>
<summary>解答</summary>

```
1. -v  詳細なデバッグ情報を表示する（トラブルシューティング時に使用）
2. -N  リモートコマンドを実行しない（ポートフォワーディング時に使用）
3. -t  疑似端末を強制的に割り当てる（sudo等の対話コマンド実行時に使用）
4. -C  通信を圧縮する（低速回線で有効）
5. -J  ジャンプホスト（踏み台サーバー）経由で接続する
```

</details>

---

## 応用問題

### 問題5: エスケープシーケンス
SSH接続中にサーバーが応答しなくなりました。Ctrl+C も効きません。この状況で接続を強制切断する方法を説明してください。

<details>
<summary>ヒント</summary>

SSHのエスケープシーケンスは行頭で入力する必要があります。

</details>

<details>
<summary>解答</summary>

以下の手順で強制切断できます：

```
1. Enter キーを押す（行頭に移動）
2. ~ を入力
3. . を入力

つまり [Enter] ~. と入力します。

すると以下のように接続が切断されます：
Connection to example.com closed.
```

その他の便利なエスケープシーケンス：
- `~?` : ヘルプを表示
- `~#` : 転送されたコネクション一覧を表示
- `~C` : SSHコマンドラインを開く

</details>

---

### 問題6: known_hosts の管理
以下の状況での対処法をそれぞれ答えてください。

1. サーバー `example.com` を再構築したため、known_hosts から古いホスト鍵を削除したい
2. `example.com` のホスト鍵を事前に確認して known_hosts に追加したい
3. `example.com` が known_hosts に登録されているか確認したい

<details>
<summary>解答</summary>

```bash
# 1. 古いホスト鍵の削除
$ ssh-keygen -R example.com

# 2. ホスト鍵の事前取得と追加
$ ssh-keyscan example.com >> ~/.ssh/known_hosts

# 3. 登録の確認
$ ssh-keygen -F example.com
```

</details>

---

### 問題7: リモートでsudoを実行
リモートサーバー `server` で `sudo apt update` を実行したいのですが、以下のコマンドではエラーになります。なぜですか？また、正しいコマンドを書いてください。

```bash
$ ssh user@server sudo apt update
```

エラー: `sudo: a terminal is required to read the password`

<details>
<summary>解答</summary>

**原因**: `sudo` はパスワード入力のために疑似端末（TTY）が必要ですが、リモートコマンド実行モードではデフォルトで疑似端末が割り当てられないためです。

**正しいコマンド**:
```bash
# -t オプションで疑似端末を強制的に割り当てる
$ ssh -t user@server sudo apt update
```

`-t` オプションにより、リモート側に疑似端末が割り当てられ、`sudo` がパスワードプロンプトを表示できるようになります。

</details>

---

### 問題8: 接続タイムアウト
SSH接続が長時間放置すると切断される問題があります。以下の設定の意味を説明し、この問題を解決するコマンドラインオプションを書いてください。

```
ServerAliveInterval 60
ServerAliveCountMax 3
```

<details>
<summary>解答</summary>

**設定の意味**:
```
ServerAliveInterval 60
→ 60秒ごとにサーバーへキープアライブパケットを送信する

ServerAliveCountMax 3
→ 3回連続で応答がなかった場合に切断する

つまり、最大 60秒 × 3回 = 180秒（3分）応答がなければ切断。
逆に言えば、サーバーが生きている限り60秒ごとに通信が発生するため、
NATやファイアウォールによるアイドルタイムアウトを防止できる。
```

**コマンドラインオプション**:
```bash
$ ssh -o "ServerAliveInterval=60" -o "ServerAliveCountMax=3" user@example.com
```

</details>

---

## チャレンジ問題

### 問題9: 複合的なリモート操作
以下の操作を1つのコマンドで実現してください。

「リモートサーバー `server` の `/var/log/nginx/access.log` から直近100行を取得し、ステータスコード 500 を含む行だけを抽出して、ローカルの `errors.txt` に保存する」

<details>
<summary>ヒント</summary>

リモートでフィルタリングしてからローカルにリダイレクトするパターンを使います。

</details>

<details>
<summary>解答</summary>

```bash
# 方法1: リモートで全処理、結果をローカルに保存
$ ssh user@server "tail -100 /var/log/nginx/access.log | grep ' 500 '" > errors.txt

# 方法2: リモートで tail だけ実行、ローカルで grep
$ ssh user@server "tail -100 /var/log/nginx/access.log" | grep " 500 " > errors.txt
```

方法1の方がネットワーク転送量が少なく効率的です。

</details>

---

### 問題10: デバッグ出力の活用
SSH接続時に `ssh -v user@example.com` を実行した際のデバッグ出力から、以下の情報を読み取る方法を説明してください。

1. どの認証方式が使われたか
2. どの秘密鍵ファイルが使用されたか
3. 接続先サーバーのSSHバージョン

<details>
<summary>解答</summary>

```bash
# 1. 認証方式の確認
$ ssh -v user@example.com 2>&1 | grep "Authentication succeeded"
# 出力例: debug1: Authentication succeeded (publickey).
# → publickey（公開鍵認証）が使われた

# 2. 使用された秘密鍵ファイル
$ ssh -v user@example.com 2>&1 | grep "Offering"
# 出力例: debug1: Offering public key: /home/user/.ssh/id_ed25519 ED25519
# → /home/user/.ssh/id_ed25519 が使用された

# 3. 接続先のSSHバージョン
$ ssh -v user@example.com 2>&1 | grep "remote software version"
# 出力例: debug1: Remote protocol version 2.0, remote software version OpenSSH_9.6
# → OpenSSH 9.6
```

`-v` の出力は標準エラー出力（stderr）に出るため、`2>&1` でリダイレクトしてから grep する必要があります。

</details>

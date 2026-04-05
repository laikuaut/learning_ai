# 第7章 演習：SSHエージェントと多段接続

---

## 基本問題

### 問題1: ssh-agentの基本操作
以下の操作のコマンドを書いてください。

1. ssh-agentを起動する
2. デフォルトの鍵をエージェントに登録する
3. 特定の鍵 `~/.ssh/id_ed25519_work` を登録する
4. 登録されている鍵の一覧を表示する
5. すべての鍵をエージェントから削除する

<details>
<summary>解答</summary>

```bash
# 1. ssh-agentの起動
$ eval "$(ssh-agent -s)"

# 2. デフォルトの鍵を登録
$ ssh-add

# 3. 特定の鍵を登録
$ ssh-add ~/.ssh/id_ed25519_work

# 4. 鍵の一覧表示
$ ssh-add -l

# 5. すべての鍵を削除
$ ssh-add -D
```

</details>

---

### 問題2: ssh-addのオプション
以下の各オプションの意味を答えてください。

1. `ssh-add -l`
2. `ssh-add -L`
3. `ssh-add -d ~/.ssh/id_ed25519`
4. `ssh-add -t 3600 ~/.ssh/id_ed25519`
5. `ssh-add -x`

<details>
<summary>解答</summary>

```
1. -l  登録されている鍵のフィンガープリントを一覧表示する
2. -L  登録されている鍵の公開鍵を一覧表示する
3. -d  指定した鍵をエージェントから削除する
4. -t  鍵の有効期限を設定する（この例では3600秒 = 1時間後に自動削除）
5. -x  エージェントをロックする（パスワードを設定し、ロック中は鍵が使えない）
```

</details>

---

### 問題3: ProxyJumpの基本
以下の構成で、踏み台経由で内部サーバーに接続するコマンドを書いてください。

```
ローカルPC → bastion.example.com → 10.0.1.10
ユーザー: admin（踏み台）、webapp（内部サーバー）
```

<details>
<summary>解答</summary>

```bash
# コマンドラインで指定
$ ssh -J admin@bastion.example.com webapp@10.0.1.10

# ~/.ssh/config で設定する場合
Host bastion
    HostName bastion.example.com
    User admin

Host internal
    HostName 10.0.1.10
    User webapp
    ProxyJump bastion

# 設定後は以下だけで接続
$ ssh internal
```

</details>

---

### 問題4: エージェントフォワーディング
エージェントフォワーディングを有効にする方法を2つ（コマンドライン、設定ファイル）書いてください。

<details>
<summary>解答</summary>

```bash
# 方法1: コマンドラインオプション
$ ssh -A user@bastion

# 方法2: ~/.ssh/config での設定
Host bastion
    HostName bastion.example.com
    User admin
    ForwardAgent yes
```

</details>

---

## 応用問題

### 問題5: セキュリティの比較
エージェントフォワーディングとProxyJumpの安全性の違いを説明してください。なぜProxyJumpの方が推奨されるのですか？

<details>
<summary>解答</summary>

```
【エージェントフォワーディング（-A / ForwardAgent yes）】
- 踏み台サーバー上にエージェントソケットが作成される
- 踏み台サーバーの管理者（root）がそのソケットを利用して、
  あなたの鍵で他のサーバーにアクセスできてしまう
- リスク: 踏み台が侵害されると、鍵が悪用される可能性がある

【ProxyJump（-J）】
- 踏み台サーバーを通るSSHトンネルを��成するだけ
- 秘密鍵はローカルPCにのみ存在し、踏み台には露出しない
- 踏み台はデータを中継するだけで、鍵にアクセスできない
- リスクが格段に低い

推奨される理由:
ProxyJumpは秘密鍵を踏み台に露出させないため、
踏み台が侵害されても鍵の悪用リスクがない。
```

</details>

---

### 問題6: 多段ProxyJump
以下の3段構成で、最終目標のサーバーに接続するコマンドと設定ファイルを書いてください。

```
ローカルPC → bastion1 → bastion2 → target-server
```

<details>
<summary>解答</summary>

```bash
# コマンドラインで複数の踏み台を経由
$ ssh -J user@bastion1,user@bastion2 user@target-server

# ~/.ssh/config での設定
Host bastion1
    HostName bastion1.example.com
    User user

Host bastion2
    HostName bastion2.example.com
    User user
    ProxyJump bastion1

Host target
    HostName target-server.example.com
    User user
    ProxyJump bastion2

# 使い方
$ ssh target
```

</details>

---

### 問題7: ControlMaster
ControlMaster（接続の多重化）の設定を書き、そのメリットを3つ挙げてください。

<details>
<summary>解答</summary>

設定（~/.ssh/config）:
```
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600
```

セットアップ:
```bash
$ mkdir -p ~/.ssh/sockets
$ chmod 700 ~/.ssh/sockets
```

メリット:
```
1. 2回目以降の接続が瞬時（TCP接続と認証のオーバーヘッドがゼロ）
2. SCP/SFTP/rsync 等のファイル転送も高速化される
3. ProxyJump使用時の多段接続のオーバーヘッドを大幅に削減

仕組み:
1回目の接続でマスター接続が確立され、
2回目以降は同じTCPコネクションを再利用するため高速。
```

</details>

---

### 問題8: ssh-agentの自動起動
シェルの起動時にssh-agentを自動起動し、デフォルトの鍵を登録するスクリプトを `.bashrc` に追加する形で書いてください。

<details>
<summary>解答</summary>

```bash
# ~/.bashrc に追加

# ssh-agent が起動していなければ起動する
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval "$(ssh-agent -s)" > /dev/null
    ssh-add ~/.ssh/id_ed25519 2>/dev/null
fi
```

または、`~/.ssh/config` で自動追加を設定する方法:
```
Host *
    AddKeysToAgent yes
```

この設定では、SSH接続時に使用された鍵が自動的にエージェントに追加されます（初回のみパスフレーズ入力が必要）。

</details>

---

## チャレンジ問題

### 問題9: 総合設計
以下の環境に対応する完全な設定（~/.ssh/config + 鍵管理 + エージェント設定）を設計してください。

環境:
- GitHub: 鍵 `id_ed25519_github`
- 会社の踏み台: `bastion.corp.com`
- 内部サーバー3台: `web(10.0.1.10)`, `api(10.0.1.20)`, `db(10.0.1.30)`
- パスフレーズ付き鍵を使用
- 接続の多重化で高速化
- キープアライブ設定

<details>
<summary>解答</summary>

```bash
# 1. 鍵の生成
$ ssh-keygen -t ed25519 -C "github" -f ~/.ssh/id_ed25519_github
$ ssh-keygen -t ed25519 -C "work" -f ~/.ssh/id_ed25519_work

# 2. ソケット用ディレクトリの作成
$ mkdir -p ~/.ssh/sockets
$ chmod 700 ~/.ssh/sockets
```

~/.ssh/config:
```
# --- GitHub ---
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github

# --- 踏み台 ---
Host bastion
    HostName bastion.corp.com
    User admin
    IdentityFile ~/.ssh/id_ed25519_work

# --- 内部サーバー（踏み台経由） ---
Host web
    HostName 10.0.1.10
    User webapp
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work

Host api
    HostName 10.0.1.20
    User appuser
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work

Host db
    HostName 10.0.1.30
    User dbadmin
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work

# --- 共通設定 ---
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    IdentitiesOnly yes
    AddKeysToAgent yes
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600
```

使い方:
```bash
$ ssh web          # 踏み台経由でWebサーバーに接続
$ scp file web:~/  # 透過的にファイルコピー
$ rsync -avz ./deploy/ api:~/app/  # 透過的に同期
```

</details>

---

### 問題10: トラブルシューティング
踏み台経由の接続 `ssh -J bastion internal-web` が失敗しています。問題の原因を特定するための手順を順番に説明してください。

<details>
<summary>解答</summary>

```bash
# ステップ1: 踏み台への接続をテスト
$ ssh -v bastion
# → 成功すれば踏み台までの接続は問題なし
# → 失敗すれば踏み台への接続が原因

# ステップ2: 踏み���上から内部サーバーへの接続をテスト
$ ssh bastion
bastion$ ssh -v internal-web
# → 成功すれば踏み台から内部サーバーは到達可能
# → 失敗すれば踏み台〜内部サーバー間が原因

# ステップ3: 踏み台から内部サーバーのポート疎通を確認
bastion$ nc -zv 10.0.1.10 22
# → "Connection to 10.0.1.10 22 port [tcp/ssh] succeeded!"
# → 失敗すればネットワークまたはファイアウォールの問題

# ステップ4: ProxyJumpの詳細ログで確認
$ ssh -vvv -J bastion internal-web
# → debug出力からどの段階で失敗しているか特定

# よくある原因:
# 1. 踏み台への認証失敗（鍵が間違っている）
# 2. 踏み台から内部サーバーへのネットワーク不通
# 3. 内部サーバーの authorized_keys に鍵が未登録
# 4. パーミッションの問題（.ssh: 700, authorized_keys: 600）
# 5. ファイアウォールで踏み台→内部サーバーのSSHがブロック
```

</details>

# 第4章 演習：SSH設定ファイル

---

## 基本問題

### 問題1: 基本的な設定
以下の条件で `~/.ssh/config` の設定を書いてください。

- エイリアス名: `dev`
- ホスト名: `dev-server.example.com`
- ユーザー名: `developer`
- ポート: `2222`
- 秘密鍵: `~/.ssh/id_ed25519_work`

<details>
<summary>解答</summary>

```
Host dev
    HostName dev-server.example.com
    User developer
    Port 2222
    IdentityFile ~/.ssh/id_ed25519_work
```

設定後は `ssh dev` だけで接続できます。

</details>

---

### 問題2: 設定の適用順序
以下の設定がある場合、`ssh dev` と `ssh staging` で使用されるユーザー名はそれぞれ何ですか？

```
Host dev
    HostName dev.example.com
    User devuser

Host staging
    HostName staging.example.com

Host *
    User defaultuser
```

<details>
<summary>解答</summary>

```
ssh dev     → ユーザー名: devuser
  理由: Host dev の設定で User devuser が指定されている

ssh staging → ユーザー名: defaultuser
  理由: Host staging に User の指定がないため、
       Host * の User defaultuser が適用される

設定は上から順に読み込まれ、最初にマッチした値が使われます。
具体的な設定を上に、一般的な設定（Host *）を下に書くのがポイントです。
```

</details>

---

### 問題3: ワイルドカード
以下の要件を満たす `~/.ssh/config` の設定を書いてください。

1. すべてのホストに対して、60秒ごとにキープアライブを送信する
2. `*.example.com` ドメインのすべてのサーバーに `admin` ユーザーで接続する
3. 指定した鍵のみを使用する（余計な鍵を送信しない）

<details>
<summary>解答</summary>

```
Host *.example.com
    User admin

Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    IdentitiesOnly yes
```

</details>

---

### 問題4: 設定項目の意味
以下の設定項目の意味をそれぞれ答えてください。

1. `IdentitiesOnly yes`
2. `AddKeysToAgent yes`
3. `HashKnownHosts yes`
4. `ConnectTimeout 10`

<details>
<summary>解答</summary>

```
1. IdentitiesOnly yes
   → 指定したIdentityFileの鍵のみを使用する。
     ssh-agentに登録されている他の鍵は送信しない。
     セキュリティ上、余計な鍵の情報を送らないために推奨。

2. AddKeysToAgent yes
   → SSH接続時に使用した鍵を自動的にssh-agentに追加する。
     2回目以降のパスフレーズ入力が不要になる。

3. HashKnownHosts yes
   → known_hostsファイルのホスト名をハッシュ化して保存する。
     ファイルが流出しても、接続先一覧が分からなくなる。

4. ConnectTimeout 10
   → 接続試行のタイムアウトを10秒に設定する。
     10秒以内に接続できなければ失敗とする。
```

</details>

---

## 応用問題

### 問題5: 踏み台サーバー経由の接続
以下の構成で、ローカルPCから内部Webサーバーに接続するための `~/.ssh/config` を書いてください。

```
ローカルPC → bastion.example.com（踏み台） → 10.0.1.10（内部Web）
                                             → 10.0.1.20（内部DB）
```

- 踏み台: ユーザー `admin`、ポート 22
- 内部Web: ユーザー `webapp`
- 内部DB: ユーザー `dbadmin`
- すべて同じ秘密鍵 `~/.ssh/id_ed25519_work` を使用

<details>
<summary>解答</summary>

```
Host bastion
    HostName bastion.example.com
    User admin
    IdentityFile ~/.ssh/id_ed25519_work

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
```

使い方：
```bash
$ ssh internal-web   # 踏み台経由で内部Webサーバーに接続
$ ssh internal-db    # 踏み台経由で内部DBサーバーに接続
```

</details>

---

### 問題6: sshd_config のセキュリティ
以下の `sshd_config` の設定を見て、セキュリティ上の問題点を3つ以上指摘してください。

```
Port 22
PermitRootLogin yes
PasswordAuthentication yes
PermitEmptyPasswords yes
MaxAuthTries 10
X11Forwarding yes
```

<details>
<summary>解答</summary>

**問題点:**

```
1. PermitRootLogin yes
   → root で直接ログインできるため、攻撃対象になりやすい
   → 対策: PermitRootLogin no に変更

2. PasswordAuthentication yes
   → パスワード認証が有効なため、ブルートフォース攻撃を受ける
   → 対策: PasswordAuthentication no に変更（公開鍵認証のみ）

3. PermitEmptyPasswords yes
   → 空パスワードでのログインを許可している（非常に危険）
   → 対策: PermitEmptyPasswords no に変更

4. MaxAuthTries 10
   → 認証試行回数が多すぎ、パスワード推測攻撃の余地を与える
   → 対策: MaxAuthTries 3 程度に制限

5. X11Forwarding yes
   → X11フォワーディングが有効（不要なら攻撃面を増やす）
   → 対策: X11Forwarding no に変更（GUIが不要な場合）
```

</details>

---

### 問題7: 設定の確認
SSH接続時に、特定のホストに対してどの設定が適用されるかを確認するコマンドは何ですか？ `dev` ホストに対する確認コマンドを書いてください。

<details>
<summary>解答</summary>

```bash
# ssh -G でホストに適用される実効設定を一覧表示
$ ssh -G dev

# 特定の項目だけ確認する場合
$ ssh -G dev | grep -i user
$ ssh -G dev | grep -i hostname
$ ssh -G dev | grep -i port
$ ssh -G dev | grep -i identityfile
```

`-G` オプションは実際に接続せず、適用される設定値を出力します。設定のデバッグに非常に便利です。

</details>

---

## チャレンジ問題

### 問題8: 完全な設定ファイル設計
以下の環境に対応する `~/.ssh/config` を設計してください。

要件:
- GitHub（個人）: 鍵 `~/.ssh/id_ed25519_github`
- 会社の踏み台: `bastion.corp.example.com`、ユーザー `admin`
- 会社の開発サーバー: `10.0.1.100`、ユーザー `dev`、踏み台経由
- 会社の本番サーバー: `10.0.1.200`、ユーザー `deploy`、踏み台経由
- 個人VPS: `vps.example.com`、ポート `2222`、ユーザー `user`
- 全ホスト共通: キープアライブ60秒、指定鍵のみ使用、ssh-agent自動追加

<details>
<summary>解答</summary>

```
# --- GitHub ---
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github

# --- 会社の踏み台 ---
Host bastion
    HostName bastion.corp.example.com
    User admin
    IdentityFile ~/.ssh/id_ed25519_work

# --- 会社の���発サーバー ---
Host work-dev
    HostName 10.0.1.100
    User dev
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work

# --- 会社の本番サーバー ---
Host work-prod
    HostName 10.0.1.200
    User deploy
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519_work

# --- 個人VPS ---
Host vps
    HostName vps.example.com
    User user
    Port 2222
    IdentityFile ~/.ssh/id_ed25519_vps

# --- 共通設定 ---
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    IdentitiesOnly yes
    AddKeysToAgent yes
    HashKnownHosts yes
```

</details>

---

### 問題9: sshd_config の変更手順
SSHサーバーの設定（`sshd_config`）を安全に変更する手順を正しい順番に並べ替えてください。

a) 設定ファイルの文法チェック（`sshd -t`）
b) 別のターミナルから新しい接続をテスト
c) 設定ファイルのバックアップ
d) SSHDのリロード（`systemctl reload sshd`）
e) 設定ファイルを編集
f) 現在のSSH接続を維持する（切断しない）

<details>
<summary>解答</summary>

正しい順番: **f → c → e → a → d → b**

```
1. f) 現在のSSH接続を維持する（切断��ない）
   → ���定ミスがあった場合の保険

2. c) 設定ファイルのバックアップ
   → sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

3. e) 設定ファイルを編集
   → sudo vim /etc/ssh/sshd_config

4. a) 設定ファイルの文法チェック
   → sudo sshd -t（エラーがなければ何も表示されない）

5. d) SSHDのリロード
   → sudo systemctl reload sshd（既存接続は切断されない）

6. b) 別のターミナルから��しい接続をテスト
   → 新しい設定で接続できることを確認

失敗した場合は既存接続からバックアップを復元:
   → sudo cp /etc/ssh/sshd_config.bak /etc/ssh/sshd_config
   → sudo systemctl reload sshd
```

</details>

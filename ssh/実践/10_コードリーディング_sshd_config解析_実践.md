# 実践課題10：コードリーディング ─ sshd_config解析 ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第3章（公開鍵認証の設定）、第4章（SSH設定ファイル）、第8章（SSHのセキュリティと運用）
> **課題の種類**: コードリーディング
> **学習目標**: SSHサーバー設定ファイル（sshd_config）を読み解き、各設定項目のセキュリティ上の意味と影響を理解する

---

## 課題の説明

以下は、ある企業の本番サーバーで使われている `sshd_config` の設定です。
設定を読んで、後に続く **10個の設問** に答えてください。

**実行は不要です。設定ファイルを読んで理解する力を鍛える課題です。**

---

## 読解対象の設定ファイル

```bash
# /etc/ssh/sshd_config
# 本番サーバー用SSH設定
# 最終更新: 2026-03-15

# ==================== 基本設定 ====================
Port 22
Port 2222
AddressFamily inet
ListenAddress 0.0.0.0

Protocol 2

# ==================== 認証設定 ====================
LoginGraceTime 30
PermitRootLogin no
StrictModes yes
MaxAuthTries 3
MaxSessions 5

PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys

PasswordAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no

# ==================== 鍵交換・暗号化 ====================
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
HostKeyAlgorithms ssh-ed25519,rsa-sha2-512,rsa-sha2-256

# ==================== アクセス制御 ====================
AllowUsers deploy monitoring
AllowGroups sshusers
DenyUsers root admin test guest
DenyGroups noremote

# ==================== ログ設定 ====================
SyslogFacility AUTH
LogLevel VERBOSE

# ==================== セッション設定 ====================
X11Forwarding no
AllowTcpForwarding yes
GatewayPorts no
PermitTunnel no
PrintMotd yes
PrintLastLog yes

ClientAliveInterval 300
ClientAliveCountMax 2

# ==================== 制限設定 ====================
Banner /etc/ssh/banner.txt

# chroot設定（sftpユーザー用）
Subsystem sftp internal-sftp

Match User sftponly
    ChrootDirectory /home/%u
    ForceCommand internal-sftp
    AllowTcpForwarding no
    X11Forwarding no
    PermitTunnel no

Match Group developers
    AllowTcpForwarding yes
    PermitTunnel yes
    MaxSessions 10

Match Address 10.0.0.0/8
    PasswordAuthentication yes
    MaxAuthTries 5
```

---

## 設問

以下の10問に答えてください。

### 問1：ポート設定

この設定では2つのポートが指定されています。このような設定にする実務上の理由を説明してください。

### 問2：認証方式

この設定で許可されている認証方式と禁止されている認証方式をそれぞれ列挙してください。

### 問3：ブルートフォース対策

ブルートフォース攻撃（brute force attack）への対策となっている設定項目を3つ以上挙げ、それぞれの効果を説明してください。

### 問4：暗号化アルゴリズム

`KexAlgorithms`、`Ciphers`、`MACs` で指定されているアルゴリズムの特徴を説明してください。なぜこれらが選ばれていると考えられますか？

### 問5：AllowUsersとDenyUsers

`AllowUsers` と `DenyUsers` が同時に指定されています。ユーザー `webadmin`（sshusersグループ所属）が接続しようとした場合、どうなりますか？

### 問6：ClientAliveの設定

`ClientAliveInterval 300` と `ClientAliveCountMax 2` の組み合わせは、無通信状態が何分続くとセッションが切断されることを意味しますか？計算過程も示してください。

### 問7：Matchブロック

3つの `Match` ブロックがあります。それぞれが適用される条件と、その効果を説明してください。

### 問8：sftponly ユーザーの制限

`Match User sftponly` の設定で `ChrootDirectory` と `ForceCommand` が指定されています。これによりsftponlyユーザーにどのような制限がかかりますか？

### 問9：内部ネットワークからの例外

`Match Address 10.0.0.0/8` ブロックの設定は、セキュリティ上どのようなトレードオフ（trade-off）がありますか？利点とリスクを説明してください。

### 問10：改善提案

この設定に対して、セキュリティまたは運用の観点から改善提案を2つ以上考えてください。

---

## 解答例

<details>
<summary>問1の解答：ポート設定</summary>

2つのポート（22番と2222番）でリッスンする理由：

1. **互換性の確保**: 標準ポート22番は、既存のスクリプトやツールがデフォルトで使用するため維持
2. **アクセス経路の冗長化**: ファイアウォールの設定変更時やポートスキャン対策として代替ポートを用意
3. **段階的な移行**: 将来的に22番を閉じて2222番のみにする場合の移行期間

実務では、セキュリティスキャナーが22番を集中的に狙うため、2222番など非標準ポートを用意することがあります。ただし、ポート変更は「隠蔽によるセキュリティ」であり、根本的な対策ではありません。

</details>

<details>
<summary>問2の解答：認証方式</summary>

**許可されている認証方式:**
- 公開鍵認証（`PubkeyAuthentication yes`）

**禁止されている認証方式:**
- パスワード認証（`PasswordAuthentication no`）
- 空パスワード（`PermitEmptyPasswords no`）
- チャレンジレスポンス認証（`ChallengeResponseAuthentication no`）

ただし `Match Address 10.0.0.0/8` により、内部ネットワーク（10.0.0.0/8）からの接続に限り、パスワード認証も許可されています。

</details>

<details>
<summary>問3の解答：ブルートフォース対策</summary>

1. **`PasswordAuthentication no`**: パスワード認証を無効化し、ブルートフォースの主要な攻撃対象を排除
2. **`MaxAuthTries 3`**: 認証の試行回数を3回に制限し、大量の試行を防止
3. **`LoginGraceTime 30`**: 認証に30秒の制限時間を設定し、自動化ツールの効率を低下させる
4. **`PermitRootLogin no`**: rootユーザーへの直接ログインを禁止し、最も狙われやすいアカウントを保護
5. **`DenyUsers root admin test guest`**: よく狙われるユーザー名を明示的にブロック
6. **`AllowUsers deploy monitoring`**: 接続可能なユーザーをホワイトリスト方式で限定

</details>

<details>
<summary>問4の解答：暗号化アルゴリズム</summary>

**KexAlgorithms（鍵交換）:**
- `curve25519-sha256` : 楕円曲線Diffie-Hellman。高速で安全性が高い
- 古いアルゴリズム（diffie-hellman-group1等）を排除している

**Ciphers（暗号化）:**
- `chacha20-poly1305` : ChaCha20ストリーム暗号 + Poly1305認証。AES-NIがない環境でも高速
- `aes256-gcm`, `aes128-gcm` : AESのGCMモード。認証暗号化を提供
- CBC モードが排除されている（パディングオラクル攻撃への耐性）

**MACs（メッセージ認証）:**
- `hmac-sha2-512-etm`, `hmac-sha2-256-etm` : Encrypt-then-MAC方式。暗号化後に認証
- `etm`（Encrypt-then-MAC）は `mac`（MAC-then-Encrypt）より安全

これらが選ばれている理由は、現在知られている脆弱性のないモダンなアルゴリズムのみを許可し、レガシーな弱いアルゴリズムをすべて排除するためです。

</details>

<details>
<summary>問5の解答：AllowUsersとDenyUsers</summary>

`webadmin` は接続**できません**。

`AllowUsers` が指定されている場合、そこに含まれるユーザーのみがログイン可能です。`webadmin` は `AllowUsers deploy monitoring` に含まれていないため、たとえ `sshusers` グループに所属していても、`AllowGroups sshusers` だけでは接続できません。

SSHのアクセス制御の評価順序：
1. `DenyUsers` → 一致すればログイン拒否
2. `AllowUsers` → 指定がある場合、一致しなければ拒否
3. `DenyGroups` → 一致すればログイン拒否
4. `AllowGroups` → 指定がある場合、一致しなければ拒否

`AllowUsers` が指定されている時点で、そこに列挙されたユーザーのみが許可されます。

</details>

<details>
<summary>問6の解答：ClientAliveの計算</summary>

**最大 10分（600秒）** で切断されます。

計算：
```
切断までの時間 = ClientAliveInterval × (ClientAliveCountMax + 1)
             = 300秒 × (2 + 1)
             = 300秒 × 3
             = 900秒 = 15分
```

正確には：
- 300秒（5分）間通信がないと、サーバーが1回目のキープアライブを送信
- さらに300秒応答がないと、2回目のキープアライブを送信
- `ClientAliveCountMax 2` は「2回の無応答を許容」なので、2回無応答の後に切断

つまり **300秒 × 2 = 600秒（10分）の無応答後** にキープアライブの失敗が `ClientAliveCountMax` に達し、切断されます。最初の300秒は通常の無通信期間なので、合計では最大 **15分** 程度です。

</details>

<details>
<summary>問7の解答：Matchブロック</summary>

1. **`Match User sftponly`**
   - 条件：`sftponly` ユーザーが接続した場合
   - 効果：chroot環境でSFTPのみ許可。シェルアクセスやポートフォワーディングを禁止

2. **`Match Group developers`**
   - 条件：`developers` グループに所属するユーザーが接続した場合
   - 効果：TCPフォワーディングとトンネルを許可。セッション数の上限を10に緩和。開発者がポートフォワーディングを使えるようにしている

3. **`Match Address 10.0.0.0/8`**
   - 条件：10.0.0.0/8（プライベートIPアドレス範囲）からの接続
   - 効果：パスワード認証を許可し、MaxAuthTriesを5に緩和。内部ネットワークからの管理を容易にしている

</details>

<details>
<summary>問8の解答：sftponlyの制限</summary>

`sftponly` ユーザーには以下の制限がかかります：

1. **`ChrootDirectory /home/%u`**: ユーザーのホームディレクトリがルートディレクトリとして見える。つまり `/home/sftponly` 以外のディレクトリにアクセスできない
2. **`ForceCommand internal-sftp`**: ログインシェルの代わりにSFTPサーバーが強制実行される。シェルコマンドの実行が不可能
3. **`AllowTcpForwarding no`**: ポートフォワーディングが禁止される
4. **`X11Forwarding no`**: X11転送が禁止される
5. **`PermitTunnel no`**: トンネリングが禁止される

結果として、`sftponly` ユーザーは自分のホームディレクトリ内でのファイルのアップロード・ダウンロードのみが可能で、それ以外の操作はすべて制限されます。

</details>

<details>
<summary>問9の解答：内部ネットワーク例外のトレードオフ</summary>

**利点:**
- 内部ネットワークからの管理が容易（公開鍵の設定なしでも接続可能）
- 緊急時のアクセス手段を確保（鍵を紛失した場合のバックアップ）
- 新規ユーザーの初期セットアップが簡単

**リスク:**
- 内部ネットワークが侵害された場合、パスワード認証への攻撃が可能になる
- 内部からのブルートフォース攻撃を許容してしまう
- 「内部ネットワーク = 安全」という前提が崩れた場合のリスクが大きい
- ゼロトラストの考え方に反している

**推奨:**
内部ネットワークでもパスワード認証を無効にし、鍵の初期配布は別の手段（構成管理ツール、USBメモリ等）で行うのが望ましいです。

</details>

<details>
<summary>問10の解答：改善提案</summary>

1. **`Match Address 10.0.0.0/8` のパスワード認証を無効化**
   - 内部ネットワークでも公開鍵認証を必須にする
   - 鍵の配布は Ansible 等の構成管理ツールで自動化

2. **`Protocol 2` の削除**
   - 現在のOpenSSHはSSH-2のみサポートしており、`Protocol 2` は廃止された設定項目
   - 不要な設定は削除して可読性を向上

3. **fail2ban の導入**
   - `MaxAuthTries` だけでなく、一定回数の認証失敗でIPアドレスを一時的にブロック

4. **`ListenAddress` の限定**
   - `0.0.0.0`（全インターフェース）ではなく、必要なインターフェースのみにバインド
   - 例：`ListenAddress 10.0.0.5`（管理用ネットワークのみ）

5. **2要素認証（2FA）の導入**
   - Google AuthenticatorやYubiKeyによる追加認証レイヤー
   - `AuthenticationMethods publickey,keyboard-interactive`

</details>

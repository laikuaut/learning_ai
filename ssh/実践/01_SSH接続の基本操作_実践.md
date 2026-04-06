# 実践課題01：SSH接続の基本操作 ★1

> **難易度**: ★☆☆☆☆（入門）
> **前提知識**: 第1章（SSHの基礎知識）、第2章（SSHクライアントの基本操作）
> **課題の種類**: ミニプロジェクト
> **学習目標**: SSHコマンドの基本的な使い方を確認し、リモートサーバーへの接続・コマンド実行・切断の一連の操作を体験する

---

## 完成イメージ

```
# サーバーに接続してシステム情報を取得する
$ ssh user@192.168.1.100
Welcome to Ubuntu 22.04 LTS

user@server:~$ hostname
server01

user@server:~$ uname -a
Linux server01 5.15.0-91-generic #101-Ubuntu SMP x86_64 GNU/Linux

user@server:~$ uptime
 14:23:05 up 45 days,  3:12,  1 user,  load average: 0.08, 0.03, 0.01

user@server:~$ df -h /
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   12G   36G  25% /

user@server:~$ exit
Connection to 192.168.1.100 closed.
```

---

## 課題の要件

1. SSHでリモートサーバーに接続する
2. 以下の情報を取得するコマンドを実行する
   - ホスト名（`hostname`）
   - OS情報（`uname -a`）
   - 稼働時間（`uptime`）
   - ディスク使用量（`df -h`）
   - メモリ使用量（`free -h`）
3. 接続を切断する
4. リモートコマンド実行（接続せずにコマンドだけ実行する方法）を試す
5. 取得した情報をローカルファイルに保存する

---

## ステップガイド

<details>
<summary>ステップ1：SSHで接続する</summary>

基本的な接続コマンドです。

```bash
# 基本形式
$ ssh ユーザー名@ホスト名またはIPアドレス

# 例：user というユーザーで 192.168.1.100 に接続
$ ssh user@192.168.1.100

# ポート番号を指定する場合（デフォルトは22番）
$ ssh -p 2222 user@192.168.1.100
```

初回接続時にはホスト鍵の確認メッセージが表示されます。

```
The authenticity of host '192.168.1.100 (192.168.1.100)' can't be established.
ED25519 key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
```

`yes` と入力すると接続が続行されます。

</details>

<details>
<summary>ステップ2：システム情報を取得する</summary>

接続後、以下のコマンドを順番に実行しましょう。

```bash
# ホスト名を確認
$ hostname

# OS・カーネル情報を表示
$ uname -a

# 稼働時間と負荷を確認
$ uptime

# ディスク使用量を人間が読みやすい形式で表示
$ df -h

# メモリ使用量を確認
$ free -h
```

</details>

<details>
<summary>ステップ3：リモートコマンド実行を試す</summary>

SSHでは接続せずにリモートでコマンドを実行する方法があります。

```bash
# 書式：ssh ユーザー名@ホスト コマンド
$ ssh user@192.168.1.100 hostname

# 複数コマンドを実行する場合はクォートで囲む
$ ssh user@192.168.1.100 "hostname; uname -a; uptime"
```

この方法はコマンド実行後に自動的に切断されます。

</details>

<details>
<summary>ステップ4：結果をファイルに保存する</summary>

リモートコマンドの出力をリダイレクトでファイルに保存できます。

```bash
# 結果をローカルファイルに保存
$ ssh user@192.168.1.100 "hostname; uname -a; uptime; df -h; free -h" > server_info.txt

# 保存した内容を確認
$ cat server_info.txt
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）─ 手動で1つずつ実行</summary>

```bash
#!/bin/bash
# SSH基本操作の練習スクリプト
# 学べる内容：SSH接続、リモートコマンド実行、出力のリダイレクト
# 実行方法：bash ssh_basic_practice.sh

# === 設定 ===
SERVER="user@192.168.1.100"

echo "===== SSH基本操作の練習 ====="

# 1. リモートコマンド実行でシステム情報を1つずつ取得
echo ""
echo "--- ホスト名 ---"
ssh "$SERVER" "hostname"

echo ""
echo "--- OS情報 ---"
ssh "$SERVER" "uname -a"

echo ""
echo "--- 稼働時間 ---"
ssh "$SERVER" "uptime"

echo ""
echo "--- ディスク使用量 ---"
ssh "$SERVER" "df -h"

echo ""
echo "--- メモリ使用量 ---"
ssh "$SERVER" "free -h"

echo ""
echo "===== 完了 ====="
```

</details>

<details>
<summary>解答例（改良版）─ 1回の接続で効率的に取得</summary>

```bash
#!/bin/bash
# SSH基本操作の練習スクリプト（改良版）
# 学べる内容：SSH接続の効率化、ヒアドキュメント、日時付きファイル保存
# 実行方法：bash ssh_basic_practice_v2.sh

# === 設定 ===
SERVER="user@192.168.1.100"
OUTPUT_FILE="server_info_$(date +%Y%m%d_%H%M%S).txt"

echo "===== サーバー情報取得ツール ====="
echo "対象サーバー: $SERVER"
echo "保存先ファイル: $OUTPUT_FILE"
echo ""

# 1回のSSH接続で全情報を取得（効率的）
ssh "$SERVER" << 'REMOTE_COMMANDS' > "$OUTPUT_FILE"
echo "=============================="
echo " サーバー情報レポート"
echo " 取得日時: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=============================="
echo ""
echo "[ホスト名]"
hostname
echo ""
echo "[OS情報]"
uname -a
echo ""
echo "[稼働時間]"
uptime
echo ""
echo "[ディスク使用量]"
df -h
echo ""
echo "[メモリ使用量]"
free -h
echo ""
echo "[ログインユーザー]"
who
echo ""
echo "[直近のログイン履歴]"
last -5
REMOTE_COMMANDS

# 結果を表示
if [ $? -eq 0 ]; then
    echo "取得成功！"
    echo ""
    cat "$OUTPUT_FILE"
else
    echo "エラー: サーバーへの接続に失敗しました。"
    exit 1
fi
```

**初心者向けとの違い:**
- ヒアドキュメント（`<< 'REMOTE_COMMANDS'`）で1回の接続にまとめている → SSH接続のオーバーヘッドを削減
- 日時付きファイル名で保存 → 過去の記録と区別できる
- エラーハンドリング（`$?` の確認）を追加 → 失敗時に原因がわかりやすい
- `who` や `last` など追加情報も取得 → より実用的なレポート

</details>

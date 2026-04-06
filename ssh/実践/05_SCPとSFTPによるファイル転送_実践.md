# 実践課題05：SCPとSFTPによるファイル転送 ★2

> **難易度**: ★★☆☆☆（基礎）
> **前提知識**: 第2章（SSHクライアントの基本操作）、第5章（ファイル転送）
> **課題の種類**: ミニプロジェクト
> **学習目標**: SCP・SFTP・rsyncの3つのファイル転送方法を実際に使い分け、用途に応じた最適な方法を選択できるようになる

---

## 完成イメージ

```
# SCP でファイルをアップロード
$ scp report.txt user@server:/home/user/documents/
report.txt                  100%  1234     1.2KB/s   00:00

# SFTP で対話的にファイルを操作
$ sftp user@server
sftp> ls /home/user/documents/
report.txt
sftp> get report.txt report_downloaded.txt
sftp> bye

# rsync で差分同期
$ rsync -avz ./project/ user@server:/home/user/project/
sending incremental file list
src/main.py
src/utils.py
sent 1,234 bytes  received 89 bytes  2,646.00 bytes/sec
```

---

## 課題の要件

1. テスト用のファイルとディレクトリを作成する
2. SCP で単一ファイルとディレクトリをアップロード・ダウンロードする
3. SFTP で対話的にファイルを操作する
4. rsync で差分同期を行い、効率の違いを確認する
5. 各方法の転送時間を比較する

---

## ステップガイド

<details>
<summary>ステップ1：テスト用ファイルを作成する</summary>

```bash
# テスト用ディレクトリを作成
$ mkdir -p ~/ssh_transfer_test/project/{src,docs,data}

# テスト用ファイルを作成
$ echo "Hello from local machine" > ~/ssh_transfer_test/hello.txt
$ echo "print('Hello, World!')" > ~/ssh_transfer_test/project/src/main.py
$ echo "# README" > ~/ssh_transfer_test/project/docs/README.md

# 少し大きめのテストファイルを作成（1MB）
$ dd if=/dev/urandom of=~/ssh_transfer_test/project/data/testdata.bin bs=1024 count=1024 2>/dev/null

# 確認
$ find ~/ssh_transfer_test -type f
```

</details>

<details>
<summary>ステップ2：SCPでファイルを転送する</summary>

```bash
# --- アップロード ---

# 単一ファイルのアップロード
$ scp ~/ssh_transfer_test/hello.txt user@server:/tmp/

# ディレクトリごとアップロード（-r オプション）
$ scp -r ~/ssh_transfer_test/project user@server:/tmp/

# --- ダウンロード ---

# 単一ファイルのダウンロード
$ scp user@server:/tmp/hello.txt ~/ssh_transfer_test/downloaded_hello.txt

# ディレクトリごとダウンロード
$ scp -r user@server:/tmp/project ~/ssh_transfer_test/downloaded_project
```

</details>

<details>
<summary>ステップ3：SFTPで対話的に操作する</summary>

```bash
$ sftp user@server
sftp> pwd                       # リモートの現在ディレクトリ
sftp> lpwd                      # ローカルの現在ディレクトリ
sftp> ls /tmp/                  # リモートのファイル一覧
sftp> lls ~/ssh_transfer_test/  # ローカルのファイル一覧
sftp> put ~/ssh_transfer_test/hello.txt /tmp/sftp_hello.txt   # アップロード
sftp> get /tmp/sftp_hello.txt ~/ssh_transfer_test/sftp_got.txt # ダウンロード
sftp> mkdir /tmp/sftp_test      # リモートにディレクトリ作成
sftp> bye                       # 切断
```

</details>

<details>
<summary>ステップ4：rsyncで差分同期する</summary>

```bash
# 初回同期（全ファイル転送）
$ rsync -avz ~/ssh_transfer_test/project/ user@server:/tmp/rsync_project/

# ファイルを1つ変更
$ echo "updated content" >> ~/ssh_transfer_test/project/src/main.py

# 2回目の同期（変更されたファイルのみ転送 ─ 高速）
$ rsync -avz ~/ssh_transfer_test/project/ user@server:/tmp/rsync_project/
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）─ 3つの方法を順番に実行</summary>

```bash
#!/bin/bash
# ファイル転送練習スクリプト
# 学べる内容：SCP、SFTP、rsync の基本操作
# 実行方法：bash file_transfer_practice.sh <ユーザー名> <サーバー>

USER="$1"
SERVER="$2"
REMOTE="${USER}@${SERVER}"
LOCAL_DIR="$HOME/ssh_transfer_test"
REMOTE_DIR="/tmp/ssh_transfer_test_$$"

if [ -z "$USER" ] || [ -z "$SERVER" ]; then
    echo "使い方: $0 <ユーザー名> <サーバー>"
    exit 1
fi

echo "===== ファイル転送練習 ====="

# --- 準備 ---
echo ""
echo "--- テストファイルの準備 ---"
mkdir -p "$LOCAL_DIR/project"/{src,docs,data}
echo "Hello from local machine - $(date)" > "$LOCAL_DIR/hello.txt"
echo "print('Hello, World!')" > "$LOCAL_DIR/project/src/main.py"
echo "# Project README" > "$LOCAL_DIR/project/docs/README.md"
dd if=/dev/urandom of="$LOCAL_DIR/project/data/testdata.bin" bs=1024 count=512 2>/dev/null
echo "テストファイルを作成しました。"
ls -lR "$LOCAL_DIR"

# --- SCP ---
echo ""
echo "--- SCP でファイル転送 ---"
echo "[アップロード] 単一ファイル"
scp "$LOCAL_DIR/hello.txt" "$REMOTE:$REMOTE_DIR/"

echo "[アップロード] ディレクトリ"
scp -r "$LOCAL_DIR/project" "$REMOTE:$REMOTE_DIR/"

echo "[ダウンロード] 単一ファイル"
scp "$REMOTE:$REMOTE_DIR/hello.txt" "$LOCAL_DIR/scp_downloaded.txt"

echo "SCP 転送完了"

# --- SFTP（バッチモード） ---
echo ""
echo "--- SFTP でファイル転送（バッチモード） ---"
sftp "$REMOTE" << EOF
ls $REMOTE_DIR/
get $REMOTE_DIR/hello.txt $LOCAL_DIR/sftp_downloaded.txt
bye
EOF
echo "SFTP 転送完了"

# --- rsync ---
echo ""
echo "--- rsync で差分同期 ---"
echo "[初回同期]"
rsync -avz "$LOCAL_DIR/project/" "$REMOTE:$REMOTE_DIR/rsync_project/"

echo ""
echo "[ファイル変更後の再同期]"
echo "# Updated: $(date)" >> "$LOCAL_DIR/project/src/main.py"
rsync -avz "$LOCAL_DIR/project/" "$REMOTE:$REMOTE_DIR/rsync_project/"
echo "rsync 同期完了（2回目は変更ファイルのみ転送されたことを確認）"

# --- クリーンアップ ---
echo ""
echo "--- リモートのテストファイルを削除 ---"
ssh "$REMOTE" "rm -rf $REMOTE_DIR"
echo "クリーンアップ完了"

echo ""
echo "===== 完了 ====="
```

</details>

<details>
<summary>解答例（改良版）─ 転送時間の計測と比較レポート付き</summary>

```bash
#!/bin/bash
# ファイル転送ベンチマーク＆練習ツール（改良版）
# 学べる内容：転送方法の比較、time計測、バッチ処理
# 実行方法：bash file_transfer_benchmark.sh <ユーザー名> <サーバー>

set -euo pipefail

USER="${1:-}"
SERVER="${2:-}"

if [ -z "$USER" ] || [ -z "$SERVER" ]; then
    echo "使い方: $0 <ユーザー名> <サーバー>"
    exit 1
fi

REMOTE="${USER}@${SERVER}"
LOCAL_DIR="$HOME/ssh_transfer_benchmark"
REMOTE_DIR="/tmp/ssh_transfer_benchmark_$$"
REPORT_FILE="$LOCAL_DIR/benchmark_report.txt"

# === ユーティリティ関数 ===

measure_time() {
    local label="$1"
    shift
    local start end elapsed
    start=$(date +%s%N)
    "$@"
    end=$(date +%s%N)
    elapsed=$(( (end - start) / 1000000 ))  # ミリ秒
    echo "$label: ${elapsed}ms" >> "$REPORT_FILE"
    echo "  $label: ${elapsed}ms"
}

create_test_files() {
    local dir="$1"
    local size_kb="$2"
    local file_count="$3"

    mkdir -p "$dir"
    for i in $(seq 1 "$file_count"); do
        dd if=/dev/urandom of="$dir/file_${i}.bin" bs=1024 count="$size_kb" 2>/dev/null
    done
}

# === メイン処理 ===

echo "===== ファイル転送ベンチマーク ====="
echo "対象: $REMOTE"
echo ""

# 準備
rm -rf "$LOCAL_DIR"
mkdir -p "$LOCAL_DIR"
echo "ファイル転送ベンチマーク結果 - $(date)" > "$REPORT_FILE"
echo "対象サーバー: $REMOTE" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"

# リモートディレクトリ作成
ssh "$REMOTE" "mkdir -p $REMOTE_DIR"

# --- テスト1: 小さいファイル（多数）の転送 ---
echo "--- テスト1: 小さいファイル（10KB x 20個）---"
create_test_files "$LOCAL_DIR/small_files" 10 20
echo "テスト1: 小さいファイル（10KB x 20個）" >> "$REPORT_FILE"

measure_time "  SCP" \
    scp -r "$LOCAL_DIR/small_files" "$REMOTE:$REMOTE_DIR/scp_small"

measure_time "  rsync" \
    rsync -az "$LOCAL_DIR/small_files/" "$REMOTE:$REMOTE_DIR/rsync_small/"

echo "" >> "$REPORT_FILE"

# --- テスト2: 大きいファイル（少数）の転送 ---
echo ""
echo "--- テスト2: 大きいファイル（1MB x 3個）---"
create_test_files "$LOCAL_DIR/large_files" 1024 3
echo "テスト2: 大きいファイル（1MB x 3個）" >> "$REPORT_FILE"

measure_time "  SCP" \
    scp -r "$LOCAL_DIR/large_files" "$REMOTE:$REMOTE_DIR/scp_large"

measure_time "  rsync" \
    rsync -az "$LOCAL_DIR/large_files/" "$REMOTE:$REMOTE_DIR/rsync_large/"

echo "" >> "$REPORT_FILE"

# --- テスト3: rsyncの差分転送テスト ---
echo ""
echo "--- テスト3: rsync差分同期（1ファイルだけ変更）---"
echo "テスト3: rsync差分同期" >> "$REPORT_FILE"

# 1ファイルだけ変更
echo "modified" >> "$LOCAL_DIR/large_files/file_1.bin"

measure_time "  rsync（差分のみ）" \
    rsync -az "$LOCAL_DIR/large_files/" "$REMOTE:$REMOTE_DIR/rsync_large/"

measure_time "  SCP（全ファイル再転送）" \
    scp -r "$LOCAL_DIR/large_files" "$REMOTE:$REMOTE_DIR/scp_large_redo"

echo "" >> "$REPORT_FILE"

# --- レポート表示 ---
echo ""
echo "===== ベンチマーク結果 ====="
cat "$REPORT_FILE"

echo ""
echo "結論:"
echo "  - 大量の小さいファイル → rsync が有利（接続の再利用）"
echo "  - 差分同期 → rsync が圧倒的に高速（変更分のみ転送）"
echo "  - 単発の転送 → SCP でも十分（シンプルで覚えやすい）"

# クリーンアップ
ssh "$REMOTE" "rm -rf $REMOTE_DIR"
echo ""
echo "リモートのテストファイルを削除しました。"
echo "ローカルのテストファイル: $LOCAL_DIR"
echo ""
echo "===== 完了 ====="
```

**初心者向けとの違い:**
- 転送時間を計測して比較レポートを生成 → 方法ごとの性能差を数値で理解
- rsyncの差分転送の威力を数値で確認 → 実務での使い分け判断に役立つ
- テストデータの自動生成 → 再現性のあるベンチマーク
- 関数化による構造の整理 → テストパターンの追加が容易

</details>

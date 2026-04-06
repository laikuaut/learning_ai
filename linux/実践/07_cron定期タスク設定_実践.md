# 実践課題07：cron定期タスク設定 ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第4章（プロセス管理）、第5章（シェルスクリプト基礎）、第8章（システム管理）
> **課題の種類**: ミニプロジェクト
> **学習目標**: cronを使ったタスクスケジューリングを理解し、定期バックアップやログローテーションを設定できるようになる

---

## 完成イメージ

以下の3つの定期タスクを設定し、自動化されたシステム管理を実現します。

```
【設定するcronジョブ】

1. 毎日 2:00  ─ ディレクトリのバックアップ
   → /tmp/backup/ に日付付きアーカイブを作成
   → 7日以上古いバックアップを自動削除

2. 毎時 0分  ─ ディスク使用量チェック
   → 使用率が80%を超えたらアラートファイルに記録

3. 毎週月曜 3:00 ─ ログファイルのクリーンアップ
   → 30日以上古いログファイルを削除

【cronジョブの設定例】
$ crontab -l
# 毎日 2:00 バックアップ
0 2 * * * /home/tanaka/scripts/backup.sh >> /home/tanaka/logs/backup.log 2>&1
# 毎時 ディスクチェック
0 * * * * /home/tanaka/scripts/disk_check.sh >> /home/tanaka/logs/disk.log 2>&1
# 毎週月曜 3:00 ログクリーンアップ
0 3 * * 1 /home/tanaka/scripts/log_cleanup.sh >> /home/tanaka/logs/cleanup.log 2>&1
```

---

## 課題の要件

1. バックアップスクリプトを作成する（tar でアーカイブ、古いファイルの削除）
2. ディスク使用量チェックスクリプトを作成する
3. ログクリーンアップスクリプトを作成する
4. crontab の書式を理解し、設定する
5. 各スクリプトが正しく動作することを手動で確認する

---

## ステップガイド

<details>
<summary>ステップ1：crontab の書式を理解する</summary>

crontab（cron table）の各フィールドの意味を確認します。

```
分  時  日  月  曜日  コマンド
┌── 分 (0-59)
│ ┌── 時 (0-23)
│ │ ┌── 日 (1-31)
│ │ │ ┌── 月 (1-12)
│ │ │ │ ┌── 曜日 (0-7, 0と7は日曜)
│ │ │ │ │
* * * * * コマンド
```

よく使われるパターン：

| 設定 | 意味 |
|------|------|
| `0 2 * * *` | 毎日 2:00 |
| `*/5 * * * *` | 5分ごと |
| `0 * * * *` | 毎時 0分 |
| `0 0 * * 0` | 毎週日曜 0:00 |
| `0 3 * * 1` | 毎週月曜 3:00 |
| `0 0 1 * *` | 毎月1日 0:00 |
| `30 4 1,15 * *` | 毎月1日と15日の 4:30 |

```bash
# 現在のcrontabを確認
$ crontab -l

# crontabを編集
$ crontab -e

# crontabをファイルから設定
$ crontab mycron.txt
```

</details>

<details>
<summary>ステップ2：バックアップスクリプトの骨組みを作る</summary>

```bash
#!/bin/bash
# バックアップスクリプトの基本構造

# バックアップ対象と保存先
SOURCE="/home/tanaka/documents"
BACKUP_DIR="/tmp/backup"
DATE=$(date '+%Y%m%d_%H%M%S')

# バックアップ先ディレクトリを作成
mkdir -p "$BACKUP_DIR"

# tar でアーカイブを作成
tar -czf "${BACKUP_DIR}/backup_${DATE}.tar.gz" "$SOURCE"

# 7日以上古いバックアップを削除
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete
```

</details>

<details>
<summary>ステップ3：ディスクチェックスクリプトの骨組みを作る</summary>

```bash
#!/bin/bash
# ディスク使用量チェック

THRESHOLD=80  # 使用率の閾値(%)

# df コマンドでディスク使用率を取得
df -h | awk 'NR>1 {print $5, $6}' | while read -r usage mount; do
    # % を除去して数値にする
    usage_num=${usage%\%}
    if [ "$usage_num" -ge "$THRESHOLD" ]; then
        echo "[警告] ${mount} の使用率が ${usage} です (閾値: ${THRESHOLD}%)"
    fi
done
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

3つのスクリプトと、crontab設定ファイルを作成します。

**backup.sh:**

```bash
#!/bin/bash
# 日次バックアップスクリプト
# 学べる内容：tar, find, date, cron
# 実行方法：bash backup.sh

# --- 設定 ---
SOURCE="/home/tanaka/documents"
BACKUP_DIR="/tmp/backup"
RETENTION_DAYS=7
DATE=$(date '+%Y%m%d_%H%M%S')
ARCHIVE_NAME="backup_${DATE}.tar.gz"

echo "[$(date)] バックアップ開始"

# バックアップ先ディレクトリを作成
mkdir -p "$BACKUP_DIR"

# バックアップ対象が存在するか確認
if [ ! -d "$SOURCE" ]; then
    echo "[エラー] バックアップ対象が見つかりません: $SOURCE"
    exit 1
fi

# tar で圧縮アーカイブを作成
tar -czf "${BACKUP_DIR}/${ARCHIVE_NAME}" -C "$(dirname "$SOURCE")" "$(basename "$SOURCE")"
echo "[完了] アーカイブ作成: ${ARCHIVE_NAME}"

# ファイルサイズを確認
ls -lh "${BACKUP_DIR}/${ARCHIVE_NAME}"

# 古いバックアップを削除
deleted=$(find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +${RETENTION_DAYS} -print -delete)
if [ -n "$deleted" ]; then
    echo "[削除] 古いバックアップ:"
    echo "$deleted"
else
    echo "[情報] 削除対象の古いバックアップはありません"
fi

echo "[$(date)] バックアップ完了"
```

**disk_check.sh:**

```bash
#!/bin/bash
# ディスク使用量チェックスクリプト
# 学べる内容：df, awk, 条件分岐
# 実行方法：bash disk_check.sh

THRESHOLD=80
ALERT_FILE="/tmp/disk_alerts.log"

echo "[$(date)] ディスクチェック開始"

has_alert=false

df -h | awk 'NR>1 {print $5, $6, $2, $3, $4}' | while read -r usage mount total used avail; do
    # % を除去
    usage_num=${usage%\%}

    # 数値でない場合はスキップ
    if ! [ "$usage_num" -eq "$usage_num" ] 2>/dev/null; then
        continue
    fi

    if [ "$usage_num" -ge "$THRESHOLD" ]; then
        alert_msg="[警告] $(date '+%Y-%m-%d %H:%M:%S') ${mount} 使用率:${usage} (全体:${total} 使用:${used} 空き:${avail})"
        echo "$alert_msg"
        echo "$alert_msg" >> "$ALERT_FILE"
        has_alert=true
    fi
done

if [ "$has_alert" = false ]; then
    echo "[正常] すべてのディスクが閾値(${THRESHOLD}%)以下です"
fi

echo "[$(date)] ディスクチェック完了"
```

**log_cleanup.sh:**

```bash
#!/bin/bash
# ログクリーンアップスクリプト
# 学べる内容：find, ログ管理
# 実行方法：bash log_cleanup.sh

LOG_DIR="/var/log"
RETENTION_DAYS=30

echo "[$(date)] ログクリーンアップ開始"

# 古いログファイルを検索
echo "--- ${RETENTION_DAYS}日以上古いログファイル ---"
old_logs=$(find "$LOG_DIR" -name "*.log" -mtime +${RETENTION_DAYS} 2>/dev/null)

if [ -n "$old_logs" ]; then
    echo "$old_logs" | while read -r logfile; do
        size=$(du -h "$logfile" | cut -f1)
        echo "  削除: $logfile ($size)"
    done

    # 実際に削除（安全のためコメントアウト、確認後に有効化）
    # find "$LOG_DIR" -name "*.log" -mtime +${RETENTION_DAYS} -delete

    echo "[注意] 安全のため実際の削除はコメントアウトされています"
    echo "確認後、スクリプト内の delete 行を有効化してください"
else
    echo "  削除対象のファイルはありません"
fi

echo "[$(date)] ログクリーンアップ完了"
```

**crontab設定ファイル (mycron.txt):**

```bash
# cron定期タスク設定
# 設定方法: crontab mycron.txt
# 確認方法: crontab -l

# 環境変数
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
HOME=/home/tanaka

# 毎日 2:00 バックアップ
0 2 * * * /home/tanaka/scripts/backup.sh >> /home/tanaka/logs/backup.log 2>&1

# 毎時 0分 ディスクチェック
0 * * * * /home/tanaka/scripts/disk_check.sh >> /home/tanaka/logs/disk.log 2>&1

# 毎週月曜 3:00 ログクリーンアップ
0 3 * * 1 /home/tanaka/scripts/log_cleanup.sh >> /home/tanaka/logs/cleanup.log 2>&1
```

</details>

<details>
<summary>解答例（改良版 ─ ローテーション・通知・ロック機能付き）</summary>

**backup_v2.sh:**

```bash
#!/bin/bash
# 日次バックアップスクリプト（改良版）
# 学べる内容：flock, ローテーション、世代管理、差分バックアップ
# 実行方法：bash backup_v2.sh [full|diff]

set -euo pipefail

# --- 設定 ---
SOURCE="/home/tanaka/documents"
BACKUP_DIR="/tmp/backup"
LOCK_FILE="/tmp/backup.lock"
RETENTION_DAYS=7
MAX_BACKUPS=10
MODE="${1:-full}"
DATE=$(date '+%Y%m%d_%H%M%S')

# ログ出力関数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# --- 排他ロック（同時実行防止） ---
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
    log "エラー: 別のバックアッププロセスが実行中です"
    exit 1
fi

log "バックアップ開始（モード: $MODE）"

mkdir -p "$BACKUP_DIR"

if [ ! -d "$SOURCE" ]; then
    log "エラー: バックアップ対象が見つかりません: $SOURCE"
    exit 1
fi

# --- バックアップ実行 ---
if [ "$MODE" = "diff" ]; then
    # 差分バックアップ：前回のフルバックアップ以降に変更されたファイルのみ
    LATEST_FULL=$(ls -t "$BACKUP_DIR"/full_*.tar.gz 2>/dev/null | head -1)
    if [ -n "$LATEST_FULL" ]; then
        ARCHIVE="${BACKUP_DIR}/diff_${DATE}.tar.gz"
        tar -czf "$ARCHIVE" --newer-mtime="$LATEST_FULL" -C "$(dirname "$SOURCE")" "$(basename "$SOURCE")" 2>/dev/null || true
        log "差分バックアップ作成: $(basename "$ARCHIVE")"
    else
        log "フルバックアップが見つからないため、フルバックアップを実行します"
        MODE="full"
    fi
fi

if [ "$MODE" = "full" ]; then
    ARCHIVE="${BACKUP_DIR}/full_${DATE}.tar.gz"
    tar -czf "$ARCHIVE" -C "$(dirname "$SOURCE")" "$(basename "$SOURCE")"
    log "フルバックアップ作成: $(basename "$ARCHIVE")"
fi

# ファイルサイズ
ARCHIVE_SIZE=$(du -h "$ARCHIVE" | cut -f1)
log "アーカイブサイズ: $ARCHIVE_SIZE"

# --- チェックサム生成 ---
sha256sum "$ARCHIVE" > "${ARCHIVE}.sha256"
log "チェックサム生成: $(basename "${ARCHIVE}.sha256")"

# --- 古いバックアップの削除（日数ベース） ---
deleted_count=0
while IFS= read -r old_file; do
    rm -f "$old_file" "${old_file}.sha256"
    log "古いファイル削除: $(basename "$old_file")"
    ((deleted_count++))
done < <(find "$BACKUP_DIR" -name "*.tar.gz" -mtime +${RETENTION_DAYS} 2>/dev/null)

# --- 世代数ベースの削除 ---
current_count=$(ls "$BACKUP_DIR"/*.tar.gz 2>/dev/null | wc -l)
if [ "$current_count" -gt "$MAX_BACKUPS" ]; then
    over=$((current_count - MAX_BACKUPS))
    ls -t "$BACKUP_DIR"/*.tar.gz | tail -"$over" | while read -r old_file; do
        rm -f "$old_file" "${old_file}.sha256"
        log "世代超過で削除: $(basename "$old_file")"
        ((deleted_count++))
    done
fi

# --- レポート ---
log "バックアップ完了"
log "  保存先: $BACKUP_DIR"
log "  アーカイブ数: $(ls "$BACKUP_DIR"/*.tar.gz 2>/dev/null | wc -l)"
log "  削除数: $deleted_count"
log "  合計サイズ: $(du -sh "$BACKUP_DIR" | cut -f1)"

# ロック解放
flock -u 9
```

**初心者向けとの違い:**
- `flock` による排他ロック → cronで前回のジョブが終わっていない場合に二重実行を防止
- フルバックアップと差分バックアップ（differential backup）の切り替え
- チェックサム（SHA-256）でデータ整合性を検証可能
- 日数ベース + 世代数ベースの二重の保持ポリシー
- `set -euo pipefail` でエラーを厳密にハンドリング

</details>

#!/bin/bash
# ============================================================================
# 04_バックアップスクリプト.sh
# ============================================================================
# 学べる内容:
#   - tar コマンドによるアーカイブ・圧縮の方法
#   - 日付を使ったファイル名の生成
#   - 古いバックアップの自動削除（世代管理）
#   - ログファイルへの記録
#   - set -euo pipefail によるエラーハンドリング
#   - trap によるエラー時の処理
#   - du, df コマンドによるディスク容量の確認
#
# 実行方法:
#   1. chmod +x 04_バックアップスクリプト.sh
#   2. ./04_バックアップスクリプト.sh <バックアップ元ディレクトリ> [バックアップ先ディレクトリ]
#      例: ./04_バックアップスクリプト.sh /var/www/html /backup
#      ※ バックアップ先を省略すると ./backups/ が使われます
#
# 動作説明:
#   指定ディレクトリを tar.gz 形式で圧縮バックアップします。
#   日付付きのファイル名で保存し、古いバックアップは自動的に削除します。
# ============================================================================

set -euo pipefail

# --- 設定 ---
MAX_BACKUPS=7          # 保持するバックアップの世代数
LOG_FILE=""            # ログファイル（後で設定）
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# --- ログ関数 ---
log() {
    local level="$1"
    shift
    local message="$*"
    local log_line="[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message"

    # 画面に表示
    echo "$log_line"

    # ログファイルにも記録（設定されている場合）
    if [ -n "$LOG_FILE" ]; then
        echo "$log_line" >> "$LOG_FILE"
    fi
}

log_info()  { log "INFO"  "$@"; }
log_warn()  { log "WARN"  "$@"; }
log_error() { log "ERROR" "$@"; }

# --- エラー時の処理 ---
cleanup_on_error() {
    log_error "エラーが発生しました。処理を中断します。"

    # 作成途中のバックアップファイルがあれば削除
    if [ -n "${BACKUP_FILE:-}" ] && [ -f "$BACKUP_FILE" ]; then
        log_warn "不完全なバックアップファイルを削除: $BACKUP_FILE"
        rm -f "$BACKUP_FILE"
    fi

    exit 1
}

# trap でエラー時の処理を登録
trap cleanup_on_error ERR

# --- 関数 ---

# 使い方の表示
usage() {
    echo "使い方: $0 <バックアップ元> [バックアップ先]"
    echo ""
    echo "  バックアップ元: バックアップ対象のディレクトリ"
    echo "  バックアップ先: バックアップファイルの保存先（省略時: ./backups/）"
    echo ""
    echo "例:"
    echo "  $0 /var/www/html /backup"
    echo "  $0 ~/projects"
}

# ディスク容量のチェック
check_disk_space() {
    local source_dir="$1"
    local dest_dir="$2"

    # バックアップ元のサイズを取得（KB単位）
    local source_size_kb
    source_size_kb=$(du -sk "$source_dir" | awk '{print $1}')

    # バックアップ先の空き容量を取得（KB単位）
    local available_kb
    available_kb=$(df -k "$dest_dir" | awk 'NR==2 {print $4}')

    # 圧縮後はおよそ半分のサイズと仮定して、余裕を持って2倍のチェック
    if [ "$source_size_kb" -gt "$available_kb" ]; then
        log_error "ディスク容量が不足しています"
        log_error "  バックアップ元サイズ: $((source_size_kb / 1024)) MB"
        log_error "  バックアップ先空き: $((available_kb / 1024)) MB"
        return 1
    fi

    log_info "ディスク容量: 十分な空きがあります ($((available_kb / 1024)) MB 利用可能)"
    return 0
}

# 古いバックアップの削除
cleanup_old_backups() {
    local backup_dir="$1"
    local prefix="$2"

    local backup_count
    backup_count=$(ls -1 "${backup_dir}/${prefix}"_*.tar.gz 2>/dev/null | wc -l)

    if [ "$backup_count" -gt "$MAX_BACKUPS" ]; then
        local delete_count=$((backup_count - MAX_BACKUPS))
        log_info "古いバックアップを削除します ($delete_count 個)"

        ls -1t "${backup_dir}/${prefix}"_*.tar.gz | tail -n "$delete_count" | while read -r old_file; do
            log_info "  削除: $(basename "$old_file")"
            rm -f "$old_file"
        done
    else
        log_info "バックアップ数: $backup_count / $MAX_BACKUPS (削除不要)"
    fi
}

# --- メイン処理 ---
main() {
    # 引数チェック
    if [ $# -lt 1 ]; then
        usage
        exit 1
    fi

    local source_dir="$1"
    local dest_dir="${2:-./backups}"

    # バックアップ元の存在確認
    if [ ! -d "$source_dir" ]; then
        log_error "バックアップ元が見つかりません: $source_dir"
        exit 1
    fi

    # バックアップ先ディレクトリの作成
    if [ ! -d "$dest_dir" ]; then
        mkdir -p "$dest_dir"
        log_info "バックアップ先ディレクトリを作成しました: $dest_dir"
    fi

    # ログファイルの設定
    LOG_FILE="${dest_dir}/backup.log"

    # バックアップファイル名の生成
    local source_basename
    source_basename=$(basename "$source_dir")
    BACKUP_FILE="${dest_dir}/${source_basename}_${TIMESTAMP}.tar.gz"

    # 処理開始
    echo "============================================"
    echo "  バックアップスクリプト"
    echo "============================================"
    log_info "バックアップを開始します"
    log_info "  バックアップ元: $source_dir"
    log_info "  バックアップ先: $BACKUP_FILE"
    log_info "  最大保持世代数: $MAX_BACKUPS"

    # ディスク容量チェック
    check_disk_space "$source_dir" "$dest_dir"

    # バックアップ元のサイズを表示
    local source_size
    source_size=$(du -sh "$source_dir" | awk '{print $1}')
    log_info "バックアップ元サイズ: $source_size"

    # バックアップの実行
    log_info "圧縮・アーカイブ中..."
    local start_time
    start_time=$(date +%s)

    tar czf "$BACKUP_FILE" -C "$(dirname "$source_dir")" "$(basename "$source_dir")"

    local end_time
    end_time=$(date +%s)
    local elapsed=$((end_time - start_time))

    # 結果の確認
    if [ -f "$BACKUP_FILE" ]; then
        local backup_size
        backup_size=$(du -sh "$BACKUP_FILE" | awk '{print $1}')
        log_info "バックアップ完了!"
        log_info "  ファイル: $(basename "$BACKUP_FILE")"
        log_info "  サイズ: $backup_size"
        log_info "  所要時間: ${elapsed}秒"
    else
        log_error "バックアップファイルの作成に失敗しました"
        exit 1
    fi

    # 古いバックアップの削除
    cleanup_old_backups "$dest_dir" "$source_basename"

    # 最終結果
    echo ""
    log_info "============================================"
    log_info "  バックアップ完了サマリー"
    log_info "============================================"
    log_info "ファイル一覧:"
    ls -lh "${dest_dir}/${source_basename}"_*.tar.gz 2>/dev/null | awk '{print "  " $5 "  " $9}'

    echo ""
    log_info "ログファイル: $LOG_FILE"
}

main "$@"

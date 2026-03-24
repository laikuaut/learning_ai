#!/bin/bash
# ============================================================================
# 01_ファイル整理スクリプト.sh
# ============================================================================
# 学べる内容:
#   - 条件分岐（if文）とループ（for文）の実践的な使い方
#   - ファイル操作コマンド（mkdir, mv）の活用
#   - 変数展開とパラメータ展開（拡張子の取得）
#   - ログ出力関数の作り方
#   - スクリプトの引数処理
#
# 実行方法:
#   1. chmod +x 01_ファイル整理スクリプト.sh
#   2. 整理したいファイルがあるディレクトリで実行:
#      ./01_ファイル整理スクリプト.sh [対象ディレクトリ]
#      ※ 引数を省略するとカレントディレクトリが対象になります
#
# 動作説明:
#   指定したディレクトリ内のファイルを拡張子ごとにフォルダに分類して移動します。
#   例: photo.jpg → images/photo.jpg
#       report.pdf → documents/report.pdf
# ============================================================================

set -euo pipefail

# --- 設定 ---
# 拡張子とフォルダ名の対応を定義
declare -A CATEGORY_MAP
CATEGORY_MAP=(
    ["jpg"]="images"
    ["jpeg"]="images"
    ["png"]="images"
    ["gif"]="images"
    ["svg"]="images"
    ["pdf"]="documents"
    ["doc"]="documents"
    ["docx"]="documents"
    ["xls"]="documents"
    ["xlsx"]="documents"
    ["txt"]="text"
    ["md"]="text"
    ["csv"]="text"
    ["mp4"]="videos"
    ["avi"]="videos"
    ["mov"]="videos"
    ["mp3"]="audio"
    ["wav"]="audio"
    ["flac"]="audio"
    ["zip"]="archives"
    ["tar"]="archives"
    ["gz"]="archives"
    ["sh"]="scripts"
    ["py"]="scripts"
    ["js"]="scripts"
)

# --- ログ関数 ---
log_info() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1"
}

log_warn() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WARN] $1"
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" >&2
}

# --- メイン処理 ---
main() {
    # 対象ディレクトリの決定（引数があればそれを使用、なければカレントディレクトリ）
    local target_dir="${1:-.}"

    # ディレクトリの存在確認
    if [ ! -d "$target_dir" ]; then
        log_error "ディレクトリが見つかりません: $target_dir"
        exit 1
    fi

    log_info "ファイル整理を開始します"
    log_info "対象ディレクトリ: $(cd "$target_dir" && pwd)"

    local moved_count=0
    local skipped_count=0

    # 対象ディレクトリ内のファイルを処理
    for file in "$target_dir"/*; do
        # ファイルでなければスキップ（ディレクトリ等）
        if [ ! -f "$file" ]; then
            continue
        fi

        # ファイル名と拡張子を取得
        local filename
        filename=$(basename "$file")
        local extension="${filename##*.}"

        # 拡張子がないファイルはスキップ
        if [ "$extension" = "$filename" ]; then
            log_warn "拡張子なし: $filename (スキップ)"
            skipped_count=$((skipped_count + 1))
            continue
        fi

        # 拡張子を小文字に変換
        extension=$(echo "$extension" | tr 'A-Z' 'a-z')

        # カテゴリの決定
        local category="${CATEGORY_MAP[$extension]:-other}"

        # フォルダの作成（存在しなければ）
        local dest_dir="$target_dir/$category"
        if [ ! -d "$dest_dir" ]; then
            mkdir -p "$dest_dir"
            log_info "フォルダ作成: $category/"
        fi

        # 同名ファイルが存在する場合の処理
        local dest_file="$dest_dir/$filename"
        if [ -f "$dest_file" ]; then
            local base="${filename%.*}"
            local timestamp
            timestamp=$(date +%Y%m%d_%H%M%S)
            dest_file="$dest_dir/${base}_${timestamp}.${extension}"
            log_warn "同名ファイルが存在するためリネーム: $filename → $(basename "$dest_file")"
        fi

        # ファイルを移動
        mv "$file" "$dest_file"
        log_info "移動: $filename → $category/"
        moved_count=$((moved_count + 1))
    done

    # 結果の表示
    echo ""
    log_info "===== 整理結果 ====="
    log_info "移動したファイル: $moved_count 個"
    log_info "スキップしたファイル: $skipped_count 個"

    # 作成されたフォルダの一覧
    echo ""
    log_info "フォルダ構成:"
    for dir in "$target_dir"/*/; do
        if [ -d "$dir" ]; then
            local count
            count=$(find "$dir" -maxdepth 1 -type f | wc -l)
            log_info "  $(basename "$dir")/ ($count ファイル)"
        fi
    done

    log_info "ファイル整理が完了しました"
}

# スクリプト実行
main "$@"

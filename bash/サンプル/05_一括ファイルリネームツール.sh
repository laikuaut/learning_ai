#!/usr/bin/env bash
# ============================================================
# 一括ファイルリネームツール
# ============================================================
# 【学べる内容】
#   - パラメータ展開（${var%...}, ${var#...}, ${var/...}）
#   - for ループによるファイル一括処理
#   - 関数の定義と引数の受け渡し
#   - getopts によるコマンドラインオプション解析
#   - ドライラン（プレビュー）モードの実装
#
# 【実行方法】
#   chmod +x 05_一括ファイルリネームツール.sh
#   ./05_一括ファイルリネームツール.sh                  # 対話型で起動
#   ./05_一括ファイルリネームツール.sh -d /path/to/dir  # ディレクトリ指定
#   ./05_一括ファイルリネームツール.sh -n              # ドライランモード
#   ./05_一括ファイルリネームツール.sh -h              # ヘルプ表示
# ============================================================
set -euo pipefail

# --- 色の定義 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# --- 設定 ---
TARGET_DIR="."
DRY_RUN=false

# ヘルプを表示する
show_help() {
    echo "使い方: $0 [オプション]"
    echo ""
    echo "オプション:"
    echo "  -d <ディレクトリ>  対象ディレクトリを指定（デフォルト: カレント）"
    echo "  -n                 ドライラン（実際にはリネームせずプレビューのみ）"
    echo "  -h                 このヘルプを表示する"
}

# 区切り線を表示する
separator() {
    printf '%55s\n' '' | tr ' ' '-'
}

# 対象ディレクトリのファイル一覧を表示する
show_files() {
    echo ""
    echo -e "${BOLD}${CYAN}対象ディレクトリ:${RESET} ${TARGET_DIR}"
    separator
    local count=0
    for f in "${TARGET_DIR}"/*; do
        if [[ -f "$f" ]]; then
            local name
            name=$(basename "$f")
            printf "  %s\n" "$name"
            ((count++))
        fi
    done
    if [[ $count -eq 0 ]]; then
        echo -e "  ${YELLOW}ファイルが見つかりません。${RESET}"
        return 1
    fi
    separator
    echo -e "  合計: ${count} ファイル"
    return 0
}

# リネームを実行（またはプレビュー）する
execute_rename() {
    local old_path="$1"
    local new_name="$2"
    local dir
    dir=$(dirname "$old_path")
    local old_name
    old_name=$(basename "$old_path")
    local new_path="${dir}/${new_name}"

    if [[ "$old_name" == "$new_name" ]]; then
        return 0
    fi

    if $DRY_RUN; then
        echo -e "  ${YELLOW}[プレビュー]${RESET} ${old_name} -> ${new_name}"
    else
        if [[ -e "$new_path" ]]; then
            echo -e "  ${RED}[スキップ]${RESET} ${new_name} は既に存在します"
            return 0
        fi
        mv "$old_path" "$new_path"
        echo -e "  ${GREEN}[リネーム]${RESET} ${old_name} -> ${new_name}"
    fi
}

# --- 操作1: プレフィックスを追加する ---
add_prefix() {
    echo -ne "  追加するプレフィックスを入力: "
    local prefix
    read -r prefix
    if [[ -z "$prefix" ]]; then
        echo -e "  ${RED}プレフィックスが空です。${RESET}"
        return
    fi

    echo ""
    local count=0
    for f in "${TARGET_DIR}"/*; do
        [[ -f "$f" ]] || continue
        local name
        name=$(basename "$f")
        execute_rename "$f" "${prefix}${name}"
        ((count++))
    done
    echo -e "\n  処理対象: ${count} ファイル"
}

# --- 操作2: サフィックスを追加する ---
add_suffix() {
    echo -ne "  追加するサフィックス（拡張子の前に挿入）を入力: "
    local suffix
    read -r suffix
    if [[ -z "$suffix" ]]; then
        echo -e "  ${RED}サフィックスが空です。${RESET}"
        return
    fi

    echo ""
    local count=0
    for f in "${TARGET_DIR}"/*; do
        [[ -f "$f" ]] || continue
        local name
        name=$(basename "$f")
        # 拡張子がある場合はその手前にサフィックスを追加する
        if [[ "$name" == *.* ]]; then
            local base="${name%.*}"    # 拡張子を除いた部分
            local ext="${name##*.}"    # 拡張子
            execute_rename "$f" "${base}${suffix}.${ext}"
        else
            execute_rename "$f" "${name}${suffix}"
        fi
        ((count++))
    done
    echo -e "\n  処理対象: ${count} ファイル"
}

# --- 操作3: 連番を付与する ---
add_sequential_number() {
    echo -ne "  連番の開始番号を入力（デフォルト: 1）: "
    local start_num
    read -r start_num
    start_num="${start_num:-1}"

    echo -ne "  桁数を入力（デフォルト: 3 -> 001, 002...）: "
    local digits
    read -r digits
    digits="${digits:-3}"

    echo ""
    local num=$start_num
    local count=0
    for f in "${TARGET_DIR}"/*; do
        [[ -f "$f" ]] || continue
        local name
        name=$(basename "$f")
        local formatted_num
        formatted_num=$(printf "%0${digits}d" "$num")
        # 拡張子がある場合は保持する
        if [[ "$name" == *.* ]]; then
            local ext="${name##*.}"
            execute_rename "$f" "${formatted_num}_${name%.*}.${ext}"
        else
            execute_rename "$f" "${formatted_num}_${name}"
        fi
        ((num++))
        ((count++))
    done
    echo -e "\n  処理対象: ${count} ファイル"
}

# --- 操作4: 文字列を置換する ---
replace_string() {
    echo -ne "  検索する文字列を入力: "
    local search
    read -r search
    if [[ -z "$search" ]]; then
        echo -e "  ${RED}検索文字列が空です。${RESET}"
        return
    fi
    echo -ne "  置換後の文字列を入力（空で削除）: "
    local replace
    read -r replace

    echo ""
    local count=0
    local matched=0
    for f in "${TARGET_DIR}"/*; do
        [[ -f "$f" ]] || continue
        local name
        name=$(basename "$f")
        ((count++))
        # パラメータ展開で文字列を置換する
        local new_name="${name//$search/$replace}"
        if [[ "$name" != "$new_name" ]]; then
            execute_rename "$f" "$new_name"
            ((matched++))
        fi
    done
    echo -e "\n  対象: ${count} ファイル / 一致: ${matched} ファイル"
}

# 対話型メニューを表示する
show_menu() {
    echo ""
    echo -e "${BOLD}${CYAN}┌──────────────────────────────────────┐${RESET}"
    echo -e "${BOLD}${CYAN}│     一括ファイルリネームツール       │${RESET}"
    echo -e "${BOLD}${CYAN}├──────────────────────────────────────┤${RESET}"
    echo -e "${BOLD}${CYAN}│${RESET}  1) プレフィックスを追加             ${BOLD}${CYAN}│${RESET}"
    echo -e "${BOLD}${CYAN}│${RESET}  2) サフィックスを追加               ${BOLD}${CYAN}│${RESET}"
    echo -e "${BOLD}${CYAN}│${RESET}  3) 連番を付与                       ${BOLD}${CYAN}│${RESET}"
    echo -e "${BOLD}${CYAN}│${RESET}  4) 文字列を置換                     ${BOLD}${CYAN}│${RESET}"
    echo -e "${BOLD}${CYAN}│${RESET}  5) ファイル一覧を表示               ${BOLD}${CYAN}│${RESET}"
    echo -e "${BOLD}${CYAN}│${RESET}  6) 終了                             ${BOLD}${CYAN}│${RESET}"
    echo -e "${BOLD}${CYAN}└──────────────────────────────────────┘${RESET}"
    if $DRY_RUN; then
        echo -e "  ${YELLOW}[ドライランモード: 実際のリネームは行いません]${RESET}"
    fi
}

# --- オプション解析 ---
while getopts ":d:nh" opt; do
    case "$opt" in
        d)
            TARGET_DIR="$OPTARG"
            if [[ ! -d "$TARGET_DIR" ]]; then
                echo -e "${RED}エラー: ディレクトリが存在しません: ${TARGET_DIR}${RESET}"
                exit 1
            fi
            ;;
        n)
            DRY_RUN=true
            ;;
        h)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}不明なオプション: -${OPTARG}${RESET}"
            show_help
            exit 1
            ;;
    esac
done

# --- メイン処理 ---
echo -e "${BOLD}${CYAN}"
echo "  一括ファイルリネームツール"
echo -e "${RESET}"

# 対話型ループ
while true; do
    show_menu
    echo -ne "\n  選択してください [1-6]: "
    read -r choice
    echo ""

    case "$choice" in
        1) add_prefix ;;
        2) add_suffix ;;
        3) add_sequential_number ;;
        4) replace_string ;;
        5) show_files || true ;;
        6)
            echo -e "${GREEN}終了します。お疲れさまでした！${RESET}"
            exit 0
            ;;
        *)
            echo -e "${RED}無効な選択です。1〜6 の数字を入力してください。${RESET}"
            ;;
    esac
done

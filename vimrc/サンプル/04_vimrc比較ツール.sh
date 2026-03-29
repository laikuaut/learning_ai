#!/bin/bash
# =============================================================================
# 学べる内容：
#   - 推奨されるvimrc設定の一覧と各項目の意味
#   - 自分のvimrcに不足している設定の発見
#   - 2つのvimrcの差分比較の方法
#
# 実行方法：
#   chmod +x 04_vimrc比較ツール.sh
#
#   # 自分のvimrcと推奨設定を比較：
#   ./04_vimrc比較ツール.sh
#   ./04_vimrc比較ツール.sh ~/.vimrc
#
#   # 2つのvimrcファイルを比較：
#   ./04_vimrc比較ツール.sh file1.vimrc file2.vimrc
# =============================================================================

# --- 色付き出力用 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# =============================================================================
# 推奨設定のベースライン（スクリプト内に埋め込み）
# =============================================================================

generate_baseline() {
    cat << 'BASELINE'
" === 基本設定 ===
set nocompatible
filetype plugin indent on
syntax enable
set encoding=utf-8
set fileencoding=utf-8
set backspace=indent,eol,start

" === インデント ===
set expandtab
set tabstop=4
set shiftwidth=4
set softtabstop=4
set autoindent
set smartindent

" === 表示 ===
set number
set cursorline
set laststatus=2
set showcmd
set showmode
set showmatch
set wrap
set ruler
set title

" === 検索 ===
set hlsearch
set incsearch
set ignorecase
set smartcase

" === 操作性 ===
set wildmenu
set wildmode=list:longest,full
set hidden
set scrolloff=5
set belloff=all

" === ファイル管理 ===
set noswapfile
set nobackup
set undofile

" === キーマッピング ===
let mapleader = "\<Space>"
inoremap jj <Esc>
nnoremap <Esc><Esc> :nohlsearch<CR>
BASELINE
}

# =============================================================================
# 設定項目を抽出する関数
# =============================================================================

extract_settings() {
    local file="$1"
    # コメント行と空行を除外し、設定行を正規化
    grep -vE '^\s*"|^\s*$' "$file" | sed 's/^\s\+//' | sort
}

# set文のキー部分だけを抽出する関数
extract_set_keys() {
    local file="$1"
    grep -oE '^\s*set\s+\S+' "$file" | \
        sed 's/^\s*set\s\+//' | \
        sed 's/=.*//' | \
        sed 's/^no//' | \
        sort -u
}

# =============================================================================
# モード1: vimrc vs 推奨ベースライン
# =============================================================================

compare_with_baseline() {
    local user_file="$1"
    local baseline_file
    baseline_file=$(mktemp)
    generate_baseline > "$baseline_file"

    echo -e "${BOLD}=============================================${RESET}"
    echo -e "${BOLD}  vimrc 比較ツール - 推奨設定との比較${RESET}"
    echo -e "${BOLD}=============================================${RESET}"
    echo ""
    echo -e "  対象ファイル: ${CYAN}${user_file}${RESET}"
    echo -e "  比較対象:     ${CYAN}推奨ベースライン設定${RESET}"
    echo ""

    # --- 推奨設定のカテゴリ別チェック ---
    local missing=0
    local present=0
    local different=0

    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${BOLD}  【1】基本設定の比較${RESET}"
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo ""

    # チェック対象の設定一覧（設定名:説明:推奨値）
    local checks=(
        "nocompatible:Vi互換モードの無効化:set nocompatible"
        "encoding:文字エンコーディング:set encoding=utf-8"
        "expandtab:スペースインデント:set expandtab"
        "number:行番号表示:set number"
        "hlsearch:検索ハイライト:set hlsearch"
        "incsearch:インクリメンタル検索:set incsearch"
        "ignorecase:大文字小文字無視:set ignorecase"
        "smartcase:スマートケース:set smartcase"
        "cursorline:カーソル行ハイライト:set cursorline"
        "laststatus:ステータスライン:set laststatus=2"
        "wildmenu:コマンド補完メニュー:set wildmenu"
        "hidden:バッファ非表示切替:set hidden"
        "scrolloff:スクロール余白:set scrolloff=5"
        "showmatch:括弧マッチ表示:set showmatch"
        "backspace:バックスペース動作:set backspace=indent,eol,start"
        "undofile:永続アンドゥ:set undofile"
        "belloff:ビープ音無効化:set belloff=all"
        "title:タイトル表示:set title"
    )

    for check in "${checks[@]}"; do
        IFS=':' read -r setting desc recommended <<< "$check"

        # ユーザーファイルでの検索
        if grep -qE "^\s*set\s+(no)?${setting}" "$user_file" 2>/dev/null; then
            user_val=$(grep -oE "^\s*set\s+(no)?${setting}\S*" "$user_file" | tail -1 | sed 's/^\s*//')

            # 推奨値と同じか確認
            if echo "$user_val" | grep -qE "^${recommended}$"; then
                echo -e "  ${GREEN}✓${RESET} ${desc}"
                echo -e "    あなた: ${user_val}"
                ((present++))
            else
                echo -e "  ${YELLOW}△${RESET} ${desc}（値が異なります）"
                echo -e "    あなた: ${YELLOW}${user_val}${RESET}"
                echo -e "    推奨:   ${GREEN}${recommended}${RESET}"
                ((different++))
            fi
        else
            echo -e "  ${RED}✗${RESET} ${desc}（未設定）"
            echo -e "    推奨: ${GREEN}${recommended}${RESET}"
            ((missing++))
        fi
    done

    echo ""

    # --- filetype / syntax のチェック ---
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${BOLD}  【2】重要な設定の確認${RESET}"
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo ""

    # filetype
    if grep -qE '^\s*filetype\s+plugin\s+indent\s+on' "$user_file"; then
        echo -e "  ${GREEN}✓${RESET} filetype plugin indent on"
        ((present++))
    else
        echo -e "  ${RED}✗${RESET} filetype plugin indent on（未設定）"
        ((missing++))
    fi

    # syntax
    if grep -qE '^\s*syntax\s+(enable|on)' "$user_file"; then
        echo -e "  ${GREEN}✓${RESET} syntax enable"
        ((present++))
    else
        echo -e "  ${RED}✗${RESET} syntax enable（未設定）"
        ((missing++))
    fi

    # mapleader
    if grep -qE '^\s*let\s+mapleader' "$user_file"; then
        leader=$(grep -oE "let\s+mapleader\s*=\s*\S+" "$user_file" | tail -1)
        echo -e "  ${GREEN}✓${RESET} Leaderキー設定: ${leader}"
        ((present++))
    else
        echo -e "  ${YELLOW}△${RESET} Leaderキー未設定（デフォルト: \\）"
        echo -e "    推奨: ${GREEN}let mapleader = \"\\<Space>\"${RESET}"
        ((missing++))
    fi

    echo ""

    # --- ユーザー独自の設定 ---
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${BOLD}  【3】あなた独自の設定（ベースラインにないもの）${RESET}"
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo ""

    local user_keys
    user_keys=$(extract_set_keys "$user_file")
    local baseline_keys
    baseline_keys=$(extract_set_keys "$baseline_file")

    local unique_found=0
    while IFS= read -r key; do
        if [ -n "$key" ] && ! echo "$baseline_keys" | grep -qx "$key"; then
            if [ "$unique_found" -eq 0 ]; then
                echo -e "  以下の設定はベースラインには含まれていない独自設定です："
                echo ""
            fi
            val=$(grep -oE "^\s*set\s+(no)?${key}\S*" "$user_file" | tail -1 | sed 's/^\s*//')
            echo -e "  ${CYAN}•${RESET} ${val}"
            ((unique_found++))
        fi
    done <<< "$user_keys"

    if [ "$unique_found" -eq 0 ]; then
        echo -e "  ${CYAN}（ベースラインにない独自設定はありません）${RESET}"
    fi

    echo ""

    # --- サマリー ---
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${BOLD}  サマリー${RESET}"
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo ""
    echo -e "  ${GREEN}一致:     ${present} 件${RESET}"
    echo -e "  ${YELLOW}値が異なる: ${different} 件${RESET}"
    echo -e "  ${RED}未設定:   ${missing} 件${RESET}"

    local total_check=$((present + different + missing))
    if [ "$total_check" -gt 0 ]; then
        local coverage=$((present * 100 / total_check))
        echo ""
        echo -e "  推奨設定カバー率: ${BOLD}${coverage}%${RESET}"
    fi

    echo ""

    # 一時ファイル削除
    rm -f "$baseline_file"
}

# =============================================================================
# モード2: 2つのvimrcファイルを比較
# =============================================================================

compare_two_files() {
    local file1="$1"
    local file2="$2"

    echo -e "${BOLD}=============================================${RESET}"
    echo -e "${BOLD}  vimrc 比較ツール - 2ファイル比較${RESET}"
    echo -e "${BOLD}=============================================${RESET}"
    echo ""
    echo -e "  ファイル1: ${CYAN}${file1}${RESET}"
    echo -e "  ファイル2: ${CYAN}${file2}${RESET}"
    echo ""

    # --- set 設定の比較 ---
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${BOLD}  【1】set 設定の比較${RESET}"
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo ""

    local keys1
    keys1=$(extract_set_keys "$file1")
    local keys2
    keys2=$(extract_set_keys "$file2")

    # ファイル1にだけある設定
    echo -e "  ${CYAN}ファイル1にのみ存在する設定：${RESET}"
    local only1=0
    while IFS= read -r key; do
        if [ -n "$key" ] && ! echo "$keys2" | grep -qx "$key"; then
            val=$(grep -oE "^\s*set\s+(no)?${key}\S*" "$file1" | tail -1 | sed 's/^\s*//')
            echo -e "    ${RED}- ${val}${RESET}"
            ((only1++))
        fi
    done <<< "$keys1"
    [ "$only1" -eq 0 ] && echo -e "    （なし）"

    echo ""

    # ファイル2にだけある設定
    echo -e "  ${CYAN}ファイル2にのみ存在する設定：${RESET}"
    local only2=0
    while IFS= read -r key; do
        if [ -n "$key" ] && ! echo "$keys1" | grep -qx "$key"; then
            val=$(grep -oE "^\s*set\s+(no)?${key}\S*" "$file2" | tail -1 | sed 's/^\s*//')
            echo -e "    ${GREEN}+ ${val}${RESET}"
            ((only2++))
        fi
    done <<< "$keys2"
    [ "$only2" -eq 0 ] && echo -e "    （なし）"

    echo ""

    # 両方にあるが値が異なる設定
    echo -e "  ${CYAN}両方に存在するが値が異なる設定：${RESET}"
    local diff_count=0
    while IFS= read -r key; do
        if [ -n "$key" ] && echo "$keys2" | grep -qx "$key"; then
            val1=$(grep -oE "^\s*set\s+(no)?${key}\S*" "$file1" | tail -1 | sed 's/^\s*//')
            val2=$(grep -oE "^\s*set\s+(no)?${key}\S*" "$file2" | tail -1 | sed 's/^\s*//')
            if [ "$val1" != "$val2" ]; then
                echo -e "    ${YELLOW}${key}:${RESET}"
                echo -e "      ファイル1: ${RED}${val1}${RESET}"
                echo -e "      ファイル2: ${GREEN}${val2}${RESET}"
                ((diff_count++))
            fi
        fi
    done <<< "$keys1"
    [ "$diff_count" -eq 0 ] && echo -e "    （なし）"

    echo ""

    # --- 詳細diff ---
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${BOLD}  【2】詳細な差分（diff）${RESET}"
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo ""

    # 有効な設定行だけを抽出して比較
    local tmp1 tmp2
    tmp1=$(mktemp)
    tmp2=$(mktemp)
    extract_settings "$file1" > "$tmp1"
    extract_settings "$file2" > "$tmp2"

    if diff -q "$tmp1" "$tmp2" > /dev/null 2>&1; then
        echo -e "  ${GREEN}有効な設定行に差分はありません${RESET}"
    else
        diff --color=never -u "$tmp1" "$tmp2" | while IFS= read -r line; do
            case "$line" in
                ---*)  echo -e "  ${RED}${line}${RESET}" ;;
                +++*)  echo -e "  ${GREEN}${line}${RESET}" ;;
                @@*)   echo -e "  ${CYAN}${line}${RESET}" ;;
                -*)    echo -e "  ${RED}${line}${RESET}" ;;
                +*)    echo -e "  ${GREEN}${line}${RESET}" ;;
                *)     echo "  ${line}" ;;
            esac
        done
    fi

    rm -f "$tmp1" "$tmp2"

    echo ""

    # --- サマリー ---
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${BOLD}  サマリー${RESET}"
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo ""
    echo -e "  ファイル1のみ: ${RED}${only1} 設定${RESET}"
    echo -e "  ファイル2のみ: ${GREEN}${only2} 設定${RESET}"
    echo -e "  値が異なる:    ${YELLOW}${diff_count} 設定${RESET}"
    echo ""
}

# =============================================================================
# メイン処理
# =============================================================================

case "$#" in
    0)
        # 引数なし: ~/.vimrc と推奨設定を比較
        if [ -f "$HOME/.vimrc" ]; then
            compare_with_baseline "$HOME/.vimrc"
        elif [ -f "$HOME/.vim/vimrc" ]; then
            compare_with_baseline "$HOME/.vim/vimrc"
        else
            echo -e "${RED}エラー: ~/.vimrc が見つかりません${RESET}"
            echo ""
            echo "使い方:"
            echo "  $0                         # ~/.vimrc と推奨設定を比較"
            echo "  $0 <vimrc>                 # 指定ファイルと推奨設定を比較"
            echo "  $0 <vimrc1> <vimrc2>       # 2つのファイルを比較"
            exit 1
        fi
        ;;
    1)
        # 引数1つ: 指定ファイルと推奨設定を比較
        if [ ! -f "$1" ]; then
            echo -e "${RED}エラー: ファイルが見つかりません: $1${RESET}"
            exit 1
        fi
        compare_with_baseline "$1"
        ;;
    2)
        # 引数2つ: 2つのファイルを比較
        if [ ! -f "$1" ]; then
            echo -e "${RED}エラー: ファイルが見つかりません: $1${RESET}"
            exit 1
        fi
        if [ ! -f "$2" ]; then
            echo -e "${RED}エラー: ファイルが見つかりません: $2${RESET}"
            exit 1
        fi
        compare_two_files "$1" "$2"
        ;;
    *)
        echo "使い方:"
        echo "  $0                         # ~/.vimrc と推奨設定を比較"
        echo "  $0 <vimrc>                 # 指定ファイルと推奨設定を比較"
        echo "  $0 <vimrc1> <vimrc2>       # 2つのファイルを比較"
        exit 1
        ;;
esac

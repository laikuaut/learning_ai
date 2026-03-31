#!/bin/bash
# =============================================================================
# 学べる内容：
#   - vimrcの基本的な設定項目と各設定の意味
#   - プログラミング言語に応じた推奨設定
#   - インデント・表示・検索・その他の主要オプション
#
# 実行方法：
#   chmod +x 01_vimrc設定ジェネレータ.sh
#   ./01_vimrc設定ジェネレータ.sh
#   # 生成された内容をファイルに保存する場合：
#   ./01_vimrc設定ジェネレータ.sh > my_vimrc
# =============================================================================

# --- 色付き出力用 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
RESET='\033[0m'

# 標準エラー出力にプロンプトを出す（stdoutはvimrc本体用に確保）
prompt() {
    echo -e "${CYAN}$1${RESET}" >&2
}

info() {
    echo -e "${GREEN}$1${RESET}" >&2
}

header() {
    echo -e "${BOLD}${YELLOW}$1${RESET}" >&2
}

# =============================================================================
# メイン処理
# =============================================================================

header "============================================="
header "  vimrc 設定ジェネレータ"
header "  対話形式であなた専用の .vimrc を生成します"
header "============================================="
echo "" >&2

# --- 1. プログラミング言語 ---
prompt "【質問1】主に使用するプログラミング言語を選んでください："
prompt "  1) Python"
prompt "  2) JavaScript / TypeScript"
prompt "  3) C / C++"
prompt "  4) Go"
prompt "  5) Ruby"
prompt "  6) 汎用（特定の言語なし）"
read -rp "番号を入力 [1-6, デフォルト: 6]: " lang_choice
lang_choice=${lang_choice:-6}

# --- 2. インデント設定 ---
prompt ""
prompt "【質問2】インデントにタブとスペースのどちらを使いますか？"
prompt "  1) スペース（推奨）"
prompt "  2) タブ"
read -rp "番号を入力 [1-2, デフォルト: 1]: " indent_type
indent_type=${indent_type:-1}

prompt ""
prompt "【質問3】インデント幅は何文字にしますか？"
prompt "  1) 2文字"
prompt "  2) 4文字"
prompt "  3) 8文字"
read -rp "番号を入力 [1-3, デフォルト: 2]: " indent_width
indent_width=${indent_width:-2}

case "$indent_width" in
    1) tab_size=2 ;;
    3) tab_size=8 ;;
    *) tab_size=4 ;;
esac

# --- 3. 行番号 ---
prompt ""
prompt "【質問4】行番号を表示しますか？"
prompt "  1) 表示する（絶対行番号）"
prompt "  2) 相対行番号を表示する"
prompt "  3) 表示しない"
read -rp "番号を入力 [1-3, デフォルト: 1]: " line_num
line_num=${line_num:-1}

# --- 4. カラースキーム ---
prompt ""
prompt "【質問5】背景色の好みは？"
prompt "  1) ダーク（暗い背景）"
prompt "  2) ライト（明るい背景）"
read -rp "番号を入力 [1-2, デフォルト: 1]: " bg_choice
bg_choice=${bg_choice:-1}

# --- 5. 検索設定 ---
prompt ""
prompt "【質問6】インクリメンタル検索を有効にしますか？（入力中にリアルタイムで検索）"
read -rp "[Y/n]: " inc_search
inc_search=${inc_search:-Y}

# --- 6. マウス ---
prompt ""
prompt "【質問7】マウス操作を有効にしますか？"
read -rp "[y/N]: " mouse_enable
mouse_enable=${mouse_enable:-N}

# --- 7. クリップボード ---
prompt ""
prompt "【質問8】システムクリップボードと連携しますか？"
read -rp "[Y/n]: " clipboard
clipboard=${clipboard:-Y}

# --- 8. Leader キー ---
prompt ""
prompt "【質問9】Leader キーをスペースキーに変更しますか？（デフォルトは \\）"
read -rp "[Y/n]: " leader_space
leader_space=${leader_space:-Y}

# =============================================================================
# vimrc 生成
# =============================================================================
info ""
info "設定を生成しています..."
info ""

cat << 'VIMRC_HEADER'
" =============================================================================
" .vimrc - 自動生成された設定ファイル
" vimrc設定ジェネレータによって作成
" =============================================================================

" ---------------------------------------------------------------------------
" 基本設定
" ---------------------------------------------------------------------------
" Vi互換モードを無効化（Vimの拡張機能を使用）
set nocompatible

" ファイルタイプ検出・プラグイン・インデントを有効化
filetype plugin indent on

" シンタックスハイライトを有効化
syntax enable

" 文字コードをUTF-8に設定
set encoding=utf-8
set fileencoding=utf-8
set fileencodings=utf-8,cp932,euc-jp,latin1

" バックスペースの挙動を直感的に
set backspace=indent,eol,start

VIMRC_HEADER

# --- インデント設定 ---
echo '" ---------------------------------------------------------------------------'
echo '" インデント設定'
echo '" ---------------------------------------------------------------------------'

if [ "$indent_type" = "1" ]; then
    echo '" タブの代わりにスペースを使用'
    echo 'set expandtab'
else
    echo '" タブ文字を使用（expandtab を無効化）'
    echo 'set noexpandtab'
fi

echo "\" タブ幅を${tab_size}文字に設定"
echo "set tabstop=${tab_size}"
echo "\" 自動インデントの幅を${tab_size}文字に設定"
echo "set shiftwidth=${tab_size}"
echo "\" タブキー押下時のスペース数"
echo "set softtabstop=${tab_size}"
echo '" 新しい行で自動インデント'
echo 'set autoindent'
echo '" 賢い自動インデント'
echo 'set smartindent'
echo ''

# --- 行番号 ---
echo '" ---------------------------------------------------------------------------'
echo '" 表示設定'
echo '" ---------------------------------------------------------------------------'

case "$line_num" in
    1)
        echo '" 行番号を表示'
        echo 'set number'
        ;;
    2)
        echo '" 相対行番号を表示（現在行は絶対行番号）'
        echo 'set number'
        echo 'set relativenumber'
        ;;
    3)
        echo '" 行番号を非表示'
        echo 'set nonumber'
        ;;
esac

# --- 背景色 ---
echo ''
if [ "$bg_choice" = "1" ]; then
    echo '" ダークカラースキーム'
    echo 'set background=dark'
    echo 'colorscheme desert'
else
    echo '" ライトカラースキーム'
    echo 'set background=light'
fi

cat << 'VIMRC_DISPLAY'

" カーソル行をハイライト
set cursorline

" ステータスラインを常に表示
set laststatus=2

" コマンドラインの行数
set cmdheight=1

" 入力中のコマンドをステータスラインに表示
set showcmd

" 現在のモードを表示
set showmode

" 対応する括弧をハイライト
set showmatch

" 折り返しを有効化
set wrap

" ルーラー（カーソル位置情報）を表示
set ruler

" ターミナルのタイトルを設定
set title

VIMRC_DISPLAY

# --- 検索設定 ---
echo '" ---------------------------------------------------------------------------'
echo '" 検索設定'
echo '" ---------------------------------------------------------------------------'

if [[ "$inc_search" =~ ^[Yy] ]]; then
    echo '" インクリメンタル検索（入力中にリアルタイム検索）'
    echo 'set incsearch'
fi

cat << 'VIMRC_SEARCH'
" 検索結果をハイライト
set hlsearch

" 大文字小文字を無視して検索
set ignorecase

" 大文字が含まれる場合は区別して検索
set smartcase

VIMRC_SEARCH

# --- マウス ---
if [[ "$mouse_enable" =~ ^[Yy] ]]; then
    echo '" マウス操作を有効化（全モード）'
    echo 'set mouse=a'
    echo ''
fi

# --- クリップボード ---
if [[ "$clipboard" =~ ^[Yy] ]]; then
    echo '" システムクリップボードと連携'
    echo 'set clipboard=unnamedplus'
    echo ''
fi

# --- Leader キー ---
if [[ "$leader_space" =~ ^[Yy] ]]; then
    cat << 'VIMRC_LEADER'
" ---------------------------------------------------------------------------
" Leaderキー設定
" ---------------------------------------------------------------------------
" Leaderキーをスペースに変更（デフォルトは \）
let mapleader = "\<Space>"

VIMRC_LEADER
fi

# --- キーマッピング ---
cat << 'VIMRC_KEYMAP'
" ---------------------------------------------------------------------------
" キーマッピング（noremapを使用して再帰マッピングを防止）
" ---------------------------------------------------------------------------
" ESCの代わりに jj で挿入モードを抜ける
inoremap jj <Esc>

" 検索ハイライトを消す
nnoremap <Esc><Esc> :nohlsearch<CR>

" ウィンドウ移動を簡単に
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" 行の先頭・末尾に移動
nnoremap H ^
nnoremap L $

" ビジュアルモードでインデント後も選択を維持
vnoremap < <gv
vnoremap > >gv

VIMRC_KEYMAP

# --- 言語固有の設定 ---
echo '" ---------------------------------------------------------------------------'
echo '" 言語固有の設定（autocmd）'
echo '" ---------------------------------------------------------------------------'
echo '" augroupで囲むことで、vimrc再読み込み時の重複登録を防止'
echo 'augroup MyFileTypeSettings'
echo '  autocmd!'

case "$lang_choice" in
    1)
        echo '  " Python: インデント4、行の長さガイド表示'
        echo '  autocmd FileType python setlocal tabstop=4 shiftwidth=4 softtabstop=4 expandtab'
        echo '  autocmd FileType python setlocal colorcolumn=80'
        echo '  autocmd FileType python setlocal textwidth=79'
        ;;
    2)
        echo '  " JavaScript/TypeScript: インデント2'
        echo '  autocmd FileType javascript,typescript setlocal tabstop=2 shiftwidth=2 softtabstop=2 expandtab'
        echo '  autocmd FileType json setlocal tabstop=2 shiftwidth=2 softtabstop=2 expandtab'
        echo '  autocmd FileType html,css setlocal tabstop=2 shiftwidth=2 softtabstop=2 expandtab'
        ;;
    3)
        echo '  " C/C++: インデント4、タブ使用も可'
        echo '  autocmd FileType c,cpp setlocal tabstop=4 shiftwidth=4 softtabstop=4'
        echo '  autocmd FileType c,cpp setlocal cinoptions+=:0  " switchのcaseインデント'
        ;;
    4)
        echo '  " Go: タブ使用、タブ幅4（Go標準）'
        echo '  autocmd FileType go setlocal tabstop=4 shiftwidth=4 softtabstop=4 noexpandtab'
        ;;
    5)
        echo '  " Ruby: インデント2'
        echo '  autocmd FileType ruby setlocal tabstop=2 shiftwidth=2 softtabstop=2 expandtab'
        ;;
esac

cat << 'VIMRC_AUTOCMD'
  " Markdownのファイルタイプ設定
  autocmd BufNewFile,BufRead *.md setlocal filetype=markdown
  " 保存時に末尾の空白を自動削除
  autocmd BufWritePre * :%s/\s\+$//ge
augroup END

VIMRC_AUTOCMD

# --- その他の便利設定 ---
cat << 'VIMRC_MISC'
" ---------------------------------------------------------------------------
" その他の便利設定
" ---------------------------------------------------------------------------
" スワップファイルを作成しない
set noswapfile

" バックアップファイルを作成しない
set nobackup

" undoファイルを有効化（永続的なアンドゥ）
set undofile
set undodir=~/.vim/undo

" コマンドライン補完を強化
set wildmenu
set wildmode=list:longest,full

" バッファを保存しなくても切り替え可能に
set hidden

" スクロール時に上下に余裕を持たせる
set scrolloff=5

" ビープ音を無効化
set belloff=all

" 高速なターミナル接続を前提とした描画
set ttyfast

" 再描画を遅延させてマクロ実行を高速化
set lazyredraw
VIMRC_MISC

info "=========================================="
info "  vimrc の生成が完了しました！"
info ""
info "  使い方："
info "    1) 出力内容を ~/.vimrc にコピー"
info "    2) または以下のコマンドで直接保存："
info "       ./01_vimrc設定ジェネレータ.sh > ~/.vimrc"
info "    3) Vimを開いて :source ~/.vimrc で反映"
info "=========================================="

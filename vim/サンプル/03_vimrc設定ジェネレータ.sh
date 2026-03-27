#!/bin/bash
# ============================================================
# vimrc設定ジェネレータ
# ============================================================
# 学べる内容:
#   - .vimrcの基本的な設定項目と役割
#   - 行番号・タブ・検索・カラースキームの設定方法
#   - キーマッピングの基本
#   - 自分好みのVim環境をカスタマイズする方法
#
# 実行方法:
#   chmod +x 03_vimrc設定ジェネレータ.sh
#   ./03_vimrc設定ジェネレータ.sh
# ============================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RESET='\033[0m'

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

section() { echo -e "\n${GREEN}========== $1 ==========${RESET}\n"; }
info()    { echo -e "${CYAN}[INFO]${RESET} $1"; }
run_cmd() { echo -e "${YELLOW}\$ $1${RESET}"; eval "$1"; }
pause()   { echo -e "\n${CYAN}[Enter を押して次へ進む]${RESET}"; read -r; }

OUTPUT="$TMPDIR/generated_vimrc"

section "vimrc 設定ジェネレータへようこそ！"
info "いくつかの質問に答えるだけで、あなた専用の .vimrc を生成します。"
pause

# ヘッダー部分を書き出し
cat > "$OUTPUT" <<'EOF'
" ============================================================
" 自動生成された .vimrc
" ============================================================
" このファイルを ~/.vimrc にコピーして使ってください。
"   cp generated_vimrc ~/.vimrc
" ============================================================

" --- 基本設定 ---
set nocompatible        " Vi互換モードを無効化
set encoding=utf-8      " 文字エンコーディング
set fileencoding=utf-8  " ファイル保存時のエンコーディング
set backspace=indent,eol,start  " Backspaceの挙動を自然に

EOF

# ----------------------------------------------------------
section "1. 行番号の設定"
echo "行番号の表示方法を選んでください:"
echo "  1) 絶対行番号（set number）"
echo "  2) 相対行番号（set relativenumber）"
echo "  3) 両方表示（set number + relativenumber）"
echo "  4) 表示しない"
echo ""
read -rp "選択 [1-4] (デフォルト: 1): " num_choice
num_choice=${num_choice:-1}

{
  echo '" --- 行番号 ---'
  case "$num_choice" in
    1) echo "set number" ;;
    2) echo "set relativenumber" ;;
    3) echo "set number"; echo "set relativenumber" ;;
    4) echo '" 行番号: 非表示' ;;
  esac
  echo ""
} >> "$OUTPUT"
info "行番号の設定を追加しました。"
pause

# ----------------------------------------------------------
section "2. タブ・インデントの設定"
echo "タブ幅を選んでください:"
echo "  1) 2スペース（Web開発向け）"
echo "  2) 4スペース（Python等の一般的な開発向け）"
echo "  3) 8スペース（カーネル・伝統的なスタイル）"
echo "  4) タブ文字をそのまま使用"
echo ""
read -rp "選択 [1-4] (デフォルト: 2): " tab_choice
tab_choice=${tab_choice:-2}

{
  echo '" --- タブ・インデント ---'
  case "$tab_choice" in
    1) echo "set tabstop=2"; echo "set shiftwidth=2"; echo "set expandtab" ;;
    2) echo "set tabstop=4"; echo "set shiftwidth=4"; echo "set expandtab" ;;
    3) echo "set tabstop=8"; echo "set shiftwidth=8"; echo "set expandtab" ;;
    4) echo "set tabstop=4"; echo "set shiftwidth=4"; echo "set noexpandtab" ;;
  esac
  echo "set autoindent          \" 自動インデント"
  echo "set smartindent         \" スマートインデント"
  echo ""
} >> "$OUTPUT"
info "タブ設定を追加しました。"
pause

# ----------------------------------------------------------
section "3. 検索の設定"
echo "検索オプションを選んでください（複数選択可、例: 123）:"
echo "  1) インクリメンタル検索（set incsearch）"
echo "  2) 検索結果をハイライト（set hlsearch）"
echo "  3) 大文字小文字を無視（set ignorecase + smartcase）"
echo ""
read -rp "選択 (デフォルト: 123): " search_choice
search_choice=${search_choice:-123}

{
  echo '" --- 検索 ---'
  [[ "$search_choice" == *1* ]] && echo "set incsearch           \" インクリメンタル検索"
  [[ "$search_choice" == *2* ]] && echo "set hlsearch            \" 検索ハイライト"
  if [[ "$search_choice" == *3* ]]; then
    echo "set ignorecase          \" 大文字小文字を無視"
    echo "set smartcase           \" 大文字を含む場合は区別"
  fi
  echo ""
} >> "$OUTPUT"
info "検索設定を追加しました。"
pause

# ----------------------------------------------------------
section "4. カラースキームと外観"
echo "カラースキームを選んでください:"
echo "  1) desert（暖色系、目に優しい）"
echo "  2) slate（青系、落ち着いた雰囲気）"
echo "  3) elflord（高コントラスト）"
echo "  4) murphy（緑系）"
echo "  5) 指定しない"
echo ""
read -rp "選択 [1-5] (デフォルト: 1): " color_choice
color_choice=${color_choice:-1}

{
  echo '" --- 外観 ---'
  echo "syntax on               \" シンタックスハイライト有効"
  case "$color_choice" in
    1) echo "colorscheme desert" ;;
    2) echo "colorscheme slate" ;;
    3) echo "colorscheme elflord" ;;
    4) echo "colorscheme murphy" ;;
    5) echo '" カラースキーム: デフォルト' ;;
  esac
  echo "set cursorline          \" カーソル行をハイライト"
  echo "set showcmd             \" 入力中のコマンドを表示"
  echo "set laststatus=2        \" ステータスラインを常に表示"
  echo "set wildmenu            \" コマンド補完を強化"
  echo ""
} >> "$OUTPUT"
info "外観設定を追加しました。"
pause

# ----------------------------------------------------------
section "5. キーマッピング"
echo "便利なキーマッピングを追加しますか？"
echo "  1) はい（おすすめ設定を追加）"
echo "  2) いいえ"
echo ""
read -rp "選択 [1-2] (デフォルト: 1): " map_choice
map_choice=${map_choice:-1}

if [[ "$map_choice" == "1" ]]; then
  cat >> "$OUTPUT" <<'EOF'
" --- キーマッピング ---
" jj で挿入モードを抜ける
inoremap jj <Esc>
" Ctrl+s で保存（ターミナル設定が必要な場合あり）
nnoremap <C-s> :w<CR>
inoremap <C-s> <Esc>:w<CR>a
" スペースでリーダーキーを設定
let mapleader = " "
" リーダー+w で保存
nnoremap <Leader>w :w<CR>
" リーダー+q で終了
nnoremap <Leader>q :q<CR>
" 検索ハイライトを消す
nnoremap <Leader>h :nohlsearch<CR>
" 行の先頭・末尾への移動をわかりやすく
nnoremap H ^
nnoremap L $

EOF
  info "キーマッピングを追加しました。"
else
  echo '" キーマッピング: なし' >> "$OUTPUT"
  echo "" >> "$OUTPUT"
fi
pause

# ----------------------------------------------------------
section "生成結果"
info "以下の .vimrc が生成されました:"
echo ""
run_cmd "cat -n '$OUTPUT'"
pause

# ----------------------------------------------------------
section "ファイルの保存"
echo "生成した .vimrc をどこに保存しますか？"
echo "  1) 現在のディレクトリに generated_vimrc として保存"
echo "  2) 表示のみ（保存しない）"
echo ""
read -rp "選択 [1-2] (デフォルト: 2): " save_choice
save_choice=${save_choice:-2}

if [[ "$save_choice" == "1" ]]; then
  cp "$OUTPUT" ./generated_vimrc
  info "generated_vimrc として保存しました。"
  info "適用するには: cp generated_vimrc ~/.vimrc"
else
  info "保存をスキップしました。"
fi

echo ""
info "ジェネレータ完了！一時ファイルは自動的に削除されます。"

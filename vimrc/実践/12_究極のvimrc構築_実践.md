# 実践課題12：究極の vimrc 構築 ★5

> **難易度**: ★★★★★（総合）
> **前提知識**: 第1章〜第8章（すべての章の知識）
> **課題の種類**: ミニプロジェクト（総合）
> **学習目標**: これまで学んだすべての知識を統合し、実務で即戦力となる完成度の高い vimrc を一から構築する

---

## 完成イメージ

```
┌──────────────────────────────────────────────────────────────┐
│  究極の vimrc に求められる要件                                 │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  【構成】                                                     │
│    - 論理的なセクション分けと折りたたみマーカー               │
│    - ftplugin によるファイルタイプ別設定の分離                │
│    - vim-plug によるプラグイン管理                             │
│    - Git 管理可能なディレクトリ構成                           │
│                                                               │
│  【安全性】                                                   │
│    - noremap 系マッピングの徹底                               │
│    - augroup による autocmd 重複防止                          │
│    - 環境条件分岐（OS、Vim バージョン、外部ツール）           │
│    - vim-plug の自動インストール                               │
│    - undodir の自動作成                                       │
│                                                               │
│  【実用機能】                                                 │
│    - 効率的なキーマッピング（Leader, ウィンドウ, バッファ）   │
│    - 検索・置換の最適化（ripgrep 連携）                       │
│    - カスタム関数（空白削除、行番号トグル等）                 │
│    - ファイルタイプ別のインデント・実行マッピング             │
│    - カーソル位置復元、外部変更の自動再読み込み               │
│                                                               │
│  【ポータビリティ】                                           │
│    - Linux / macOS / Windows で動作する                       │
│    - git clone → vim 起動だけで環境構築が完了する             │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 課題の要件

以下のすべての要件を満たす vimrc を一から構築してください。

### 必須要件（10項目）

1. **基本設定**: `nocompatible`, エンコーディング, `backspace`, `belloff` の設定
2. **表示設定**: ハイブリッド行番号、カーソルライン、ステータスライン（モード表示付き）、不可視文字の可視化、True Color 対応
3. **インデント設定**: デフォルトのインデント幅設定、`shiftround` の有効化
4. **検索設定**: 基本4設定、`wrapscan`、外部 grep ツール連携（ripgrep 対応）
5. **キーマッピング**: Leader キーの設定、ノーマル/挿入/ビジュアル/コマンドラインの各モード用マッピング（最低15個）
6. **autocmd**: `augroup` で囲んだファイルタイプ別設定（最低4言語）、カーソル位置復元、ファイル自動再読み込み
7. **カスタム関数**: 末尾空白削除、少なくとも1つの追加関数
8. **プラグイン管理**: vim-plug の自動インストール、最低3つのプラグイン登録と設定
9. **バックアップ/Undo**: スワップファイル無効化、永続 Undo の設定（ディレクトリ自動作成）
10. **環境対応**: OS 判定またはツール存在チェックを含む条件分岐が最低2箇所

### 品質要件

- すべてのマッピングに `noremap` 系を使用すること
- すべての autocmd が `augroup` で囲まれていること
- セクションごとにコメントで区切られていること
- `:source %` で再読み込みしてもエラーが出ないこと（冪等性）
- 新しい環境でも自動的にセットアップが完了する設計であること

---

## ステップガイド

<details>
<summary>ステップ1：全体のアウトラインを設計する</summary>

まずセクション構成を決めてから中身を埋めていくのが効率的です。

```vim
" ============================================================
" vimrc - My Ultimate Configuration
" Author: (あなたの名前)
" Last Updated: (日付)
" ============================================================

" {{{ 1. Bootstrap (vim-plug)
" }}}

" {{{ 2. Plugins
" }}}

" {{{ 3. General Settings
" }}}

" {{{ 4. Display
" }}}

" {{{ 5. Indent
" }}}

" {{{ 6. Search
" }}}

" {{{ 7. Key Mappings
" }}}

" {{{ 8. Autocmd
" }}}

" {{{ 9. Custom Functions & Commands
" }}}

" {{{ 10. Plugin Config
" }}}
```

各セクションに何を書くかを先にコメントで書き出してから、実装に入りましょう。

</details>

<details>
<summary>ステップ2：安全性に関する設定を先に書く</summary>

以下は「どの vimrc にも最初に書くべき」定型パターンです。

```vim
" vim-plug 自動インストール
let s:plug_path = expand('~/.vim/autoload/plug.vim')
if !filereadable(s:plug_path)
  silent execute '!curl -fLo ' . s:plug_path . ' --create-dirs '
    \ . 'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

" undodir 自動作成
if !isdirectory(expand('~/.vim/undodir'))
  call mkdir(expand('~/.vim/undodir'), 'p')
endif

" 環境判定
let s:is_mac = has('macunix')
let s:is_linux = has('unix') && !has('macunix')
let s:is_win = has('win32') || has('win64')
```

</details>

<details>
<summary>ステップ3：マッピングを体系的に設計する</summary>

Leader マッピングの体系を事前に設計すると、一貫性のあるキーバインドになります。

```
┌──────────────────────────────────────────────┐
│  Leader マッピングの設計例                     │
├──────────────────────────────────────────────┤
│  <Leader>w  → 保存                           │
│  <Leader>q  → 終了                           │
│  <Leader>e  → ファイルエクスプローラー        │
│  <Leader>/  → 検索ハイライト解除             │
│  <Leader>f  → ファイル検索（fzf）            │
│  <Leader>b  → バッファ一覧                   │
│  <Leader>v  → 垂直分割                       │
│  <Leader>s  → 水平分割                       │
│  <Leader>tw → 末尾空白削除                   │
│  <Leader>tn → 行番号トグル                   │
│  <Leader>r  → ファイル実行（FT別）           │
│  <Leader>ev → vimrc を開く                   │
│  <Leader>sv → vimrc を再読み込み             │
└──────────────────────────────────────────────┘
```

</details>

<details>
<summary>ステップ4：テストと検証</summary>

完成した vimrc を以下の手順で検証しましょう。

1. **起動テスト**: `vim -u your_vimrc` でエラーなく起動するか
2. **再読み込みテスト**: `:source %` を3回実行してエラーが出ないか（冪等性）
3. **マッピングテスト**: `:map <Leader>` で Leader マッピングが正しく登録されているか
4. **ファイルタイプテスト**: `.py`, `.js`, `.html`, `Makefile` を開いてインデント幅が正しいか
5. **プラグインテスト**: `:PlugStatus` でプラグインが正常にインストールされているか
6. **関数テスト**: `:TrimWhitespace` 等のカスタムコマンドが動作するか

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け ─ 必要十分な構成）</summary>

```vim
" ============================================================
" vimrc - My Configuration
" ============================================================

" --- vim-plug 自動インストール ---
let s:plug_path = expand('~/.vim/autoload/plug.vim')
if !filereadable(s:plug_path)
  silent execute '!curl -fLo ' . s:plug_path . ' --create-dirs '
    \ . 'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

" --- プラグイン ---
call plug#begin('~/.vim/plugged')
  Plug 'morhetz/gruvbox'
  Plug 'tpope/vim-commentary'
  Plug 'tpope/vim-surround'
call plug#end()

" --- 基本設定 ---
set nocompatible
set encoding=utf-8
set fileencoding=utf-8
set fileencodings=utf-8,cp932,euc-jp
set backspace=indent,eol,start
set belloff=all
set hidden
set confirm
set autoread
set updatetime=300
set timeoutlen=500

" --- 表示設定 ---
syntax enable
filetype plugin indent on

set number relativenumber
set cursorline
set scrolloff=5
set laststatus=2
set showcmd
set showmatch
set wrap linebreak

set list
set listchars=tab:»\ ,trail:·,extends:>,precedes:<

set background=dark
silent! colorscheme gruvbox

set statusline=%f\ %m%r\ [%{&fenc!=''?&fenc:&enc}/%{&ff}]%=\ %Y\ %l:%c\ %p%%

" --- インデント ---
set tabstop=2 shiftwidth=2 softtabstop=2
set expandtab
set autoindent
set shiftround

" --- 検索 ---
set hlsearch incsearch
set ignorecase smartcase
set wrapscan

if executable('rg')
  set grepprg=rg\ --vimgrep\ --smart-case
  set grepformat=%f:%l:%c:%m
endif

" --- バックアップ / Undo ---
set nobackup noswapfile nowritebackup
set undofile
if !isdirectory(expand('~/.vim/undodir'))
  call mkdir(expand('~/.vim/undodir'), 'p')
endif
set undodir=~/.vim/undodir

" --- クリップボード ---
if has('unnamedplus')
  set clipboard=unnamedplus
else
  set clipboard=unnamed
endif

set wildmenu
set wildmode=list:longest,full

" --- キーマッピング ---
let mapleader = "\<Space>"

" ノーマルモード
nnoremap Y y$
nnoremap j gj
nnoremap k gk
nnoremap n nzzzv
nnoremap N Nzzzv
nnoremap <Leader>w :w<CR>
nnoremap <Leader>q :q<CR>
nnoremap <Leader>/ :nohlsearch<CR>
nnoremap <Leader>e :Explore<CR>
nnoremap <Leader>ev :edit $MYVIMRC<CR>
nnoremap <Leader>sv :source $MYVIMRC<CR>
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" 挿入モード
inoremap jj <Esc>

" ビジュアルモード
vnoremap < <gv
vnoremap > >gv

" --- autocmd ---
augroup vimrc_filetypes
  autocmd!
  autocmd FileType python     setlocal ts=4 sw=4 sts=4 expandtab colorcolumn=88
  autocmd FileType javascript setlocal ts=2 sw=2 sts=2 expandtab
  autocmd FileType html,css   setlocal ts=2 sw=2 sts=2 expandtab
  autocmd FileType make       setlocal noexpandtab ts=4 sw=4
  autocmd FileType help       nnoremap <buffer> q :q<CR>
augroup END

augroup vimrc_general
  autocmd!
  autocmd BufReadPost *
    \ if line("'\"") >= 1 && line("'\"") <= line("$") && &ft !~# 'commit' |
    \   exe "normal! g`\"" |
    \ endif
  autocmd FocusGained,BufEnter * checktime
augroup END

" --- カスタム関数 ---
function! s:TrimWhitespace() abort
  let l:save = winsaveview()
  keeppatterns %s/\s\+$//e
  call winrestview(l:save)
endfunction

command! TrimWhitespace call s:TrimWhitespace()
nnoremap <Leader>tw :TrimWhitespace<CR>
```

</details>

<details>
<summary>解答例（改良版 ─ プロ仕様の完成形）</summary>

```vim
" ============================================================
" vimrc - Ultimate Configuration
" Author: Vim Enthusiast
" Last Updated: 2025-01-01
" Description: Portable, safe, and productive Vim configuration.
"              Works on Linux, macOS, and Windows.
"              Run `git clone` + `vim` to set up.
" ============================================================

" {{{ 1. Environment Detection
let s:is_mac   = has('macunix')
let s:is_linux = has('unix') && !has('macunix')
let s:is_win   = has('win32') || has('win64')
let s:has_rg   = executable('rg')
let s:vim_dir  = s:is_win ? expand('~/vimfiles') : expand('~/.vim')
" }}}

" {{{ 2. Bootstrap (vim-plug)
let s:plug_path = s:vim_dir . '/autoload/plug.vim'
if !filereadable(s:plug_path)
  echo "Installing vim-plug..."
  if s:is_win
    silent execute '!powershell -Command "New-Item -ItemType Directory -Path '
      \ . s:vim_dir . '/autoload -Force; Invoke-WebRequest -Uri '
      \ . 'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
      \ . ' -OutFile ' . s:plug_path . '"'
  else
    silent execute '!curl -fLo ' . s:plug_path . ' --create-dirs '
      \ . 'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
  endif
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif
" }}}

" {{{ 3. Plugins
call plug#begin(s:vim_dir . '/plugged')

  " テーマ
  Plug 'morhetz/gruvbox'

  " 編集支援
  Plug 'tpope/vim-commentary'
  Plug 'tpope/vim-surround'
  Plug 'tpope/vim-repeat'
  Plug 'jiangmiao/auto-pairs'

  " ファイル操作
  Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
  Plug 'junegunn/fzf.vim'

  " Git
  Plug 'airblade/vim-gitgutter'

call plug#end()
" }}}

" {{{ 4. General Settings
set nocompatible
set encoding=utf-8
scriptencoding utf-8
set fileencoding=utf-8
set fileencodings=utf-8,cp932,euc-jp

let mapleader = "\<Space>"
let maplocalleader = ","

set hidden
set confirm
set autoread
set updatetime=300
set timeoutlen=500
set backspace=indent,eol,start
set belloff=all
set mouse=a
set history=1000
" }}}

" {{{ 5. Display
syntax enable
filetype plugin indent on

set number relativenumber
set cursorline
set signcolumn=yes
set scrolloff=8
set sidescrolloff=8
set laststatus=2
set noshowmode
set showcmd
set showmatch
set shortmess+=c
set wrap linebreak
set display=lastline

set list
set listchars=tab:▸\ ,trail:·,extends:>,precedes:<,nbsp:+

if has('termguicolors')
  let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum"
  let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum"
  set termguicolors
endif

set background=dark
silent! colorscheme gruvbox

" カスタムステータスライン
let g:mode_map = {
  \ 'n': 'NOR', 'i': 'INS', 'v': 'VIS',
  \ 'V': 'V-L', "\<C-v>": 'V-B',
  \ 'c': 'CMD', 'R': 'REP', 't': 'TER',
  \ 's': 'SEL', 'S': 'S-L', "\<C-s>": 'S-B'
  \ }

set statusline=
set statusline+=\ %{get(g:mode_map,mode(),'???')}
set statusline+=\ \|\ %f\ %m%r%h%w
set statusline+=\ [%{&fenc!=''?&fenc:&enc}/%{&ff}]
set statusline+=%=
set statusline+=\ %Y
set statusline+=\ \|\ %l:%c\ (%L)\ %p%%\
" }}}

" {{{ 6. Indent
set tabstop=2 shiftwidth=2 softtabstop=2
set expandtab smarttab
set autoindent
set shiftround
" }}}

" {{{ 7. Search
set hlsearch incsearch
set ignorecase smartcase
set wrapscan

if s:has_rg
  set grepprg=rg\ --vimgrep\ --smart-case\ --hidden\ --glob\ '!.git'
  set grepformat=%f:%l:%c:%m
endif
" }}}

" {{{ 8. Backup / Undo / Clipboard
set nobackup noswapfile nowritebackup

set undofile
let s:undodir = s:vim_dir . '/undodir'
if !isdirectory(s:undodir)
  call mkdir(s:undodir, 'p')
endif
let &undodir = s:undodir

if has('unnamedplus')
  set clipboard=unnamedplus
else
  set clipboard=unnamed
endif

set wildmenu
set wildmode=list:longest,full
set completeopt=menuone,noinsert,noselect
" }}}

" {{{ 9. Key Mappings

" --- ノーマルモード: 基本操作の改善 ---
nnoremap Y y$
nnoremap <expr> j v:count == 0 ? 'gj' : 'j'
nnoremap <expr> k v:count == 0 ? 'gk' : 'k'
nnoremap n nzzzv
nnoremap N Nzzzv
nnoremap J mzJ`z
nnoremap U <C-r>

" --- ノーマルモード: Leader マッピング ---
nnoremap <Leader>w  :w<CR>
nnoremap <Leader>q  :q<CR>
nnoremap <Leader>x  :x<CR>
nnoremap <Leader>/  :nohlsearch<CR>
nnoremap <Leader>e  :Explore<CR>
nnoremap <Leader>ev :edit $MYVIMRC<CR>
nnoremap <Leader>sv :source $MYVIMRC<CR>

" ウィンドウ操作
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l
nnoremap <Leader>v :vsplit<CR>
nnoremap <Leader>sp :split<CR>
nnoremap + <C-w>5+
nnoremap - <C-w>5-

" バッファ操作
nnoremap ]b :bnext<CR>
nnoremap [b :bprevious<CR>
nnoremap <Leader>bd :bdelete<CR>

" Quickfix 操作
nnoremap ]q :cnext<CR>zz
nnoremap [q :cprevious<CR>zz

" --- 挿入モード ---
inoremap jj <Esc>
inoremap <C-a> <Home>
inoremap <C-e> <End>
inoremap <C-h> <Left>
inoremap <C-l> <Right>

" --- ビジュアルモード ---
vnoremap < <gv
vnoremap > >gv
vnoremap J :move '>+1<CR>gv=gv
vnoremap K :move '<-2<CR>gv=gv
vnoremap p "_dP

" --- コマンドラインモード ---
cnoremap <C-a> <Home>
cnoremap <C-e> <End>
cnoremap <C-p> <Up>
cnoremap <C-n> <Down>
" }}}

" {{{ 10. Autocmd
augroup vimrc_filetypes
  autocmd!
  autocmd FileType python     setlocal ts=4 sw=4 sts=4 expandtab colorcolumn=88
  autocmd FileType go         setlocal ts=4 sw=4 noexpandtab
  autocmd FileType javascript,typescript setlocal ts=2 sw=2 sts=2 expandtab colorcolumn=100
  autocmd FileType html,css   setlocal ts=2 sw=2 sts=2 expandtab
  autocmd FileType yaml,json  setlocal ts=2 sw=2 sts=2 expandtab
  autocmd FileType make       setlocal noexpandtab ts=4 sw=4
  autocmd FileType markdown   setlocal wrap linebreak spell spelllang=en,cjk
  autocmd FileType vim        setlocal ts=2 sw=2 sts=2 expandtab foldmethod=marker
  autocmd FileType help       nnoremap <buffer> q :q<CR>

  " Python / JS の実行マッピング
  autocmd FileType python     nnoremap <buffer> <Leader>r :!python3 %<CR>
  autocmd FileType javascript nnoremap <buffer> <Leader>r :!node %<CR>
  autocmd FileType sh         nnoremap <buffer> <Leader>r :!bash %<CR>
augroup END

augroup vimrc_general
  autocmd!

  " カーソル位置復元（コミットメッセージは除外）
  autocmd BufReadPost *
    \ if line("'\"") >= 1 && line("'\"") <= line("$") && &ft !~# 'commit' |
    \   exe "normal! g`\"" |
    \ endif

  " 外部で変更されたファイルの自動再読み込み
  autocmd FocusGained,BufEnter * checktime

  " 挿入モードを離れたら paste モードを無効化
  autocmd InsertLeave * set nopaste

  " ウィンドウリサイズ時に均等分割
  autocmd VimResized * wincmd =
augroup END
" }}}

" {{{ 11. Custom Functions & Commands

" 末尾空白の削除
function! s:TrimWhitespace() abort
  let l:save = winsaveview()
  keeppatterns %s/\s\+$//e
  call winrestview(l:save)
  echo "末尾空白を削除しました"
endfunction
command! TrimWhitespace call s:TrimWhitespace()
nnoremap <Leader>tw :TrimWhitespace<CR>

" 行番号モードのトグル
function! s:ToggleNumber() abort
  if &number && &relativenumber
    set nonumber norelativenumber
    echo "行番号: OFF"
  elseif &relativenumber
    set number
    echo "行番号: ハイブリッド"
  elseif &number
    set nonumber relativenumber
    echo "行番号: 相対"
  else
    set number norelativenumber
    echo "行番号: 絶対"
  endif
endfunction
command! ToggleNumber call s:ToggleNumber()
nnoremap <Leader>tn :ToggleNumber<CR>

" Quickfix トグル
function! s:ToggleQuickfix() abort
  let l:nr = winnr('$')
  cclose
  if l:nr == winnr('$')
    copen
  endif
endfunction
command! ToggleQuickfix call s:ToggleQuickfix()
nnoremap <Leader>cc :ToggleQuickfix<CR>

" スクラッチバッファ
function! s:ScratchBuffer() abort
  enew
  setlocal buftype=nofile bufhidden=wipe nobuflisted noswapfile
  echo "スクラッチバッファを作成しました"
endfunction
command! ScratchBuffer call s:ScratchBuffer()
nnoremap <Leader>sc :ScratchBuffer<CR>
" }}}

" {{{ 12. Plugin Config

" --- fzf.vim ---
if isdirectory(s:vim_dir . '/plugged/fzf.vim')
  nnoremap <Leader>f  :Files<CR>
  nnoremap <Leader>b  :Buffers<CR>
  nnoremap <Leader>rg :Rg<Space>
  nnoremap <Leader>l  :Lines<CR>
  nnoremap <Leader>h  :History<CR>
endif

" --- vim-gitgutter ---
let g:gitgutter_sign_added    = '+'
let g:gitgutter_sign_modified = '~'
let g:gitgutter_sign_removed  = '-'
nnoremap ]g :GitGutterNextHunk<CR>
nnoremap [g :GitGutterPrevHunk<CR>

" --- netrw ---
let g:netrw_banner    = 0
let g:netrw_liststyle = 3
let g:netrw_winsize   = 25
" }}}
```

**初心者向けとの違い:**
- OS 検出と Vim ディレクトリの自動判定で Windows / Linux / macOS すべてに対応
- vim-plug のインストールスクリプトも OS 別に対応（curl / PowerShell）
- `<expr>` マッピングでカウント付きの j/k を論理行移動に最適化
- `U` を Redo にリマップして直感的な操作を実現
- `VimResized` でウィンドウリサイズ時に自動均等分割
- `InsertLeave` で paste モードを自動解除
- Quickfix トグル、スクラッチバッファなど実用的な関数を完備
- プラグインの存在チェックでプラグイン未インストール時もエラーなく動作
- Git hunk ナビゲーション（`]g` / `[g`）で差分の確認が効率的に
- モード表示付きカスタムステータスラインで `lightline` 等のプラグインが不要
- 7つのファイルタイプと3つの実行マッピングで多言語開発に対応

</details>

# 実践課題11：プラグイン管理と dotfiles ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第1章（vimrcの基本と仕組み）、第6章（autocmdとファイルタイプ別設定）、第8章（実践的なvimrc構築）
> **課題の種類**: ミニプロジェクト
> **学習目標**: vim-plug を使ったプラグイン管理と、Git で dotfiles を管理する仕組みを構築できるようになる

---

## 完成イメージ

```
┌──────────────────────────────────────────────────────────┐
│  プラグイン管理とdotfiles 管理の目標                       │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ~/.vim/                                                  │
│  ├── vimrc              ← メインの設定ファイル            │
│  ├── autoload/                                            │
│  │   └── plug.vim       ← vim-plug 本体                  │
│  ├── plugged/           ← インストールされたプラグイン    │
│  │   ├── gruvbox/                                        │
│  │   ├── vim-commentary/                                 │
│  │   └── ...                                             │
│  ├── ftplugin/          ← ファイルタイプ別設定            │
│  │   ├── python.vim                                      │
│  │   └── javascript.vim                                  │
│  ├── undodir/           ← 永続 Undo ファイル              │
│  └── .gitignore         ← plugged/ と undodir/ を除外    │
│                                                           │
│  Git で管理 → 別のマシンで git clone するだけで環境復元   │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## 課題の要件

### Part 1: vim-plug によるプラグイン管理
1. vim-plug の自動インストール処理を vimrc に記述する
2. 以下のプラグインを `Plug` コマンドで登録する
   - カラースキーム（例: `gruvbox`）
   - コメント操作（例: `vim-commentary`）
   - ファジーファインダー（例: `fzf.vim`）
3. 各プラグインの基本設定を記述する
4. `:PlugInstall` でプラグインをインストールできることを確認する

### Part 2: ディレクトリ構成の整理
1. `~/.vim/vimrc` をメイン設定ファイルとして配置する
2. `~/.vim/ftplugin/` にファイルタイプ別の設定を分離する
3. `~/.vim/undodir/` を永続 Undo 用ディレクトリとして設定する

### Part 3: Git による dotfiles 管理
1. `~/.vim/` ディレクトリを Git リポジトリとして初期化する
2. `.gitignore` で `plugged/` と `undodir/` を除外する
3. 別のマシンで環境を再構築する手順を理解する

---

## ステップガイド

<details>
<summary>ステップ1：vim-plug の自動インストールを記述する</summary>

vim-plug がまだインストールされていない場合に、自動的にダウンロードする処理です。

```vim
" vim-plug の自動インストール
let s:plug_path = expand('~/.vim/autoload/plug.vim')
if !filereadable(s:plug_path)
  echo "vim-plug をインストールしています..."
  silent execute '!curl -fLo ' . s:plug_path . ' --create-dirs '
    \ . 'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif
```

この処理により、新しいマシンで vimrc をコピーするだけで vim-plug が自動インストールされます。

</details>

<details>
<summary>ステップ2：プラグインを登録する</summary>

`call plug#begin()` と `call plug#end()` の間にプラグインを登録します。

```vim
call plug#begin('~/.vim/plugged')

" カラースキーム
Plug 'morhetz/gruvbox'

" コメント操作（gcc でコメントトグル）
Plug 'tpope/vim-commentary'

" 囲み文字操作（cs"' で " を ' に変更など）
Plug 'tpope/vim-surround'

" ファジーファインダー
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'

call plug#end()
```

</details>

<details>
<summary>ステップ3：プラグインの設定を記述する</summary>

```vim
" --- gruvbox ---
set background=dark
colorscheme gruvbox

" --- fzf.vim ---
nnoremap <Leader>f :Files<CR>
nnoremap <Leader>b :Buffers<CR>
nnoremap <Leader>rg :Rg<Space>
```

`colorscheme` は `plug#end()` の後に記述する必要があります。`plug#end()` がプラグインの `runtimepath` を設定するためです。

</details>

<details>
<summary>ステップ4：ftplugin でファイルタイプ別設定を分離する</summary>

```bash
# ディレクトリを作成
mkdir -p ~/.vim/ftplugin
```

`~/.vim/ftplugin/python.vim` を作成します。

```vim
" ~/.vim/ftplugin/python.vim
setlocal tabstop=4 shiftwidth=4 softtabstop=4 expandtab
setlocal colorcolumn=88
setlocal textwidth=88
nnoremap <buffer> <Leader>r :!python3 %<CR>
```

</details>

<details>
<summary>ステップ5：Git で管理する</summary>

```bash
# Git リポジトリとして初期化
cd ~/.vim
git init

# .gitignore を作成
cat > .gitignore << 'EOF'
plugged/
undodir/
*.swp
*.swo
*~
EOF

# 初回コミット
git add -A
git commit -m "Initial vimrc setup"

# GitHub にプッシュ（リモートリポジトリを作成済みの場合）
# git remote add origin https://github.com/username/dotfiles-vim.git
# git push -u origin main
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

**~/.vim/vimrc:**

```vim
" ============================================================
" vimrc - プラグイン管理版
" ============================================================

" --- vim-plug 自動インストール ---
let s:plug_path = expand('~/.vim/autoload/plug.vim')
if !filereadable(s:plug_path)
  echo "vim-plug をインストールしています..."
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

" --- 表示設定 ---
syntax enable
filetype plugin indent on
set number
set cursorline
set laststatus=2
set showcmd

" --- カラースキーム ---
set background=dark
silent! colorscheme gruvbox

" --- インデント ---
set tabstop=2 shiftwidth=2 softtabstop=2 expandtab
set autoindent

" --- 検索 ---
set hlsearch incsearch
set ignorecase smartcase

" --- 操作 ---
set backspace=indent,eol,start
set belloff=all
set hidden
set confirm

" --- バックアップ ---
set nobackup noswapfile nowritebackup
set undofile
if !isdirectory(expand('~/.vim/undodir'))
  call mkdir(expand('~/.vim/undodir'), 'p')
endif
set undodir=~/.vim/undodir

" --- マッピング ---
let mapleader = "\<Space>"
nnoremap <Leader>w :w<CR>
nnoremap <Leader>q :q<CR>
nnoremap <Esc><Esc> :nohlsearch<CR>
```

**~/.vim/.gitignore:**

```
plugged/
undodir/
*.swp
*.swo
*~
```

</details>

<details>
<summary>解答例（改良版 ─ 完全な dotfiles 構成）</summary>

**~/.vim/vimrc:**

```vim
" ============================================================
" vimrc - Complete Configuration with Plugin Management
" ============================================================

" {{{ 1. vim-plug Bootstrap
let s:plug_path = expand('~/.vim/autoload/plug.vim')
if !filereadable(s:plug_path)
  silent execute '!curl -fLo ' . s:plug_path . ' --create-dirs '
    \ . 'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif
" }}}

" {{{ 2. Plugins
call plug#begin('~/.vim/plugged')

  " --- テーマ ---
  Plug 'morhetz/gruvbox'

  " --- 編集支援 ---
  Plug 'tpope/vim-commentary'       " gcc でコメントトグル
  Plug 'tpope/vim-surround'         " cs"' で囲み文字変更
  Plug 'tpope/vim-repeat'           " . で surround 等の操作を繰り返し
  Plug 'jiangmiao/auto-pairs'       " 括弧の自動補完

  " --- ファイル操作 ---
  Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
  Plug 'junegunn/fzf.vim'

  " --- Git ---
  Plug 'airblade/vim-gitgutter'     " 変更行にマーク表示

call plug#end()
" }}}

" {{{ 3. General Settings
set nocompatible
set encoding=utf-8
scriptencoding utf-8
set fileencoding=utf-8
set fileencodings=utf-8,cp932,euc-jp

let mapleader = "\<Space>"
set hidden
set confirm
set autoread
set updatetime=300
set timeoutlen=500
set backspace=indent,eol,start
set belloff=all
" }}}

" {{{ 4. Display
syntax enable
filetype plugin indent on

set number relativenumber
set cursorline
set signcolumn=yes
set scrolloff=8
set laststatus=2
set showcmd
set noshowmode
set wrap linebreak

set list
set listchars=tab:▸\ ,trail:·,extends:>,precedes:<

if has('termguicolors')
  let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum"
  let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum"
  set termguicolors
endif

set background=dark
silent! colorscheme gruvbox

set statusline=
set statusline+=\ %f\ %m%r
set statusline+=\ [%{&fenc!=''?&fenc:&enc}/%{&ff}]
set statusline+=%=
set statusline+=\ %Y\ \|\ %l:%c\ %p%%\
" }}}

" {{{ 5. Indent
set tabstop=2 shiftwidth=2 softtabstop=2
set expandtab smarttab
set autoindent
set shiftround
" }}}

" {{{ 6. Search
set hlsearch incsearch
set ignorecase smartcase
set wrapscan

if executable('rg')
  set grepprg=rg\ --vimgrep\ --smart-case
  set grepformat=%f:%l:%c:%m
endif
" }}}

" {{{ 7. Backup / Undo
set nobackup noswapfile nowritebackup
set undofile
if !isdirectory(expand('~/.vim/undodir'))
  call mkdir(expand('~/.vim/undodir'), 'p')
endif
set undodir=~/.vim/undodir

if has('unnamedplus')
  set clipboard=unnamedplus
else
  set clipboard=unnamed
endif

set wildmenu
set wildmode=list:longest,full
" }}}

" {{{ 8. Key Mappings
nnoremap Y y$
nnoremap <expr> j v:count == 0 ? 'gj' : 'j'
nnoremap <expr> k v:count == 0 ? 'gk' : 'k'
nnoremap n nzzzv
nnoremap N Nzzzv

inoremap jj <Esc>

vnoremap < <gv
vnoremap > >gv
vnoremap J :move '>+1<CR>gv=gv
vnoremap K :move '<-2<CR>gv=gv

nnoremap <Leader>w :w<CR>
nnoremap <Leader>q :q<CR>
nnoremap <Leader>/ :nohlsearch<CR>
nnoremap <Leader>e :Explore<CR>

nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l
" }}}

" {{{ 9. Plugin Config

" --- fzf.vim ---
nnoremap <Leader>f :Files<CR>
nnoremap <Leader>b :Buffers<CR>
nnoremap <Leader>rg :Rg<Space>
nnoremap <Leader>l :Lines<CR>

" --- vim-gitgutter ---
set updatetime=100
let g:gitgutter_sign_added = '+'
let g:gitgutter_sign_modified = '~'
let g:gitgutter_sign_removed = '-'
" }}}

" {{{ 10. Autocmd
augroup vimrc_autocmd
  autocmd!

  autocmd BufReadPost *
    \ if line("'\"") >= 1 && line("'\"") <= line("$") && &ft !~# 'commit' |
    \   exe "normal! g`\"" |
    \ endif

  autocmd FocusGained,BufEnter * checktime
augroup END
" }}}
```

**~/.vim/ftplugin/python.vim:**

```vim
setlocal tabstop=4 shiftwidth=4 softtabstop=4 expandtab
setlocal colorcolumn=88
setlocal textwidth=88
nnoremap <buffer> <Leader>r :!python3 %<CR>
nnoremap <buffer> <Leader>p oprint(f"DEBUG: {}")<Esc>F}i
```

**~/.vim/ftplugin/javascript.vim:**

```vim
setlocal tabstop=2 shiftwidth=2 softtabstop=2 expandtab
setlocal colorcolumn=100
nnoremap <buffer> <Leader>l oconsole.log();<Esc>F(a
```

**~/.vim/.gitignore:**

```
# プラグインはインストール時に取得するため除外
plugged/

# Undo 履歴はマシン固有のため除外
undodir/

# Vim のテンポラリファイル
*.swp
*.swo
*~
.netrwhist
```

**環境の復元手順（README.md に記載する内容）:**

```bash
# 1. リポジトリをクローン
git clone https://github.com/username/dotfiles-vim.git ~/.vim

# 2. シンボリックリンクを作成（~/.vimrc が必要な場合）
ln -s ~/.vim/vimrc ~/.vimrc

# 3. Vim を起動する（vim-plug が自動インストールされ、プラグインも自動取得される）
vim
```

**初心者向けとの違い:**
- 折りたたみマーカーによるセクション構成で見通しの良い構造
- `vim-repeat`, `auto-pairs`, `vim-gitgutter` など実用的なプラグインを追加
- ftplugin による設定分離で vimrc の肥大化を防止
- `.gitignore` に除外理由をコメントで記載
- 環境復元手順を明記し、ポータブルな設定を実現

</details>

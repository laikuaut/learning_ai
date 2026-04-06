# 実践課題09：リファクタリング ─ レガシー vimrc ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第1章〜第7章（vimrc の基本設定、表示、インデント、検索、キーマッピング、autocmd、関数とカスタムコマンド）
> **課題の種類**: リファクタリング
> **学習目標**: 古い書き方や非効率な構成の vimrc を、モダンなベストプラクティスに沿って整理・改善する力を養う

---

## 課題の説明

以下の vimrc は長年にわたって継ぎ足しで追加された「レガシー vimrc」です。
動作はしますが、多くの問題があります。以下の観点でリファクタリングしてください。

### リファクタリングの観点

1. **構成の整理**: セクション分けとコメントの追加
2. **非推奨の書き方の修正**: `map` → `noremap` 系への変更
3. **重複・矛盾の解消**: 矛盾する設定や無意味な設定の除去
4. **autocmd の安全化**: `augroup` による重複防止
5. **可搬性の向上**: 環境依存部分に条件分岐を追加
6. **関数化**: 繰り返しロジックの関数への切り出し

---

## リファクタリング対象の vimrc

```vim
set nocompatible
syntax on
set number
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab
set autoindent
set smartindent
filetype on
filetype plugin on
filetype indent on
set hlsearch
set incsearch
set ignorecase
set smartcase
set ruler
set showcmd
set showmatch
set laststatus=2
set encoding=utf-8
set fileencoding=utf-8
set backspace=indent,eol,start
set belloff=all

" move
map j gj
map k gk

" save
map <C-s> :w<CR>
imap <C-s> <Esc>:w<CR>a

" jj to exit insert mode
imap jj <Esc>

" window
map <C-h> <C-w>h
map <C-j> <C-w>j
map <C-k> <C-w>k
map <C-l> <C-w>l

" tab
set tabstop=2
set shiftwidth=2

" statusline
set statusline=%f\ %m%r%h%w%=%l/%L\ %c\ %p%%

nmap Y y$
nmap <Space>w :w<CR>
nmap <Space>q :q<CR>
vmap < <gv
vmap > >gv

" search
nmap <Space>/ :nohlsearch<CR>

" python
autocmd FileType python setlocal tabstop=4
autocmd FileType python setlocal shiftwidth=4
autocmd FileType python setlocal expandtab
autocmd FileType python setlocal colorcolumn=79

" javascript
autocmd FileType javascript setlocal tabstop=2
autocmd FileType javascript setlocal shiftwidth=2
autocmd FileType javascript setlocal expandtab

" html
autocmd FileType html setlocal tabstop=2
autocmd FileType html setlocal shiftwidth=2
autocmd FileType html setlocal expandtab

autocmd FileType make setlocal noexpandtab

" cursor restore
autocmd BufReadPost * if line("'\"") > 0 && line("'\"") <= line("$") | exe "normal! g'\"" | endif

set undofile
set undodir=~/.vim/undodir

set clipboard=unnamed

let g:netrw_banner = 0
let g:netrw_liststyle = 3

set cursorline
set scrolloff=5
set list
set listchars=tab:>-,trail:.

set nobackup
set noswapfile
set nowritebackup

set wildmenu
set wildmode=list:longest,full

set wrap
set linebreak
```

---

## 発見すべき問題点

<details>
<summary>ヒント：問題点の一覧（11個）</summary>

| # | 問題 | カテゴリ |
|---|------|---------|
| 1 | `map` / `nmap` / `imap` / `vmap` を使っている（再帰マッピング） | 非推奨 |
| 2 | `filetype on` → `filetype plugin on` → `filetype indent on` が冗長 | 重複 |
| 3 | `set tabstop=4` の後に `set tabstop=2` があり矛盾している | 矛盾 |
| 4 | `Leader` キーが設定されていないのに `<Space>` を直接使っている | 非推奨 |
| 5 | autocmd が `augroup` で囲まれていない | 安全性 |
| 6 | autocmd FileType で同じファイルタイプの設定が分散している | 重複 |
| 7 | `undodir` のディレクトリ存在チェックがない | 可搬性 |
| 8 | `syntax on` より `syntax enable` の方が推奨される | 非推奨 |
| 9 | セクション分けやコメントが不十分 | 構成 |
| 10 | `set clipboard=unnamed` は OS によって `unnamedplus` にすべき | 可搬性 |
| 11 | 設定の順序がバラバラ（`cursorline` が最後の方にある等） | 構成 |

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け ─ 最低限の修正）</summary>

最低限の問題を修正した「安全なバージョン」です。

```vim
" ==================================================
" 基本設定
" ==================================================
set nocompatible
set encoding=utf-8
set fileencoding=utf-8

" ==================================================
" 表示設定
" ==================================================
syntax enable
filetype plugin indent on

set number
set cursorline
set ruler
set showcmd
set showmatch
set scrolloff=5
set wrap
set linebreak

set list
set listchars=tab:>-,trail:.

" ステータスライン
set laststatus=2
set statusline=%f\ %m%r%h%w%=%l/%L\ %c\ %p%%

" ==================================================
" インデント設定
" ==================================================
set tabstop=2
set shiftwidth=2
set softtabstop=2
set expandtab
set autoindent
set smartindent

" ==================================================
" 検索設定
" ==================================================
set hlsearch
set incsearch
set ignorecase
set smartcase

" ==================================================
" 操作設定
" ==================================================
set backspace=indent,eol,start
set belloff=all
set hidden
set confirm
set wildmenu
set wildmode=list:longest,full
set clipboard=unnamed

" ==================================================
" バックアップ・スワップ・Undo
" ==================================================
set nobackup
set noswapfile
set nowritebackup
set undofile
set undodir=~/.vim/undodir

" ==================================================
" キーマッピング
" ==================================================
let mapleader = "\<Space>"

" Y で行末までヤンク
nnoremap Y y$

" 表示行単位で移動
nnoremap j gj
nnoremap k gk

" jj でノーマルモードに戻る
inoremap jj <Esc>

" Ctrl+s で保存
nnoremap <C-s> :w<CR>
inoremap <C-s> <Esc>:w<CR>a

" Leader マッピング
nnoremap <Leader>w :w<CR>
nnoremap <Leader>q :q<CR>
nnoremap <Leader>/ :nohlsearch<CR>

" ウィンドウ間移動
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" インデント後に選択を維持
vnoremap < <gv
vnoremap > >gv

" ==================================================
" ファイルタイプ別設定
" ==================================================
augroup MyFileTypes
  autocmd!
  autocmd FileType python setlocal tabstop=4 shiftwidth=4 softtabstop=4 expandtab colorcolumn=79
  autocmd FileType javascript,html setlocal tabstop=2 shiftwidth=2 softtabstop=2 expandtab
  autocmd FileType make setlocal noexpandtab
augroup END

" カーソル位置復元
augroup RestoreCursor
  autocmd!
  autocmd BufReadPost *
    \ if line("'\"") > 0 && line("'\"") <= line("$") |
    \   exe "normal! g'\"" |
    \ endif
augroup END

" ==================================================
" プラグイン設定
" ==================================================
let g:netrw_banner = 0
let g:netrw_liststyle = 3
```

</details>

<details>
<summary>解答例（改良版 ─ 完全にモダン化）</summary>

```vim
" ============================================================
" vimrc - リファクタリング完了版
" ============================================================

" {{{ 1. 基本設定
set nocompatible
set encoding=utf-8
scriptencoding utf-8
set fileencoding=utf-8
set fileencodings=utf-8,cp932,euc-jp
" }}}

" {{{ 2. 表示設定
syntax enable
filetype plugin indent on

set number relativenumber
set cursorline
set signcolumn=yes
set ruler
set showcmd
set showmatch
set scrolloff=8
set sidescrolloff=8
set wrap
set linebreak
set display=lastline

" 不可視文字
set list
set listchars=tab:▸\ ,trail:·,extends:>,precedes:<

" True Color 対応
if has('termguicolors')
  let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum"
  let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum"
  set termguicolors
endif

" ステータスライン
set laststatus=2
set noshowmode
set statusline=
set statusline+=\ %f\ %m%r%h%w
set statusline+=\ [%{&fenc!=''?&fenc:&enc}/%{&ff}]
set statusline+=%=
set statusline+=\ %Y\ \|\ %l:%c\ %p%%\
" }}}

" {{{ 3. インデント設定
set tabstop=2
set shiftwidth=2
set softtabstop=2
set expandtab
set smarttab
set autoindent
set shiftround
" }}}

" {{{ 4. 検索設定
set hlsearch
set incsearch
set ignorecase
set smartcase
set wrapscan

if executable('rg')
  set grepprg=rg\ --vimgrep\ --smart-case
  set grepformat=%f:%l:%c:%m
endif
" }}}

" {{{ 5. 操作設定
set backspace=indent,eol,start
set belloff=all
set hidden
set confirm
set autoread
set updatetime=300
set timeoutlen=500
set wildmenu
set wildmode=list:longest,full
set completeopt=menuone,noinsert,noselect

" クリップボード（OS 別に対応）
if has('unnamedplus')
  set clipboard=unnamedplus
else
  set clipboard=unnamed
endif
" }}}

" {{{ 6. バックアップ・スワップ・Undo
set nobackup
set noswapfile
set nowritebackup
set undofile
if !isdirectory(expand('~/.vim/undodir'))
  call mkdir(expand('~/.vim/undodir'), 'p')
endif
set undodir=~/.vim/undodir
" }}}

" {{{ 7. キーマッピング
let mapleader = "\<Space>"
let maplocalleader = ","

" --- ノーマルモード ---
nnoremap Y y$
nnoremap <expr> j v:count == 0 ? 'gj' : 'j'
nnoremap <expr> k v:count == 0 ? 'gk' : 'k'
nnoremap n nzzzv
nnoremap N Nzzzv

nnoremap <Leader>w :w<CR>
nnoremap <Leader>q :q<CR>
nnoremap <Leader>/ :nohlsearch<CR>
nnoremap <Leader>e :Explore<CR>

nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" --- 挿入モード ---
inoremap jj <Esc>
inoremap <C-s> <Esc>:w<CR>a

" --- ビジュアルモード ---
vnoremap < <gv
vnoremap > >gv
vnoremap J :move '>+1<CR>gv=gv
vnoremap K :move '<-2<CR>gv=gv
vnoremap p "_dP

" --- コマンドラインモード ---
cnoremap <C-a> <Home>
cnoremap <C-e> <End>
" }}}

" {{{ 8. ファイルタイプ別設定
augroup vimrc_filetypes
  autocmd!
  autocmd FileType python     setlocal ts=4 sw=4 sts=4 expandtab colorcolumn=88
  autocmd FileType javascript setlocal ts=2 sw=2 sts=2 expandtab
  autocmd FileType typescript setlocal ts=2 sw=2 sts=2 expandtab
  autocmd FileType html,css   setlocal ts=2 sw=2 sts=2 expandtab
  autocmd FileType make       setlocal noexpandtab ts=4 sw=4
  autocmd FileType yaml       setlocal ts=2 sw=2 sts=2 expandtab
  autocmd FileType help       nnoremap <buffer> q :q<CR>
augroup END
" }}}

" {{{ 9. 自動コマンド
augroup vimrc_autocmd
  autocmd!

  " カーソル位置復元（コミットメッセージは除外）
  autocmd BufReadPost *
    \ if line("'\"") >= 1 && line("'\"") <= line("$") && &ft !~# 'commit' |
    \   exe "normal! g`\"" |
    \ endif

  " 外部で変更されたファイルの自動再読み込み
  autocmd FocusGained,BufEnter * checktime

  " 保存時に末尾空白を自動削除
  autocmd BufWritePre * call s:TrimWhitespace()
augroup END

function! s:TrimWhitespace() abort
  let l:save = winsaveview()
  keeppatterns %s/\s\+$//e
  call winrestview(l:save)
endfunction
command! TrimWhitespace call s:TrimWhitespace()
" }}}

" {{{ 10. プラグイン設定
let g:netrw_banner = 0
let g:netrw_liststyle = 3
let g:netrw_winsize = 25
" }}}
```

**元の vimrc からの主な改善点:**
- `map` / `nmap` / `imap` / `vmap` を全て `noremap` 系に統一し、再帰マッピングのリスクを排除
- `filetype on` + `filetype plugin on` + `filetype indent on` を `filetype plugin indent on` の1行に統合
- `tabstop=4` と `tabstop=2` の矛盾を解消（デフォルト2、Python のみ4に統一）
- `<Space>` 直接使用を `let mapleader` + `<Leader>` に変更
- 全 autocmd を `augroup` で囲み、重複登録を防止
- 同じファイルタイプの分散した設定を1行にまとめて簡潔化
- `undodir` の存在チェックと自動作成を追加
- `syntax on` を `syntax enable` に変更（カスタムカラーを保持）
- `clipboard` を `has('unnamedplus')` で OS 別に自動判定
- 折りたたみマーカーでセクション構成を明確化
- `scrolloff`, `signcolumn`, `termguicolors` など実用的な設定を追加
- 末尾空白の自動削除関数を追加

</details>

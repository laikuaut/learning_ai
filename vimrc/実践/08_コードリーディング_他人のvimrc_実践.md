# 実践課題08：コードリーディング ─ 他人の vimrc ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第1章〜第7章（vimrc の基本設定、表示、インデント、検索、キーマッピング、autocmd、関数とカスタムコマンド）
> **課題の種類**: コードリーディング
> **学習目標**: 他人が書いた vimrc を読み解き、各設定の意図・処理の流れ・設計判断を理解する力を養う

---

## 課題の説明

以下の vimrc は、あるベテランエンジニアが実際に使っている設定ファイルです。
コードを読んで、後に続く **10個の設問** に答えてください。

**Vim で実行する必要はありません。コードを読んで理解する力を鍛える課題です。**

---

## 読解対象の vimrc

```vim
" ============================================================
" ~/.vimrc - Vim configuration
" Author: senior_dev
" Last Updated: 2025-01-15
" ============================================================

" {{{ 1. Bootstrap
set nocompatible
set encoding=utf-8
scriptencoding utf-8

if has('vim_starting')
  set runtimepath+=~/.vim/plugged/vim-plug
  if !isdirectory(expand('~/.vim/plugged/vim-plug'))
    echo "Installing vim-plug..."
    call system('git clone https://github.com/junegunn/vim-plug.git ~/.vim/plugged/vim-plug/autoload')
  endif
endif
" }}}

" {{{ 2. General Settings
let mapleader = "\<Space>"
let maplocalleader = ","

set hidden
set confirm
set autoread
set updatetime=300
set timeoutlen=500

set nobackup
set nowritebackup
set noswapfile
set undofile
if !isdirectory(expand('~/.vim/undodir'))
  call mkdir(expand('~/.vim/undodir'), 'p')
endif
set undodir=~/.vim/undodir
" }}}

" {{{ 3. Display
set number relativenumber
set cursorline
set signcolumn=yes
set scrolloff=8
set sidescrolloff=8
set laststatus=2
set noshowmode
set shortmess+=c

syntax enable
filetype plugin indent on

if has('termguicolors')
  let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum"
  let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum"
  set termguicolors
endif

set statusline=
set statusline+=\ %{g:mode_map[mode()]}
set statusline+=\ \|\ %f\ %m%r
set statusline+=%=
set statusline+=\ %{&ft!=''?&ft:'none'}
set statusline+=\ \|\ %{&fenc!=''?&fenc:&enc}
set statusline+=\ \|\ %l:%c\ %p%%\

let g:mode_map = {
  \ 'n': 'NORMAL', 'i': 'INSERT', 'v': 'VISUAL',
  \ 'V': 'V-LINE', "\<C-v>": 'V-BLOCK',
  \ 'c': 'COMMAND', 'R': 'REPLACE', 't': 'TERMINAL'
  \ }
" }}}

" {{{ 4. Search
set hlsearch incsearch
set ignorecase smartcase
set wrapscan

if executable('rg')
  set grepprg=rg\ --vimgrep\ --smart-case\ --hidden
  set grepformat=%f:%l:%c:%m
endif
" }}}

" {{{ 5. Indent
set tabstop=2 shiftwidth=2 softtabstop=2
set expandtab smarttab
set autoindent
set shiftround
" }}}

" {{{ 6. Key Mappings
nnoremap Y y$
nnoremap <expr> j v:count == 0 ? 'gj' : 'j'
nnoremap <expr> k v:count == 0 ? 'gk' : 'k'
nnoremap n nzzzv
nnoremap N Nzzzv

inoremap jk <Esc>
inoremap <C-a> <Home>
inoremap <C-e> <End>

vnoremap < <gv
vnoremap > >gv
vnoremap J :move '>+1<CR>gv=gv
vnoremap K :move '<-2<CR>gv=gv
vnoremap p "_dP

nnoremap <Leader>w :w<CR>
nnoremap <Leader>q :q<CR>
nnoremap <Leader>e :Explore<CR>
nnoremap <Leader>/ :nohlsearch<CR>

nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l
nnoremap <Leader>v :vsplit<CR>
nnoremap <Leader>s :split<CR>
" }}}

" {{{ 7. Autocmd
augroup vimrc_autocmd
  autocmd!

  autocmd FileType python setlocal ts=4 sw=4 sts=4 colorcolumn=88
  autocmd FileType go     setlocal ts=4 sw=4 noexpandtab
  autocmd FileType make   setlocal ts=4 sw=4 noexpandtab
  autocmd FileType yaml   setlocal ts=2 sw=2 sts=2

  autocmd FileType help nnoremap <buffer> q :q<CR>

  autocmd BufReadPost *
    \ if line("'\"") >= 1 && line("'\"") <= line("$") && &ft !~# 'commit' |
    \   exe "normal! g`\"" |
    \ endif

  autocmd TextYankPost *
    \ if has('##TextYankPost') |
    \   silent! lua vim.highlight.on_yank({timeout=200}) |
    \ endif

  autocmd FocusGained,BufEnter * checktime
augroup END
" }}}

" {{{ 8. Custom Functions
function! s:TrimWhitespace() abort
  let l:save = winsaveview()
  keeppatterns %s/\s\+$//e
  call winrestview(l:save)
endfunction

command! TrimWhitespace call s:TrimWhitespace()
nnoremap <Leader>tw :TrimWhitespace<CR>

function! s:ToggleQuickfix() abort
  let l:nr = winnr('$')
  cclose
  if l:nr == winnr('$')
    copen
  endif
endfunction

command! ToggleQuickfix call s:ToggleQuickfix()
nnoremap <Leader>cc :ToggleQuickfix<CR>
" }}}
```

---

## 設問

以下の10問に答えてください。各設問について、vimrc のどの部分が根拠になるかも示してください。

### 問1（基本理解）
`{{{ ... }}}` で囲まれたコメントは何のために使われていますか？ Vim のどの機能と関連していますか？

### 問2（Bootstrap セクション）
`has('vim_starting')` の条件分岐は何を判定していますか？ なぜこの条件が必要ですか？

### 問3（General Settings）
`set hidden` と `set confirm` を組み合わせている理由を説明してください。どちらか一方だけではどのような問題がありますか？

### 問4（Display セクション）
`&t_8f` と `&t_8b` に設定されている `\<Esc>[38;2;%lu;%lu;%lum` は何ですか？ なぜ `termguicolors` の前に設定していますか？

### 問5（ステータスライン）
`set noshowmode` を設定している理由を、ステータスラインの定義と照らし合わせて説明してください。

### 問6（Key Mappings）
`nnoremap <expr> j v:count == 0 ? 'gj' : 'j'` の動作を具体例を挙げて説明してください。`5j` と素の `j` でどう挙動が変わりますか？

### 問7（Key Mappings）
`vnoremap p "_dP` は何をしていますか？ このマッピングがない場合にどのような不便が生じますか？

### 問8（Autocmd セクション）
カーソル位置復元の autocmd で `&ft !~# 'commit'` という条件が付いている理由を説明してください。

### 問9（Custom Functions）
`s:TrimWhitespace()` 関数で `winsaveview()` と `winrestview()` を使っている理由を説明してください。これらを省略するとどうなりますか？

### 問10（設計判断）
この vimrc 全体を通して、著者が意識している設計原則を3つ挙げてください。具体的な設定を根拠として示してください。

---

## 解答例

<details>
<summary>問1の解答</summary>

`{{{ ... }}}` は Vim の**折りたたみマーカー**（fold marker）です。`set foldmethod=marker` を設定すると、`{{{` と `}}}` で囲まれた範囲を折りたたむ（fold）ことができます。

これにより、長い vimrc をセクション単位で折りたたんで見通しをよくできます。`zo` で展開、`zc` で折りたたみ、`zM` で全折りたたみ、`zR` で全展開ができます。

</details>

<details>
<summary>問2の解答</summary>

`has('vim_starting')` は、**Vim が起動処理中かどうか**を判定します。`:source ~/.vimrc` での再読み込み時には `false` になります。

これにより、vim-plug のインストール確認とクローンは**Vim の初回起動時のみ**実行され、`:source` での再読み込み時には実行されません。毎回 Git の存在確認をすることを避け、再読み込みを高速に保つための工夫です。

</details>

<details>
<summary>問3の解答</summary>

- `set hidden` は、バッファが変更されていても保存せずに他のバッファに切り替えられるようにします
- `set confirm` は、保存されていないバッファを閉じようとした時に確認ダイアログを出します

**`hidden` だけの場合**: 変更を保存し忘れたまま Vim を終了してしまうリスクがあります。
**`confirm` だけの場合**: バッファを切り替えるたびに保存を要求され、作業のテンポが悪くなります。

両方を組み合わせることで、「作業中は自由に切り替えられるが、終了時には確認が入る」という安全かつ効率的な動作になります。

</details>

<details>
<summary>問4の解答</summary>

`\<Esc>[38;2;%lu;%lu;%lum` は **ANSI エスケープシーケンス**で、ターミナルに True Color（24ビットカラー）を指示するための制御コードです。

- `t_8f`: 前景色（foreground）の制御シーケンス
- `t_8b`: 背景色（background）の制御シーケンス
- `38;2` は前景色、`48;2` は背景色を表す SGR パラメータです
- `%lu` は赤・緑・青の各値が入るプレースホルダーです

**`termguicolors` の前に設定する理由**: `termguicolors` を有効にすると、Vim はこれらのエスケープシーケンスを使って色を出力します。シーケンスが正しく設定されていない状態で `termguicolors` を有効にすると、ターミナルによっては色が崩れます。

</details>

<details>
<summary>問5の解答</summary>

`set noshowmode` は、Vim のデフォルト動作である「画面下部に `-- INSERT --` などのモード表示」を無効にします。

この vimrc では、ステータスラインに `g:mode_map[mode()]` を使って独自にモード名を表示しています（`NORMAL`, `INSERT`, `VISUAL` など）。Vim のデフォルトのモード表示と重複するため、`noshowmode` で片方を無効にしています。

カスタムステータスラインにモード情報を統合することで、表示がスッキリし、ステータスラインの一箇所で全情報を確認できるという利点があります。

</details>

<details>
<summary>問6の解答</summary>

`<expr>` を使ったマッピングは、右辺を**式として評価**して結果をキーとして実行します。

- `v:count` はマッピングの前に入力されたカウント数を保持する特殊変数です
- `v:count == 0` → カウントなし → `gj`（表示行で移動）
- `v:count != 0` → カウントあり → `j`（論理行で移動）

**具体例:**
- 素の `j`: `gj` が実行される。折り返された長い行の中で、画面上の次の行に移動します
- `5j`: 通常の `j` が実行される。論理的な5行下に移動します（`5gj` ではない）

これにより、普段は表示行移動の恩恵を受けつつ、`10j` のような数値指定時は正確に論理行数で移動できます。

</details>

<details>
<summary>問7の解答</summary>

`vnoremap p "_dP` は、ビジュアルモードで選択範囲にペーストする際の動作を改善します。

- `"_d` → 選択範囲をブラックホールレジスタ（`"_`）に削除（ヤンクレジスタを上書きしない）
- `P` → カーソルの前にペースト

**このマッピングがない場合の問題:**
ビジュアルモードで文字列を選択して `p` でペーストすると、ペーストされた内容が**選択されていた文字列で上書き**されます。

例えば、`hello` をヤンクして `world` を選択して `p` すると:
- マッピングなし: `hello` がペーストされるが、ヤンクレジスタが `world` に変わる。もう一度ペーストすると `world` がペーストされてしまう
- マッピングあり: `hello` がペーストされ、ヤンクレジスタは `hello` のまま保持される。何度でも同じ内容をペーストできる

</details>

<details>
<summary>問8の解答</summary>

`&ft !~# 'commit'` は、ファイルタイプが `commit`（Git のコミットメッセージ）でない場合にのみカーソル位置を復元する条件です。

**理由**: `git commit` を実行すると、Vim がコミットメッセージの編集画面を開きます。この時、前回開いた時のカーソル位置（通常はメッセージの途中）に戻ってしまうと、新しいコミットメッセージを書き始める位置がずれて不便です。

コミットメッセージは毎回ファイルの先頭（1行目）から書き始めるのが自然なので、このファイルタイプを除外しています。`!~#` は**大文字小文字を区別する正規表現マッチの否定**です。

</details>

<details>
<summary>問9の解答</summary>

- `winsaveview()` → 現在のウィンドウの状態（カーソル位置、スクロール位置、折りたたみ状態など）を辞書として保存します
- `winrestview()` → 保存した状態を復元します

**省略した場合の問題:**
`%s/\s\+$//e` は置換コマンドです。実行すると:
1. カーソルが最後に置換が行われた位置に移動してしまう
2. 画面のスクロール位置が変わってしまう

つまり、末尾空白を削除する度に「今見ていた場所」から離れてしまいます。`winsaveview()` / `winrestview()` で元の位置を保存・復元することで、ユーザーは末尾空白削除の影響を意識せずに作業を続けられます。

また、`keeppatterns` を使うことで、置換パターンが検索履歴に残ることも防いでいます。

</details>

<details>
<summary>問10の解答</summary>

### 設計原則1: 安全性の確保
- `nnoremap` を一貫して使用し、`nmap` を使っていない（再帰マッピングの回避）
- `augroup ... autocmd! ... augroup END` で autocmd の重複を防止
- `undodir` のディレクトリ自動作成で初回起動時のエラーを防止
- `set confirm` で未保存データの損失を防止

### 設計原則2: 冪等性（べきとうせい）の担保
- `has('vim_starting')` で起動時のみの処理を分離
- `autocmd!` で再読み込み時の重複を防止
- ディレクトリの存在チェック後に `mkdir` するパターン
- これにより `:source ~/.vimrc` を何度実行しても同じ結果になる

### 設計原則3: 段階的な機能強化（graceful degradation）
- `if has('termguicolors')` で True Color 非対応環境でもエラーなく動作
- `if executable('rg')` で ripgrep がない環境でも標準の grep にフォールバック
- `if has('##TextYankPost')` でイベントが使えない古い Vim でもエラーにならない
- 環境を問わず最低限の機能は保証し、対応環境では追加機能を有効にする設計

</details>

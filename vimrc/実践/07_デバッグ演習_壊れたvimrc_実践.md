# 実践課題07：デバッグ演習 ─ 壊れた vimrc ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第1章〜第6章（vimrc の基本設定、表示、インデント、検索、キーマッピング、autocmd）
> **課題の種類**: デバッグ
> **学習目標**: バグだらけの vimrc を読み解き、問題の原因を特定して修正する力を養う

---

## 課題の説明

以下の vimrc には **10個のバグ** が埋め込まれています。
この vimrc を使って Vim を起動すると、エラーが表示されたり意図しない動作になったりします。すべてのバグを見つけて修正してください。

### 進め方

1. 以下のバグ入り vimrc を `~/.vimrc_debug` として保存する
2. `vim -u ~/.vimrc_debug` で読み込んで起動する
3. エラーメッセージや動作を手がかりにバグを特定する
4. 1つずつ修正し、`:source %` で再読み込みして確認する
5. すべての設定が正常に動作すれば完了

---

## バグ入り vimrc

以下のコードをそのまま `~/.vimrc_debug` として保存してください。

```vim
" ==================================================
" 基本設定
" ==================================================
set nocompatible
set encoding=uft-8                    " バグ1
set fileencoding=utf-8

" ==================================================
" 表示設定
" ==================================================
set number
set relativnumber                     " バグ2
set cursorline
syntax enable

" ステータスライン
set laststatus=2
set statusline=%F%m%r%h%w\ [%{&enc}][%{&ff}]%=行:%l/%L\ 列%c\ %p%%

" ==================================================
" インデント設定
" ==================================================
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab
set autoindent
set smartintent                       " バグ3

" ==================================================
" 検索設定
" ==================================================
set hlsearch
set incsearch
set ignorecase
set smartcase

" ==================================================
" キーマッピング
" ==================================================
let mapleader = "\<Space>"

" Y で行末までヤンク
nmap Y y$                             " バグ4

" 表示行単位で移動
nnoremap j gj
nnoremap k gk

" jj でノーマルモードに戻る
nnoremap jj <Esc>                     " バグ5

" Leader + w で保存
nnoremap <Leader>w :w<CR>

" 検索ハイライトを消す
nnoremap <Esc><Esc> :nohlsearch<CR>

" インデント後に選択を維持
vnoremap < <gv
vnoremap > >gv

" ウィンドウ間移動
noremap <C-h> <C-w>h
noremap <C-j> <C-w>j
noremap <C-k> <C-w>k
noremap <C-l> <C-w>l

" ==================================================
" autocmd
" ==================================================
" バグ6: augroup が使われていない
autocmd FileType python setlocal tabstop=4 shiftwidth=4 expandtab
autocmd FileType python setlocal colorcolumn=79
autocmd FileType javascript setlocal tabstop=2 shiftwidth=2 expandtab
autocmd FileType make setlocal noexpandtab

" カーソル位置復元
autocmd BufReadPost *
  \ if line("'\"") > 0 && line("'\"") <= line("$")
  \   exe "normal! g'\""
  \ endif                             " バグ7

" ==================================================
" netrw 設定
" ==================================================
let g:netrw_banner = 0
let g:netrw_liststyle = 3
let g:netrw_winsize = 25

" ==================================================
" バックアップとスワップ
" ==================================================
set nobackup
set noswapfile
set undofile
set undodir=~/.vim/undodir            " バグ8

" ==================================================
" クリップボード
" ==================================================
set clipboard=unnamedpuls             " バグ9

" ==================================================
" 補完設定
" ==================================================
set wildmenu
set wildmode=list:longest,full
set completeopt=menuone,noinsert,noselect

" vimrc を素早く開く
nnoremap <Leader>ev :edit $MYVIMRC<CR>
nnoremap <Leader>sv :source $MYVIMRC<CR>

" ==================================================
" カラースキーム
" ==================================================
colorscheme desert
set background=light                  " バグ10
```

---

## バグのヒント

<details>
<summary>ヒント（バグの種類を確認する）</summary>

10個のバグは以下のカテゴリに分類できます。

| カテゴリ | バグの数 |
|---|:---:|
| オプション名のスペルミス | 3個 |
| 値のスペルミス | 2個 |
| マッピングの種類の間違い | 2個 |
| autocmd の構文エラー | 2個 |
| 設定の矛盾 | 1個 |

</details>

<details>
<summary>ヒント（各バグの場所）</summary>

1. **バグ1**: `encoding` の値にスペルミスがあります
2. **バグ2**: `relativenumber` のスペルが間違っています
3. **バグ3**: `smartindent` のスペルが間違っています
4. **バグ4**: `nmap` は非推奨です。`nnoremap` を使うべきです
5. **バグ5**: `jj` のマッピングは挿入モード用なのに `nnoremap` になっています
6. **バグ6**: autocmd が `augroup` で囲まれていないため、`:source` で重複登録されます
7. **バグ7**: 複数行にわたる autocmd の行継続で `|` が不足しています
8. **バグ8**: `undodir` で指定したディレクトリが存在しない可能性があります
9. **バグ9**: `unnamedplus` のスペルが間違っています
10. **バグ10**: `desert` カラースキームは `dark` 背景向けなのに `light` に設定しています

</details>

---

## 解答例

<details>
<summary>解答例（修正版）</summary>

```vim
" ==================================================
" 基本設定
" ==================================================
set nocompatible
set encoding=utf-8                    " 修正1: uft-8 → utf-8
set fileencoding=utf-8

" ==================================================
" 表示設定
" ==================================================
set number
set relativenumber                    " 修正2: relativnumber → relativenumber
set cursorline
syntax enable

" ステータスライン
set laststatus=2
set statusline=%F%m%r%h%w\ [%{&enc}][%{&ff}]%=行:%l/%L\ 列:%c\ %p%%

" ==================================================
" インデント設定
" ==================================================
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab
set autoindent
set smartindent                       " 修正3: smartintent → smartindent

" ==================================================
" 検索設定
" ==================================================
set hlsearch
set incsearch
set ignorecase
set smartcase

" ==================================================
" キーマッピング
" ==================================================
let mapleader = "\<Space>"

" Y で行末までヤンク
nnoremap Y y$                         " 修正4: nmap → nnoremap

" 表示行単位で移動
nnoremap j gj
nnoremap k gk

" jj でノーマルモードに戻る
inoremap jj <Esc>                     " 修正5: nnoremap → inoremap

" Leader + w で保存
nnoremap <Leader>w :w<CR>

" 検索ハイライトを消す
nnoremap <Esc><Esc> :nohlsearch<CR>

" インデント後に選択を維持
vnoremap < <gv
vnoremap > >gv

" ウィンドウ間移動
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" ==================================================
" autocmd
" ==================================================
" 修正6: augroup で囲んで autocmd! でクリアする
augroup MyFileTypes
  autocmd!
  autocmd FileType python setlocal tabstop=4 shiftwidth=4 expandtab
  autocmd FileType python setlocal colorcolumn=79
  autocmd FileType javascript setlocal tabstop=2 shiftwidth=2 expandtab
  autocmd FileType make setlocal noexpandtab
augroup END

" カーソル位置復元
" 修正7: 行継続の | を追加
augroup RestoreCursor
  autocmd!
  autocmd BufReadPost *
    \ if line("'\"") > 0 && line("'\"") <= line("$") |
    \   exe "normal! g'\"" |
    \ endif
augroup END

" ==================================================
" netrw 設定
" ==================================================
let g:netrw_banner = 0
let g:netrw_liststyle = 3
let g:netrw_winsize = 25

" ==================================================
" バックアップとスワップ
" ==================================================
set nobackup
set noswapfile
set undofile
" 修正8: undodir のディレクトリを自動作成する
if !isdirectory(expand('~/.vim/undodir'))
  call mkdir(expand('~/.vim/undodir'), 'p')
endif
set undodir=~/.vim/undodir

" ==================================================
" クリップボード
" ==================================================
set clipboard=unnamedplus             " 修正9: unnamedpuls → unnamedplus

" ==================================================
" 補完設定
" ==================================================
set wildmenu
set wildmode=list:longest,full
set completeopt=menuone,noinsert,noselect

" vimrc を素早く開く
nnoremap <Leader>ev :edit $MYVIMRC<CR>
nnoremap <Leader>sv :source $MYVIMRC<CR>

" ==================================================
" カラースキーム
" ==================================================
set background=dark                   " 修正10: light → dark（desert は暗い背景向け）
colorscheme desert
```

</details>

<details>
<summary>各バグの詳細解説</summary>

### バグ1: `set encoding=uft-8`
**問題**: `uft-8` はタイポです。正しくは `utf-8` です。
**影響**: Vim が起動時にエラーを出します。マルチバイト文字（日本語など）が正しく表示されません。
**対処法**: スペルミスは `:set encoding?` で現在値を確認し、`:h encoding` でヘルプを参照するのが確実です。

### バグ2: `set relativnumber`
**問題**: `relativnumber` は存在しないオプションです。正しくは `relativenumber` です。
**影響**: 相対行番号が表示されません。
**対処法**: `:set` コマンドでは Tab 補完が使えます。`set relat<Tab>` で正しいオプション名が補完されます。

### バグ3: `set smartintent`
**問題**: `smartintent` は存在しません。正しくは `smartindent` です。
**影響**: 構文に応じた自動インデントが効きません。
**対処法**: indent と intent は紛らわしいスペルミスの代表例です。

### バグ4: `nmap Y y$`
**問題**: `nmap` は再帰的マッピングです。安全のため `nnoremap` を使うべきです。
**影響**: もし `y` や `$` が別のマッピングで上書きされていた場合、意図しない動作になります。
**対処法**: **原則として常に `noremap` 系を使う**のがベストプラクティスです。

### バグ5: `nnoremap jj <Esc>`
**問題**: `jj` で Esc する機能は**挿入モード**用です。`nnoremap` はノーマルモードのマッピングなので、挿入モードでは効きません。
**影響**: 挿入モードで `jj` を押してもノーマルモードに戻れません。代わりにノーマルモードで `jj` が Esc として動作してしまいます。
**対処法**: `inoremap jj <Esc>` に修正します。

### バグ6: augroup を使っていない
**問題**: autocmd が `augroup` で囲まれていないため、`:source ~/.vimrc` で再読み込みするたびに同じ autocmd が重複して登録されます。
**影響**: 再読み込みを繰り返すと、同じ処理が何度も実行されるようになり、パフォーマンスが低下します。
**対処法**: `augroup ... autocmd! ... augroup END` で囲みます。

### バグ7: 行継続の `|` が不足
**問題**: 複数行にわたる autocmd では、各コマンドの区切りに `|`（パイプ）が必要です。
**影響**: `if` 文が正しく解釈されず、エラーになるかカーソル位置復元が動作しません。
**対処法**: `line("$") |` と `g'\"" |` のように `|` を追加します。

### バグ8: undodir のディレクトリが存在しない
**問題**: `undodir=~/.vim/undodir` と指定していますが、このディレクトリが存在しない場合、undo ファイルが作成されずエラーになります。
**影響**: `undofile` を有効にしているのに永続 undo が機能しません。
**対処法**: `mkdir()` でディレクトリを自動作成するか、事前に手動で作成しておきます。

### バグ9: `set clipboard=unnamedpuls`
**問題**: `unnamedpuls` はタイポです。正しくは `unnamedplus` です。
**影響**: システムクリップボードとの連携が機能せず、Vim 内でヤンクした内容を他のアプリにペーストできません。
**対処法**: `:h clipboard` でヘルプを確認します。

### バグ10: `set background=light` と `colorscheme desert` の矛盾
**問題**: `desert` カラースキームは暗い背景（dark）向けに設計されています。`background=light` と組み合わせると、テキストが見づらくなります。
**影響**: 背景色と文字色のコントラストが悪く、読みにくいカラーリングになります。
**対処法**: `set background=dark` に変更し、`colorscheme` の**前に**記述します。

</details>

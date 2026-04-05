# 実践課題09：コードリーディング ─ 熟練者のvimrc ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第1章〜第7章（vimrcの基本〜関数とカスタムコマンド）
> **課題の種類**: コードリーディング
> **学習目標**: 経験豊富な開発者が書いたvimrcを読み解き、各設定の意図・設計パターン・工夫を理解する

---

## 課題の説明

以下は経験10年のVimユーザーが実際に使っているvimrc（抜粋）です。
コードを読んで、後に続く **10個の設問** に答えてください。

**実行は不要です。コードを読んで理解する力を鍛える課題です。**

---

## 読解対象コード

```vim
" ===========================================
" Experienced Developer's vimrc
" Last updated: 2024-04-15
" ===========================================

" {{{ 1. 基本設定
set nocompatible
set encoding=utf-8
scriptencoding utf-8
set fileencodings=utf-8,cp932,euc-jp,latin1
set fileformats=unix,dos,mac
set hidden
set autoread
set nobackup
set noswapfile
set undofile
set undodir=~/.vim/undo
" }}}

" {{{ 2. 表示設定
set number relativenumber
set signcolumn=yes
set cursorline
set laststatus=2
set noshowmode
set shortmess+=c
set pumheight=10
set scrolloff=8
set sidescrolloff=8
set display=lastline
set ambiwidth=double
" }}}

" {{{ 3. インデントと編集
set expandtab tabstop=4 shiftwidth=4 softtabstop=4
set smartindent
set shiftround
set virtualedit=block
set formatoptions+=mM
set nrformats-=octal
" }}}

" {{{ 4. 検索
set incsearch hlsearch
set ignorecase smartcase
set wrapscan
if executable('rg')
    set grepprg=rg\ --vimgrep\ --smart-case
    set grepformat=%f:%l:%c:%m
endif
" }}}

" {{{ 5. キーマッピング
let mapleader = "\<Space>"
let maplocalleader = ","

" 安全な終了
nnoremap ZZ <Nop>
nnoremap ZQ <Nop>
nnoremap <Leader>q :confirm quit<CR>

" 表示行移動
nnoremap <expr> j v:count == 0 ? 'gj' : 'j'
nnoremap <expr> k v:count == 0 ? 'gk' : 'k'

" 検索結果を中央に
nnoremap n nzzzv
nnoremap N Nzzzv

" ヤンク改善
nnoremap Y y$
vnoremap p "_dP

" バッファ操作
nnoremap <Leader>bn :bnext<CR>
nnoremap <Leader>bp :bprevious<CR>
nnoremap <Leader>bd :bdelete<CR>

" quickfix
nnoremap <Leader>co :copen<CR>
nnoremap <Leader>cc :cclose<CR>
nnoremap ]q :cnext<CR>zz
nnoremap [q :cprevious<CR>zz

" ターミナル
if has('terminal')
    nnoremap <Leader>tt :terminal<CR>
    tnoremap <Esc><Esc> <C-\><C-n>
endif
" }}}

" {{{ 6. autocmd
augroup vimrc_autocmd
    autocmd!

    " 最後の編集位置を復元
    autocmd BufReadPost *
        \ if line("'\"") >= 1 && line("'\"") <= line("$") && &filetype !~# 'commit' |
        \     execute "normal! g`\"" |
        \ endif

    " ヘルプを右側に開く
    autocmd FileType help wincmd L

    " quickfixを自動で開く
    autocmd QuickFixCmdPost [^l]* cwindow
    autocmd QuickFixCmdPost l* lwindow

    " ヤンクした範囲をハイライト
    if exists('##TextYankPost')
        autocmd TextYankPost * silent! lua vim.highlight.on_yank({timeout=200})
    endif

    " ターミナルを開いたら挿入モードに
    if has('terminal')
        autocmd TerminalOpen * setlocal nonumber norelativenumber signcolumn=no
        autocmd TerminalOpen * startinsert
    endif
augroup END

augroup vimrc_filetype
    autocmd!
    autocmd FileType python     setlocal colorcolumn=88 textwidth=88
    autocmd FileType javascript,typescript,vue,html,css,json,yaml
        \ setlocal tabstop=2 shiftwidth=2
    autocmd FileType make       setlocal noexpandtab tabstop=8 shiftwidth=8
    autocmd FileType go         setlocal noexpandtab tabstop=4 shiftwidth=4
    autocmd FileType gitcommit  setlocal spell spelllang=en,cjk textwidth=72
augroup END
" }}}

" {{{ 7. カスタムコマンドと関数
" 行末空白の削除（カーソル位置を保持）
function! s:TrimWhitespace() abort
    let l:save = winsaveview()
    keeppatterns %s/\s\+$//e
    call winrestview(l:save)
endfunction
command! TrimWhitespace call s:TrimWhitespace()

" 現在のバッファの差分をプレビュー
command! DiffOrig vert new | set buftype=nofile | read ++edit # | 0d_
    \ | diffthis | wincmd p | diffthis

" パスをクリップボードにコピー
command! CopyPath let @+ = expand('%:p')
command! CopyFileName let @+ = expand('%:t')
command! CopyRelPath let @+ = expand('%')

" Quickfixの内容をバッファに展開
function! s:QuickfixToBuffer() abort
    let l:items = getqflist()
    if empty(l:items)
        echo "Quickfix is empty"
        return
    endif
    new
    setlocal buftype=nofile
    let l:lines = []
    for l:item in l:items
        let l:fname = bufname(l:item.bufnr)
        call add(l:lines, printf('%s:%d:%d: %s',
            \ l:fname, l:item.lnum, l:item.col, l:item.text))
    endfor
    call setline(1, l:lines)
endfunction
command! QfToBuffer call s:QuickfixToBuffer()

" プロジェクトルートに移動
function! s:CdProjectRoot() abort
    let l:markers = ['.git', 'Makefile', 'package.json', 'Cargo.toml', 'go.mod']
    let l:dir = expand('%:p:h')
    while l:dir !=# '/'
        for l:marker in l:markers
            if isdirectory(l:dir . '/' . l:marker) || filereadable(l:dir . '/' . l:marker)
                execute 'lcd' fnameescape(l:dir)
                echo 'Project root: ' . l:dir
                return
            endif
        endfor
        let l:dir = fnamemodify(l:dir, ':h')
    endwhile
    echo 'Project root not found'
endfunction
command! CdRoot call s:CdProjectRoot()
" }}}
```

---

## 設問

以下の10問に答えてください。

### 問1：`set hidden` の役割

`set hidden` はどのような動作を可能にしますか？これがない場合、バッファ操作（`:bnext` など）でどのような問題が発生しますか？

<details>
<summary>解答</summary>

`set hidden` を設定すると、**未保存のバッファがあっても別のバッファに切り替えられる**ようになります。

この設定がない場合、変更があるバッファを離れようとすると「保存していない変更があります」というエラーが出て切り替えられません。複数ファイルを行き来するワークフローでは必須の設定です。

</details>

### 問2：`number` と `relativenumber` の併用

`set number relativenumber` とした場合、行番号はどのように表示されますか？なぜこの組み合わせが有用なのでしょうか？

<details>
<summary>解答</summary>

両方を有効にすると、**カーソル行は絶対行番号**、**それ以外は相対行番号**（カーソルからの距離）が表示されます。

```
  3  function hello()
  2      let x = 1
  1      let y = 2
  5  ← カーソル行（絶対行番号）
  1      return x + y
  2  endfunction
  3
```

これが有用な理由は、`5j`（5行下に移動）や `3dk`（3行上まで削除）のようなカウント指定の移動・操作で、目で見てすぐに必要な数字がわかるからです。

</details>

### 問3：`undofile` と `noswapfile` の組み合わせ

この開発者は `noswapfile` でスワップファイルを無効にしつつ、`undofile` でアンドゥファイルを有効にしています。この設計判断の意図は何でしょうか？

<details>
<summary>解答</summary>

- **`noswapfile`**: スワップファイルはクラッシュ時の復旧用ですが、Git管理下のプロジェクトでは `git stash` や `git checkout` で復旧できるため、スワップファイルの必要性が低いです。また、同一ファイルを複数のVimで開く際の警告を避けられます。

- **`undofile`**: Vimを終了しても**アンドゥ履歴がファイルに永続化**されます。翌日にファイルを開き直しても `u` で昨日の変更を取り消せるため、非常に便利です。

つまり「クラッシュ復旧はGitに任せ、アンドゥ履歴の永続化の方が実用価値が高い」という判断です。

</details>

### 問4：`<expr>` マッピングの動作

```vim
nnoremap <expr> j v:count == 0 ? 'gj' : 'j'
```

この `<expr>` マッピングはどのように動作しますか？`nnoremap j gj` と比べたメリットは何ですか？

<details>
<summary>解答</summary>

`<expr>` はマッピングの右辺を**式（expression）として評価**します。

- `v:count` はユーザーが入力した数値プレフィックスです
- `v:count == 0` は数値を指定していないとき（ただの `j`）
- 数値なし → `gj`（表示行移動）を実行
- 数値あり → `j`（論理行移動）を実行（例: `5j` で5行移動）

**メリット**: 単純な `nnoremap j gj` だと、`5j` で「表示行で5行分」移動してしまい、折り返しのある行で期待と異なる動作になります。`<expr>` を使うことで、普段は表示行移動、カウント指定時は正確な論理行移動という**最善の使い分け**ができます。

</details>

### 問5：`ZZ` と `ZQ` の `<Nop>` マッピング

```vim
nnoremap ZZ <Nop>
nnoremap ZQ <Nop>
```

なぜこれらのキーを無効化しているのでしょうか？

<details>
<summary>解答</summary>

- `ZZ` = `:wq`（保存して終了）
- `ZQ` = `:q!`（保存せず終了）

これらは**たった2キーでVimが終了する**ため、うっかり押してしまうと未保存の作業を失う危険があります。特に `ZQ` は確認なしで変更を破棄します。

代わりに `<Leader>q` で `:confirm quit`（未保存時に確認ダイアログを表示）を使うことで、安全な終了フローを強制しています。

</details>

### 問6：`keeppatterns` の役割

```vim
function! s:TrimWhitespace() abort
    let l:save = winsaveview()
    keeppatterns %s/\s\+$//e
    call winrestview(l:save)
endfunction
```

`keeppatterns` を付けない場合、どのような問題が起きますか？`winsaveview()` / `winrestview()` は何をしていますか？

<details>
<summary>解答</summary>

- **`keeppatterns`**: これがないと、`%s/\s\+$//e` を実行した後に**検索パターン**（`@/` レジスタ）が `\s\+$` に書き換わってしまいます。ユーザーが `n` で次の検索結果に移動しようとすると、意図しないパターンで検索されます。`keeppatterns` は検索パターンを変更しないようにします。

- **`winsaveview()`**: カーソル位置、スクロール位置、折りたたみ状態などを保存します。
- **`winrestview()`**: 保存した状態を復元します。

これにより、行末空白を削除しても**ユーザーの画面状態に一切影響を与えない**透明な操作になります。

</details>

### 問7：`grepprg` の条件付き設定

```vim
if executable('rg')
    set grepprg=rg\ --vimgrep\ --smart-case
    set grepformat=%f:%l:%c:%m
endif
```

なぜ `if executable('rg')` で囲んでいるのですか？`rg` が使える場合、デフォルトの `grep` と比べてどのようなメリットがありますか？

<details>
<summary>解答</summary>

- **`if executable('rg')`**: `rg`（ripgrep）がインストールされていない環境でもエラーにならないようにするためです。vimrcを複数のマシンで共有する場合、すべての環境に `rg` があるとは限りません。

- **メリット**: `rg` はデフォルトの `grep` と比べて:
  1. 桁違いに高速（Rust製、並列処理）
  2. `.gitignore` を自動的に尊重する
  3. `--smart-case` で大文字小文字の自動判定
  4. `--vimgrep` でVimの quickfix 形式に出力

`:grep pattern` を実行すると `rg` で検索され、結果が quickfix リストに入るので、`]q` / `[q` で結果間を移動できます。

</details>

### 問8：`DiffOrig` コマンドの動作

```vim
command! DiffOrig vert new | set buftype=nofile | read ++edit # | 0d_
    \ | diffthis | wincmd p | diffthis
```

このコマンドは何をしていますか？各パイプ（`|`）で区切られた処理を順に説明してください。

<details>
<summary>解答</summary>

`DiffOrig` は**現在のバッファの編集内容と、保存されているファイルの内容を比較**するコマンドです。

1. `vert new` — 垂直分割で新しい空バッファを作成
2. `set buftype=nofile` — このバッファはファイルに紐付かない一時バッファに設定
3. `read ++edit #` — `#`（直前のバッファ = 元のファイル）のディスク上の内容を読み込む
4. `0d_` — 1行目の空行を削除（`read` で入る余分な行）
5. `diffthis` — この一時バッファをdiff対象にする
6. `wincmd p` — 元のバッファに戻る
7. `diffthis` — 元のバッファもdiff対象にする

結果として、「保存後に自分がどこを変更したか」が左右に色分けで表示されます。Git管理外のファイルや、コミット前の確認に便利です。

</details>

### 問9：`s:CdProjectRoot()` の設計

```vim
function! s:CdProjectRoot() abort
    let l:markers = ['.git', 'Makefile', 'package.json', 'Cargo.toml', 'go.mod']
    let l:dir = expand('%:p:h')
    while l:dir !=# '/'
        ...
    endwhile
endfunction
```

この関数はどのようなアルゴリズムでプロジェクトルートを見つけていますか？`s:` プレフィックスと `abort` の意味は何ですか？

<details>
<summary>解答</summary>

**アルゴリズム**:
1. 現在のファイルが存在するディレクトリから開始（`expand('%:p:h')`）
2. そのディレクトリにマーカーファイル/ディレクトリ（`.git`、`Makefile` など）があるか確認
3. なければ親ディレクトリに移動（`fnamemodify(l:dir, ':h')`）
4. ルート（`/`）に到達するまで繰り返す
5. 見つかったら `lcd`（ローカルカレントディレクトリ）を変更

**`s:` プレフィックス**: スクリプトローカルスコープ。この関数はこのvimrcファイル内からしか呼べません。名前の衝突を防ぐための良い習慣です。

**`abort`**: 関数内でエラーが発生した場合、即座に関数を終了します。これがないとエラーが起きても後続の行が実行され続け、意図しない動作になります。

</details>

### 問10：全体の設計パターン

このvimrc全体を通して、著者が一貫して適用している設計原則やパターンを3つ以上挙げてください。

<details>
<summary>解答</summary>

1. **環境非依存性（ポータビリティ）**: `if executable('rg')`、`if has('terminal')`、`if exists('##TextYankPost')` のように、環境やVimのバージョンに応じて条件分岐しています。これにより、異なるマシンやバージョンでも安全に使えます。

2. **非破壊性**: `keeppatterns`、`winsaveview()`/`winrestview()`、`ZZ`/`ZQ` の無効化など、ユーザーの意図しない変更を防ぐ配慮が随所にあります。

3. **スコープの最小化**: `s:` プレフィックス（スクリプトローカル関数）、`l:` プレフィックス（ローカル変数）、`setlocal`（バッファローカル設定）で、影響範囲を最小限に抑えています。

4. **構造化と整理**: `augroup` による autocmd のグループ化、`{{{ }}}` による折りたたみマーカー、カテゴリ別のセクション分けで、設定ファイルの可読性を確保しています。

5. **安全なデフォルト**: `confirm quit`、`noswapfile` + `undofile`、`nrformats-=octal`（8進数の無効化）など、事故を未然に防ぐ設定を選択しています。

6. **`noremap` の一貫使用**: すべてのマッピングが `nnoremap`、`vnoremap` など非再帰マッピングで定義されています。

</details>

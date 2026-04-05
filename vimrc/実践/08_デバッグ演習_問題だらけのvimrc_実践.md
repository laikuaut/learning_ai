# 実践課題08：デバッグ演習 ─ 問題だらけのvimrc ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第1章〜第6章（vimrcの基本〜autocmd）
> **課題の種類**: デバッグ
> **学習目標**: 動作しない・意図通りに動かないvimrc設定のバグを読み解き、原因を特定して修正する力を養う

---

## 課題の説明

以下のvimrcには **10個のバグ** が埋め込まれています。
設定を読み解き、すべてのバグを見つけて修正してください。

### 進め方

1. 下のバグ入りvimrcをファイルに保存する
2. `vim -u buggy.vim` で読み込んで動作を確認する
3. 1つずつバグを修正し、`:source %` で再読み込みして確認する
4. 全設定が意図通りに動作すれば完了

### バグの種類

- 構文エラー（Vimが起動時にエラーを出す）
- 論理エラー（エラーは出ないが意図した動作にならない）
- 設計ミス（動作はするが問題を引き起こす）

---

## バグ入りvimrc

以下のコードをそのまま `buggy.vim` として保存してください。

```vim
" ===========================================
" バグ入りvimrc（10個のバグがあります）
" ===========================================

" --- 基本設定 ---
set nocompatible
set encoding=utf-8
set fileencoding utf-8            " バグ1: 構文エラー

" --- 表示設定 ---
set number
set cursorline
syntax on
colorscheme desert
set background=light              " バグ2: desertは暗い背景用のカラースキーム

" --- インデント ---
set tabstop=4
set shiftwidth=2                  " バグ3: tabstopとshiftwidthが不一致
set softtabstop=4
set expandtab
set autoindent

" --- 検索 ---
set incsearch
set hlsearch
set smartcase                     " バグ4: ignorecaseなしでsmartcase

" --- ハイライト解除 ---
nmap <Esc><Esc> :nohlsearch<CR>  " バグ5: nmapを使っている

" --- キーマッピング ---
let mapleader = "\<Space>"

nnoremap j gj
nnoremap k gk
nnoremap gj j                     " バグ6がなければこれは問題ないが...

" --- ウィンドウ移動 ---
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
inoremap <C-l> <C-w>l            " バグ7: モードの指定ミス

" --- ファイルタイプ別設定 ---
autocmd FileType python setlocal tabstop=4 shiftwidth=4 expandtab
autocmd FileType html setlocal tabstop=2 shiftwidth=2 expandtab
autocmd FileType make setlocal tabstop=8 shiftwidth=8 expandtab    " バグ8: Makefileにexpandtab
autocmd FileType python setlocal tabstop=4 shiftwidth=4 expandtab
                                  " バグ9: augroupで囲んでいない（再読み込みで重複）

" --- 保存時の自動処理 ---
augroup AutoSave
    autocmd BufWritePre * %s/\s\+$//   " バグ10: eフラグがない
augroup END
```

---

## 各バグの解説と修正

<details>
<summary>バグ1：fileencodingの構文エラー</summary>

**症状**: Vimの起動時にエラーメッセージが表示される

**原因**: `set` で値を設定するときは `=` が必要

```vim
" 修正前（バグ）
set fileencoding utf-8

" 修正後
set fileencoding=utf-8
```

**ポイント**: `set option=value` が正しい構文です。`=` を忘れると `fileencoding` と `utf-8` を別々のオプションとして解釈しようとしてエラーになります。

</details>

<details>
<summary>バグ2：カラースキームと背景色の不一致</summary>

**症状**: エラーは出ないが、色が見にくく読みづらい

**原因**: `desert` は暗い背景（dark）用のカラースキームなのに `background=light` を設定している

```vim
" 修正前（バグ）
colorscheme desert
set background=light

" 修正後
set background=dark       " desertに合わせてdarkに変更
colorscheme desert        " backgroundの後にcolorschemeを設定
```

**ポイント**: `background` の設定は `colorscheme` の**前**に書くべきです。順序が逆だと、カラースキームの色が正しく適用されないことがあります。

</details>

<details>
<summary>バグ3：tabstopとshiftwidthの不一致</summary>

**症状**: Tab キーで4スペース入るが、`>>` で2スペースしかインデントされない

**原因**: `tabstop=4` と `shiftwidth=2` が不一致

```vim
" 修正前（バグ）
set tabstop=4
set shiftwidth=2

" 修正後（すべて揃える）
set tabstop=4
set shiftwidth=4
set softtabstop=4
```

**ポイント**: 特別な理由がない限り、`tabstop`、`shiftwidth`、`softtabstop` は同じ値にするのがベストプラクティスです。

</details>

<details>
<summary>バグ4：ignorecaseなしのsmartcase</summary>

**症状**: `smartcase` が機能しない（常に大文字小文字を区別する）

**原因**: `smartcase` は `ignorecase` が有効なときだけ機能する

```vim
" 修正前（バグ）
set smartcase             " ignorecaseがない！

" 修正後
set ignorecase            " まず大文字小文字を無視する設定
set smartcase             " 大文字を含む場合のみ区別
```

**ポイント**: `smartcase` は `ignorecase` の動作を条件付きで変えるオプションです。前提となる `ignorecase` が無いと何も起きません。

</details>

<details>
<summary>バグ5：nmapによる再帰マッピング</summary>

**症状**: 現時点ではたまたま動くが、他のマッピングとの組み合わせで予期しない動作になる可能性がある

**原因**: `nmap` は再帰的マッピングで、右辺のキーが更にマッピングされる

```vim
" 修正前（バグ）
nmap <Esc><Esc> :nohlsearch<CR>

" 修正後
nnoremap <Esc><Esc> :nohlsearch<CR>
```

**ポイント**: マッピングは常に `noremap` 系を使うのが原則です。`nmap`、`imap`、`vmap` は特別な理由がない限り使いません。

</details>

<details>
<summary>バグ6：j/kのマッピングと元の動作へのアクセス</summary>

**症状**: `gj`（元の論理行のj）にアクセスする手段がなくなる…が `nnoremap` なので実は問題ない

**解説**: これは**バグではありません（ひっかけ）**。

```vim
nnoremap j gj     " j を押すと gj（表示行移動）
nnoremap k gk     " k を押すと gk（表示行移動）
nnoremap gj j     " gj を押すと j（論理行移動）
```

`nnoremap` は非再帰なので、右辺の `j` や `gj` は**元の動作**を指します。もしこれが `nmap` だったら無限ループになりますが、`nnoremap` なので正しく動作します。

**ポイント**: `noremap` と `map` の違いを理解するための重要な例です。

</details>

<details>
<summary>バグ7：ウィンドウ移動のモード指定ミス</summary>

**症状**: `<C-l>` が挿入モードでしか動作しない。ノーマルモードで右のウィンドウに移動できない

**原因**: `<C-l>` だけ `inoremap` になっている

```vim
" 修正前（バグ）
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
inoremap <C-l> <C-w>l    " inoremap になっている！

" 修正後
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l    " nnoremap に統一
```

**ポイント**: コピー&ペーストでマッピングを書く際、モードのプレフィックスを変え忘れるのはよくあるミスです。

</details>

<details>
<summary>バグ8：Makefileにexpandtab</summary>

**症状**: Makefile内のレシピがスペースでインデントされ、makeコマンドでエラーになる

**原因**: Makefileのレシピはタブ文字が必須だが `expandtab` が設定されている

```vim
" 修正前（バグ）
autocmd FileType make setlocal tabstop=8 shiftwidth=8 expandtab

" 修正後
autocmd FileType make setlocal tabstop=8 shiftwidth=8 noexpandtab
```

**ポイント**: Makefileは「タブ文字でなければならない」という厳格なルールがあります。`noexpandtab` を明示しましょう。

</details>

<details>
<summary>バグ9：augroupで囲んでいないautocmd</summary>

**症状**: `:source ~/.vimrc` で再読み込みするたびに同じ `autocmd` が重複登録され、ファイルを開くたびに設定が複数回実行される

**原因**: `augroup` + `autocmd!` で囲んでいない

```vim
" 修正前（バグ）
autocmd FileType python setlocal tabstop=4 shiftwidth=4 expandtab
autocmd FileType html setlocal tabstop=2 shiftwidth=2 expandtab
autocmd FileType make setlocal tabstop=8 shiftwidth=8 noexpandtab

" 修正後
augroup FileTypeSettings
    autocmd!
    autocmd FileType python setlocal tabstop=4 shiftwidth=4 expandtab
    autocmd FileType html setlocal tabstop=2 shiftwidth=2 expandtab
    autocmd FileType make setlocal tabstop=8 shiftwidth=8 noexpandtab
augroup END
```

**ポイント**: `autocmd!` はグループ内の既存 autocmd をクリアします。これにより再読み込み時の重複が防げます。

</details>

<details>
<summary>バグ10：置換コマンドのeフラグ欠落</summary>

**症状**: 行末に空白がないファイルを保存すると「パターンが見つかりません」エラーが表示される

**原因**: `%s/\s\+$//` に `e` フラグがない

```vim
" 修正前（バグ）
autocmd BufWritePre * %s/\s\+$//

" 修正後
augroup AutoSave
    autocmd!
    autocmd BufWritePre * %s/\s\+$//e
augroup END
```

**ポイント**: `e` フラグは「パターンが見つからなくてもエラーにしない」という意味です。保存のたびに行末空白があるとは限らないので必須です。

</details>

---

## 修正済みの完成版

<details>
<summary>全バグ修正後のvimrc</summary>

```vim
" ===========================================
" バグ修正済みvimrc
" ===========================================

" --- 基本設定 ---
set nocompatible
set encoding=utf-8
set fileencoding=utf-8

" --- 表示設定 ---
set number
set cursorline
syntax on
set background=dark
colorscheme desert

" --- インデント ---
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab
set autoindent

" --- 検索 ---
set incsearch
set hlsearch
set ignorecase
set smartcase

" --- ハイライト解除 ---
nnoremap <Esc><Esc> :nohlsearch<CR>

" --- キーマッピング ---
let mapleader = "\<Space>"

nnoremap j gj
nnoremap k gk
nnoremap gj j

" --- ウィンドウ移動 ---
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" --- ファイルタイプ別設定 ---
augroup FileTypeSettings
    autocmd!
    autocmd FileType python setlocal tabstop=4 shiftwidth=4 expandtab
    autocmd FileType html setlocal tabstop=2 shiftwidth=2 expandtab
    autocmd FileType make setlocal tabstop=8 shiftwidth=8 noexpandtab
augroup END

" --- 保存時の自動処理 ---
augroup AutoSave
    autocmd!
    autocmd BufWritePre * %s/\s\+$//e
augroup END
```

</details>

---

## デバッグのコツ

vimrcのデバッグで役立つテクニックをまとめます。

| テクニック | コマンド | 説明 |
|-----------|---------|------|
| オプション値の確認 | `:set tabstop?` | 現在の値を表示 |
| オプションの設定元を確認 | `:verbose set tabstop?` | どのファイルの何行目で設定されたか |
| マッピングの確認 | `:map <C-l>` | キーに割り当てられた動作を表示 |
| マッピングの設定元 | `:verbose nmap <C-l>` | どこで定義されたか |
| autocmdの確認 | `:autocmd FileType python` | 登録されたautocmdを一覧 |
| メッセージの確認 | `:messages` | 直前のエラーメッセージを確認 |
| 設定なしで起動 | `vim -u NONE` | 素の状態で起動して問題切り分け |
| 特定の設定で起動 | `vim -u buggy.vim` | 指定したvimrcだけで起動 |

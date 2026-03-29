# 第6章：autocmd とファイルタイプ別設定

## この章のゴール

- `autocmd` の構文とイベントの種類を理解する
- `augroup` を使って autocmd の重複を防ぐ方法を身につける
- ファイルタイプ検出の仕組みと設定方法を理解する
- ファイルタイプ別にインデントや設定を切り替えられる
- `ftplugin` ディレクトリを使った設定の分離ができる
- 実用的な `autocmd` を活用できる

---

## 1. autocmd の基本

### autocmd とは

`autocmd`（auto command）は、特定のイベントが発生した時に自動的にコマンドを実行する仕組みです。

```vim
" 構文
autocmd {イベント} {パターン} {コマンド}

" 例: Python ファイルを開いた時にインデントを4スペースに設定
autocmd FileType python setlocal tabstop=4 shiftwidth=4 expandtab
```

### 主要なイベント一覧

```
  ┌─────────────────┬──────────────────────────────────────┐
  │ イベント        │ 発生タイミング                       │
  ├─────────────────┼──────────────────────────────────────┤
  │ BufNewFile      │ 新しいファイルの編集を開始した時     │
  │ BufRead         │ 既存ファイルを読み込んだ時           │
  │ BufReadPost     │ ファイル読み込み完了後               │
  │ BufWrite        │ ファイルを書き込む前                 │
  │ BufWritePost    │ ファイルを書き込んだ後               │
  │ BufEnter        │ バッファに入った時                   │
  │ BufLeave        │ バッファから離れた時                 │
  ├─────────────────┼──────────────────────────────────────┤
  │ FileType        │ ファイルタイプが設定された時         │
  ├─────────────────┼──────────────────────────────────────┤
  │ VimEnter        │ Vim の起動が完了した時               │
  │ VimLeave        │ Vim を終了する時                     │
  ├─────────────────┼──────────────────────────────────────┤
  │ InsertEnter     │ 挿入モードに入った時                 │
  │ InsertLeave     │ 挿入モードから離れた時               │
  ├─────────────────┼──────────────────────────────────────┤
  │ WinEnter        │ ウィンドウに入った時                 │
  │ WinLeave        │ ウィンドウから離れた時               │
  ├─────────────────┼──────────────────────────────────────┤
  │ CursorHold      │ カーソルが一定時間動かなかった時     │
  │ CursorMoved     │ カーソルが移動した時                 │
  └─────────────────┴──────────────────────────────────────┘
```

### パターンの書き方

```vim
" ファイルパターン
autocmd BufRead *.py  echo "Python ファイルを読み込みました"
autocmd BufRead *.js  echo "JavaScript ファイルを読み込みました"
autocmd BufRead *.txt echo "テキストファイルを読み込みました"

" 複数パターン
autocmd BufRead *.py,*.rb echo "Python または Ruby"

" 全てのファイル
autocmd BufRead * echo "何かのファイルを読み込みました"

" FileType イベントではファイルタイプ名を指定
autocmd FileType python setlocal expandtab
autocmd FileType javascript,typescript setlocal shiftwidth=2
```

### ポイントまとめ

- `autocmd` は `イベント` + `パターン` + `コマンド` の3要素で構成されます
- `FileType` イベントが最もよく使われます
- `BufRead` / `BufWrite` でファイルの読み書き時の処理を設定できます

---

## 2. augroup の重要性

### autocmd の重複問題

vimrc を `:source` で再読み込みすると、`autocmd` が重複して登録されてしまいます。

```
  問題: .vimrc を3回 :source した場合

  1回目: autocmd FileType python setlocal expandtab  ← 1つ登録
  2回目: autocmd FileType python setlocal expandtab  ← 2つ目が追加
  3回目: autocmd FileType python setlocal expandtab  ← 3つ目が追加

  → Python ファイルを開くたびに同じコマンドが3回実行される！
```

### augroup で重複を防ぐ

```vim
" 正しい書き方: augroup + autocmd!
augroup MyPythonSettings
  autocmd!                " このグループの autocmd を全て削除
  autocmd FileType python setlocal tabstop=4 shiftwidth=4 expandtab
augroup END
```

```
  augroup の動作:

  1回目の :source:
  ┌─ MyPythonSettings ──────────────────────┐
  │ autocmd!  → グループ内を全削除（空なので何もしない）│
  │ autocmd FileType python ...  → 登録     │
  └──────────────────────────────────────────┘

  2回目の :source:
  ┌─ MyPythonSettings ──────────────────────┐
  │ autocmd!  → 前回の autocmd を削除       │
  │ autocmd FileType python ...  → 再登録   │
  └──────────────────────────────────────────┘

  → 何回 :source しても autocmd は常に1つだけ！
```

### augroup の命名規約

```vim
" グループ名は自由に決められます
" 分かりやすい名前を付けましょう

augroup MyFileTypeSettings
  autocmd!
  autocmd FileType python setlocal expandtab tabstop=4 shiftwidth=4
  autocmd FileType javascript setlocal expandtab tabstop=2 shiftwidth=2
augroup END

augroup MyAutoSave
  autocmd!
  autocmd FocusLost * silent! wall
augroup END
```

> **重要**: vimrc 内の全ての `autocmd` は必ず `augroup` で囲みましょう。これは Vim の設定における最も重要なベストプラクティスの1つです。

### ポイントまとめ

- `autocmd` は `:source` のたびに重複登録されてしまいます
- `augroup` + `autocmd!` のパターンで重複を防ぎます
- vimrc 内の全ての `autocmd` は `augroup` で囲むのが鉄則です

---

## 3. ファイルタイプ検出

### filetype の設定

```vim
" ファイルタイプ検出の有効化（再掲）
filetype on             " ファイルタイプの検出
filetype plugin on      " ファイルタイプ別プラグイン
filetype indent on      " ファイルタイプ別インデント

" まとめて有効化
filetype plugin indent on
```

### ファイルタイプの確認方法

```vim
" 現在のファイルタイプを確認
:set filetype?
" → filetype=python

" ファイルタイプを手動で設定
:set filetype=javascript

" 省略形
:set ft=python
```

### ファイルタイプ検出の仕組み

```
  Vim のファイルタイプ検出の流れ:

  ファイルを開く
      │
      ▼
  拡張子で判定  ─→  .py → python
      │              .js → javascript
      │              .ts → typescript
      │              .html → html
      ▼
  拡張子で判定できない場合
      │
      ▼
  ファイル内容で判定  ─→  #!/bin/bash → sh
      │                    #!/usr/bin/env python → python
      ▼
  判定できない場合 → filetype が空のまま
```

### ポイントまとめ

- `filetype plugin indent on` で自動検出を有効化します
- `:set filetype?` で現在のファイルタイプを確認できます
- 拡張子やシバン（`#!`）でファイルタイプが自動判定されます

---

## 4. ファイルタイプ別設定

### autocmd FileType による設定

最もよく使われるパターンです。ファイルタイプが検出された時に設定を適用します。

```vim
augroup FileTypeSettings
  autocmd!
  " Python
  autocmd FileType python setlocal
    \ tabstop=4
    \ shiftwidth=4
    \ softtabstop=4
    \ expandtab
    \ textwidth=79
    \ colorcolumn=80

  " JavaScript / TypeScript
  autocmd FileType javascript,typescript setlocal
    \ tabstop=2
    \ shiftwidth=2
    \ softtabstop=2
    \ expandtab

  " Go（タブ文字を使用）
  autocmd FileType go setlocal
    \ tabstop=4
    \ shiftwidth=4
    \ softtabstop=0
    \ noexpandtab

  " HTML / CSS
  autocmd FileType html,css setlocal
    \ tabstop=2
    \ shiftwidth=2
    \ expandtab

  " Markdown
  autocmd FileType markdown setlocal
    \ textwidth=80
    \ wrap
    \ spell

  " Makefile（タブ必須）
  autocmd FileType make setlocal
    \ noexpandtab
    \ tabstop=4
    \ shiftwidth=4
augroup END
```

### 複数行の autocmd

長い設定は `\`（バックスラッシュ）で行を継続できます。

```vim
" 行継続の例（\ の前にスペースが必要）
autocmd FileType python setlocal
  \ tabstop=4
  \ shiftwidth=4
  \ expandtab
```

### ポイントまとめ

- `autocmd FileType` でファイルタイプごとの設定を適用します
- `setlocal` を使ってバッファローカルに設定します
- 行が長い場合は `\` で行を継続できます

---

## 5. ftplugin ディレクトリ

### ftplugin とは

`ftplugin`（filetype plugin）ディレクトリを使うと、ファイルタイプ別の設定をファイルに分離できます。vimrc が長くなってきた場合に有効です。

```
  ディレクトリ構造:

  ~/.vim/
  └── ftplugin/
      ├── python.vim       ← Python 用の設定
      ├── javascript.vim   ← JavaScript 用の設定
      ├── go.vim           ← Go 用の設定
      ├── html.vim         ← HTML 用の設定
      └── markdown.vim     ← Markdown 用の設定
```

### ftplugin ファイルの書き方

```vim
" ~/.vim/ftplugin/python.vim
" Python 用の設定

setlocal tabstop=4
setlocal shiftwidth=4
setlocal softtabstop=4
setlocal expandtab
setlocal textwidth=79
setlocal colorcolumn=80

" Python 用のマッピング
nnoremap <buffer> <Leader>r :!python3 %<CR>
```

```vim
" ~/.vim/ftplugin/javascript.vim
" JavaScript 用の設定

setlocal tabstop=2
setlocal shiftwidth=2
setlocal softtabstop=2
setlocal expandtab

" JavaScript 用のマッピング
nnoremap <buffer> <Leader>r :!node %<CR>
```

### autocmd vs ftplugin

```
  ┌──────────────┬──────────────────────┬──────────────────────┐
  │              │ autocmd FileType     │ ftplugin             │
  ├──────────────┼──────────────────────┼──────────────────────┤
  │ 設定場所     │ .vimrc 内            │ ~/.vim/ftplugin/     │
  │ 管理         │ 1ファイルにまとまる  │ 言語ごとに分離       │
  │ 適した規模   │ 少量の設定           │ 大量の設定           │
  │ augroup      │ 必要                 │ 不要（自動管理）     │
  └──────────────┴──────────────────────┴──────────────────────┘

  少ない設定 → autocmd FileType で十分
  多い設定   → ftplugin ディレクトリで分離
```

### setlocal と <buffer> の重要性

ftplugin 内では必ず `setlocal` と `<buffer>` を使います。

```vim
" ○ 正しい: バッファローカルな設定
setlocal expandtab
nnoremap <buffer> <Leader>r :!python3 %<CR>

" × 間違い: グローバルな設定（他のファイルにも影響する）
set expandtab
nnoremap <Leader>r :!python3 %<CR>
```

### ポイントまとめ

- `~/.vim/ftplugin/言語名.vim` でファイルタイプ別設定を分離できます
- ftplugin 内では `setlocal` と `<buffer>` を使います
- 設定が少ない場合は `autocmd FileType` で十分です

---

## 6. カスタムファイルタイプの定義

### 独自のファイルタイプを設定

Vim が認識しないファイル拡張子に対して、手動でファイルタイプを設定できます。

```vim
augroup CustomFileTypes
  autocmd!
  " .env ファイルを sh として認識させる
  autocmd BufRead,BufNewFile *.env setfiletype sh

  " .mdx ファイルを markdown として認識させる
  autocmd BufRead,BufNewFile *.mdx setfiletype markdown

  " Docker 関連ファイル
  autocmd BufRead,BufNewFile Dockerfile.* setfiletype dockerfile
  autocmd BufRead,BufNewFile docker-compose*.yml setfiletype yaml

  " .conf ファイルを設定ファイルとして認識
  autocmd BufRead,BufNewFile *.conf setfiletype conf
augroup END
```

### ポイントまとめ

- `BufRead,BufNewFile` でファイルパターンを指定します
- `setfiletype` でファイルタイプを設定します

---

## 7. 実用的な autocmd 例

### 最後のカーソル位置を復元

```vim
" ファイルを開いた時に、前回の編集位置にカーソルを復元
augroup RestoreCursorPosition
  autocmd!
  autocmd BufReadPost *
    \ if line("'\"") >= 1 && line("'\"") <= line("$") && &ft !~# 'commit'
    \ |   execute "normal! g`\""
    \ | endif
augroup END
```

### 末尾の空白を自動削除

```vim
" 保存時に行末の余分な空白を自動削除
augroup TrimTrailingWhitespace
  autocmd!
  autocmd BufWritePre * :%s/\s\+$//e
augroup END
```

> **注意**: Markdown では末尾スペース2つが改行を意味するため、除外したい場合があります。

```vim
" Markdown を除外する場合
augroup TrimTrailingWhitespace
  autocmd!
  autocmd BufWritePre * if &ft != 'markdown' | :%s/\s\+$//e | endif
augroup END
```

### ファイル保存時に自動でディレクトリを作成

```vim
" 存在しないディレクトリのファイルを保存する時に、ディレクトリを自動作成
augroup AutoMkdir
  autocmd!
  autocmd BufWritePre * call s:auto_mkdir(expand('<afile>:p:h'))
augroup END

function! s:auto_mkdir(dir)
  if !isdirectory(a:dir)
    call mkdir(a:dir, 'p')
  endif
endfunction
```

### quickfix ウィンドウを自動で開く

```vim
" :grep 等の後に自動で quickfix ウィンドウを開く
augroup AutoQuickfix
  autocmd!
  autocmd QuickFixCmdPost *grep* cwindow
augroup END
```

### 挿入モードでカーソル行のハイライトを制御

```vim
" 挿入モードでは cursorline を無効化
augroup CursorLineControl
  autocmd!
  autocmd InsertEnter * set nocursorline
  autocmd InsertLeave * set cursorline
augroup END
```

### ターミナルバッファの設定

```vim
" ターミナルを開いた時に行番号を非表示にする
augroup TerminalSettings
  autocmd!
  autocmd TerminalOpen * setlocal nonumber norelativenumber
augroup END
```

### ポイントまとめ

- カーソル位置の復元は多くの vimrc で使われる定番設定です
- 末尾空白の自動削除は `BufWritePre` イベントで実現します
- `autocmd` を活用すると Vim を細かくカスタマイズできます
- 全ての `autocmd` を `augroup` で囲むことを忘れないでください

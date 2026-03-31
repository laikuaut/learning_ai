# 第6章 演習：autocmdとファイルタイプ別設定

---

## 演習の目標

この演習では、以下のスキルを確認します。

- `autocmd` の基本的な構文を理解し、正しく記述できる
- `augroup` と `autocmd!` を使ったグループ化パターンを適用できる
- `FileType` イベントを使ったファイルタイプ別の設定ができる
- 言語ごとのインデント設定（Python / JavaScript / Go など）を記述できる
- `ftplugin` ディレクトリの仕組みを理解している
- カーソル位置の復元や末尾空白の自動削除などの実用的な autocmd を作成できる

---

## 基本問題

### 問題6-1：autocmd の構文理解

以下の `autocmd` の設定を読み、それぞれ何をしているか説明してください。

```vim
" 設定A
autocmd BufWritePre * :%s/\s\+$//e

" 設定B
autocmd FileType python setlocal expandtab tabstop=4 shiftwidth=4

" 設定C
autocmd BufNewFile,BufRead *.md setlocal filetype=markdown
```

**期待される出力例：**

```
設定A：ファイルを保存する直前（BufWritePre）に、すべてのファイル（*）に対して、
       行末の空白文字を削除する置換コマンドを実行する。
       /e フラグにより、マッチしない場合もエラーを出さない。

設定B：ファイルタイプが python と判定されたとき、
       タブをスペースに展開（expandtab）、タブ幅を4（tabstop=4）、
       自動インデント幅を4（shiftwidth=4）に設定する。
       setlocal により、そのバッファにのみ設定が適用される。

設定C：新規ファイル作成時（BufNewFile）または既存ファイル読み込み時（BufRead）に、
       拡張子が .md のファイルのファイルタイプを markdown に設定する。
```

<details>
<summary>ヒント</summary>

- `autocmd` の構文は `autocmd {イベント} {パターン} {コマンド}` です
- `BufWritePre` は「バッファを書き込む前」に発生するイベントです
- `FileType` は「ファイルタイプが判定されたとき」に発生するイベントです
- `BufNewFile` と `BufRead` はそれぞれ「新規ファイル作成時」「ファイル読み込み時」に発生します
- `setlocal` は現在のバッファにのみ設定を適用します（`set` はグローバル）

</details>

<details>
<summary>解答例</summary>

```
設定A：autocmd BufWritePre * :%s/\s\+$//e
  - イベント：BufWritePre（ファイル保存の直前）
  - パターン：*（すべてのファイル）
  - コマンド：:%s/\s\+$//e
    - %s → ファイル全体を対象に置換
    - \s\+$ → 行末の1つ以上の空白文字にマッチ
    - // → 空文字列に置換（削除）
    - e → マッチしなくてもエラーを出さないフラグ

設定B：autocmd FileType python setlocal expandtab tabstop=4 shiftwidth=4
  - イベント：FileType python（ファイルタイプがpythonと判定されたとき）
  - コマンド：setlocal で以下を現在バッファに設定
    - expandtab → Tab キーでスペースを入力
    - tabstop=4 → タブ文字の表示幅を4に
    - shiftwidth=4 → 自動インデントの幅を4に

設定C：autocmd BufNewFile,BufRead *.md setlocal filetype=markdown
  - イベント：BufNewFile,BufRead（新規作成時 または ファイル読み込み時）
  - パターン：*.md（拡張子が .md のファイル）
  - コマンド：ファイルタイプを markdown に設定
```

</details>

---

### 問題6-2：augroup と autocmd! パターン

以下の2つの設定を比較し、なぜ設定Bが推奨されるのか説明してください。

```vim
" 設定A（問題あり）
autocmd FileType python setlocal expandtab tabstop=4 shiftwidth=4
autocmd FileType python setlocal colorcolumn=80

" 設定B（推奨パターン）
augroup PythonSettings
  autocmd!
  autocmd FileType python setlocal expandtab tabstop=4 shiftwidth=4
  autocmd FileType python setlocal colorcolumn=80
augroup END
```

(1) 設定Aで `.vimrc` を `:source ~/.vimrc` で再読み込みすると何が起きますか。
(2) `autocmd!` は何をしていますか。
(3) `augroup` を使う利点を説明してください。

**期待される出力例：**

```
(1) autocmd が重複登録される。再読み込みのたびに同じ autocmd が追加され、
    Pythonファイルを開くたびに同じ処理が複数回実行されてしまう。

(2) autocmd! は、そのグループ内の既存の autocmd をすべて削除する。
    これにより、再読み込み時に古い autocmd が残ることを防ぐ。

(3) augroup の利点：
    - autocmd をグループとして管理でき、一括削除が可能
    - autocmd! と組み合わせることで、再読み込み時の重複登録を防止
    - 関連する autocmd をまとめて可読性が向上
```

<details>
<summary>ヒント</summary>

- `.vimrc` を `:source` で再読み込みすると、すべてのコマンドが再実行されます
- `autocmd` は追加型のコマンドです。同じ設定を再度実行すると、重複して登録されます
- `augroup グループ名 ... augroup END` で autocmd をグループ化できます
- `autocmd!` はグループ内で実行すると、そのグループの autocmd をすべて削除します

</details>

<details>
<summary>解答例</summary>

```
(1) 設定Aでは `:source ~/.vimrc` を実行するたびに autocmd が追加登録される。
    例えば3回再読み込みすると、同じ autocmd が3つ登録され、
    Pythonファイルを開くたびに各設定が3回実行される。
    これはパフォーマンスの低下や予期しない動作の原因になる。

(2) autocmd! は「このグループに属する autocmd をすべて削除する」コマンド。
    augroup 内の先頭で autocmd! を実行することで、
    以前に登録された同グループの autocmd を一度クリアしてから
    新しい autocmd を登録する。これにより重複登録を防止できる。

(3) augroup を使う利点：
    - 重複防止：autocmd! と組み合わせて再読み込み時の重複を防げる
    - 管理性：関連する autocmd をグループとしてまとめて管理できる
    - 一括操作：:autocmd! グループ名 でグループ内の autocmd を一括削除できる
    - 可読性：設定の意図が明確になる
```

**推奨テンプレート：**

```vim
augroup グループ名
  autocmd!           " グループ内の既存 autocmd をクリア
  autocmd イベント パターン コマンド
  autocmd イベント パターン コマンド
augroup END
```

</details>

---

## 応用問題

### 問題6-3：ファイルタイプ別インデント設定

以下の言語に対して、それぞれ適切なインデント設定を `autocmd` で記述してください。`augroup` と `autocmd!` パターンを使用すること。

| 言語 | タブ/スペース | 幅 | 追加設定 |
|---|---|---|---|
| Python | スペース | 4 | 80桁にカラムライン表示 |
| JavaScript | スペース | 2 | ― |
| Go | タブ | 4 | ― |
| Makefile | タブ | 8 | ― |
| HTML | スペース | 2 | テキスト折り返し無効 |

**期待される出力例：**

```vim
augroup FileTypeIndent
  autocmd!
  autocmd FileType python     setlocal expandtab   tabstop=4 shiftwidth=4 colorcolumn=80
  autocmd FileType javascript setlocal expandtab   tabstop=2 shiftwidth=2
  autocmd FileType go         setlocal noexpandtab tabstop=4 shiftwidth=4
  autocmd FileType make       setlocal noexpandtab tabstop=8 shiftwidth=8
  autocmd FileType html       setlocal expandtab   tabstop=2 shiftwidth=2 nowrap
augroup END
```

<details>
<summary>ヒント</summary>

- `expandtab` はタブキーでスペースを挿入、`noexpandtab` はタブ文字を挿入します
- `tabstop` はタブ文字の表示幅、`shiftwidth` は自動インデントの幅です
- `colorcolumn=80` は80桁目に縦線を表示します
- `nowrap` は行の折り返し表示を無効にします
- Go と Makefile はタブ文字を使うのが言語の慣例です
- FileType で使うファイルタイプ名は `:set filetype?` で確認できます

</details>

<details>
<summary>解答例</summary>

```vim
" ファイルタイプ別のインデント設定
" augroup でグループ化し、autocmd! で重複登録を防止する
augroup FileTypeIndent
  autocmd!

  " Python：スペース4、PEP 8 に従い80桁にカラムライン
  " expandtab → Tab キーでスペースを挿入
  autocmd FileType python setlocal expandtab tabstop=4 shiftwidth=4 colorcolumn=80

  " JavaScript：スペース2（Prettier 等のデフォルトに合わせる）
  autocmd FileType javascript setlocal expandtab tabstop=2 shiftwidth=2

  " Go：タブ4（gofmt がタブを使用するため noexpandtab）
  " Go ではタブを使うのが公式のスタイルガイド
  autocmd FileType go setlocal noexpandtab tabstop=4 shiftwidth=4

  " Makefile：タブ8（Makefile はタブ文字が構文的に必須）
  " スペースに変換するとエラーになるため、必ず noexpandtab にする
  autocmd FileType make setlocal noexpandtab tabstop=8 shiftwidth=8

  " HTML：スペース2、折り返し無効
  " nowrap → 長い行を折り返さず、横スクロールで表示
  autocmd FileType html setlocal expandtab tabstop=2 shiftwidth=2 nowrap
augroup END
```

**よくある間違い：** Makefile の FileType 名は `makefile` ではなく `make` です。`:set filetype?` で正確な名前を確認する習慣をつけましょう。

</details>

---

### 問題6-4：カーソル位置の復元

ファイルを開いたとき、前回閉じた位置にカーソルを自動的に復元する `autocmd` を作成してください。以下の条件を満たすこと。

1. 前回のカーソル位置が有効な場合のみ復元する（ファイルの範囲内であること）
2. コミットメッセージ（`gitcommit`）では復元しない（常に先頭から書き始めるため）
3. `augroup` と `autocmd!` パターンを使用すること

**期待される出力例：**

```vim
augroup RestoreCursor
  autocmd!
  autocmd BufReadPost *
    \ if line("'\"") >= 1 && line("'\"") <= line("$") && &filetype != 'gitcommit'
    \ |   execute "normal! g`\""
    \ | endif
augroup END
```

<details>
<summary>ヒント</summary>

- `'\"` は前回カーソルがあった位置を記録する特殊マーク（`"` マーク）です
- `line("'\"")` は `"` マークの行番号を返します（マークが無い場合は 0）
- `line("$")` はファイルの最終行番号を返します
- `g\`"` は `"` マークの位置にジャンプするコマンドです
- `\` は `.vimrc` での行継続（前の行からの続き）を示します
- `BufReadPost` はファイル読み込み完了後のイベントです

</details>

<details>
<summary>解答例</summary>

```vim
" ファイルを開いたとき、前回のカーソル位置を復元する
" Vimは ~/.viminfo（または ~/.vim/viminfo）にカーソル位置を自動保存している
augroup RestoreCursor
  autocmd!
  " BufReadPost：ファイルの読み込みが完了した後に実行
  " *：すべてのファイルが対象
  autocmd BufReadPost *
    \ if line("'\"") >= 1 && line("'\"") <= line("$") && &filetype != 'gitcommit'
    \ |   execute "normal! g`\""
    \ | endif
augroup END
```

**各部分の解説：**

```
line("'\"") >= 1          → " マーク（前回位置）が存在する（0 でない）
line("'\"") <= line("$")  → マークの行がファイルの最終行以内（ファイルが
                             短くなっていた場合の対策）
&filetype != 'gitcommit'  → git のコミットメッセージでは復元しない
                             （毎回先頭から書き始めるのが自然なため）
execute "normal! g`\""    → " マークの位置にジャンプ
                             g` はマーク位置にジャンプするコマンド
```

**補足：** Vim 8.2.3519 以降では `defaults.vim` にこの機能が含まれていますが、カスタム `.vimrc` を使用している場合は `defaults.vim` が読み込まれないため、自分で記述する必要があります。

</details>

---

### 問題6-5：ftplugin ディレクトリの活用

`autocmd FileType` で設定が増えてくると `.vimrc` が長くなります。`ftplugin` ディレクトリを使って設定を分離する方法について、以下の問いに答えてください。

1. Python 用のファイルタイププラグインを配置するファイルパスを答えてください
2. そのファイルに以下の設定を記述してください
   - スペース4、80桁カラムライン
   - `<Leader>r` で現在のファイルを Python で実行
3. `ftplugin` のファイル内で `setlocal` を使うべき理由を説明してください

**期待される出力例：**

```
1. ~/.vim/ftplugin/python.vim（または ~/.vim/after/ftplugin/python.vim）

2. ファイルの内容：
```

```vim
" ~/.vim/ftplugin/python.vim
setlocal expandtab tabstop=4 shiftwidth=4
setlocal colorcolumn=80

nnoremap <buffer> <Leader>r :!python3 %<CR>
```

```
3. setlocal を使う理由：
   set はグローバル設定を変更するため、他のファイルタイプのバッファにも
   影響してしまう。setlocal を使えば現在のバッファにのみ設定が適用され、
   ファイルタイプ別の設定として正しく機能する。
```

<details>
<summary>ヒント</summary>

- `ftplugin` ディレクトリは `~/.vim/ftplugin/` に配置します
- ファイル名は `{ファイルタイプ}.vim` にします（例：`python.vim`）
- `<buffer>` を使ったマッピングは、そのバッファでのみ有効です
- `%` はコマンドラインで現在のファイル名に展開されます
- `filetype plugin on` が `.vimrc` に設定されている必要があります

</details>

<details>
<summary>解答例</summary>

```
1. ~/.vim/ftplugin/python.vim
   （デフォルトの設定を上書きしたい場合は ~/.vim/after/ftplugin/python.vim）
```

```vim
" ~/.vim/ftplugin/python.vim
" このファイルは Python ファイルを開いたときに自動的に読み込まれる
" 前提条件：.vimrc に filetype plugin on が設定されていること

" インデント設定
" setlocal を使って現在のバッファにのみ適用
setlocal expandtab tabstop=4 shiftwidth=4 softtabstop=4

" 80桁にカラムラインを表示（PEP 8 のスタイルガイドに準拠）
setlocal colorcolumn=80

" <Leader>r で現在の Python ファイルを実行
" <buffer> により、このバッファでのみ有効なマッピングになる
" % は現在のファイル名に展開される
nnoremap <buffer> <Leader>r :!python3 %<CR>
```

```
3. setlocal を使うべき理由：
   - set はグローバル設定を変更する。例えば set tabstop=4 とすると、
     その後に開く JavaScript ファイルにも tabstop=4 が適用されてしまう
   - setlocal はそのバッファ（ファイル）にのみ設定を適用する
   - 同様に、マッピングには <buffer> を付けてバッファローカルにする
   - ftplugin では必ず setlocal と <buffer> を使うのがベストプラクティス
```

**ディレクトリ構成例：**

```
~/.vim/
├── ftplugin/
│   ├── python.vim      ← Pythonファイル用の設定
│   ├── javascript.vim  ← JavaScriptファイル用の設定
│   ├── go.vim          ← Goファイル用の設定
│   └── markdown.vim    ← Markdownファイル用の設定
└── vimrc
```

</details>

---

## チャレンジ問題

### 問題6-6：実用的な autocmd の総合設定

以下の要件をすべて満たす `autocmd` 設定を `.vimrc` に記述してください。すべて `augroup` を使い、適切にグループ化すること。

1. **末尾空白の自動削除**：ファイル保存時に行末の空白を自動削除する（ただし、Markdown ファイルは除外する。Markdown では行末の2つのスペースが改行を意味するため）
2. **自動的に親ディレクトリを作成**：ファイルを保存するとき、ディレクトリが存在しなければ自動的に作成する
3. **ファイルタイプ別の設定**：Python、JavaScript、Go、Markdown に対して適切なインデントとオプションを設定する
4. **カーソル位置の復元**：前回の編集位置を復元する（gitcommit を除く）

**期待される出力例：**

```vim
" --- 末尾空白の自動削除 ---
augroup TrimWhitespace
  autocmd!
  autocmd BufWritePre * if &filetype != 'markdown'
    \ | %s/\s\+$//e
    \ | endif
augroup END

" --- 親ディレクトリの自動作成 ---
augroup AutoMkdir
  autocmd!
  autocmd BufWritePre * call mkdir(expand('<afile>:p:h'), 'p')
augroup END

" --- ファイルタイプ別設定 ---
augroup FileTypeSettings
  autocmd!
  autocmd FileType python     setlocal expandtab   tabstop=4 shiftwidth=4 colorcolumn=80
  autocmd FileType javascript setlocal expandtab   tabstop=2 shiftwidth=2
  autocmd FileType go         setlocal noexpandtab tabstop=4 shiftwidth=4
  autocmd FileType markdown   setlocal expandtab   tabstop=2 shiftwidth=2 wrap spell
augroup END

" --- カーソル位置の復元 ---
augroup RestoreCursor
  autocmd!
  autocmd BufReadPost *
    \ if line("'\"") >= 1 && line("'\"") <= line("$") && &filetype != 'gitcommit'
    \ |   execute "normal! g`\""
    \ | endif
augroup END
```

<details>
<summary>ヒント</summary>

- 機能ごとに別の `augroup` でグループ化すると、管理しやすくなります
- Markdown では行末のスペース2つが `<br>` 相当の改行になるため、空白削除から除外します
- `mkdir()` の第2引数 `'p'` は、`mkdir -p` と同じで親ディレクトリも再帰的に作成します
- `expand('<afile>:p:h')` は、保存対象のファイルのディレクトリパスに展開されます
- Markdown では `spell`（スペルチェック）と `wrap`（行折り返し）を有効にすると便利です

</details>

<details>
<summary>解答例</summary>

```vim
" ==============================================================================
" autocmd 総合設定
" 機能ごとに augroup を分けて管理しやすくする
" ==============================================================================

" --- 末尾空白の自動削除 ---
" ファイル保存時に行末の余分な空白を自動削除
" Markdown は除外（行末スペース2つが改行 <br> の意味を持つため）
augroup TrimWhitespace
  autocmd!
  autocmd BufWritePre * if &filetype != 'markdown'
    \ | %s/\s\+$//e
    \ | endif
augroup END

" --- 親ディレクトリの自動作成 ---
" 存在しないディレクトリにファイルを保存しようとしたとき、
" 自動的にディレクトリを作成する（mkdir -p 相当）
" 例：:e new_dir/sub_dir/file.txt → new_dir/sub_dir/ が自動作成される
augroup AutoMkdir
  autocmd!
  " expand('<afile>:p:h')
  "   <afile> → 保存対象のファイル名
  "   :p      → フルパスに展開
  "   :h      → ディレクトリ部分のみ取得（head）
  " mkdir() の 'p' フラグで親ディレクトリも再帰的に作成
  autocmd BufWritePre * call mkdir(expand('<afile>:p:h'), 'p')
augroup END

" --- ファイルタイプ別設定 ---
" 言語ごとに適切なインデント幅とオプションを設定
augroup FileTypeSettings
  autocmd!
  " Python：PEP 8 準拠（スペース4、80桁ライン）
  autocmd FileType python setlocal expandtab tabstop=4 shiftwidth=4 colorcolumn=80

  " JavaScript：スペース2（業界標準）
  autocmd FileType javascript setlocal expandtab tabstop=2 shiftwidth=2

  " Go：タブ4（gofmt の公式スタイル）
  autocmd FileType go setlocal noexpandtab tabstop=4 shiftwidth=4

  " Markdown：スペース2、折り返し有効、スペルチェック有効
  autocmd FileType markdown setlocal expandtab tabstop=2 shiftwidth=2 wrap spell
augroup END

" --- カーソル位置の復元 ---
" ファイルを開いたとき、前回の編集位置にカーソルを復元する
" gitcommit（コミットメッセージ）では常に先頭から書くため除外
augroup RestoreCursor
  autocmd!
  autocmd BufReadPost *
    \ if line("'\"") >= 1 && line("'\"") <= line("$") && &filetype != 'gitcommit'
    \ |   execute "normal! g`\""
    \ | endif
augroup END
```

**設計のポイント：**

```
┌──────────────────────────────────────────────────────┐
│ augroup の分け方のベストプラクティス                 │
├──────────────────────────────────────────────────────┤
│ 1. 機能ごとに別の augroup にする                    │
│    → 特定の機能だけ無効にしたい場合に便利            │
│                                                      │
│ 2. グループ名は内容を表す分かりやすい名前にする      │
│    → TrimWhitespace, RestoreCursor など              │
│                                                      │
│ 3. 必ず autocmd! を先頭に書く                        │
│    → :source ~/.vimrc での再読み込みに対応            │
│                                                      │
│ 4. setlocal と <buffer> を使う                       │
│    → グローバル設定を汚染しない                      │
└──────────────────────────────────────────────────────┘
```

</details>

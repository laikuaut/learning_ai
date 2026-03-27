# 第1章 演習：Bashの基本と環境設定

---

## 演習の目標

この演習では、以下のスキルを確認します。

- Bashのバージョンを確認し、シェルの基本情報を取得できる
- 設定ファイル（`.bashrc`、`.bash_profile`など）の違いを理解している
- エイリアスを作成・管理できる
- プロンプト（PS1）をカスタマイズできる
- コマンド履歴を効率的に活用できる
- `.bashrc` に実用的な設定を記述できる

---

## 基本問題

### 問題1：Bashのバージョン確認

以下の要件を満たすコマンドを実行してください。

1. Bashのバージョンを表示する（2つの方法で）
2. 現在使用しているシェルのパスを確認する

**期待される出力例：**

```
# 方法1
GNU bash, version 5.2.15(1)-release (x86_64-pc-linux-gnu)
...

# 方法2
5.2.15(1)-release

# 使用中のシェルパス
/bin/bash
```

<details>
<summary>ヒント</summary>

- `bash --version` コマンドと `$BASH_VERSION` 変数の2つの方法があります
- 現在のシェルパスは `$SHELL` 変数または `$0` で確認できます

</details>

<details>
<summary>解答例</summary>

```bash
# 方法1：bash --version コマンドで詳細なバージョン情報を表示
bash --version

# 方法2：BASH_VERSION 変数でバージョン文字列のみ表示
echo "$BASH_VERSION"

# 現在使用しているシェルのパスを表示
# $SHELL はログインシェルのパスを保持する環境変数
echo "$SHELL"
```

</details>

---

### 問題2：設定ファイルの違い

次の設定ファイルについて、それぞれ「いつ読み込まれるか」を答えてください。

1. `~/.bash_profile`
2. `~/.bashrc`
3. `~/.bash_logout`
4. `/etc/profile`

また、以下のコマンドを実行して、自分の環境にどの設定ファイルが存在するか確認してください。

**期待される出力例：**

```
/home/user/.bashrc は存在します
/home/user/.bash_profile は存在しません
/home/user/.bash_logout は存在します
/etc/profile は存在します
```

<details>
<summary>ヒント</summary>

- ファイルの存在確認には `test -f` または `[ -f ]` を使います
- `&&` と `||` で成功時・失敗時の処理を分けられます

</details>

<details>
<summary>解答例</summary>

```bash
# 各設定ファイルの役割（回答）：
# 1. ~/.bash_profile : ログインシェル起動時に1回だけ読み込まれる
# 2. ~/.bashrc       : 対話型の非ログインシェル起動時に毎回読み込まれる
# 3. ~/.bash_logout  : ログインシェル終了時に読み込まれる
# 4. /etc/profile    : 全ユーザー共通のログインシェル起動時設定

# 設定ファイルの存在確認スクリプト
# -f はファイルが存在し通常ファイルであるかを判定するテスト演算子
for file in ~/.bashrc ~/.bash_profile ~/.bash_logout /etc/profile; do
    if [ -f "$file" ]; then
        echo "$file は存在します"
    else
        echo "$file は存在しません"
    fi
done
```

</details>

---

### 問題3：エイリアスの作成

以下のエイリアスを作成し、動作を確認してください。

1. `ll` → `ls -la` の短縮形
2. `cls` → 画面をクリアする
3. `myip` → 自分のIPアドレスを表示する（`hostname -I` を使用）
4. 現在設定されているエイリアスの一覧を表示する

**期待される出力例：**

```
# alias 一覧表示（抜粋）
alias cls='clear'
alias ll='ls -la'
alias myip='hostname -I'
```

<details>
<summary>ヒント</summary>

- `alias 名前='コマンド'` で設定します
- `alias` を引数なしで実行すると一覧表示されます
- `unalias 名前` で解除できます

</details>

<details>
<summary>解答例</summary>

```bash
# エイリアスの作成
# alias コマンドで短縮名を定義する
alias ll='ls -la'      # ls -la を ll で実行できるようにする
alias cls='clear'       # 画面クリアの短縮形
alias myip='hostname -I' # IPアドレス表示の短縮形

# 動作確認：ll を実行
ll

# 設定されているエイリアスの一覧を表示
# 引数なしの alias コマンドは全エイリアスを表示する
alias

# エイリアスの削除（不要になった場合）
# unalias cls
```

</details>

---

## 応用問題

### 問題4：PS1プロンプトのカスタマイズ

以下の要件を満たすPS1プロンプトを設定してください。

1. ユーザー名、ホスト名、現在のディレクトリを表示する
2. 色付きで表示する（ユーザー名を緑、ディレクトリをシアンにする）
3. プロンプトの末尾に `$` を表示する

**期待される出力例：**

```
user@myhost:~/projects$
```

（上記の `user` が緑色、`~/projects` がシアン色で表示されます）

<details>
<summary>ヒント</summary>

- PS1で使えるエスケープシーケンス：`\u`（ユーザー名）、`\h`（ホスト名）、`\w`（カレントディレクトリ）
- 色コード：`\[\e[32m\]`（緑）、`\[\e[36m\]`（シアン）、`\[\e[0m\]`（リセット）
- `\[...\]` で囲むと、Bashが表示幅の計算から除外します

</details>

<details>
<summary>解答例</summary>

```bash
# PS1 プロンプトのカスタマイズ
# \u : 現在のユーザー名
# \h : ホスト名（最初の . まで）
# \w : カレントディレクトリ（ホームは ~ で表示）
# \[\e[32m\] : 緑色開始（\[...\] は表示幅計算から除外する記法）
# \[\e[36m\] : シアン色開始
# \[\e[0m\]  : 色をリセット（これを忘れると以降すべて色付きになる）

PS1='\[\e[32m\]\u\[\e[0m\]@\h:\[\e[36m\]\w\[\e[0m\]\$ '

# 設定を確認
echo "現在のPS1: $PS1"

# 永続化したい場合は ~/.bashrc に追記する
# echo "PS1='\[\e[32m\]\u\[\e[0m\]@\h:\[\e[36m\]\w\[\e[0m\]\$ '" >> ~/.bashrc
```

</details>

---

### 問題5：コマンド履歴の活用

以下の操作を実行してください。

1. コマンド履歴の最新10件を表示する
2. 履歴から特定の文字列（`ls`）を含むコマンドを検索する
3. 履歴のサイズ（保存件数）を確認する
4. `HISTCONTROL` の設定値を確認し、重複コマンドを記録しない設定にする

**期待される出力例：**

```
# 最新10件
 1001  cd /home/user
 1002  ls -la
 1003  pwd
 ...

# ls を含む履歴
  502  ls -la /tmp
  601  ls *.txt
  ...

# 履歴サイズ
HISTSIZE=1000
HISTFILESIZE=2000

# HISTCONTROL の設定
HISTCONTROL=ignoreboth
```

<details>
<summary>ヒント</summary>

- `history` コマンドに件数を指定できます
- `history | grep パターン` で検索できます
- `HISTSIZE`、`HISTFILESIZE` で履歴サイズを確認します
- `HISTCONTROL` には `ignoredups`、`ignorespace`、`ignoreboth` などがあります

</details>

<details>
<summary>解答例</summary>

```bash
# 1. コマンド履歴の最新10件を表示
# history コマンドに数値を渡すと最新N件を表示する
history 10

# 2. 履歴から "ls" を含むコマンドを検索
# パイプで grep に渡してフィルタリングする
history | grep "ls"

# 3. 履歴の保存件数を確認
# HISTSIZE はメモリ上の履歴数、HISTFILESIZE はファイルの履歴数
echo "HISTSIZE=$HISTSIZE"
echo "HISTFILESIZE=$HISTFILESIZE"

# 4. HISTCONTROL の確認と設定
# ignoredups  : 直前と同じコマンドを記録しない
# ignorespace : スペースで始まるコマンドを記録しない
# ignoreboth  : 上記の両方を有効にする
echo "現在の設定: HISTCONTROL=$HISTCONTROL"

# 重複を記録しない設定にする
HISTCONTROL=ignoreboth
echo "変更後: HISTCONTROL=$HISTCONTROL"
```

</details>

---

### 問題6：.bashrcの実用的な設定

以下の内容を含む `.bashrc` の設定スニペットを作成してください（直接 `.bashrc` を編集せず、スクリプトとして作成してかまいません）。

1. よく使うエイリアスを3つ以上定義する
2. `PATH` に `~/bin` を追加する（重複追加を防ぐ）
3. 履歴の設定（サイズ、重複排除、タイムスタンプ表示）を行う

**期待される出力例：**

```
# === エイリアス設定 ===
alias ll='ls -la'
alias la='ls -A'
alias ..='cd ..'

# === PATH 設定 ===
PATH に ~/bin を追加しました

# === 履歴設定 ===
HISTSIZE=5000
HISTFILESIZE=10000
HISTCONTROL=ignoreboth
HISTTIMEFORMAT=%F %T
```

<details>
<summary>ヒント</summary>

- PATHの重複チェックには `case "$PATH" in *"$HOME/bin"*) ...` が使えます
- `HISTTIMEFORMAT` で履歴にタイムスタンプを付けられます

</details>

<details>
<summary>解答例</summary>

```bash
#!/bin/bash
# .bashrc 設定スニペットの例

# === エイリアス設定 ===
# よく使うコマンドの短縮形を定義する
alias ll='ls -la'       # 詳細表示（隠しファイル含む）
alias la='ls -A'        # 隠しファイルのみ表示（. と .. を除く）
alias ..='cd ..'        # 1つ上のディレクトリに移動
alias ...='cd ../..'    # 2つ上のディレクトリに移動
alias grep='grep --color=auto'  # grep の結果を色付き表示

echo "# === エイリアス設定 ==="
alias ll la .. ... grep 2>/dev/null

# === PATH 設定 ===
# ~/bin をPATHに追加（すでに含まれていなければ）
# case文でPATHに ~/bin が含まれているかチェックする
echo ""
echo "# === PATH 設定 ==="
case "$PATH" in
    *"$HOME/bin"*)
        echo "PATH に ~/bin はすでに含まれています"
        ;;
    *)
        export PATH="$HOME/bin:$PATH"
        echo "PATH に ~/bin を追加しました"
        ;;
esac

# === 履歴設定 ===
# HISTSIZE      : メモリ上に保持する履歴の件数
# HISTFILESIZE  : ~/.bash_history に保存する最大行数
# HISTCONTROL   : ignoreboth = 重複と空白始まりを除外
# HISTTIMEFORMAT: 履歴にタイムスタンプを表示する書式
echo ""
echo "# === 履歴設定 ==="
HISTSIZE=5000
HISTFILESIZE=10000
HISTCONTROL=ignoreboth
HISTTIMEFORMAT="%F %T  "

echo "HISTSIZE=$HISTSIZE"
echo "HISTFILESIZE=$HISTFILESIZE"
echo "HISTCONTROL=$HISTCONTROL"
echo "HISTTIMEFORMAT=$HISTTIMEFORMAT"
```

</details>

---

## チャレンジ問題

### 問題7：シェル起動の流れを調査する

以下のスクリプトを作成して、ログインシェルと非ログインシェルで読み込まれるファイルの違いを確認してください。

1. 各設定ファイル（`/etc/profile`、`~/.bash_profile`、`~/.bashrc`、`~/.profile`）の存在を確認する
2. 現在のシェルがログインシェルかどうかを判定する
3. 判定結果に基づいて「読み込まれるファイルの順番」を表示する

**期待される出力例：**

```
=== シェル起動ファイル調査 ===

[ファイル存在チェック]
  /etc/profile     : 存在します
  ~/.bash_profile  : 存在しません
  ~/.bashrc        : 存在します
  ~/.profile       : 存在します
  ~/.bash_logout   : 存在します

[ログインシェル判定]
  現在のシェルはログインシェルではありません

[読み込み順序（非ログインシェルの場合）]
  1. ~/.bashrc
```

<details>
<summary>ヒント</summary>

- `shopt -q login_shell` でログインシェルかどうかを判定できます（終了ステータスで判断）
- ログインシェルの読み込み順：`/etc/profile` → `~/.bash_profile` or `~/.bash_login` or `~/.profile`
- 非ログインシェルの読み込み順：`~/.bashrc`

</details>

<details>
<summary>解答例</summary>

```bash
#!/bin/bash
# シェル起動ファイルの調査スクリプト

echo "=== シェル起動ファイル調査 ==="
echo ""

# 1. 各設定ファイルの存在確認
echo "[ファイル存在チェック]"
# チェック対象のファイルを配列に格納
files=(
    "/etc/profile"
    "$HOME/.bash_profile"
    "$HOME/.bash_login"
    "$HOME/.bashrc"
    "$HOME/.profile"
    "$HOME/.bash_logout"
)

for file in "${files[@]}"; do
    # printf で表示幅を揃える（-20s は左詰め20文字）
    if [ -f "$file" ]; then
        printf "  %-20s : 存在します\n" "$file"
    else
        printf "  %-20s : 存在しません\n" "$file"
    fi
done

echo ""

# 2. ログインシェルの判定
# shopt -q login_shell は、ログインシェルなら終了ステータス0を返す
echo "[ログインシェル判定]"
if shopt -q login_shell; then
    login_shell="yes"
    echo "  現在のシェルはログインシェルです"
else
    login_shell="no"
    echo "  現在のシェルはログインシェルではありません"
fi

echo ""

# 3. 読み込み順序の表示
if [ "$login_shell" = "yes" ]; then
    echo "[読み込み順序（ログインシェルの場合）]"
    echo "  1. /etc/profile"
    # Bashは以下の3つを順番に探し、最初に見つかったものだけ読む
    if [ -f "$HOME/.bash_profile" ]; then
        echo "  2. ~/.bash_profile （見つかったのでこれを読み込み）"
    elif [ -f "$HOME/.bash_login" ]; then
        echo "  2. ~/.bash_login （見つかったのでこれを読み込み）"
    elif [ -f "$HOME/.profile" ]; then
        echo "  2. ~/.profile （見つかったのでこれを読み込み）"
    fi
    echo "  ※ 終了時: ~/.bash_logout"
else
    echo "[読み込み順序（非ログインシェルの場合）]"
    echo "  1. ~/.bashrc"
fi
```

</details>

---

### 問題8：カスタムプロンプト関数の作成

Gitリポジトリ内にいるときに、ブランチ名をプロンプトに表示する仕組みを作成してください。

1. 現在のGitブランチ名を取得する関数 `git_branch` を定義する
2. その関数を使ってPS1を設定する
3. Gitリポジトリ外ではブランチ名を表示しないようにする

**期待される出力例：**

```
# Gitリポジトリ内の場合
user@host:~/myproject (main)$

# Gitリポジトリ外の場合
user@host:~/documents$
```

<details>
<summary>ヒント</summary>

- `git branch --show-current 2>/dev/null` で現在のブランチ名を取得できます
- 関数内で `local` 変数を使いましょう
- PS1の中で `$(関数名)` と書くと、プロンプト表示のたびに関数が実行されます

</details>

<details>
<summary>解答例</summary>

```bash
#!/bin/bash
# Gitブランチ表示付きカスタムプロンプト

# 現在のGitブランチ名を取得する関数
# Gitリポジトリ外では何も出力しない
git_branch() {
    # local で関数内ローカル変数を宣言する
    local branch
    # git branch --show-current で現在のブランチ名を取得
    # 2>/dev/null でGitリポジトリ外でのエラーメッセージを抑制
    branch=$(git branch --show-current 2>/dev/null)

    # ブランチ名が空でなければ表示する
    # -n は文字列が空でないことをテストする演算子
    if [ -n "$branch" ]; then
        echo " ($branch)"
    fi
}

# PS1 を設定
# \$(git_branch) : プロンプト表示のたびに git_branch 関数を実行
# シングルクォートで囲むことで、設定時ではなく表示時に展開される
PS1='\[\e[32m\]\u\[\e[0m\]@\h:\[\e[36m\]\w\[\e[33m\]$(git_branch)\[\e[0m\]\$ '

echo "プロンプトを設定しました。"
echo "Gitリポジトリ内に移動するとブランチ名が表示されます。"

# 動作テスト
echo ""
echo "=== 動作テスト ==="
echo "現在のディレクトリ: $(pwd)"
branch_result=$(git_branch)
if [ -n "$branch_result" ]; then
    echo "Gitブランチ:$branch_result"
else
    echo "ここはGitリポジトリではありません"
fi
```

</details>

---

## まとめ

この演習では以下の内容を確認しました。

| カテゴリ | 学んだこと |
|---|---|
| バージョン確認 | `bash --version`、`$BASH_VERSION` |
| 設定ファイル | `.bashrc`、`.bash_profile` の違いと読み込み順 |
| エイリアス | `alias`、`unalias` によるコマンド短縮 |
| プロンプト | PS1のエスケープシーケンスと色付け |
| コマンド履歴 | `history`、`HISTCONTROL`、`HISTTIMEFORMAT` |
| .bashrc | PATH設定、エイリアス、履歴設定の実践 |

# 第1章 演習：Gitの基本概念とセットアップ

---

## 基本問題

### 問題1: バージョン管理の概念

以下の説明のうち、**分散型バージョン管理システム（Git）**の特徴として正しいものをすべて選んでください。

a) リポジトリのコピーをローカルに持つため、オフラインでも作業できる
b) 中央サーバーが停止すると、全員が作業できなくなる
c) 各開発者がリポジトリの完全なコピーを持つ
d) コミット履歴はサーバーにのみ保存される
e) ブランチの作成・切り替えが高速に行える

<details>
<summary>解答</summary>

**a, c, e** が正しいです。

```
a) ○ - Gitはローカルにリポジトリの完全なコピーを持つため、オフラインでもコミットや履歴閲覧が可能です
b) × - これは集中型（SVN等）の特徴です。Gitではローカルで作業を継続できます
c) ○ - 「分散型」の名前の通り、各開発者が完全なリポジトリを持ちます
d) × - コミット履歴はローカルにも保存されます
e) ○ - Gitのブランチはポインタの移動で実現されるため非常に高速です
```

</details>

---

### 問題2: git init によるリポジトリの作成

新しいプロジェクト用のディレクトリを作成し、Gitリポジトリとして初期化してください。
初期化後、`.git` ディレクトリが作成されていることを確認してください。

期待される出力例：
```
Initialized empty Git repository in /home/user/my-project/.git/
.git
```

<details>
<summary>ヒント</summary>

`mkdir` でディレクトリを作成し、`git init` で初期化します。`ls -a` で隠しディレクトリを確認できます。

</details>

<details>
<summary>解答</summary>

```bash
# 1. プロジェクト用のディレクトリを作成
$ mkdir my-project

# 2. ディレクトリに移動
$ cd my-project

# 3. Gitリポジトリとして初期化
$ git init
Initialized empty Git repository in /home/user/my-project/.git/

# 4. .git ディレクトリが作成されていることを確認
$ ls -a | grep .git
.git

# 補足: .git ディレクトリの中身を確認
$ ls .git/
HEAD  branches  config  description  hooks  info  objects  refs
```

- `git init` はカレントディレクトリに `.git` ディレクトリを作成します
- `.git` ディレクトリにはリポジトリのすべての管理情報が含まれます
- このディレクトリを削除するとGit管理が解除されます

</details>

---

### 問題3: git config の設定

Gitのユーザー名とメールアドレスをグローバル設定として登録し、設定内容を確認してください。

期待される出力例：
```
user.name=田中太郎
user.email=tanaka@example.com
```

<details>
<summary>ヒント</summary>

`git config --global` で設定し、`git config --list` や `git config --global user.name` で確認できます。

</details>

<details>
<summary>解答</summary>

```bash
# 1. ユーザー名を設定
$ git config --global user.name "田中太郎"

# 2. メールアドレスを設定
$ git config --global user.email "tanaka@example.com"

# 3. 設定内容を確認（個別に確認する方法）
$ git config --global user.name
田中太郎

$ git config --global user.email
tanaka@example.com

# 4. 設定内容を一覧で確認
$ git config --list --global
user.name=田中太郎
user.email=tanaka@example.com
```

- `--global` はそのユーザーのすべてのリポジトリに適用される設定です
- 設定ファイルは `~/.gitconfig` に保存されます
- リポジトリ単位で上書きしたい場合は `--local`（デフォルト）を使います

</details>

---

### 問題4: .gitignore ファイルの作成

以下の要件を満たす `.gitignore` ファイルを作成してください。

- `node_modules/` ディレクトリを除外する
- `.env` ファイルを除外する
- 拡張子 `.log` のファイルをすべて除外する
- `dist/` ディレクトリを除外する
- ただし `dist/.gitkeep` は追跡対象にする

期待される `.gitignore` の内容例：
```
node_modules/
.env
*.log
dist/
!dist/.gitkeep
```

<details>
<summary>ヒント</summary>

`!` を行頭に付けると、直前のルールの例外（否定パターン）を指定できます。

</details>

<details>
<summary>解答</summary>

```bash
# .gitignore ファイルを作成
$ cat <<'EOF' > .gitignore
# 依存パッケージ
node_modules/

# 環境変数ファイル（秘密情報を含むため）
.env

# ログファイル
*.log

# ビルド成果物
dist/
# ただし dist ディレクトリ自体は保持する
!dist/.gitkeep
EOF

# 内容を確認
$ cat .gitignore
# 依存パッケージ
node_modules/

# 環境変数ファイル（秘密情報を含むため）
.env

# ログファイル
*.log

# ビルド成果物
dist/
# ただし dist ディレクトリ自体は保持する
!dist/.gitkeep

# dist/.gitkeep ファイルを作成しておく
$ mkdir -p dist
$ touch dist/.gitkeep
```

- `.gitignore` はプロジェクトルートに置くのが一般的です
- `#` でコメントを書けます。なぜ除外するか理由を添えると親切です
- `!` の否定パターンは、先に除外されたルールを上書きします
- `.gitkeep` は空ディレクトリをGit管理するための慣習的なファイル名です（Git自体に特別な意味はありません）

</details>

---

## 応用問題

### 問題5: プロジェクトの初期セットアップ

新しいWebアプリケーションプロジェクト `webapp` を一から準備してください。以下の手順をすべて実行してください。

1. `webapp` ディレクトリを作成してGitリポジトリを初期化する
2. デフォルトブランチ名を `main` に設定する
3. ユーザー名・メールアドレスをリポジトリローカルで設定する
4. 適切な `.gitignore` を作成する（`node_modules/`, `.env`, `*.log`, `.DS_Store`）
5. `README.md` を作成する
6. 最初のコミットを作成する

期待される最終出力例（`git log`）：
```
commit abc1234 (HEAD -> main)
Author: 開発者名 <dev@example.com>
Date:   ...

    Initial commit: プロジェクトの初期セットアップ
```

<details>
<summary>ヒント</summary>

`git init` の直後に `git branch -m main` でデフォルトブランチ名を変更できます。
または `git init -b main` で初期化時に指定することもできます。

</details>

<details>
<summary>解答</summary>

```bash
# 1. ディレクトリ作成とGitリポジトリの初期化（-b main でブランチ名を指定）
$ mkdir webapp
$ cd webapp
$ git init -b main
Initialized empty Git repository in /home/user/webapp/.git/

# 2. ローカル設定（このリポジトリ専用の設定）
$ git config --local user.name "開発者名"
$ git config --local user.email "dev@example.com"

# 3. .gitignore の作成
$ cat <<'EOF' > .gitignore
# 依存パッケージ
node_modules/

# 環境変数
.env
.env.local

# ログ
*.log

# OS固有ファイル
.DS_Store
Thumbs.db

# エディタ設定
.vscode/
.idea/
EOF

# 4. README.md の作成
$ cat <<'EOF' > README.md
# webapp

Webアプリケーションプロジェクト

## セットアップ

npm install
EOF

# 5. ステージングとコミット
$ git add .gitignore README.md
$ git commit -m "Initial commit: プロジェクトの初期セットアップ"
[main (root-commit) abc1234] Initial commit: プロジェクトの初期セットアップ
 2 files changed, 20 insertions(+)

# 6. 結果の確認
$ git log --oneline
abc1234 (HEAD -> main) Initial commit: プロジェクトの初期セットアップ
```

- `git init -b main` で最初からブランチ名を `main` に設定できます（Git 2.28以降）
- `--local` 設定は `.git/config` に保存され、グローバル設定より優先されます
- 最初のコミットには `.gitignore` と `README.md` を含めるのがベストプラクティスです

</details>

---

## チャレンジ問題

### 問題6: 複数プロジェクトでの Git 設定の使い分け

以下のシナリオに対応する設定を行ってください。

**シナリオ:** あなたは個人プロジェクトと会社プロジェクトの両方をGitで管理しています。

- 個人プロジェクト (`~/personal/blog`) では `my-name` / `my@personal.com` を使う
- 会社プロジェクト (`~/work/app`) では `会社の名前` / `name@company.com` を使う

それぞれのリポジトリで正しいユーザー情報が表示されることを確認してください。

期待される出力例：
```
# ~/personal/blog での確認
user.name=my-name
user.email=my@personal.com

# ~/work/app での確認
user.name=会社の名前
user.email=name@company.com
```

<details>
<summary>ヒント</summary>

方法1: 各リポジトリで `git config --local` を使って個別に設定する方法があります。
方法2: `~/.gitconfig` に `includeIf` ディレクティブを設定すると、ディレクトリパスによって自動的に設定を切り替えられます。

</details>

<details>
<summary>解答</summary>

**方法1: リポジトリごとの --local 設定（シンプルな方法）**

```bash
# 個人プロジェクトの設定
$ mkdir -p ~/personal/blog && cd ~/personal/blog
$ git init -b main
$ git config --local user.name "my-name"
$ git config --local user.email "my@personal.com"

# 会社プロジェクトの設定
$ mkdir -p ~/work/app && cd ~/work/app
$ git init -b main
$ git config --local user.name "会社の名前"
$ git config --local user.email "name@company.com"

# 確認
$ cd ~/personal/blog && git config user.name && git config user.email
my-name
my@personal.com

$ cd ~/work/app && git config user.name && git config user.email
会社の名前
name@company.com
```

**方法2: includeIf による自動切り替え（推奨・応用的な方法）**

```bash
# 会社用の設定ファイルを作成
$ cat <<'EOF' > ~/.gitconfig-work
[user]
    name = 会社の名前
    email = name@company.com
EOF

# グローバル設定に includeIf を追加
$ git config --global user.name "my-name"
$ git config --global user.email "my@personal.com"
$ git config --global --add includeIf."gitdir:~/work/".path "~/.gitconfig-work"

# 確認: ~/work/ 以下のリポジトリでは自動的に会社の設定が使われる
$ cd ~/work/app
$ git config user.name
会社の名前

$ cd ~/personal/blog
$ git config user.name
my-name
```

- 方法1はシンプルですが、新しいリポジトリを作るたびに設定が必要です
- 方法2は `includeIf` を使って、ディレクトリパスに基づいて自動切り替えできます
- 方法2では `gitdir:~/work/` のパス末尾の `/` が重要です（サブディレクトリ全体に適用される意味）
- 現場では方法2が推奨されます。設定忘れによるコミットミスを防げるためです

</details>

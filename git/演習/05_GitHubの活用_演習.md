# 第5章 演習：GitHubの活用

---

## 基本問題

### 問題1: リポジトリの作成とREADME.md

以下の手順を実行して、GitHubリポジトリを作成し、ローカルリポジトリと連携してください。

1. GitHub上で `my-first-project` という名前のパブリックリポジトリを作成してください（READMEなし）
2. ローカルでリポジトリを初期化し、以下の内容の `README.md` を作成してください
3. GitHubにプッシュしてください

README.mdの内容：
```markdown
# My First Project
プログラミング学習用のサンプルプロジェクトです。

## セットアップ
git clone https://github.com/<ユーザー名>/my-first-project.git

## ライセンス
MIT
```

期待される実行結果：
```
$ git remote -v
origin  https://github.com/<ユーザー名>/my-first-project.git (fetch)
origin  https://github.com/<ユーザー名>/my-first-project.git (push)
```

<details>
<summary>ヒント</summary>

`git remote add origin` でリモートリポジトリを登録できます。初回プッシュには `-u` オプションを付けます。GitHub CLI (`gh`) を使えばコマンドラインからリポジトリを作成できます。

</details>

<details>
<summary>解答</summary>

```bash
# 1. GitHub CLI でリポジトリを作成（Web UIでも可）
$ gh repo create my-first-project --public --clone
$ cd my-first-project

# 2. README.md を作成
$ cat << 'EOF' > README.md
# My First Project
プログラミング学習用のサンプルプロジェクトです。

## セットアップ
git clone https://github.com/<ユーザー名>/my-first-project.git

## ライセンス
MIT
EOF

# 3. コミットしてプッシュ
$ git add README.md
$ git commit -m "docs: READMEを追加"
$ git push -u origin main

# 4. リモートの確認
$ git remote -v
origin  https://github.com/<ユーザー名>/my-first-project.git (fetch)
origin  https://github.com/<ユーザー名>/my-first-project.git (push)
```

解説：
- `gh repo create --public --clone` でリポジトリ作成とクローンを一度に行えます
- Web UIで作成した場合は `git remote add origin <URL>` でリモートを登録します
- `-u` オプションにより、以降は `git push` だけでプッシュできます
- GitHub CLIを使う場合は事前に `gh auth login` で認証を済ませておきましょう

</details>

---

### 問題2: Issue の作成と管理

以下のシナリオに基づいて、GitHub Issue を作成してください。

- タイトル：「ログイン画面のバリデーションを追加する」
- ラベル：`enhancement`
- 担当者：自分自身
- 本文にはやるべきことをチェックリスト形式で記載

期待される Issue 本文：
```markdown
## 概要
ログイン画面にバリデーション機能を追加します。

## タスク
- [ ] メールアドレスの形式チェック
- [ ] パスワードの文字数チェック（8文字以上）
- [ ] エラーメッセージの表示
- [ ] ユニットテストの作成
```

<details>
<summary>ヒント</summary>

GitHub CLI (`gh`) を使うとコマンドラインから Issue を作成できます。`gh issue create` コマンドを確認してみましょう。ラベルが存在しない場合は `gh label create` で事前に作成できます。

</details>

<details>
<summary>解答</summary>

```bash
# ラベルが存在しない場合は作成
$ gh label create enhancement --description "機能追加" --color 0E8A16

# GitHub CLI を使った Issue 作成
$ gh issue create \
  --title "ログイン画面のバリデーションを追加する" \
  --label "enhancement" \
  --assignee "@me" \
  --body "## 概要
ログイン画面にバリデーション機能を追加します。

## タスク
- [ ] メールアドレスの形式チェック
- [ ] パスワードの文字数チェック（8文字以上）
- [ ] エラーメッセージの表示
- [ ] ユニットテストの作成"

# 作成した Issue の確認
$ gh issue list
$ gh issue view 1
```

解説：
- `--assignee "@me"` で自分自身をアサインできます
- Issue 本文のチェックリストはGitHub上で個別にチェック可能です
- ラベルは事前にリポジトリに存在する必要があります
- Issue番号は自動で採番されます。PR本文から `#1` のように参照できます

</details>

---

## 応用問題

### 問題3: プルリクエストの作成とレビュー

以下の手順でプルリクエスト（PR）を作成してください。

1. `feature/add-login` ブランチを作成する
2. `login.html` ファイルを追加してコミットする
3. GitHubにプッシュしてPRを作成する
4. PRの説明には Issue #1 への参照を含める

期待されるPRの内容：
```
タイトル: feat: ログイン画面を追加
本文:
  ## 変更内容
  - ログイン画面のHTMLを追加しました

  ## 関連Issue
  Closes #1
```

<details>
<summary>ヒント</summary>

PR本文に `Closes #1` と書くと、PRがマージされたときにIssue #1が自動でクローズされます。`Fixes` や `Resolves` でも同様の動作をします。

</details>

<details>
<summary>解答</summary>

```bash
# 1. ブランチを作成して切り替え
$ git switch -c feature/add-login

# 2. ファイルを追加してコミット
$ cat << 'EOF' > login.html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>ログイン</title>
</head>
<body>
  <h1>ログイン</h1>
  <form>
    <label for="email">メールアドレス</label>
    <input type="email" id="email" required>
    <label for="password">パスワード</label>
    <input type="password" id="password" required minlength="8">
    <button type="submit">ログイン</button>
  </form>
</body>
</html>
EOF

$ git add login.html
$ git commit -m "feat: ログイン画面を追加"

# 3. プッシュしてPRを作成
$ git push -u origin feature/add-login

$ gh pr create \
  --title "feat: ログイン画面を追加" \
  --body "## 変更内容
- ログイン画面のHTMLを追加しました

## 関連Issue
Closes #1"

# 4. PRの確認
$ gh pr view
```

解説：
- `Closes #1` によりマージ時にIssue #1が自動クローズされます
- `git switch -c` は `git checkout -b` と同じ機能ですが、よりモダンな書き方です
- レビュアーを指定する場合は `--reviewer <ユーザー名>` を追加します
- PRはマージ前にレビューを受けるのがチーム開発のベストプラクティスです

</details>

---

### 問題4: GitHub Actions で CI を設定する

以下のワークフローファイルを作成して、プッシュ時に自動でテストが実行されるようにしてください。

要件：
- `main` ブランチへのプッシュとPRで実行される
- Node.js 20 を使用する
- `npm ci` で依存関係をインストール
- `npm test` でテストを実行

期待されるファイルパス：`.github/workflows/ci.yml`

<details>
<summary>ヒント</summary>

GitHub Actionsのワークフローは `.github/workflows/` ディレクトリに YAML ファイルとして配置します。`actions/checkout` と `actions/setup-node` が基本的なアクションです。

</details>

<details>
<summary>解答</summary>

```bash
# ディレクトリを作成
$ mkdir -p .github/workflows

# ワークフローファイルを作成
$ cat << 'EOF' > .github/workflows/ci.yml
name: CI

# トリガー条件
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      # リポジトリのチェックアウト
      - uses: actions/checkout@v4

      # Node.js のセットアップ
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      # 依存関係のインストール
      - run: npm ci

      # テストの実行
      - run: npm test
EOF

# コミットしてプッシュ
$ git add .github/workflows/ci.yml
$ git commit -m "ci: GitHub ActionsでCI設定を追加"
$ git push
```

解説：
- `actions/checkout@v4` はリポジトリのコードを取得するための公式アクションです
- `cache: 'npm'` で `node_modules` のキャッシュが有効になり、ビルド時間が短縮されます
- `npm ci` は `package-lock.json` に基づいて厳密にインストールするため、CIに適しています
- ワークフローの実行状況は GitHub の「Actions」タブで確認できます

</details>

---

## チャレンジ問題

### 問題5: GitHub Pages でサイトを公開する

以下の手順で、GitHub Pages を使って静的サイトを公開してください。

1. `docs/index.html` を作成する
2. GitHub Actions を使ってデプロイするワークフローを作成する
3. サイトが公開されることを確認する

`docs/index.html` の内容：
```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Portfolio</title>
  <style>
    body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 2rem; }
    h1 { color: #333; }
  </style>
</head>
<body>
  <h1>My Portfolio</h1>
  <p>GitHub Pagesで公開したサイトです。</p>
</body>
</html>
```

期待される結果：
```
公開URL: https://<ユーザー名>.github.io/<リポジトリ名>/
```

<details>
<summary>ヒント</summary>

GitHub Pages は「Settings > Pages」から設定できます。GitHub Actions を使う方法では、`actions/configure-pages`、`actions/upload-pages-artifact`、`actions/deploy-pages` の3つのアクションを組み合わせます。

</details>

<details>
<summary>解答</summary>

```bash
# 1. ドキュメントディレクトリとHTMLファイルを作成
$ mkdir -p docs
$ cat << 'EOF' > docs/index.html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Portfolio</title>
  <style>
    body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 2rem; }
    h1 { color: #333; }
  </style>
</head>
<body>
  <h1>My Portfolio</h1>
  <p>GitHub Pagesで公開したサイトです。</p>
</body>
</html>
EOF

# 2. GitHub Actions のデプロイワークフローを作成
$ mkdir -p .github/workflows
$ cat << 'EOF' > .github/workflows/deploy-pages.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

# GitHub Pages へのデプロイ権限
permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    steps:
      - uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: 'docs'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
EOF

# 3. コミットしてプッシュ
$ git add docs/index.html .github/workflows/deploy-pages.yml
$ git commit -m "feat: GitHub Pagesでポートフォリオサイトを公開"
$ git push
```

解説：
- GitHub Pages の設定で「Source」を「GitHub Actions」に変更する必要があります
- `permissions` でワークフローにPages デプロイ権限を付与しています
- `environment: github-pages` はGitHubが自動的に作成する環境です
- デプロイ後、`https://<ユーザー名>.github.io/<リポジトリ名>/` でアクセスできます
- 公開には数分かかることがあります。Actions タブでデプロイ状況を確認してください

</details>

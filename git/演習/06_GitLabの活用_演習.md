# 第6章 演習：GitLabの活用

---

## 基本問題

### 問題1: GitLab プロジェクトの作成とクローン

以下の手順を実行して、GitLabにプロジェクトを作成し、ローカルにクローンしてください。

1. GitLabで `my-gitlab-project` という名前のプロジェクトを作成する
2. ローカルにクローンする
3. `README.md` を作成してプッシュする

期待される実行結果：
```
$ git remote -v
origin  https://gitlab.com/<ユーザー名>/my-gitlab-project.git (fetch)
origin  https://gitlab.com/<ユーザー名>/my-gitlab-project.git (push)

$ git log --oneline
abc1234 (HEAD -> main, origin/main) docs: READMEを追加
```

<details>
<summary>ヒント</summary>

GitLab CLIは `glab` コマンドで利用できます。`glab repo create` でプロジェクトを作成できます。Web UIの場合は「New project > Create blank project」から作成します。

</details>

<details>
<summary>解答</summary>

```bash
# 方法1: GitLab CLI (glab) を使う場合
$ glab repo create my-gitlab-project --public
$ git clone https://gitlab.com/<ユーザー名>/my-gitlab-project.git
$ cd my-gitlab-project

# 方法2: Web UIで作成後にクローンする場合
$ git clone https://gitlab.com/<ユーザー名>/my-gitlab-project.git
$ cd my-gitlab-project

# README.md を作成
$ cat << 'EOF' > README.md
# My GitLab Project
GitLab学習用のプロジェクトです。

## セットアップ
git clone https://gitlab.com/<ユーザー名>/my-gitlab-project.git
EOF

# コミットしてプッシュ
$ git add README.md
$ git commit -m "docs: READMEを追加"
$ git push -u origin main
```

解説：
- GitLabでは「プロジェクト」がGitHubの「リポジトリ」に相当します
- `glab` はGitLab公式CLIツールです。事前に `glab auth login` で認証が必要です
- SSHキーを登録している場合は `git@gitlab.com:<ユーザー名>/my-gitlab-project.git` でもクローンできます

</details>

---

### 問題2: マージリクエストの作成

以下の手順でマージリクエスト（MR）を作成してください。GitHubのプルリクエストに相当する機能です。

1. `feature/add-about-page` ブランチを作成する
2. `about.html` を追加してコミットする
3. GitLabにプッシュしてMRを作成する

期待されるMRの内容：
```
タイトル: feat: Aboutページを追加
説明:
  ## 変更内容
  - Aboutページを追加しました

  ## 関連Issue
  Closes #1
```

<details>
<summary>ヒント</summary>

`git push` 時に `-o merge_request.create` オプションを使うと、プッシュと同時にMRを作成できます。GitLab CLI (`glab`) の `glab mr create` でも作成可能です。

</details>

<details>
<summary>解答</summary>

```bash
# 1. ブランチを作成
$ git switch -c feature/add-about-page

# 2. ファイルを追加
$ cat << 'EOF' > about.html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>About</title>
</head>
<body>
  <h1>About</h1>
  <p>このプロジェクトについての説明ページです。</p>
</body>
</html>
EOF

$ git add about.html
$ git commit -m "feat: Aboutページを追加"

# 方法1: プッシュ時にMRを自動作成（GitLab固有の機能）
$ git push -u origin feature/add-about-page \
  -o merge_request.create \
  -o merge_request.title="feat: Aboutページを追加" \
  -o merge_request.description="## 変更内容
- Aboutページを追加しました

## 関連Issue
Closes #1"

# 方法2: GitLab CLI を使う場合
$ git push -u origin feature/add-about-page
$ glab mr create \
  --title "feat: Aboutページを追加" \
  --description "## 変更内容
- Aboutページを追加しました

## 関連Issue
Closes #1"
```

解説：
- GitLabではプルリクエストを「マージリクエスト（MR）」と呼びます
- `-o merge_request.create` はGitLabのプッシュオプションで、プッシュと同時にMRを作成できます
- `Closes #1` はGitHubと同様に、マージ時にIssueを自動クローズします
- MRにはレビュアーの指定、マイルストーンの設定、ラベル付けなどが可能です

</details>

---

## 応用問題

### 問題3: .gitlab-ci.yml の作成（基本的なパイプライン）

以下の要件を満たす `.gitlab-ci.yml` を作成して、GitLab CI/CD パイプラインを構築してください。

要件：
- Node.js 20 のDockerイメージを使用する
- `npm ci` で依存関係をインストール
- `npm test` でテストを実行する
- `main` ブランチへのプッシュとMRで実行される

期待されるファイル：`.gitlab-ci.yml`

<details>
<summary>ヒント</summary>

GitLab CI/CDの設定はリポジトリルートの `.gitlab-ci.yml` に記述します。`image` でDockerイメージを、`script` で実行するコマンドを指定します。GitHub Actionsと異なり、設定ファイルは1つだけです。

</details>

<details>
<summary>解答</summary>

```bash
# .gitlab-ci.yml を作成
$ cat << 'EOF' > .gitlab-ci.yml
# 使用するDockerイメージ
image: node:20

# パイプラインのステージ定義
stages:
  - test

# キャッシュ設定（ビルド時間短縮のため）
cache:
  paths:
    - node_modules/

# テストジョブ
test:
  stage: test
  script:
    # 依存関係のインストール
    - npm ci
    # テストの実行
    - npm test
  rules:
    # main ブランチへのプッシュ時に実行
    - if: '$CI_COMMIT_BRANCH == "main"'
    # マージリクエスト時に実行
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
EOF

# コミットしてプッシュ
$ git add .gitlab-ci.yml
$ git commit -m "ci: GitLab CI/CDのテストパイプラインを追加"
$ git push
```

解説：
- `image: node:20` でジョブ実行環境のDockerイメージを指定します
- `cache` で `node_modules/` をキャッシュすると、次回以降のパイプラインが高速化されます
- `rules` は `only/except` に代わるモダンな条件指定方法です
- `$CI_COMMIT_BRANCH` や `$CI_PIPELINE_SOURCE` はGitLabの定義済み変数です
- パイプラインの実行状況は「CI/CD > Pipelines」から確認できます

</details>

---

### 問題4: イシューボードの活用

以下のシナリオに基づいて、GitLabのイシューボードを構築してください。

1. 以下のラベルを作成する：`To Do`, `Doing`, `Review`, `Done`
2. 各ラベルに対応するIssueを作成する
3. イシューボードの構成を確認する

作成するIssue：
| Issue | ラベル |
|---|---|
| ログイン機能の実装 | `Doing` |
| ユーザー登録画面のデザイン | `To Do` |
| APIのエラーハンドリング | `Review` |

期待される結果：
```
$ glab issue list
#3  APIのエラーハンドリング         Review
#2  ユーザー登録画面のデザイン      To Do
#1  ログイン機能の実装              Doing
```

<details>
<summary>ヒント</summary>

GitLab CLIの `glab label create` でラベルを作成し、`glab issue create` でIssueを作成します。イシューボードはWeb UIの「Plan > Issue boards」から確認できます。

</details>

<details>
<summary>解答</summary>

```bash
# 1. ラベルの作成
$ glab label create "To Do" --color "#0000FF" --description "未着手のタスク"
$ glab label create "Doing" --color "#FFA500" --description "作業中のタスク"
$ glab label create "Review" --color "#800080" --description "レビュー待ちのタスク"
$ glab label create "Done" --color "#008000" --description "完了したタスク"

# 2. Issue の作成
$ glab issue create \
  --title "ログイン機能の実装" \
  --label "Doing" \
  --description "ログイン機能を実装します。"

$ glab issue create \
  --title "ユーザー登録画面のデザイン" \
  --label "To Do" \
  --description "ユーザー登録画面のUIデザインを作成します。"

$ glab issue create \
  --title "APIのエラーハンドリング" \
  --label "Review" \
  --description "API呼び出し時のエラーハンドリングを追加します。"

# 3. Issue 一覧の確認
$ glab issue list

# 4. イシューボードはWeb UIで確認
# URL: https://gitlab.com/<ユーザー名>/<プロジェクト名>/-/boards
```

解説：
- GitLabのイシューボードはラベルに基づいてカラム（列）を自動生成します
- ボードの各カラムにIssueをドラッグ&ドロップすると、自動的にラベルが付け替えられます
- デフォルトで「Open」と「Closed」のカラムが存在します
- カンバン方式のタスク管理を外部ツールなしで実現できるのがGitLabの利点です
- 複数のボードを作成して、チームやマイルストーンごとに管理することも可能です

</details>

---

## チャレンジ問題

### 問題5: 複数ステージのCI/CDパイプライン構築

以下の要件を満たす本格的なCI/CDパイプラインを `.gitlab-ci.yml` で構築してください。

要件：
- 3つのステージ：`build`、`test`、`deploy`
- `build` ステージ：`npm ci` と `npm run build` を実行
- `test` ステージ：`npm test` を実行（buildの成果物を利用）
- `deploy` ステージ：`main` ブランチの場合のみ実行
- 各ステージ間でビルド成果物を受け渡す

期待されるパイプラインの流れ：
```
[build] → [test] → [deploy]
                      ↑ main ブランチのみ
```

<details>
<summary>ヒント</summary>

GitLab CI/CDでは `artifacts` を使ってステージ間でファイルを受け渡せます。`dependencies` で依存するジョブを指定すると、そのジョブの成果物をダウンロードできます。`rules` で特定ブランチのみの実行条件を設定できます。

</details>

<details>
<summary>解答</summary>

```bash
$ cat << 'EOF' > .gitlab-ci.yml
# 使用するDockerイメージ
image: node:20

# パイプラインのステージ定義（実行順序）
stages:
  - build
  - test
  - deploy

# 全ジョブ共通のキャッシュ設定
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/

# ========== ビルドステージ ==========
build:
  stage: build
  script:
    - npm ci
    - npm run build
  artifacts:
    # ビルド成果物を後続ステージに渡す
    paths:
      - dist/
      - node_modules/
    # 成果物の保持期間
    expire_in: 1 hour

# ========== テストステージ ==========
test:unit:
  stage: test
  # build ジョブの成果物を利用
  dependencies:
    - build
  script:
    - npm test
  # テスト結果レポートの出力
  artifacts:
    when: always
    reports:
      junit: test-results.xml

test:lint:
  stage: test
  dependencies:
    - build
  script:
    - npx eslint . --format stylish

# ========== デプロイステージ ==========
deploy:
  stage: deploy
  dependencies:
    - build
  script:
    - echo "Deploying to production..."
    - echo "Deploy target -> dist/"
    # 実際のデプロイコマンドをここに記述
    # 例: rsync, scp, AWS CLI, kubectl など
  rules:
    # main ブランチへのプッシュ時のみ実行
    - if: '$CI_COMMIT_BRANCH == "main"'
  environment:
    name: production
    url: https://example.com
EOF

# コミットしてプッシュ
$ git add .gitlab-ci.yml
$ git commit -m "ci: 複数ステージのCI/CDパイプラインを構築"
$ git push
```

解説：
- `stages` の定義順にステージが実行されます。同一ステージ内のジョブは並列実行されます
- `artifacts` でビルド成果物を保存し、`dependencies` で後続ジョブに渡します
- `test:unit` と `test:lint` は同じ `test` ステージなので並列に実行されます
- `expire_in` で成果物の保持期間を設定し、ストレージを節約できます
- `environment` を設定すると、GitLabの「Deployments」画面でデプロイ履歴を追跡できます
- `rules` による条件分岐で、デプロイは `main` ブランチのみに限定しています
- `when: always` を指定すると、テストが失敗してもレポートが出力されます

</details>

---

### 問題6: GitLab Container Registry の活用

GitLab Container Registry を使って、Dockerイメージをビルドしてレジストリにプッシュするパイプラインを追加してください。

要件：
- `Dockerfile` を作成する
- パイプラインでDockerイメージをビルドする
- GitLabのContainer Registryにプッシュする

期待される結果：
```
イメージ: registry.gitlab.com/<ユーザー名>/<プロジェクト名>:latest
```

<details>
<summary>ヒント</summary>

GitLab CI/CDには `$CI_REGISTRY`、`$CI_REGISTRY_IMAGE` などのDocker関連の定義済み変数があります。`docker:dind`（Docker in Docker）サービスを使うと、パイプライン内でDockerコマンドを実行できます。

</details>

<details>
<summary>解答</summary>

```bash
# 1. Dockerfile を作成
$ cat << 'EOF' > Dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --production

COPY . .

EXPOSE 3000
CMD ["node", "server.js"]
EOF

# 2. .gitlab-ci.yml にDockerビルドジョブを追加
$ cat << 'EOF' >> .gitlab-ci.yml

# ========== Dockerイメージのビルドとプッシュ ==========
docker-build:
  stage: build
  image: docker:24
  services:
    # Docker in Docker サービス
    - docker:24-dind
  variables:
    DOCKER_TLS_CERTDIR: "/certs"
  before_script:
    # GitLab Container Registry にログイン
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    # イメージをビルド
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
    - docker build -t $CI_REGISTRY_IMAGE:latest .
    # レジストリにプッシュ
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
    - docker push $CI_REGISTRY_IMAGE:latest
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
EOF

# 3. コミットしてプッシュ
$ git add Dockerfile .gitlab-ci.yml
$ git commit -m "ci: DockerイメージのビルドとContainer Registryへのプッシュを追加"
$ git push
```

解説：
- `$CI_REGISTRY_USER` と `$CI_REGISTRY_PASSWORD` はGitLabが自動で提供する認証情報です
- `$CI_REGISTRY_IMAGE` は `registry.gitlab.com/<ユーザー名>/<プロジェクト名>` に展開されます
- `$CI_COMMIT_SHORT_SHA` でコミットハッシュをタグとして使い、バージョン管理できます
- `docker:24-dind` サービスにより、パイプライン内でDockerコマンドが使えます
- Container Registryの内容はWeb UIの「Deploy > Container Registry」から確認できます
- 本番環境では `latest` タグだけでなく、セマンティックバージョニング（例: `v1.2.3`）のタグも付けることを推奨します

</details>

# 第5章：GitHubの活用

## この章のゴール

- GitHub（ギットハブ）の基本機能を理解し、リポジトリの作成・管理ができるようになる
- プルリクエスト（Pull Request）を使ったコードレビューの流れを実践できるようになる
- Issue、GitHub Actions、GitHub Pages などの主要機能を活用できるようになる

---

## 5.1 GitHub とは

GitHub（ギットハブ）は、世界最大のコードホスティングサービス（code hosting service）です。Git リポジトリをクラウド上で管理し、チームでの共同開発を強力にサポートします。2018年に Microsoft が買収し、現在は Microsoft の傘下で運営されています。

```
┌─────────────────────────────────────────────────┐
│                   GitHub                         │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │リポジトリ │  │プルリク   │  │ Issue    │      │
│  │管理      │  │エスト    │  │管理      │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Actions  │  │ Pages    │  │セキュリティ│      │
│  │(CI/CD)   │  │(Web公開) │  │機能      │      │
│  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────┘
```

GitHub を使うメリットは以下のとおりです。

| メリット | 説明 |
|---|---|
| バックアップ | コードをクラウドに安全に保存できます |
| 共同開発 | 世界中の開発者とコードを共有・協力できます |
| コードレビュー | プルリクエストを通じて品質を向上させます |
| CI/CD | GitHub Actions で自動テスト・デプロイが可能です |
| 公開・共有 | オープンソースプロジェクトを簡単に公開できます |

---

## 5.2 アカウント作成とプロフィール設定

### アカウント作成手順

1. [https://github.com](https://github.com) にアクセスします
2. 「Sign up」をクリックします
3. メールアドレス、パスワード、ユーザー名を入力します
4. メール認証を完了します

### プロフィール設定のポイント

プロフィールは開発者としての名刺です。以下の項目を設定しましょう。

```
Settings → Profile で設定できる項目：
  - Name（表示名）
  - Bio（自己紹介文）
  - Company（所属）
  - Location（居住地）
  - Website（Webサイト）
  - Social accounts（SNSアカウント）
```

### プロフィール README の作成

ユーザー名と同じ名前のリポジトリを作成し、`README.md` を置くと、プロフィールページに表示されます。これは自己紹介として非常に有効です。

```bash
# ユーザー名が "tanaka" の場合
# GitHub 上で "tanaka" という名前のリポジトリを作成し、README.md を追加する

# ローカルで作成する場合
mkdir tanaka && cd tanaka
git init
cat > README.md << 'EOF'
### こんにちは！田中です 👋
- 🔭 現在はWebアプリケーション開発をしています
- 🌱 TypeScript と React を勉強中です
- 📫 連絡先: tanaka@example.com
EOF
git add README.md
git commit -m "プロフィール README を追加"
git remote add origin https://github.com/tanaka/tanaka.git
git push -u origin main
```

---

## 5.3 リポジトリの作成

### Public と Private の違い

| 項目 | Public（公開） | Private（非公開） |
|---|---|---|
| 閲覧 | 誰でも可能 | 招待されたユーザーのみ |
| フォーク | 誰でも可能 | 権限のあるユーザーのみ |
| 料金 | 無料 | 無料（コラボレーター数に制限あり） |
| 用途 | OSS、ポートフォリオ | 社内プロジェクト、個人開発 |

### コマンドラインからリポジトリを作成して連携する

```bash
# 1. ローカルにプロジェクトを作成
mkdir my-project
cd my-project
git init

# 2. ファイルを作成してコミット
echo "# My Project" > README.md
echo "node_modules/" > .gitignore
git add README.md .gitignore
git commit -m "初回コミット: README と .gitignore を追加"

# 3. GitHub 上でリモートリポジトリを作成済みとして、連携する
git remote add origin https://github.com/ユーザー名/my-project.git

# 4. プッシュ（-u で上流ブランチを設定）
git push -u origin main
```

### gh コマンド（GitHub CLI）を使う方法

GitHub CLI（`gh`）を使うと、コマンドラインから直接リポジトリを作成できます。

```bash
# GitHub CLI でリポジトリを作成（Public）
gh repo create my-project --public --source=. --remote=origin --push

# Private リポジトリの場合
gh repo create my-project --private --source=. --remote=origin --push
```

> **よくある間違い：** `git remote add origin` のURLを間違えるケースが多いです。GitHub のリポジトリページからURLをコピーしましょう。HTTPS と SSH の2種類があるので、自分の認証方式に合ったURLを選択してください。

### ポイントまとめ

- Public は公開プロジェクト、Private は非公開プロジェクトに使います
- GitHub CLI（`gh`）を使うとコマンドラインから効率的に操作できます
- リモートURLは HTTPS と SSH の2種類があります

---

## 5.4 README.md の書き方

README.md はプロジェクトの「顔」です。マークダウン記法（Markdown）で記述します。初めてプロジェクトを見る人が最初に読むファイルなので、丁寧に書きましょう。

### README に含めるべき要素

```markdown
# プロジェクト名

プロジェクトの概要を1〜2文で説明します。

## 機能

- 機能1の説明
- 機能2の説明
- 機能3の説明

## 必要な環境

- Python 3.12 以上
- pip

## インストール方法

git clone https://github.com/ユーザー名/プロジェクト名.git
cd プロジェクト名
pip install -r requirements.txt

## 使い方

python main.py

## テストの実行方法

python -m pytest

## ライセンス

MIT License
```

### 良い README のチェックリスト

1. **何をするプロジェクトか**が一目でわかること
2. **セットアップ手順**が明確であること
3. **使い方の例**が含まれていること
4. **テストの実行方法**が書かれていること
5. **ライセンス**が明記されていること

---

## 5.5 プルリクエスト（Pull Request）の作成と流れ

プルリクエスト（Pull Request、略称 PR）は、自分の変更を他のブランチに統合してもらうためのリクエストです。チーム開発の中核となる機能です。

### プルリクエストの全体の流れ

```
  開発者A                    GitHub                     レビュアーB
    │                         │                            │
    │  1. ブランチ作成         │                            │
    │  git checkout -b        │                            │
    │    feature/login        │                            │
    │                         │                            │
    │  2. コード変更 & コミット │                            │
    │  git add & commit       │                            │
    │                         │                            │
    │  3. プッシュ             │                            │
    │  git push origin ──────>│                            │
    │    feature/login        │                            │
    │                         │                            │
    │  4. PR 作成 ───────────>│  5. PR 通知 ──────────────>│
    │                         │                            │
    │                         │  6. コードレビュー          │
    │                         │<─────── レビューコメント ───│
    │                         │                            │
    │  7. 修正 & 再プッシュ    │                            │
    │  ──────────────────────>│                            │
    │                         │  8. Approve ───────────────│
    │                         │                            │
    │  9. マージ               │                            │
    │  ──────────────────────>│                            │
    │                         │                            │
    │  10. ブランチ削除        │                            │
    └─────────────────────────┴────────────────────────────┘
```

### プルリクエストの作成手順

```bash
# 1. 最新の main を取得
git checkout main
git pull origin main

# 2. 作業ブランチを作成
git checkout -b feature/add-login

# 3. コードを変更してコミット
git add src/login.py
git commit -m "feat: ログイン機能を追加"

# 4. リモートにプッシュ
git push origin feature/add-login
```

プッシュ後、GitHub のリポジトリページに「Compare & pull request」ボタンが表示されます。クリックして以下を記入します。

- **タイトル**: 変更内容を簡潔に記述（例:「ログイン機能を追加」）
- **説明**: 変更の背景、内容、テスト方法を記述
- **レビュアー（Reviewers）**: レビューを依頼したい人を指定
- **ラベル（Labels）**: `bug`、`enhancement` などのラベルを付与
- **担当者（Assignees）**: 担当者を指定

### マージの3つの方法

| 方法 | 説明 | 履歴 |
|---|---|---|
| Create a merge commit | マージコミットを作成 | すべてのコミットが残る |
| Squash and merge | 複数コミットを1つにまとめる | 履歴がきれいになる |
| Rebase and merge | リベースしてマージ | 直線的な履歴になる |

### ポイントまとめ

- プルリクエストはチーム開発で品質を担保する重要な仕組みです
- PRの説明文はレビュアーが理解しやすいように丁寧に書きましょう
- 小さな単位でPRを作成すると、レビューがスムーズになります
- マージ方法は3種類あり、チームのルールに合わせて選びましょう

---

## 5.6 コードレビューの方法

GitHub のコードレビューには3つのアクション（action）があります。

| アクション | 意味 | 使いどころ |
|---|---|---|
| **Approve** | 承認 | 問題なくマージしてよい場合 |
| **Request Changes** | 変更要求 | 修正が必要な場合 |
| **Comment** | コメントのみ | 意見や質問がある場合（承認でも拒否でもない） |

### レビューの手順

1. PRの「Files changed」タブを開きます
2. 変更箇所を確認し、行番号の「+」をクリックしてコメントを追加します
3. 複数箇所にコメントする場合は「Start a review」で一括送信できます
4. すべて確認したら「Review changes」から上記3つのいずれかを選択して送信します

### 良いコードレビューのコツ

- **問題点だけでなく良い点も褒める**（ポジティブなフィードバック）
- **理由を説明する**（「こうした方がいい」ではなく「こうするとXXの理由で改善します」）
- **質問形式で提案する**（「XXにしませんか？」）
- **些細なスタイルの違いは自動ツール（linter）に任せる**

> **よくある間違い：** プルリクエストなしで main ブランチに直接 push するのは、現場では重大なルール違反とみなされます。必ずブランチを切ってPRを作成し、レビューを経てからマージしましょう。

---

## 5.7 Issue の活用

イシュー（Issue）は、バグ報告・機能要望・タスク管理に使う機能です。プロジェクトの「やることリスト」として活用します。

### Issue テンプレートの作成

`.github/ISSUE_TEMPLATE/bug_report.md` を作成すると、Issue 作成時にテンプレートが自動適用されます。

```markdown
---
name: バグ報告
about: バグの報告にはこのテンプレートを使ってください
title: "[BUG] "
labels: bug
---

## バグの概要
<!-- バグの内容を簡潔に説明してください -->

## 再現手順
1.
2.
3.

## 期待される動作
<!-- 本来どう動くべきか -->

## 実際の動作
<!-- 実際にどう動いたか -->

## スクリーンショット
<!-- あれば貼り付けてください -->

## 環境
- OS:
- ブラウザ:
- バージョン:
```

### Issue とプルリクエストの連携

コミットメッセージやPR説明文にキーワードを書くと、マージ時に Issue が自動クローズされます。

```bash
# 以下のキーワードが使えます
# Closes, Fixes, Resolves（大文字小文字は問いません）

git commit -m "fix: ログイン時のエラーを修正 Closes #42"
```

### ポイントまとめ

- Issue はプロジェクトのタスク管理に欠かせない機能です
- テンプレートを用意すると報告の品質が統一されます
- `Closes #番号` でPRとIssueを連携させましょう

---

## 5.8 GitHub Actions の基本

GitHub Actions（ギットハブ アクションズ）は、CI/CD（継続的インテグレーション/継続的デリバリー）を実現する自動化ツールです。

### CI/CD とは

```
CI（継続的インテグレーション）          CD（継続的デリバリー）
┌─────────────────────────┐    ┌─────────────────────────┐
│ コード変更                │    │ ステージング環境に        │
│   ↓                     │    │ 自動デプロイ              │
│ 自動ビルド               │    │   ↓                     │
│   ↓                     │    │ 本番環境に                │
│ 自動テスト               │    │ デプロイ（手動 or 自動）   │
│   ↓                     │    │                          │
│ 結果通知                 │    │                          │
└─────────────────────────┘    └─────────────────────────┘
```

### ワークフローファイルの作成

`.github/workflows/` ディレクトリにYAMLファイルを配置します。

```yaml
# .github/workflows/test.yml
name: テスト実行

# main ブランチへのプッシュとPR作成時に実行
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      # リポジトリのコードをチェックアウト
      - uses: actions/checkout@v4

      # Python をセットアップ
      - name: Python セットアップ
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      # 依存パッケージをインストール
      - name: 依存パッケージインストール
        run: pip install -r requirements.txt

      # テストを実行
      - name: テスト実行
        run: python -m pytest
```

### GitHub Actions の構造

```
ワークフロー (Workflow)  ← .yml ファイル1つに対応
  └── ジョブ (Job)       ← 並列実行可能な処理単位
        └── ステップ (Step)  ← ジョブ内の個別の処理
              ├── uses: 再利用可能なアクション
              └── run: シェルコマンド
```

### ポイントまとめ

- GitHub Actions はリポジトリ内の `.github/workflows/` にYAMLで定義します
- `on` でトリガー条件、`jobs` で実行内容を指定します
- 公式やコミュニティのアクションを `uses` で再利用できます

---

## 5.9 GitHub Pages でWebサイト公開

GitHub Pages（ギットハブ ページズ）は、リポジトリのコードから静的Webサイト（static website）を無料で公開できる機能です。

### 設定手順

1. リポジトリの「Settings」→「Pages」を開きます
2. Source で「Deploy from a branch」を選択します
3. ブランチ（例: `main`）とフォルダ（`/` または `/docs`）を選択します
4. 「Save」をクリックします

公開URLは `https://ユーザー名.github.io/リポジトリ名/` になります。

### 簡単なサンプル

```bash
# GitHub Pages 用のリポジトリを作成
mkdir my-portfolio && cd my-portfolio
git init

# index.html を作成
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>My Portfolio</title>
</head>
<body>
  <h1>ようこそ！</h1>
  <p>これは GitHub Pages で公開されたサイトです。</p>
</body>
</html>
EOF

git add index.html
git commit -m "GitHub Pages 用のサイトを作成"
git remote add origin https://github.com/ユーザー名/my-portfolio.git
git push -u origin main
```

---

## 5.10 GitHub のセキュリティ機能

GitHub は、コードの安全性を高めるセキュリティ機能を複数提供しています。

### Dependabot（ディペンダボット）

依存パッケージの脆弱性（vulnerability）を自動で検出し、更新PRを作成してくれます。

```yaml
# .github/dependabot.yml
version: 2
updates:
  # npm パッケージの更新を毎週チェック
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    # PR の最大同時オープン数
    open-pull-requests-limit: 10
```

### Secret scanning（シークレットスキャニング）

APIキーやパスワードなどの機密情報（secret）がコードに含まれていないか自動検出します。検出された場合、該当するサービスプロバイダーに通知が送られ、キーが無効化されることもあります。

### Branch protection（ブランチ保護）の設定

main ブランチへの直接プッシュを禁止し、PRとレビューを必須にできます。

| 設定項目 | 説明 |
|---|---|
| Require a pull request before merging | PR を必須にする |
| Require approvals | 承認を必須にする（人数指定可能） |
| Require status checks to pass | CI のパスを必須にする |
| Require branches to be up to date | マージ前に最新であることを要求 |
| Include administrators | 管理者にもルールを適用する |

> **よくある間違い：** `.env` ファイルやAPIキーを含むファイルをコミットしてしまうケースが多発しています。`.gitignore` に必ず `.env` を追加しましょう。万が一コミットしてしまった場合は、履歴から削除するだけでなく、キーを即座に無効化して再発行してください。

### ポイントまとめ

- Dependabot で依存パッケージの脆弱性を自動検出しましょう
- Secret scanning で機密情報の漏洩を防ぎましょう
- Branch protection で main ブランチを保護し、レビュー必須にしましょう
- `.gitignore` を正しく設定し、機密情報をコミットしないようにしましょう

---

## 第5章の総まとめ

| 項目 | 要点 |
|---|---|
| GitHub | 世界最大のコードホスティングサービス |
| リポジトリ | Public（公開）と Private（非公開）を使い分ける |
| プルリクエスト | チーム開発の品質管理の中核。小さい単位で作成する |
| コードレビュー | Approve / Request Changes / Comment の3種類 |
| Issue | バグ報告・機能要望・タスク管理に活用 |
| GitHub Actions | CI/CD を YAML で定義して自動化 |
| GitHub Pages | 静的Webサイトを無料で公開 |
| セキュリティ | Dependabot、Secret scanning、Branch protection |

次の章では、もう1つの主要なGitプラットフォームであるGitLabについて学びます。

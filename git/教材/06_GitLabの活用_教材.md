# 第6章：GitLabの活用

## この章のゴール

- GitLab（ギットラブ）の特徴とGitHubとの違いを理解する
- GitLab のプロジェクト作成とマージリクエストの流れを習得する
- GitLab CI/CD の基本的な設定方法を実践できるようになる

---

## 6.1 GitLab とは

GitLab（ギットラブ）は、DevOps（デブオプス）プラットフォームとして設計されたGitリポジトリ管理サービスです。ソースコード管理だけでなく、CI/CD、プロジェクト管理、セキュリティテスト、モニタリングまで、開発ライフサイクル全体を1つのプラットフォームでカバーすることを目指しています。

```
┌─────────────────────────────────────────────────────────┐
│                    GitLab DevOps Platform                │
│                                                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ Plan    │→│ Create  │→│ Verify  │→│ Package │   │
│  │(計画)   │  │(開発)   │  │(検証)   │  │(配布)   │   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
│       ↑                                       │          │
│       │   ┌─────────┐  ┌─────────┐           ↓          │
│       │   │ Monitor │←│ Release │←──────────┘          │
│       │   │(監視)   │  │(リリース)│                      │
│       │   └─────────┘  └─────────┘                      │
│       └──────────┘                                       │
└─────────────────────────────────────────────────────────┘
```

### GitLab のエディション

| エディション | 特徴 | 対象 |
|---|---|---|
| Free | 基本機能が無料で使える | 個人・小規模チーム |
| Premium | 高度なプロジェクト管理機能 | 中規模チーム |
| Ultimate | セキュリティ・コンプライアンス機能 | 大規模企業 |

---

## 6.2 GitHub との違い

GitLab と GitHub は、どちらもGitリポジトリをホスティングするサービスですが、設計思想や機能に違いがあります。

### 機能比較表

| 機能 | GitHub | GitLab |
|---|---|---|
| コードホスティング | ○ | ○ |
| プルリクエスト/マージリクエスト | Pull Request | Merge Request |
| CI/CD | GitHub Actions | GitLab CI/CD（組み込み） |
| セルフホスト | GitHub Enterprise（有料） | Community Edition（無料） |
| コンテナレジストリ | GitHub Packages | GitLab Container Registry |
| イシューボード | GitHub Projects | Issue Board（組み込み） |
| Wiki | ○ | ○ |
| ページ機能 | GitHub Pages | GitLab Pages |
| セキュリティスキャン | Dependabot 等 | SAST/DAST（組み込み） |
| 設計思想 | コラボレーション重視 | DevOps全体をカバー |

### 主な違いのポイント

```
GitHub の特徴:
  ・世界最大のOSSコミュニティ
  ・サードパーティとの連携が豊富
  ・GitHub Actions のマーケットプレイスが充実

GitLab の特徴:
  ・DevOps機能がオールインワン
  ・セルフホストが無料（Community Edition）
  ・CI/CD が最初から組み込まれている
```

---

## 6.3 セルフホスト版 vs SaaS版

GitLab にはセルフホスト版（self-managed）と SaaS版（gitlab.com）の2つの利用形態があります。

| 項目 | セルフホスト版 | SaaS版（gitlab.com） |
|---|---|---|
| インフラ管理 | 自社で管理 | GitLab 社が管理 |
| データの場所 | 自社サーバー内 | GitLab社のクラウド |
| カスタマイズ | 自由にカスタマイズ可能 | 制限あり |
| 初期コスト | サーバー構築が必要 | アカウント作成のみ |
| アップデート | 自分で適用 | 自動的に最新版 |
| 適したケース | セキュリティ要件が厳しい企業 | 手軽に始めたい場合 |

### セルフホスト版のインストール例（Ubuntu）

```bash
# GitLab Community Edition のインストール（Ubuntu 22.04）
# 必要なパッケージをインストール
sudo apt-get update
sudo apt-get install -y curl openssh-server ca-certificates tzdata perl

# GitLab のパッケージリポジトリを追加
curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash

# GitLab CE をインストール（URLは自社のドメインに置き換え）
sudo EXTERNAL_URL="https://gitlab.example.com" apt-get install gitlab-ce

# 初期パスワードの確認
sudo cat /etc/gitlab/initial_root_password
```

> **よくある間違い：** セルフホスト版はインストールしただけで終わりではありません。定期的なアップデート、バックアップ、セキュリティパッチの適用が必要です。運用体制が整っていない場合は SaaS版の利用を検討しましょう。

### ポイントまとめ

- セルフホスト版はデータを自社内に保持できるメリットがあります
- SaaS版は運用の手間が不要で、すぐに使い始められます
- セキュリティ要件と運用体制に応じて選択しましょう

---

## 6.4 GitLab のプロジェクト作成

GitLab ではリポジトリを「プロジェクト（project）」と呼びます。

### プロジェクトの作成手順

1. GitLab にログインします
2. 「New project」をクリックします
3. 以下のいずれかを選択します：
   - **Create blank project**: 空のプロジェクトを作成
   - **Create from template**: テンプレートから作成
   - **Import project**: 他のサービスからインポート（GitHub からの移行にも対応）
   - **Run CI/CD for external repository**: 外部リポジトリのCI/CDのみ利用

### グループとサブグループ

GitLab では「グループ（group）」を使ってプロジェクトを組織的に管理できます。

```
会社名グループ (company)
├── フロントエンドサブグループ (frontend)
│   ├── web-app プロジェクト
│   └── mobile-app プロジェクト
├── バックエンドサブグループ (backend)
│   ├── api-server プロジェクト
│   └── batch-jobs プロジェクト
└── インフラサブグループ (infrastructure)
    ├── terraform プロジェクト
    └── monitoring プロジェクト
```

### コマンドラインからプロジェクトと連携

```bash
# 既存のローカルリポジトリを GitLab に連携
cd my-project
git remote add origin https://gitlab.com/グループ名/プロジェクト名.git
git push -u origin main

# GitLab からクローン
git clone https://gitlab.com/グループ名/プロジェクト名.git
```

---

## 6.5 マージリクエスト（Merge Request）

マージリクエスト（Merge Request、略称 MR）は、GitHub のプルリクエスト（PR）に相当する機能です。機能名は異なりますが、基本的な流れは同じです。

### GitHub PR との用語対応表

| GitHub | GitLab | 説明 |
|---|---|---|
| Pull Request | Merge Request | コードの統合リクエスト |
| Reviewer | Reviewer | レビュアー |
| Checks | Pipeline | 自動テストの結果 |
| Draft PR | Draft MR | 作業中のリクエスト |
| Auto-merge | Auto-merge | 条件を満たしたら自動マージ |

### マージリクエストの作成手順

```bash
# 1. 作業ブランチを作成
git checkout -b feature/user-registration

# 2. コードを変更してコミット
git add src/registration.py
git commit -m "feat: ユーザー登録機能を追加"

# 3. リモートにプッシュ
git push origin feature/user-registration
```

プッシュすると、ターミナルにMR作成用のURLが表示されます。

```
remote: To create a merge request for feature/user-registration, visit:
remote:   https://gitlab.com/group/project/-/merge_requests/new?merge_request...
```

### マージリクエストの承認ルール

GitLab では、マージに必要な承認者数やグループを詳細に設定できます。

```
承認ルールの例：
  ・最低2名の承認が必要
  ・セキュリティチームから1名以上の承認が必要
  ・コード所有者（CODEOWNERS）の承認が必要
```

### ポイントまとめ

- GitLab の Merge Request は GitHub の Pull Request と同等の機能です
- プッシュ時にMR作成用のURLが表示されるので活用しましょう
- 承認ルールを設定して品質を担保しましょう

---

## 6.6 GitLab CI/CD

GitLab CI/CD は、GitLab に組み込まれた継続的インテグレーション/継続的デリバリーの仕組みです。リポジトリのルートに `.gitlab-ci.yml` ファイルを配置するだけで有効になります。

### 基本的な .gitlab-ci.yml

```yaml
# .gitlab-ci.yml

# パイプラインのステージを定義
stages:
  - build
  - test
  - deploy

# ビルドジョブ
build_job:
  stage: build
  image: python:3.12
  script:
    - pip install -r requirements.txt
    - python setup.py build
  artifacts:
    paths:
      - build/

# テストジョブ
test_job:
  stage: test
  image: python:3.12
  script:
    - pip install -r requirements.txt
    - python -m pytest --junitxml=report.xml
  artifacts:
    reports:
      junit: report.xml

# デプロイジョブ（main ブランチのみ）
deploy_job:
  stage: deploy
  script:
    - echo "デプロイを実行します"
    - ./deploy.sh
  only:
    - main
  environment:
    name: production
    url: https://example.com
```

### GitHub Actions との比較

| 項目 | GitLab CI/CD | GitHub Actions |
|---|---|---|
| 設定ファイル | `.gitlab-ci.yml`（1ファイル） | `.github/workflows/*.yml`（複数可） |
| 実行環境 | GitLab Runner | GitHub-hosted Runner |
| Docker対応 | `image:` で指定 | `container:` で指定 |
| キャッシュ | `cache:` キーワード | `actions/cache` アクション |
| 成果物 | `artifacts:` キーワード | `actions/upload-artifact` |

### ポイントまとめ

- `.gitlab-ci.yml` をリポジトリのルートに置くだけでCI/CDが有効になります
- `stages` でパイプラインの流れを、`script` で実行内容を定義します
- `only` や `rules` でジョブの実行条件を制御できます

---

## 6.7 GitLab Runner の概念

GitLab Runner（ギットラブ ランナー）は、CI/CDパイプラインのジョブを実際に実行するエージェント（agent）です。

```
┌──────────────┐        ┌──────────────┐
│   GitLab     │        │ GitLab Runner │
│   Server     │───────>│  (実行環境)    │
│              │  ジョブ  │              │
│  パイプライン │<───────│  ジョブ結果    │
│  管理        │        │  を返却       │
└──────────────┘        └──────────────┘
```

### Runner の種類

| 種類 | 説明 | 用途 |
|---|---|---|
| Shared Runner | GitLab.com が提供する共有ランナー | 手軽に使いたい場合 |
| Group Runner | グループ内で共有するランナー | チーム用 |
| Project Runner | 特定プロジェクト専用のランナー | 特殊な要件がある場合 |

### Runner の Executor（実行方式）

| Executor | 説明 |
|---|---|
| Docker | Docker コンテナ内でジョブを実行（最も一般的） |
| Shell | Runner がインストールされたマシンのシェルで実行 |
| Kubernetes | Kubernetes クラスタ上でジョブを実行 |
| Docker Machine | オンデマンドでDockerホストを起動 |

### セルフホスト Runner のインストール例

```bash
# Linux に GitLab Runner をインストール
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
sudo apt-get install gitlab-runner

# Runner を登録
sudo gitlab-runner register \
  --url "https://gitlab.com/" \
  --registration-token "プロジェクトのトークン" \
  --description "my-runner" \
  --executor "docker" \
  --docker-image "python:3.12"
```

---

## 6.8 パイプラインの構成

パイプライン（pipeline）は、CI/CDの一連の処理の流れです。ステージ（stages）とジョブ（jobs）で構成されます。

### パイプラインの構造

```
パイプライン (Pipeline)
│
├── Stage: build ─────────────────────────────
│   └── [build_job] ──→ 成功 ──→ 次のステージへ
│
├── Stage: test ──────────────────────────────
│   ├── [unit_test]  ──→ 成功 ┐
│   └── [lint_check] ──→ 成功 ┴→ 次のステージへ
│      （同じステージ内のジョブは並列実行）
│
└── Stage: deploy ────────────────────────────
    └── [deploy_job] ──→ 成功 ──→ パイプライン完了
```

### 実用的なパイプラインの例

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

# キャッシュ設定（全ジョブ共通）
default:
  cache:
    paths:
      - .cache/pip/

# コードの静的解析
lint:
  stage: lint
  image: python:3.12
  script:
    - pip install flake8
    - flake8 src/

# ユニットテスト
unit_test:
  stage: test
  image: python:3.12
  script:
    - pip install -r requirements.txt
    - python -m pytest tests/unit/

# 結合テスト
integration_test:
  stage: test
  image: python:3.12
  services:
    - postgres:16
  variables:
    POSTGRES_DB: testdb
    POSTGRES_USER: testuser
    POSTGRES_PASSWORD: testpass
  script:
    - pip install -r requirements.txt
    - python -m pytest tests/integration/

# Docker イメージのビルド
build_image:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

# 本番デプロイ
deploy_production:
  stage: deploy
  script:
    - echo "本番環境にデプロイします"
  environment:
    name: production
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
```

### ポイントまとめ

- パイプラインは stages（段階）と jobs（個別処理）で構成されます
- 同じステージ内のジョブは並列実行されます
- `rules` でジョブの実行条件を細かく制御できます
- `when: manual` で手動承認を必須にできます

---

## 6.9 イシューボード（Issue Board）でのタスク管理

GitLab のイシューボード（Issue Board）は、カンバン方式（Kanban）でタスクを視覚的に管理できる機能です。

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│   Open       │  Doing       │  Review      │   Done       │
│  (未着手)     │  (作業中)     │ (レビュー中)  │  (完了)       │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ ┌──────────┐ │ ┌──────────┐ │ ┌──────────┐ │ ┌──────────┐ │
│ │ #15      │ │ │ #12      │ │ │ #10      │ │ │ #8       │ │
│ │ API設計  │ │ │ 認証機能  │ │ │ DB設計   │ │ │ 環境構築  │ │
│ └──────────┘ │ └──────────┘ │ └──────────┘ │ └──────────┘ │
│ ┌──────────┐ │              │              │ ┌──────────┐ │
│ │ #16      │ │              │              │ │ #9       │ │
│ │ テスト計画│ │              │              │ │ CI設定   │ │
│ └──────────┘ │              │              │ └──────────┘ │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

### イシューボードの活用方法

1. **ラベルを作成**: `Open`、`Doing`、`Review`、`Done` などのラベルを作成します
2. **ボードにリストを追加**: 各ラベルに対応するリストをボードに追加します
3. **Issue をドラッグ&ドロップ**: カードを移動するだけでラベルが自動更新されます

### マイルストーン（Milestone）との連携

マイルストーンを設定すると、リリース単位でIssueを管理できます。

```
マイルストーン: v1.0.0（期限: 2026-04-30）
  ├── Issue #8:  環境構築 [Done]
  ├── Issue #9:  CI設定   [Done]
  ├── Issue #10: DB設計   [Review]
  ├── Issue #12: 認証機能  [Doing]
  └── Issue #15: API設計  [Open]
  
  進捗: 40%（2/5 完了）
```

---

## 6.10 GitLab Container Registry

GitLab Container Registry（コンテナレジストリ）は、Docker イメージを GitLab 上で管理できる機能です。

### コンテナレジストリの利用

```bash
# GitLab Container Registry にログイン
docker login registry.gitlab.com

# Docker イメージをビルド
docker build -t registry.gitlab.com/グループ名/プロジェクト名:latest .

# イメージをプッシュ
docker push registry.gitlab.com/グループ名/プロジェクト名:latest

# イメージをプル
docker pull registry.gitlab.com/グループ名/プロジェクト名:latest
```

### CI/CD でのコンテナレジストリ活用

```yaml
# .gitlab-ci.yml
build_and_push:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker build -t $CI_REGISTRY_IMAGE:latest .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker push $CI_REGISTRY_IMAGE:latest
```

---

## 6.11 GitHub vs GitLab 選択ガイド

どちらを選ぶべきかは、チームの状況や要件によって異なります。

### GitHub を選ぶべきケース

- **オープンソースプロジェクト**を運営する場合
- **大きなコミュニティ**とつながりたい場合
- **GitHub Actions のマーケットプレイス**を活用したい場合
- **既にGitHubに慣れている**チームの場合

### GitLab を選ぶべきケース

- **セルフホスト**でデータを社内に置きたい場合
- **DevOps機能をオールインワン**で使いたい場合
- **組み込みのCI/CD**を重視する場合
- **セキュリティスキャン**を統合的に管理したい場合

### 両方使う場合

大きな組織では、OSSプロジェクトはGitHub、社内プロジェクトはGitLabという使い分けも一般的です。GitLab には GitHub からのインポート機能もあるため、移行も比較的容易です。

### ポイントまとめ

- GitHub はコミュニティとエコシステムが強み
- GitLab はオールインワンの DevOps プラットフォームが強み
- プロジェクトの要件とチームの状況に応じて選択しましょう
- 両方を使い分けることも有効な選択肢です

---

## 第6章の総まとめ

| 項目 | 要点 |
|---|---|
| GitLab | DevOps全体をカバーするオールインワンプラットフォーム |
| セルフホスト | Community Edition は無料、データを自社管理できる |
| マージリクエスト | GitHub の Pull Request と同等の機能 |
| GitLab CI/CD | `.gitlab-ci.yml` で設定、GitLab に組み込み済み |
| GitLab Runner | CI/CD ジョブを実行するエージェント |
| パイプライン | stages と jobs で構成、同ステージは並列実行 |
| Issue Board | カンバン方式でタスクを視覚的に管理 |
| Container Registry | Docker イメージを GitLab 上で管理 |

次の章では、チーム開発で使われるワークフロー（Git Flow、GitHub Flow など）について学びます。

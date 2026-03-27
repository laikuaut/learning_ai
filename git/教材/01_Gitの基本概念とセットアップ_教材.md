# 第1章：Gitの基本概念とセットアップ

## この章のゴール

- バージョン管理（version control）の必要性を理解する
- Git の特徴と他のバージョン管理システムとの違いを説明できる
- Git をインストールし、初期設定を完了する
- `git init` でリポジトリを作成できる
- `.gitignore` の基本的な書き方を理解する

---

## 1. バージョン管理とは何か

### なぜバージョン管理が必要なのか

プログラミングや文書作成をしていると、以下のような経験はありませんか？

```
プロジェクト/
├── report_最終版.docx
├── report_最終版_修正.docx
├── report_最終版_修正2.docx
├── report_本当の最終版.docx
└── report_提出用_これが本当の最終版.docx
```

このようなファイル管理には多くの問題があります。

- どれが最新版かわからなくなる
- いつ、誰が、何を変更したか追跡できない
- 以前の状態に戻したいときに戻せない
- 複数人で同時に編集すると上書き事故が起きる

バージョン管理システム（VCS: Version Control System）は、これらの問題を解決するためのツールです。ファイルの変更履歴を自動的に記録し、いつでも過去の状態に戻すことができます。

### ポイントまとめ

- バージョン管理はファイルの変更履歴を管理する仕組みです
- 「いつ・誰が・何を・なぜ変更したか」を記録します
- 過去の任意の時点に戻すことができます

---

## 2. Gitの特徴と歴史

### Gitの誕生

Git は、Linux カーネルの開発者である **リーナス・トーバルズ（Linus Torvalds）** が2005年に開発しました。Linux カーネルの開発で使っていたバージョン管理ツール BitKeeper が無料で使えなくなったことがきっかけです。

Git の設計目標は以下の通りです。

- **高速であること** — 大規模プロジェクトでもストレスなく動作する
- **分散型であること** — ネットワークなしでも作業できる
- **データの完全性** — SHA-1 ハッシュで変更履歴が壊れないことを保証する
- **ブランチ操作が軽量** — 気軽にブランチを作成・切り替えできる

### 集中型 vs 分散型

バージョン管理システムには大きく分けて2つの方式があります。

```
【集中型（Centralized）- SVN など】

    ┌─────────────────┐
    │  中央サーバー     │
    │  (リポジトリ)     │
    └───────┬─────────┘
        ┌───┼───┐
        │   │   │
        ▼   ▼   ▼
       PC1 PC2 PC3
      (作業) (作業) (作業)
       コピー コピー コピー

  ※ サーバーに接続できないと履歴の確認・コミットができない


【分散型（Distributed）- Git】

    ┌─────────────────┐
    │  リモートリポジトリ │
    │  (GitHub等)       │
    └───────┬─────────┘
        ┌───┼───┐
        │   │   │
        ▼   ▼   ▼
       PC1 PC2 PC3
      (完全な  (完全な  (完全な
     リポジトリ リポジトリ リポジトリ
       コピー)  コピー)  コピー)

  ※ 各PCに完全な履歴があるので、オフラインでも作業可能
```

| 比較項目 | 集中型（SVN等） | 分散型（Git） |
|---|---|---|
| リポジトリ | サーバーに1つ | 各PCに完全なコピー |
| オフライン作業 | 不可 | 可能 |
| 速度 | ネットワーク依存 | ローカルで高速 |
| バックアップ | サーバー障害がリスク | 各PCがバックアップ |
| ブランチ | 重い操作 | 軽量・高速 |

### Git の仕組み：スナップショット

多くのバージョン管理システムがファイルの「差分（delta）」を保存するのに対し、Git はファイル全体の「スナップショット（snapshot）」を保存します。

```
【差分管理（他のVCS）】
  v1 → v2: ファイルAの3行目を変更
  v2 → v3: ファイルBを追加

【スナップショット管理（Git）】
  v1: [ファイルA-v1] [ファイルB-v1]
  v2: [ファイルA-v2] [ファイルB-v1]  ← 変更なしのファイルはリンクで参照
  v3: [ファイルA-v2] [ファイルB-v2] [ファイルC-v1]
```

この方式により、特定の時点の状態を高速に復元できます。

### ポイントまとめ

- Git はリーナス・トーバルズが2005年に開発した分散型バージョン管理システムです
- 分散型なので各開発者がリポジトリの完全なコピーを持ちます
- オフラインでもコミットや履歴確認が可能です
- Git はスナップショット方式でファイルの状態を管理します

---

## 3. Gitの3つのエリア

Git を理解するうえで最も重要な概念が **3つのエリア** です。

```
  ┌──────────────┐     git add     ┌──────────────┐   git commit   ┌──────────────┐
  │              │ ──────────────> │              │ ─────────────> │              │
  │ ワーキング    │                 │ ステージング   │                │ リポジトリ    │
  │ ツリー       │                 │ エリア        │                │ (.git)       │
  │ (Working     │                 │ (Staging     │                │ (Repository) │
  │  Tree)       │                 │  Area/Index) │                │              │
  │              │ <────────────── │              │ <───────────── │              │
  └──────────────┘  ファイルを編集   └──────────────┘ git restore    └──────────────┘

  あなたが実際に          次のコミットに含める         変更履歴が
  編集するファイル群       変更を選ぶ場所             永久に保存される場所
```

| エリア | 説明 | 例え |
|---|---|---|
| ワーキングツリー（Working Tree） | 実際にファイルを編集する作業場所 | 作業机の上 |
| ステージングエリア（Staging Area） | 次のコミットに含める変更を選択する場所 | 発送する荷物の梱包エリア |
| リポジトリ（Repository） | 変更履歴が保存される場所（.git ディレクトリ） | 倉庫 |

この3段階の仕組みにより、変更したファイルの中から **コミットに含めたいものだけを選んで** 記録できます。これが Git の大きな特徴です。

### ポイントまとめ

- Git には「ワーキングツリー」「ステージングエリア」「リポジトリ」の3つのエリアがあります
- `git add` でワーキングツリーからステージングエリアへ変更を移します
- `git commit` でステージングエリアの変更をリポジトリに記録します

---

## 4. Gitのインストール

### Windows

Git 公式サイト（https://git-scm.com/）からインストーラーをダウンロードしてインストールします。

```bash
# インストール確認
git --version
# 出力例: git version 2.44.0.windows.1
```

winget を使う方法もあります。

```bash
winget install --id Git.Git -e --source winget
```

### macOS

Xcode Command Line Tools に含まれている Git を使うか、Homebrew でインストールします。

```bash
# Xcode Command Line Tools のインストール（Git が含まれる）
xcode-select --install

# または Homebrew でインストール（推奨）
brew install git

# インストール確認
git --version
# 出力例: git version 2.44.0
```

### Linux（Ubuntu / Debian）

```bash
sudo apt update
sudo apt install git

# インストール確認
git --version
# 出力例: git version 2.43.0
```

### Linux（Fedora / RHEL）

```bash
sudo dnf install git

# インストール確認
git --version
```

### ポイントまとめ

- 各OS用のインストール方法があります
- インストール後は `git --version` で確認しましょう

---

## 5. Gitの初期設定

Git を使い始める前に、ユーザー名とメールアドレスを設定する必要があります。この情報はすべてのコミットに記録されます。

### ユーザー名とメールアドレスの設定

```bash
# ユーザー名を設定
git config --global user.name "Taro Yamada"

# メールアドレスを設定
git config --global user.email "taro@example.com"
```

### その他の推奨設定

```bash
# デフォルトブランチ名を main に設定（推奨）
git config --global init.defaultBranch main

# エディタを設定（VS Code の例）
git config --global core.editor "code --wait"

# 改行コードの自動変換設定
# Windows の場合
git config --global core.autocrlf true
# macOS / Linux の場合
git config --global core.autocrlf input

# 日本語ファイル名の文字化け防止
git config --global core.quotepath false

# 出力に色をつける
git config --global color.ui auto
```

### 設定の確認

```bash
# すべての設定を一覧表示
git config --list

# 特定の設定値を確認
git config user.name
git config user.email
```

### 設定の3つのレベル

Git の設定には3つのレベルがあり、より具体的な設定が優先されます。

```
優先度:  高 ◀────────────────────────────────▶ 低

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   local      │  │   global     │  │   system     │
│ リポジトリ    │  │ ユーザー全体  │  │ システム全体  │
│ ごとの設定    │  │ の設定       │  │ の設定       │
│              │  │              │  │              │
│ .git/config  │  │ ~/.gitconfig │  │ /etc/        │
│              │  │              │  │ gitconfig    │
└──────────────┘  └──────────────┘  └──────────────┘
```

```bash
# リポジトリ単位で別のメールアドレスを使う例
git config user.email "taro@company.com"
```

> **よくある間違い：** 初期設定をせずに `git commit` を実行するとエラーになります。Git を使い始める前に必ず `user.name` と `user.email` を設定してください。また、`--global` を付け忘れると、そのリポジトリだけに設定が適用されます。

### ポイントまとめ

- `git config --global user.name` と `user.email` は最初に必ず設定します
- `--global` はPC全体の設定、`--local`（または省略）はリポジトリ単位の設定です
- `init.defaultBranch main` を設定しておくと、デフォルトブランチが `main` になります

---

## 6. git init でリポジトリを作成する

新しいプロジェクトで Git を使い始めるには `git init` コマンドを実行します。

### リポジトリの作成

```bash
# プロジェクト用のディレクトリを作成
mkdir my-project
cd my-project

# Git リポジトリとして初期化
git init
# 出力: Initialized empty Git repository in /home/user/my-project/.git/
```

`git init` を実行すると、ディレクトリ内に `.git` という隠しフォルダが作成されます。このフォルダに Git の管理情報がすべて保存されます。

```
my-project/
└── .git/           ← Git が自動作成する管理用ディレクトリ
    ├── HEAD        ← 現在のブランチを指すポインタ
    ├── config      ← このリポジトリの設定
    ├── hooks/      ← フックスクリプト
    ├── objects/    ← コミットやファイルのデータ
    └── refs/       ← ブランチやタグのポインタ
```

> **よくある間違い：** `.git` フォルダを手動で削除すると、すべての変更履歴が失われます。絶対に削除しないでください。

### 最初のコミットまでの流れ

```bash
# 1. プロジェクトディレクトリを作成して移動
mkdir my-project && cd my-project

# 2. Git リポジトリとして初期化
git init

# 3. ファイルを作成
echo "# My Project" > README.md

# 4. ステージングエリアに追加
git add README.md

# 5. コミット（変更を記録）
git commit -m "最初のコミット: READMEを追加"

# 6. 履歴を確認
git log
# 出力例:
# commit a1b2c3d... (HEAD -> main)
# Author: Taro Yamada <taro@example.com>
# Date:   Thu Mar 27 10:05:00 2026 +0900
#
#     最初のコミット: READMEを追加
```

### ポイントまとめ

- `git init` でディレクトリを Git リポジトリとして初期化します
- `.git` フォルダが Git の管理情報をすべて含んでいます
- `.git` フォルダは決して手動で削除しないでください

---

## 7. .gitignore の基本

`.gitignore` ファイルは、Git に **追跡させたくないファイル** を指定するための設定ファイルです。

### なぜ .gitignore が必要か

以下のようなファイルは Git で管理すべきではありません。

| 種類 | 例 | 理由 |
|---|---|---|
| パスワード・機密情報 | `.env`, `credentials.json` | セキュリティリスク |
| ビルド成果物 | `dist/`, `build/`, `*.o` | 再生成可能 |
| 依存パッケージ | `node_modules/`, `venv/` | 再インストール可能・サイズが巨大 |
| OS生成ファイル | `.DS_Store`, `Thumbs.db` | 不要 |
| エディタ設定 | `.vscode/`, `.idea/` | 個人の環境依存 |

### .gitignore の書き方

プロジェクトのルートに `.gitignore` ファイルを作成します。

```bash
# .gitignore の例

# コメントは # で始めます

# 特定のファイルを無視
.env
credentials.json

# 特定の拡張子を無視（ワイルドカード）
*.log
*.tmp
*.bak

# ディレクトリを無視（末尾に / をつける）
node_modules/
dist/
build/
__pycache__/

# OS生成ファイル
.DS_Store
Thumbs.db

# ただし特定のファイルは追跡する（否定パターン）
!important.log
```

### 基本的なパターン記法

| パターン | 意味 | 例 |
|----------|------|-----|
| `file.txt` | 特定のファイル名 | `file.txt` にマッチ |
| `*.log` | ワイルドカード | すべての `.log` ファイル |
| `dir/` | ディレクトリ全体 | `dir/` 以下すべて |
| `**/logs` | 任意の階層の `logs` | どの階層の `logs` にもマッチ |
| `!important.log` | 除外の例外（否定） | `*.log` から `important.log` を除く |
| `#` | コメント | 無視される |

### .gitignore を作成する実践例

```bash
# プロジェクトで .gitignore を作成
cat << 'EOF' > .gitignore
# 依存パッケージ
node_modules/

# 環境変数ファイル
.env
.env.local

# ビルド成果物
dist/
build/

# ログファイル
*.log

# OS生成ファイル
.DS_Store
Thumbs.db
EOF

# .gitignore をステージングしてコミット
git add .gitignore
git commit -m ".gitignore を追加"
```

> **よくある間違い：** `.gitignore` に追加しても、すでに Git に追跡されているファイルは無視されません。先に `git rm --cached ファイル名` で追跡を外す必要があります。

```bash
# すでに追跡中のファイルを追跡対象から外す（ファイル自体は削除しない）
git rm --cached .env
git commit -m ".env をバージョン管理から除外"
```

### ポイントまとめ

- `.gitignore` で Git に追跡させたくないファイルを指定します
- パスワード、ビルド成果物、依存パッケージなどを除外しましょう
- すでに追跡中のファイルは `git rm --cached` で先に除外する必要があります
- GitHub が公開している言語別の `.gitignore` テンプレート（github/gitignore）を活用すると便利です

---

## 章のポイントまとめ

| 項目 | 内容 |
|---|---|
| バージョン管理 | ファイルの変更履歴を記録・管理する仕組み |
| Git | 分散型バージョン管理システム（各PCに完全な履歴を保持） |
| 3つのエリア | ワーキングツリー → ステージングエリア → リポジトリ |
| 初期設定 | `git config --global user.name` / `user.email` |
| リポジトリ作成 | `git init` で `.git` フォルダが作られる |
| .gitignore | 追跡不要なファイルを指定する設定ファイル |

次の章では、`git add` や `git commit` などの基本操作を詳しく学びます。

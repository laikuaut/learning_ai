# 第7章：プロジェクト管理とCLAUDE.md - 演習問題

---

## 基本問題

### 問題1：設定ファイルの階層

Claude Codeの設定ファイルとその役割を正しく組み合わせてください。

| ファイル | 役割 |
|---|---|
| 1. CLAUDE.md | A. 個人的な設定（Git管理対象外） |
| 2. .claude/settings.json | B. 全プロジェクト共通のグローバル設定 |
| 3. .claude/settings.local.json | C. プロジェクト固有の指示書 |
| 4. ~/.claude/settings.json | D. プロジェクトの技術的設定（Git管理対象） |

**期待される解答：**
```
1-?, 2-?, 3-?, 4-?
```

<details>
<summary>ヒント</summary>

- CLAUDE.mdはMarkdownで書かれた「指示書」です
- settings.jsonはJSON形式の「設定ファイル」です
- `~`はホームディレクトリを表します

</details>

<details>
<summary>解答例</summary>

```
1-C, 2-D, 3-A, 4-B
```

- **CLAUDE.md**: プロジェクトルートに配置する指示書。プロジェクトの概要、規約、コマンド等を記載
- **.claude/settings.json**: プロジェクト内の技術的設定。権限やMCPサーバー設定。チームで共有（Git管理対象）
- **.claude/settings.local.json**: 個人的な設定。ローカル環境固有の情報。Git管理対象外
- **~/.claude/settings.json**: ユーザーのホームディレクトリにあるグローバル設定。全プロジェクトに適用

</details>

---

### 問題2：CLAUDE.mdの必須項目

以下のうち、CLAUDE.mdに書くべき情報として**適切なもの**をすべて選んでください。

A. プロジェクトの概要説明
B. Pythonの基本的な文法解説
C. テストの実行コマンド
D. JavaScriptの変数の宣言方法
E. ディレクトリ構成の説明
F. コーディング規約
G. AIの一般的な仕組みの解説
H. デプロイ手順の注意事項

**期待される解答：**
```
適切なもの: ___
```

<details>
<summary>ヒント</summary>

CLAUDE.mdにはプロジェクト**固有**の情報を書きます。一般的なプログラミング知識はClaude Codeがすでに持っています。

</details>

<details>
<summary>解答例</summary>

```
適切なもの: A, C, E, F, H
```

- A（○）: プロジェクトの概要はClaude Codeがプロジェクトを理解するために重要
- B（×）: 一般的なPython文法はClaude Codeが既に知っている知識
- C（○）: テスト実行コマンドはプロジェクト固有の情報
- D（×）: JavaScriptの基本文法は一般知識
- E（○）: ディレクトリ構成はプロジェクト固有の情報
- F（○）: コーディング規約はプロジェクトごとに異なる
- G（×）: AIの一般的な仕組みはプロジェクトに関係ない
- H（○）: デプロイ手順はプロジェクト固有の重要情報

</details>

---

### 問題3：設定の優先順位

以下の3つの設定が同時に存在する場合、Claude Codeが実際に従う設定はどれですか？

**状況：** モデル設定が3箇所で異なる値に設定されている

```
# CLAUDE.md
OpusモデルでコードレビューしてくださいI

# .claude/settings.json
{ "model": "claude-sonnet-4-6" }

# プロンプト（直接の指示）
> Haikuモデルでこのコードを確認して
```

**期待される解答：**
```
どの設定が優先される？: ___
理由: ___
```

<details>
<summary>ヒント</summary>

設定の優先順位は：直接の指示 > プロジェクト設定 > グローバル設定 です。

</details>

<details>
<summary>解答例</summary>

```
どの設定が優先される？: プロンプト（直接の指示）でのHaikuモデル指定
理由: 設定の優先順位は「直接の指示 > プロジェクト設定 > グローバル設定」の
      順番です。ユーザーがプロンプトで直接指示した内容が最も優先されます。
      CLAUDE.mdや設定ファイルの内容よりも、その場の指示が優先されます。
```

優先順位（高い順）：
1. プロンプト（直接の指示） ← 最優先
2. CLAUDE.md（プロジェクト指示書）
3. .claude/settings.json（プロジェクト設定）
4. ~/.claude/settings.json（グローバル設定）

</details>

---

## 応用問題

### 問題4：CLAUDE.mdの作成

以下のプロジェクト情報を基に、CLAUDE.mdを作成してください。

**プロジェクト情報：**
- プロジェクト名：TaskManager API
- 概要：タスク管理アプリのバックエンドAPI
- 技術スタック：Python 3.12, FastAPI, SQLAlchemy, PostgreSQL, pytest
- 開発サーバー起動：`uvicorn src.main:app --reload`
- テスト実行：`pytest tests/`
- リンター：`ruff check src/`
- フォーマッター：`ruff format src/`
- ディレクトリ構成：src/（routers, services, models, schemas, core）
- 規約：関数名はスネークケース、クラス名はパスカルケース
- 注意事項：src/core/config.py は環境変数を管理しているので直接値を書かないこと

<details>
<summary>ヒント</summary>

CLAUDE.mdの基本構成：概要 → 技術スタック → ディレクトリ構成 → 開発コマンド → コーディング規約 → 注意事項

</details>

<details>
<summary>解答例</summary>

```markdown
# TaskManager API

## 概要
タスク管理アプリケーションのバックエンドAPI。
RESTful APIを提供し、フロントエンドと連携します。

## 技術スタック
- 言語: Python 3.12
- フレームワーク: FastAPI
- ORM: SQLAlchemy
- データベース: PostgreSQL
- テスト: pytest

## ディレクトリ構成
```
src/
├── routers/    # APIエンドポイント定義
├── services/   # ビジネスロジック
├── models/     # SQLAlchemyモデル
├── schemas/    # Pydanticスキーマ
├── core/       # 設定・共通処理
└── main.py     # エントリポイント
```

## 開発コマンド
- `uvicorn src.main:app --reload` - 開発サーバー起動
- `pytest tests/` - テスト実行
- `ruff check src/` - リンター実行
- `ruff format src/` - フォーマッター実行

## コーディング規約
- 関数名: スネークケース（例: get_user_by_id）
- クラス名: パスカルケース（例: UserService）

## 注意事項
- src/core/config.py は環境変数を管理しています。
  設定値を直接ハードコーディングせず、環境変数経由で取得してください。
```

</details>

---

### 問題5：settings.jsonの設計

以下の要件を満たす `.claude/settings.json` を作成してください。

**要件：**
- ファイルの読み込みと検索を自動許可
- `pytest`と`ruff`の実行を自動許可
- GitHub MCPサーバーを設定
- `rm -rf` コマンドを明示的に拒否

<details>
<summary>ヒント</summary>

- permissions.allow にツール名とBashコマンドを配列で指定
- permissions.deny に拒否するコマンドを配列で指定
- mcpServers にサーバー設定をオブジェクトで指定

</details>

<details>
<summary>解答例</summary>

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(pytest tests/)",
      "Bash(ruff check src/)",
      "Bash(ruff format src/)"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  },
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

- `Read`, `Glob`, `Grep` はファイルの読み込み・検索系ツール
- `Bash(コマンド)` 形式で特定のコマンドのみを許可
- `deny` で危険なコマンドを明示的に拒否
- MCPサーバーは `command` と `args` で起動方法を指定
- 環境変数は `${変数名}` 形式で参照可能

</details>

---

## チャレンジ問題

### 問題6：チーム開発向けCLAUDE.md設計

5人のチームで開発するReact + Node.jsプロジェクトのCLAUDE.mdを設計してください。以下の要件を満たす必要があります。

**要件：**
- ブランチ戦略（Git Flow）の説明
- コミットメッセージのConventional Commits形式
- PRのルール（レビュワー最低1人承認）
- フロントエンド（React）とバックエンド（Node.js）のディレクトリが分かれている
- CI/CDではGitHub Actionsを使用
- `src/generated/` ディレクトリは自動生成なので編集禁止

<details>
<summary>ヒント</summary>

チーム開発のCLAUDE.mdでは、個人開発以上に「ルール」と「禁止事項」を明確にすることが重要です。

</details>

<details>
<summary>解答例</summary>

```markdown
# ProjectName

## 概要
React + Node.js によるフルスタックWebアプリケーション。
フロントエンドとバックエンドがモノレポ構成で管理されています。

## 技術スタック
### フロントエンド
- React 18 + TypeScript
- Vite（ビルドツール）
- Tailwind CSS

### バックエンド
- Node.js 20 + Express + TypeScript
- Prisma（ORM）
- PostgreSQL

## ディレクトリ構成
```
├── frontend/          # Reactフロントエンド
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── services/
│   └── package.json
├── backend/           # Node.jsバックエンド
│   ├── src/
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── models/
│   │   └── generated/  ← 編集禁止（Prisma自動生成）
│   └── package.json
└── .github/workflows/ # CI/CD設定
```

## 開発コマンド
- フロントエンド: `cd frontend && npm run dev`
- バックエンド: `cd backend && npm run dev`
- テスト（全体）: `npm test`（ルートで実行）
- リント: `npm run lint`

## ブランチ戦略（Git Flow）
- main: 本番環境（直接pushは禁止）
- develop: 開発環境のメインブランチ
- feature/*: 機能開発（developから分岐）
- fix/*: バグ修正（developから分岐）
- hotfix/*: 緊急修正（mainから分岐）
- release/*: リリース準備

## コミットメッセージ規約
Conventional Commits形式を使用:
- feat: 新機能追加
- fix: バグ修正
- docs: ドキュメント変更
- style: コードスタイル変更（機能に影響なし）
- refactor: リファクタリング
- test: テスト追加・修正
- chore: ビルド設定等の変更

例: `feat(frontend): ユーザープロフィール画面を追加`

## PRルール
- PRはdevelopブランチに対して作成すること
- 最低1人のレビュワーの承認が必要
- CIが通ることを確認してからマージ
- タイトルは「[種別] 概要」形式

## 注意事項
- backend/src/generated/ は Prisma が自動生成するファイルです。
  絶対に手動で編集しないでください。
- 環境変数は .env.example を参照して .env を作成してください。
- .env ファイルはコミットしないでください。
```

</details>

---

### 問題7：トラブルシューティング

以下の問題が発生した場合、どのように対処しますか？

**問題：** チームメンバーのAさんが `.claude/settings.local.json` にAPIキーを直接書いてGitにコミットしてしまいました。

対処手順をステップバイステップで記述してください。

<details>
<summary>ヒント</summary>

1. 機密情報の漏洩への対処
2. Gitの履歴からの削除
3. 再発防止策

</details>

<details>
<summary>解答例</summary>

```
Step 1: APIキーの無効化
まず最優先で、漏洩したAPIキーをプロバイダーの管理画面で
無効化（revoke）します。新しいAPIキーを発行します。

Step 2: Gitの履歴からファイルを削除
gitの履歴にAPIキーが残っているため、以下のコマンドで
履歴からファイルを削除します：

  git filter-branch --force --index-filter \
    'git rm --cached --ignore-unmatch .claude/settings.local.json' \
    --prune-empty -- --all

  または、git-filter-repo ツールを使用：
  git filter-repo --path .claude/settings.local.json --invert-paths

Step 3: .gitignoreに追加
.gitignore に以下を追加して、今後コミットされないようにします：
  .claude/settings.local.json

Step 4: チームへの周知
- settings.local.json は個人設定であり、
  Git管理対象外であることをチームに周知
- CLAUDE.md に注意事項として追記

Step 5: CLAUDE.mdに注意事項を追記
「.claude/settings.local.json はGit管理対象外です。
機密情報（APIキー等）はこのファイルまたは環境変数で管理し、
絶対にコミットしないでください。」
```

</details>

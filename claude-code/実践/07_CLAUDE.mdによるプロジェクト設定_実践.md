# 実践課題07：CLAUDE.mdによるプロジェクト設定 ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第1章〜第6章（基本操作、ファイル操作、Git連携、MCP、フック）、第7章（プロジェクト管理とCLAUDE.md）
> **課題の種類**: 設計課題
> **学習目標**: CLAUDE.mdファイルの設計原則を理解し、プロジェクトの特性に応じた効果的なCLAUDE.mdを設計・作成できるようになる

---

## 完成イメージ

架空のプロジェクトに対して、チーム開発で活用できるCLAUDE.mdを設計します。

```
my-ecommerce-api/
├── CLAUDE.md              ← 今回作成するファイル
├── src/
│   └── CLAUDE.md          ← サブディレクトリのCLAUDE.md
├── .claude/
│   └── settings.json
├── package.json
└── ...
```

CLAUDE.mdの構成例:
```markdown
# ECサイトバックエンドAPI

## 概要
...

## 技術スタック
...

## ディレクトリ構成
...

## コーディング規約
...

## 開発コマンド
...

## 重要なルール
...
```

---

## 課題の要件

1. 以下の3つのプロジェクトシナリオから1つを選び、CLAUDE.mdを設計する
   - シナリオA：ECサイトのバックエンドAPI（Express + PostgreSQL）
   - シナリオB：ブログプラットフォーム（Next.js + Prisma）
   - シナリオC：チャットアプリ（Python FastAPI + WebSocket）
2. CLAUDE.mdに以下のセクションを含める
   - プロジェクト概要
   - 技術スタック
   - ディレクトリ構成
   - コーディング規約（命名規則、インポート順など）
   - 開発コマンド（テスト、ビルド、起動）
   - 重要なルール（変更禁止のファイル、セキュリティ上の注意など）
3. サブディレクトリ用のCLAUDE.md（`src/CLAUDE.md`等）を1つ以上作成する
4. CLAUDE.mdの配置場所（ルート、サブディレクトリ、ホーム）の違いを理解する

---

## ステップガイド

<details>
<summary>ステップ1：プロジェクト構造の作成</summary>

ここではシナリオAを例に進めます。

```bash
# プロジェクト作成
mkdir -p ~/claude-code-practice/task07/my-ecommerce-api
cd ~/claude-code-practice/task07/my-ecommerce-api
git init

# ディレクトリ構造を作成
mkdir -p src/{controllers,services,models,middleware,utils}
mkdir -p tests/{unit,integration}
mkdir -p docs
mkdir -p .claude

# ダミーファイルを配置
touch src/controllers/userController.js
touch src/controllers/productController.js
touch src/services/authService.js
touch src/services/paymentService.js
touch src/models/User.js
touch src/models/Product.js
touch src/middleware/auth.js
touch tests/unit/auth.test.js
touch docs/api-spec.md

cat > package.json << 'EOF'
{
  "name": "my-ecommerce-api",
  "version": "1.0.0",
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "test": "jest",
    "test:unit": "jest tests/unit",
    "test:integration": "jest tests/integration",
    "lint": "eslint src/",
    "build": "tsc"
  }
}
EOF
```

</details>

<details>
<summary>ステップ2：ルートCLAUDE.mdの作成</summary>

以下の内容を含むCLAUDE.mdを作成します。

```markdown
# ECサイトバックエンドAPI

## 概要
ECサイトのバックエンドREST APIです。商品管理、ユーザー認証、
注文処理、決済連携を提供します。

## 技術スタック
- 言語: JavaScript (Node.js 20)
- フレームワーク: Express 4.x
- データベース: PostgreSQL 15 + Prisma ORM
- テスト: Jest + Supertest
- リンター: ESLint + Prettier

## ディレクトリ構成
```
src/
├── controllers/  # APIエンドポイント（ルーティング）
├── services/     # ビジネスロジック
├── models/       # Prismaモデル定義
├── middleware/    # Express ミドルウェア
└── utils/        # 共通ユーティリティ
tests/
├── unit/         # ユニットテスト
└── integration/  # 統合テスト
```

## コーディング規約
- 変数名・関数名: camelCase
- クラス名: PascalCase
- ファイル名: controllers/services は camelCase、models は PascalCase
- インポート順: 1)Node.js標準 → 2)外部パッケージ → 3)プロジェクト内
- エラーハンドリング: try-catchを使用し、カスタムエラークラスでラップ

## 開発コマンド
- `npm run dev` : 開発サーバー起動
- `npm test` : 全テスト実行
- `npm run test:unit` : ユニットテストのみ
- `npm run lint` : リンター実行

## 重要なルール
- `src/middleware/auth.js` は認証の根幹。変更時は必ずセキュリティレビュー
- `.env`ファイルは絶対にコミットしない
- データベースマイグレーションは`npx prisma migrate dev`で行う
- APIのレスポンス形式は`{ success: boolean, data: any, error?: string }`で統一
```

</details>

<details>
<summary>ステップ3：サブディレクトリCLAUDE.mdの作成</summary>

`src/CLAUDE.md` にソースコード固有のルールを記載します。

```markdown
# src/ ディレクトリのルール

## controllerの書き方
- 1ファイル1リソース（userController, productController等）
- バリデーションはcontrollerで行い、ビジネスロジックはserviceに委譲
- レスポンスは必ず `res.json()` で統一フォーマットを使用

## serviceの書き方
- データベースアクセスはserviceからのみ行う
- controllerから直接Prismaクライアントを呼ばない
- エラーは `AppError` クラスでラップして投げる

## テストの慣例
- テストファイル名は `対象モジュール.test.js`
- describe() でモジュール名、it() でテスト内容を記述
```

</details>

<details>
<summary>ステップ4：CLAUDE.mdの配置場所の使い分け</summary>

CLAUDE.mdは複数の場所に配置でき、それぞれ適用範囲が異なります。

```
~/.claude/CLAUDE.md（ユーザーレベル）
  → 自分がどのプロジェクトでも従ってほしいルール
  → 例：「常に日本語でコメントを書いてください」
  → 例：「コミットメッセージはConventional Commitsに従ってください」

プロジェクトルート/CLAUDE.md（プロジェクトレベル）
  → チーム全員で共有するプロジェクトのルール
  → Gitにコミットしてチームで共有

サブディレクトリ/CLAUDE.md（ディレクトリレベル）
  → 特定のディレクトリ固有のルール
  → そのディレクトリ以下で作業するときにのみ適用
```

適用の優先順位:
```
サブディレクトリ > プロジェクトルート > ユーザーレベル
（より具体的な設定が優先されます）
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）── シナリオAの最小構成</summary>

```bash
cd ~/claude-code-practice/task07/my-ecommerce-api

# ルートCLAUDE.md
cat > CLAUDE.md << 'MDEOF'
# ECサイトバックエンドAPI

## 概要
ECサイトのバックエンドREST API。Express + PostgreSQLで構築。

## 開発コマンド
- `npm run dev` : 開発サーバー起動
- `npm test` : テスト実行
- `npm run lint` : リンター実行

## ルール
- コミットメッセージは日本語でOK
- .envファイルはコミットしないこと
MDEOF

# 確認
cat CLAUDE.md
```

</details>

<details>
<summary>解答例（改良版）── 実務レベルの詳細なCLAUDE.md</summary>

```bash
cd ~/claude-code-practice/task07/my-ecommerce-api

# 充実したルートCLAUDE.md
cat > CLAUDE.md << 'MDEOF'
# ECサイトバックエンドAPI

## 概要
ECサイトのバックエンドREST APIです。商品管理、ユーザー認証、注文処理、決済連携を提供します。
フロントエンド（Next.js）とJSON形式のAPIで連携します。

## 技術スタック
- ランタイム: Node.js 20 LTS
- フレームワーク: Express 4.x
- データベース: PostgreSQL 15
- ORM: Prisma 5.x
- テスト: Jest + Supertest
- リンター: ESLint + Prettier
- 認証: JWT（jsonwebtoken）

## ディレクトリ構成
```
src/
├── controllers/  # APIエンドポイント（HTTPリクエスト処理）
├── services/     # ビジネスロジック（DBアクセスもここ）
├── models/       # Prismaスキーマとカスタム型
├── middleware/    # Express ミドルウェア（認証、エラーハンドリング）
└── utils/        # 共通ユーティリティ（ロガー、バリデータ等）
tests/
├── unit/         # ユニットテスト（サービス層中心）
└── integration/  # 統合テスト（API全体の動作確認）
```

## コーディング規約
- 変数・関数: camelCase（例: getUserById）
- クラス: PascalCase（例: UserService）
- 定数: UPPER_SNAKE_CASE（例: MAX_LOGIN_ATTEMPTS）
- ファイル名: controllers/servicesはcamelCase、modelsはPascalCase
- インポート順: Node.js標準 → 外部パッケージ → プロジェクト内（空行で区切る）
- 非同期処理: async/await を使用（.then()チェーンは避ける）
- エラー: AppErrorクラスでラップ、HTTPステータスコードを付与

## 開発コマンド
- `npm run dev` : 開発サーバー起動（nodemon使用、ホットリロード）
- `npm test` : 全テスト実行
- `npm run test:unit` : ユニットテストのみ
- `npm run test:integration` : 統合テストのみ（DB接続が必要）
- `npm run lint` : ESLint実行
- `npm run lint:fix` : ESLint自動修正
- `npx prisma migrate dev` : DBマイグレーション実行
- `npx prisma studio` : DB管理UI起動

## 重要なルール
- **絶対に変更しないファイル**: `prisma/migrations/`（既存マイグレーション）
- **変更時にレビュー必須**: `src/middleware/auth.js`、`prisma/schema.prisma`
- **コミット禁止**: `.env`、`*.pem`、`*.key`
- **APIレスポンス形式**: `{ success: boolean, data: any, error?: string }` で統一
- **テスト**: 新機能追加時はユニットテストを必ず書く
- **DB操作**: 直接SQLを書かずPrisma ORMを通す
MDEOF

# サブディレクトリCLAUDE.md
cat > src/CLAUDE.md << 'MDEOF'
# src/ コーディングルール

## controller → service → model の3層アーキテクチャ
- controller: HTTPリクエストの受付とレスポンスの返却のみ
- service: ビジネスロジックとDBアクセス
- controllerからPrismaクライアントを直接呼ばない

## エラーハンドリング
```js
// 正しい例
throw new AppError("User not found", 404);

// 悪い例
res.status(404).json({ error: "User not found" });  // controllerで直接返さない
```

## バリデーション
- リクエストのバリデーションはcontrollerで行う
- ビジネスルールのバリデーションはserviceで行う
MDEOF

git add -A
git commit -m "Add CLAUDE.md for project configuration"
```

**初心者向けとの違い:**
- 初心者向けは最小限の情報で「まず動く」ことを重視しています
- 改良版はチーム開発を想定し、コーディング規約やアーキテクチャの方針まで詳細に記載しています
- サブディレクトリのCLAUDE.mdを追加することで、ディレクトリ固有のルールを明確化しています
- 実務では、CLAUDE.mdは「新しいチームメンバーへの引き継ぎ書」のような役割も果たします

</details>

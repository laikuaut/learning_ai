# 第1章: Next.js の基本

## 1.1 Next.js とは何か

Next.js は **React ベースのフルスタック Web フレームワーク**である。Vercel 社が開発・保守しており、React 単体では実現が難しいサーバーサイドレンダリング（SSR）、静的サイト生成（SSG）、API ルート、ファイルベースルーティングなどの機能を標準で提供する。

### React 単体との違い

| 機能 | React 単体 | Next.js |
|------|-----------|---------|
| ルーティング | 別途 react-router 等が必要 | ファイルベースで自動 |
| SSR/SSG | 自前で構築が必要 | 標準搭載 |
| API エンドポイント | Express 等が別途必要 | route.ts で統合 |
| 画像最適化 | 自前実装 | next/image で自動 |
| バンドル最適化 | webpack 設定が必要 | ゼロコンフィグ |
| SEO | SPA なので困難 | SSR/SSG で容易 |

### Next.js を選ぶべき場面

- **SEO が重要なサイト**（ブログ、EC サイト、コーポレートサイト）
- **初回表示速度が重要なアプリ**
- **フルスタック開発を一つのプロジェクトで完結させたい場合**
- **段階的な静的再生成（ISR）が必要な場合**

---

## 1.2 開発環境のセットアップ

### 前提条件

- **Node.js**: 18.17 以上（推奨: 20.x LTS）
- **パッケージマネージャ**: npm, yarn, pnpm, bun のいずれか
- **エディタ**: VS Code（推奨拡張: ES7+ React/Redux/React-Native snippets, Tailwind CSS IntelliSense）

### プロジェクトの作成

```bash
# npx を使う場合（最も一般的）
npx create-next-app@latest my-app

# yarn を使う場合
yarn create next-app my-app

# pnpm を使う場合
pnpm create next-app my-app

# bun を使う場合
bunx create-next-app my-app
```

### 対話式セットアップの選択肢

```
✔ What is your project named? … my-app
✔ Would you like to use TypeScript? … Yes    ← 推奨: Yes
✔ Would you like to use ESLint? … Yes        ← 推奨: Yes
✔ Would you like to use Tailwind CSS? … Yes  ← 推奨: Yes
✔ Would you like your code inside a `src/` directory? … Yes  ← 好みによる
✔ Would you like to use App Router? (recommended) … Yes      ← 必ず Yes
✔ Would you like to use Turbopack for next dev? … Yes        ← 推奨: Yes
✔ Would you like to customize the import alias (@/* by default)? … No
```

> **重要**: 本教材では **App Router** を前提とする。Pages Router は旧方式であり、新規プロジェクトでは App Router を使用すること。

---

## 1.3 プロジェクト構造

`create-next-app` で生成される典型的なプロジェクト構造は以下の通りである。

```
my-app/
├── app/                    # App Router のメインディレクトリ
│   ├── layout.tsx          # ルートレイアウト（必須）
│   ├── page.tsx            # トップページ (/)
│   ├── globals.css         # グローバルスタイル
│   └── favicon.ico         # ファビコン
├── public/                 # 静的ファイル（画像等）
│   ├── next.svg
│   └── vercel.svg
├── node_modules/           # 依存パッケージ
├── .eslintrc.json          # ESLint 設定
├── .gitignore              # Git 除外設定
├── next.config.ts          # Next.js 設定ファイル
├── package.json            # プロジェクト設定・依存関係
├── postcss.config.mjs      # PostCSS 設定（Tailwind 用）
├── tailwind.config.ts      # Tailwind CSS 設定
└── tsconfig.json           # TypeScript 設定
```

### 各ファイル・ディレクトリの役割

#### `app/` ディレクトリ
App Router の中核。このディレクトリ内のファイル構造がそのまま URL ルーティングに対応する。

#### `app/layout.tsx`（ルートレイアウト）
**全ページに共通するレイアウト**を定義する。`<html>` タグと `<body>` タグを含む必須ファイル。

```tsx
// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'My App',
  description: 'Next.js で作ったアプリ',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

#### `app/page.tsx`（トップページ）
`/` にアクセスしたときに表示されるページコンポーネント。

```tsx
// app/page.tsx
export default function HomePage() {
  return (
    <main>
      <h1>ようこそ Next.js へ！</h1>
      <p>これはトップページです。</p>
    </main>
  )
}
```

#### `public/` ディレクトリ
静的ファイルを配置する。`/public/images/logo.png` は `/images/logo.png` としてアクセス可能。

#### `next.config.ts`
Next.js のカスタム設定を記述する。

```ts
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // 画像の外部ドメインを許可
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
      },
    ],
  },
}

export default nextConfig
```

---

## 1.4 Pages Router と App Router の違い

### Pages Router（旧方式）

```
pages/
├── index.tsx          → /
├── about.tsx          → /about
├── blog/
│   ├── index.tsx      → /blog
│   └── [id].tsx       → /blog/:id
└── api/
    └── hello.ts       → /api/hello
```

- `getServerSideProps`、`getStaticProps` でデータ取得
- 全コンポーネントがクライアントコンポーネント
- `_app.tsx`、`_document.tsx` でレイアウト管理

### App Router（新方式・推奨）

```
app/
├── page.tsx           → /
├── layout.tsx         → 共通レイアウト
├── about/
│   └── page.tsx       → /about
├── blog/
│   ├── page.tsx       → /blog
│   └── [id]/
│       └── page.tsx   → /blog/:id
└── api/
    └── hello/
        └── route.ts   → /api/hello
```

- **サーバーコンポーネント**がデフォルト
- `layout.tsx` でネスト可能なレイアウト
- `loading.tsx`、`error.tsx` で UI 状態を宣言的に管理
- React Server Components (RSC) の完全サポート
- Server Actions でフォーム処理

### 移行の判断基準

| 状況 | 推奨 |
|------|------|
| 新規プロジェクト | App Router |
| 既存 Pages Router プロジェクト | 段階的に App Router へ移行 |
| 両方が混在するプロジェクト | 共存可能（同一プロジェクト内で並行運用可） |

---

## 1.5 開発サーバーの起動と基本操作

### 開発サーバーの起動

```bash
# 開発サーバーを起動（デフォルト: http://localhost:3000）
npm run dev

# ポートを指定する場合
npm run dev -- -p 4000

# Turbopack を使う場合（高速）
npm run dev -- --turbopack
```

### 基本的な npm スクリプト

```json
// package.json の scripts セクション
{
  "scripts": {
    "dev": "next dev",           // 開発サーバー起動
    "build": "next build",       // 本番ビルド
    "start": "next start",       // 本番サーバー起動
    "lint": "next lint"          // ESLint 実行
  }
}
```

### 開発中の便利な機能

1. **Hot Module Replacement (HMR)**: ファイルを保存すると自動でブラウザに反映される
2. **Fast Refresh**: React コンポーネントの状態を保持したまま更新
3. **エラーオーバーレイ**: エラーがブラウザ上に分かりやすく表示される
4. **TypeScript の自動検出**: `tsconfig.json` を自動生成・更新

### ビルドと本番実行

```bash
# 本番用にビルド
npm run build

# ビルド結果を確認（.next ディレクトリに生成される）
# - 静的ページは HTML ファイルとして生成
# - 動的ページはサーバーサイドで処理

# 本番サーバーを起動
npm start
```

---

## 1.6 最初のページを作ってみよう

### ステップ 1: トップページを編集

```tsx
// app/page.tsx
export default function HomePage() {
  return (
    <main style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Next.js 学習サイト</h1>
      <p>Next.js の基本を学びましょう。</p>

      <section>
        <h2>学習コンテンツ</h2>
        <ul>
          <li>ルーティングの基本</li>
          <li>サーバーコンポーネント</li>
          <li>データ取得</li>
          <li>API ルート</li>
        </ul>
      </section>
    </main>
  )
}
```

### ステップ 2: 新しいページを追加

```tsx
// app/about/page.tsx
export default function AboutPage() {
  return (
    <main style={{ padding: '2rem' }}>
      <h1>About</h1>
      <p>このサイトは Next.js の学習用に作成されました。</p>
    </main>
  )
}
```

この時点で `/about` にアクセスすると上記のページが表示される。**ファイルを作るだけでルーティングが完了する**のが App Router の特長である。

### ステップ 3: レイアウトにナビゲーションを追加

```tsx
// app/layout.tsx
import type { Metadata } from 'next'
import Link from 'next/link'
import './globals.css'

export const metadata: Metadata = {
  title: 'Next.js 学習サイト',
  description: 'Next.js を基礎から学ぶ',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body>
        <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc' }}>
          <Link href="/" style={{ marginRight: '1rem' }}>ホーム</Link>
          <Link href="/about">About</Link>
        </nav>
        {children}
      </body>
    </html>
  )
}
```

> **ポイント**: `<a>` タグではなく `next/link` の `<Link>` コンポーネントを使用すること。クライアントサイドナビゲーションにより、ページ遷移が高速になる。

---

## 1.7 TypeScript の活用

Next.js は TypeScript を第一級でサポートしている。

### 基本的な型定義

```tsx
// コンポーネントの Props 型定義
type CardProps = {
  title: string
  description: string
  href?: string  // オプショナル
}

export default function Card({ title, description, href }: CardProps) {
  return (
    <div>
      <h3>{title}</h3>
      <p>{description}</p>
      {href && <a href={href}>詳細を見る</a>}
    </div>
  )
}
```

### Next.js 固有の型

```tsx
import type { Metadata } from 'next'
import type { NextRequest } from 'next/server'

// ページの Metadata 型
export const metadata: Metadata = {
  title: 'ページタイトル',
}

// 動的ルートの Params 型
type PageProps = {
  params: Promise<{ id: string }>
}

export default async function Page({ params }: PageProps) {
  const { id } = await params
  return <div>ID: {id}</div>
}
```

---

## 1.8 まとめ

本章で学んだこと:

1. **Next.js** は React ベースのフルスタックフレームワークである
2. **create-next-app** でプロジェクトを簡単に作成できる
3. **App Router** が推奨される新しいルーティング方式である
4. `app/` ディレクトリ内のファイル構造が URL に直接対応する
5. `layout.tsx` で共通レイアウト、`page.tsx` でページを定義する
6. **開発サーバー**は `npm run dev` で起動する
7. `next/link` の `Link` コンポーネントでクライアントサイドナビゲーションを実現する

### 次章の予告

第2章では、App Router のルーティングシステムを詳しく学ぶ。動的ルート、ルートグループ、パラレルルートなどの高度な機能を扱う。

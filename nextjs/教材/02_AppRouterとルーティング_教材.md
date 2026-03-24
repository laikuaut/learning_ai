# 第2章: App Router とルーティング

## 2.1 App Router の基本概念

App Router は Next.js 13 で導入され、Next.js 14 以降で安定版となったルーティングシステムである。**ファイルシステムベースのルーティング**を採用しており、`app/` ディレクトリ内のフォルダ構造がそのまま URL パスに対応する。

### ルーティングの基本ルール

```
app/
├── page.tsx              → /
├── about/
│   └── page.tsx          → /about
├── blog/
│   ├── page.tsx          → /blog
│   └── [slug]/
│       └── page.tsx      → /blog/hello-world, /blog/my-post など
├── dashboard/
│   ├── layout.tsx        → /dashboard 以下の共通レイアウト
│   ├── page.tsx          → /dashboard
│   └── settings/
│       └── page.tsx      → /dashboard/settings
```

**重要なルール**:
- `page.tsx` があるディレクトリだけが URL としてアクセス可能になる
- `page.tsx` がないディレクトリは URL としては無効（404 になる）
- フォルダ名がそのまま URL セグメントになる

---

## 2.2 特殊ファイルの役割

App Router では、ディレクトリ内に特定の名前のファイルを配置することで、自動的に特別な振る舞いが割り当てられる。

### ファイル一覧と優先順位

| ファイル名 | 役割 | 必須 |
|-----------|------|------|
| `layout.tsx` | 共通レイアウト（子ルートと共有） | ルートのみ必須 |
| `page.tsx` | ページ本体（URL に対応するUI） | ルートを作るなら必須 |
| `loading.tsx` | ローディング UI（Suspense ベース） | 任意 |
| `error.tsx` | エラー UI（Error Boundary ベース） | 任意 |
| `not-found.tsx` | 404 ページ | 任意 |
| `template.tsx` | レイアウトの再マウント版 | 任意 |
| `default.tsx` | パラレルルートのデフォルト | パラレルルート時 |
| `route.ts` | API エンドポイント | API ルート時 |

### レンダリング順序（ネスト構造）

```
layout.tsx
  └── template.tsx
        └── error.tsx（Error Boundary）
              └── loading.tsx（Suspense Boundary）
                    └── not-found.tsx
                          └── page.tsx
```

---

## 2.3 layout.tsx — レイアウト

### ルートレイアウト（必須）

```tsx
// app/layout.tsx — ルートレイアウトは必ず必要
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body>
        <header>
          <nav>サイト共通ナビゲーション</nav>
        </header>
        <main>{children}</main>
        <footer>フッター</footer>
      </body>
    </html>
  )
}
```

### ネストされたレイアウト

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div style={{ display: 'flex' }}>
      <aside style={{ width: '250px' }}>
        <nav>
          <ul>
            <li><a href="/dashboard">概要</a></li>
            <li><a href="/dashboard/analytics">分析</a></li>
            <li><a href="/dashboard/settings">設定</a></li>
          </ul>
        </nav>
      </aside>
      <section style={{ flex: 1 }}>{children}</section>
    </div>
  )
}
```

このレイアウトは `/dashboard`、`/dashboard/analytics`、`/dashboard/settings` すべてで共有される。**ページ遷移時にレイアウトは再レンダリングされない**（状態が保持される）。

### layout.tsx の特徴

1. **状態が保持される**: ナビゲーション間でレイアウトコンポーネントの状態は維持される
2. **再レンダリングされない**: 子ルート間の移動ではレイアウトは再レンダリングされない
3. **ネスト可能**: 親子関係のディレクトリで複数のレイアウトを重ねられる
4. **サーバーコンポーネント**: デフォルトでサーバーコンポーネントとして動作する

---

## 2.4 loading.tsx — ローディング UI

`loading.tsx` を配置すると、ページの読み込み中に自動的にローディング UI が表示される。内部的には React の `<Suspense>` を使用している。

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', padding: '2rem' }}>
      <div className="spinner" />
      <p>読み込み中...</p>
    </div>
  )
}
```

### 動作の仕組み

```tsx
// Next.js が内部的に行っていること（概念図）
<Layout>
  <Suspense fallback={<Loading />}>
    <Page />
  </Suspense>
</Layout>
```

ページコンポーネントの読み込みが完了するまで `Loading` コンポーネントが表示される。**ストリーミング SSR** と組み合わせることで、ページの一部を先に表示し、残りを非同期で読み込む体験を実現できる。

---

## 2.5 error.tsx — エラーハンドリング

`error.tsx` はそのルートセグメント内で発生したエラーをキャッチし、フォールバック UI を表示する。React の Error Boundary をベースにしている。

```tsx
// app/dashboard/error.tsx
'use client' // error.tsx は必ずクライアントコンポーネントにする

import { useEffect } from 'react'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // エラーをログサービスに送信する
    console.error(error)
  }, [error])

  return (
    <div style={{ padding: '2rem', textAlign: 'center' }}>
      <h2>エラーが発生しました</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>
        もう一度試す
      </button>
    </div>
  )
}
```

### 注意点

- `error.tsx` は **必ず `'use client'`** を付ける（Error Boundary はクライアント機能のため）
- `reset()` 関数で再レンダリングを試行できる
- **同じディレクトリの `layout.tsx` のエラーはキャッチしない**（親の `error.tsx` でキャッチする）
- ルートレイアウトのエラーには `app/global-error.tsx` を使用する

### global-error.tsx

```tsx
// app/global-error.tsx — ルートレイアウトのエラーをキャッチ
'use client'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <html>
      <body>
        <h2>重大なエラーが発生しました</h2>
        <button onClick={() => reset()}>もう一度試す</button>
      </body>
    </html>
  )
}
```

---

## 2.6 not-found.tsx — 404 ページ

```tsx
// app/not-found.tsx
import Link from 'next/link'

export default function NotFound() {
  return (
    <div style={{ textAlign: 'center', padding: '4rem' }}>
      <h1>404</h1>
      <h2>ページが見つかりません</h2>
      <p>お探しのページは存在しないか、移動された可能性があります。</p>
      <Link href="/">ホームに戻る</Link>
    </div>
  )
}
```

### プログラムから 404 をトリガーする

```tsx
// app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation'

export default async function BlogPost({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const post = await getPost(slug)

  if (!post) {
    notFound() // not-found.tsx を表示する
  }

  return <article>{post.content}</article>
}
```

---

## 2.7 動的ルート

### 基本的な動的ルート — `[param]`

```
app/blog/[slug]/page.tsx  →  /blog/hello-world, /blog/my-post
```

```tsx
// app/blog/[slug]/page.tsx
type Props = {
  params: Promise<{ slug: string }>
}

export default async function BlogPost({ params }: Props) {
  const { slug } = await params
  return <h1>記事: {slug}</h1>
}
```

### 複数の動的セグメント

```
app/shop/[category]/[productId]/page.tsx
→ /shop/electronics/123
→ params = { category: 'electronics', productId: '123' }
```

```tsx
// app/shop/[category]/[productId]/page.tsx
type Props = {
  params: Promise<{ category: string; productId: string }>
}

export default async function ProductPage({ params }: Props) {
  const { category, productId } = await params
  return (
    <div>
      <p>カテゴリ: {category}</p>
      <p>商品ID: {productId}</p>
    </div>
  )
}
```

### キャッチオールセグメント — `[...param]`

```
app/docs/[...slug]/page.tsx
→ /docs/a          → slug = ['a']
→ /docs/a/b        → slug = ['a', 'b']
→ /docs/a/b/c      → slug = ['a', 'b', 'c']
→ /docs             → 404（マッチしない）
```

```tsx
// app/docs/[...slug]/page.tsx
type Props = {
  params: Promise<{ slug: string[] }>
}

export default async function DocsPage({ params }: Props) {
  const { slug } = await params
  return <p>パス: {slug.join(' / ')}</p>
}
```

### オプショナルキャッチオール — `[[...param]]`

```
app/docs/[[...slug]]/page.tsx
→ /docs             → slug = undefined（マッチする！）
→ /docs/a           → slug = ['a']
→ /docs/a/b         → slug = ['a', 'b']
```

---

## 2.8 ルートグループ — `(group)`

フォルダ名を `()` で囲むと、**URL パスに影響を与えずにルートを整理**できる。

### 用途 1: 論理的な整理

```
app/
├── (marketing)/
│   ├── about/
│   │   └── page.tsx      → /about
│   ├── contact/
│   │   └── page.tsx      → /contact
│   └── layout.tsx         → マーケティングページ用レイアウト
├── (shop)/
│   ├── products/
│   │   └── page.tsx      → /products
│   ├── cart/
│   │   └── page.tsx      → /cart
│   └── layout.tsx         → ショップ用レイアウト
```

### 用途 2: 異なるレイアウトの適用

```tsx
// app/(marketing)/layout.tsx — マーケティング用レイアウト
export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div>
      <header>マーケティングサイトヘッダー</header>
      {children}
    </div>
  )
}

// app/(shop)/layout.tsx — ショップ用レイアウト
export default function ShopLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div>
      <header>ショップヘッダー（カートアイコン付き）</header>
      {children}
    </div>
  )
}
```

### 用途 3: 認証状態によるレイアウト分離

```
app/
├── (auth)/
│   ├── login/
│   │   └── page.tsx      → /login（シンプルなレイアウト）
│   ├── register/
│   │   └── page.tsx      → /register
│   └── layout.tsx
├── (dashboard)/
│   ├── dashboard/
│   │   └── page.tsx      → /dashboard（サイドバー付きレイアウト）
│   └── layout.tsx
```

---

## 2.9 パラレルルート — `@slot`

パラレルルートを使うと、**同じレイアウト内で複数のページを同時にレンダリング**できる。ダッシュボードのように複数の独立したセクションを持つ UI に最適。

### ディレクトリ構造

```
app/dashboard/
├── layout.tsx
├── page.tsx
├── @analytics/
│   ├── page.tsx
│   └── default.tsx
├── @team/
│   ├── page.tsx
│   └── default.tsx
```

### レイアウトで複数のスロットを受け取る

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  analytics,
  team,
}: {
  children: React.ReactNode
  analytics: React.ReactNode
  team: React.ReactNode
}) {
  return (
    <div>
      <div>{children}</div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
        <div>{analytics}</div>
        <div>{team}</div>
      </div>
    </div>
  )
}
```

```tsx
// app/dashboard/@analytics/page.tsx
export default function AnalyticsPage() {
  return (
    <div>
      <h2>アクセス解析</h2>
      <p>今月のPV: 12,345</p>
    </div>
  )
}

// app/dashboard/@team/page.tsx
export default function TeamPage() {
  return (
    <div>
      <h2>チームメンバー</h2>
      <ul>
        <li>田中太郎</li>
        <li>鈴木花子</li>
      </ul>
    </div>
  )
}
```

### default.tsx の重要性

パラレルルートでは、ナビゲーション時にスロットの対応するページが存在しない場合に `default.tsx` が使用される。これがないと 404 になる。

```tsx
// app/dashboard/@analytics/default.tsx
export default function Default() {
  return null // または適切なフォールバック UI
}
```

---

## 2.10 インターセプトルート

インターセプトルートを使うと、**現在のレイアウトを維持しながら別のルートのコンテンツを表示**できる。モーダルの実装に最適。

### 規約

| 記法 | 意味 |
|------|------|
| `(.)folder` | 同じレベルのルートをインターセプト |
| `(..)folder` | 1つ上のレベルをインターセプト |
| `(..)(..)folder` | 2つ上のレベルをインターセプト |
| `(...)folder` | ルートからインターセプト |

### モーダルの例

```
app/
├── feed/
│   ├── page.tsx           → 投稿一覧
│   └── (..)photo/[id]/
│       └── page.tsx       → モーダルで写真表示
├── photo/[id]/
│   └── page.tsx           → 直接アクセス時のフルページ表示
├── layout.tsx
└── @modal/
    └── default.tsx
```

---

## 2.11 ナビゲーション

### Link コンポーネント

```tsx
import Link from 'next/link'

export default function Navigation() {
  return (
    <nav>
      {/* 基本 */}
      <Link href="/about">About</Link>

      {/* 動的ルート */}
      <Link href={`/blog/${post.slug}`}>記事を読む</Link>

      {/* オブジェクト形式 */}
      <Link
        href={{
          pathname: '/blog/[slug]',
          query: { slug: 'hello-world' },
        }}
      >
        記事
      </Link>

      {/* スクロール位置の制御 */}
      <Link href="/about" scroll={false}>About（スクロール維持）</Link>

      {/* アクティブリンクの検出は usePathname で */}
    </nav>
  )
}
```

### useRouter（プログラムによるナビゲーション）

```tsx
'use client'

import { useRouter } from 'next/navigation'

export default function LoginForm() {
  const router = useRouter()

  const handleLogin = async () => {
    const success = await login()
    if (success) {
      router.push('/dashboard')       // ページ遷移
      // router.replace('/dashboard') // 履歴を置き換え
      // router.back()                // 戻る
      // router.forward()             // 進む
      // router.refresh()             // 現在のページを再取得
    }
  }

  return <button onClick={handleLogin}>ログイン</button>
}
```

### usePathname と useSearchParams

```tsx
'use client'

import { usePathname, useSearchParams } from 'next/navigation'

export default function Breadcrumb() {
  const pathname = usePathname()        // 例: '/blog/hello'
  const searchParams = useSearchParams() // 例: ?page=2

  const page = searchParams.get('page') // '2'

  return (
    <div>
      <p>現在のパス: {pathname}</p>
      {page && <p>ページ: {page}</p>}
    </div>
  )
}
```

---

## 2.12 まとめ

本章で学んだこと:

1. **App Router** はファイルシステムベースのルーティングを提供する
2. **特殊ファイル**（`layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`）で UI 状態を宣言的に管理する
3. **動的ルート** `[param]` で可変の URL パスに対応する
4. **ルートグループ** `(group)` で URL に影響を与えずにファイルを整理できる
5. **パラレルルート** `@slot` で複数のページを同時にレンダリングする
6. **インターセプトルート** でモーダルパターンを実現する
7. `Link` コンポーネントと `useRouter` でナビゲーションを制御する

### 次章の予告

第3章では、App Router の核心であるサーバーコンポーネントとクライアントコンポーネントの使い分けについて詳しく学ぶ。

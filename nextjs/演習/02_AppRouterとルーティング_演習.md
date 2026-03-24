# 第2章 演習：App Router とルーティング

---

## 演習1（基本）：特殊ファイルの役割を整理しよう

以下の App Router 特殊ファイルについて、それぞれの役割を一言で説明してください。

1. `page.tsx`
2. `layout.tsx`
3. `loading.tsx`
4. `error.tsx`
5. `not-found.tsx`
6. `template.tsx`
7. `route.ts`

<details>
<summary>ヒント</summary>

各ファイルは App Router のレンダリングパイプラインにおいて特定の役割を担っています。表示順序（layout → template → error boundary → loading → page）を意識して整理しましょう。

</details>

<details>
<summary>解答例</summary>

1. **`page.tsx`**: ページ本体。そのルートにアクセスしたときに表示される UI コンポーネント。
2. **`layout.tsx`**: 共通レイアウト。子ルートで共有され、ナビゲーション間で状態が保持される。
3. **`loading.tsx`**: ローディング UI。ページの読み込み中に自動的に表示される（Suspense ベース）。
4. **`error.tsx`**: エラー UI。ルートセグメント内で発生したエラーをキャッチしてフォールバック UI を表示する（Error Boundary ベース）。必ず `'use client'` が必要。
5. **`not-found.tsx`**: 404 ページ。ルートが存在しない場合や `notFound()` が呼ばれた場合に表示される。
6. **`template.tsx`**: レイアウトの再マウント版。layout.tsx と似ているが、ナビゲーションのたびに再マウントされる。
7. **`route.ts`**: API エンドポイント。HTTP メソッド（GET, POST 等）に対応するハンドラを定義する。`page.tsx` と同じディレクトリには共存できない。

</details>

---

## 演習2（基本）：loading.tsx を作成しよう

ダッシュボードページ（`/dashboard`）にローディング UI を追加してください。

**要件：**
- `app/dashboard/page.tsx` を作成する
- `app/dashboard/loading.tsx` を作成する
- ローディング中に「読み込み中...」と表示する

<details>
<summary>ヒント</summary>

`loading.tsx` を配置するだけで、そのルートのページが読み込まれるまで自動的にローディング UI が表示されます。内部的には React の `<Suspense>` が使われています。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '4rem',
    }}>
      <p style={{ fontSize: '1.2rem', color: '#666' }}>読み込み中...</p>
    </div>
  )
}
```

```tsx
// app/dashboard/page.tsx
export default function DashboardPage() {
  return (
    <div style={{ padding: '2rem' }}>
      <h1>ダッシュボード</h1>
      <p>ダッシュボードの内容がここに表示されます。</p>
    </div>
  )
}
```

`loading.tsx` を配置することで、Next.js が自動的に以下のような構造を構築します:

```tsx
<Layout>
  <Suspense fallback={<Loading />}>
    <Page />
  </Suspense>
</Layout>
```

</details>

---

## 演習3（基本）：error.tsx を作成しよう

エラーが発生したときにフォールバック UI を表示する `error.tsx` を作成してください。

**要件：**
- `app/dashboard/error.tsx` を作成する
- `'use client'` ディレクティブを付ける
- エラーメッセージを表示する
- 「もう一度試す」ボタンで `reset()` を呼び出す

<details>
<summary>ヒント</summary>

`error.tsx` は必ずクライアントコンポーネント（`'use client'`）にする必要があります。`error` オブジェクトと `reset` 関数が props として渡されます。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/dashboard/error.tsx
'use client' // 必須: Error Boundary はクライアントコンポーネント

import { useEffect } from 'react'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // エラーをログに記録（本番環境ではログサービスに送信）
    console.error('ダッシュボードエラー:', error)
  }, [error])

  return (
    <div style={{
      padding: '2rem',
      textAlign: 'center',
      backgroundColor: '#fff5f5',
      borderRadius: '8px',
      margin: '2rem',
    }}>
      <h2 style={{ color: '#e53e3e' }}>エラーが発生しました</h2>
      <p style={{ color: '#666' }}>{error.message}</p>
      <button
        onClick={() => reset()}
        style={{
          padding: '0.5rem 1rem',
          backgroundColor: '#3182ce',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
        }}
      >
        もう一度試す
      </button>
    </div>
  )
}
```

`error.tsx` は同じディレクトリの `page.tsx` で発生したエラーをキャッチします。ただし、同じディレクトリの `layout.tsx` のエラーはキャッチしません（親の `error.tsx` でキャッチされます）。

</details>

---

## 演習4（基本）：not-found.tsx をカスタマイズしよう

カスタムの 404 ページを作成してください。

**要件：**
- `app/not-found.tsx` を作成する
- 「ページが見つかりません」というメッセージを表示する
- ホームに戻る `Link` を配置する

<details>
<summary>ヒント</summary>

`app/not-found.tsx` を配置するだけで、存在しない URL にアクセスしたときにカスタムの 404 ページが表示されます。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/not-found.tsx
import Link from 'next/link'

export default function NotFound() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '60vh',
    }}>
      <h1 style={{ fontSize: '4rem', margin: '0' }}>404</h1>
      <h2>ページが見つかりません</h2>
      <p style={{ color: '#666' }}>
        お探しのページは存在しないか、移動された可能性があります。
      </p>
      <Link
        href="/"
        style={{
          marginTop: '1rem',
          padding: '0.75rem 1.5rem',
          backgroundColor: '#0070f3',
          color: 'white',
          borderRadius: '6px',
          textDecoration: 'none',
        }}
      >
        ホームに戻る
      </Link>
    </div>
  )
}
```

ブラウザで `/nonexistent-page` のような存在しない URL にアクセスすると、このカスタム 404 ページが表示されます。

</details>

---

## 演習5（応用）：動的ルートを作成しよう

ブログ記事の動的ルートを作成し、URL パラメータを表示してください。

**要件：**
- `app/blog/[slug]/page.tsx` を作成する
- URL パラメータ `slug` を取得して表示する
- `/blog/hello-world` や `/blog/my-post` にアクセスしてパラメータが正しく表示されることを確認する

<details>
<summary>ヒント</summary>

動的ルートは `[パラメータ名]` フォルダで作成します。`params` は Next.js 15 以降では `Promise` として渡されるため、`await` で展開する必要があります。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/blog/[slug]/page.tsx
type Props = {
  params: Promise<{ slug: string }>
}

export default async function BlogPostPage({ params }: Props) {
  const { slug } = await params

  return (
    <article style={{ padding: '2rem', maxWidth: '700px', margin: '0 auto' }}>
      <h1>ブログ記事: {slug}</h1>
      <p style={{ color: '#666' }}>
        この記事は slug パラメータ「{slug}」で識別されています。
      </p>
      <p>
        URL を変えてアクセスしてみましょう:
      </p>
      <ul>
        <li><code>/blog/hello-world</code></li>
        <li><code>/blog/nextjs-tutorial</code></li>
        <li><code>/blog/react-tips</code></li>
      </ul>
    </article>
  )
}
```

`[slug]` フォルダ内の `page.tsx` は、`slug` に任意の値がマッチします。`params.slug` でその値を取得できます。

</details>

---

## 演習6（応用）：ルートグループでレイアウトを分離しよう

ルートグループ `()` を使って、マーケティングページとアプリケーションページで異なるレイアウトを適用してください。

**要件：**
- `(marketing)` グループ: トップページと About ページ（ヘッダー付きレイアウト）
- `(app)` グループ: ダッシュボードページ（サイドバー付きレイアウト）
- URL にはグループ名が含まれないこと（`/about`, `/dashboard`）

```
app/
├── layout.tsx
├── (marketing)/
│   ├── layout.tsx
│   ├── page.tsx           → /
│   └── about/
│       └── page.tsx       → /about
├── (app)/
│   ├── layout.tsx
│   └── dashboard/
│       └── page.tsx       → /dashboard
```

<details>
<summary>ヒント</summary>

`()` で囲んだフォルダ名は URL パスに影響しません。各グループに独自の `layout.tsx` を配置することで、セクションごとに異なるレイアウトを適用できます。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/layout.tsx（ルートレイアウト）
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body style={{ margin: 0, fontFamily: 'sans-serif' }}>
        {children}
      </body>
    </html>
  )
}
```

```tsx
// app/(marketing)/layout.tsx（マーケティング用レイアウト）
import Link from 'next/link'

export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div>
      <header style={{
        padding: '1rem 2rem',
        backgroundColor: '#1a202c',
        color: 'white',
      }}>
        <nav style={{ display: 'flex', gap: '1rem' }}>
          <Link href="/" style={{ color: 'white' }}>ホーム</Link>
          <Link href="/about" style={{ color: 'white' }}>About</Link>
          <Link href="/dashboard" style={{ color: 'white' }}>ダッシュボード</Link>
        </nav>
      </header>
      <main style={{ padding: '2rem' }}>{children}</main>
    </div>
  )
}
```

```tsx
// app/(app)/layout.tsx（アプリケーション用レイアウト）
import Link from 'next/link'

export default function AppLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <aside style={{
        width: '250px',
        backgroundColor: '#f7fafc',
        borderRight: '1px solid #e2e8f0',
        padding: '1rem',
      }}>
        <h3>メニュー</h3>
        <nav>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            <li><Link href="/dashboard">ダッシュボード</Link></li>
            <li><Link href="/">マーケティングサイトへ</Link></li>
          </ul>
        </nav>
      </aside>
      <main style={{ flex: 1, padding: '2rem' }}>{children}</main>
    </div>
  )
}
```

```tsx
// app/(marketing)/page.tsx
export default function HomePage() {
  return <h1>マーケティングトップページ</h1>
}

// app/(marketing)/about/page.tsx
export default function AboutPage() {
  return <h1>About ページ</h1>
}

// app/(app)/dashboard/page.tsx
export default function DashboardPage() {
  return <h1>ダッシュボード</h1>
}
```

`(marketing)` と `(app)` はそれぞれ異なる `layout.tsx` を持ちますが、URL にグループ名は含まれません。`/` はヘッダー付き、`/dashboard` はサイドバー付きで表示されます。

</details>

---

## 演習7（応用）：usePathname でアクティブリンクを実装しよう

ナビゲーションで現在のページに対応するリンクをハイライト表示してください。

**要件：**
- `app/components/NavLink.tsx` をクライアントコンポーネントとして作成する
- `usePathname` を使って現在のパスを取得する
- 現在のパスに一致するリンクにスタイルを適用する

<details>
<summary>ヒント</summary>

`usePathname` は `'use client'` コンポーネント内で使用できます。`next/navigation` からインポートしてください。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/components/NavLink.tsx
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

type NavLinkProps = {
  href: string
  children: React.ReactNode
}

export default function NavLink({ href, children }: NavLinkProps) {
  const pathname = usePathname()
  const isActive = pathname === href

  return (
    <Link
      href={href}
      style={{
        color: isActive ? '#0070f3' : '#333',
        fontWeight: isActive ? 'bold' : 'normal',
        textDecoration: 'none',
        borderBottom: isActive ? '2px solid #0070f3' : 'none',
        paddingBottom: '4px',
      }}
    >
      {children}
    </Link>
  )
}
```

```tsx
// app/layout.tsx
import NavLink from './components/NavLink'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body>
        <nav style={{ display: 'flex', gap: '1.5rem', padding: '1rem 2rem' }}>
          <NavLink href="/">ホーム</NavLink>
          <NavLink href="/about">About</NavLink>
          <NavLink href="/blog">ブログ</NavLink>
        </nav>
        {children}
      </body>
    </html>
  )
}
```

`usePathname` はクライアント側で動作するため、`'use client'` が必要です。ナビゲーション部分だけをクライアントコンポーネントに切り出すことで、レイアウトの大部分はサーバーコンポーネントのままに保てます。

</details>

---

## 演習8（チャレンジ）：キャッチオールセグメントでドキュメントページを作ろう

キャッチオールセグメント `[...slug]` を使って、階層的なドキュメントページを作成してください。

**要件：**
- `app/docs/[...slug]/page.tsx` を作成する
- URL の各セグメントをパンくずリスト風に表示する
- `/docs/react/hooks/useState` のような深い階層にも対応する

<details>
<summary>ヒント</summary>

キャッチオールセグメント `[...slug]` を使うと、`slug` は文字列の配列として渡されます。例: `/docs/a/b/c` → `slug = ['a', 'b', 'c']`。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/docs/[...slug]/page.tsx
import Link from 'next/link'

type Props = {
  params: Promise<{ slug: string[] }>
}

export default async function DocsPage({ params }: Props) {
  const { slug } = await params

  return (
    <div style={{ padding: '2rem' }}>
      {/* パンくずリスト */}
      <nav style={{ marginBottom: '1rem', color: '#666' }}>
        <Link href="/docs" style={{ color: '#0070f3' }}>Docs</Link>
        {slug.map((segment, index) => {
          const href = '/docs/' + slug.slice(0, index + 1).join('/')
          return (
            <span key={index}>
              {' / '}
              {index === slug.length - 1 ? (
                <strong>{segment}</strong>
              ) : (
                <Link href={href} style={{ color: '#0070f3' }}>
                  {segment}
                </Link>
              )}
            </span>
          )
        })}
      </nav>

      <h1>{slug[slug.length - 1]}</h1>
      <p>パス: /docs/{slug.join('/')}</p>
      <p>セグメント数: {slug.length}</p>
      <p>各セグメント: {slug.join(' → ')}</p>
    </div>
  )
}
```

`/docs/react/hooks/useState` にアクセスすると、`slug` は `['react', 'hooks', 'useState']` となります。キャッチオールセグメントは任意の深さの階層を1つのルートで処理できるため、ドキュメントサイトなどに最適です。

</details>

---

## 演習9（チャレンジ）：useRouter でプログラムナビゲーションを実装しよう

検索フォームを作成し、送信時にプログラムで検索結果ページに遷移してください。

**要件：**
- `app/components/SearchForm.tsx` をクライアントコンポーネントとして作成する
- `useRouter` を使ってプログラムナビゲーションを行う
- 検索キーワードをクエリパラメータとして渡す（`/search?q=キーワード`）
- `app/search/page.tsx` で `searchParams` を取得して表示する

<details>
<summary>ヒント</summary>

`useRouter` は `next/navigation` からインポートします。`router.push('/search?q=キーワード')` でクエリパラメータ付きのナビゲーションが可能です。`searchParams` は `page.tsx` の props として受け取れます。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/components/SearchForm.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function SearchForm() {
  const [query, setQuery] = useState('')
  const router = useRouter()

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (query.trim()) {
      // プログラムでナビゲーション
      router.push(`/search?q=${encodeURIComponent(query)}`)
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '0.5rem' }}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="検索キーワードを入力..."
        style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid #ccc' }}
      />
      <button
        type="submit"
        style={{
          padding: '0.5rem 1rem',
          backgroundColor: '#0070f3',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
        }}
      >
        検索
      </button>
    </form>
  )
}
```

```tsx
// app/search/page.tsx
type Props = {
  searchParams: Promise<{ q?: string }>
}

export default async function SearchPage({ searchParams }: Props) {
  const { q } = await searchParams

  return (
    <div style={{ padding: '2rem' }}>
      <h1>検索結果</h1>
      {q ? (
        <p>「{q}」の検索結果を表示しています。</p>
      ) : (
        <p>検索キーワードが指定されていません。</p>
      )}
    </div>
  )
}
```

`useRouter` はクライアントコンポーネントでのプログラムナビゲーションに使います。一方、`searchParams` はサーバーコンポーネントの `page.tsx` で直接受け取れます。

</details>

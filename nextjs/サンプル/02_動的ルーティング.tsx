/**
 * ============================================================
 * サンプル02: 動的ルーティング
 * ============================================================
 *
 * 【学べる内容】
 *   - 動的セグメント [param] によるルーティング
 *   - params（Promise）からのパラメータ取得
 *   - 複数の動的セグメント
 *   - キャッチオールセグメント [...slug]
 *   - notFound() による 404 ハンドリング
 *   - generateStaticParams による静的生成
 *
 * 【前提条件】
 *   - npx create-next-app@latest my-app でプロジェクト作成済み
 *   - App Router + TypeScript を選択済み
 *
 * 【ファイルの配置場所】
 *   各セクションを以下のパスに分割して配置してください:
 *
 *   1. app/blog/page.tsx             — ブログ一覧ページ
 *   2. app/blog/[slug]/page.tsx      — 個別記事ページ（動的ルート）
 *   3. app/shop/[category]/[id]/page.tsx — 複数パラメータ
 *   4. app/docs/[...slug]/page.tsx   — キャッチオールセグメント
 *   5. app/not-found.tsx             — カスタム 404 ページ
 *
 * 【実行方法】
 *   cd my-app
 *   npm run dev
 *   以下の URL にアクセス:
 *     http://localhost:3000/blog
 *     http://localhost:3000/blog/hello-world
 *     http://localhost:3000/shop/electronics/42
 *     http://localhost:3000/docs/react/hooks/useState
 *
 * ============================================================
 */

// ============================================================
// 1. app/blog/page.tsx — ブログ一覧ページ
// ============================================================
// 静的なブログ一覧から、各記事の動的ルートへリンクします。

import Link from 'next/link'

// 記事データの型定義
type Post = {
  slug: string
  title: string
  excerpt: string
  date: string
}

// ダミーの記事データ（実際には API やデータベースから取得）
const posts: Post[] = [
  {
    slug: 'nextjs-intro',
    title: 'Next.js 入門',
    excerpt: 'Next.js の基本的な概念と使い方を解説します。',
    date: '2026-03-01',
  },
  {
    slug: 'app-router-guide',
    title: 'App Router 完全ガイド',
    excerpt: 'App Router のルーティングシステムを詳しく学びます。',
    date: '2026-03-10',
  },
  {
    slug: 'server-components',
    title: 'サーバーコンポーネント活用術',
    excerpt: 'RSC を使ったパフォーマンス最適化の方法を紹介します。',
    date: '2026-03-20',
  },
]

export default function BlogListPage() {
  return (
    <div style={{ padding: '2rem', maxWidth: '700px', margin: '0 auto' }}>
      <h1>ブログ</h1>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {posts.map((post) => (
          <li
            key={post.slug}
            style={{
              padding: '1.5rem',
              borderBottom: '1px solid #e2e8f0',
            }}
          >
            <p style={{ color: '#999', fontSize: '0.85rem', margin: '0 0 0.25rem' }}>
              {post.date}
            </p>
            {/* 動的ルートへのリンク */}
            <Link
              href={`/blog/${post.slug}`}
              style={{ fontSize: '1.2rem', color: '#0070f3', textDecoration: 'none' }}
            >
              {post.title}
            </Link>
            <p style={{ color: '#666', margin: '0.5rem 0 0' }}>{post.excerpt}</p>
          </li>
        ))}
      </ul>
    </div>
  )
}

// ============================================================
// 2. app/blog/[slug]/page.tsx — 個別記事ページ（動的ルート）
// ============================================================
// [slug] フォルダにより、/blog/任意の値 がマッチします。
// params は Promise として渡されるため、await で展開します。

// import { notFound } from 'next/navigation'
// import type { Metadata } from 'next'

/*
// 記事データの取得（実際には API やデータベースを使用）
function getPost(slug: string): Post | undefined {
  return posts.find((post) => post.slug === slug)
}

// 動的メタデータの生成
type Props = {
  params: Promise<{ slug: string }>
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params
  const post = getPost(slug)

  if (!post) {
    return { title: '記事が見つかりません' }
  }

  return {
    title: post.title,
    description: post.excerpt,
  }
}

// 静的生成するパスの一覧（ビルド時に HTML が生成される）
export async function generateStaticParams() {
  return posts.map((post) => ({
    slug: post.slug,
  }))
}

export default async function BlogPostPage({ params }: Props) {
  const { slug } = await params
  const post = getPost(slug)

  // 記事が見つからない場合は 404 を表示
  if (!post) {
    notFound()
  }

  return (
    <article style={{ padding: '2rem', maxWidth: '700px', margin: '0 auto' }}>
      <p style={{ color: '#999' }}>{post.date}</p>
      <h1>{post.title}</h1>
      <p style={{ lineHeight: 1.8, color: '#333' }}>
        {post.excerpt}
      </p>
      <p style={{ lineHeight: 1.8, color: '#333' }}>
        これは slug パラメータ「{slug}」に対応する記事ページです。
        動的ルーティングにより、任意のスラッグがこのページにマッチします。
      </p>
      <Link href="/blog" style={{ color: '#0070f3' }}>
        ← 一覧に戻る
      </Link>
    </article>
  )
}
*/

// ============================================================
// 3. app/shop/[category]/[id]/page.tsx — 複数パラメータ
// ============================================================
// 複数の動的セグメントを使用する例です。
// /shop/electronics/42 → category='electronics', id='42'

/*
type ShopProps = {
  params: Promise<{ category: string; id: string }>
}

export default async function ProductPage({ params }: ShopProps) {
  const { category, id } = await params

  return (
    <div style={{ padding: '2rem', maxWidth: '700px', margin: '0 auto' }}>
      <nav style={{ color: '#999', marginBottom: '1rem' }}>
        ショップ / {category} / 商品 {id}
      </nav>
      <h1>商品詳細</h1>
      <dl style={{ lineHeight: 2 }}>
        <dt style={{ fontWeight: 'bold' }}>カテゴリ:</dt>
        <dd>{category}</dd>
        <dt style={{ fontWeight: 'bold' }}>商品ID:</dt>
        <dd>{id}</dd>
      </dl>
      <p style={{ color: '#666' }}>
        複数の動的セグメントを使うことで、
        <code>/shop/[category]/[id]</code> のような階層的な URL を処理できます。
      </p>
    </div>
  )
}
*/

// ============================================================
// 4. app/docs/[...slug]/page.tsx — キャッチオールセグメント
// ============================================================
// [...slug] は任意の深さの URL パスにマッチします。
// /docs/react          → slug = ['react']
// /docs/react/hooks    → slug = ['react', 'hooks']
// /docs/react/hooks/useState → slug = ['react', 'hooks', 'useState']

/*
type DocsProps = {
  params: Promise<{ slug: string[] }>
}

export default async function DocsPage({ params }: DocsProps) {
  const { slug } = await params

  return (
    <div style={{ padding: '2rem', maxWidth: '700px', margin: '0 auto' }}>
      {// パンくずリスト }
      <nav style={{ marginBottom: '1.5rem' }}>
        <Link href="/docs" style={{ color: '#0070f3' }}>Docs</Link>
        {slug.map((segment, index) => {
          const href = '/docs/' + slug.slice(0, index + 1).join('/')
          const isLast = index === slug.length - 1
          return (
            <span key={index}>
              <span style={{ margin: '0 0.5rem', color: '#999' }}>/</span>
              {isLast ? (
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

      <div style={{
        backgroundColor: '#f7fafc',
        padding: '1rem',
        borderRadius: '8px',
        marginTop: '1rem',
      }}>
        <h3>パス情報</h3>
        <p>URL: /docs/{slug.join('/')}</p>
        <p>セグメント数: {slug.length}</p>
        <p>パスの階層: {slug.join(' → ')}</p>
      </div>

      <p style={{ marginTop: '1rem', color: '#666' }}>
        キャッチオールセグメント <code>[...slug]</code> を使うと、
        任意の深さの URL パスを1つのページコンポーネントで処理できます。
        ドキュメントサイトやヘルプセンターの実装に最適です。
      </p>
    </div>
  )
}
*/

// ============================================================
// 5. app/not-found.tsx — カスタム 404 ページ
// ============================================================

/*
export default function NotFound() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '60vh',
    }}>
      <h1 style={{ fontSize: '6rem', margin: 0, color: '#e2e8f0' }}>404</h1>
      <h2 style={{ color: '#4a5568' }}>ページが見つかりません</h2>
      <p style={{ color: '#718096' }}>
        お探しのページは存在しないか、移動された可能性があります。
      </p>
      <Link
        href="/"
        style={{
          marginTop: '1.5rem',
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
*/

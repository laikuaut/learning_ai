/**
 * ============================================================
 * サンプル01: App Router の基本的なページ構成
 * ============================================================
 *
 * 【学べる内容】
 *   - App Router のファイルベースルーティング
 *   - ルートレイアウト（layout.tsx）の役割
 *   - ページコンポーネント（page.tsx）の作成
 *   - next/link を使ったクライアントサイドナビゲーション
 *   - TypeScript によるコンポーネントの型定義
 *
 * 【前提条件】
 *   - npx create-next-app@latest my-app でプロジェクトを作成済みであること
 *   - TypeScript + App Router を選択していること
 *
 * 【ファイルの配置場所】
 *   このファイルの各セクションを、以下のパスに分割して配置してください:
 *
 *   1. app/layout.tsx       — ルートレイアウト
 *   2. app/page.tsx         — トップページ (/)
 *   3. app/about/page.tsx   — About ページ (/about)
 *   4. app/contact/page.tsx — お問い合わせページ (/contact)
 *   5. app/components/Card.tsx — 再利用可能なカードコンポーネント
 *
 * 【実行方法】
 *   cd my-app
 *   npm run dev
 *   ブラウザで http://localhost:3000 にアクセス
 *
 * ============================================================
 */

// ============================================================
// 1. app/layout.tsx — ルートレイアウト
// ============================================================
// すべてのページに共通するレイアウトを定義します。
// <html> と <body> タグは必須です。

import type { Metadata } from 'next'
import Link from 'next/link'

// メタデータの設定（SEO に重要）
export const metadata: Metadata = {
  title: {
    default: 'Next.js 学習サイト',
    template: '%s | Next.js 学習サイト',
  },
  description: 'Next.js を基礎から学べるサイトです',
}

// ナビゲーションリンクの型定義
type NavItem = {
  href: string
  label: string
}

// ナビゲーション項目を配列で管理（変更が容易）
const navItems: NavItem[] = [
  { href: '/', label: 'ホーム' },
  { href: '/about', label: 'About' },
  { href: '/contact', label: 'お問い合わせ' },
]

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body style={{ margin: 0, fontFamily: 'sans-serif', color: '#333' }}>
        {/* === ヘッダー（全ページ共通） === */}
        <header
          style={{
            backgroundColor: '#1a202c',
            color: 'white',
            padding: '1rem 2rem',
          }}
        >
          <nav style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
            <strong style={{ marginRight: 'auto' }}>Next.js 学習サイト</strong>
            {navItems.map((item) => (
              // Link コンポーネントでクライアントサイドナビゲーション
              // <a> タグではなく Link を使うことで、ページ遷移が高速になります
              <Link
                key={item.href}
                href={item.href}
                style={{ color: 'white', textDecoration: 'none' }}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </header>

        {/* === メインコンテンツ（各ページの内容がここに入る） === */}
        <main style={{ maxWidth: '960px', margin: '0 auto', padding: '2rem' }}>
          {children}
        </main>

        {/* === フッター（全ページ共通） === */}
        <footer
          style={{
            backgroundColor: '#f7fafc',
            padding: '1.5rem 2rem',
            textAlign: 'center',
            borderTop: '1px solid #e2e8f0',
          }}
        >
          <p style={{ margin: 0, color: '#666' }}>
            &copy; 2026 Next.js 学習サイト. All rights reserved.
          </p>
        </footer>
      </body>
    </html>
  )
}

// ============================================================
// 2. app/page.tsx — トップページ (/)
// ============================================================
// サーバーコンポーネント（デフォルト）として動作します。
// 'use client' がないため、サーバーでレンダリングされます。

// import Card from './components/Card'

/*
export default function HomePage() {
  // 特徴データの配列
  const features = [
    {
      title: 'ファイルベースルーティング',
      description:
        'フォルダ構造がそのまま URL に対応します。設定ファイルなしでルーティングが完了します。',
    },
    {
      title: 'サーバーコンポーネント',
      description:
        'デフォルトでサーバーサイドレンダリング。SEO に有利で、初回表示が高速です。',
    },
    {
      title: 'TypeScript 対応',
      description:
        '型安全な開発が標準で行えます。コンパイル時にエラーを検出できます。',
    },
  ]

  return (
    <div>
      <h1>Next.js を学ぼう</h1>
      <p style={{ color: '#666', fontSize: '1.1rem', lineHeight: 1.6 }}>
        React ベースのフルスタックフレームワーク Next.js の基本を学びましょう。
        App Router を使ったモダンな Web アプリケーション開発を体験できます。
      </p>

      <h2>主な特徴</h2>
      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        {features.map((feature, index) => (
          <Card
            key={index}
            title={feature.title}
            description={feature.description}
          />
        ))}
      </div>
    </div>
  )
}
*/

// ============================================================
// 3. app/about/page.tsx — About ページ (/about)
// ============================================================

// import type { Metadata } from 'next'

// ページ固有のメタデータ（layout.tsx のテンプレートが適用される）
// export const metadata: Metadata = {
//   title: 'About',
//   description: 'このサイトについての説明ページです',
// }

/*
export default function AboutPage() {
  return (
    <div>
      <h1>About</h1>
      <p style={{ lineHeight: 1.8 }}>
        このサイトは Next.js の学習のために作成されました。
        App Router、サーバーコンポーネント、データフェッチングなど、
        モダンな Next.js の機能を段階的に学べます。
      </p>
    </div>
  )
}
*/

// ============================================================
// 4. app/contact/page.tsx — お問い合わせページ (/contact)
// ============================================================

// import type { Metadata } from 'next'

// export const metadata: Metadata = {
//   title: 'お問い合わせ',
//   description: 'お問い合わせフォームです',
// }

/*
export default function ContactPage() {
  return (
    <div>
      <h1>お問い合わせ</h1>
      <p style={{ color: '#666' }}>
        ご質問やご要望がありましたら、以下のフォームからお気軽にご連絡ください。
      </p>
      <form style={{ maxWidth: '500px' }}>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="name" style={{ display: 'block', marginBottom: '0.25rem' }}>
            お名前
          </label>
          <input
            type="text"
            id="name"
            name="name"
            style={{ width: '100%', padding: '0.5rem', boxSizing: 'border-box' }}
          />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="email" style={{ display: 'block', marginBottom: '0.25rem' }}>
            メールアドレス
          </label>
          <input
            type="email"
            id="email"
            name="email"
            style={{ width: '100%', padding: '0.5rem', boxSizing: 'border-box' }}
          />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="message" style={{ display: 'block', marginBottom: '0.25rem' }}>
            メッセージ
          </label>
          <textarea
            id="message"
            name="message"
            rows={5}
            style={{ width: '100%', padding: '0.5rem', boxSizing: 'border-box' }}
          />
        </div>
        <button
          type="submit"
          style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: '#0070f3',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '1rem',
          }}
        >
          送信する
        </button>
      </form>
    </div>
  )
}
*/

// ============================================================
// 5. app/components/Card.tsx — 再利用可能なカードコンポーネント
// ============================================================

// Props の型定義（TypeScript の活用）
type CardProps = {
  title: string
  description: string
}

function Card({ title, description }: CardProps) {
  return (
    <div
      style={{
        border: '1px solid #e2e8f0',
        borderRadius: '8px',
        padding: '1.5rem',
        flex: '1 1 250px',
        minWidth: '250px',
      }}
    >
      <h3 style={{ margin: '0 0 0.5rem', color: '#1a202c' }}>{title}</h3>
      <p style={{ margin: 0, color: '#666', lineHeight: 1.6 }}>{description}</p>
    </div>
  )
}

export default Card

/**
 * ============================================================
 * サンプル05: ネストレイアウト設計とメタデータ
 * ============================================================
 *
 * 【学べる内容】
 *   - ネストされたレイアウトの構築
 *   - ルートグループ () によるレイアウト分離
 *   - Metadata API の活用（静的・動的メタデータ）
 *   - title.template による統一的なタイトル管理
 *   - フォントの最適化（next/font）
 *   - 認証状態によるレイアウト切り替えパターン
 *
 * 【前提条件】
 *   - npx create-next-app@latest my-app でプロジェクト作成済み
 *   - App Router + TypeScript を選択済み
 *
 * 【ファイルの配置場所】
 *   各セクションを以下のディレクトリ構造に従って配置してください:
 *
 *   app/
 *   ├── layout.tsx                    ← ルートレイアウト (セクション1)
 *   ├── (marketing)/
 *   │   ├── layout.tsx               ← マーケティング用 (セクション2)
 *   │   ├── page.tsx                 → /
 *   │   ├── about/page.tsx           → /about
 *   │   └── pricing/page.tsx         → /pricing
 *   ├── (auth)/
 *   │   ├── layout.tsx               ← 認証ページ用 (セクション3)
 *   │   ├── login/page.tsx           → /login
 *   │   └── register/page.tsx        → /register
 *   ├── (dashboard)/
 *   │   ├── layout.tsx               ← ダッシュボード用 (セクション4)
 *   │   ├── dashboard/page.tsx       → /dashboard
 *   │   └── dashboard/settings/
 *   │       ├── layout.tsx           ← 設定タブ用 (セクション5)
 *   │       ├── page.tsx             → /dashboard/settings
 *   │       └── profile/page.tsx     → /dashboard/settings/profile
 *
 * 【実行方法】
 *   cd my-app
 *   npm run dev
 *   以下の URL にアクセスして、各レイアウトの違いを確認:
 *     http://localhost:3000/           (マーケティングレイアウト)
 *     http://localhost:3000/login      (認証レイアウト)
 *     http://localhost:3000/dashboard  (ダッシュボードレイアウト)
 *
 * ============================================================
 */

// ============================================================
// 1. app/layout.tsx — ルートレイアウト
// ============================================================
// すべてのページの基盤となるレイアウトです。
// <html> と <body> タグを含む唯一のファイルです。

import type { Metadata, Viewport } from 'next'
import { Noto_Sans_JP } from 'next/font/google'

// Google Fonts の最適化読み込み
// - ビルド時にフォントファイルをダウンロード（セルフホスティング）
// - レイアウトシフトを防止する size-adjust が自動適用
const notoSansJP = Noto_Sans_JP({
  subsets: ['latin'],
  weight: ['400', '700'],
  display: 'swap',
  variable: '--font-noto-sans-jp',
})

// グローバルなメタデータ設定
export const metadata: Metadata = {
  // title.template: 子ページの title を '%s | サイト名' に変換
  title: {
    default: 'My SaaS App',
    template: '%s | My SaaS App',
  },
  description: 'モダンな SaaS アプリケーション',
  // robots: 検索エンジンへの指示
  robots: {
    index: true,
    follow: true,
  },
  // Open Graph のデフォルト設定
  openGraph: {
    siteName: 'My SaaS App',
    locale: 'ja_JP',
    type: 'website',
  },
}

// Viewport の設定（Next.js 14+ 推奨形式）
export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#1a202c' },
  ],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja" className={notoSansJP.variable}>
      <body
        style={{
          margin: 0,
          fontFamily: 'var(--font-noto-sans-jp), sans-serif',
          color: '#2d3748',
          backgroundColor: '#ffffff',
        }}
      >
        {/* 各ルートグループのレイアウトが children に入る */}
        {children}
      </body>
    </html>
  )
}

// ============================================================
// 2. app/(marketing)/layout.tsx — マーケティング用レイアウト
// ============================================================
// ランディングページ、料金ページなどの公開ページ用
// ヘッダー + フッターのシンプルなレイアウト

/*
import Link from 'next/link'

export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {// ヘッダー: ロゴ + ナビゲーション + CTA }
      <header style={{
        padding: '1rem 2rem',
        borderBottom: '1px solid #e2e8f0',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <Link href="/" style={{ fontWeight: 'bold', fontSize: '1.2rem', textDecoration: 'none', color: '#2d3748' }}>
          My SaaS App
        </Link>
        <nav style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
          <Link href="/about" style={{ textDecoration: 'none', color: '#4a5568' }}>About</Link>
          <Link href="/pricing" style={{ textDecoration: 'none', color: '#4a5568' }}>料金</Link>
          <Link
            href="/login"
            style={{
              padding: '0.5rem 1rem',
              backgroundColor: '#0070f3',
              color: 'white',
              borderRadius: '6px',
              textDecoration: 'none',
            }}
          >
            ログイン
          </Link>
        </nav>
      </header>

      {// メインコンテンツ }
      <main style={{ flex: 1 }}>
        {children}
      </main>

      {// フッター }
      <footer style={{
        padding: '2rem',
        backgroundColor: '#1a202c',
        color: '#a0aec0',
        textAlign: 'center',
      }}>
        <p>&copy; 2026 My SaaS App. All rights reserved.</p>
      </footer>
    </div>
  )
}
*/

// ============================================================
// 3. app/(auth)/layout.tsx — 認証ページ用レイアウト
// ============================================================
// ログイン、登録ページ用のシンプルな中央寄せレイアウト
// ヘッダーやサイドバーは不要

/*
import Link from 'next/link'

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: '#f7fafc',
    }}>
      {// ロゴ }
      <Link
        href="/"
        style={{
          marginBottom: '2rem',
          fontWeight: 'bold',
          fontSize: '1.5rem',
          textDecoration: 'none',
          color: '#2d3748',
        }}
      >
        My SaaS App
      </Link>

      {// カード型のコンテンツエリア }
      <div style={{
        width: '100%',
        maxWidth: '420px',
        padding: '2rem',
        backgroundColor: '#ffffff',
        borderRadius: '12px',
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
      }}>
        {children}
      </div>

      {// フッターリンク }
      <p style={{ marginTop: '1.5rem', color: '#a0aec0', fontSize: '0.85rem' }}>
        <Link href="/" style={{ color: '#0070f3' }}>ホームに戻る</Link>
      </p>
    </div>
  )
}
*/

// ============================================================
// 4. app/(dashboard)/layout.tsx — ダッシュボード用レイアウト
// ============================================================
// ログイン後のアプリケーション用
// サイドバー + ヘッダーの管理画面レイアウト

/*
import Link from 'next/link'

// サイドバーのメニュー項目
type MenuItem = {
  href: string
  label: string
  icon: string // 絵文字で簡易的にアイコン表現
}

const menuItems: MenuItem[] = [
  { href: '/dashboard', label: 'ダッシュボード', icon: '📊' },
  { href: '/dashboard/settings', label: '設定', icon: '⚙️' },
]

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      {// サイドバー }
      <aside style={{
        width: '260px',
        backgroundColor: '#1a202c',
        color: '#e2e8f0',
        padding: '1.5rem',
        display: 'flex',
        flexDirection: 'column',
      }}>
        {// アプリ名 }
        <h2 style={{
          fontSize: '1.1rem',
          margin: '0 0 2rem',
          paddingBottom: '1rem',
          borderBottom: '1px solid #2d3748',
        }}>
          My SaaS App
        </h2>

        {// メニュー }
        <nav style={{ flex: 1 }}>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            {menuItems.map((item) => (
              <li key={item.href} style={{ marginBottom: '0.25rem' }}>
                <Link
                  href={item.href}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.75rem',
                    padding: '0.75rem 1rem',
                    borderRadius: '8px',
                    textDecoration: 'none',
                    color: '#e2e8f0',
                    transition: 'background-color 0.2s',
                  }}
                >
                  <span>{item.icon}</span>
                  <span>{item.label}</span>
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        {// ユーザー情報 }
        <div style={{
          padding: '1rem',
          borderTop: '1px solid #2d3748',
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem',
        }}>
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: '50%',
            backgroundColor: '#4a5568',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '0.85rem',
          }}>
            TN
          </div>
          <div>
            <p style={{ margin: 0, fontSize: '0.9rem' }}>田中太郎</p>
            <p style={{ margin: 0, fontSize: '0.75rem', color: '#a0aec0' }}>管理者</p>
          </div>
        </div>
      </aside>

      {// メインエリア }
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {// ヘッダーバー }
        <header style={{
          padding: '1rem 2rem',
          borderBottom: '1px solid #e2e8f0',
          backgroundColor: '#ffffff',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <h1 style={{ margin: 0, fontSize: '1.25rem' }}>ダッシュボード</h1>
          <Link href="/" style={{ color: '#e53e3e', textDecoration: 'none', fontSize: '0.9rem' }}>
            ログアウト
          </Link>
        </header>

        {// コンテンツ }
        <main style={{ flex: 1, padding: '2rem', backgroundColor: '#f7fafc' }}>
          {children}
        </main>
      </div>
    </div>
  )
}
*/

// ============================================================
// 5. app/(dashboard)/dashboard/settings/layout.tsx — 設定タブ
// ============================================================
// ダッシュボードレイアウトの中に、さらにネストされたレイアウト
// 設定ページ内のタブナビゲーション

/*
import Link from 'next/link'

const settingsTabs = [
  { href: '/dashboard/settings', label: '一般設定' },
  { href: '/dashboard/settings/profile', label: 'プロフィール' },
]

export default function SettingsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div>
      <h2 style={{ margin: '0 0 1rem' }}>設定</h2>

      {// タブナビゲーション }
      <div style={{
        display: 'flex',
        gap: '0',
        borderBottom: '2px solid #e2e8f0',
        marginBottom: '1.5rem',
      }}>
        {settingsTabs.map((tab) => (
          <Link
            key={tab.href}
            href={tab.href}
            style={{
              padding: '0.75rem 1.5rem',
              textDecoration: 'none',
              color: '#4a5568',
              borderBottom: '2px solid transparent',
              marginBottom: '-2px',
              transition: 'all 0.2s',
            }}
          >
            {tab.label}
          </Link>
        ))}
      </div>

      {// タブのコンテンツ }
      {children}
    </div>
  )
}
*/

// ============================================================
// 各ページの例（簡易版）
// ============================================================

/*
// app/(marketing)/page.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'ホーム',
  description: 'SaaS アプリケーションのランディングページ',
}

export default function HomePage() {
  return (
    <div style={{ padding: '4rem 2rem', textAlign: 'center' }}>
      <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>
        ビジネスを次のレベルへ
      </h1>
      <p style={{ fontSize: '1.2rem', color: '#666', maxWidth: '600px', margin: '0 auto' }}>
        My SaaS App は、チームの生産性を最大化するためのツールです。
      </p>
    </div>
  )
}

// app/(auth)/login/page.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'ログイン',
}

export default function LoginPage() {
  return (
    <div>
      <h1 style={{ textAlign: 'center', marginBottom: '1.5rem' }}>ログイン</h1>
      <form>
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: 'block', marginBottom: '0.25rem' }}>メールアドレス</label>
          <input type="email" style={{ width: '100%', padding: '0.5rem', boxSizing: 'border-box', borderRadius: '6px', border: '1px solid #e2e8f0' }} />
        </div>
        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{ display: 'block', marginBottom: '0.25rem' }}>パスワード</label>
          <input type="password" style={{ width: '100%', padding: '0.5rem', boxSizing: 'border-box', borderRadius: '6px', border: '1px solid #e2e8f0' }} />
        </div>
        <button style={{ width: '100%', padding: '0.75rem', backgroundColor: '#0070f3', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}>
          ログイン
        </button>
      </form>
    </div>
  )
}

// app/(dashboard)/dashboard/page.tsx
export default function DashboardPage() {
  return (
    <div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem' }}>
        <div style={{ padding: '1.5rem', backgroundColor: '#fff', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <p style={{ color: '#a0aec0', margin: '0 0 0.25rem' }}>総ユーザー数</p>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', margin: 0 }}>1,234</p>
        </div>
        <div style={{ padding: '1.5rem', backgroundColor: '#fff', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <p style={{ color: '#a0aec0', margin: '0 0 0.25rem' }}>月間売上</p>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', margin: 0 }}>¥567,890</p>
        </div>
        <div style={{ padding: '1.5rem', backgroundColor: '#fff', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <p style={{ color: '#a0aec0', margin: '0 0 0.25rem' }}>アクティブ率</p>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', margin: 0 }}>87.5%</p>
        </div>
      </div>
    </div>
  )
}
*/

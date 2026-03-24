/**
 * ============================================================
 * サンプル03: データフェッチング（fetch、キャッシュ、再検証）
 * ============================================================
 *
 * 【学べる内容】
 *   - サーバーコンポーネントでの async/await データ取得
 *   - fetch のキャッシュオプション（force-cache, no-store, revalidate）
 *   - Promise.all による並列データ取得
 *   - Suspense を使ったストリーミング SSR
 *   - エラーハンドリングと notFound()
 *   - ISR（Incremental Static Regeneration）の設定
 *
 * 【前提条件】
 *   - npx create-next-app@latest my-app でプロジェクト作成済み
 *   - App Router + TypeScript を選択済み
 *
 * 【ファイルの配置場所】
 *   各セクションを以下のパスに分割して配置してください:
 *
 *   1. app/users/page.tsx          — ユーザー一覧（基本の fetch）
 *   2. app/dashboard/page.tsx      — Suspense + ストリーミング
 *   3. app/posts/[id]/page.tsx     — 動的ルート + エラーハンドリング
 *   4. app/blog/page.tsx           — ISR 設定付きページ
 *
 * 【実行方法】
 *   cd my-app
 *   npm run dev
 *   以下の URL にアクセス:
 *     http://localhost:3000/users
 *     http://localhost:3000/dashboard
 *     http://localhost:3000/posts/1
 *     http://localhost:3000/blog
 *
 * ============================================================
 */

// ============================================================
// 1. app/users/page.tsx — 基本的なデータフェッチング
// ============================================================
// サーバーコンポーネントでは async/await で直接データを取得できます。
// useEffect や useState は不要です。

// 型定義
type User = {
  id: number
  name: string
  email: string
  company: {
    name: string
  }
}

export default async function UsersPage() {
  // サーバー上でデータを取得（クライアントには HTML が送信される）
  const res = await fetch('https://jsonplaceholder.typicode.com/users', {
    // キャッシュオプション:
    // cache: 'force-cache'  → 静的生成（デフォルト）
    // cache: 'no-store'     → 毎回取得（SSR）
    // next: { revalidate: 3600 } → ISR（1時間ごとに再検証）
    next: { revalidate: 3600 },
  })

  if (!res.ok) {
    throw new Error('ユーザーデータの取得に失敗しました')
  }

  const users: User[] = await res.json()

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>ユーザー一覧</h1>
      <p style={{ color: '#666' }}>
        このデータはサーバーで取得され、HTML に含まれた状態でクライアントに送信されます。
        ページのソースを表示すると、ユーザー情報が HTML に含まれていることが確認できます。
      </p>

      <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))' }}>
        {users.map((user) => (
          <div
            key={user.id}
            style={{
              border: '1px solid #e2e8f0',
              borderRadius: '8px',
              padding: '1.25rem',
            }}
          >
            <h3 style={{ margin: '0 0 0.5rem' }}>{user.name}</h3>
            <p style={{ margin: '0 0 0.25rem', color: '#4a5568' }}>{user.email}</p>
            <p style={{ margin: 0, color: '#a0aec0', fontSize: '0.85rem' }}>
              {user.company.name}
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}

// ============================================================
// 2. app/dashboard/page.tsx — Suspense + 並列データ取得
// ============================================================
// Suspense を使うと、各セクションが独立してストリーミングされます。
// データ取得が完了した順にコンテンツが表示されます。

/*
import { Suspense } from 'react'

export default function DashboardPage() {
  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>ダッシュボード</h1>
      <p style={{ color: '#666' }}>
        各セクションが独立して読み込まれます（Suspense + ストリーミング SSR）
      </p>

      <div style={{ display: 'grid', gap: '1.5rem' }}>
        {// 各セクションに Suspense を設定 → 個別にストリーミング }
        <Suspense fallback={<LoadingCard title="ユーザー統計" />}>
          <UserStats />
        </Suspense>

        <Suspense fallback={<LoadingCard title="最近の投稿" />}>
          <RecentPosts />
        </Suspense>

        <Suspense fallback={<LoadingCard title="TODO サマリー" />}>
          <TodoSummary />
        </Suspense>
      </div>
    </div>
  )
}

// ローディングカードコンポーネント
function LoadingCard({ title }: { title: string }) {
  return (
    <div style={{
      border: '1px solid #e2e8f0',
      borderRadius: '8px',
      padding: '1.5rem',
      backgroundColor: '#f7fafc',
    }}>
      <h2 style={{ margin: '0 0 0.5rem' }}>{title}</h2>
      <p style={{ color: '#a0aec0' }}>読み込み中...</p>
    </div>
  )
}

// 非同期サーバーコンポーネント: ユーザー統計
async function UserStats() {
  const res = await fetch('https://jsonplaceholder.typicode.com/users', {
    cache: 'no-store', // 毎回最新データを取得
  })
  const users = await res.json()

  return (
    <div style={{
      border: '1px solid #e2e8f0',
      borderRadius: '8px',
      padding: '1.5rem',
    }}>
      <h2 style={{ margin: '0 0 1rem' }}>ユーザー統計</h2>
      <p style={{ fontSize: '2rem', fontWeight: 'bold', margin: 0 }}>
        {users.length} <span style={{ fontSize: '1rem', color: '#666' }}>人</span>
      </p>
    </div>
  )
}

// 非同期サーバーコンポーネント: 最近の投稿
async function RecentPosts() {
  const res = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5', {
    cache: 'no-store',
  })
  const posts = await res.json()

  return (
    <div style={{
      border: '1px solid #e2e8f0',
      borderRadius: '8px',
      padding: '1.5rem',
    }}>
      <h2 style={{ margin: '0 0 1rem' }}>最近の投稿</h2>
      <ul style={{ margin: 0, paddingLeft: '1.25rem' }}>
        {posts.map((post: any) => (
          <li key={post.id} style={{ marginBottom: '0.5rem' }}>
            {post.title}
          </li>
        ))}
      </ul>
    </div>
  )
}

// 非同期サーバーコンポーネント: TODO サマリー
async function TodoSummary() {
  const res = await fetch('https://jsonplaceholder.typicode.com/todos', {
    cache: 'no-store',
  })
  const todos = await res.json()
  const completed = todos.filter((t: any) => t.completed).length
  const total = todos.length

  return (
    <div style={{
      border: '1px solid #e2e8f0',
      borderRadius: '8px',
      padding: '1.5rem',
    }}>
      <h2 style={{ margin: '0 0 1rem' }}>TODO サマリー</h2>
      <div style={{ display: 'flex', gap: '2rem' }}>
        <div>
          <p style={{ color: '#666', margin: '0 0 0.25rem' }}>総数</p>
          <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: 0 }}>{total}</p>
        </div>
        <div>
          <p style={{ color: '#666', margin: '0 0 0.25rem' }}>完了</p>
          <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: 0, color: '#38a169' }}>
            {completed}
          </p>
        </div>
        <div>
          <p style={{ color: '#666', margin: '0 0 0.25rem' }}>完了率</p>
          <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: 0 }}>
            {Math.round((completed / total) * 100)}%
          </p>
        </div>
      </div>
    </div>
  )
}
*/

// ============================================================
// 3. app/posts/[id]/page.tsx — エラーハンドリング + notFound
// ============================================================

/*
import { notFound } from 'next/navigation'
import type { Metadata } from 'next'

type Post = {
  id: number
  title: string
  body: string
  userId: number
}

type PostPageProps = {
  params: Promise<{ id: string }>
}

// 動的メタデータ
export async function generateMetadata({ params }: PostPageProps): Promise<Metadata> {
  const { id } = await params
  const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${id}`)

  if (!res.ok) return { title: '記事が見つかりません' }

  const post: Post = await res.json()
  return {
    title: post.title,
    description: post.body.slice(0, 160),
  }
}

export default async function PostPage({ params }: PostPageProps) {
  const { id } = await params

  // データの取得
  const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${id}`)

  // 404 の場合
  if (res.status === 404) {
    notFound() // not-found.tsx を表示
  }

  // その他の HTTP エラー
  if (!res.ok) {
    throw new Error(`データの取得に失敗しました（ステータス: ${res.status}）`)
  }

  const post: Post = await res.json()

  // ユーザー情報も並列で取得
  const userRes = await fetch(`https://jsonplaceholder.typicode.com/users/${post.userId}`)
  const user = await userRes.json()

  return (
    <article style={{ padding: '2rem', maxWidth: '700px', margin: '0 auto' }}>
      <p style={{ color: '#a0aec0', marginBottom: '0.25rem' }}>
        投稿者: {user.name}
      </p>
      <h1 style={{ marginBottom: '1.5rem' }}>{post.title}</h1>
      <p style={{ lineHeight: 1.8, color: '#4a5568' }}>{post.body}</p>

      <div style={{
        marginTop: '2rem',
        padding: '1rem',
        backgroundColor: '#f7fafc',
        borderRadius: '8px',
        fontSize: '0.85rem',
        color: '#666',
      }}>
        <p>このページの動的パラメータ: id = {id}</p>
        <p>エラーハンドリング: 存在しない ID（例: /posts/999）にアクセスすると 404 が表示されます</p>
      </div>
    </article>
  )
}
*/

// ============================================================
// 4. app/blog/page.tsx — ISR（Incremental Static Regeneration）
// ============================================================

/*
// ルートセグメント設定: 60秒ごとに再検証
export const revalidate = 60

type BlogPost = {
  id: number
  title: string
  body: string
}

export default async function BlogPage() {
  const res = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=10', {
    // fetch レベルでもリバリデーション間隔を指定可能
    next: {
      revalidate: 60,
      tags: ['blog-posts'], // タグベースの再検証用
    },
  })
  const posts: BlogPost[] = await res.json()

  // ISR の動作確認用: ページの生成日時を表示
  const generatedAt = new Date().toLocaleString('ja-JP', {
    timeZone: 'Asia/Tokyo',
  })

  return (
    <div style={{ padding: '2rem', maxWidth: '700px', margin: '0 auto' }}>
      <h1>ブログ（ISR デモ）</h1>

      <div style={{
        padding: '1rem',
        backgroundColor: '#ebf8ff',
        borderRadius: '8px',
        marginBottom: '1.5rem',
        fontSize: '0.9rem',
      }}>
        <p style={{ margin: '0 0 0.25rem' }}>
          <strong>ページ生成日時:</strong> {generatedAt}
        </p>
        <p style={{ margin: 0, color: '#666' }}>
          60秒間はキャッシュが返されます。60秒後のアクセスでバックグラウンド再生成が開始されます。
        </p>
      </div>

      <ul style={{ listStyle: 'none', padding: 0 }}>
        {posts.map((post) => (
          <li key={post.id} style={{
            padding: '1rem 0',
            borderBottom: '1px solid #e2e8f0',
          }}>
            <h3 style={{ margin: '0 0 0.5rem' }}>{post.title}</h3>
            <p style={{ margin: 0, color: '#666', lineHeight: 1.6 }}>
              {post.body.slice(0, 100)}...
            </p>
          </li>
        ))}
      </ul>
    </div>
  )
}
*/

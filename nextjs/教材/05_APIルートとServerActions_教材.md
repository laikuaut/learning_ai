# 第5章: API ルートと Server Actions

## この章のゴール

- Route Handlers（API ルート）の作成方法と RESTful API の設計パターンを習得する
- Server Actions の仕組みを理解し、フォーム送信やデータ変更を安全に実装できるようになる
- Route Handlers と Server Actions の使い分けを明確にする
- バリデーション、エラーハンドリング、楽観的更新（Optimistic Updates）の実践的なパターンを学ぶ

---

## 5.1 なぜ API ルートと Server Actions が必要なのか

### 従来のフルスタック開発

従来の React アプリケーションでは、フロントエンドとバックエンドは別々のプロジェクトとして開発されることが一般的でした。

```
従来の構成:
┌──────────────┐    HTTP     ┌──────────────┐
│  React SPA   │ ────────→  │  Express.js  │ → DB
│ (フロントエンド) │ ←──────── │  (バックエンド)  │
└──────────────┘            └──────────────┘
```

この構成には以下の課題がありました。

- フロントエンドとバックエンドのリポジトリが分離し、開発・デプロイが複雑化する
- CORS（Cross-Origin Resource Sharing）の設定が必要
- API 仕様の同期が難しい（型の不整合が起きやすい）

### Next.js の統合アプローチ

Next.js では、フロントエンドとバックエンドを **同一プロジェクト** 内で開発できます。

```
Next.js の構成:
┌───────────────────────────────────┐
│            Next.js                │
│  ┌───────────┐  ┌──────────────┐ │
│  │ フロントエンド │  │ Route Handlers│ │ → DB
│  │ (React)    │  │ Server Actions│ │
│  └───────────┘  └──────────────┘ │
└───────────────────────────────────┘
```

---

## 5.2 Route Handlers — API エンドポイントの作成

### 基本構造

Route Handlers は `app` ディレクトリ内の `route.ts`（または `route.js`）ファイルで定義します。

```
app/
├── api/
│   ├── posts/
│   │   ├── route.ts          → GET /api/posts, POST /api/posts
│   │   └── [id]/
│   │       └── route.ts      → GET /api/posts/:id, PUT, DELETE
│   └── users/
│       └── route.ts          → GET /api/users
```

> **重要**: `route.ts` と `page.tsx` は**同じディレクトリに共存できません**。API エンドポイントには `api/` ディレクトリを使うのが慣例です。

### GET リクエスト

```tsx
// app/api/posts/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // データベースからデータを取得
    const posts = await prisma.post.findMany({
      orderBy: { createdAt: 'desc' },
    })

    return NextResponse.json(posts)
  } catch (error) {
    return NextResponse.json(
      { error: 'データの取得に失敗しました' },
      { status: 500 }
    )
  }
}
```

### POST リクエスト

```tsx
// app/api/posts/route.ts（同じファイルに追加）
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    // バリデーション
    if (!body.title || !body.content) {
      return NextResponse.json(
        { error: 'タイトルと本文は必須です' },
        { status: 400 }
      )
    }

    // データベースに保存
    const post = await prisma.post.create({
      data: {
        title: body.title,
        content: body.content,
      },
    })

    return NextResponse.json(post, { status: 201 })
  } catch (error) {
    return NextResponse.json(
      { error: '記事の作成に失敗しました' },
      { status: 500 }
    )
  }
}
```

### 動的ルートの Route Handler

```tsx
// app/api/posts/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'

// GET /api/posts/:id — 個別記事の取得
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params

  const post = await prisma.post.findUnique({
    where: { id },
  })

  if (!post) {
    return NextResponse.json(
      { error: '記事が見つかりません' },
      { status: 404 }
    )
  }

  return NextResponse.json(post)
}

// PUT /api/posts/:id — 記事の更新
export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const body = await request.json()

  try {
    const post = await prisma.post.update({
      where: { id },
      data: {
        title: body.title,
        content: body.content,
      },
    })

    return NextResponse.json(post)
  } catch (error) {
    return NextResponse.json(
      { error: '記事の更新に失敗しました' },
      { status: 500 }
    )
  }
}

// DELETE /api/posts/:id — 記事の削除
export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params

  try {
    await prisma.post.delete({
      where: { id },
    })

    return NextResponse.json({ message: '削除しました' })
  } catch (error) {
    return NextResponse.json(
      { error: '記事の削除に失敗しました' },
      { status: 500 }
    )
  }
}
```

### サポートされる HTTP メソッド

| メソッド | 用途 | エクスポート名 |
|---------|------|-------------|
| `GET` | データの取得 | `GET` |
| `POST` | データの作成 | `POST` |
| `PUT` | データの全体更新 | `PUT` |
| `PATCH` | データの部分更新 | `PATCH` |
| `DELETE` | データの削除 | `DELETE` |
| `HEAD` | ヘッダーのみ取得 | `HEAD` |
| `OPTIONS` | CORS プリフライト | `OPTIONS` |

---

## 5.3 Route Handlers の高度な機能

### リクエスト情報の取得

```tsx
// app/api/search/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  // クエリパラメータの取得
  const searchParams = request.nextUrl.searchParams
  const query = searchParams.get('q')       // ?q=nextjs
  const page = searchParams.get('page')      // ?page=2
  const limit = searchParams.get('limit')    // ?limit=10

  // ヘッダーの取得
  const authHeader = request.headers.get('Authorization')
  const contentType = request.headers.get('Content-Type')

  // Cookie の取得
  const sessionToken = request.cookies.get('session')

  return NextResponse.json({
    query,
    page: Number(page) || 1,
    limit: Number(limit) || 10,
  })
}
```

### レスポンスのカスタマイズ

```tsx
// カスタムヘッダーの設定
export async function GET() {
  const data = { message: 'Hello' }

  return NextResponse.json(data, {
    status: 200,
    headers: {
      'Cache-Control': 'public, max-age=3600',
      'X-Custom-Header': 'custom-value',
    },
  })
}

// リダイレクト
import { redirect } from 'next/navigation'

export async function GET() {
  redirect('/new-url')
}

// ストリーミングレスポンス
export async function GET() {
  const encoder = new TextEncoder()
  const stream = new ReadableStream({
    async start(controller) {
      for (let i = 0; i < 5; i++) {
        controller.enqueue(encoder.encode(`データ ${i}\n`))
        await new Promise(resolve => setTimeout(resolve, 1000))
      }
      controller.close()
    },
  })

  return new Response(stream, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  })
}
```

### CORS の設定

```tsx
// app/api/public/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const data = { message: '公開 API' }

  return NextResponse.json(data, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  })
}

export async function OPTIONS() {
  return NextResponse.json({}, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  })
}
```

### Route Handler のキャッシュ

```tsx
// GET メソッドは静的にキャッシュされる（デフォルト）
export async function GET() {
  const data = await fetch('https://api.example.com/data')
  return NextResponse.json(await data.json())
}

// 動的にしたい場合
export const dynamic = 'force-dynamic'

// または動的関数を使用
export async function GET(request: NextRequest) {
  const token = request.cookies.get('session') // cookies → 動的
  // ...
}
```

---

## 5.4 Server Actions — サーバー側の関数呼び出し

### Server Actions とは

Server Actions は、**クライアントから直接呼び出せるサーバー上の関数**です。`'use server'` ディレクティブで宣言し、フォーム送信やデータ変更に使用します。

従来の API ルート経由のデータ変更と比較すると、はるかにシンプルに実装できます。

```
従来のアプローチ:
クライアント → fetch('/api/posts', { method: 'POST' }) → Route Handler → DB

Server Actions:
クライアント → createPost() → サーバーで実行 → DB
```

### 基本的な Server Action

```tsx
// app/actions/posts.ts
'use server' // ファイル全体を Server Actions として宣言

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  // フォームデータの取得
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  // バリデーション
  if (!title || !content) {
    return { error: 'タイトルと本文は必須です' }
  }

  // データベースに保存
  await prisma.post.create({
    data: { title, content },
  })

  // キャッシュの再検証
  revalidatePath('/blog')

  // リダイレクト
  redirect('/blog')
}
```

### フォームでの使用

```tsx
// app/blog/new/page.tsx — サーバーコンポーネント
import { createPost } from '@/app/actions/posts'

export default function NewPostPage() {
  return (
    <div>
      <h1>新しい記事を書く</h1>

      {/* action 属性に Server Action を渡す */}
      <form action={createPost}>
        <div>
          <label htmlFor="title">タイトル</label>
          <input
            type="text"
            id="title"
            name="title"
            required
          />
        </div>
        <div>
          <label htmlFor="content">本文</label>
          <textarea
            id="content"
            name="content"
            rows={10}
            required
          />
        </div>
        <button type="submit">投稿する</button>
      </form>
    </div>
  )
}
```

> **ポイント**: Server Actions を `<form>` の `action` 属性に渡すと、フォーム送信時にサーバー上で直接実行されます。JavaScript が無効な環境でも動作するプログレッシブエンハンスメントが実現します。

### インラインの Server Action

ファイルを分けずに、コンポーネント内で直接定義することもできます。

```tsx
// app/feedback/page.tsx
export default function FeedbackPage() {
  async function submitFeedback(formData: FormData) {
    'use server' // 関数内で宣言

    const message = formData.get('message') as string
    await saveFeedback(message)
  }

  return (
    <form action={submitFeedback}>
      <textarea name="message" placeholder="ご意見をお聞かせください" />
      <button type="submit">送信</button>
    </form>
  )
}
```

---

## 5.5 Server Actions の高度なパターン

### useFormStatus — 送信状態の表示

```tsx
// app/components/SubmitButton.tsx
'use client'

import { useFormStatus } from 'react-dom'

export default function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button type="submit" disabled={pending}>
      {pending ? '送信中...' : '送信する'}
    </button>
  )
}
```

```tsx
// app/blog/new/page.tsx
import { createPost } from '@/app/actions/posts'
import SubmitButton from '@/app/components/SubmitButton'

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input type="text" name="title" />
      <textarea name="content" />
      <SubmitButton />
    </form>
  )
}
```

> **注意**: `useFormStatus` は `<form>` の**子コンポーネント**内でしか使えません。フォームと同じコンポーネントでは動作しないため、必ずボタンを別コンポーネントに分離してください。

### useActionState — アクションの状態管理

```tsx
// app/actions/posts.ts
'use server'

type State = {
  error?: string
  success?: boolean
}

export async function createPost(
  prevState: State,
  formData: FormData
): Promise<State> {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  if (!title) {
    return { error: 'タイトルは必須です' }
  }

  if (title.length < 3) {
    return { error: 'タイトルは3文字以上にしてください' }
  }

  try {
    await prisma.post.create({
      data: { title, content },
    })
    revalidatePath('/blog')
    return { success: true }
  } catch (e) {
    return { error: '記事の作成に失敗しました' }
  }
}
```

```tsx
// app/blog/new/page.tsx
'use client'

import { useActionState } from 'react'
import { createPost } from '@/app/actions/posts'
import SubmitButton from '@/app/components/SubmitButton'

export default function NewPostPage() {
  const [state, formAction] = useActionState(createPost, {})

  return (
    <form action={formAction}>
      {state.error && (
        <div style={{ color: 'red' }}>{state.error}</div>
      )}
      {state.success && (
        <div style={{ color: 'green' }}>記事を投稿しました！</div>
      )}

      <input type="text" name="title" />
      <textarea name="content" />
      <SubmitButton />
    </form>
  )
}
```

### useOptimistic — 楽観的更新

楽観的更新は、サーバーの応答を待たずに UI を先に更新するパターンです。ユーザーに即座のフィードバックを与えられます。

```tsx
// app/components/LikeButton.tsx
'use client'

import { useOptimistic } from 'react'
import { toggleLike } from '@/app/actions/likes'

type Props = {
  postId: string
  liked: boolean
  likeCount: number
}

export default function LikeButton({ postId, liked, likeCount }: Props) {
  const [optimisticState, addOptimistic] = useOptimistic(
    { liked, likeCount },
    (current, newLiked: boolean) => ({
      liked: newLiked,
      likeCount: newLiked ? current.likeCount + 1 : current.likeCount - 1,
    })
  )

  async function handleLike() {
    addOptimistic(!optimisticState.liked) // 即座にUIを更新
    await toggleLike(postId)              // サーバーで実際に処理
  }

  return (
    <form action={handleLike}>
      <button type="submit">
        {optimisticState.liked ? '❤️' : '🤍'} {optimisticState.likeCount}
      </button>
    </form>
  )
}
```

### イベントハンドラからの呼び出し

Server Actions はフォームだけでなく、イベントハンドラからも呼び出せます。

```tsx
// app/components/DeleteButton.tsx
'use client'

import { deletePost } from '@/app/actions/posts'
import { useTransition } from 'react'

export default function DeleteButton({ postId }: { postId: string }) {
  const [isPending, startTransition] = useTransition()

  function handleDelete() {
    if (!confirm('本当に削除しますか？')) return

    startTransition(async () => {
      await deletePost(postId)
    })
  }

  return (
    <button onClick={handleDelete} disabled={isPending}>
      {isPending ? '削除中...' : '削除'}
    </button>
  )
}
```

---

## 5.6 バリデーション

### Zod を使ったサーバーサイドバリデーション

```tsx
// lib/validations/post.ts
import { z } from 'zod'

export const createPostSchema = z.object({
  title: z
    .string()
    .min(1, 'タイトルは必須です')
    .max(100, 'タイトルは100文字以内にしてください'),
  content: z
    .string()
    .min(10, '本文は10文字以上で入力してください')
    .max(10000, '本文は10000文字以内にしてください'),
  category: z.enum(['tech', 'life', 'news'], {
    errorMap: () => ({ message: '有効なカテゴリを選択してください' }),
  }),
})

export type CreatePostInput = z.infer<typeof createPostSchema>
```

```tsx
// app/actions/posts.ts
'use server'

import { createPostSchema } from '@/lib/validations/post'
import { revalidatePath } from 'next/cache'

type State = {
  errors?: {
    title?: string[]
    content?: string[]
    category?: string[]
  }
  message?: string
}

export async function createPost(
  prevState: State,
  formData: FormData
): Promise<State> {
  // Zod でバリデーション
  const validatedFields = createPostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
    category: formData.get('category'),
  })

  // バリデーションエラー
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
      message: '入力内容に問題があります',
    }
  }

  // データベースに保存
  try {
    await prisma.post.create({
      data: validatedFields.data,
    })
  } catch (e) {
    return { message: 'データベースエラーが発生しました' }
  }

  revalidatePath('/blog')
  redirect('/blog')
}
```

```tsx
// app/blog/new/page.tsx
'use client'

import { useActionState } from 'react'
import { createPost } from '@/app/actions/posts'

export default function NewPostForm() {
  const [state, formAction] = useActionState(createPost, {})

  return (
    <form action={formAction}>
      <div>
        <label htmlFor="title">タイトル</label>
        <input type="text" id="title" name="title" />
        {state.errors?.title && (
          <p style={{ color: 'red' }}>{state.errors.title[0]}</p>
        )}
      </div>

      <div>
        <label htmlFor="content">本文</label>
        <textarea id="content" name="content" />
        {state.errors?.content && (
          <p style={{ color: 'red' }}>{state.errors.content[0]}</p>
        )}
      </div>

      <div>
        <label htmlFor="category">カテゴリ</label>
        <select id="category" name="category">
          <option value="">選択してください</option>
          <option value="tech">技術</option>
          <option value="life">生活</option>
          <option value="news">ニュース</option>
        </select>
        {state.errors?.category && (
          <p style={{ color: 'red' }}>{state.errors.category[0]}</p>
        )}
      </div>

      {state.message && (
        <p style={{ color: 'red' }}>{state.message}</p>
      )}

      <button type="submit">投稿する</button>
    </form>
  )
}
```

---

## 5.7 Route Handlers vs Server Actions — 使い分けガイド

| 観点 | Route Handlers | Server Actions |
|------|---------------|----------------|
| 主な用途 | 外部向け API、Webhook | フォーム送信、データ変更 |
| HTTP メソッド | GET, POST, PUT, DELETE 等 | POST のみ（内部的に） |
| 呼び出し元 | 外部クライアント、モバイルアプリ | Next.js のフロントエンド |
| プログレッシブエンハンスメント | なし | あり（JS なしでも動作） |
| キャッシュ再検証 | 手動で実装 | `revalidatePath/Tag` が統合 |
| 型安全性 | リクエスト/レスポンスの型定義が必要 | 引数と戻り値で直接型付け |
| テスト | HTTP クライアントでテスト | 関数として直接テスト |

### 判断フロー

```
データの変更が必要？
  → NO → サーバーコンポーネントで直接 fetch
  → YES
    ↓
外部から呼ばれる API？（モバイルアプリ、Webhook、他サービス）
  → YES → Route Handlers
  → NO
    ↓
Next.js のフロントエンドからのデータ変更？
  → YES → Server Actions
```

---

## 5.8 ファイルアップロード

### Server Actions でのファイルアップロード

```tsx
// app/actions/upload.ts
'use server'

import { writeFile } from 'fs/promises'
import path from 'path'

export async function uploadFile(formData: FormData) {
  const file = formData.get('file') as File

  if (!file) {
    return { error: 'ファイルが選択されていません' }
  }

  // ファイルサイズチェック（5MB以下）
  if (file.size > 5 * 1024 * 1024) {
    return { error: 'ファイルサイズは5MB以下にしてください' }
  }

  // 許可する MIME タイプ
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    return { error: 'JPEG、PNG、WebP のみアップロードできます' }
  }

  const bytes = await file.arrayBuffer()
  const buffer = Buffer.from(bytes)

  // ファイル名にタイムスタンプを付加
  const filename = `${Date.now()}-${file.name}`
  const filepath = path.join(process.cwd(), 'public', 'uploads', filename)

  await writeFile(filepath, buffer)

  return { success: true, url: `/uploads/${filename}` }
}
```

```tsx
// app/upload/page.tsx
import { uploadFile } from '@/app/actions/upload'

export default function UploadPage() {
  return (
    <form action={uploadFile}>
      <input type="file" name="file" accept="image/*" />
      <button type="submit">アップロード</button>
    </form>
  )
}
```

### Route Handlers でのファイルアップロード

```tsx
// app/api/upload/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { writeFile } from 'fs/promises'
import path from 'path'

export async function POST(request: NextRequest) {
  const formData = await request.formData()
  const file = formData.get('file') as File

  if (!file) {
    return NextResponse.json(
      { error: 'ファイルが見つかりません' },
      { status: 400 }
    )
  }

  const bytes = await file.arrayBuffer()
  const buffer = Buffer.from(bytes)
  const filename = `${Date.now()}-${file.name}`
  const filepath = path.join(process.cwd(), 'public', 'uploads', filename)

  await writeFile(filepath, buffer)

  return NextResponse.json({
    url: `/uploads/${filename}`,
  })
}
```

---

## 5.9 よくある間違い

### 間違い1: Server Actions で機密データを引数に含める

```tsx
// 悪い例: クライアントから userId を受け取る
'use server'
export async function deletePost(userId: string, postId: string) {
  // userId はクライアントが改ざんできる！
  await prisma.post.delete({
    where: { id: postId, authorId: userId },
  })
}

// 良い例: サーバーでセッションから userId を取得する
'use server'
import { auth } from '@/lib/auth'

export async function deletePost(postId: string) {
  const session = await auth()
  if (!session?.user?.id) {
    throw new Error('認証が必要です')
  }

  await prisma.post.delete({
    where: { id: postId, authorId: session.user.id },
  })
}
```

### 間違い2: Server Actions でリダイレクトを try-catch で囲む

```tsx
// 悪い例: redirect は内部的にエラーをスローするため catch される
'use server'
export async function createPost(formData: FormData) {
  try {
    await prisma.post.create({ data: { /* ... */ } })
    redirect('/blog') // ← これが catch で捕まってしまう！
  } catch (error) {
    return { error: '失敗しました' }
  }
}

// 良い例: redirect を try-catch の外に置く
'use server'
export async function createPost(formData: FormData) {
  try {
    await prisma.post.create({ data: { /* ... */ } })
  } catch (error) {
    return { error: '失敗しました' }
  }

  revalidatePath('/blog')
  redirect('/blog') // try-catch の外
}
```

### 間違い3: useFormStatus をフォームと同じコンポーネントで使う

```tsx
// 悪い例: useFormStatus が動作しない
'use client'
import { useFormStatus } from 'react-dom'

export default function Form() {
  const { pending } = useFormStatus() // ← 動作しない！

  return (
    <form action={someAction}>
      <button disabled={pending}>送信</button>
    </form>
  )
}

// 良い例: ボタンを子コンポーネントに分離
function SubmitButton() {
  const { pending } = useFormStatus() // ← form の子なので動作する
  return <button disabled={pending}>{pending ? '送信中...' : '送信'}</button>
}

export default function Form() {
  return (
    <form action={someAction}>
      <SubmitButton />
    </form>
  )
}
```

---

## 5.10 現場でのベストプラクティス

### 1. Server Actions のファイル構成

```
app/
├── actions/
│   ├── posts.ts      ← 記事関連のアクション
│   ├── users.ts      ← ユーザー関連のアクション
│   ├── auth.ts       ← 認証関連のアクション
│   └── upload.ts     ← アップロード関連のアクション
├── api/
│   ├── webhook/
│   │   └── route.ts  ← 外部からの Webhook
│   └── v1/
│       └── posts/
│           └── route.ts ← 外部向け API
```

### 2. エラーハンドリングの統一

```tsx
// lib/action-utils.ts
type ActionResult<T = void> =
  | { success: true; data: T }
  | { success: false; error: string }

export function actionSuccess<T>(data: T): ActionResult<T> {
  return { success: true, data }
}

export function actionError(error: string): ActionResult<never> {
  return { success: false, error }
}
```

### 3. 認証チェックの共通化

```tsx
// lib/auth-action.ts
'use server'

import { auth } from '@/lib/auth'

export async function authenticatedAction<T>(
  action: (userId: string) => Promise<T>
): Promise<T> {
  const session = await auth()
  if (!session?.user?.id) {
    throw new Error('認証が必要です')
  }
  return action(session.user.id)
}

// 使用例
export async function createPost(formData: FormData) {
  return authenticatedAction(async (userId) => {
    await prisma.post.create({
      data: {
        title: formData.get('title') as string,
        authorId: userId,
      },
    })
    revalidatePath('/blog')
  })
}
```

---

## 5.11 ポイントまとめ

本章で学んだこと:

1. **Route Handlers** は `route.ts` で定義し、RESTful API を構築できます
2. **Server Actions** は `'use server'` で宣言し、フォーム送信やデータ変更に最適です
3. `useFormStatus` で送信中の状態を、`useActionState` でアクションの結果を管理できます
4. `useOptimistic` で**楽観的更新**を実現し、体感速度を向上させられます
5. **Zod** などのライブラリでサーバーサイドバリデーションを実装すべきです
6. Server Actions では**セッションから認証情報を取得**し、クライアントからの入力を信頼しないことが重要です
7. 外部向け API には Route Handlers を、内部のデータ変更には Server Actions を使い分けましょう

### 次章の予告

第6章では、レイアウトの高度な活用とメタデータ API について学びます。SEO 対策や OGP の設定を含む、実務で必須の知識を習得しましょう。

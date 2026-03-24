# 第5章 演習：API ルートと Server Actions

---

## 演習1（基本）：GET API ルートを作成しよう

ダミーのユーザーデータを返す GET API エンドポイントを作成してください。

**要件：**
- `app/api/users/route.ts` を作成する
- JSON 形式でユーザーの配列を返す
- ステータスコード 200 を返す

<details>
<summary>ヒント</summary>

`route.ts` ファイルで `GET` 関数をエクスポートすると、GET リクエストに対するハンドラになります。`NextResponse.json()` でJSON レスポンスを返せます。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/api/users/route.ts
import { NextResponse } from 'next/server'

// ダミーデータ
const users = [
  { id: 1, name: '田中太郎', email: 'tanaka@example.com' },
  { id: 2, name: '鈴木花子', email: 'suzuki@example.com' },
  { id: 3, name: '佐藤一郎', email: 'sato@example.com' },
]

// GET /api/users
export async function GET() {
  return NextResponse.json(users)
}
```

ブラウザで `http://localhost:3000/api/users` にアクセスすると、JSON データが返されます。

</details>

---

## 演習2（基本）：POST API ルートを作成しよう

新しいユーザーを追加する POST API エンドポイントを作成してください。

**要件：**
- 同じ `app/api/users/route.ts` に POST ハンドラを追加する
- リクエストボディから `name` と `email` を取得する
- バリデーション: `name` と `email` が空の場合はエラーを返す
- 成功時はステータスコード 201 を返す

<details>
<summary>ヒント</summary>

`request.json()` でリクエストボディを JSON として取得できます。バリデーションに失敗した場合は `NextResponse.json()` の第2引数で `{ status: 400 }` を指定します。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'

const users = [
  { id: 1, name: '田中太郎', email: 'tanaka@example.com' },
  { id: 2, name: '鈴木花子', email: 'suzuki@example.com' },
  { id: 3, name: '佐藤一郎', email: 'sato@example.com' },
]

// GET /api/users
export async function GET() {
  return NextResponse.json(users)
}

// POST /api/users
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    // バリデーション
    if (!body.name || !body.email) {
      return NextResponse.json(
        { error: '名前とメールアドレスは必須です' },
        { status: 400 }
      )
    }

    // 新しいユーザーを作成（実際にはデータベースに保存する）
    const newUser = {
      id: users.length + 1,
      name: body.name,
      email: body.email,
    }

    return NextResponse.json(newUser, { status: 201 })
  } catch (error) {
    return NextResponse.json(
      { error: 'リクエストの処理に失敗しました' },
      { status: 500 }
    )
  }
}
```

ターミナルで以下のコマンドを実行して動作確認できます:
```bash
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"山田花子","email":"yamada@example.com"}'
```

</details>

---

## 演習3（基本）：Server Action で基本的なフォーム送信を実装しよう

Server Action を使って、お問い合わせフォームの送信処理を実装してください。

**要件：**
- `app/actions/contact.ts` に Server Action を定義する
- `'use server'` ディレクティブを使用する
- `<form>` の `action` 属性に Server Action を渡す

<details>
<summary>ヒント</summary>

Server Action は `'use server'` をファイルの先頭に記述することで宣言します。`<form action={serverAction}>` のように使い、`FormData` で入力値を取得します。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/actions/contact.ts
'use server'

export async function submitContact(formData: FormData) {
  const name = formData.get('name') as string
  const email = formData.get('email') as string
  const message = formData.get('message') as string

  // バリデーション
  if (!name || !email || !message) {
    return { error: 'すべての項目を入力してください' }
  }

  // 実際にはデータベースに保存やメール送信を行う
  console.log('お問い合わせ受信:', { name, email, message })

  return { success: true }
}
```

```tsx
// app/contact/page.tsx
import { submitContact } from '@/app/actions/contact'

export default function ContactPage() {
  return (
    <div style={{ padding: '2rem', maxWidth: '500px', margin: '0 auto' }}>
      <h1>お問い合わせ</h1>
      <form action={submitContact}>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="name" style={{ display: 'block', marginBottom: '0.25rem' }}>
            お名前
          </label>
          <input
            type="text"
            id="name"
            name="name"
            required
            style={{ width: '100%', padding: '0.5rem' }}
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
            required
            style={{ width: '100%', padding: '0.5rem' }}
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
            required
            style={{ width: '100%', padding: '0.5rem' }}
          />
        </div>
        <button
          type="submit"
          style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: '#0070f3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          送信する
        </button>
      </form>
    </div>
  )
}
```

Server Action は `<form>` の `action` 属性に直接渡せます。フォーム送信時にサーバー上で関数が実行されます。JavaScript が無効な環境でも動作するプログレッシブエンハンスメントが実現します。

</details>

---

## 演習4（応用）：useFormStatus で送信中の状態を表示しよう

フォーム送信中に「送信中...」と表示されるボタンを作成してください。

**要件：**
- `useFormStatus` を使って送信状態を取得する
- 送信中はボタンを無効化し、テキストを「送信中...」に変更する
- ボタンは別のクライアントコンポーネントに分離する

<details>
<summary>ヒント</summary>

`useFormStatus` は `react-dom` からインポートし、`<form>` の**子コンポーネント**内でのみ動作します。フォームと同じコンポーネントでは使えないため、ボタンを別コンポーネントに分離する必要があります。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/components/SubmitButton.tsx
'use client'

import { useFormStatus } from 'react-dom'

export default function SubmitButton() {
  // useFormStatus は <form> の子コンポーネント内でのみ動作する
  const { pending } = useFormStatus()

  return (
    <button
      type="submit"
      disabled={pending}
      style={{
        padding: '0.75rem 1.5rem',
        backgroundColor: pending ? '#ccc' : '#0070f3',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: pending ? 'default' : 'pointer',
      }}
    >
      {pending ? '送信中...' : '送信する'}
    </button>
  )
}
```

```tsx
// app/contact/page.tsx
import { submitContact } from '@/app/actions/contact'
import SubmitButton from '@/app/components/SubmitButton'

export default function ContactPage() {
  return (
    <div style={{ padding: '2rem', maxWidth: '500px', margin: '0 auto' }}>
      <h1>お問い合わせ</h1>
      <form action={submitContact}>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="name">お名前</label>
          <input type="text" id="name" name="name" required style={{ width: '100%', padding: '0.5rem' }} />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="email">メールアドレス</label>
          <input type="email" id="email" name="email" required style={{ width: '100%', padding: '0.5rem' }} />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="message">メッセージ</label>
          <textarea id="message" name="message" rows={5} required style={{ width: '100%', padding: '0.5rem' }} />
        </div>
        {/* SubmitButton は form の子なので useFormStatus が動作する */}
        <SubmitButton />
      </form>
    </div>
  )
}
```

**よくある間違い**: `useFormStatus` をフォームと同じコンポーネントで使おうとすると動作しません。必ずボタンを子コンポーネントに分離してください。

</details>

---

## 演習5（応用）：useActionState でバリデーションエラーを表示しよう

`useActionState` を使って、フォームのバリデーションエラーを画面に表示してください。

**要件：**
- Server Action でバリデーションを行い、エラーメッセージを返す
- `useActionState` でアクションの結果を状態として管理する
- エラー時はフィールドごとにエラーメッセージを表示する

<details>
<summary>ヒント</summary>

`useActionState` は第1引数に Server Action を、第2引数に初期状態を渡します。Server Action は第1引数に前回の状態（`prevState`）を受け取るように変更する必要があります。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/actions/register.ts
'use server'

type State = {
  errors?: {
    name?: string[]
    email?: string[]
    password?: string[]
  }
  message?: string
  success?: boolean
}

export async function registerUser(
  prevState: State,
  formData: FormData
): Promise<State> {
  const name = formData.get('name') as string
  const email = formData.get('email') as string
  const password = formData.get('password') as string

  const errors: State['errors'] = {}

  // バリデーション
  if (!name || name.length < 2) {
    errors.name = ['名前は2文字以上で入力してください']
  }
  if (!email || !email.includes('@')) {
    errors.email = ['有効なメールアドレスを入力してください']
  }
  if (!password || password.length < 8) {
    errors.password = ['パスワードは8文字以上で入力してください']
  }

  // エラーがある場合
  if (Object.keys(errors).length > 0) {
    return { errors, message: '入力内容に問題があります' }
  }

  // 登録処理（実際にはデータベースに保存）
  console.log('ユーザー登録:', { name, email })

  return { success: true, message: '登録が完了しました' }
}
```

```tsx
// app/register/page.tsx
'use client'

import { useActionState } from 'react'
import { registerUser } from '@/app/actions/register'
import SubmitButton from '@/app/components/SubmitButton'

export default function RegisterPage() {
  const [state, formAction] = useActionState(registerUser, {})

  return (
    <div style={{ padding: '2rem', maxWidth: '400px', margin: '0 auto' }}>
      <h1>ユーザー登録</h1>

      {state.success && (
        <div style={{ padding: '1rem', backgroundColor: '#c6f6d5', borderRadius: '4px', marginBottom: '1rem' }}>
          {state.message}
        </div>
      )}

      {state.message && !state.success && (
        <div style={{ padding: '1rem', backgroundColor: '#fed7d7', borderRadius: '4px', marginBottom: '1rem' }}>
          {state.message}
        </div>
      )}

      <form action={formAction}>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="name">名前</label>
          <input type="text" id="name" name="name" style={{ width: '100%', padding: '0.5rem' }} />
          {state.errors?.name && (
            <p style={{ color: 'red', fontSize: '0.85rem' }}>{state.errors.name[0]}</p>
          )}
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="email">メールアドレス</label>
          <input type="email" id="email" name="email" style={{ width: '100%', padding: '0.5rem' }} />
          {state.errors?.email && (
            <p style={{ color: 'red', fontSize: '0.85rem' }}>{state.errors.email[0]}</p>
          )}
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="password">パスワード</label>
          <input type="password" id="password" name="password" style={{ width: '100%', padding: '0.5rem' }} />
          {state.errors?.password && (
            <p style={{ color: 'red', fontSize: '0.85rem' }}>{state.errors.password[0]}</p>
          )}
        </div>
        <SubmitButton />
      </form>
    </div>
  )
}
```

`useActionState` を使うと、Server Action の戻り値をコンポーネントの状態として管理できます。Server Action の第1引数が `prevState` に変わる点に注意してください。

</details>

---

## 演習6（応用）：動的ルートの API エンドポイントを作成しよう

個別のリソースに対する CRUD 操作を行う API エンドポイントを作成してください。

**要件：**
- `app/api/posts/[id]/route.ts` を作成する
- GET（個別取得）、PUT（更新）、DELETE（削除）に対応する
- 存在しないリソースの場合は 404 を返す

<details>
<summary>ヒント</summary>

動的ルートの Route Handler では、第2引数で `params` を受け取ります。`params` は `Promise` として渡されるため `await` が必要です。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/api/posts/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'

// ダミーデータ
const posts = [
  { id: '1', title: 'Next.js 入門', content: 'Next.js の基本を学びます' },
  { id: '2', title: 'App Router', content: 'App Router の仕組みを理解します' },
  { id: '3', title: 'Server Components', content: 'RSC の活用方法を学びます' },
]

// GET /api/posts/:id — 個別取得
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const post = posts.find((p) => p.id === id)

  if (!post) {
    return NextResponse.json(
      { error: '記事が見つかりません' },
      { status: 404 }
    )
  }

  return NextResponse.json(post)
}

// PUT /api/posts/:id — 更新
export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const body = await request.json()
  const postIndex = posts.findIndex((p) => p.id === id)

  if (postIndex === -1) {
    return NextResponse.json(
      { error: '記事が見つかりません' },
      { status: 404 }
    )
  }

  // バリデーション
  if (!body.title || !body.content) {
    return NextResponse.json(
      { error: 'タイトルと本文は必須です' },
      { status: 400 }
    )
  }

  // 更新（実際にはデータベースを更新する）
  const updatedPost = { ...posts[postIndex], ...body }

  return NextResponse.json(updatedPost)
}

// DELETE /api/posts/:id — 削除
export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const postIndex = posts.findIndex((p) => p.id === id)

  if (postIndex === -1) {
    return NextResponse.json(
      { error: '記事が見つかりません' },
      { status: 404 }
    )
  }

  return NextResponse.json({ message: `記事 ${id} を削除しました` })
}
```

ターミナルで動作確認:
```bash
# 取得
curl http://localhost:3000/api/posts/1

# 更新
curl -X PUT http://localhost:3000/api/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"更新タイトル","content":"更新内容"}'

# 削除
curl -X DELETE http://localhost:3000/api/posts/1
```

</details>

---

## 演習7（チャレンジ）：Route Handlers と Server Actions の使い分けを判断しよう

以下の各シナリオについて、Route Handlers と Server Actions のどちらを使うべきか判断してください。理由も添えてください。

1. ブログ記事の新規投稿フォーム
2. モバイルアプリ向けの REST API
3. 外部サービスからの Webhook 受信
4. 「いいね」ボタンのクリック処理
5. ファイルアップロード処理
6. 外部サービスとの OAuth 連携

<details>
<summary>ヒント</summary>

「呼び出し元が何か」を基準に考えます。Next.js のフロントエンドからのデータ変更は Server Actions、外部からのアクセスは Route Handlers が適しています。

</details>

<details>
<summary>解答例</summary>

1. **ブログ記事の新規投稿フォーム → Server Actions**
   - 理由: Next.js のフロントエンドからのフォーム送信。プログレッシブエンハンスメント、`revalidatePath` との統合が容易。

2. **モバイルアプリ向けの REST API → Route Handlers**
   - 理由: 外部クライアント（モバイルアプリ）からのアクセス。RESTful な URL 設計と HTTP メソッドの使い分けが必要。

3. **外部サービスからの Webhook 受信 → Route Handlers**
   - 理由: 外部サービスが指定 URL に POST リクエストを送信する。Server Actions は Next.js の内部呼び出し専用。

4. **「いいね」ボタンのクリック処理 → Server Actions**
   - 理由: Next.js のフロントエンドからのデータ変更。`useOptimistic` と組み合わせた楽観的更新が実装しやすい。

5. **ファイルアップロード処理 → Server Actions（または Route Handlers）**
   - 理由: Next.js のフォームから送信する場合は Server Actions が適切。外部クライアントからのアップロードの場合は Route Handlers。

6. **外部サービスとの OAuth 連携 → Route Handlers**
   - 理由: OAuth のコールバック URL として外部サービスからリダイレクトされるため、Route Handlers が必要。

</details>

---

## 演習8（チャレンジ）：削除確認付きの DELETE ボタンを実装しよう

イベントハンドラから Server Action を呼び出す削除ボタンを、確認ダイアログ付きで実装してください。

**要件：**
- `useTransition` を使ってペンディング状態を管理する
- `confirm()` で削除前に確認する
- 削除完了後にキャッシュを再検証する

<details>
<summary>ヒント</summary>

Server Action はフォームだけでなく、`onClick` などのイベントハンドラからも呼び出せます。`useTransition` の `startTransition` 内で呼び出すことで、ペンディング状態を管理できます。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/actions/posts.ts
'use server'

import { revalidatePath } from 'next/cache'

export async function deletePost(postId: string) {
  // 実際にはデータベースから削除する
  console.log(`記事 ${postId} を削除しました`)

  // キャッシュの再検証
  revalidatePath('/posts')
}
```

```tsx
// app/components/DeleteButton.tsx
'use client'

import { useTransition } from 'react'
import { deletePost } from '@/app/actions/posts'

type Props = {
  postId: string
  postTitle: string
}

export default function DeleteButton({ postId, postTitle }: Props) {
  const [isPending, startTransition] = useTransition()

  function handleDelete() {
    // 確認ダイアログ
    if (!confirm(`「${postTitle}」を削除しますか？この操作は取り消せません。`)) {
      return
    }

    // startTransition 内で Server Action を呼び出す
    startTransition(async () => {
      await deletePost(postId)
    })
  }

  return (
    <button
      onClick={handleDelete}
      disabled={isPending}
      style={{
        padding: '0.5rem 1rem',
        backgroundColor: isPending ? '#ccc' : '#e53e3e',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: isPending ? 'default' : 'pointer',
      }}
    >
      {isPending ? '削除中...' : '削除'}
    </button>
  )
}
```

```tsx
// app/posts/page.tsx
import DeleteButton from '@/app/components/DeleteButton'

const posts = [
  { id: '1', title: 'Next.js 入門' },
  { id: '2', title: 'App Router ガイド' },
  { id: '3', title: 'Server Components 活用' },
]

export default function PostsPage() {
  return (
    <div style={{ padding: '2rem' }}>
      <h1>記事管理</h1>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {posts.map((post) => (
          <li key={post.id} style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '1rem',
            borderBottom: '1px solid #eaeaea',
          }}>
            <span>{post.title}</span>
            <DeleteButton postId={post.id} postTitle={post.title} />
          </li>
        ))}
      </ul>
    </div>
  )
}
```

`useTransition` を使うことで、Server Action の実行中に `isPending` が `true` になり、ボタンの無効化やローディング表示が可能になります。`confirm()` による確認ダイアログは、誤操作を防止するための重要な UX パターンです。

</details>

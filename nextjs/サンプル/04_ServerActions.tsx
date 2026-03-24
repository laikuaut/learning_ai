/**
 * ============================================================
 * サンプル04: Server Actions（フォーム処理、サーバーアクション）
 * ============================================================
 *
 * 【学べる内容】
 *   - Server Actions ('use server') の基本
 *   - <form action={serverAction}> によるフォーム送信
 *   - useFormStatus で送信中の状態を表示
 *   - useActionState でバリデーションエラーを管理
 *   - イベントハンドラからの Server Action 呼び出し
 *   - revalidatePath によるキャッシュ再検証
 *
 * 【前提条件】
 *   - npx create-next-app@latest my-app でプロジェクト作成済み
 *   - App Router + TypeScript を選択済み
 *
 * 【ファイルの配置場所】
 *   各セクションを以下のパスに分割して配置してください:
 *
 *   1. app/actions/todo.ts           — Server Action の定義
 *   2. app/components/SubmitButton.tsx — 送信ボタン（useFormStatus）
 *   3. app/todo/page.tsx             — TODO アプリページ
 *   4. app/feedback/page.tsx         — フィードバックフォーム（useActionState）
 *
 * 【実行方法】
 *   cd my-app
 *   npm run dev
 *   http://localhost:3000/todo
 *   http://localhost:3000/feedback
 *
 * ============================================================
 */

// ============================================================
// 1. app/actions/todo.ts — Server Actions の定義
// ============================================================
// 'use server' をファイルの先頭に置くと、このファイル内のすべての
// エクスポートされた関数が Server Action として扱われます。

'use server'

import { revalidatePath } from 'next/cache'

// TODO の型定義
type Todo = {
  id: string
  text: string
  completed: boolean
  createdAt: string
}

// インメモリのTODOデータ（実際にはデータベースを使用）
// 注意: 開発サーバーではホットリロード時にリセットされます
const todos: Todo[] = [
  { id: '1', text: 'Next.js の基本を学ぶ', completed: true, createdAt: '2026-03-20' },
  { id: '2', text: 'App Router を理解する', completed: false, createdAt: '2026-03-21' },
  { id: '3', text: 'Server Actions を試す', completed: false, createdAt: '2026-03-22' },
]

// TODO の一覧を取得
export async function getTodos(): Promise<Todo[]> {
  // 実際にはデータベースから取得する
  return [...todos]
}

// 新しい TODO を追加する Server Action
export async function addTodo(formData: FormData) {
  const text = formData.get('text') as string

  // バリデーション
  if (!text || text.trim().length === 0) {
    return { error: 'テキストを入力してください' }
  }

  if (text.length > 100) {
    return { error: 'テキストは100文字以内にしてください' }
  }

  // 新しい TODO を作成（実際にはデータベースに保存）
  const newTodo: Todo = {
    id: String(Date.now()),
    text: text.trim(),
    completed: false,
    createdAt: new Date().toISOString().split('T')[0],
  }

  todos.push(newTodo)

  // /todo ページのキャッシュを再検証
  revalidatePath('/todo')

  return { success: true }
}

// TODO の完了状態を切り替える Server Action
export async function toggleTodo(id: string) {
  const todo = todos.find((t) => t.id === id)
  if (todo) {
    todo.completed = !todo.completed
  }

  revalidatePath('/todo')
}

// TODO を削除する Server Action
export async function deleteTodo(id: string) {
  const index = todos.findIndex((t) => t.id === id)
  if (index !== -1) {
    todos.splice(index, 1)
  }

  revalidatePath('/todo')
}

// ============================================================
// 2. app/components/SubmitButton.tsx — 送信中の状態表示
// ============================================================
// useFormStatus は <form> の子コンポーネント内でのみ動作します。
// フォームと同じコンポーネントでは使えないため、必ず分離してください。

/*
// SubmitButton.tsx
'use client'

import { useFormStatus } from 'react-dom'

type Props = {
  label?: string
  pendingLabel?: string
}

export default function SubmitButton({
  label = '送信',
  pendingLabel = '送信中...',
}: Props) {
  // useFormStatus は親の <form> の送信状態を取得する
  const { pending } = useFormStatus()

  return (
    <button
      type="submit"
      disabled={pending}
      style={{
        padding: '0.5rem 1.5rem',
        backgroundColor: pending ? '#a0aec0' : '#0070f3',
        color: 'white',
        border: 'none',
        borderRadius: '6px',
        cursor: pending ? 'default' : 'pointer',
        fontSize: '0.95rem',
        transition: 'background-color 0.2s',
      }}
    >
      {pending ? pendingLabel : label}
    </button>
  )
}
*/

// ============================================================
// 3. app/todo/page.tsx — TODO アプリ
// ============================================================
// サーバーコンポーネントで TODO を取得し、
// Server Actions でデータの追加・更新・削除を行います。

/*
import { getTodos, addTodo, toggleTodo, deleteTodo } from '@/app/actions/todo'
import SubmitButton from '@/app/components/SubmitButton'
import TodoItem from './TodoItem'

export default async function TodoPage() {
  // サーバーでTODOを取得
  const todos = await getTodos()

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
      <h1>TODO アプリ</h1>
      <p style={{ color: '#666' }}>
        Server Actions を使った CRUD 操作のデモです。
      </p>

      {// 追加フォーム }
      <form
        action={addTodo}
        style={{
          display: 'flex',
          gap: '0.5rem',
          marginBottom: '1.5rem',
        }}
      >
        <input
          type="text"
          name="text"
          placeholder="新しい TODO を入力..."
          required
          style={{
            flex: 1,
            padding: '0.5rem',
            border: '1px solid #e2e8f0',
            borderRadius: '6px',
          }}
        />
        <SubmitButton label="追加" pendingLabel="追加中..." />
      </form>

      {// TODO リスト }
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {todos.map((todo) => (
          <TodoItem key={todo.id} todo={todo} />
        ))}
      </ul>

      {todos.length === 0 && (
        <p style={{ textAlign: 'center', color: '#a0aec0' }}>
          TODO がありません。新しい TODO を追加してください。
        </p>
      )}
    </div>
  )
}
*/

// ============================================================
// app/todo/TodoItem.tsx — 個別の TODO アイテム
// ============================================================
// イベントハンドラから Server Action を呼び出す例です。

/*
'use client'

import { useTransition } from 'react'
import { toggleTodo, deleteTodo } from '@/app/actions/todo'

type Todo = {
  id: string
  text: string
  completed: boolean
  createdAt: string
}

export default function TodoItem({ todo }: { todo: Todo }) {
  const [isPending, startTransition] = useTransition()

  function handleToggle() {
    startTransition(async () => {
      await toggleTodo(todo.id)
    })
  }

  function handleDelete() {
    if (!confirm('この TODO を削除しますか？')) return
    startTransition(async () => {
      await deleteTodo(todo.id)
    })
  }

  return (
    <li style={{
      display: 'flex',
      alignItems: 'center',
      gap: '0.75rem',
      padding: '0.75rem',
      borderBottom: '1px solid #e2e8f0',
      opacity: isPending ? 0.5 : 1,
      transition: 'opacity 0.2s',
    }}>
      {// チェックボックス }
      <button
        onClick={handleToggle}
        disabled={isPending}
        style={{
          background: 'none',
          border: 'none',
          fontSize: '1.2rem',
          cursor: 'pointer',
        }}
      >
        {todo.completed ? '✅' : '⬜'}
      </button>

      {// テキスト }
      <span style={{
        flex: 1,
        textDecoration: todo.completed ? 'line-through' : 'none',
        color: todo.completed ? '#a0aec0' : '#2d3748',
      }}>
        {todo.text}
      </span>

      {// 日付 }
      <span style={{ color: '#a0aec0', fontSize: '0.8rem' }}>
        {todo.createdAt}
      </span>

      {// 削除ボタン }
      <button
        onClick={handleDelete}
        disabled={isPending}
        style={{
          background: 'none',
          border: 'none',
          color: '#e53e3e',
          cursor: 'pointer',
          fontSize: '0.85rem',
        }}
      >
        削除
      </button>
    </li>
  )
}
*/

// ============================================================
// 4. app/feedback/page.tsx — useActionState でエラー管理
// ============================================================

/*
'use client'

import { useActionState } from 'react'
import SubmitButton from '@/app/components/SubmitButton'

// Server Action（インラインではなく別ファイルに定義推奨）
import { submitFeedback } from '@/app/actions/feedback'

export default function FeedbackPage() {
  // useActionState: Server Action の結果を状態として管理
  // 第1引数: Server Action
  // 第2引数: 初期状態
  const [state, formAction] = useActionState(submitFeedback, {})

  return (
    <div style={{ padding: '2rem', maxWidth: '500px', margin: '0 auto' }}>
      <h1>フィードバック</h1>

      {// 成功メッセージ }
      {state.success && (
        <div style={{
          padding: '1rem',
          backgroundColor: '#c6f6d5',
          borderRadius: '8px',
          marginBottom: '1rem',
          color: '#22543d',
        }}>
          フィードバックを送信しました。ありがとうございます！
        </div>
      )}

      {// エラーメッセージ }
      {state.message && !state.success && (
        <div style={{
          padding: '1rem',
          backgroundColor: '#fed7d7',
          borderRadius: '8px',
          marginBottom: '1rem',
          color: '#c53030',
        }}>
          {state.message}
        </div>
      )}

      <form action={formAction}>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="name" style={{ display: 'block', marginBottom: '0.25rem' }}>
            お名前 <span style={{ color: '#e53e3e' }}>*</span>
          </label>
          <input
            type="text"
            id="name"
            name="name"
            style={{
              width: '100%',
              padding: '0.5rem',
              border: `1px solid ${state.errors?.name ? '#e53e3e' : '#e2e8f0'}`,
              borderRadius: '6px',
              boxSizing: 'border-box',
            }}
          />
          {state.errors?.name && (
            <p style={{ color: '#e53e3e', fontSize: '0.85rem', margin: '0.25rem 0 0' }}>
              {state.errors.name[0]}
            </p>
          )}
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="email" style={{ display: 'block', marginBottom: '0.25rem' }}>
            メールアドレス <span style={{ color: '#e53e3e' }}>*</span>
          </label>
          <input
            type="email"
            id="email"
            name="email"
            style={{
              width: '100%',
              padding: '0.5rem',
              border: `1px solid ${state.errors?.email ? '#e53e3e' : '#e2e8f0'}`,
              borderRadius: '6px',
              boxSizing: 'border-box',
            }}
          />
          {state.errors?.email && (
            <p style={{ color: '#e53e3e', fontSize: '0.85rem', margin: '0.25rem 0 0' }}>
              {state.errors.email[0]}
            </p>
          )}
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="rating" style={{ display: 'block', marginBottom: '0.25rem' }}>
            評価 <span style={{ color: '#e53e3e' }}>*</span>
          </label>
          <select
            id="rating"
            name="rating"
            style={{
              width: '100%',
              padding: '0.5rem',
              border: '1px solid #e2e8f0',
              borderRadius: '6px',
              boxSizing: 'border-box',
            }}
          >
            <option value="">選択してください</option>
            <option value="5">5 - とても満足</option>
            <option value="4">4 - 満足</option>
            <option value="3">3 - 普通</option>
            <option value="2">2 - 不満</option>
            <option value="1">1 - とても不満</option>
          </select>
        </div>

        <div style={{ marginBottom: '1.5rem' }}>
          <label htmlFor="message" style={{ display: 'block', marginBottom: '0.25rem' }}>
            メッセージ <span style={{ color: '#e53e3e' }}>*</span>
          </label>
          <textarea
            id="message"
            name="message"
            rows={5}
            style={{
              width: '100%',
              padding: '0.5rem',
              border: `1px solid ${state.errors?.message ? '#e53e3e' : '#e2e8f0'}`,
              borderRadius: '6px',
              boxSizing: 'border-box',
            }}
          />
          {state.errors?.message && (
            <p style={{ color: '#e53e3e', fontSize: '0.85rem', margin: '0.25rem 0 0' }}>
              {state.errors.message[0]}
            </p>
          )}
        </div>

        <SubmitButton label="送信する" pendingLabel="送信中..." />
      </form>
    </div>
  )
}
*/

// ============================================================
// app/actions/feedback.ts — フィードバック用の Server Action
// ============================================================

/*
'use server'

type FeedbackState = {
  errors?: {
    name?: string[]
    email?: string[]
    message?: string[]
  }
  message?: string
  success?: boolean
}

export async function submitFeedback(
  prevState: FeedbackState,
  formData: FormData
): Promise<FeedbackState> {
  const name = formData.get('name') as string
  const email = formData.get('email') as string
  const rating = formData.get('rating') as string
  const message = formData.get('message') as string

  const errors: FeedbackState['errors'] = {}

  // バリデーション
  if (!name || name.length < 2) {
    errors.name = ['名前は2文字以上で入力してください']
  }
  if (!email || !email.includes('@')) {
    errors.email = ['有効なメールアドレスを入力してください']
  }
  if (!message || message.length < 10) {
    errors.message = ['メッセージは10文字以上で入力してください']
  }

  if (Object.keys(errors).length > 0) {
    return { errors, message: '入力内容に問題があります' }
  }

  // 保存処理（実際にはデータベースやメール送信）
  console.log('フィードバック受信:', { name, email, rating, message })

  return { success: true }
}
*/

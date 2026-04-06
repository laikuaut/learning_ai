# 実践課題06：Server Actions フォーム ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第3章（サーバーコンポーネント）、第5章（APIルートとServer Actions）
> **課題の種類**: ミニプロジェクト
> **学習目標**: Server Actions によるフォーム送信、バリデーション（Validation）、楽観的更新（Optimistic Updates）を組み合わせて実践する

---

## 完成イメージ

TODOアプリをServer Actionsで実装します。フォーム送信がサーバー上で処理され、ページが自動的に再検証（Revalidation）されます。

```
┌──────────────────────────────────────┐
│  ✅ TODO アプリ                       │
├──────────────────────────────────────┤
│                                      │
│  ┌─────────────────────┐ [追加]     │
│  │ 新しいタスクを入力...  │            │
│  └─────────────────────┘            │
│                                      │
│  □ Next.jsの復習をする     [削除]     │
│  ■ TypeScriptの型を学ぶ   [削除]     │
│  □ テストを書く           [削除]     │
│                                      │
│  完了: 1/3 (33%)                     │
└──────────────────────────────────────┘
```

---

## 課題の要件

1. Server Actions を使って TODO の追加・削除・完了切替を実装する
2. フォームのバリデーション（空文字チェック、文字数制限）を行う
3. `revalidatePath` でデータ変更後にページを再検証する
4. `useFormStatus` でフォーム送信中の状態を表示する
5. データはファイルシステムまたはインメモリ配列で保持する（データベース不要）

---

## ステップガイド

<details>
<summary>ステップ1：Server Actions の基本を理解する</summary>

Server Actions は `'use server'` ディレクティブで宣言する非同期関数です。フォームの `action` 属性に直接渡せます。

```tsx
// app/actions.ts
'use server'

export async function addTodo(formData: FormData) {
  const title = formData.get('title') as string
  // サーバー上で実行される処理
}
```

```tsx
// app/page.tsx
import { addTodo } from './actions'

export default function Page() {
  return (
    <form action={addTodo}>
      <input name="title" />
      <button type="submit">追加</button>
    </form>
  )
}
```

</details>

<details>
<summary>ステップ2：バリデーションを追加する</summary>

```tsx
'use server'

export async function addTodo(formData: FormData) {
  const title = formData.get('title') as string

  // サーバーサイドバリデーション
  if (!title || title.trim().length === 0) {
    return { error: 'タイトルを入力してください' }
  }

  if (title.length > 100) {
    return { error: 'タイトルは100文字以内にしてください' }
  }

  // TODO を追加する処理...
}
```

</details>

<details>
<summary>ステップ3：useFormStatus で送信状態を表示する</summary>

```tsx
'use client'

import { useFormStatus } from 'react-dom'

function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button type="submit" disabled={pending}>
      {pending ? '追加中...' : '追加'}
    </button>
  )
}
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

### lib/todos.ts

```tsx
// インメモリデータストア（サーバー再起動で初期化されます）
export type Todo = {
  id: string
  title: string
  completed: boolean
  createdAt: string
}

let todos: Todo[] = [
  { id: '1', title: 'Next.jsの復習をする', completed: false, createdAt: '2026-04-01' },
  { id: '2', title: 'TypeScriptの型を学ぶ', completed: true, createdAt: '2026-04-02' },
  { id: '3', title: 'テストを書く', completed: false, createdAt: '2026-04-03' },
]

export function getTodos(): Todo[] {
  return [...todos].sort(
    (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  )
}

export function addTodoToStore(title: string): Todo {
  const newTodo: Todo = {
    id: Date.now().toString(),
    title,
    completed: false,
    createdAt: new Date().toISOString().split('T')[0],
  }
  todos.push(newTodo)
  return newTodo
}

export function deleteTodoFromStore(id: string): void {
  todos = todos.filter((todo) => todo.id !== id)
}

export function toggleTodoInStore(id: string): void {
  todos = todos.map((todo) =>
    todo.id === id ? { ...todo, completed: !todo.completed } : todo
  )
}
```

### app/todos/actions.ts

```tsx
'use server'

import { revalidatePath } from 'next/cache'
import { addTodoToStore, deleteTodoFromStore, toggleTodoInStore } from '@/lib/todos'

export async function addTodoAction(formData: FormData) {
  const title = formData.get('title') as string

  // サーバーサイドバリデーション
  if (!title || title.trim().length === 0) {
    return { error: 'タイトルを入力してください' }
  }

  if (title.trim().length > 100) {
    return { error: 'タイトルは100文字以内にしてください' }
  }

  // TODOを追加
  addTodoToStore(title.trim())

  // ページを再検証して最新データを表示
  revalidatePath('/todos')
}

export async function deleteTodoAction(formData: FormData) {
  const id = formData.get('id') as string
  deleteTodoFromStore(id)
  revalidatePath('/todos')
}

export async function toggleTodoAction(formData: FormData) {
  const id = formData.get('id') as string
  toggleTodoInStore(id)
  revalidatePath('/todos')
}
```

### app/todos/SubmitButton.tsx

```tsx
'use client'

import { useFormStatus } from 'react-dom'

export default function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button
      type="submit"
      disabled={pending}
      style={{
        padding: '10px 20px',
        backgroundColor: pending ? '#94a3b8' : '#2563eb',
        color: 'white',
        border: 'none',
        borderRadius: '0 8px 8px 0',
        cursor: pending ? 'not-allowed' : 'pointer',
        fontSize: '14px',
        whiteSpace: 'nowrap',
      }}
    >
      {pending ? '追加中...' : '追加'}
    </button>
  )
}
```

### app/todos/page.tsx

```tsx
import { getTodos } from '@/lib/todos'
import { addTodoAction, deleteTodoAction, toggleTodoAction } from './actions'
import SubmitButton from './SubmitButton'

export default function TodosPage() {
  const todos = getTodos()
  const completedCount = todos.filter(function (t) {
    return t.completed
  }).length

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '24px' }}>
      <h1>TODO アプリ</h1>

      {/* 追加フォーム */}
      <form
        action={addTodoAction}
        style={{
          display: 'flex',
          marginBottom: '24px',
        }}
      >
        <input
          name="title"
          placeholder="新しいタスクを入力..."
          style={{
            flex: 1,
            padding: '10px 16px',
            border: '1px solid #e2e8f0',
            borderRadius: '8px 0 0 8px',
            fontSize: '14px',
            outline: 'none',
          }}
        />
        <SubmitButton />
      </form>

      {/* TODO一覧 */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {todos.map(function (todo) {
          return (
            <div
              key={todo.id}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px 16px',
                backgroundColor: 'white',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
              }}
            >
              {/* 完了切替 */}
              <form action={toggleTodoAction}>
                <input type="hidden" name="id" value={todo.id} />
                <button
                  type="submit"
                  style={{
                    width: '24px',
                    height: '24px',
                    border: '2px solid #cbd5e1',
                    borderRadius: '4px',
                    backgroundColor: todo.completed ? '#2563eb' : 'white',
                    color: 'white',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '12px',
                  }}
                >
                  {todo.completed ? '✓' : ''}
                </button>
              </form>

              {/* タイトル */}
              <span
                style={{
                  flex: 1,
                  textDecoration: todo.completed ? 'line-through' : 'none',
                  color: todo.completed ? '#94a3b8' : '#1e293b',
                }}
              >
                {todo.title}
              </span>

              {/* 削除 */}
              <form action={deleteTodoAction}>
                <input type="hidden" name="id" value={todo.id} />
                <button
                  type="submit"
                  style={{
                    padding: '4px 12px',
                    backgroundColor: 'transparent',
                    color: '#ef4444',
                    border: '1px solid #fecaca',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '12px',
                  }}
                >
                  削除
                </button>
              </form>
            </div>
          )
        })}
      </div>

      {/* 統計 */}
      <div
        style={{
          marginTop: '24px',
          padding: '16px',
          backgroundColor: '#f8fafc',
          borderRadius: '8px',
          textAlign: 'center',
          color: '#64748b',
        }}
      >
        完了: {completedCount}/{todos.length}{' '}
        ({todos.length > 0 ? Math.round((completedCount / todos.length) * 100) : 0}%)
      </div>
    </div>
  )
}
```

</details>

<details>
<summary>解答例（改良版 ─ useActionState + useOptimistic）</summary>

### app/todos/TodoForm.tsx

```tsx
'use client'

import { useActionState } from 'react'
import { useRef } from 'react'
import { addTodoAction } from './actions'

export default function TodoForm() {
  const formRef = useRef<HTMLFormElement>(null)

  // useActionState でServer Actionの戻り値を管理
  const [state, formAction, isPending] = useActionState(
    async (prevState: { error?: string } | null, formData: FormData) => {
      const result = await addTodoAction(formData)
      if (!result?.error) {
        formRef.current?.reset() // 成功時にフォームをクリア
      }
      return result ?? null
    },
    null
  )

  return (
    <form
      ref={formRef}
      action={formAction}
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '8px',
        marginBottom: '24px',
      }}
    >
      <div style={{ display: 'flex' }}>
        <input
          name="title"
          placeholder="新しいタスクを入力..."
          maxLength={100}
          style={{
            flex: 1,
            padding: '10px 16px',
            border: `1px solid ${state?.error ? '#fecaca' : '#e2e8f0'}`,
            borderRadius: '8px 0 0 8px',
            fontSize: '14px',
            outline: 'none',
          }}
        />
        <button
          type="submit"
          disabled={isPending}
          style={{
            padding: '10px 20px',
            backgroundColor: isPending ? '#94a3b8' : '#2563eb',
            color: 'white',
            border: 'none',
            borderRadius: '0 8px 8px 0',
            cursor: isPending ? 'not-allowed' : 'pointer',
          }}
        >
          {isPending ? '追加中...' : '追加'}
        </button>
      </div>
      {state?.error && (
        <p style={{ color: '#ef4444', fontSize: '14px', margin: 0 }}>
          {state.error}
        </p>
      )}
    </form>
  )
}
```

### app/todos/TodoList.tsx

```tsx
'use client'

import { useOptimistic } from 'react'
import { toggleTodoAction, deleteTodoAction } from './actions'

type Todo = {
  id: string
  title: string
  completed: boolean
}

export default function TodoList({ todos }: { todos: Todo[] }) {
  // 楽観的更新 — UIを即座に更新し、サーバーの応答を待たない
  const [optimisticTodos, addOptimistic] = useOptimistic(
    todos,
    (
      state: Todo[],
      action: { type: 'toggle' | 'delete'; id: string }
    ) => {
      if (action.type === 'toggle') {
        return state.map((todo) =>
          todo.id === action.id
            ? { ...todo, completed: !todo.completed }
            : todo
        )
      }
      if (action.type === 'delete') {
        return state.filter((todo) => todo.id !== action.id)
      }
      return state
    }
  )

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      {optimisticTodos.map((todo) => (
        <div
          key={todo.id}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            padding: '12px 16px',
            backgroundColor: 'white',
            border: '1px solid #e2e8f0',
            borderRadius: '8px',
            transition: 'opacity 0.2s',
          }}
        >
          <form
            action={async (formData) => {
              addOptimistic({ type: 'toggle', id: todo.id })
              await toggleTodoAction(formData)
            }}
          >
            <input type="hidden" name="id" value={todo.id} />
            <button
              type="submit"
              style={{
                width: '24px',
                height: '24px',
                border: '2px solid #cbd5e1',
                borderRadius: '4px',
                backgroundColor: todo.completed ? '#2563eb' : 'white',
                color: 'white',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              {todo.completed ? '✓' : ''}
            </button>
          </form>

          <span
            style={{
              flex: 1,
              textDecoration: todo.completed ? 'line-through' : 'none',
              color: todo.completed ? '#94a3b8' : '#1e293b',
            }}
          >
            {todo.title}
          </span>

          <form
            action={async (formData) => {
              addOptimistic({ type: 'delete', id: todo.id })
              await deleteTodoAction(formData)
            }}
          >
            <input type="hidden" name="id" value={todo.id} />
            <button
              type="submit"
              style={{
                padding: '4px 12px',
                backgroundColor: 'transparent',
                color: '#ef4444',
                border: '1px solid #fecaca',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              削除
            </button>
          </form>
        </div>
      ))}
    </div>
  )
}
```

### app/todos/page.tsx（改良版）

```tsx
import { getTodos } from '@/lib/todos'
import TodoForm from './TodoForm'
import TodoList from './TodoList'

export default function TodosPage() {
  const todos = getTodos()
  const completedCount = todos.filter((t) => t.completed).length

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '24px' }}>
      <h1>TODO アプリ</h1>
      <TodoForm />
      <TodoList todos={todos} />
      <div
        style={{
          marginTop: '24px',
          padding: '16px',
          backgroundColor: '#f8fafc',
          borderRadius: '8px',
          textAlign: 'center',
          color: '#64748b',
        }}
      >
        完了: {completedCount}/{todos.length}{' '}
        ({todos.length > 0 ? Math.round((completedCount / todos.length) * 100) : 0}%)
      </div>
    </div>
  )
}
```

**初心者向けとの違い:**
- `useActionState` でフォームの送信状態とバリデーションエラーを一元管理
- `useOptimistic` でチェック/削除時にUIを即座に更新（サーバー応答を待たない）
- フォーム送信成功時に `formRef.current?.reset()` で入力欄を自動クリア
- エラーメッセージの表示/非表示をstateで制御
- コンポーネントを `TodoForm` と `TodoList` に分離し、責務を明確化

</details>

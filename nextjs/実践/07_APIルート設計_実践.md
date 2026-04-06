# 実践課題07：APIルート設計 ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第4章（データフェッチング）、第5章（APIルートとServer Actions）
> **課題の種類**: 設計課題
> **学習目標**: Route Handlers による RESTful API の設計、リクエスト/レスポンスの処理、エラーハンドリングのパターンを実践する

---

## 完成イメージ

書籍管理APIを設計・実装します。CRUD操作をRoute Handlersで実現し、フロントエンドからfetchで呼び出します。

```
API エンドポイント:
┌──────────────────────────────────────────────────┐
│ GET    /api/books        → 書籍一覧の取得        │
│ POST   /api/books        → 新規書籍の追加        │
│ GET    /api/books/:id    → 書籍詳細の取得        │
│ PUT    /api/books/:id    → 書籍情報の更新        │
│ DELETE /api/books/:id    → 書籍の削除            │
│ GET    /api/books/search?q=... → 書籍の検索      │
└──────────────────────────────────────────────────┘

フロントエンド:
┌──────────────────────────────────────┐
│  📚 書籍管理                         │
├──────────────────────────────────────┤
│  検索: [TypeScript      ] [検索]     │
│                                      │
│  ┌────────────────────────────┐      │
│  │ 実践TypeScript             │      │
│  │ 著者: 鈴木太郎  ¥3,200    │      │
│  │ ISBN: 978-4-xxx-xxxxx-x   │      │
│  │ [編集] [削除]             │      │
│  └────────────────────────────┘      │
└──────────────────────────────────────┘
```

---

## 課題の要件

1. `app/api/books/route.ts` に GET（一覧）と POST（追加）を実装する
2. `app/api/books/[id]/route.ts` に GET（詳細）、PUT（更新）、DELETE（削除）を実装する
3. `app/api/books/search/route.ts` に検索機能を実装する
4. 適切な HTTP ステータスコード（200, 201, 400, 404, 500）を返す
5. リクエストボディのバリデーションを行う
6. フロントエンドから API を呼び出すページを作成する

---

## ステップガイド

<details>
<summary>ステップ1：データモデルを定義する</summary>

```tsx
// lib/books.ts
export type Book = {
  id: string
  title: string
  author: string
  price: number
  isbn: string
  publishedAt: string
}
```

</details>

<details>
<summary>ステップ2：Route Handlers の基本形を理解する</summary>

```tsx
// app/api/books/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  // 一覧取得
  return NextResponse.json({ data: [] })
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  // 追加処理
  return NextResponse.json({ data: newBook }, { status: 201 })
}
```

</details>

<details>
<summary>ステップ3：URLSearchParamsでクエリパラメータを取得する</summary>

```tsx
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const query = searchParams.get('q')
  // 検索処理
}
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

### lib/books.ts

```tsx
export type Book = {
  id: string
  title: string
  author: string
  price: number
  isbn: string
  publishedAt: string
}

let books: Book[] = [
  {
    id: '1',
    title: '実践TypeScript',
    author: '鈴木太郎',
    price: 3200,
    isbn: '978-4-000-00001-1',
    publishedAt: '2025-06-15',
  },
  {
    id: '2',
    title: 'Next.js実践入門',
    author: '田中花子',
    price: 3600,
    isbn: '978-4-000-00002-2',
    publishedAt: '2025-09-20',
  },
  {
    id: '3',
    title: 'React設計パターン',
    author: '佐藤次郎',
    price: 2800,
    isbn: '978-4-000-00003-3',
    publishedAt: '2025-03-10',
  },
]

export function getAllBooks(): Book[] {
  return [...books]
}

export function getBookById(id: string): Book | undefined {
  return books.find(function (book) {
    return book.id === id
  })
}

export function addBook(data: Omit<Book, 'id'>): Book {
  const newBook: Book = {
    ...data,
    id: Date.now().toString(),
  }
  books.push(newBook)
  return newBook
}

export function updateBook(id: string, data: Partial<Omit<Book, 'id'>>): Book | null {
  const index = books.findIndex(function (book) {
    return book.id === id
  })
  if (index === -1) return null
  books[index] = { ...books[index], ...data }
  return books[index]
}

export function deleteBook(id: string): boolean {
  const length = books.length
  books = books.filter(function (book) {
    return book.id !== id
  })
  return books.length < length
}

export function searchBooks(query: string): Book[] {
  const lowerQuery = query.toLowerCase()
  return books.filter(function (book) {
    return (
      book.title.toLowerCase().includes(lowerQuery) ||
      book.author.toLowerCase().includes(lowerQuery)
    )
  })
}
```

### app/api/books/route.ts

```tsx
import { NextRequest, NextResponse } from 'next/server'
import { getAllBooks, addBook } from '@/lib/books'

// GET /api/books — 書籍一覧を取得
export async function GET() {
  const books = getAllBooks()
  return NextResponse.json({ data: books })
}

// POST /api/books — 新規書籍を追加
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    // バリデーション
    if (!body.title || typeof body.title !== 'string') {
      return NextResponse.json(
        { error: 'タイトルは必須です' },
        { status: 400 }
      )
    }
    if (!body.author || typeof body.author !== 'string') {
      return NextResponse.json(
        { error: '著者名は必須です' },
        { status: 400 }
      )
    }
    if (typeof body.price !== 'number' || body.price < 0) {
      return NextResponse.json(
        { error: '価格は0以上の数値で指定してください' },
        { status: 400 }
      )
    }

    const newBook = addBook({
      title: body.title,
      author: body.author,
      price: body.price,
      isbn: body.isbn || '',
      publishedAt: body.publishedAt || new Date().toISOString().split('T')[0],
    })

    return NextResponse.json({ data: newBook }, { status: 201 })
  } catch {
    return NextResponse.json(
      { error: 'リクエストの処理に失敗しました' },
      { status: 500 }
    )
  }
}
```

### app/api/books/[id]/route.ts

```tsx
import { NextRequest, NextResponse } from 'next/server'
import { getBookById, updateBook, deleteBook } from '@/lib/books'

// GET /api/books/:id — 書籍詳細を取得
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const book = getBookById(id)

  if (!book) {
    return NextResponse.json(
      { error: '書籍が見つかりません' },
      { status: 404 }
    )
  }

  return NextResponse.json({ data: book })
}

// PUT /api/books/:id — 書籍情報を更新
export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params
    const body = await request.json()

    const updated = updateBook(id, body)

    if (!updated) {
      return NextResponse.json(
        { error: '書籍が見つかりません' },
        { status: 404 }
      )
    }

    return NextResponse.json({ data: updated })
  } catch {
    return NextResponse.json(
      { error: '更新に失敗しました' },
      { status: 500 }
    )
  }
}

// DELETE /api/books/:id — 書籍を削除
export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const deleted = deleteBook(id)

  if (!deleted) {
    return NextResponse.json(
      { error: '書籍が見つかりません' },
      { status: 404 }
    )
  }

  return NextResponse.json({ message: '削除しました' })
}
```

### app/api/books/search/route.ts

```tsx
import { NextRequest, NextResponse } from 'next/server'
import { searchBooks } from '@/lib/books'

export async function GET(request: NextRequest) {
  const query = request.nextUrl.searchParams.get('q')

  if (!query) {
    return NextResponse.json(
      { error: '検索キーワードを指定してください（?q=キーワード）' },
      { status: 400 }
    )
  }

  const results = searchBooks(query)
  return NextResponse.json({ data: results, count: results.length })
}
```

### app/books/BookManager.tsx

```tsx
'use client'

import { useState, useEffect } from 'react'

type Book = {
  id: string
  title: string
  author: string
  price: number
  isbn: string
}

export default function BookManager() {
  const [books, setBooks] = useState<Book[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [title, setTitle] = useState('')
  const [author, setAuthor] = useState('')
  const [price, setPrice] = useState('')
  const [error, setError] = useState('')

  // 書籍一覧を取得
  async function fetchBooks() {
    const res = await fetch('/api/books')
    const json = await res.json()
    setBooks(json.data)
  }

  useEffect(function () {
    fetchBooks()
  }, [])

  // 書籍を追加
  async function handleAdd(e: React.FormEvent) {
    e.preventDefault()
    setError('')

    const res = await fetch('/api/books', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title,
        author,
        price: Number(price),
      }),
    })

    const json = await res.json()

    if (!res.ok) {
      setError(json.error)
      return
    }

    setTitle('')
    setAuthor('')
    setPrice('')
    fetchBooks()
  }

  // 書籍を削除
  async function handleDelete(id: string) {
    await fetch(`/api/books/${id}`, { method: 'DELETE' })
    fetchBooks()
  }

  // 検索
  async function handleSearch() {
    if (!searchQuery.trim()) {
      fetchBooks()
      return
    }

    const res = await fetch(`/api/books/search?q=${encodeURIComponent(searchQuery)}`)
    const json = await res.json()
    setBooks(json.data)
  }

  return (
    <div style={{ maxWidth: '700px', margin: '0 auto', padding: '24px' }}>
      <h1>書籍管理</h1>

      {/* 検索 */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '24px' }}>
        <input
          value={searchQuery}
          onChange={function (e) { setSearchQuery(e.target.value) }}
          placeholder="タイトルまたは著者で検索..."
          style={{
            flex: 1,
            padding: '8px 16px',
            border: '1px solid #e2e8f0',
            borderRadius: '8px',
          }}
        />
        <button
          onClick={handleSearch}
          style={{
            padding: '8px 16px',
            backgroundColor: '#2563eb',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
          }}
        >
          検索
        </button>
      </div>

      {/* 追加フォーム */}
      <form onSubmit={handleAdd} style={{ marginBottom: '24px', padding: '16px', backgroundColor: '#f8fafc', borderRadius: '8px' }}>
        <h2 style={{ fontSize: '16px', marginTop: 0 }}>書籍を追加</h2>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          <input value={title} onChange={function (e) { setTitle(e.target.value) }} placeholder="タイトル" style={{ flex: 2, padding: '8px', border: '1px solid #e2e8f0', borderRadius: '4px' }} />
          <input value={author} onChange={function (e) { setAuthor(e.target.value) }} placeholder="著者" style={{ flex: 1, padding: '8px', border: '1px solid #e2e8f0', borderRadius: '4px' }} />
          <input value={price} onChange={function (e) { setPrice(e.target.value) }} placeholder="価格" type="number" style={{ width: '100px', padding: '8px', border: '1px solid #e2e8f0', borderRadius: '4px' }} />
          <button type="submit" style={{ padding: '8px 16px', backgroundColor: '#22c55e', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>追加</button>
        </div>
        {error && <p style={{ color: '#ef4444', fontSize: '14px', marginBottom: 0 }}>{error}</p>}
      </form>

      {/* 一覧 */}
      {books.map(function (book) {
        return (
          <div key={book.id} style={{ padding: '16px', border: '1px solid #e2e8f0', borderRadius: '8px', marginBottom: '12px', backgroundColor: 'white' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <strong style={{ fontSize: '16px' }}>{book.title}</strong>
                <div style={{ fontSize: '14px', color: '#64748b', marginTop: '4px' }}>
                  著者: {book.author} / ¥{book.price.toLocaleString()}
                </div>
                {book.isbn && (
                  <div style={{ fontSize: '12px', color: '#94a3b8', marginTop: '2px' }}>
                    ISBN: {book.isbn}
                  </div>
                )}
              </div>
              <button
                onClick={function () { handleDelete(book.id) }}
                style={{
                  padding: '4px 12px',
                  color: '#ef4444',
                  border: '1px solid #fecaca',
                  borderRadius: '4px',
                  backgroundColor: 'transparent',
                  cursor: 'pointer',
                }}
              >
                削除
              </button>
            </div>
          </div>
        )
      })}
    </div>
  )
}
```

### app/books/page.tsx

```tsx
import BookManager from './BookManager'

export default function BooksPage() {
  return <BookManager />
}
```

</details>

<details>
<summary>解答例（改良版 ─ バリデーション関数分離 + 型安全なレスポンス）</summary>

### lib/validation.ts

```tsx
type ValidationResult =
  | { success: true; data: Record<string, unknown> }
  | { success: false; error: string }

export function validateBook(body: unknown): ValidationResult {
  if (!body || typeof body !== 'object') {
    return { success: false, error: '不正なリクエストです' }
  }

  const data = body as Record<string, unknown>

  if (!data.title || typeof data.title !== 'string' || data.title.trim().length === 0) {
    return { success: false, error: 'タイトルは必須です' }
  }

  if (data.title.length > 200) {
    return { success: false, error: 'タイトルは200文字以内にしてください' }
  }

  if (!data.author || typeof data.author !== 'string' || data.author.trim().length === 0) {
    return { success: false, error: '著者名は必須です' }
  }

  if (typeof data.price !== 'number' || data.price < 0 || !Number.isInteger(data.price)) {
    return { success: false, error: '価格は0以上の整数で指定してください' }
  }

  return { success: true, data }
}
```

### app/api/books/route.ts（改良版）

```tsx
import { NextRequest, NextResponse } from 'next/server'
import { getAllBooks, addBook } from '@/lib/books'
import { validateBook } from '@/lib/validation'

// レスポンスヘッダーの共通設定
function jsonResponse<T>(data: T, status = 200) {
  return NextResponse.json(data, {
    status,
    headers: {
      'Cache-Control': 'no-store',
    },
  })
}

function errorResponse(message: string, status: number) {
  return jsonResponse({ error: message, status }, status)
}

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl
  const page = Number(searchParams.get('page') ?? '1')
  const limit = Number(searchParams.get('limit') ?? '10')

  const allBooks = getAllBooks()
  const start = (page - 1) * limit
  const paginatedBooks = allBooks.slice(start, start + limit)

  return jsonResponse({
    data: paginatedBooks,
    pagination: {
      page,
      limit,
      total: allBooks.length,
      totalPages: Math.ceil(allBooks.length / limit),
    },
  })
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const validation = validateBook(body)

    if (!validation.success) {
      return errorResponse(validation.error, 400)
    }

    const newBook = addBook({
      title: body.title.trim(),
      author: body.author.trim(),
      price: body.price,
      isbn: body.isbn?.trim() ?? '',
      publishedAt: body.publishedAt ?? new Date().toISOString().split('T')[0],
    })

    return jsonResponse({ data: newBook }, 201)
  } catch {
    return errorResponse('リクエストの解析に失敗しました', 400)
  }
}
```

**初心者向けとの違い:**
- バリデーション関数を `lib/validation.ts` に分離し再利用可能にする
- ページネーション（`?page=1&limit=10`）をサポート
- レスポンスのヘルパー関数で形式を統一
- `Cache-Control` ヘッダーでキャッシュ制御を明示
- `trim()` で入力値の前後空白を除去
- エラーレスポンスにステータスコードも含める

</details>

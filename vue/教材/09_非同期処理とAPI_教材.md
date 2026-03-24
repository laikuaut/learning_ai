# 第9章：非同期処理とAPI連携

## 9.1 Vue での非同期処理の基本

Web アプリケーションでは、サーバーからデータを取得する非同期処理が不可欠です。Vue 3 では composable を使って非同期処理を整理します。

### 基本的なデータ取得

```vue
<script setup>
import { ref, onMounted } from 'vue'

const users = ref([])
const isLoading = ref(false)
const error = ref(null)

async function fetchUsers() {
  isLoading.value = true
  error.value = null

  try {
    const response = await fetch('https://jsonplaceholder.typicode.com/users')
    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`)
    }
    users.value = await response.json()
  } catch (e) {
    error.value = e.message
  } finally {
    isLoading.value = false
  }
}

// コンポーネントマウント時にデータを取得
onMounted(() => {
  fetchUsers()
})
</script>

<template>
  <!-- ローディング状態 -->
  <div v-if="isLoading" class="loading">
    <p>読み込み中...</p>
  </div>

  <!-- エラー状態 -->
  <div v-else-if="error" class="error">
    <p>エラーが発生しました: {{ error }}</p>
    <button @click="fetchUsers">再試行</button>
  </div>

  <!-- データ表示 -->
  <div v-else>
    <ul>
      <li v-for="user in users" :key="user.id">
        {{ user.name }} ({{ user.email }})
      </li>
    </ul>
  </div>
</template>
```

---

## 9.2 useFetch Composable

データ取得ロジックを再利用可能な composable に切り出します。

```js
// composables/useFetch.js
import { ref, watchEffect, toValue, isRef } from 'vue'

export function useFetch(url, options = {}) {
  const data = ref(null)
  const error = ref(null)
  const isLoading = ref(false)
  const statusCode = ref(null)

  async function execute() {
    isLoading.value = true
    error.value = null
    data.value = null
    statusCode.value = null

    try {
      const resolvedUrl = toValue(url)
      if (!resolvedUrl) return

      const response = await fetch(resolvedUrl, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      })

      statusCode.value = response.status

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status} ${response.statusText}`)
      }

      data.value = await response.json()
    } catch (e) {
      error.value = e.message
    } finally {
      isLoading.value = false
    }
  }

  // url がリアクティブなら変更を自動追跡
  if (isRef(url) || typeof url === 'function') {
    watchEffect(() => {
      execute()
    })
  } else {
    // 静的URLの場合は即座に実行
    execute()
  }

  return {
    data,
    error,
    isLoading,
    statusCode,
    refetch: execute
  }
}
```

### 使用例

```vue
<script setup>
import { ref, computed } from 'vue'
import { useFetch } from '@/composables/useFetch'

// 静的URL
const { data: users, isLoading, error, refetch } = useFetch(
  'https://jsonplaceholder.typicode.com/users'
)

// 動的URL（リアクティブ）
const userId = ref(1)
const userUrl = computed(() =>
  `https://jsonplaceholder.typicode.com/users/${userId.value}`
)
const { data: user, isLoading: userLoading } = useFetch(userUrl)
// userId が変わると自動的に再取得
</script>

<template>
  <div>
    <select v-model.number="userId">
      <option v-for="n in 10" :key="n" :value="n">ユーザー {{ n }}</option>
    </select>

    <div v-if="userLoading">読み込み中...</div>
    <div v-else-if="user">
      <h2>{{ user.name }}</h2>
      <p>{{ user.email }}</p>
    </div>
  </div>
</template>
```

---

## 9.3 CRUD操作の実装

### API クライアント

```js
// services/api.js
const BASE_URL = 'https://jsonplaceholder.typicode.com'

async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`

  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
  }

  const response = await fetch(url, config)

  if (!response.ok) {
    const errorData = await response.json().catch(() => null)
    throw new Error(
      errorData?.message || `HTTP Error: ${response.status}`
    )
  }

  // 204 No Content の場合はnullを返す
  if (response.status === 204) return null

  return response.json()
}

export const api = {
  get: (endpoint) => request(endpoint),
  post: (endpoint, data) => request(endpoint, {
    method: 'POST',
    body: JSON.stringify(data)
  }),
  put: (endpoint, data) => request(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),
  patch: (endpoint, data) => request(endpoint, {
    method: 'PATCH',
    body: JSON.stringify(data)
  }),
  delete: (endpoint) => request(endpoint, {
    method: 'DELETE'
  })
}
```

### CRUD Composable

```js
// composables/usePosts.js
import { ref } from 'vue'
import { api } from '@/services/api'

export function usePosts() {
  const posts = ref([])
  const currentPost = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  // 一覧取得（Read）
  async function fetchPosts() {
    isLoading.value = true
    error.value = null
    try {
      posts.value = await api.get('/posts')
    } catch (e) {
      error.value = e.message
    } finally {
      isLoading.value = false
    }
  }

  // 詳細取得（Read）
  async function fetchPost(id) {
    isLoading.value = true
    error.value = null
    try {
      currentPost.value = await api.get(`/posts/${id}`)
    } catch (e) {
      error.value = e.message
    } finally {
      isLoading.value = false
    }
  }

  // 作成（Create）
  async function createPost(postData) {
    isLoading.value = true
    error.value = null
    try {
      const newPost = await api.post('/posts', postData)
      posts.value.unshift(newPost)  // 先頭に追加
      return newPost
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      isLoading.value = false
    }
  }

  // 更新（Update）
  async function updatePost(id, postData) {
    isLoading.value = true
    error.value = null
    try {
      const updated = await api.put(`/posts/${id}`, postData)
      const index = posts.value.findIndex(p => p.id === id)
      if (index !== -1) {
        posts.value[index] = updated
      }
      return updated
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      isLoading.value = false
    }
  }

  // 削除（Delete）
  async function deletePost(id) {
    isLoading.value = true
    error.value = null
    try {
      await api.delete(`/posts/${id}`)
      posts.value = posts.value.filter(p => p.id !== id)
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      isLoading.value = false
    }
  }

  return {
    posts,
    currentPost,
    isLoading,
    error,
    fetchPosts,
    fetchPost,
    createPost,
    updatePost,
    deletePost
  }
}
```

---

## 9.4 ローディングとエラー状態のUI

### ローディングコンポーネント

```vue
<!-- components/LoadingSpinner.vue -->
<template>
  <div class="loading-spinner" :class="{ overlay: overlay }">
    <div class="spinner"></div>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup>
defineProps({
  message: { type: String, default: '' },
  overlay: { type: Boolean, default: false }
})
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
}

.overlay {
  position: fixed;
  inset: 0;
  background: rgba(255, 255, 255, 0.8);
  z-index: 100;
  justify-content: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e0e0e0;
  border-top: 4px solid #42b883;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
```

### エラーコンポーネント

```vue
<!-- components/ErrorMessage.vue -->
<script setup>
const props = defineProps({
  message: { type: String, required: true },
  retryable: { type: Boolean, default: true }
})

const emit = defineEmits(['retry'])
</script>

<template>
  <div class="error-container" role="alert">
    <div class="error-icon">!</div>
    <p class="error-message">{{ message }}</p>
    <button v-if="retryable" @click="emit('retry')" class="retry-button">
      再試行
    </button>
  </div>
</template>

<style scoped>
.error-container {
  padding: 1rem;
  border: 1px solid #e74c3c;
  border-radius: 8px;
  background: #fdf0ef;
  text-align: center;
}

.error-icon {
  width: 40px;
  height: 40px;
  margin: 0 auto 0.5rem;
  border-radius: 50%;
  background: #e74c3c;
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-message {
  color: #c0392b;
}

.retry-button {
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #e74c3c;
  border-radius: 4px;
  background: white;
  color: #e74c3c;
  cursor: pointer;
}

.retry-button:hover {
  background: #e74c3c;
  color: white;
}
</style>
```

### 統合した使用例

```vue
<script setup>
import { onMounted } from 'vue'
import { usePosts } from '@/composables/usePosts'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ErrorMessage from '@/components/ErrorMessage.vue'

const { posts, isLoading, error, fetchPosts, deletePost } = usePosts()

onMounted(() => fetchPosts())
</script>

<template>
  <div class="posts-page">
    <h1>投稿一覧</h1>

    <LoadingSpinner v-if="isLoading" message="投稿を読み込み中..." />

    <ErrorMessage
      v-else-if="error"
      :message="error"
      @retry="fetchPosts"
    />

    <div v-else-if="posts.length === 0" class="empty">
      <p>投稿がありません</p>
    </div>

    <div v-else class="posts-list">
      <article v-for="post in posts" :key="post.id" class="post-card">
        <h2>{{ post.title }}</h2>
        <p>{{ post.body }}</p>
        <button @click="deletePost(post.id)">削除</button>
      </article>
    </div>
  </div>
</template>
```

---

## 9.5 Suspense（実験的機能）

`<Suspense>` は非同期コンポーネントのローディング状態を宣言的に処理します。

### async setup を持つコンポーネント

```vue
<!-- components/AsyncUserProfile.vue -->
<script setup>
// トップレベル await を使うと、このコンポーネントは非同期になる
const response = await fetch('https://jsonplaceholder.typicode.com/users/1')
const user = await response.json()
</script>

<template>
  <div class="user-profile">
    <h2>{{ user.name }}</h2>
    <p>{{ user.email }}</p>
    <p>{{ user.phone }}</p>
  </div>
</template>
```

### Suspense で囲む

```vue
<!-- App.vue -->
<script setup>
import { ref } from 'vue'
import AsyncUserProfile from './components/AsyncUserProfile.vue'

const showProfile = ref(true)
</script>

<template>
  <button @click="showProfile = !showProfile">
    {{ showProfile ? '非表示' : '表示' }}
  </button>

  <Suspense v-if="showProfile">
    <!-- default スロット: 非同期コンポーネント -->
    <template #default>
      <AsyncUserProfile />
    </template>

    <!-- fallback スロット: ローディング中の表示 -->
    <template #fallback>
      <div class="loading">ユーザー情報を読み込み中...</div>
    </template>
  </Suspense>
</template>
```

### Suspense のイベント

```vue
<template>
  <Suspense
    @pending="onPending"
    @resolve="onResolve"
    @fallback="onFallback"
  >
    <template #default>
      <AsyncComponent />
    </template>
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>

<script setup>
function onPending() {
  console.log('非同期処理開始')
}

function onResolve() {
  console.log('非同期処理完了')
}

function onFallback() {
  console.log('フォールバック表示')
}
</script>
```

> **注意**: Suspense は Vue 3 ではまだ**実験的機能**です。API が変更される可能性があります。

---

## 9.6 axios の紹介

`fetch` の代替として **axios** も広く使われています。

### インストール

```bash
npm install axios
```

### 基本的な使い方

```js
// services/axios.js
import axios from 'axios'

// インスタンスの作成（共通設定）
const apiClient = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
  timeout: 10000,  // 10秒でタイムアウト
  headers: {
    'Content-Type': 'application/json'
  }
})

// リクエストインターセプター（リクエスト前の共通処理）
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// レスポンスインターセプター（レスポンス後の共通処理）
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // 認証エラー → ログインページへ
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default apiClient
```

### fetch vs axios の比較

| 特徴 | `fetch` | `axios` |
|------|---------|---------|
| ブラウザ標準 | はい | いいえ（追加インストール） |
| JSON自動変換 | 手動（`.json()`） | 自動 |
| タイムアウト | AbortController で手動 | `timeout` オプション |
| インターセプター | なし | あり |
| エラーハンドリング | 4xx/5xxでも rejected にならない | 4xx/5xx で rejected |
| リクエストキャンセル | AbortController | CancelToken / AbortController |
| バンドルサイズ | 0KB | 約13KB |

---

## 9.7 デバウンスとキャンセル

### デバウンス（入力の連続送信を防ぐ）

```js
// composables/useDebounce.js
import { ref, watch } from 'vue'

export function useDebounce(source, delay = 300) {
  const debounced = ref(source.value)

  let timeout
  watch(source, (newValue) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      debounced.value = newValue
    }, delay)
  })

  return debounced
}
```

```vue
<script setup>
import { ref, watch } from 'vue'
import { useDebounce } from '@/composables/useDebounce'
import { useFetch } from '@/composables/useFetch'

const searchQuery = ref('')
const debouncedQuery = useDebounce(searchQuery, 500)

// debouncedQuery が変わった時だけ API を呼ぶ
const searchUrl = computed(() =>
  debouncedQuery.value
    ? `https://api.example.com/search?q=${debouncedQuery.value}`
    : null
)

const { data: results, isLoading } = useFetch(searchUrl)
</script>

<template>
  <input v-model="searchQuery" placeholder="検索..." />
  <div v-if="isLoading">検索中...</div>
  <ul v-else-if="results">
    <li v-for="item in results" :key="item.id">{{ item.name }}</li>
  </ul>
</template>
```

### リクエストのキャンセル

```js
// composables/useCancellableFetch.js
import { ref, watchEffect } from 'vue'

export function useCancellableFetch(url) {
  const data = ref(null)
  const error = ref(null)
  const isLoading = ref(false)

  watchEffect((onCleanup) => {
    const resolvedUrl = toValue(url)
    if (!resolvedUrl) return

    const controller = new AbortController()

    isLoading.value = true
    error.value = null

    fetch(resolvedUrl, { signal: controller.signal })
      .then(res => res.json())
      .then(json => {
        data.value = json
      })
      .catch(e => {
        if (e.name !== 'AbortError') {
          error.value = e.message
        }
      })
      .finally(() => {
        isLoading.value = false
      })

    // 次の実行前 or コンポーネント破棄時にキャンセル
    onCleanup(() => {
      controller.abort()
    })
  })

  return { data, error, isLoading }
}
```

---

## 9.8 ページネーション

```vue
<script setup>
import { ref, computed, watch } from 'vue'

const allPosts = ref([])
const currentPage = ref(1)
const perPage = ref(10)
const isLoading = ref(false)
const totalCount = ref(0)

const totalPages = computed(() => Math.ceil(totalCount.value / perPage.value))

const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  return allPosts.value.slice(start, start + perPage.value)
})

// ページ番号の配列を生成
const pageNumbers = computed(() => {
  const pages = []
  const current = currentPage.value
  const total = totalPages.value

  // 最大5ページ分のボタンを表示
  let start = Math.max(1, current - 2)
  let end = Math.min(total, start + 4)
  start = Math.max(1, end - 4)

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

async function fetchAllPosts() {
  isLoading.value = true
  try {
    const response = await fetch('https://jsonplaceholder.typicode.com/posts')
    allPosts.value = await response.json()
    totalCount.value = allPosts.value.length
  } finally {
    isLoading.value = false
  }
}

function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

fetchAllPosts()
</script>

<template>
  <div>
    <div v-if="isLoading">読み込み中...</div>

    <div v-else>
      <article v-for="post in paginatedPosts" :key="post.id">
        <h3>{{ post.title }}</h3>
        <p>{{ post.body }}</p>
      </article>

      <!-- ページネーションUI -->
      <nav class="pagination">
        <button @click="goToPage(1)" :disabled="currentPage === 1">
          最初
        </button>
        <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">
          前へ
        </button>

        <button
          v-for="page in pageNumbers"
          :key="page"
          @click="goToPage(page)"
          :class="{ active: page === currentPage }"
        >
          {{ page }}
        </button>

        <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">
          次へ
        </button>
        <button @click="goToPage(totalPages)" :disabled="currentPage === totalPages">
          最後
        </button>
      </nav>

      <p>{{ currentPage }} / {{ totalPages }} ページ（全{{ totalCount }}件）</p>
    </div>
  </div>
</template>
```

---

## 9.9 本章のまとめ

| 概念 | 説明 |
|------|------|
| `fetch` | ブラウザ標準の HTTP リクエスト API |
| `useFetch` composable | データ取得ロジックの再利用 |
| ローディング状態 | `isLoading` で UI を切り替え |
| エラー状態 | `error` でエラーメッセージを表示 |
| `Suspense` | 非同期コンポーネントの宣言的なローディング処理 |
| `axios` | 高機能な HTTP クライアントライブラリ |
| デバウンス | 連続した入力の API 呼び出しを制御 |
| AbortController | リクエストのキャンセル |

### 次章予告

第10章では **実践パターン** を学びます。provide/inject、teleport、トランジション/アニメーション、動的コンポーネント、TypeScript との統合など、実務で必要な高度なテクニックをカバーします。

# 第8章：状態管理 Pinia

## 8.1 状態管理とは

アプリケーションが大きくなると、複数のコンポーネント間でデータを共有する必要が出てきます。props/emits だけでは管理が複雑になるため、**グローバルな状態管理**ライブラリを使います。

### なぜ Pinia なのか

Pinia は Vue.js の**公式状態管理ライブラリ**です（Vuex の後継）。

| 特徴 | 説明 |
|------|------|
| 軽量 | 約1KB（gzip圧縮後） |
| TypeScript 完全対応 | 型推論が優れている |
| Composition API 対応 | `setup()` スタイルで定義可能 |
| DevTools 連携 | Vue DevTools で状態を確認・変更可能 |
| mutation 不要 | Vuex の mutation が不要でシンプル |
| SSR 対応 | サーバーサイドレンダリング対応 |

### インストール

```bash
npm install pinia
```

### 初期設定

```js
// src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)  // Pinia をプラグインとして登録
app.mount('#app')
```

---

## 8.2 ストアの定義

### Options Store（Options API スタイル）

```js
// stores/counter.js
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  // state: リアクティブなデータ（data に相当）
  state: () => ({
    count: 0,
    name: 'カウンター'
  }),

  // getters: 算出プロパティ（computed に相当）
  getters: {
    doubled: (state) => state.count * 2,
    // 他の getter を使う
    quadrupled() {
      return this.doubled * 2
    }
  },

  // actions: メソッド（methods に相当）
  actions: {
    increment() {
      this.count++  // this で state にアクセス
    },
    decrement() {
      this.count--
    },
    async fetchCount() {
      const response = await fetch('/api/count')
      const data = await response.json()
      this.count = data.count
    }
  }
})
```

### Setup Store（Composition API スタイル — 推奨）

```js
// stores/counter.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  // ref() → state
  const count = ref(0)
  const name = ref('カウンター')

  // computed() → getters
  const doubled = computed(() => count.value * 2)
  const quadrupled = computed(() => doubled.value * 2)

  // function → actions
  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  async function fetchCount() {
    const response = await fetch('/api/count')
    const data = await response.json()
    count.value = data.count
  }

  // 外部に公開するものを return
  return {
    count,
    name,
    doubled,
    quadrupled,
    increment,
    decrement,
    fetchCount
  }
})
```

---

## 8.3 ストアの使用

### コンポーネントからの利用

```vue
<script setup>
import { useCounterStore } from '@/stores/counter'
import { storeToRefs } from 'pinia'

// ストアインスタンスを取得
const counterStore = useCounterStore()

// ✅ storeToRefs でリアクティビティを維持したまま分割代入
const { count, name, doubled } = storeToRefs(counterStore)

// actions は直接分割代入してOK（リアクティブではないため）
const { increment, decrement } = counterStore
</script>

<template>
  <div>
    <h2>{{ name }}</h2>
    <p>カウント: {{ count }}</p>
    <p>2倍: {{ doubled }}</p>
    <button @click="increment">+1</button>
    <button @click="decrement">-1</button>

    <!-- ストアに直接アクセスも可能 -->
    <button @click="counterStore.count = 0">リセット</button>
  </div>
</template>
```

### state の変更方法

```js
const store = useCounterStore()

// 方法1: 直接変更
store.count++

// 方法2: $patch（複数のプロパティを一括変更）
store.$patch({
  count: 10,
  name: '新しいカウンター'
})

// 方法3: $patch に関数を渡す（配列操作などに便利）
store.$patch((state) => {
  state.count += 10
  state.name = `カウンター (${state.count})`
})

// 方法4: action を呼ぶ（推奨: ロジックをストアに集約）
store.increment()

// state 全体をリセット
store.$reset()
```

---

## 8.4 実践的なストア設計

### ユーザー認証ストア

```js
// stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const isLoading = ref(false)
  const error = ref(null)

  // getters
  const isAuthenticated = computed(() => !!token.value)
  const userName = computed(() => user.value?.name || 'ゲスト')
  const userRole = computed(() => user.value?.role || 'guest')
  const isAdmin = computed(() => userRole.value === 'admin')

  // actions
  async function login(email, password) {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })

      if (!response.ok) throw new Error('ログインに失敗しました')

      const data = await response.json()
      token.value = data.token
      user.value = data.user
      localStorage.setItem('token', data.token)
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      isLoading.value = false
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  async function fetchUser() {
    if (!token.value) return

    try {
      const response = await fetch('/api/me', {
        headers: { Authorization: `Bearer ${token.value}` }
      })
      if (response.ok) {
        user.value = await response.json()
      } else {
        logout()
      }
    } catch {
      logout()
    }
  }

  return {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
    userName,
    userRole,
    isAdmin,
    login,
    logout,
    fetchUser
  }
})
```

### Todo リストストア

```js
// stores/todos.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useTodoStore = defineStore('todos', () => {
  const todos = ref([])
  const filter = ref('all')  // 'all' | 'active' | 'completed'
  let nextId = 1

  // getters
  const filteredTodos = computed(() => {
    switch (filter.value) {
      case 'active':
        return todos.value.filter(t => !t.done)
      case 'completed':
        return todos.value.filter(t => t.done)
      default:
        return todos.value
    }
  })

  const totalCount = computed(() => todos.value.length)
  const activeCount = computed(() => todos.value.filter(t => !t.done).length)
  const completedCount = computed(() => todos.value.filter(t => t.done).length)
  const allCompleted = computed(() => todos.value.length > 0 && activeCount.value === 0)

  // actions
  function addTodo(text) {
    todos.value.push({
      id: nextId++,
      text,
      done: false,
      createdAt: new Date()
    })
  }

  function removeTodo(id) {
    todos.value = todos.value.filter(t => t.id !== id)
  }

  function toggleTodo(id) {
    const todo = todos.value.find(t => t.id === id)
    if (todo) {
      todo.done = !todo.done
    }
  }

  function updateTodo(id, text) {
    const todo = todos.value.find(t => t.id === id)
    if (todo) {
      todo.text = text
    }
  }

  function clearCompleted() {
    todos.value = todos.value.filter(t => !t.done)
  }

  function toggleAll() {
    const allDone = allCompleted.value
    todos.value.forEach(t => t.done = !allDone)
  }

  return {
    todos,
    filter,
    filteredTodos,
    totalCount,
    activeCount,
    completedCount,
    allCompleted,
    addTodo,
    removeTodo,
    toggleTodo,
    updateTodo,
    clearCompleted,
    toggleAll
  }
})
```

---

## 8.5 ストアの購読（Subscribe）

ストアの変更を監視できます。

```js
const store = useCounterStore()

// state の変更を購読
const unsubscribe = store.$subscribe((mutation, state) => {
  console.log('変更タイプ:', mutation.type)
  // 'direct' | 'patch object' | 'patch function'
  console.log('ストアID:', mutation.storeId)
  console.log('新しい state:', state)

  // ローカルストレージに自動保存
  localStorage.setItem('counter', JSON.stringify(state))
})

// 購読を解除
unsubscribe()

// action の実行を購読
store.$onAction(({ name, args, after, onError }) => {
  console.log(`Action "${name}" が実行された。引数:`, args)

  after((result) => {
    console.log(`Action "${name}" が完了。結果:`, result)
  })

  onError((error) => {
    console.error(`Action "${name}" でエラー:`, error)
  })
})
```

---

## 8.6 ストアの合成

ストア同士を組み合わせて使えます。

```js
// stores/cart.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  const authStore = useAuthStore()  // 他のストアを利用

  const totalItems = computed(() =>
    items.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  const totalPrice = computed(() =>
    items.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
  )

  // 認証ストアのユーザー情報を活用
  const discount = computed(() => {
    if (authStore.userRole === 'premium') return 0.1
    if (authStore.userRole === 'vip') return 0.2
    return 0
  })

  const finalPrice = computed(() => {
    return Math.floor(totalPrice.value * (1 - discount.value))
  })

  function addItem(product, quantity = 1) {
    const existing = items.value.find(i => i.id === product.id)
    if (existing) {
      existing.quantity += quantity
    } else {
      items.value.push({ ...product, quantity })
    }
  }

  function removeItem(productId) {
    items.value = items.value.filter(i => i.id !== productId)
  }

  async function checkout() {
    if (!authStore.isAuthenticated) {
      throw new Error('ログインが必要です')
    }

    const response = await fetch('/api/checkout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authStore.token}`
      },
      body: JSON.stringify({ items: items.value })
    })

    if (response.ok) {
      items.value = []  // カートをクリア
    }
  }

  return {
    items,
    totalItems,
    totalPrice,
    discount,
    finalPrice,
    addItem,
    removeItem,
    checkout
  }
})
```

---

## 8.7 Pinia プラグイン

Pinia の機能を拡張するプラグインを作成できます。

### ローカルストレージ永続化プラグイン

```js
// plugins/piniaLocalStorage.js
export function piniaLocalStoragePlugin({ store }) {
  // ストアの初期化時にローカルストレージから復元
  const saved = localStorage.getItem(`pinia-${store.$id}`)
  if (saved) {
    store.$patch(JSON.parse(saved))
  }

  // 変更時に自動保存
  store.$subscribe((mutation, state) => {
    localStorage.setItem(`pinia-${store.$id}`, JSON.stringify(state))
  })
}
```

```js
// main.js
import { createPinia } from 'pinia'
import { piniaLocalStoragePlugin } from './plugins/piniaLocalStorage'

const pinia = createPinia()
pinia.use(piniaLocalStoragePlugin)
```

### Vue DevTools

Vue DevTools をインストールすると、Pinia のストアを視覚的に確認・操作できます。

```
Chrome: Vue.js devtools
Firefox: Vue.js devtools

機能:
- ストアの state をリアルタイムで確認
- state を直接編集
- action の実行履歴
- タイムトラベルデバッグ
```

---

## 8.8 ストア設計のベストプラクティス

### ファイル構成

```
src/stores/
├── auth.js       # 認証
├── cart.js       # カート
├── todos.js      # Todoリスト
├── ui.js         # UIの状態（モーダル、トースト等）
└── index.js      # バレルエクスポート
```

### ガイドライン

1. **機能ごとにストアを分割** — 1ストア1関心事
2. **Setup Store を使う** — Composition API との一貫性
3. **storeToRefs で分割代入** — リアクティビティの維持
4. **ビジネスロジックは action に** — コンポーネントを薄く保つ
5. **API呼び出しはストアの action で** — データフローを一元管理
6. **state は直接変更せず action 経由が望ましい** — 変更箇所の追跡

---

## 8.9 本章のまとめ

| 概念 | 説明 |
|------|------|
| `defineStore` | ストアの定義 |
| `state` (ref) | リアクティブなデータ |
| `getters` (computed) | 派生データ |
| `actions` (function) | 状態を変更するメソッド |
| `storeToRefs` | リアクティビティを維持して分割代入 |
| `$patch` | state の一括変更 |
| `$subscribe` | state 変更の監視 |
| `$onAction` | action 実行の監視 |
| `$reset` | state の初期化 |

### 次章予告

第9章では **非同期処理と API 連携** を学びます。composable での fetch 管理、ローディング/エラー状態の処理、Suspense の使い方を理解します。

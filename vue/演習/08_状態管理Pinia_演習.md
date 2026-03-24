# 第8章 演習：状態管理 Pinia

> 対応教材: `教材/08_状態管理Pinia_教材.md`
>
> この演習では、Pinia を使ったグローバル状態管理、
> ストアの定義方法、コンポーネント間でのデータ共有を練習します。

---

## 演習8-1：はじめてのストア定義（基本）

### 問題

Pinia を使って、カウンターストアを作成してください。

**要件:**
1. `useCounterStore` を Composition API スタイル（Setup Store）で定義
2. `count` state、`doubled` getter、`increment`/`decrement`/`reset` action
3. 2つのコンポーネントから同じストアを参照して、値が共有されることを確認

<details>
<summary>ヒント</summary>

Setup Store は `defineStore` の第2引数に関数を渡すスタイルです。

```js
export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubled = computed(() => count.value * 2)
  function increment() { count.value++ }
  return { count, doubled, increment }
})
```

</details>

<details>
<summary>解答例</summary>

```js
// stores/counter.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// ========================================
// Setup Store（Composition API スタイル）
// ref → state、computed → getters、function → actions
// ========================================
export const useCounterStore = defineStore('counter', () => {
  // state
  const count = ref(0)

  // getters（算出プロパティ）
  const doubled = computed(() => count.value * 2)
  const isPositive = computed(() => count.value > 0)

  // actions（メソッド）
  function increment() {
    count.value++
  }

  function decrement() {
    if (count.value > 0) count.value--
  }

  function reset() {
    count.value = 0
  }

  function incrementBy(amount) {
    count.value += amount
  }

  // 公開する値を return
  return { count, doubled, isPositive, increment, decrement, reset, incrementBy }
})
```

```vue
<!-- CounterDisplay.vue -->
<script setup>
import { useCounterStore } from '@/stores/counter'

// ストアのインスタンスを取得
// 複数のコンポーネントで同じストアを参照すると、値が共有される
const counter = useCounterStore()
</script>

<template>
  <div style="padding: 16px; background: #e8f5e9; border-radius: 8px;">
    <h3>カウンター表示</h3>
    <p>カウント: {{ counter.count }}</p>
    <p>2倍: {{ counter.doubled }}</p>
  </div>
</template>
```

```vue
<!-- CounterControls.vue -->
<script setup>
import { useCounterStore } from '@/stores/counter'

const counter = useCounterStore()
</script>

<template>
  <div style="padding: 16px; background: #e3f2fd; border-radius: 8px;">
    <h3>カウンター操作</h3>
    <button @click="counter.increment()">+1</button>
    <button @click="counter.decrement()">-1</button>
    <button @click="counter.incrementBy(10)">+10</button>
    <button @click="counter.reset()">リセット</button>
  </div>
</template>
```

**ポイント:**
- 異なるコンポーネントで `useCounterStore()` を呼んでも、同じストアのインスタンスが返されます
- Setup Store は Composition API の知識がそのまま使えるので、Vue 3 では推奨されるスタイルです

</details>

---

## 演習8-2：TODOストアを作ろう（基本）

### 問題

Pinia でTODO管理ストアを作成し、複数コンポーネントからCRUD操作を行ってください。

**要件:**
1. Todo の追加、削除、完了切替、フィルタリング
2. `activeCount` / `completedCount` の getter
3. `clearCompleted` action
4. TodoForm コンポーネントと TodoList コンポーネントで分離

<details>
<summary>ヒント</summary>

- ストアにTodoの配列と操作関数を定義します
- `storeToRefs` でリアクティビティを保ったまま分割代入できます

```js
import { storeToRefs } from 'pinia'
const store = useTodoStore()
const { todos, activeCount } = storeToRefs(store)
```

</details>

<details>
<summary>解答例</summary>

```js
// stores/todo.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useTodoStore = defineStore('todo', () => {
  const todos = ref([
    { id: 1, text: 'Pinia を学ぶ', done: false },
    { id: 2, text: 'ストアを作る', done: false },
  ])
  const filter = ref('all') // 'all' | 'active' | 'done'

  // getters
  const filteredTodos = computed(() => {
    if (filter.value === 'active') return todos.value.filter(t => !t.done)
    if (filter.value === 'done') return todos.value.filter(t => t.done)
    return todos.value
  })

  const activeCount = computed(() => todos.value.filter(t => !t.done).length)
  const completedCount = computed(() => todos.value.filter(t => t.done).length)

  // actions
  function addTodo(text) {
    if (!text.trim()) return
    todos.value.push({ id: Date.now(), text: text.trim(), done: false })
  }

  function toggleTodo(id) {
    const todo = todos.value.find(t => t.id === id)
    if (todo) todo.done = !todo.done
  }

  function removeTodo(id) {
    todos.value = todos.value.filter(t => t.id !== id)
  }

  function clearCompleted() {
    todos.value = todos.value.filter(t => !t.done)
  }

  function setFilter(f) {
    filter.value = f
  }

  return {
    todos, filter, filteredTodos, activeCount, completedCount,
    addTodo, toggleTodo, removeTodo, clearCompleted, setFilter
  }
})
```

```vue
<!-- TodoForm.vue -->
<script setup>
import { ref } from 'vue'
import { useTodoStore } from '@/stores/todo'

const store = useTodoStore()
const input = ref('')

function submit() {
  store.addTodo(input.value)
  input.value = ''
}
</script>

<template>
  <div style="display: flex; gap: 8px; margin-bottom: 16px;">
    <input v-model="input" @keyup.enter="submit" placeholder="新しいタスク..." style="flex: 1; padding: 8px;" />
    <button @click="submit">追加</button>
  </div>
</template>
```

```vue
<!-- TodoList.vue -->
<script setup>
import { useTodoStore } from '@/stores/todo'
import { storeToRefs } from 'pinia'

const store = useTodoStore()
// storeToRefs でリアクティビティを保ったまま分割代入
const { filteredTodos, activeCount, filter } = storeToRefs(store)
</script>

<template>
  <div>
    <div style="display: flex; gap: 8px; margin-bottom: 12px;">
      <button v-for="f in ['all', 'active', 'done']" :key="f"
        @click="store.setFilter(f)"
        :style="{ padding: '4px 12px', borderRadius: '12px', border: 'none', cursor: 'pointer', background: filter === f ? '#5c6bc0' : '#eee', color: filter === f ? 'white' : '#666' }">
        {{ f === 'all' ? 'すべて' : f === 'active' ? '未完了' : '完了' }}
      </button>
    </div>

    <p style="color: #888;">残り {{ activeCount }} 件</p>

    <div v-for="todo in filteredTodos" :key="todo.id" style="display: flex; align-items: center; gap: 8px; padding: 8px; border-bottom: 1px solid #eee;">
      <input type="checkbox" :checked="todo.done" @change="store.toggleTodo(todo.id)" />
      <span :style="{ flex: 1, textDecoration: todo.done ? 'line-through' : 'none' }">{{ todo.text }}</span>
      <button @click="store.removeTodo(todo.id)" style="color: red; background: none; border: none; cursor: pointer;">削除</button>
    </div>

    <button v-if="store.completedCount > 0" @click="store.clearCompleted()" style="margin-top: 12px; color: #888; background: none; border: 1px solid #ddd; padding: 4px 12px; border-radius: 6px; cursor: pointer;">
      完了済みを削除
    </button>
  </div>
</template>
```

**ポイント:**
- `storeToRefs` を使わずに `const { todos } = store` とすると、リアクティビティが失われます
- メソッド（actions）は `storeToRefs` を使わず直接 `store.addTodo()` と呼べます

</details>

---

## 演習8-3：ストア間の連携（応用）

### 問題

ショッピングカートアプリで、商品ストアとカートストアを分けて連携させてください。

**要件:**
1. `useProductStore` — 商品一覧の管理
2. `useCartStore` — カート内商品の管理、合計金額の算出
3. カートストアが商品ストアを参照して商品情報を取得
4. 在庫管理（カートに追加すると在庫が減る）

<details>
<summary>ヒント</summary>

- ストアの中で別のストアを呼び出せます
- `const productStore = useProductStore()` をアクション内で使います

</details>

<details>
<summary>解答例</summary>

```js
// stores/products.js
export const useProductStore = defineStore('products', () => {
  const products = ref([
    { id: 1, name: 'Vue.js入門書', price: 2980, stock: 5 },
    { id: 2, name: 'TypeScriptガイド', price: 3480, stock: 3 },
    { id: 3, name: 'Pinia実践', price: 2500, stock: 10 },
  ])

  function decreaseStock(productId) {
    const product = products.value.find(p => p.id === productId)
    if (product && product.stock > 0) {
      product.stock--
      return true
    }
    return false
  }

  function increaseStock(productId) {
    const product = products.value.find(p => p.id === productId)
    if (product) product.stock++
  }

  return { products, decreaseStock, increaseStock }
})
```

```js
// stores/cart.js
export const useCartStore = defineStore('cart', () => {
  const items = ref([]) // { productId, quantity }

  const totalPrice = computed(() => {
    // 別のストアを参照して商品情報を取得
    const productStore = useProductStore()
    return items.value.reduce((sum, item) => {
      const product = productStore.products.find(p => p.id === item.productId)
      return sum + (product ? product.price * item.quantity : 0)
    }, 0)
  })

  const totalItems = computed(() => {
    return items.value.reduce((sum, item) => sum + item.quantity, 0)
  })

  function addToCart(productId) {
    const productStore = useProductStore()
    // 在庫チェック
    if (!productStore.decreaseStock(productId)) return false

    const existing = items.value.find(i => i.productId === productId)
    if (existing) {
      existing.quantity++
    } else {
      items.value.push({ productId, quantity: 1 })
    }
    return true
  }

  function removeFromCart(productId) {
    const productStore = useProductStore()
    const item = items.value.find(i => i.productId === productId)
    if (!item) return

    // 在庫を戻す
    for (let i = 0; i < item.quantity; i++) {
      productStore.increaseStock(productId)
    }
    items.value = items.value.filter(i => i.productId !== productId)
  }

  return { items, totalPrice, totalItems, addToCart, removeFromCart }
})
```

**ポイント:**
- ストアの中で他のストアを使うことで、責務を分離しつつ連携できます
- getters（computed）内で他のストアを参照すると、そのストアの値が変わった時に自動で再計算されます
- 循環参照に注意：ストアAがストアBを参照し、ストアBがストアAを参照するとエラーになる場合があります

</details>

---

## 演習8-4：ストアの永続化（チャレンジ）

### 問題

ストアの状態を `localStorage` に保存し、ページをリロードしても状態が復元されるようにしてください。

**要件:**
1. ストアの状態変更を `watch` で監視し、`localStorage` に保存
2. ストア初期化時に `localStorage` から復元
3. 汎用的な `usePersistedStore` composable として実装

<details>
<summary>ヒント</summary>

- `watch` にオプション `{ deep: true }` を指定するとオブジェクト内部の変更も検知します
- Pinia の `$subscribe` メソッドでストアの変更を監視することもできます

</details>

<details>
<summary>解答例</summary>

```js
// composables/usePersistedState.js
import { watch } from 'vue'

// ストアの state を localStorage に永続化する composable
export function usePersistedState(store, key) {
  // localStorage から復元
  const saved = localStorage.getItem(key)
  if (saved) {
    try {
      store.$patch(JSON.parse(saved))
    } catch (e) {
      console.warn('Failed to restore state:', e)
    }
  }

  // $subscribe でストアの変更を監視して保存
  store.$subscribe((mutation, state) => {
    localStorage.setItem(key, JSON.stringify(state))
  })
}
```

```js
// stores/settings.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSettingsStore = defineStore('settings', () => {
  const theme = ref('light')
  const language = ref('ja')
  const fontSize = ref(16)

  function setTheme(t) { theme.value = t }
  function setLanguage(l) { language.value = l }
  function setFontSize(s) { fontSize.value = s }

  return { theme, language, fontSize, setTheme, setLanguage, setFontSize }
})
```

```vue
<!-- App.vue で永続化を有効にする -->
<script setup>
import { useSettingsStore } from '@/stores/settings'
import { usePersistedState } from '@/composables/usePersistedState'

const settings = useSettingsStore()
// localStorage のキー 'app-settings' に保存・復元
usePersistedState(settings, 'app-settings')
</script>
```

**ポイント:**
- `$subscribe` はストアの変更を監視するPinia組み込みのメソッドです
- `$patch` はストアの状態を部分的に更新するメソッドです
- 実務ではプラグイン（`pinia-plugin-persistedstate`）がよく使われますが、仕組みを理解することが大切です

</details>

---

## まとめ

| 演習 | レベル | 学習ポイント |
|------|--------|-------------|
| 8-1 | 基本 | Setup Store の定義、state / getters / actions |
| 8-2 | 基本 | CRUD ストア、storeToRefs |
| 8-3 | 応用 | ストア間の連携、責務分離 |
| 8-4 | チャレンジ | ストアの永続化、$subscribe |

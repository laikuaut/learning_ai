# 第5章：Composition API

## 5.1 Composition API の概要

Composition API は Vue 3 で導入された、コンポーネントのロジックを**関数ベース**で記述する仕組みです。

### Options API vs Composition API

```vue
<!-- Options API（Vue 2 スタイル） -->
<script>
export default {
  data() {
    return {
      count: 0,
      message: ''
    }
  },
  computed: {
    doubled() {
      return this.count * 2
    }
  },
  methods: {
    increment() {
      this.count++
    }
  },
  mounted() {
    console.log('マウントされた')
  }
}
</script>
```

```vue
<!-- Composition API -->
<script setup>
import { ref, computed, onMounted } from 'vue'

const count = ref(0)
const message = ref('')

const doubled = computed(() => count.value * 2)

function increment() {
  count.value++
}

onMounted(() => {
  console.log('マウントされた')
})
</script>
```

### Composition API のメリット

1. **関連するロジックをまとめられる** — 機能ごとにコードをグループ化
2. **ロジックの再利用** — composable として関数に切り出せる
3. **TypeScript との親和性** — 型推論が効きやすい
4. **テスタビリティ** — 関数単位でテスト可能

---

## 5.2 setup() 関数

`<script setup>` の裏側にある `setup()` 関数を理解しましょう。

### setup() の基本

```vue
<script>
import { ref, computed } from 'vue'

export default {
  props: {
    initialCount: {
      type: Number,
      default: 0
    }
  },
  emits: ['update'],
  setup(props, context) {
    // props: リアクティブなプロパティ（読み取り専用）
    const count = ref(props.initialCount)

    // context.emit: イベントの発火
    function increment() {
      count.value++
      context.emit('update', count.value)
    }

    // context.attrs: 渡された属性（propsに定義されていないもの）
    console.log(context.attrs)

    // context.slots: スロット
    console.log(context.slots)

    // context.expose: 外部に公開するプロパティ/メソッド
    context.expose({ count, increment })

    // テンプレートで使用する値を return
    return {
      count,
      increment
    }
  }
}
</script>

<template>
  <button @click="increment">{{ count }}</button>
</template>
```

### `<script setup>` — 推奨される記法

`<script setup>` は `setup()` の糖衣構文で、より簡潔に書けます。

```vue
<script setup>
import { ref } from 'vue'

// トップレベルの変数・関数はテンプレートで自動的に使える
// return は不要

const count = ref(0)

function increment() {
  count.value++
}

// インポートしたコンポーネントも自動登録
import MyComponent from './MyComponent.vue'
</script>

<template>
  <button @click="increment">{{ count }}</button>
  <MyComponent />
</template>
```

### `<script setup>` での props / emits

```vue
<script setup>
// defineProps と defineEmits はマクロ（import 不要）
const props = defineProps({
  title: String,
  count: Number
})

const emit = defineEmits(['update', 'close'])

// 使用
console.log(props.title)
emit('update', 42)
</script>
```

### defineExpose — 外部への公開

`<script setup>` のコンポーネントは、デフォルトで外部からアクセスできません。`defineExpose` で明示的に公開します。

```vue
<!-- ChildComponent.vue -->
<script setup>
import { ref } from 'vue'

const count = ref(0)
const message = ref('hello')

function reset() {
  count.value = 0
}

// 外部（親コンポーネント）に公開するものだけ指定
defineExpose({
  count,
  reset
})
// message は外部からアクセスできない
</script>
```

```vue
<!-- ParentComponent.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import ChildComponent from './ChildComponent.vue'

const childRef = ref(null)

onMounted(() => {
  console.log(childRef.value.count)  // 0
  childRef.value.reset()             // メソッド呼び出し
  // childRef.value.message          // undefined（公開されていない）
})
</script>

<template>
  <ChildComponent ref="childRef" />
</template>
```

---

## 5.3 ライフサイクルフック

コンポーネントの生成から破棄までの各段階で処理を実行できます。

### ライフサイクルの流れ

```
setup()
  │
  ↓
onBeforeMount    ── DOM描画前
  │
  ↓
onMounted        ── DOM描画後 ★よく使う
  │
  ↓（データ変更時）
onBeforeUpdate   ── DOM更新前
  │
  ↓
onUpdated        ── DOM更新後
  │
  ↓（コンポーネント破棄時）
onBeforeUnmount  ── 破棄前 ★クリーンアップ
  │
  ↓
onUnmounted      ── 破棄後
```

### 使用例

```vue
<script setup>
import {
  ref,
  onBeforeMount,
  onMounted,
  onBeforeUpdate,
  onUpdated,
  onBeforeUnmount,
  onUnmounted
} from 'vue'

const count = ref(0)

// ----- マウント系 -----

onBeforeMount(() => {
  // DOM描画前に実行
  // DOM要素にはまだアクセスできない
  console.log('beforeMount: DOMはまだない')
})

onMounted(() => {
  // DOM描画後に実行（最もよく使う）
  // DOM要素にアクセスできる
  console.log('mounted: DOMが利用可能')

  // タイマーの開始
  const timer = setInterval(() => {
    count.value++
  }, 1000)

  // イベントリスナーの登録
  window.addEventListener('resize', handleResize)

  // API呼び出し
  fetchData()
})

// ----- 更新系 -----

onBeforeUpdate(() => {
  console.log('beforeUpdate: DOM更新前')
})

onUpdated(() => {
  console.log('updated: DOM更新後')
  // 注意: ここでデータを変更すると無限ループになる可能性がある
})

// ----- アンマウント系 -----

onBeforeUnmount(() => {
  console.log('beforeUnmount: 破棄前')
})

onUnmounted(() => {
  // クリーンアップ処理（メモリリーク防止）
  console.log('unmounted: 破棄後')

  // タイマーの停止
  clearInterval(timer)

  // イベントリスナーの解除
  window.removeEventListener('resize', handleResize)
})

function handleResize() {
  console.log('リサイズ:', window.innerWidth)
}

async function fetchData() {
  // APIからデータを取得
}
</script>
```

### 実践的なパターン：マウント/アンマウント

```vue
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// ----- タイマー管理 -----
const seconds = ref(0)
let timer = null

onMounted(() => {
  timer = setInterval(() => {
    seconds.value++
  }, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

// ----- ウィンドウサイズ監視 -----
const windowWidth = ref(0)

function updateWidth() {
  windowWidth.value = window.innerWidth
}

onMounted(() => {
  windowWidth.value = window.innerWidth
  window.addEventListener('resize', updateWidth)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateWidth)
})

// ----- IntersectionObserver -----
const targetEl = ref(null)
const isVisible = ref(false)
let observer = null

onMounted(() => {
  observer = new IntersectionObserver(([entry]) => {
    isVisible.value = entry.isIntersecting
  })
  if (targetEl.value) {
    observer.observe(targetEl.value)
  }
})

onUnmounted(() => {
  if (observer) observer.disconnect()
})
</script>

<template>
  <p>経過時間: {{ seconds }}秒</p>
  <p>ウィンドウ幅: {{ windowWidth }}px</p>
  <div ref="targetEl">
    {{ isVisible ? '画面内' : '画面外' }}
  </div>
</template>
```

---

## 5.4 Composables — ロジックの再利用

Composable（コンポーザブル）は、Composition API を使った**再利用可能な関数**です。`use` プレフィックスを付ける慣習があります。

### 基本的な composable

```js
// composables/useCounter.js
import { ref, computed } from 'vue'

export function useCounter(initialValue = 0) {
  const count = ref(initialValue)

  const doubled = computed(() => count.value * 2)
  const isPositive = computed(() => count.value > 0)

  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  function reset() {
    count.value = initialValue
  }

  // リアクティブな値と関数を返す
  return {
    count,
    doubled,
    isPositive,
    increment,
    decrement,
    reset
  }
}
```

```vue
<!-- 使用側 -->
<script setup>
import { useCounter } from '@/composables/useCounter'

// 複数のインスタンスを作れる
const { count, doubled, increment, decrement, reset } = useCounter(10)
const { count: count2, increment: increment2 } = useCounter(0)
</script>

<template>
  <p>カウンター1: {{ count }}（2倍: {{ doubled }}）</p>
  <button @click="increment">+1</button>
  <button @click="decrement">-1</button>
  <button @click="reset">リセット</button>

  <p>カウンター2: {{ count2 }}</p>
  <button @click="increment2">+1</button>
</template>
```

### 実践的な composable：マウス位置

```js
// composables/useMouse.js
import { ref, onMounted, onUnmounted } from 'vue'

export function useMouse() {
  const x = ref(0)
  const y = ref(0)

  function update(event) {
    x.value = event.clientX
    y.value = event.clientY
  }

  // ライフサイクルフックも composable 内で使える
  onMounted(() => window.addEventListener('mousemove', update))
  onUnmounted(() => window.removeEventListener('mousemove', update))

  return { x, y }
}
```

### 実践的な composable：ローカルストレージ

```js
// composables/useLocalStorage.js
import { ref, watch } from 'vue'

export function useLocalStorage(key, defaultValue) {
  // ローカルストレージから初期値を取得
  const stored = localStorage.getItem(key)
  const data = ref(stored ? JSON.parse(stored) : defaultValue)

  // 値が変更されたらローカルストレージに保存
  watch(data, (newValue) => {
    localStorage.setItem(key, JSON.stringify(newValue))
  }, { deep: true })

  return data
}
```

```vue
<script setup>
import { useLocalStorage } from '@/composables/useLocalStorage'

// ブラウザを閉じても値が保持される
const theme = useLocalStorage('theme', 'light')
const settings = useLocalStorage('settings', {
  fontSize: 14,
  language: 'ja'
})
</script>
```

### 実践的な composable：フェッチ

```js
// composables/useFetch.js
import { ref, watchEffect, toValue } from 'vue'

export function useFetch(url) {
  const data = ref(null)
  const error = ref(null)
  const isLoading = ref(false)

  async function fetchData() {
    isLoading.value = true
    data.value = null
    error.value = null

    try {
      const response = await fetch(toValue(url))
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      data.value = await response.json()
    } catch (e) {
      error.value = e.message
    } finally {
      isLoading.value = false
    }
  }

  // url がリアクティブなら自動追跡
  watchEffect(() => {
    fetchData()
  })

  return { data, error, isLoading, refetch: fetchData }
}
```

### composable の組み合わせ

```js
// composables/useUserSearch.js
import { ref, computed } from 'vue'
import { useFetch } from './useFetch'
import { useDebounce } from './useDebounce'

export function useUserSearch() {
  const searchQuery = ref('')
  const debouncedQuery = useDebounce(searchQuery, 300)

  const url = computed(() =>
    debouncedQuery.value
      ? `/api/users?q=${debouncedQuery.value}`
      : null
  )

  const { data: users, isLoading, error } = useFetch(url)

  return {
    searchQuery,
    users,
    isLoading,
    error
  }
}
```

---

## 5.5 Composable のベストプラクティス

### ファイル構成

```
src/
├── composables/
│   ├── useCounter.js
│   ├── useFetch.js
│   ├── useLocalStorage.js
│   ├── useMouse.js
│   ├── useDebounce.js
│   └── index.js          # バレルエクスポート
```

```js
// composables/index.js
export { useCounter } from './useCounter'
export { useFetch } from './useFetch'
export { useLocalStorage } from './useLocalStorage'
export { useMouse } from './useMouse'
```

### 規約とルール

1. **`use` プレフィックスを付ける** — `useCounter`、`useFetch` など
2. **引数は ref/getter も受け入れる** — `toValue()` で値を取り出す
3. **リアクティブな値を返す** — 呼び出し側で分割代入できるよう `ref` で返す
4. **副作用はクリーンアップする** — `onUnmounted` でリスナーを解除
5. **同期的に呼び出す** — `setup()` / `<script setup>` のトップレベルで呼ぶ

```js
// ❌ 非同期の中で呼ばない
async function loadData() {
  const { data } = useFetch('/api/data')  // ライフサイクルと紐付かない
}

// ✅ トップレベルで呼ぶ
const { data } = useFetch('/api/data')
```

---

## 5.6 本章のまとめ

| 概念 | 説明 |
|------|------|
| `setup()` | Composition API のエントリーポイント |
| `<script setup>` | setup() の糖衣構文（推奨） |
| ライフサイクルフック | コンポーネントの各段階で処理を実行 |
| `onMounted` | DOM描画後の処理（最頻出） |
| `onUnmounted` | クリーンアップ処理 |
| Composable | `use` プレフィックスの再利用可能関数 |
| `defineExpose` | 外部に公開するAPI |

### 次章予告

第6章では、**フォームとバリデーション** について学びます。さまざまな入力要素との `v-model` 連携、カスタムバリデーションの実装、VeeValidate ライブラリの紹介を行います。

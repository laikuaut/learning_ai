# 第5章 演習：Composition API

> 対応教材: `教材/05_CompositionAPI_教材.md`
>
> この演習では、Composition API の基本（ref、reactive、computed、watch）と、
> ロジックの再利用（composable）を練習します。

---

## 演習5-1：ref と reactive の使い分け（基本）

### 問題

以下の要件を満たすプロフィール編集フォームを Composition API で作成してください。

**要件:**
1. `ref` でユーザー名を管理する
2. `reactive` でプロフィール情報（email、age、bio）をまとめて管理する
3. 「保存」ボタンをクリックすると、入力内容を表示エリアに反映する
4. 文字数カウントを `computed` で算出する

<details>
<summary>ヒント</summary>

- `ref` はプリミティブ値（文字列、数値など）に使います。テンプレート内では自動的にアンラップされます。
- `reactive` はオブジェクトに使います。テンプレート内で `.value` は不要です。
- `computed` は依存する値が変わると自動で再計算されます。

```vue
<script setup>
import { ref, reactive, computed } from 'vue'

const name = ref('')
const profile = reactive({ email: '', age: 0, bio: '' })
const bioLength = computed(() => profile.bio.length)
</script>
```

</details>

<details>
<summary>解答例</summary>

```vue
<script setup>
import { ref, reactive, computed } from 'vue'

// ref: プリミティブ値に使う（.value でアクセス）
const username = ref('')

// reactive: オブジェクトに使う（.value 不要）
const profile = reactive({
  email: '',
  age: null,
  bio: ''
})

// computed: 依存する値が変わると自動で再計算
const bioLength = computed(() => profile.bio.length)
const isValid = computed(() => {
  return username.value.trim().length > 0
    && profile.email.includes('@')
    && profile.age > 0
})

// 保存済みデータ
const savedData = ref(null)

function saveProfile() {
  if (!isValid.value) return
  // スプレッド構文でコピー（元のreactiveオブジェクトの参照を渡さない）
  savedData.value = {
    username: username.value,
    ...profile
  }
}
</script>

<template>
  <div style="max-width: 500px; margin: 0 auto; padding: 20px;">
    <h2>プロフィール編集</h2>

    <div style="margin-bottom: 12px;">
      <label style="display: block; margin-bottom: 4px; font-weight: bold;">ユーザー名</label>
      <input v-model="username" placeholder="ユーザー名" style="width: 100%; padding: 8px;" />
    </div>

    <div style="margin-bottom: 12px;">
      <label style="display: block; margin-bottom: 4px; font-weight: bold;">メール</label>
      <input v-model="profile.email" type="email" placeholder="email@example.com" style="width: 100%; padding: 8px;" />
    </div>

    <div style="margin-bottom: 12px;">
      <label style="display: block; margin-bottom: 4px; font-weight: bold;">年齢</label>
      <input v-model.number="profile.age" type="number" min="0" style="width: 100%; padding: 8px;" />
    </div>

    <div style="margin-bottom: 12px;">
      <label style="display: block; margin-bottom: 4px; font-weight: bold;">自己紹介</label>
      <textarea v-model="profile.bio" rows="3" placeholder="自己紹介..." style="width: 100%; padding: 8px;"></textarea>
      <p :style="{ color: bioLength > 200 ? 'red' : '#666', fontSize: '13px' }">
        {{ bioLength }} / 200 文字
      </p>
    </div>

    <button
      @click="saveProfile"
      :disabled="!isValid"
      style="padding: 10px 24px; background: #5c6bc0; color: white; border: none; border-radius: 6px; cursor: pointer;"
    >
      保存
    </button>

    <!-- 保存結果の表示 -->
    <div v-if="savedData" style="margin-top: 20px; padding: 16px; background: #e8f5e9; border-radius: 8px;">
      <h3>保存されたプロフィール</h3>
      <p><strong>名前:</strong> {{ savedData.username }}</p>
      <p><strong>メール:</strong> {{ savedData.email }}</p>
      <p><strong>年齢:</strong> {{ savedData.age }}</p>
      <p><strong>自己紹介:</strong> {{ savedData.bio }}</p>
    </div>
  </div>
</template>
```

**ポイント:**
- `ref` はプリミティブ値、`reactive` はオブジェクトに使い分けます
- テンプレート内では `ref` の `.value` は不要です（自動アンラップ）
- `computed` はゲッター関数を受け取り、依存値が変わると自動再計算します

</details>

---

## 演習5-2：watch と watchEffect（基本）

### 問題

検索キーワードの入力を `watch` で監視し、入力が止まってから300ms後に検索を実行する（デバウンス）機能を作成してください。

**要件:**
1. 検索キーワード入力欄
2. `watch` でキーワードの変更を監視
3. 入力が止まってから300ms後に検索実行（デバウンス処理）
4. 検索実行中はローディング表示
5. `watchEffect` で検索結果の件数をコンソールに出力

<details>
<summary>ヒント</summary>

- `watch` の第3引数に `{ immediate: true }` を指定すると、初回も実行されます
- デバウンスには `setTimeout` と `clearTimeout` を組み合わせます
- `watch` のコールバック内で返す関数はクリーンアップ関数です

```vue
watch(keyword, (newVal) => {
  const timer = setTimeout(() => {
    search(newVal)
  }, 300)
  // クリーンアップ：次の変更時に前のタイマーをキャンセル
  return () => clearTimeout(timer)  // ← Vue 3ではonCleanupを使う
})
```

</details>

<details>
<summary>解答例</summary>

```vue
<script setup>
import { ref, watch, watchEffect } from 'vue'

const keyword = ref('')
const results = ref([])
const isSearching = ref(false)

// テスト用データ
const allItems = [
  'JavaScript', 'TypeScript', 'Python', 'Ruby', 'Go',
  'React', 'Vue.js', 'Angular', 'Svelte', 'Next.js',
  'Node.js', 'Deno', 'Bun', 'Express', 'Fastify',
  'HTML', 'CSS', 'Sass', 'Tailwind CSS', 'Bootstrap',
]

// ========================================
// watch：特定のリアクティブな値の変更を監視
// keywordが変わるたびにコールバックが呼ばれる
// ========================================
let debounceTimer = null

watch(keyword, (newVal, oldVal) => {
  console.log(`キーワード変更: "${oldVal}" → "${newVal}"`)

  // 前のタイマーをクリア（デバウンス）
  if (debounceTimer) clearTimeout(debounceTimer)

  if (!newVal.trim()) {
    results.value = []
    return
  }

  isSearching.value = true

  // 300ms後に検索実行
  debounceTimer = setTimeout(() => {
    results.value = allItems.filter(item =>
      item.toLowerCase().includes(newVal.toLowerCase())
    )
    isSearching.value = false
  }, 300)
})

// ========================================
// watchEffect：依存するリアクティブな値を自動で追跡
// results が変わるたびに自動で再実行される
// ========================================
watchEffect(() => {
  if (results.value.length > 0) {
    console.log(`検索結果: ${results.value.length} 件`)
  }
})
</script>

<template>
  <div style="max-width: 400px; margin: 0 auto; padding: 20px;">
    <h2>検索（デバウンス付き）</h2>

    <input
      v-model="keyword"
      placeholder="キーワードを入力..."
      style="width: 100%; padding: 10px; font-size: 16px; border: 2px solid #ddd; border-radius: 8px;"
    />

    <p v-if="isSearching" style="color: #888; margin-top: 8px;">検索中...</p>

    <p v-else-if="keyword && results.length === 0" style="color: #888; margin-top: 8px;">
      該当なし
    </p>

    <ul v-else style="margin-top: 12px; list-style: none; padding: 0;">
      <li
        v-for="item in results"
        :key="item"
        style="padding: 8px 12px; border-bottom: 1px solid #eee;"
      >
        {{ item }}
      </li>
    </ul>
  </div>
</template>
```

**watch と watchEffect の違い:**
- `watch`: 特定の値を明示的に指定して監視。古い値と新しい値の両方を受け取れる
- `watchEffect`: コールバック内で使用しているリアクティブな値を**自動で追跡**。初回も即座に実行される

</details>

---

## 演習5-3：composable（カスタム関数）を作ろう（応用）

### 問題

以下の2つの composable を作成し、コンポーネントで使用してください。

1. **`useLocalStorage(key, defaultValue)`** — localStorage と同期するリアクティブな値
2. **`useWindowSize()`** — ウィンドウサイズをリアクティブに取得

<details>
<summary>ヒント</summary>

- composable は `use` で始まる関数で、中にリアクティブな値やライフサイクルフックを含められます
- `onMounted` / `onUnmounted` でイベントリスナーの登録・解除を行います

</details>

<details>
<summary>解答例</summary>

```vue
<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'

// ========================================
// composable 1: useLocalStorage
// localStorage とリアクティブな値を同期する
// ========================================
function useLocalStorage(key, defaultValue) {
  // localStorage から初期値を取得
  const stored = localStorage.getItem(key)
  const data = ref(stored ? JSON.parse(stored) : defaultValue)

  // data が変更されたら localStorage に保存
  watch(data, (newVal) => {
    localStorage.setItem(key, JSON.stringify(newVal))
  }, { deep: true })

  return data
}

// ========================================
// composable 2: useWindowSize
// ウィンドウサイズをリアクティブに追跡する
// ========================================
function useWindowSize() {
  const width = ref(window.innerWidth)
  const height = ref(window.innerHeight)

  function update() {
    width.value = window.innerWidth
    height.value = window.innerHeight
  }

  onMounted(() => {
    window.addEventListener('resize', update)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', update)
  })

  return { width, height }
}

// ========================================
// composable を使う
// ========================================
const username = useLocalStorage('username', '')
const theme = useLocalStorage('theme', 'light')
const { width, height } = useWindowSize()
</script>

<template>
  <div
    :style="{
      maxWidth: '500px',
      margin: '0 auto',
      padding: '20px',
      backgroundColor: theme === 'dark' ? '#333' : '#fff',
      color: theme === 'dark' ? '#fff' : '#333',
      minHeight: '100vh'
    }"
  >
    <h2>Composable の実践</h2>

    <div style="margin-bottom: 16px;">
      <label>名前（localStorage に保存されます）:</label>
      <input v-model="username" style="width: 100%; padding: 8px; margin-top: 4px;" />
      <p style="font-size: 13px; color: #888;">
        リロードしても値が保持されることを確認してください
      </p>
    </div>

    <div style="margin-bottom: 16px;">
      <label>テーマ:</label>
      <select v-model="theme" style="padding: 8px; margin-left: 8px;">
        <option value="light">ライト</option>
        <option value="dark">ダーク</option>
      </select>
    </div>

    <div style="padding: 16px; background: rgba(128,128,128,0.1); border-radius: 8px;">
      <p>ウィンドウサイズ: {{ width }} x {{ height }}</p>
      <p>デバイス: {{ width < 768 ? 'モバイル' : width < 1024 ? 'タブレット' : 'デスクトップ' }}</p>
    </div>
  </div>
</template>
```

**composable の利点:**
- ロジックをコンポーネントから分離して再利用できる
- テストが容易（関数単位でテスト可能）
- 関連するロジック（state + watch + ライフサイクル）をまとめて管理できる

</details>

---

## 演習5-4：ライフサイクルフックを理解しよう（応用）

### 問題

以下のライフサイクルフックを使い、タイマー付きクイズアプリを作成してください。

**要件:**
1. `onMounted` でタイマー開始
2. `onUnmounted` でタイマーのクリーンアップ
3. 制限時間（30秒）以内に3問のクイズに回答
4. 時間切れで終了

<details>
<summary>ヒント</summary>

- `onMounted` はコンポーネントがDOMに追加された後に呼ばれます
- `onUnmounted` はコンポーネントがDOMから削除される前に呼ばれます
- `setInterval` のIDを `ref` か変数で保持し、`onUnmounted` でクリアします

</details>

<details>
<summary>解答例</summary>

```vue
<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const questions = [
  { question: 'Vue 3 の Composition API で状態を定義するために使う関数は？', options: ['ref', 'data', 'state', 'var'], answer: 0 },
  { question: 'テンプレート内で条件付きレンダリングに使うディレクティブは？', options: ['v-show', 'v-if', 'v-when', 'v-cond'], answer: 1 },
  { question: 'リストのレンダリングに使うディレクティブは？', options: ['v-loop', 'v-each', 'v-for', 'v-list'], answer: 2 },
]

const currentIndex = ref(0)
const score = ref(0)
const timeLeft = ref(30)
const isFinished = ref(false)
const selectedAnswer = ref(null)
let timerId = null

const currentQuestion = computed(() => questions[currentIndex.value])
const progress = computed(() => ((30 - timeLeft.value) / 30) * 100)

function selectAnswer(index) {
  if (selectedAnswer.value !== null) return
  selectedAnswer.value = index

  if (index === currentQuestion.value.answer) {
    score.value++
  }

  // 1秒後に次の問題へ
  setTimeout(() => {
    if (currentIndex.value < questions.length - 1) {
      currentIndex.value++
      selectedAnswer.value = null
    } else {
      finishQuiz()
    }
  }, 1000)
}

function finishQuiz() {
  isFinished.value = true
  if (timerId) clearInterval(timerId)
}

function restartQuiz() {
  currentIndex.value = 0
  score.value = 0
  timeLeft.value = 30
  isFinished.value = false
  selectedAnswer.value = null
  startTimer()
}

function startTimer() {
  if (timerId) clearInterval(timerId)
  timerId = setInterval(() => {
    timeLeft.value--
    if (timeLeft.value <= 0) {
      finishQuiz()
    }
  }, 1000)
}

// コンポーネントがマウントされたらタイマー開始
onMounted(() => {
  startTimer()
})

// コンポーネントがアンマウントされたらタイマークリア（メモリリーク防止）
onUnmounted(() => {
  if (timerId) clearInterval(timerId)
})
</script>

<template>
  <div style="max-width: 500px; margin: 0 auto; padding: 20px;">
    <h2>Vue クイズ</h2>

    <!-- 結果画面 -->
    <div v-if="isFinished" style="text-align: center; padding: 40px;">
      <h3 :style="{ color: score === questions.length ? '#43a047' : '#333' }">
        {{ score === questions.length ? '全問正解！' : 'クイズ終了！' }}
      </h3>
      <p style="font-size: 48px; margin: 16px 0;">{{ score }} / {{ questions.length }}</p>
      <p v-if="timeLeft <= 0" style="color: #e53935;">時間切れ！</p>
      <button @click="restartQuiz" style="padding: 10px 24px; background: #5c6bc0; color: white; border: none; border-radius: 6px; cursor: pointer; margin-top: 16px;">
        もう一度
      </button>
    </div>

    <!-- クイズ画面 -->
    <div v-else>
      <!-- 進捗バー -->
      <div style="height: 6px; background: #e0e0e0; border-radius: 3px; margin-bottom: 16px;">
        <div :style="{ width: progress + '%', height: '100%', background: timeLeft <= 10 ? '#e53935' : '#5c6bc0', borderRadius: '3px', transition: 'width 1s' }"></div>
      </div>

      <div style="display: flex; justify-content: space-between; margin-bottom: 16px; color: #666;">
        <span>問題 {{ currentIndex + 1 }} / {{ questions.length }}</span>
        <span :style="{ color: timeLeft <= 10 ? '#e53935' : '#666', fontWeight: timeLeft <= 10 ? 'bold' : 'normal' }">
          残り {{ timeLeft }} 秒
        </span>
      </div>

      <div style="background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <h3 style="margin-bottom: 16px;">{{ currentQuestion.question }}</h3>

        <div v-for="(option, index) in currentQuestion.options" :key="index">
          <button
            @click="selectAnswer(index)"
            :disabled="selectedAnswer !== null"
            :style="{
              width: '100%', padding: '12px', margin: '4px 0', border: '2px solid',
              borderRadius: '8px', cursor: selectedAnswer !== null ? 'default' : 'pointer',
              textAlign: 'left', fontSize: '15px',
              borderColor: selectedAnswer === null ? '#e0e0e0'
                : index === currentQuestion.answer ? '#43a047'
                : index === selectedAnswer ? '#e53935' : '#e0e0e0',
              backgroundColor: selectedAnswer === null ? 'white'
                : index === currentQuestion.answer ? '#e8f5e9'
                : index === selectedAnswer ? '#ffebee' : 'white',
            }"
          >
            {{ option }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
```

**ライフサイクルフックのまとめ:**
- `onMounted`: DOM描画後。タイマー開始、API呼び出し、DOM操作に使う
- `onUnmounted`: コンポーネント破棄前。タイマークリア、イベントリスナー解除に使う
- `onMounted` で始めた処理は必ず `onUnmounted` でクリーンアップする

</details>

---

## 演習5-5：Options API から Composition API へ書き換え（チャレンジ）

### 問題

以下の Options API で書かれたコンポーネントを Composition API（`<script setup>`）に書き換えてください。

```vue
<script>
export default {
  data() {
    return {
      todos: [],
      newTodo: '',
      filter: 'all'
    }
  },
  computed: {
    filteredTodos() {
      if (this.filter === 'active') return this.todos.filter(t => !t.done)
      if (this.filter === 'done') return this.todos.filter(t => t.done)
      return this.todos
    },
    remaining() {
      return this.todos.filter(t => !t.done).length
    }
  },
  methods: {
    addTodo() {
      if (!this.newTodo.trim()) return
      this.todos.push({ id: Date.now(), text: this.newTodo.trim(), done: false })
      this.newTodo = ''
    },
    toggleTodo(id) {
      const todo = this.todos.find(t => t.id === id)
      if (todo) todo.done = !todo.done
    },
    removeTodo(id) {
      this.todos = this.todos.filter(t => t.id !== id)
    }
  },
  mounted() {
    console.log('Todo app mounted')
  }
}
</script>
```

<details>
<summary>ヒント</summary>

- `data()` → `ref()` または `reactive()`
- `computed` → `computed()`
- `methods` → 普通の関数
- `mounted()` → `onMounted()`
- `this` は不要になります

</details>

<details>
<summary>解答例</summary>

```vue
<script setup>
import { ref, computed, onMounted } from 'vue'

// data() → ref()
const todos = ref([])
const newTodo = ref('')
const filter = ref('all')

// computed → computed()
const filteredTodos = computed(() => {
  if (filter.value === 'active') return todos.value.filter(t => !t.done)
  if (filter.value === 'done') return todos.value.filter(t => t.done)
  return todos.value
})

const remaining = computed(() => {
  return todos.value.filter(t => !t.done).length
})

// methods → 普通の関数
function addTodo() {
  if (!newTodo.value.trim()) return
  todos.value.push({ id: Date.now(), text: newTodo.value.trim(), done: false })
  newTodo.value = ''
}

function toggleTodo(id) {
  const todo = todos.value.find(t => t.id === id)
  if (todo) todo.done = !todo.done
}

function removeTodo(id) {
  todos.value = todos.value.filter(t => t.id !== id)
}

// mounted → onMounted()
onMounted(() => {
  console.log('Todo app mounted')
})
</script>

<template>
  <div style="max-width: 500px; margin: 0 auto; padding: 20px;">
    <h2>Todo（Composition API版）</h2>

    <div style="display: flex; gap: 8px; margin-bottom: 16px;">
      <input
        v-model="newTodo"
        @keyup.enter="addTodo"
        placeholder="新しいタスク..."
        style="flex: 1; padding: 8px;"
      />
      <button @click="addTodo" style="padding: 8px 16px;">追加</button>
    </div>

    <div style="display: flex; gap: 8px; margin-bottom: 12px;">
      <button
        v-for="f in ['all', 'active', 'done']"
        :key="f"
        @click="filter = f"
        :style="{
          padding: '4px 12px', border: 'none', borderRadius: '12px', cursor: 'pointer',
          background: filter === f ? '#5c6bc0' : '#e0e0e0',
          color: filter === f ? 'white' : '#666'
        }"
      >
        {{ f === 'all' ? 'すべて' : f === 'active' ? '未完了' : '完了' }}
      </button>
    </div>

    <p style="color: #888; margin-bottom: 8px;">残り {{ remaining }} 件</p>

    <div v-for="todo in filteredTodos" :key="todo.id" style="display: flex; align-items: center; gap: 8px; padding: 8px; border-bottom: 1px solid #eee;">
      <input type="checkbox" :checked="todo.done" @change="toggleTodo(todo.id)" />
      <span :style="{ flex: 1, textDecoration: todo.done ? 'line-through' : 'none', color: todo.done ? '#999' : '#333' }">
        {{ todo.text }}
      </span>
      <button @click="removeTodo(todo.id)" style="color: red; background: none; border: none; cursor: pointer;">削除</button>
    </div>
  </div>
</template>
```

**書き換えのまとめ:**

| Options API | Composition API |
|-------------|-----------------|
| `data()` | `ref()` / `reactive()` |
| `computed: {}` | `computed(() => ...)` |
| `methods: {}` | 普通の関数宣言 |
| `mounted()` | `onMounted(() => ...)` |
| `this.xxx` | `xxx.value`（refの場合） |
| `watch: {}` | `watch()` / `watchEffect()` |

</details>

---

## まとめ

| 演習 | レベル | 学習ポイント |
|------|--------|-------------|
| 5-1 | 基本 | ref / reactive / computed の使い分け |
| 5-2 | 基本 | watch / watchEffect、デバウンス |
| 5-3 | 応用 | composable（カスタム関数）の作成 |
| 5-4 | 応用 | ライフサイクルフック（onMounted / onUnmounted） |
| 5-5 | チャレンジ | Options API → Composition API への書き換え |

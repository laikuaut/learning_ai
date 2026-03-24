# 第9章 演習：非同期処理とAPI連携

> 対応教材: `教材/09_非同期処理とAPI_教材.md`
>
> この演習では、fetch API を使ったデータ取得、ローディング/エラー状態の管理、
> composable によるデータ取得ロジックの再利用を練習します。

---

## 演習9-1：基本的なデータ取得（基本）

### 問題

JSONPlaceholder API からユーザー一覧を取得して表示してください。

**要件:**
1. `onMounted` でAPI呼び出し
2. ローディング中はスピナーを表示
3. エラー時はエラーメッセージと再試行ボタンを表示
4. 取得したデータをカード形式で表示

**API:** `https://jsonplaceholder.typicode.com/users`

<details>
<summary>ヒント</summary>

- `fetch` + `async/await` でデータを取得します
- `isLoading`、`error`、`data` の3つの状態で画面を切り替えます
- `try/catch/finally` でエラーハンドリングとローディング状態の管理を行います

</details>

<details>
<summary>解答例</summary>

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

onMounted(() => {
  fetchUsers()
})
</script>

<template>
  <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
    <h2>ユーザー一覧</h2>

    <!-- ローディング -->
    <div v-if="isLoading" style="text-align: center; padding: 40px; color: #888;">
      読み込み中...
    </div>

    <!-- エラー -->
    <div v-else-if="error" style="padding: 20px; background: #ffebee; border-radius: 8px; text-align: center;">
      <p style="color: #c62828;">エラー: {{ error }}</p>
      <button @click="fetchUsers" style="margin-top: 8px; padding: 8px 16px;">再試行</button>
    </div>

    <!-- データ表示 -->
    <div v-else>
      <div v-for="user in users" :key="user.id" style="padding: 16px; margin-bottom: 8px; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
        <h3 style="margin-bottom: 4px;">{{ user.name }}</h3>
        <p style="color: #666; font-size: 14px;">{{ user.email }}</p>
        <p style="color: #888; font-size: 13px;">{{ user.company.name }}</p>
      </div>
    </div>
  </div>
</template>
```

**ポイント:**
- `v-if` / `v-else-if` / `v-else` で3つの状態（ローディング / エラー / データ表示）を切り替えます
- `finally` ブロックで `isLoading` を `false` にすれば、成功時もエラー時もローディングが確実に解除されます
- 再試行ボタンは同じ `fetchUsers` 関数を呼ぶだけでOKです

</details>

---

## 演習9-2：useFetch composable を作ろう（基本）

### 問題

データ取得ロジックを再利用可能な `useFetch` composable に切り出してください。

**要件:**
1. URL を引数に受け取る
2. `data`、`isLoading`、`error` をリアクティブに返す
3. URL が変更されたら自動で再取得する
4. `refresh` 関数で手動再取得も可能にする

<details>
<summary>ヒント</summary>

- `watchEffect` を使うと、依存する ref が変わった時に自動で再実行されます
- composable は `use` で始まる関数で、ref や computed を返します

</details>

<details>
<summary>解答例</summary>

```js
// composables/useFetch.js
import { ref, watchEffect, isRef, unref } from 'vue'

export function useFetch(url) {
  const data = ref(null)
  const error = ref(null)
  const isLoading = ref(false)

  async function execute() {
    // url が ref なら .value で取得、そうでなければそのまま
    const urlValue = unref(url)
    if (!urlValue) return

    isLoading.value = true
    error.value = null
    data.value = null

    try {
      const response = await fetch(urlValue)
      if (!response.ok) throw new Error(`HTTP Error: ${response.status}`)
      data.value = await response.json()
    } catch (e) {
      error.value = e.message
    } finally {
      isLoading.value = false
    }
  }

  // url が ref の場合、変更を自動追跡して再取得
  if (isRef(url)) {
    watchEffect(() => {
      execute()
    })
  } else {
    // 通常の文字列の場合は即時実行
    execute()
  }

  return { data, error, isLoading, refresh: execute }
}
```

```vue
<!-- 使用例 -->
<script setup>
import { ref, computed } from 'vue'
import { useFetch } from '@/composables/useFetch'

const userId = ref(1)
const url = computed(() => `https://jsonplaceholder.typicode.com/users/${userId.value}`)

// url が変わると自動で再取得される
const { data: user, isLoading, error, refresh } = useFetch(url)
</script>

<template>
  <div style="max-width: 400px; margin: 0 auto; padding: 20px;">
    <h2>ユーザー詳細</h2>

    <div style="display: flex; gap: 4px; margin-bottom: 16px;">
      <button v-for="id in 5" :key="id" @click="userId = id"
        :style="{ padding: '6px 12px', background: userId === id ? '#5c6bc0' : '#eee', color: userId === id ? 'white' : '#333', border: 'none', borderRadius: '6px', cursor: 'pointer' }">
        ユーザー {{ id }}
      </button>
    </div>

    <p v-if="isLoading" style="color: #888;">読み込み中...</p>
    <p v-else-if="error" style="color: #e53935;">{{ error }}</p>

    <div v-else-if="user" style="padding: 16px; background: #f8f9fa; border-radius: 8px;">
      <h3>{{ user.name }}</h3>
      <p>{{ user.email }}</p>
      <p>{{ user.phone }}</p>
      <button @click="refresh" style="margin-top: 8px;">再取得</button>
    </div>
  </div>
</template>
```

**ポイント:**
- `useFetch` に `ref` や `computed` を渡すと、値が変わった時に自動で再取得されます
- `unref()` は ref なら `.value` を返し、そうでなければ値をそのまま返すユーティリティです
- この `useFetch` パターンは VueUse ライブラリでも提供されている定番パターンです

</details>

---

## 演習9-3：検索とページネーション（応用）

### 問題

API を使った検索機能とページネーションを実装してください。

**要件:**
1. 検索キーワードでフィルタリング（デバウンス付き）
2. 1ページあたり5件表示のページネーション
3. ページ変更時にスムーズなローディング表示
4. 検索結果の件数表示

**API:** `https://jsonplaceholder.typicode.com/posts`

<details>
<summary>ヒント</summary>

- JSONPlaceholder は `_page` と `_limit` クエリパラメータに対応しています
- デバウンスには `setTimeout` / `clearTimeout` を使います
- 検索キーワードが変わったらページを1に戻します

</details>

<details>
<summary>解答例</summary>

```vue
<script setup>
import { ref, watch, computed } from 'vue'

const posts = ref([])
const isLoading = ref(false)
const keyword = ref('')
const currentPage = ref(1)
const totalCount = ref(0)
const perPage = 5

let debounceTimer = null

async function fetchPosts() {
  isLoading.value = true
  try {
    // JSONPlaceholder は _page と _limit をサポート
    let url = `https://jsonplaceholder.typicode.com/posts?_page=${currentPage.value}&_limit=${perPage}`

    const response = await fetch(url)
    // x-total-count ヘッダーで全件数を取得
    totalCount.value = parseInt(response.headers.get('x-total-count') || '100')
    const allPosts = await response.json()

    // クライアントサイドで検索フィルタ
    if (keyword.value) {
      posts.value = allPosts.filter(p =>
        p.title.includes(keyword.value.toLowerCase())
      )
    } else {
      posts.value = allPosts
    }
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

const totalPages = computed(() => Math.ceil(totalCount.value / perPage))

// キーワード変更時（デバウンス付き）
watch(keyword, () => {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    currentPage.value = 1
    fetchPosts()
  }, 300)
})

// ページ変更時
watch(currentPage, () => {
  fetchPosts()
})

// 初回取得
fetchPosts()
</script>

<template>
  <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
    <h2>投稿検索</h2>

    <input
      v-model="keyword"
      placeholder="キーワードで検索..."
      style="width: 100%; padding: 10px; margin-bottom: 16px; border: 2px solid #ddd; border-radius: 8px;"
    />

    <p v-if="isLoading" style="text-align: center; color: #888; padding: 40px;">読み込み中...</p>

    <div v-else>
      <div v-for="post in posts" :key="post.id" style="padding: 16px; margin-bottom: 8px; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
        <h3 style="font-size: 16px; margin-bottom: 4px;">{{ post.title }}</h3>
        <p style="color: #666; font-size: 14px;">{{ post.body.substring(0, 80) }}...</p>
      </div>

      <p v-if="posts.length === 0" style="text-align: center; color: #888; padding: 20px;">
        該当する投稿がありません
      </p>

      <!-- ページネーション -->
      <div style="display: flex; justify-content: center; gap: 4px; margin-top: 20px;">
        <button
          @click="currentPage--"
          :disabled="currentPage <= 1"
          style="padding: 6px 12px;"
        >
          前へ
        </button>

        <button
          v-for="page in Math.min(totalPages, 10)"
          :key="page"
          @click="currentPage = page"
          :style="{
            padding: '6px 12px', border: 'none', borderRadius: '6px', cursor: 'pointer',
            background: currentPage === page ? '#5c6bc0' : '#eee',
            color: currentPage === page ? 'white' : '#333'
          }"
        >
          {{ page }}
        </button>

        <button
          @click="currentPage++"
          :disabled="currentPage >= totalPages"
          style="padding: 6px 12px;"
        >
          次へ
        </button>
      </div>

      <p style="text-align: center; color: #888; font-size: 13px; margin-top: 8px;">
        ページ {{ currentPage }} / {{ totalPages }}
      </p>
    </div>
  </div>
</template>
```

**ポイント:**
- `x-total-count` ヘッダーは JSONPlaceholder が返す全件数の情報です
- デバウンスによって、入力のたびにAPIを叩くのではなく、入力が止まってから取得します
- 検索時にページを1に戻すのを忘れないようにしましょう

</details>

---

## 演習9-4：楽観的更新（チャレンジ）

### 問題

TODOアプリで「楽観的更新（Optimistic Update）」パターンを実装してください。

**楽観的更新とは:**
APIの応答を待たずに先にUIを更新し、失敗したらロールバックするパターンです。

**要件:**
1. TODOの完了切替時、即座にUIを更新（APIレスポンスを待たない）
2. API呼び出し成功 → そのまま
3. API呼び出し失敗 → UIを元に戻す（ロールバック）+ エラー通知

<details>
<summary>ヒント</summary>

1. まず現在の状態を保存（バックアップ）
2. 即座にUIを更新
3. APIを呼び出し
4. 失敗したらバックアップから復元

</details>

<details>
<summary>解答例</summary>

```vue
<script setup>
import { ref } from 'vue'

const todos = ref([
  { id: 1, text: 'Vue.js を学ぶ', completed: false },
  { id: 2, text: 'Pinia を学ぶ', completed: false },
  { id: 3, text: 'テストを書く', completed: true },
])
const error = ref(null)

// 疑似API（50%の確率で失敗する）
async function fakeApi(id, completed) {
  await new Promise(resolve => setTimeout(resolve, 1000))
  if (Math.random() < 0.5) {
    throw new Error('サーバーエラーが発生しました')
  }
  return { id, completed }
}

async function toggleTodo(id) {
  const todo = todos.value.find(t => t.id === id)
  if (!todo) return

  // 1. 現在の状態をバックアップ
  const previousState = todo.completed

  // 2. 楽観的にUIを即座に更新
  todo.completed = !todo.completed
  error.value = null

  try {
    // 3. APIを呼び出し（レスポンスを待つ）
    await fakeApi(id, todo.completed)
    // 成功 → 何もしない（UIは既に更新済み）
  } catch (e) {
    // 4. 失敗 → ロールバック（UIを元に戻す）
    todo.completed = previousState
    error.value = `「${todo.text}」の更新に失敗しました: ${e.message}`

    // 3秒後にエラーメッセージを消す
    setTimeout(() => { error.value = null }, 3000)
  }
}
</script>

<template>
  <div style="max-width: 400px; margin: 0 auto; padding: 20px;">
    <h2>楽観的更新 デモ</h2>
    <p style="color: #888; font-size: 13px; margin-bottom: 16px;">
      チェックを切り替えると即座にUIが更新されます。<br />
      50%の確率でAPI失敗→元に戻ります。
    </p>

    <!-- エラー通知 -->
    <div v-if="error" style="padding: 12px; background: #ffebee; border-radius: 8px; color: #c62828; margin-bottom: 12px; transition: opacity 0.3s;">
      {{ error }}
    </div>

    <div v-for="todo in todos" :key="todo.id" style="display: flex; align-items: center; gap: 8px; padding: 12px; border-bottom: 1px solid #eee;">
      <input type="checkbox" :checked="todo.completed" @change="toggleTodo(todo.id)" />
      <span :style="{ textDecoration: todo.completed ? 'line-through' : 'none', color: todo.completed ? '#999' : '#333' }">
        {{ todo.text }}
      </span>
    </div>
  </div>
</template>
```

**楽観的更新のメリット:**
- APIレスポンスを待たないため、UIがスナップリーに反応する
- ユーザーは即座にフィードバックを得られる

**デメリット:**
- ロールバック処理の実装が必要
- 一時的にサーバーとクライアントの状態が不整合になる

</details>

---

## まとめ

| 演習 | レベル | 学習ポイント |
|------|--------|-------------|
| 9-1 | 基本 | fetch API、ローディング/エラー状態管理 |
| 9-2 | 基本 | useFetch composable、ロジックの再利用 |
| 9-3 | 応用 | 検索、ページネーション、デバウンス |
| 9-4 | チャレンジ | 楽観的更新パターン、ロールバック |

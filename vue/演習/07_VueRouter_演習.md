# 第7章 演習：Vue Router

> 対応教材: `教材/07_VueRouter_教材.md`
>
> この演習では、Vue Router を使った SPA のルーティング、
> 動的パラメータ、ナビゲーションガード、レイアウトの共有を練習します。

---

## 演習7-1：基本的なルーティング設定（基本）

### 問題

3ページ構成のSPAを Vue Router で作成してください。

**要件:**
1. `/` → ホームページ
2. `/about` → Aboutページ
3. `/contact` → お問い合わせページ
4. ナビゲーションバーに `<router-link>` を配置
5. アクティブなリンクにスタイルを適用

<details>
<summary>ヒント</summary>

- `createRouter` と `createWebHistory` でルーターインスタンスを作成します
- `<router-link>` はSPA遷移用のリンクです（`<a>` タグの代わり）
- `<router-view>` はルートに対応するコンポーネントの表示場所です
- `.router-link-active` クラスが自動付与されます

</details>

<details>
<summary>解答例</summary>

```js
// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import ContactView from '../views/ContactView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/about', name: 'about', component: AboutView },
    { path: '/contact', name: 'contact', component: ContactView },
    // 404: どのルートにもマッチしない場合
    { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('../views/NotFound.vue') }
  ]
})

export default router
```

```vue
<!-- App.vue -->
<template>
  <div>
    <nav style="display: flex; gap: 16px; padding: 16px; background: #2c3e50;">
      <!-- router-link は SPA 遷移用のリンク。to でパスを指定 -->
      <router-link to="/" style="color: white; text-decoration: none;">ホーム</router-link>
      <router-link to="/about" style="color: white; text-decoration: none;">About</router-link>
      <router-link to="/contact" style="color: white; text-decoration: none;">お問い合わせ</router-link>
    </nav>

    <!-- ルートに対応するコンポーネントがここに表示される -->
    <main style="padding: 20px;">
      <router-view />
    </main>
  </div>
</template>

<style>
/* アクティブなリンクに自動で付与されるクラス */
.router-link-active {
  font-weight: bold;
  border-bottom: 2px solid #3498db;
  padding-bottom: 4px;
}
</style>
```

**ポイント:**
- `<router-link>` は `<a>` タグとして描画されますが、クリック時にページリロードを防ぎます
- `<router-view>` は現在のURLに対応するコンポーネントが表示される場所です
- `.router-link-active` と `.router-link-exact-active` が自動でクラス付与されます

</details>

---

## 演習7-2：動的ルートとパラメータ（基本）

### 問題

ブログ記事の一覧と詳細ページを動的ルートで作成してください。

**要件:**
1. `/posts` → 記事一覧
2. `/posts/:id` → 記事詳細（`useRoute` でパラメータ取得）
3. 存在しない記事IDの場合は「記事が見つかりません」を表示
4. 詳細ページに「一覧に戻る」リンク

<details>
<summary>ヒント</summary>

- `useRoute()` で現在のルート情報にアクセスできます
- `route.params.id` でURLパラメータを取得します
- 値は文字列なので `Number()` で変換が必要な場合があります

</details>

<details>
<summary>解答例</summary>

```js
// ルート定義
const routes = [
  { path: '/posts', name: 'posts', component: PostList },
  { path: '/posts/:id', name: 'post-detail', component: PostDetail },
]
```

```vue
<!-- PostDetail.vue -->
<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const posts = [
  { id: 1, title: 'Vue 3 入門', content: 'Vue 3 の基本を学びましょう。Composition API が大きな特徴です。', category: 'frontend' },
  { id: 2, title: 'Pinia 実践', content: 'Pinia を使った状態管理のベストプラクティスを紹介します。', category: 'frontend' },
  { id: 3, title: 'TypeScript 入門', content: 'TypeScript で型安全な開発を始めましょう。', category: 'language' },
]

// useRoute で URL パラメータを取得
// route.params.id は文字列なので Number() で変換
const post = computed(() => {
  return posts.find(p => p.id === Number(route.params.id))
})

function goBack() {
  // useRouter でプログラム的に遷移
  router.push('/posts')
  // router.back() でブラウザの戻る操作も可能
}
</script>

<template>
  <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
    <div v-if="post">
      <h1>{{ post.title }}</h1>
      <span style="padding: 2px 8px; background: #e3f2fd; border-radius: 12px; font-size: 12px;">
        {{ post.category }}
      </span>
      <p style="margin-top: 16px; line-height: 1.8;">{{ post.content }}</p>
    </div>

    <div v-else style="text-align: center; padding: 40px;">
      <h2>記事が見つかりません</h2>
      <p>ID: {{ route.params.id }} の記事は存在しません。</p>
    </div>

    <button @click="goBack" style="margin-top: 16px; padding: 8px 16px;">
      ← 一覧に戻る
    </button>
  </div>
</template>
```

**ポイント:**
- `useRoute()` は現在のルート情報（params、query、path など）を取得するフック
- `useRouter()` はプログラム的な遷移（`push`、`replace`、`back`）に使うフック
- `route.params` の値は常に文字列です

</details>

---

## 演習7-3：ネストされたルート（応用）

### 問題

管理画面のレイアウトをネストされたルートで作成してください。

**要件:**
1. `/admin` にサイドバー付きレイアウト
2. `/admin/dashboard` → ダッシュボード
3. `/admin/users` → ユーザー管理
4. `/admin/settings` → 設定
5. サイドバーのアクティブリンクにスタイル適用

<details>
<summary>ヒント</summary>

- 親ルートのコンポーネントに `<router-view>` を配置すると、子ルートがそこに表示されます
- `children` プロパティで子ルートを定義します

```js
{
  path: '/admin',
  component: AdminLayout,
  children: [
    { path: 'dashboard', component: Dashboard },
    { path: 'users', component: Users },
  ]
}
```

</details>

<details>
<summary>解答例</summary>

```js
const routes = [
  {
    path: '/admin',
    component: AdminLayout,
    // redirect で /admin アクセス時に /admin/dashboard へ転送
    redirect: '/admin/dashboard',
    children: [
      { path: 'dashboard', name: 'admin-dashboard', component: Dashboard },
      { path: 'users', name: 'admin-users', component: Users },
      { path: 'settings', name: 'admin-settings', component: Settings },
    ]
  }
]
```

```vue
<!-- AdminLayout.vue -->
<script setup>
const menuItems = [
  { path: '/admin/dashboard', label: 'ダッシュボード', icon: '📊' },
  { path: '/admin/users', label: 'ユーザー管理', icon: '👥' },
  { path: '/admin/settings', label: '設定', icon: '⚙️' },
]
</script>

<template>
  <div style="display: flex; min-height: 100vh;">
    <!-- サイドバー -->
    <aside style="width: 240px; background: #1a1a2e; color: white; padding: 20px;">
      <h2 style="font-size: 18px; margin-bottom: 24px;">管理画面</h2>
      <nav>
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          style="display: block; padding: 10px 12px; margin-bottom: 4px; border-radius: 8px; color: #ccc; text-decoration: none;"
          active-class="active-link"
        >
          {{ item.icon }} {{ item.label }}
        </router-link>
      </nav>
    </aside>

    <!-- メインコンテンツ：子ルートがここに表示される -->
    <main style="flex: 1; padding: 24px; background: #f5f5f5;">
      <router-view />
    </main>
  </div>
</template>

<style>
.active-link {
  background: #0f3460 !important;
  color: white !important;
  font-weight: bold;
}
</style>
```

**ポイント:**
- ネストされたルートは親のレイアウト内に `<router-view>` で子を表示します
- `redirect` で親パスへのアクセスを子パスに転送できます
- `active-class` プロパティでアクティブ時のクラス名をカスタマイズできます

</details>

---

## 演習7-4：ナビゲーションガード（チャレンジ）

### 問題

ログイン認証付きの保護されたルートを実装してください。

**要件:**
1. `/login` → ログインページ
2. `/admin/*` → 保護されたページ（ログイン必須）
3. 未認証で `/admin/*` にアクセスすると `/login` にリダイレクト
4. ログイン後に元々アクセスしようとしたページにリダイレクト
5. `beforeEach` グローバルガードで実装

<details>
<summary>ヒント</summary>

- `router.beforeEach((to, from) => {...})` でグローバルガードを設定します
- ルートの `meta` プロパティに認証必須フラグを付けます
- リダイレクト先をクエリパラメータで渡すとログイン後の遷移先を指定できます

</details>

<details>
<summary>解答例</summary>

```js
// router/index.js
const routes = [
  { path: '/login', name: 'login', component: LoginView },
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true },  // 認証必須フラグ
    children: [
      { path: 'dashboard', component: Dashboard },
      { path: 'settings', component: Settings },
    ]
  }
]

const router = createRouter({ history: createWebHistory(), routes })

// グローバルナビゲーションガード
router.beforeEach((to, from) => {
  const isAuthenticated = localStorage.getItem('token')

  // 認証が必要なルートで、未認証の場合
  if (to.meta.requiresAuth && !isAuthenticated) {
    // ログイン後に元のページに戻れるよう、redirect クエリを付与
    return {
      path: '/login',
      query: { redirect: to.fullPath }
    }
  }

  // ログイン済みでログインページにアクセスした場合はダッシュボードへ
  if (to.path === '/login' && isAuthenticated) {
    return '/admin/dashboard'
  }
})
```

```vue
<!-- LoginView.vue -->
<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')

function login() {
  if (email.value === 'admin@example.com' && password.value === 'password') {
    localStorage.setItem('token', 'dummy-token')
    // ログイン前にアクセスしようとしたページに遷移
    const redirect = route.query.redirect || '/admin/dashboard'
    router.push(redirect)
  } else {
    error.value = '認証に失敗しました'
  }
}

function logout() {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>
```

**ポイント:**
- `meta` はルートにカスタム情報を付与するための仕組みです
- `beforeEach` はすべてのルート遷移の前に実行されます
- `return { path: '/login' }` で遷移先を変更（リダイレクト）できます
- ログイン後のリダイレクト先をクエリパラメータで保持するのは実務でよく使われるパターンです

</details>

---

## まとめ

| 演習 | レベル | 学習ポイント |
|------|--------|-------------|
| 7-1 | 基本 | router-link、router-view、基本ルート設定 |
| 7-2 | 基本 | 動的ルート、useRoute、useRouter |
| 7-3 | 応用 | ネストされたルート、レイアウト共有 |
| 7-4 | チャレンジ | ナビゲーションガード、認証付きルート |

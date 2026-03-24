# 第7章：Vue Router

## 7.1 Vue Router とは

Vue Router は Vue.js の公式ルーティングライブラリです。URLに応じて異なるコンポーネント（ページ）を表示する **SPA（Single Page Application）** を構築できます。

### インストールと初期設定

```bash
# 既存プロジェクトに追加する場合
npm install vue-router@4

# または、プロジェクト作成時に「Add Vue Router? → Yes」を選択
```

---

## 7.2 ルーターの設定

### ルーター定義ファイル

```js
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// ページコンポーネントをインポート
import HomeView from '@/views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'

// ルート定義
const routes = [
  {
    path: '/',           // URL パス
    name: 'home',        // ルート名（任意だが推奨）
    component: HomeView  // 表示するコンポーネント
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    // 遅延ローディング（必要な時にだけ読み込む）
    path: '/contact',
    name: 'contact',
    component: () => import('@/views/ContactView.vue')
  }
]

// ルーターインスタンスを作成
const router = createRouter({
  // HTML5 History モード（URLに # が付かない）
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
```

### main.js への登録

```js
// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(router)   // ルーターをプラグインとして登録
app.mount('#app')
```

### App.vue

```vue
<!-- src/App.vue -->
<script setup>
</script>

<template>
  <div id="app">
    <nav>
      <!-- RouterLink: ページ遷移リンク（a タグに変換される） -->
      <RouterLink to="/">ホーム</RouterLink>
      <RouterLink to="/about">アバウト</RouterLink>
      <RouterLink to="/contact">お問い合わせ</RouterLink>
    </nav>

    <!-- RouterView: マッチしたコンポーネントが表示される場所 -->
    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
nav a {
  margin-right: 1rem;
}

/* アクティブなリンクに自動付与されるクラス */
nav a.router-link-active {
  font-weight: bold;
  color: #42b883;
}
</style>
```

---

## 7.3 RouterLink の詳細

```vue
<template>
  <!-- 文字列パス -->
  <RouterLink to="/about">アバウト</RouterLink>

  <!-- 名前付きルート（推奨: パスの変更に強い） -->
  <RouterLink :to="{ name: 'about' }">アバウト</RouterLink>

  <!-- パラメータ付き -->
  <RouterLink :to="{ name: 'user', params: { id: 123 } }">
    ユーザー
  </RouterLink>

  <!-- クエリパラメータ付き -->
  <RouterLink :to="{ name: 'search', query: { q: 'vue' } }">
    検索
  </RouterLink>
  <!-- → /search?q=vue -->

  <!-- replace: 履歴に追加せず置き換え -->
  <RouterLink to="/about" replace>アバウト</RouterLink>

  <!-- カスタム active クラス -->
  <RouterLink
    to="/about"
    active-class="active"
    exact-active-class="exact-active"
  >
    アバウト
  </RouterLink>
</template>
```

---

## 7.4 動的ルーティング（パラメータ）

URL の一部を変数として受け取る機能です。

### ルート定義

```js
// router/index.js
const routes = [
  // 動的セグメント :id
  {
    path: '/users/:id',
    name: 'user',
    component: () => import('@/views/UserView.vue')
  },
  // 複数のパラメータ
  {
    path: '/posts/:year/:month/:slug',
    name: 'post',
    component: () => import('@/views/PostView.vue')
  },
  // オプショナルパラメータ（? を付ける）
  {
    path: '/users/:id/posts/:postId?',
    name: 'userPost',
    component: () => import('@/views/UserPostView.vue')
  }
]
```

### パラメータの取得

```vue
<!-- views/UserView.vue -->
<script setup>
import { useRoute, useRouter } from 'vue-router'
import { ref, watch } from 'vue'

// useRoute: 現在のルート情報にアクセス
const route = useRoute()

// useRouter: ルーター操作メソッドにアクセス
const router = useRouter()

const user = ref(null)

// パラメータの取得
console.log(route.params.id)    // '/users/123' → '123'
console.log(route.query)        // '/users/123?tab=posts' → { tab: 'posts' }
console.log(route.path)         // '/users/123'
console.log(route.name)         // 'user'
console.log(route.fullPath)     // '/users/123?tab=posts'

// パラメータの変更を監視（同じコンポーネントでIDだけ変わる場合）
watch(
  () => route.params.id,
  async (newId) => {
    user.value = await fetchUser(newId)
  },
  { immediate: true }
)

async function fetchUser(id) {
  const response = await fetch(`/api/users/${id}`)
  return response.json()
}

// プログラムによるナビゲーション
function goToEdit() {
  router.push({ name: 'userEdit', params: { id: route.params.id } })
}

function goBack() {
  router.back()  // ブラウザの「戻る」と同じ
}

function goForward() {
  router.forward()  // ブラウザの「進む」と同じ
}

function replaceRoute() {
  router.replace({ name: 'home' })  // 履歴を置き換え
}
</script>

<template>
  <div v-if="user">
    <h1>{{ user.name }}</h1>
    <button @click="goToEdit">編集</button>
    <button @click="goBack">戻る</button>
  </div>
</template>
```

---

## 7.5 ネストされたルート

ルートの中にさらにルートを定義し、レイアウトの入れ子構造を実現します。

```js
// router/index.js
const routes = [
  {
    path: '/dashboard',
    component: () => import('@/views/DashboardLayout.vue'),
    children: [
      {
        path: '',          // /dashboard
        name: 'dashboard',
        component: () => import('@/views/DashboardHome.vue')
      },
      {
        path: 'profile',   // /dashboard/profile
        name: 'profile',
        component: () => import('@/views/DashboardProfile.vue')
      },
      {
        path: 'settings',  // /dashboard/settings
        name: 'settings',
        component: () => import('@/views/DashboardSettings.vue')
      }
    ]
  }
]
```

```vue
<!-- views/DashboardLayout.vue（親レイアウト） -->
<template>
  <div class="dashboard">
    <aside class="sidebar">
      <nav>
        <RouterLink :to="{ name: 'dashboard' }">ホーム</RouterLink>
        <RouterLink :to="{ name: 'profile' }">プロフィール</RouterLink>
        <RouterLink :to="{ name: 'settings' }">設定</RouterLink>
      </nav>
    </aside>

    <main class="content">
      <!-- 子ルートのコンポーネントがここに表示される -->
      <RouterView />
    </main>
  </div>
</template>
```

---

## 7.6 ナビゲーションガード

ルート遷移の前後に処理を挟むことができます。認証チェックなどに利用します。

### グローバルガード

```js
// router/index.js
const router = createRouter({ /* ... */ })

// beforeEach: 全ルート遷移前に実行
router.beforeEach((to, from) => {
  // to: 遷移先のルート情報
  // from: 遷移元のルート情報

  const isAuthenticated = checkAuth()  // 認証チェック

  // 認証が必要なルートかつ未認証の場合
  if (to.meta.requiresAuth && !isAuthenticated) {
    // ログインページにリダイレクト
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  // undefined または true を返すと遷移を許可
  // false を返すと遷移をキャンセル
})

// afterEach: 全ルート遷移後に実行
router.afterEach((to, from) => {
  // ページタイトルの更新
  document.title = to.meta.title || 'マイアプリ'
})
```

### ルート定義での meta フィールド

```js
const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: { title: 'ログイン', requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { title: 'ダッシュボード', requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import('@/views/AdminView.vue'),
    meta: { title: '管理画面', requiresAuth: true, requiresAdmin: true }
  }
]
```

### ルート単位のガード

```js
const routes = [
  {
    path: '/admin',
    component: AdminView,
    beforeEnter: (to, from) => {
      // このルートに入る前だけ実行
      if (!isAdmin()) {
        return { name: 'home' }
      }
    }
  }
]
```

### コンポーネント内ガード

```vue
<script setup>
import { onBeforeRouteLeave, onBeforeRouteUpdate } from 'vue-router'
import { ref } from 'vue'

const hasUnsavedChanges = ref(false)

// ルートから離れる前に確認
onBeforeRouteLeave((to, from) => {
  if (hasUnsavedChanges.value) {
    const answer = window.confirm('保存されていない変更があります。離れますか？')
    if (!answer) return false  // 遷移をキャンセル
  }
})

// 同じコンポーネントでルートが更新された時
onBeforeRouteUpdate((to, from) => {
  console.log(`パラメータ変更: ${from.params.id} → ${to.params.id}`)
})
</script>
```

---

## 7.7 高度なルーティング

### 404 ページ（キャッチオール）

```js
const routes = [
  // ... 他のルート ...

  // キャッチオール: マッチしないURL
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue')
  }
]
```

### リダイレクト

```js
const routes = [
  {
    path: '/home',
    redirect: '/'  // /home → / にリダイレクト
  },
  {
    path: '/old-about',
    redirect: { name: 'about' }  // 名前付きルートへリダイレクト
  },
  {
    // 動的リダイレクト
    path: '/search/:query',
    redirect: (to) => {
      return { path: '/results', query: { q: to.params.query } }
    }
  }
]
```

### エイリアス

```js
const routes = [
  {
    path: '/users',
    alias: ['/members', '/people'],  // 複数のURLで同じコンポーネント
    component: UserListView
  }
]
```

### ルート遷移アニメーション

```vue
<!-- App.vue -->
<template>
  <RouterView v-slot="{ Component }">
    <Transition name="fade" mode="out-in">
      <component :is="Component" />
    </Transition>
  </RouterView>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
```

### スクロール制御

```js
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // ブラウザの戻る/進むボタンで元のスクロール位置を復元
    if (savedPosition) {
      return savedPosition
    }
    // ハッシュがある場合（アンカーリンク）
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    // それ以外はページトップに
    return { top: 0 }
  }
})
```

---

## 7.8 ルーティングのベストプラクティス

### ファイル構成

```
src/
├── router/
│   └── index.js
├── views/           # ページコンポーネント（ルートに対応）
│   ├── HomeView.vue
│   ├── AboutView.vue
│   └── users/
│       ├── UserListView.vue
│       └── UserDetailView.vue
└── components/      # 再利用可能コンポーネント（ページ内の部品）
    ├── UserCard.vue
    └── UserForm.vue
```

### 命名規則

- **views/**: `〇〇View.vue` — ルートに対応するページ
- **components/**: `〇〇.vue` — ページ内で使う再利用可能部品
- **ルート名**: キャメルケース（`userDetail`）またはケバブケース（`user-detail`）

---

## 7.9 本章のまとめ

| 概念 | 説明 |
|------|------|
| `createRouter` | ルーターインスタンスの作成 |
| `RouterView` | マッチしたコンポーネントの表示場所 |
| `RouterLink` | ページ遷移リンク |
| `useRoute()` | 現在のルート情報（params, query 等） |
| `useRouter()` | ルーター操作（push, replace, back 等） |
| `children` | ネストされたルート |
| `beforeEach` | グローバルナビゲーションガード |
| `meta` | ルートのメタ情報（認証フラグ等） |
| 遅延ローディング | `() => import(...)` でコード分割 |

### 次章予告

第8章では **Pinia** を使った状態管理を学びます。複数のコンポーネント間でデータを共有する方法、ストアの設計パターンを理解します。

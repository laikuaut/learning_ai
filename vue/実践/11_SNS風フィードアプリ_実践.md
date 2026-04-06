# 実践課題11：SNS風フィードアプリ ★5

> **難易度**: ★★★★★（総合）
> **前提知識**: 第1章〜第9章（全章の知識を活用）
> **課題の種類**: ミニプロジェクト（総合設計）
> **学習目標**: composable によるロジック分離、`provide` / `inject` によるグローバル状態管理、非同期データ取得、複雑なコンポーネント間連携を統合する

---

## 完成イメージ

投稿の作成・いいね・コメント・検索ができるSNS風フィードアプリです。

```
┌──────────────────────────────────────────────┐
│ 📱 Vue Feed       [太郎 ▼]   [☀️/🌙]       │
├──────────────────────────────────────────────┤
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ 今何してる？                          │   │
│  │ [投稿内容を入力...                 ]  │   │
│  │ [📷 画像]  [🏷️ タグ]    [投稿する]  │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  検索: [キーワード...]  タグ: [#Vue] [#JS]  │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ 🧑 太郎              3分前          │   │
│  │                                      │   │
│  │ Vue.jsの学習進捗をシェア！           │   │
│  │ Composition APIが便利すぎる          │   │
│  │                                      │   │
│  │ #Vue #学習                           │   │
│  │                                      │   │
│  │ ❤️ 5  💬 2  [いいね] [コメント]     │   │
│  │                                      │   │
│  │ ┌────────────────────────────────┐  │   │
│  │ │ 花子: すごいですね！           │  │   │
│  │ │ 次郎: 参考になります          │  │   │
│  │ │ [コメントを入力...   ] [送信]  │  │   │
│  │ └────────────────────────────────┘  │   │
│  └──────────────────────────────────────┘   │
└──────────────────────────────────────────────┘
```

---

## 課題の要件

### 必須機能

1. **投稿作成**: テキスト入力（必須）+ タグ入力でフィードに追加
2. **フィード表示**: 投稿を新しい順に一覧表示
3. **いいね**: 各投稿にいいねボタン（トグル式、カウント表示）
4. **コメント**: 各投稿にコメントを追加できる（折りたたみ表示）
5. **検索**: キーワードで投稿をフィルタ
6. **タグフィルタ**: タグクリックで該当投稿を絞り込み
7. **ダーク/ライトモード**: テーマ切替
8. **ユーザー切替**: 複数ユーザーから選択して投稿

### 設計要件

- **composable** を2つ以上作成する（`useFeed`、`useTheme` など）
- **provide / inject** でテーマと現在のユーザーを共有する
- コンポーネントは最低6つに分割する
- `computed` を3つ以上使用する
- `watch` を1つ以上使用する

---

## ステップガイド

<details>
<summary>ステップ1：データ構造を設計する</summary>

```js
// 投稿データ
const post = {
  id: 1,
  author: "太郎",
  content: "Vue.jsの学習進捗をシェア！",
  tags: ["Vue", "学習"],
  likes: ["花子", "次郎"],      // いいねしたユーザー名の配列
  comments: [
    { id: 1, author: "花子", text: "すごいですね！", createdAt: "..." },
  ],
  createdAt: "2024-03-15T10:30:00",
}

// ユーザー
const users = ["太郎", "花子", "次郎", "四郎"]
```

</details>

<details>
<summary>ステップ2：composable を設計する</summary>

```js
// useFeed: フィードの状態管理
function useFeed() {
  const posts = ref([...初期データ])
  const searchQuery = ref("")
  const selectedTag = ref(null)

  const filteredPosts = computed(() => { /* フィルタ・ソート */ })
  const allTags = computed(() => { /* 全タグ抽出 */ })

  function addPost(content, tags, author) { /* 投稿追加 */ }
  function toggleLike(postId, userName) { /* いいねトグル */ }
  function addComment(postId, text, author) { /* コメント追加 */ }

  return { posts, searchQuery, selectedTag, filteredPosts, allTags, addPost, toggleLike, addComment }
}
```

</details>

<details>
<summary>ステップ3：コンポーネント構造を設計する</summary>

```
App（テーマ・ユーザー provide）
├── AppHeader（タイトル・ユーザー切替・テーマ切替）
├── PostForm（投稿フォーム）
├── FilterBar（検索・タグフィルタ）
├── PostList（投稿一覧）
│   └── PostCard（1投稿）
│       └── CommentSection（コメント一覧 + 入力）
└── StatsFooter（統計情報）
```

</details>

---

## 解答例

<details>
<summary>解答例（全体コード）</summary>

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>Vue Feed - SNS風フィードアプリ</title>
  <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
  <style>
    :root { --bg: #f0f2f5; --card: #fff; --text: #333; --sub: #888; --border: #e0e0e0; --primary: #1976d2; --hover: #f5f5f5; }
    .dark { --bg: #1a1a2e; --card: #16213e; --text: #e0e0e0; --sub: #8899aa; --border: #2a3a5a; --primary: #2d88ff; --hover: #1c2d4a; }
    * { margin: 0; padding: 0; box-sizing: border-box; transition: background 0.3s, color 0.3s; }
    body { font-family: sans-serif; background: var(--bg); color: var(--text); }
    #app { max-width: 600px; margin: 0 auto; padding: 16px; }
    .card { background: var(--card); border-radius: 12px; padding: 16px; margin-bottom: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
    .header { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; margin-bottom: 12px; }
    .header h1 { font-size: 20px; }
    .header-actions { display: flex; align-items: center; gap: 8px; }
    .icon-btn { background: none; border: 1px solid var(--border); border-radius: 8px; padding: 6px 10px; cursor: pointer; color: var(--text); font-size: 14px; }
    .tag { display: inline-block; padding: 2px 10px; background: var(--primary); color: white; border-radius: 12px; font-size: 11px; margin: 2px; cursor: pointer; }
    .tag.inactive { background: var(--border); color: var(--text); }
  </style>
</head>
<body>
  <div id="app" :class="{ dark: isDark }">
    <!-- ヘッダー -->
    <app-header></app-header>

    <!-- 投稿フォーム -->
    <post-form @submit="handleNewPost"></post-form>

    <!-- フィルタバー -->
    <filter-bar
      :all-tags="feed.allTags.value"
      :search-query="feed.searchQuery.value"
      :selected-tag="feed.selectedTag.value"
      @update-search="feed.searchQuery.value = $event"
      @select-tag="feed.selectedTag.value = $event"
    ></filter-bar>

    <!-- 投稿一覧 -->
    <div v-if="feed.filteredPosts.value.length === 0" class="card" style="text-align: center; color: var(--sub); padding: 40px;">
      投稿が見つかりません
    </div>
    <post-card
      v-for="post in feed.filteredPosts.value"
      :key="post.id"
      :post="post"
      @toggle-like="feed.toggleLike($event, currentUser)"
      @add-comment="(postId, text) => feed.addComment(postId, text, currentUser)"
    ></post-card>

    <!-- 統計 -->
    <stats-footer :posts="feed.posts.value"></stats-footer>
  </div>

  <script>
    const { createApp, ref, reactive, computed, watch, provide, inject } = Vue

    // ==================== composable: useTheme ====================
    function useTheme() {
      const saved = localStorage.getItem('vueFeedTheme')
      const isDark = ref(saved === 'dark')
      watch(isDark, (val) => localStorage.setItem('vueFeedTheme', val ? 'dark' : 'light'))
      function toggle() { isDark.value = !isDark.value }
      return { isDark, toggle }
    }

    // ==================== composable: useFeed ====================
    function useFeed() {
      const posts = ref([
        {
          id: 1, author: "太郎",
          content: "Vue.jsの学習進捗をシェア！Composition APIが便利すぎる。refとreactiveの違いも理解できてきた。",
          tags: ["Vue", "学習"], likes: ["花子", "次郎", "四郎"],
          comments: [
            { id: 1, author: "花子", text: "すごいですね！私もComposition API勉強中です", createdAt: "2024-03-15T11:00:00" },
            { id: 2, author: "次郎", text: "参考になります！", createdAt: "2024-03-15T11:30:00" },
          ],
          createdAt: "2024-03-15T10:30:00"
        },
        {
          id: 2, author: "花子",
          content: "CSSの新しいコンテナクエリを試してみました。レスポンシブデザインが劇的に楽になりそう！",
          tags: ["CSS", "フロントエンド"], likes: ["太郎"],
          comments: [
            { id: 3, author: "太郎", text: "コンテナクエリ気になってました！", createdAt: "2024-03-14T16:00:00" },
          ],
          createdAt: "2024-03-14T15:00:00"
        },
        {
          id: 3, author: "次郎",
          content: "TypeScriptの型パズルにハマっています。ジェネリクスが深い...",
          tags: ["TypeScript", "学習"], likes: [],
          comments: [],
          createdAt: "2024-03-13T09:00:00"
        },
        {
          id: 4, author: "四郎",
          content: "Piniaの状態管理がシンプルで驚きました。Vuexからの移行も簡単でした。",
          tags: ["Vue", "Pinia"], likes: ["太郎", "花子"],
          comments: [
            { id: 4, author: "太郎", text: "Pinia最高ですよね！DevToolsとの連携が特に良い", createdAt: "2024-03-12T20:00:00" },
          ],
          createdAt: "2024-03-12T18:00:00"
        },
      ])

      const searchQuery = ref("")
      const selectedTag = ref(null)

      const allTags = computed(() => {
        const tagSet = new Set()
        posts.value.forEach(p => p.tags.forEach(t => tagSet.add(t)))
        return [...tagSet].sort()
      })

      const filteredPosts = computed(() => {
        let result = [...posts.value]

        if (searchQuery.value.trim()) {
          const q = searchQuery.value.trim().toLowerCase()
          result = result.filter(p =>
            p.content.toLowerCase().includes(q) || p.author.toLowerCase().includes(q)
          )
        }

        if (selectedTag.value) {
          result = result.filter(p => p.tags.includes(selectedTag.value))
        }

        // 新しい順
        result.sort((a, b) => b.createdAt.localeCompare(a.createdAt))
        return result
      })

      function addPost(content, tags, author) {
        posts.value.unshift({
          id: Date.now(),
          author: author,
          content: content,
          tags: tags,
          likes: [],
          comments: [],
          createdAt: new Date().toISOString()
        })
      }

      function toggleLike(postId, userName) {
        const post = posts.value.find(p => p.id === postId)
        if (!post) return
        const index = post.likes.indexOf(userName)
        if (index >= 0) {
          post.likes.splice(index, 1)
        } else {
          post.likes.push(userName)
        }
      }

      function addComment(postId, text, author) {
        const post = posts.value.find(p => p.id === postId)
        if (!post) return
        post.comments.push({
          id: Date.now(),
          author: author,
          text: text,
          createdAt: new Date().toISOString()
        })
      }

      function deletePost(postId) {
        posts.value = posts.value.filter(p => p.id !== postId)
      }

      return { posts, searchQuery, selectedTag, allTags, filteredPosts, addPost, toggleLike, addComment, deletePost }
    }

    // ==================== utility ====================
    function timeAgo(dateStr) {
      const diff = Date.now() - new Date(dateStr).getTime()
      const min = Math.floor(diff / 60000)
      if (min < 1) return "たった今"
      if (min < 60) return min + "分前"
      const hours = Math.floor(min / 60)
      if (hours < 24) return hours + "時間前"
      const days = Math.floor(hours / 24)
      return days + "日前"
    }

    // ==================== App ====================
    const app = createApp({
      setup() {
        const { isDark, toggle: toggleTheme } = useTheme()
        const feed = useFeed()
        const users = ["太郎", "花子", "次郎", "四郎"]
        const currentUser = ref("太郎")

        provide("isDark", isDark)
        provide("toggleTheme", toggleTheme)
        provide("currentUser", currentUser)
        provide("users", users)
        provide("timeAgo", timeAgo)

        function handleNewPost(data) {
          feed.addPost(data.content, data.tags, currentUser.value)
        }

        return { isDark, feed, currentUser, handleNewPost }
      }
    })

    // ==================== AppHeader ====================
    app.component('app-header', {
      setup() {
        const isDark = inject("isDark")
        const toggleTheme = inject("toggleTheme")
        const currentUser = inject("currentUser")
        const users = inject("users")
        return { isDark, toggleTheme, currentUser, users }
      },
      template: `
        <div class="header">
          <h1>📱 Vue Feed</h1>
          <div class="header-actions">
            <select :value="currentUser" @change="currentUser = $event.target.value"
              style="padding: 6px 10px; border: 1px solid var(--border); border-radius: 8px; background: var(--card); color: var(--text); font-size: 13px;">
              <option v-for="u in users" :key="u" :value="u">{{ u }}</option>
            </select>
            <button class="icon-btn" @click="toggleTheme">{{ isDark ? '☀️' : '🌙' }}</button>
          </div>
        </div>
      `
    })

    // ==================== PostForm ====================
    app.component('post-form', {
      emits: ['submit'],
      setup(props, { emit }) {
        const content = ref("")
        const tagInput = ref("")
        const tags = ref([])

        function addTag() {
          const t = tagInput.value.trim().replace(/^#/, '')
          if (t && !tags.value.includes(t)) { tags.value.push(t) }
          tagInput.value = ""
        }
        function removeTag(tag) { tags.value = tags.value.filter(t => t !== tag) }
        function submit() {
          if (!content.value.trim()) return
          emit('submit', { content: content.value.trim(), tags: [...tags.value] })
          content.value = ""
          tags.value = []
        }
        return { content, tagInput, tags, addTag, removeTag, submit }
      },
      template: `
        <div class="card">
          <textarea v-model="content" placeholder="今何してる？" rows="3"
            style="width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 8px; background: var(--bg); color: var(--text); font-size: 14px; resize: vertical; box-sizing: border-box;"></textarea>
          <div style="display: flex; gap: 6px; margin-top: 8px; flex-wrap: wrap;">
            <span class="tag" v-for="tag in tags" :key="tag" @click="removeTag(tag)">
              #{{ tag }} ✗
            </span>
          </div>
          <div style="display: flex; gap: 8px; margin-top: 8px; align-items: center;">
            <input v-model="tagInput" @keyup.enter="addTag" placeholder="#タグを追加"
              style="flex: 1; padding: 8px; border: 1px solid var(--border); border-radius: 8px; background: var(--bg); color: var(--text); font-size: 13px;" />
            <button @click="addTag" class="icon-btn">🏷️</button>
            <button @click="submit" :disabled="!content.trim()"
              :style="{
                padding: '8px 20px', border: 'none', borderRadius: '8px', cursor: content.trim() ? 'pointer' : 'default',
                background: content.trim() ? 'var(--primary)' : 'var(--border)', color: 'white', fontWeight: 'bold', fontSize: '13px'
              }">投稿する</button>
          </div>
        </div>
      `
    })

    // ==================== FilterBar ====================
    app.component('filter-bar', {
      props: ['allTags', 'searchQuery', 'selectedTag'],
      emits: ['update-search', 'select-tag'],
      template: `
        <div class="card" style="padding: 12px 16px;">
          <input :value="searchQuery" @input="$emit('update-search', $event.target.value)" placeholder="キーワードで検索..."
            style="width: 100%; padding: 8px 12px; border: 1px solid var(--border); border-radius: 8px; background: var(--bg); color: var(--text); font-size: 13px; margin-bottom: 8px; box-sizing: border-box;" />
          <div style="display: flex; gap: 4px; flex-wrap: wrap;">
            <span class="tag" :class="{ inactive: selectedTag !== null }" @click="$emit('select-tag', null)" style="font-size: 12px;">全て</span>
            <span class="tag" v-for="tag in allTags" :key="tag" :class="{ inactive: selectedTag !== tag }"
              @click="$emit('select-tag', selectedTag === tag ? null : tag)" style="font-size: 12px;">#{{ tag }}</span>
          </div>
        </div>
      `
    })

    // ==================== PostCard ====================
    app.component('post-card', {
      props: ['post'],
      emits: ['toggle-like', 'add-comment'],
      setup(props) {
        const currentUser = inject("currentUser")
        const timeAgo = inject("timeAgo")
        const showComments = ref(false)
        const commentText = ref("")

        const isLiked = computed(() => props.post.likes.includes(currentUser.value))

        function submitComment() {
          if (!commentText.value.trim()) return
          // emitは setup の第2引数からも取れるが、ここではテンプレート側で emit する
        }

        return { currentUser, timeAgo, showComments, commentText, isLiked }
      },
      template: `
        <div class="card">
          <!-- ヘッダー -->
          <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <div style="width: 36px; height: 36px; border-radius: 50%; background: var(--primary); color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px;">{{ post.author[0] }}</div>
              <strong>{{ post.author }}</strong>
            </div>
            <span style="color: var(--sub); font-size: 12px;">{{ timeAgo(post.createdAt) }}</span>
          </div>

          <!-- 本文 -->
          <p style="margin-bottom: 10px; line-height: 1.6;">{{ post.content }}</p>

          <!-- タグ -->
          <div v-if="post.tags.length > 0" style="margin-bottom: 10px;">
            <span class="tag" v-for="tag in post.tags" :key="tag">#{{ tag }}</span>
          </div>

          <!-- アクションバー -->
          <div style="display: flex; gap: 16px; align-items: center; padding-top: 8px; border-top: 1px solid var(--border);">
            <button @click="$emit('toggle-like', post.id)"
              :style="{ background: 'none', border: 'none', cursor: 'pointer', color: isLiked ? '#e91e63' : 'var(--sub)', fontSize: '14px' }">
              {{ isLiked ? '❤️' : '🤍' }} {{ post.likes.length }}
            </button>
            <button @click="showComments = !showComments"
              style="background: none; border: none; cursor: pointer; color: var(--sub); font-size: 14px;">
              💬 {{ post.comments.length }}
            </button>
          </div>

          <!-- コメントセクション -->
          <div v-if="showComments" style="margin-top: 12px; padding-top: 8px; border-top: 1px solid var(--border);">
            <div v-for="comment in post.comments" :key="comment.id"
              style="padding: 8px; margin-bottom: 6px; background: var(--bg); border-radius: 8px; font-size: 13px;">
              <strong>{{ comment.author }}</strong>
              <span style="color: var(--sub); font-size: 11px; margin-left: 6px;">{{ timeAgo(comment.createdAt) }}</span>
              <p style="margin-top: 4px;">{{ comment.text }}</p>
            </div>
            <div style="display: flex; gap: 8px; margin-top: 8px;">
              <input v-model="commentText" @keyup.enter="submitLocalComment" placeholder="コメントを入力..."
                style="flex: 1; padding: 8px; border: 1px solid var(--border); border-radius: 8px; background: var(--bg); color: var(--text); font-size: 13px;" />
              <button @click="submitLocalComment"
                :style="{ padding: '8px 14px', border: 'none', borderRadius: '8px', cursor: 'pointer', background: 'var(--primary)', color: 'white', fontSize: '13px' }">送信</button>
            </div>
          </div>
        </div>
      `,
      methods: {
        submitLocalComment() {
          if (!this.commentText.trim()) return
          this.$emit('add-comment', this.post.id, this.commentText.trim())
          this.commentText = ""
        }
      }
    })

    // ==================== StatsFooter ====================
    app.component('stats-footer', {
      props: ['posts'],
      setup(props) {
        const totalLikes = computed(() => props.posts.reduce((s, p) => s + p.likes.length, 0))
        const totalComments = computed(() => props.posts.reduce((s, p) => s + p.comments.length, 0))
        return { totalLikes, totalComments }
      },
      template: `
        <div style="text-align: center; padding: 16px; color: var(--sub); font-size: 12px;">
          {{ posts.length }}件の投稿 · ❤️ {{ totalLikes }} いいね · 💬 {{ totalComments }} コメント
        </div>
      `
    })

    app.mount('#app')
  </script>
</body>
</html>
```

</details>

<details>
<summary>設計ポイントの解説</summary>

### 1. composable によるロジック分離

| composable | 責務 |
|---|---|
| `useTheme` | ダーク/ライトモードの管理、localStorage永続化 |
| `useFeed` | 投稿データのCRUD、フィルタリング、ソート |

### 2. provide / inject の活用

| キー | 内容 | 利用先 |
|---|---|---|
| `isDark` | テーマ状態 | AppHeader |
| `toggleTheme` | テーマ切替関数 | AppHeader |
| `currentUser` | 現在のユーザー名 | AppHeader, PostCard |
| `users` | ユーザー一覧 | AppHeader |
| `timeAgo` | 時間表示ユーティリティ | PostCard |

### 3. コンポーネント間通信

- **親 → 子**: `props`（PostCard の `post` など）
- **子 → 親**: `$emit`（PostForm の `submit`、PostCard の `toggle-like` など）
- **グローバル**: `provide` / `inject`（テーマ、ユーザー）

### 4. computed の活用

- `filteredPosts`: 検索 + タグフィルタ + ソート
- `allTags`: 全投稿からユニークタグを抽出
- `isLiked`: 現在ユーザーがいいね済みかどうか
- `totalLikes` / `totalComments`: 統計集計

### よくある間違い

- **`v-for` で `:key` を忘れる** → コメント追加時に表示がおかしくなる
- **`push` / `splice` で配列を直接操作** → Vue 3のProxyは検知できるが、意図しない変更に注意
- **`provide` にリアクティブでない値を渡す** → テーマ切替が子に反映されない

</details>

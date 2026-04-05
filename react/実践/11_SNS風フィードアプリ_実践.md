# 実践課題11：SNS風フィードアプリ ★5

> **難易度**: ★★★★★（総合）
> **前提知識**: 第1章〜第10章（全章の知識を総合的に活用）
> **課題の種類**: ミニプロジェクト（総合設計）
> **学習目標**: コンポーネント設計、state管理（useReducer）、Context、カスタムフック、パフォーマンス最適化を統合して実務レベルのアプリを構築する

---

## 完成イメージ

```
┌────────────────────────���────────────────┐
│ 📱 SNS Feed           [🌙] [太郎 ▼]    │
├─────────────────────────────────────────┤
│                                         │
│ ┌─ 新規投稿 ─────────────────────────┐  │
│ │ [今何してる？                     ] │  │
│ │                        [投稿する]  │  │
│ └───────────────────────────────────┘  │
│                                         │
│ ┌─ 花子 ── 2分前 ──────────────────┐  │
│ │ Reactの勉強が楽しい！             │  │
│ │ ♡ 5  💬 2  🔄 1                   │  │
│ │ ┌─ コメント ──────────────────┐   │  │
│ │ │ 太郎: いいね！              │   │  │
│ │ │ 次郎: 僕も始めました        │   │  │
│ │ └────────────────────────────┘   │  │
│ └───────────────────────────────────┘  │
│                                         │
│ ┌─ 太郎 ── 1時間前 ────────────────┐  │
│ │ 今日のランチは最高でした 🍕        │  │
│ │ ♡ 12  💬 0  🔄 3                  │  │
│ └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

---

## 課題の要件

### 必須機能

1. **投稿一覧**: 投稿を新しい順で表示（ユーザー名・内容・日時・いいね数・コメント数）
2. **新規投稿**: テキスト入力で投稿を追加（空は不可）
3. **いいね**: 各投稿にいいねボタン（トグル式、自分がいいねしたか表示）
4. **コメント**: 各投稿にコメントを追加・表示
5. **ダーク/ライトモード**: Context でテーマ切替
6. **ユーザー切替**: 複数ユーザーを切り替えて投稿・いいね可能

### 設計要件

- **useReducer** で投稿データを管理する
- **Context** でテーマとユーザー情報を管理する
- **カスタムフック** を最低2つ作成する（例: `useTimeAgo`, `usePosts`）
- **React.memo** で不要な再レンダリングを防ぐ（最低1コンポーネント）
- コンポーネントは最低6つに分割する

---

## ステップガイド

<details>
<summary>ステップ1：データ構造とReducerを設計する</summary>

```jsx
const initialState = {
  posts: [
    {
      id: 1,
      userId: "hanako",
      content: "Reactの勉強が楽しい！",
      createdAt: Date.now() - 120000,
      likes: ["taro", "jiro"],
      comments: [
        { id: 1, userId: "taro", text: "いいね！", createdAt: Date.now() - 60000 },
      ],
    },
    // ...
  ],
};

function postsReducer(state, action) {
  switch (action.type) {
    case "ADD_POST": ...
    case "TOGGLE_LIKE": ...
    case "ADD_COMMENT": ...
    default: return state;
  }
}
```

</details>

<details>
<summary>ステップ2：Context を設計する</summary>

```jsx
// テーマ Context
const ThemeContext = React.createContext();

// ユーザー Context
const UserContext = React.createContext();

const USERS = {
  taro:   { name: "太郎", avatar: "🧑" },
  hanako: { name: "花子", avatar: "👩" },
  jiro:   { name: "次郎", avatar: "👦" },
};
```

</details>

<details>
<summary>ステップ3：useTimeAgo カスタムフックを作る</summary>

```jsx
function useTimeAgo(timestamp) {
  const [timeAgo, setTimeAgo] = React.useState("");

  React.useEffect(() => {
    function update() {
      var diff = Math.floor((Date.now() - timestamp) / 1000);
      if (diff < 60) setTimeAgo(diff + "秒前");
      else if (diff < 3600) setTimeAgo(Math.floor(diff / 60) + "分前");
      else if (diff < 86400) setTimeAgo(Math.floor(diff / 3600) + "時間前");
      else setTimeAgo(Math.floor(diff / 86400) + "日前");
    }
    update();
    var timer = setInterval(update, 60000);
    return () => clearInterval(timer);
  }, [timestamp]);

  return timeAgo;
}
```

</details>

<details>
<summary>ステップ4：コンポーネントを分割する</summary>

```
App
├── Header（テーマ切替、ユーザー切替）
├── PostForm（新規投稿フォーム）
├── PostList（投稿一覧）
│   └── PostCard（1つの投稿）
│       ├── LikeButton（いいねボタン）
│       └── CommentSection（コメント欄）
│           └── CommentItem（1つのコメント）
└── Footer
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
  <title>SNS風フィードアプリ</title>
  <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: sans-serif; }
  </style>
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">
    // ==================== 定数 ====================
    const USERS = {
      taro:   { name: "太郎", avatar: "🧑" },
      hanako: { name: "花子", avatar: "👩" },
      jiro:   { name: "次郎", avatar: "👦" },
    };

    const THEMES = {
      light: { bg: "#f0f2f5", card: "#fff", text: "#333", sub: "#666", border: "#ddd", headerBg: "#fff", accent: "#1877f2" },
      dark:  { bg: "#18191a", card: "#242526", text: "#e4e6eb", sub: "#b0b3b8", border: "#3e4042", headerBg: "#242526", accent: "#2d88ff" },
    };

    // ==================== Context ====================
    const ThemeContext = React.createContext();
    const UserContext = React.createContext();

    function useTheme() { return React.useContext(ThemeContext); }
    function useUser() { return React.useContext(UserContext); }

    // ==================== Reducer ====================
    const initialState = {
      posts: [
        { id: 1, userId: "hanako", content: "Reactの勉強が楽しい！", createdAt: Date.now() - 120000, likes: ["taro", "jiro"], comments: [{ id: 101, userId: "taro", text: "いいね！", createdAt: Date.now() - 60000 }, { id: 102, userId: "jiro", text: "僕も始めました", createdAt: Date.now() - 30000 }] },
        { id: 2, userId: "taro", content: "今日のランチは最高でした 🍕", createdAt: Date.now() - 3600000, likes: ["hanako", "jiro", "taro"], comments: [] },
        { id: 3, userId: "jiro", content: "週末はハイキングに行ってきます ⛰️", createdAt: Date.now() - 7200000, likes: ["hanako"], comments: [{ id: 201, userId: "hanako", text: "楽しんできてね！", createdAt: Date.now() - 3000000 }] },
      ],
    };

    function postsReducer(state, action) {
      switch (action.type) {
        case "ADD_POST":
          return { ...state, posts: [{ id: Date.now(), userId: action.payload.userId, content: action.payload.content, createdAt: Date.now(), likes: [], comments: [] }, ...state.posts] };
        case "TOGGLE_LIKE": {
          return { ...state, posts: state.posts.map(function(p) {
            if (p.id !== action.payload.postId) return p;
            var userId = action.payload.userId;
            var newLikes = p.likes.includes(userId) ? p.likes.filter(function(id) { return id !== userId; }) : [...p.likes, userId];
            return { ...p, likes: newLikes };
          })};
        }
        case "ADD_COMMENT":
          return { ...state, posts: state.posts.map(function(p) {
            if (p.id !== action.payload.postId) return p;
            return { ...p, comments: [...p.comments, { id: Date.now(), userId: action.payload.userId, text: action.payload.text, createdAt: Date.now() }] };
          })};
        default: return state;
      }
    }

    // ==================== カスタムフック ====================
    function useTimeAgo(timestamp) {
      const [text, setText] = React.useState("");
      React.useEffect(function() {
        function update() {
          var diff = Math.floor((Date.now() - timestamp) / 1000);
          if (diff < 60) setText(diff + "秒前");
          else if (diff < 3600) setText(Math.floor(diff / 60) + "分前");
          else if (diff < 86400) setText(Math.floor(diff / 3600) + "時間前");
          else setText(Math.floor(diff / 86400) + "日前");
        }
        update();
        var timer = setInterval(update, 60000);
        return function() { clearInterval(timer); };
      }, [timestamp]);
      return text;
    }

    // ==================== コンポーネント ====================
    function Header() {
      var theme = useTheme();
      var user = useUser();
      var colors = THEMES[theme.current];
      return (
        <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px 20px", background: colors.headerBg, borderBottom: "1px solid " + colors.border, position: "sticky", top: 0, zIndex: 10 }}>
          <h1 style={{ fontSize: 20, color: colors.accent }}>📱 SNS Feed</h1>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <button onClick={theme.toggle} style={{ background: "none", border: "none", fontSize: 20, cursor: "pointer" }}>
              {theme.current === "light" ? "🌙" : "☀️"}
            </button>
            <select value={user.currentId} onChange={function(e) { user.setCurrentId(e.target.value); }}
              style={{ padding: "4px 8px", borderRadius: 6, border: "1px solid " + colors.border, background: colors.card, color: colors.text }}>
              {Object.keys(USERS).map(function(id) { return <option key={id} value={id}>{USERS[id].avatar} {USERS[id].name}</option>; })}
            </select>
          </div>
        </header>
      );
    }

    function PostForm({ dispatch }) {
      var theme = useTheme();
      var user = useUser();
      var colors = THEMES[theme.current];
      const [text, setText] = React.useState("");

      function handleSubmit(e) {
        e.preventDefault();
        if (!text.trim()) return;
        dispatch({ type: "ADD_POST", payload: { userId: user.currentId, content: text.trim() } });
        setText("");
      }

      return (
        <form onSubmit={handleSubmit} style={{ background: colors.card, borderRadius: 8, padding: 16, marginBottom: 16, border: "1px solid " + colors.border }}>
          <div style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
            <span style={{ fontSize: 28 }}>{USERS[user.currentId].avatar}</span>
            <textarea value={text} onChange={function(e) { setText(e.target.value); }} placeholder="今何してる？"
              style={{ flex: 1, padding: 10, border: "1px solid " + colors.border, borderRadius: 8, resize: "vertical", minHeight: 60, background: colors.bg, color: colors.text, fontSize: 15 }} />
          </div>
          <div style={{ textAlign: "right", marginTop: 8 }}>
            <button type="submit" disabled={!text.trim()}
              style={{ padding: "8px 24px", background: text.trim() ? colors.accent : "#ccc", color: "white", border: "none", borderRadius: 6, cursor: text.trim() ? "pointer" : "default", fontSize: 14, fontWeight: "bold" }}>
              投稿する
            </button>
          </div>
        </form>
      );
    }

    function LikeButton({ post, dispatch }) {
      var user = useUser();
      var theme = useTheme();
      var colors = THEMES[theme.current];
      var isLiked = post.likes.includes(user.currentId);
      return (
        <button onClick={function() { dispatch({ type: "TOGGLE_LIKE", payload: { postId: post.id, userId: user.currentId } }); }}
          style={{ background: "none", border: "none", cursor: "pointer", color: isLiked ? "#e74c3c" : colors.sub, fontSize: 14 }}>
          {isLiked ? "❤️" : "♡"} {post.likes.length}
        </button>
      );
    }

    function CommentSection({ post, dispatch }) {
      var theme = useTheme();
      var user = useUser();
      var colors = THEMES[theme.current];
      const [showComments, setShowComments] = React.useState(false);
      const [commentText, setCommentText] = React.useState("");

      function handleAddComment(e) {
        e.preventDefault();
        if (!commentText.trim()) return;
        dispatch({ type: "ADD_COMMENT", payload: { postId: post.id, userId: user.currentId, text: commentText.trim() } });
        setCommentText("");
      }

      return (
        <div>
          <button onClick={function() { setShowComments(!showComments); }}
            style={{ background: "none", border: "none", cursor: "pointer", color: colors.sub, fontSize: 14 }}>
            💬 {post.comments.length}
          </button>
          {showComments && post.comments.length > 0 && (
            <div style={{ marginTop: 8, paddingTop: 8, borderTop: "1px solid " + colors.border }}>
              {post.comments.map(function(c) {
                return (
                  <div key={c.id} style={{ marginBottom: 6, fontSize: 13 }}>
                    <strong style={{ color: colors.accent }}>{USERS[c.userId] ? USERS[c.userId].name : c.userId}</strong>
                    <span style={{ color: colors.text, marginLeft: 6 }}>{c.text}</span>
                  </div>
                );
              })}
            </div>
          )}
          {showComments && (
            <form onSubmit={handleAddComment} style={{ display: "flex", gap: 6, marginTop: 8 }}>
              <input value={commentText} onChange={function(e) { setCommentText(e.target.value); }} placeholder="コメント..."
                style={{ flex: 1, padding: "6px 10px", border: "1px solid " + colors.border, borderRadius: 16, fontSize: 13, background: colors.bg, color: colors.text }} />
              <button type="submit" style={{ padding: "6px 12px", background: colors.accent, color: "white", border: "none", borderRadius: 16, fontSize: 12, cursor: "pointer" }}>送信</button>
            </form>
          )}
        </div>
      );
    }

    var PostCard = React.memo(function PostCard({ post, dispatch }) {
      var theme = useTheme();
      var colors = THEMES[theme.current];
      var timeAgo = useTimeAgo(post.createdAt);
      var author = USERS[post.userId] || { name: post.userId, avatar: "👤" };

      return (
        <div style={{ background: colors.card, borderRadius: 8, padding: 16, marginBottom: 12, border: "1px solid " + colors.border }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
            <span style={{ fontSize: 28 }}>{author.avatar}</span>
            <div>
              <div style={{ fontWeight: "bold", color: colors.text }}>{author.name}</div>
              <div style={{ fontSize: 12, color: colors.sub }}>{timeAgo}</div>
            </div>
          </div>
          <p style={{ color: colors.text, lineHeight: 1.6, marginBottom: 12, fontSize: 15 }}>{post.content}</p>
          <div style={{ display: "flex", gap: 16 }}>
            <LikeButton post={post} dispatch={dispatch} />
            <CommentSection post={post} dispatch={dispatch} />
          </div>
        </div>
      );
    });

    // ==================== App ====================
    function App() {
      const [state, dispatch] = React.useReducer(postsReducer, initialState);
      const [theme, setTheme] = React.useState("light");
      const [currentUserId, setCurrentUserId] = React.useState("taro");

      var themeValue = { current: theme, toggle: function() { setTheme(function(t) { return t === "light" ? "dark" : "light"; }); } };
      var userValue = { currentId: currentUserId, setCurrentId: setCurrentUserId };
      var colors = THEMES[theme];

      return (
        <ThemeContext.Provider value={themeValue}>
          <UserContext.Provider value={userValue}>
            <div style={{ minHeight: "100vh", background: colors.bg, transition: "background 0.3s" }}>
              <Header />
              <main style={{ maxWidth: 600, margin: "0 auto", padding: 20 }}>
                <PostForm dispatch={dispatch} />
                {state.posts.map(function(post) {
                  return <PostCard key={post.id} post={post} dispatch={dispatch} />;
                })}
              </main>
            </div>
          </UserContext.Provider>
        </ThemeContext.Provider>
      );
    }

    ReactDOM.createRoot(document.getElementById("root")).render(<App />);
  </script>
</body>
</html>
```

</details>

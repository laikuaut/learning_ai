# 第1章：Vue.jsの基本

## 1.1 Vue.jsとは何か

Vue.js（ビュー）は、ユーザーインターフェースを構築するためのプログレッシブJavaScriptフレームワークです。「プログレッシブ」とは、小さなウィジェットから大規模なSPA（Single Page Application）まで、必要に応じて段階的に機能を追加できることを意味します。

### Vue.jsの特徴

| 特徴 | 説明 |
|------|------|
| リアクティブ | データの変更がUIに自動反映される |
| コンポーネント指向 | UIを再利用可能な部品に分割できる |
| Composition API | ロジックを関数として整理・再利用できる |
| 軽量・高速 | 仮想DOMによる効率的な描画更新 |
| エコシステム | Vue Router、Pinia、Vite との統合 |

### Vue 3 と Vue 2 の主な違い

- **Composition API** が標準（Options API も引き続き利用可能）
- **`<script setup>`** による簡潔な記法
- **パフォーマンス向上** — 仮想DOMの最適化、Tree-shaking対応
- **TypeScript** のネイティブサポート強化
- **Teleport、Suspense、Fragment** などの新機能

---

## 1.2 開発環境のセットアップ（Vite）

Vue 3 の公式推奨ビルドツールは **Vite**（ヴィート）です。

### 前提条件

- **Node.js** 18.0 以上がインストール済みであること
- ターミナル（コマンドプロンプト、PowerShell、Git Bash など）

```bash
# Node.js のバージョン確認
node --version
# v18.0.0 以上であることを確認

# npm のバージョン確認
npm --version
```

### プロジェクトの作成

```bash
# Vite で Vue プロジェクトを作成
npm create vue@latest

# 対話形式で設定を選択：
# ✔ Project name: … my-vue-app
# ✔ Add TypeScript? … No（最初はNoでOK）
# ✔ Add JSX Support? … No
# ✔ Add Vue Router? … No（第7章で追加）
# ✔ Add Pinia? … No（第8章で追加）
# ✔ Add Vitest? … No
# ✔ Add ESLint? … Yes
# ✔ Add Prettier? … Yes

# プロジェクトに移動して依存関係をインストール
cd my-vue-app
npm install

# 開発サーバーを起動
npm run dev
```

ブラウザで `http://localhost:5173` を開くと、Vueの初期画面が表示されます。

### プロジェクト構造

```
my-vue-app/
├── node_modules/       # 依存パッケージ
├── public/             # 静的ファイル
│   └── favicon.ico
├── src/                # ソースコード
│   ├── assets/         # CSS、画像など
│   ├── components/     # コンポーネント
│   ├── App.vue         # ルートコンポーネント
│   └── main.js         # エントリーポイント
├── index.html          # HTMLテンプレート
├── package.json        # プロジェクト設定
└── vite.config.js      # Vite設定
```

---

## 1.3 createApp — アプリケーションの起点

Vueアプリケーションは `createApp` 関数で作成します。

### main.js（エントリーポイント）

```js
// main.js
import { createApp } from 'vue'  // Vue から createApp をインポート
import App from './App.vue'       // ルートコンポーネントをインポート

// アプリケーションインスタンスを作成し、#app要素にマウント
const app = createApp(App)
app.mount('#app')

// 上記は以下のようにチェーンで書くことも可能
// createApp(App).mount('#app')
```

### index.html

```html
<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vue アプリ</title>
  </head>
  <body>
    <!-- Vue がこの要素を制御する -->
    <div id="app"></div>
    <!-- Vite がスクリプトを挿入 -->
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

### createApp の流れ

```
createApp(App)    →  アプリケーションインスタンスを作成
  .use(router)    →  プラグインを登録（任意）
  .use(pinia)     →  状態管理を登録（任意）
  .mount('#app')  →  DOM要素にマウント（描画開始）
```

---

## 1.4 テンプレート構文の基本

Vueのテンプレートは、HTML拡張構文を使ってデータを画面に表示します。

### マスタッシュ構文 {{ }}（テキスト展開）

```vue
<script setup>
import { ref } from 'vue'

const message = ref('こんにちは、Vue!')
const count = ref(42)
</script>

<template>
  <!-- 変数の値をテキストとして表示 -->
  <h1>{{ message }}</h1>

  <!-- JavaScript式を書ける -->
  <p>カウント: {{ count }}</p>
  <p>2倍: {{ count * 2 }}</p>
  <p>大文字: {{ message.toUpperCase() }}</p>

  <!-- 三項演算子もOK -->
  <p>{{ count > 10 ? '多い' : '少ない' }}</p>
</template>
```

**重要なルール：**
- `{{ }}` の中には **JavaScript式** を書ける（値を返すもの）
- **文（statement）** は書けない（`if`、`for`、`let` など）
- 関数呼び出しは可能だが、副作用のある関数は避ける

```vue
<!-- OK: 式 -->
{{ number + 1 }}
{{ ok ? 'はい' : 'いいえ' }}
{{ message.split('').reverse().join('') }}

<!-- NG: 文 -->
{{ let x = 1 }}          <!-- エラー -->
{{ if (ok) { return 1 } }} <!-- エラー -->
```

---

## 1.5 v-bind — 属性のバインディング

HTML属性に動的な値を設定するには `v-bind` ディレクティブを使います。

```vue
<script setup>
import { ref } from 'vue'

const imageUrl = ref('/images/logo.png')
const altText = ref('Vue.jsロゴ')
const linkUrl = ref('https://vuejs.org')
const isDisabled = ref(true)
const inputId = ref('username')
</script>

<template>
  <!-- v-bind:属性名="式" -->
  <img v-bind:src="imageUrl" v-bind:alt="altText" />

  <!-- 省略記法 :属性名="式"（実務ではこちらが主流） -->
  <img :src="imageUrl" :alt="altText" />

  <!-- さまざまな属性をバインド -->
  <a :href="linkUrl">公式サイト</a>
  <button :disabled="isDisabled">送信</button>
  <label :for="inputId">ユーザー名</label>
  <input :id="inputId" type="text" />
</template>
```

### クラスのバインディング

```vue
<script setup>
import { ref } from 'vue'

const isActive = ref(true)
const hasError = ref(false)
const activeClass = ref('active')
</script>

<template>
  <!-- オブジェクト構文：条件に応じてクラスを切り替え -->
  <div :class="{ active: isActive, 'text-danger': hasError }">
    条件付きクラス
  </div>

  <!-- 配列構文：複数のクラスを指定 -->
  <div :class="[activeClass, 'base-class']">
    配列クラス
  </div>

  <!-- 静的classとの併用も可能 -->
  <div class="static-class" :class="{ active: isActive }">
    混合クラス
  </div>
</template>
```

### スタイルのバインディング

```vue
<script setup>
import { ref } from 'vue'

const textColor = ref('red')
const fontSize = ref(16)
</script>

<template>
  <!-- オブジェクト構文（キャメルケースを推奨） -->
  <p :style="{ color: textColor, fontSize: fontSize + 'px' }">
    動的スタイル
  </p>

  <!-- ケバブケースも可能（引用符で囲む） -->
  <p :style="{ 'font-size': fontSize + 'px' }">
    ケバブケース
  </p>
</template>
```

---

## 1.6 最初のVueコンポーネント

すべてを組み合わせて、最初のコンポーネントを作りましょう。

### App.vue

```vue
<script setup>
import { ref } from 'vue'

// リアクティブなデータ
const appName = ref('はじめてのVueアプリ')
const description = ref('Vue.js 3 を学習中です')
const version = ref(3)
const isNew = ref(true)
const logoUrl = ref('https://vuejs.org/images/logo.svg')
</script>

<template>
  <div class="app">
    <!-- テキスト展開 -->
    <h1>{{ appName }}</h1>
    <p>{{ description }}</p>

    <!-- 属性バインディング -->
    <img :src="logoUrl" :alt="appName" width="100" />

    <!-- 式の利用 -->
    <p>Vue バージョン: {{ version }}</p>
    <p>ステータス: {{ isNew ? '最新' : '旧バージョン' }}</p>

    <!-- クラスバインディング -->
    <span :class="{ badge: true, 'badge-new': isNew }">
      v{{ version }}
    </span>
  </div>
</template>

<style scoped>
.app {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  text-align: center;
  padding: 2rem;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
}

.badge-new {
  background-color: #42b883;
  color: white;
}
</style>
```

---

## 1.7 Vite の便利な機能

### ホットモジュールリプレースメント（HMR）

`npm run dev` で起動中は、ファイルを保存するだけでブラウザが自動更新されます。ページ全体のリロードではなく、変更されたモジュールだけが差し替えられるため、状態を維持したまま開発できます。

### エイリアス（パスの短縮）

```js
// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      // '@' で src ディレクトリを参照できる
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
```

```js
// エイリアスを使ったインポート
import MyComponent from '@/components/MyComponent.vue'
```

### ビルド（本番用）

```bash
# 本番用にビルド
npm run build

# dist/ フォルダに最適化されたファイルが出力される
# ビルド結果をプレビュー
npm run preview
```

---

## 1.8 本章のまとめ

| 概念 | 説明 |
|------|------|
| `createApp` | Vueアプリケーションインスタンスを作成する関数 |
| `.mount('#app')` | DOMにアプリケーションをマウント（描画開始） |
| `{{ }}` | テンプレート内でJavaScript式を評価しテキスト表示 |
| `v-bind` / `:` | HTML属性に動的な値をバインド |
| `:class` | 条件付きCSSクラスの適用 |
| `:style` | インラインスタイルの動的設定 |
| `ref()` | リアクティブなデータを作成（次章で詳解） |
| `<script setup>` | Composition API の簡潔な記法 |
| Vite | Vue公式推奨のビルドツール |

### 次章予告

第2章では、Vueの核心機能である **リアクティビティシステム** を詳しく学びます。`ref()`、`reactive()`、`computed()`、`watch()` などを使って、データの変更を自動的にUIに反映する仕組みを理解しましょう。

# 第1章 演習：Vue.jsの基本

> 対応教材: `教材/01_Vueの基本_教材.md`
>
> この演習では、Vueアプリケーションの作成、SFC（単一ファイルコンポーネント）の構造、
> テンプレート内でのデータ表示、イベントハンドリングの基礎を確認します。

---

## 演習1-1：はじめてのVueコンポーネント（基本）

### 問題

以下の要件を満たす `HelloVue.vue` コンポーネントを作成してください。

1. `greeting` という文字列のリアクティブ変数に `"こんにちは、Vue 3！"` を格納する
2. `author` というリアクティブ変数に自分の名前を格納する
3. テンプレートに `<h1>` で `greeting` を、`<p>` で `「作成者: ○○」` を表示する

### 期待される画面表示

```
こんにちは、Vue 3！
作成者: 太郎
```

<details>
<summary>ヒント</summary>

- `<script setup>` ブロック内で `ref()` を使ってリアクティブ変数を宣言します
- テンプレートでは `{{ 変数名 }}` のマスタッシュ構文でデータを表示します
- `ref` は `vue` パッケージからインポートします

</details>

<details>
<summary>解答例</summary>

```vue
<!-- HelloVue.vue -->
<script setup>
import { ref } from 'vue'

// リアクティブな変数を宣言
// ref() で包むことで、値が変更されたときにテンプレートが自動的に再描画される
const greeting = ref('こんにちは、Vue 3！')
const author = ref('太郎')
</script>

<template>
  <!-- マスタッシュ構文 {{ }} でリアクティブ変数の値を表示 -->
  <h1>{{ greeting }}</h1>
  <p>作成者: {{ author }}</p>
</template>

<style scoped>
/* scoped を付けると、このコンポーネントだけに適用されるスタイルになる */
h1 {
  color: #42b883; /* Vue のブランドカラー */
}
</style>
```

**ポイント解説:**
- `<script setup>` は Composition API の糖衣構文（シンタックスシュガー）です。`export default` や `setup()` を書く必要がありません。
- `ref()` で作った変数は、テンプレートでは自動的にアンラップされるため `.value` は不要です。
- `scoped` 属性を付けたスタイルは、そのコンポーネント内の要素にのみ適用されます。

</details>

---

## 演習1-2：クリックイベントの処理（基本）

### 問題

ボタンをクリックするたびにカウントが1ずつ増える `ClickCounter.vue` を作成してください。

**要件:**
1. `count` というリアクティブ変数を `0` で初期化する
2. `increment` 関数を定義し、`count` を1増やす
3. 画面に現在のカウントとボタンを表示する
4. ボタンのテキストは「クリック！」とする

<details>
<summary>ヒント</summary>

- イベントハンドリングには `@click` ディレクティブ（`v-on:click` の省略形）を使います
- `ref` の値を変更するには、`script` 内では `.value` プロパティにアクセスします
- テンプレートでは `.value` は不要です

</details>

<details>
<summary>解答例</summary>

```vue
<!-- ClickCounter.vue -->
<script setup>
import { ref } from 'vue'

// カウントの状態を管理するリアクティブ変数
const count = ref(0)

// ボタンクリック時に呼ばれる関数
function increment() {
  // script 内では .value を使ってリアクティブ変数の値にアクセスする
  count.value++
}
</script>

<template>
  <div class="counter">
    <!-- マスタッシュ構文でカウントを表示 -->
    <p>現在のカウント: {{ count }}</p>

    <!-- @click でクリックイベントをハンドリング -->
    <button @click="increment">クリック！</button>
  </div>
</template>

<style scoped>
.counter {
  text-align: center;
  padding: 20px;
}

button {
  padding: 8px 24px;
  font-size: 16px;
  cursor: pointer;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
}

button:hover {
  background-color: #369870;
}
</style>
```

**ポイント解説:**
- `@click="increment"` は `v-on:click="increment"` の省略記法です。Vue では `@` を使った省略形が一般的です。
- 関数名だけを渡す場合（`@click="increment"`）、関数が自動的に呼び出されます。引数を渡したい場合は `@click="increment(5)"` のように書きます。

</details>

---

## 演習1-3：バグ修正問題（基本）

### 問題

以下のコンポーネントには3つのバグがあります。すべて見つけて修正してください。

```vue
<script setup>
import { ref } from 'Vue'

const name = ref('太郎')
const age = ref(25)

function birthday() {
  age++
}
</script>

<template>
  <div>
    <p>名前: {{ name.value }}</p>
    <p>年齢: {{ age }}歳</p>
    <button @click="birthday">お誕生日おめでとう！</button>
  </div>
</template>
```

<details>
<summary>ヒント</summary>

1. Vue のインポート元のパッケージ名を確認してください
2. `ref` の値を変更する際の `.value` の使い方を確認してください
3. テンプレート内で `ref` の値を表示する際のルールを確認してください

</details>

<details>
<summary>解答例</summary>

**バグ1:** インポート元が `'Vue'`（大文字V）になっている → 正しくは `'vue'`（小文字v）

```js
// ❌ 間違い
import { ref } from 'Vue'
// ✅ 正しい
import { ref } from 'vue'
```

**バグ2:** `birthday` 関数内で `.value` を使っていない

```js
// ❌ 間違い — ref オブジェクト自体に ++ しても値は変わらない
age++
// ✅ 正しい — .value プロパティを通じて値を変更する
age.value++
```

**バグ3:** テンプレートで `.value` を付けてしまっている

```html
<!-- ❌ 間違い — テンプレートでは ref は自動アンラップされるので .value は不要 -->
<p>名前: {{ name.value }}</p>
<!-- ✅ 正しい -->
<p>名前: {{ name }}</p>
```

**修正後の完全なコード:**

```vue
<script setup>
import { ref } from 'vue'  /* バグ1修正: 'vue' は小文字 */

const name = ref('太郎')
const age = ref(25)

function birthday() {
  age.value++  /* バグ2修正: .value を付けて値にアクセス */
}
</script>

<template>
  <div>
    <p>名前: {{ name }}</p>  <!-- バグ3修正: テンプレートでは .value 不要 -->
    <p>年齢: {{ age }}歳</p>
    <button @click="birthday">お誕生日おめでとう！</button>
  </div>
</template>
```

**覚えておくべきルール:**
- `script` 内では `ref` の値にアクセスするとき `.value` が**必要**
- `template` 内では `ref` が自動的にアンラップされるので `.value` は**不要**

</details>

---

## 演習1-4：テンプレート内での式の活用（応用）

### 問題

商品情報を表示する `ProductCard.vue` を作成してください。

**要件:**
1. 以下のリアクティブ変数を定義する:
   - `productName`: `"Vue.js入門書"`
   - `price`: `2980`（数値）
   - `taxRate`: `0.1`（数値）
   - `inStock`: `true`（真偽値）
2. テンプレートで以下を表示する:
   - 商品名
   - 税込価格（`price * (1 + taxRate)` を計算し、`toLocaleString()` で桁区切り表示）
   - 在庫状態（`inStock` が `true` なら `"在庫あり"`, `false` なら `"在庫切れ"`）
3. 三項演算子をテンプレート内で使用する

<details>
<summary>ヒント</summary>

- テンプレートの `{{ }}` 内では JavaScript の式を書くことができます
- 三項演算子: `条件 ? 真の場合の値 : 偽の場合の値`
- `Math.floor()` で小数点以下を切り捨てられます
- `数値.toLocaleString()` で `"3,278"` のような桁区切り文字列になります

</details>

<details>
<summary>解答例</summary>

```vue
<!-- ProductCard.vue -->
<script setup>
import { ref } from 'vue'

// 商品データ
const productName = ref('Vue.js入門書')
const price = ref(2980)        // 税抜価格
const taxRate = ref(0.1)       // 消費税率（10%）
const inStock = ref(true)      // 在庫の有無
</script>

<template>
  <div class="product-card">
    <!-- 商品名の表示 -->
    <h2>{{ productName }}</h2>

    <!-- 税込価格の計算と桁区切り表示 -->
    <!-- テンプレート内で JavaScript の式を記述できる -->
    <p class="price">
      税込価格: ¥{{ Math.floor(price * (1 + taxRate)).toLocaleString() }}
    </p>

    <!-- 三項演算子で在庫状態を切り替え表示 -->
    <p :class="inStock ? 'in-stock' : 'out-of-stock'">
      {{ inStock ? '✓ 在庫あり' : '✗ 在庫切れ' }}
    </p>

    <!-- ボタンの活性/非活性も inStock に連動 -->
    <button :disabled="!inStock">
      {{ inStock ? 'カートに入れる' : '入荷をお知らせ' }}
    </button>
  </div>
</template>

<style scoped>
.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  max-width: 300px;
}

.price {
  font-size: 1.2em;
  font-weight: bold;
  color: #e53e3e;
}

.in-stock {
  color: #38a169;
}

.out-of-stock {
  color: #e53e3e;
}
</style>
```

**ポイント解説:**
- テンプレート内の `{{ }}` では、変数の参照だけでなく、計算式やメソッド呼び出しなどの JavaScript 式を記述できます。
- `:class`（`v-bind:class` の省略形）で動的にCSSクラスを切り替えることができます。
- `:disabled` で HTML の `disabled` 属性を動的に制御できます。
- ただし、テンプレート内に複雑な計算を書きすぎると可読性が下がるため、複雑な処理は `computed` を使うことが推奨されます（第2章で学びます）。

</details>

---

## 演習1-5：複数のイベントハンドリング（応用）

### 問題

簡易的なプロフィールエディタ `ProfileEditor.vue` を作成してください。

**要件:**
1. `name`（文字列）と `isEditing`（真偽値）のリアクティブ変数を用意する
2. `isEditing` が `false` のとき：名前を `<p>` タグで表示し、「編集」ボタンを表示する
3. `isEditing` が `true` のとき：名前を `<input>` タグで表示し、「保存」ボタンを表示する
4. 「編集」ボタンをクリックすると `isEditing` が `true` になる
5. 「保存」ボタンをクリックすると `isEditing` が `false` になる
6. 「リセット」ボタンで名前を初期値 `"ゲスト"` に戻す

<details>
<summary>ヒント</summary>

- `v-if` / `v-else` を使って表示を切り替えます
- `<input>` と `ref` の値を連動させるには `v-model` ディレクティブを使います（詳細は第6章で学びます）
- 複数の関数を定義して、それぞれのボタンに割り当てましょう

</details>

<details>
<summary>解答例</summary>

```vue
<!-- ProfileEditor.vue -->
<script setup>
import { ref } from 'vue'

// 状態管理用のリアクティブ変数
const name = ref('ゲスト')        // 表示名
const isEditing = ref(false)      // 編集モードかどうか

// 編集モードに切り替える
function startEditing() {
  isEditing.value = true
}

// 保存して表示モードに戻る
function save() {
  isEditing.value = false
}

// 名前を初期値にリセットする
function reset() {
  name.value = 'ゲスト'
  isEditing.value = false
}
</script>

<template>
  <div class="profile-editor">
    <h2>プロフィール</h2>

    <!-- 表示モード（isEditing が false のとき） -->
    <div v-if="!isEditing">
      <p>名前: {{ name }}</p>
      <button @click="startEditing">編集</button>
    </div>

    <!-- 編集モード（isEditing が true のとき） -->
    <div v-else>
      <label>
        名前:
        <!-- v-model で input の値と ref を双方向バインディング -->
        <input v-model="name" type="text" />
      </label>
      <button @click="save">保存</button>
    </div>

    <!-- リセットボタンは常に表示 -->
    <button @click="reset" class="reset-btn">リセット</button>
  </div>
</template>

<style scoped>
.profile-editor {
  padding: 20px;
  max-width: 400px;
}

input {
  padding: 4px 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  margin: 4px;
  padding: 6px 16px;
  cursor: pointer;
}

.reset-btn {
  background-color: #e53e3e;
  color: white;
  border: none;
  border-radius: 4px;
}
</style>
```

**ポイント解説:**
- `v-if` と `v-else` は**隣接する兄弟要素**でなければなりません。間に別の要素を挟むとエラーになります。
- `v-model` は `<input>` の `value` 属性と `input` イベントの双方向バインディングの省略記法です。ユーザーの入力がリアルタイムに `name.value` に反映されます。
- 関数名は目的が分かるように命名すると、テンプレートの可読性が上がります。

</details>

---

## 演習1-6：SFCの構造理解 — 設計問題（チャレンジ）

### 問題

あなたはECサイトの商品一覧ページを作ることになりました。以下の仕様を満たすコンポーネント設計を考えてください。

**画面仕様:**
- 画面上部にサイト名「Vue Shop」を表示するヘッダー
- 中央に商品カード（商品名、価格、画像URL）を3つ表示
- 各商品カードに「カートに追加」ボタン
- 画面下部にカート内の商品数を表示するフッター

**設問:**
1. この画面を構成するのに必要なコンポーネントをリストアップし、それぞれの責務を述べてください
2. `App.vue` のテンプレート部分の骨組みを `<script setup>` 形式で記述してください
3. 商品データ（3つ分）をどのように管理するか、コード例を示してください

<details>
<summary>ヒント</summary>

- コンポーネントは「単一責任の原則」に従い、1つのコンポーネントが1つの役割を持つようにします
- 商品データは配列として管理し、`v-for`（第3章で詳しく学びます）でループ表示するのが定石です
- カート内の商品数は `ref` で管理できます

</details>

<details>
<summary>解答例</summary>

**1. コンポーネント構成と責務**

| コンポーネント | 責務 |
|--------------|------|
| `App.vue` | 全体レイアウト、商品データとカート状態の管理 |
| `SiteHeader.vue` | サイト名やナビゲーションの表示 |
| `ProductCard.vue` | 個々の商品情報の表示とカート追加ボタン |
| `CartFooter.vue` | カート内の商品数の表示 |

**2. App.vue のコード例**

```vue
<!-- App.vue -->
<script setup>
import { ref } from 'vue'
import SiteHeader from './components/SiteHeader.vue'
import ProductCard from './components/ProductCard.vue'
import CartFooter from './components/CartFooter.vue'

// 商品データ（3. の回答を兼ねる）
// 実務ではAPIから取得するが、ここではハードコーディングで定義
const products = ref([
  {
    id: 1,
    name: 'Vue.js入門書',
    price: 2980,
    image: '/images/book-vue.jpg'
  },
  {
    id: 2,
    name: 'TypeScript実践ガイド',
    price: 3480,
    image: '/images/book-ts.jpg'
  },
  {
    id: 3,
    name: 'Web開発パーフェクトガイド',
    price: 4200,
    image: '/images/book-web.jpg'
  }
])

// カート内の商品数
const cartCount = ref(0)

// カートに追加する関数
function addToCart() {
  cartCount.value++
}
</script>

<template>
  <div class="app">
    <!-- ヘッダー -->
    <SiteHeader />

    <!-- 商品一覧 -->
    <main class="product-list">
      <!--
        v-for で配列をループして商品カードを表示
        :key はVueがDOM要素を効率的に更新するために必要な一意の識別子
      -->
      <ProductCard
        v-for="product in products"
        :key="product.id"
        :name="product.name"
        :price="product.price"
        :image="product.image"
        @add-to-cart="addToCart"
      />
    </main>

    <!-- フッター -->
    <CartFooter :count="cartCount" />
  </div>
</template>

<style scoped>
.product-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  padding: 20px;
}
</style>
```

**ポイント解説:**
- 商品データは**配列のオブジェクト**として管理するのが一般的です。各商品に `id` を持たせると、`v-for` の `:key` に使えます。
- `:name="product.name"` は props（親→子へのデータ渡し）で、第4章で詳しく学びます。
- `@add-to-cart="addToCart"` はカスタムイベント（子→親への通知）で、第4章で詳しく学びます。
- この段階ではすべてを理解する必要はありません。「コンポーネントの分割単位」と「データの管理場所」を意識する練習です。

</details>

---

## 演習1-7：createApp とプラグイン（チャレンジ）

### 問題

以下の `main.js` を読んで、設問に答えてください。

```js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import HomeView from './views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomeView }
  ]
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
```

**設問:**
1. `createApp(App)` は何をしていますか？
2. `app.use()` は何をしていますか？この例では何を登録していますか？
3. `app.mount('#app')` の `'#app'` は何を指していますか？
4. `app.use()` と `app.mount()` の呼び出し順序を入れ替えるとどうなりますか？

<details>
<summary>ヒント</summary>

- `createApp` は Vue アプリケーションのインスタンスを生成する関数です
- `app.use()` はプラグイン（追加機能）を登録するメソッドです
- `app.mount()` は実際の DOM 要素にアプリケーションを紐づけます
- プラグインの登録は mount の前に行う必要があります

</details>

<details>
<summary>解答例</summary>

**1. `createApp(App)` について**

`App` コンポーネントをルート（最上位）コンポーネントとして、Vueアプリケーションインスタンスを生成しています。この時点ではまだ画面には何も表示されません。アプリケーションの「設計図」を作っている段階です。

**2. `app.use()` について**

`app.use()` はプラグイン（外部ライブラリや追加機能）をアプリケーションに登録するメソッドです。

この例では以下の2つを登録しています:
- `createPinia()` — 状態管理ライブラリ Pinia（第8章で詳しく学ぶ）
- `router` — ルーティングライブラリ Vue Router（第7章で詳しく学ぶ）

プラグインを `use()` で登録すると、アプリケーション全体のどのコンポーネントからでもその機能を利用できるようになります。

**3. `app.mount('#app')` について**

`'#app'` は CSS セレクターで、`index.html` 内の `<div id="app"></div>` 要素を指しています。この DOM 要素の中に Vue アプリケーションがレンダリングされます。

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
  <body>
    <div id="app"></div>  <!-- ← ここに Vue アプリが描画される -->
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

**4. 呼び出し順序の入れ替えについて**

`app.mount()` を先に呼ぶと、プラグインが登録されていない状態でアプリケーションが描画されるため、Router や Pinia を使っているコンポーネントでエラーが発生します。**プラグインの登録は必ず `mount()` の前に行う**必要があります。

```js
// ✅ 正しい順序
app.use(createPinia())  // 1. プラグイン登録
app.use(router)         // 2. プラグイン登録
app.mount('#app')       // 3. マウント（最後に実行）

// ❌ 間違い — mount 後の use は反映されない
app.mount('#app')
app.use(createPinia())  // ⚠ 警告が出る
```

</details>

---

## まとめ

| 演習 | レベル | 学習ポイント |
|------|--------|-------------|
| 1-1 | 基本 | SFC構造、ref、マスタッシュ構文 |
| 1-2 | 基本 | イベントハンドリング、@click |
| 1-3 | 基本 | よくあるバグパターンの理解 |
| 1-4 | 応用 | テンプレート内の式、動的バインディング |
| 1-5 | 応用 | v-if/v-else、v-model、複数関数 |
| 1-6 | チャレンジ | コンポーネント設計の考え方 |
| 1-7 | チャレンジ | createApp、プラグイン、mount の理解 |

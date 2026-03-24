# 第1章 演習：Next.js の基本

---

## 演習1（基本）：Next.js プロジェクトを作成しよう

ターミナルを使って新しい Next.js プロジェクトを作成し、開発サーバーを起動してください。

**要件：**
- プロジェクト名は `my-first-nextjs` とする
- TypeScript、App Router を有効にする
- 開発サーバーを起動して `http://localhost:3000` にアクセスし、初期画面が表示されることを確認する

<details>
<summary>ヒント</summary>

`npx create-next-app@latest` コマンドを実行し、対話式の質問に答えます。App Router は「Yes」を選択してください。

</details>

<details>
<summary>解答例</summary>

```bash
# プロジェクトの作成
npx create-next-app@latest my-first-nextjs

# 対話式の選択肢（推奨）
# TypeScript → Yes
# ESLint → Yes
# Tailwind CSS → Yes
# src/ directory → Yes（好みによる）
# App Router → Yes（必須）
# Turbopack → Yes
# import alias → No

# プロジェクトに移動して開発サーバーを起動
cd my-first-nextjs
npm run dev
```

ブラウザで `http://localhost:3000` にアクセスすると、Next.js の初期画面が表示されます。

</details>

---

## 演習2（基本）：トップページを編集しよう

`app/page.tsx` を編集して、自分のオリジナルのトップページを作成してください。

**要件：**
- `<h1>` タグで「ようこそ！」と表示する
- `<p>` タグで簡単な説明文を表示する
- ファイルを保存して、ブラウザに自動で反映されることを確認する

<details>
<summary>ヒント</summary>

`app/page.tsx` はルート `/` に対応するページです。デフォルトの内容をすべて削除して、シンプルな JSX を返す関数コンポーネントにしましょう。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/page.tsx
export default function HomePage() {
  return (
    <main style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>ようこそ！</h1>
      <p>これは Next.js で作った最初のページです。</p>
      <p>ファイルを保存すると、自動的にブラウザに反映されます。</p>
    </main>
  )
}
```

ブラウザで `http://localhost:3000` にアクセスすると、編集した内容が表示されます。Hot Module Replacement (HMR) により、ファイル保存と同時にブラウザが自動更新されます。

</details>

---

## 演習3（基本）：新しいページを追加しよう

`/about` にアクセスしたときに表示される「About」ページを作成してください。

**要件：**
- `app/about/page.tsx` ファイルを作成する
- ページタイトルと自己紹介的な内容を含める
- ブラウザで `/about` にアクセスして表示を確認する

<details>
<summary>ヒント</summary>

App Router では、`app/` ディレクトリ内にフォルダを作り、その中に `page.tsx` を配置するだけで新しいルートが作成されます。`about` フォルダを作り、`page.tsx` を配置しましょう。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/about/page.tsx
export default function AboutPage() {
  return (
    <main style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>About</h1>
      <p>このサイトは Next.js の学習のために作成しました。</p>
      <p>App Router を使って、ファイルベースのルーティングを体験しています。</p>
    </main>
  )
}
```

`app/about/page.tsx` を作成するだけで、`/about` にアクセスしたときにこのページが表示されます。これが App Router のファイルベースルーティングです。

</details>

---

## 演習4（基本）：Link コンポーネントでページ間をナビゲーションしよう

`next/link` の `Link` コンポーネントを使って、トップページと About ページを行き来できるようにしてください。

**要件：**
- トップページに About ページへのリンクを追加する
- About ページにトップページへのリンクを追加する
- `<a>` タグではなく `Link` コンポーネントを使う

<details>
<summary>ヒント</summary>

`import Link from 'next/link'` でインポートし、`<Link href="/about">About</Link>` のように使用します。`Link` を使うとクライアントサイドナビゲーションが行われ、ページ遷移が高速になります。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/page.tsx
import Link from 'next/link'

export default function HomePage() {
  return (
    <main style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>ようこそ！</h1>
      <p>これは Next.js で作った最初のページです。</p>
      <Link href="/about" style={{ color: '#0070f3' }}>
        About ページへ
      </Link>
    </main>
  )
}
```

```tsx
// app/about/page.tsx
import Link from 'next/link'

export default function AboutPage() {
  return (
    <main style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>About</h1>
      <p>このサイトは Next.js の学習のために作成しました。</p>
      <Link href="/" style={{ color: '#0070f3' }}>
        ホームに戻る
      </Link>
    </main>
  )
}
```

`Link` コンポーネントを使うと、ページ遷移時にフルリロードが発生せず、クライアントサイドナビゲーションで高速にページが切り替わります。

</details>

---

## 演習5（基本）：レイアウトにナビゲーションバーを追加しよう

`app/layout.tsx` を編集して、全ページに共通のナビゲーションバーを追加してください。

**要件：**
- ヘッダーに「ホーム」と「About」のリンクを含むナビゲーションを配置する
- フッターにコピーライト表示を追加する
- `Link` コンポーネントを使用する

<details>
<summary>ヒント</summary>

`app/layout.tsx` はすべてのページに適用される共通レイアウトです。`<html>` タグと `<body>` タグを含む必要があります。`children` プロパティが各ページの内容を表します。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/layout.tsx
import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'My Next.js App',
  description: 'Next.js 学習用アプリケーション',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body>
        {/* 共通ナビゲーション */}
        <header style={{
          padding: '1rem',
          borderBottom: '1px solid #eaeaea',
          display: 'flex',
          gap: '1rem',
        }}>
          <Link href="/">ホーム</Link>
          <Link href="/about">About</Link>
        </header>

        {/* 各ページのコンテンツ */}
        <main>{children}</main>

        {/* 共通フッター */}
        <footer style={{
          padding: '1rem',
          borderTop: '1px solid #eaeaea',
          textAlign: 'center',
        }}>
          <p>&copy; 2026 My Next.js App</p>
        </footer>
      </body>
    </html>
  )
}
```

`layout.tsx` に配置したナビゲーションとフッターは、トップページでも About ページでも共通して表示されます。ページ遷移時にレイアウト部分は再レンダリングされません。

</details>

---

## 演習6（応用）：Props を使った再利用可能なカードコンポーネントを作ろう

カードコンポーネントを作成し、トップページで複数のカードを表示してください。

**要件：**
- `app/components/Card.tsx` を作成する
- Props として `title`（string）と `description`（string）を受け取る
- TypeScript の型定義を使用する
- トップページで3枚以上のカードを表示する

<details>
<summary>ヒント</summary>

`type CardProps = { title: string; description: string }` のように型を定義します。コンポーネントはサーバーコンポーネント（デフォルト）のままで構いません。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/components/Card.tsx
type CardProps = {
  title: string
  description: string
}

export default function Card({ title, description }: CardProps) {
  return (
    <div style={{
      border: '1px solid #eaeaea',
      borderRadius: '8px',
      padding: '1.5rem',
      maxWidth: '300px',
    }}>
      <h3 style={{ margin: '0 0 0.5rem' }}>{title}</h3>
      <p style={{ margin: 0, color: '#666' }}>{description}</p>
    </div>
  )
}
```

```tsx
// app/page.tsx
import Link from 'next/link'
import Card from './components/Card'

export default function HomePage() {
  const features = [
    { title: 'ファイルベースルーティング', description: 'フォルダ構造がそのまま URL に対応します。' },
    { title: 'サーバーコンポーネント', description: 'デフォルトでサーバーサイドレンダリングされます。' },
    { title: 'TypeScript サポート', description: '型安全な開発が標準で行えます。' },
  ]

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Next.js 学習サイト</h1>
      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        {features.map((feature, index) => (
          <Card
            key={index}
            title={feature.title}
            description={feature.description}
          />
        ))}
      </div>
    </div>
  )
}
```

コンポーネントに型定義を付けることで、Props の不足や型のミスマッチをコンパイル時に検出できます。

</details>

---

## 演習7（応用）：複数の階層を持つページ構造を作ろう

以下のページ構造を作成し、各ページに内容を記述してください。

**要件：**
- `/` — トップページ
- `/about` — About ページ
- `/blog` — ブログ一覧ページ
- `/blog/first-post` — 個別ブログ記事ページ

```
app/
├── page.tsx              → /
├── about/
│   └── page.tsx          → /about
├── blog/
│   ├── page.tsx          → /blog
│   └── first-post/
│       └── page.tsx      → /blog/first-post
```

<details>
<summary>ヒント</summary>

App Router では、フォルダをネストするだけで階層的な URL が作れます。`blog` フォルダ内に `page.tsx` と `first-post` フォルダを作りましょう。

</details>

<details>
<summary>解答例</summary>

```tsx
// app/blog/page.tsx
import Link from 'next/link'

export default function BlogPage() {
  return (
    <div style={{ padding: '2rem' }}>
      <h1>ブログ一覧</h1>
      <ul>
        <li>
          <Link href="/blog/first-post">最初のブログ記事</Link>
        </li>
      </ul>
    </div>
  )
}
```

```tsx
// app/blog/first-post/page.tsx
import Link from 'next/link'

export default function FirstPostPage() {
  return (
    <article style={{ padding: '2rem', maxWidth: '700px', margin: '0 auto' }}>
      <h1>最初のブログ記事</h1>
      <p>これは Next.js で作成した最初のブログ記事です。</p>
      <p>App Router のファイルベースルーティングにより、フォルダ構造がそのまま URL パスになります。</p>
      <Link href="/blog">← ブログ一覧に戻る</Link>
    </article>
  )
}
```

`/blog/first-post` のように階層化されたルートも、フォルダ構造に合わせてファイルを配置するだけで自動的に認識されます。

</details>

---

## 演習8（応用）：プロジェクト構造の各ファイルの役割を説明しよう

`create-next-app` で生成される以下のファイルについて、それぞれの役割を説明してください。

1. `app/layout.tsx`
2. `app/page.tsx`
3. `next.config.ts`
4. `tsconfig.json`
5. `package.json`
6. `public/` ディレクトリ

<details>
<summary>ヒント</summary>

各ファイルは Next.js のプロジェクトにおいて固有の役割を持っています。App Router の仕組みとして特別な意味を持つファイルと、一般的な Node.js プロジェクトの設定ファイルに分けて考えましょう。

</details>

<details>
<summary>解答例</summary>

1. **`app/layout.tsx`**: ルートレイアウト。全ページに共通する `<html>` と `<body>` タグを含む必須ファイル。ナビゲーションやフッターなどの共通 UI を配置する。
2. **`app/page.tsx`**: トップページ（`/`）のコンポーネント。`app` ディレクトリ直下の `page.tsx` がルート URL に対応する。
3. **`next.config.ts`**: Next.js のカスタム設定ファイル。画像の外部ドメイン許可、リダイレクト設定、環境変数の公開など、フレームワークレベルの設定を行う。
4. **`tsconfig.json`**: TypeScript の設定ファイル。コンパイラオプションやパスエイリアス（`@/`）の設定を管理する。Next.js が自動的に最適な設定を生成・更新する。
5. **`package.json`**: プロジェクトの依存パッケージと npm スクリプト（`dev`, `build`, `start`, `lint`）を管理するファイル。
6. **`public/` ディレクトリ**: 静的ファイル（画像、アイコン等）を配置する場所。`public/images/logo.png` は `/images/logo.png` として直接アクセスできる。

</details>

---

## 演習9（チャレンジ）：ナビゲーションメニュー付きの学習サイトを構築しよう

以下の要件を満たす学習サイトの骨組みを構築してください。

**要件：**
- 共通レイアウト（ヘッダー、フッター）
- 5つ以上のページ（ホーム、About、コース一覧、お問い合わせ、利用規約）
- ナビゲーションは全ページに `Link` コンポーネントで表示
- 各ページに最低限の内容を記述
- TypeScript の型定義を使用

<details>
<summary>ヒント</summary>

まずディレクトリ構造を設計しましょう。各ページフォルダに `page.tsx` を配置し、`layout.tsx` でナビゲーションを定義します。

```
app/
├── layout.tsx
├── page.tsx
├── about/page.tsx
├── courses/page.tsx
├── contact/page.tsx
└── terms/page.tsx
```

</details>

<details>
<summary>解答例</summary>

```tsx
// app/layout.tsx
import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'プログラミング学習サイト',
  description: 'プログラミングを基礎から学べるサイトです',
}

// ナビゲーションリンクの型定義
type NavItem = {
  href: string
  label: string
}

const navItems: NavItem[] = [
  { href: '/', label: 'ホーム' },
  { href: '/about', label: 'About' },
  { href: '/courses', label: 'コース一覧' },
  { href: '/contact', label: 'お問い合わせ' },
  { href: '/terms', label: '利用規約' },
]

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body style={{ margin: 0, fontFamily: 'sans-serif' }}>
        <header style={{
          backgroundColor: '#2c3e50',
          color: 'white',
          padding: '1rem 2rem',
        }}>
          <nav style={{ display: 'flex', gap: '1.5rem' }}>
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                style={{ color: 'white', textDecoration: 'none' }}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </header>

        <main style={{ minHeight: '80vh', padding: '2rem' }}>
          {children}
        </main>

        <footer style={{
          backgroundColor: '#ecf0f1',
          padding: '1rem 2rem',
          textAlign: 'center',
        }}>
          <p>&copy; 2026 プログラミング学習サイト</p>
        </footer>
      </body>
    </html>
  )
}
```

```tsx
// app/page.tsx
export default function HomePage() {
  return (
    <div>
      <h1>プログラミング学習サイトへようこそ</h1>
      <p>初心者から上級者まで、幅広いコースを提供しています。</p>
    </div>
  )
}
```

```tsx
// app/about/page.tsx
export default function AboutPage() {
  return (
    <div>
      <h1>About</h1>
      <p>当サイトはプログラミング学習を支援するために運営されています。</p>
    </div>
  )
}
```

```tsx
// app/courses/page.tsx
export default function CoursesPage() {
  return (
    <div>
      <h1>コース一覧</h1>
      <ul>
        <li>HTML/CSS 入門</li>
        <li>JavaScript 基礎</li>
        <li>React 入門</li>
        <li>Next.js 実践</li>
      </ul>
    </div>
  )
}
```

```tsx
// app/contact/page.tsx
export default function ContactPage() {
  return (
    <div>
      <h1>お問い合わせ</h1>
      <p>ご質問やご要望がありましたら、お気軽にご連絡ください。</p>
    </div>
  )
}
```

```tsx
// app/terms/page.tsx
export default function TermsPage() {
  return (
    <div>
      <h1>利用規約</h1>
      <p>本サイトの利用にあたっては、以下の規約に同意していただく必要があります。</p>
    </div>
  )
}
```

ナビゲーションリンクの配列を型定義付きで管理することで、追加・変更が容易になります。

</details>

---

## 演習10（チャレンジ）：ビルドして本番モードで動作確認しよう

開発サーバーではなく、本番ビルドを行い、本番サーバーとして起動してください。

**要件：**
1. `npm run build` でプロジェクトをビルドする
2. ビルド結果の出力を確認する（静的ページと動的ページの区別）
3. `npm start` で本番サーバーを起動する
4. `http://localhost:3000` にアクセスして動作を確認する

<details>
<summary>ヒント</summary>

`npm run build` を実行すると、Next.js が各ルートを分析し、静的に生成できるページと動的に処理が必要なページを自動的に判定します。ビルド出力に表示される `○`（静的）と `ƒ`（動的）のアイコンに注目してください。

</details>

<details>
<summary>解答例</summary>

```bash
# 1. 本番ビルド
npm run build

# ビルド出力の例:
# Route (app)                  Size     First Load JS
# ┌ ○ /                       5.2 kB   92 kB
# ├ ○ /about                  142 B    87 kB
# ├ ○ /blog                   156 B    87 kB
# └ ○ /blog/first-post        178 B    87 kB
#
# ○ = 静的（Static）
# ƒ = 動的（Dynamic）

# 2. 本番サーバーを起動
npm start

# 3. ブラウザで http://localhost:3000 にアクセス
```

ビルド結果で `○` と表示されたルートは静的に HTML が生成されており、CDN から配信可能な高速なページです。開発サーバー（`npm run dev`）と本番サーバー（`npm start`）では挙動が異なる場合があるため、デプロイ前に本番モードでの動作確認は重要です。

</details>

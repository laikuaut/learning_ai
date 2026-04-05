# 第1章：Playwrightの基本とセットアップ

## この章のゴール

- Playwrightとは何か、E2Eテストの位置づけを理解する
- Playwrightの開発環境をセットアップできる
- 最初のテストを書いて実行できる
- テストの基本構造（`test`、`expect`、`page`）を理解する
- テストレポートの見方を把握する

---

## 1. Playwrightとは

### E2Eテストの位置づけ

**Playwright（プレイライト）** は、Microsoft が開発したブラウザ自動化・E2Eテストフレームワークです。実際のブラウザを操作してWebアプリケーション全体の動作を検証します。

```
┌─────────────────────────────────────────────────────────┐
│              テストピラミッド                              │
├─────────────────────────────────────────────────────────┤
│                                                          │
│          ╱╲         E2Eテスト ← Playwright               │
│         ╱  ╲        （ブラウザを操作して全体を検証）       │
│        ╱────╲                                            │
│       ╱      ╲      統合テスト                            │
│      ╱        ╲     （複数モジュールの連携を検証）         │
│     ╱──────────╲                                         │
│    ╱            ╲   ユニットテスト                        │
│   ╱              ╲  （個々の関数・コンポーネントを検証）   │
│  ╱────────────────╲                                      │
│                                                          │
│  下に行くほど：速い、安い、数が多い                       │
│  上に行くほど：遅い、高い、信頼性が高い                   │
└─────────────────────────────────────────────────────────┘
```

### ��ぜPlaywrightを使うのか

| 特徴 | 説明 |
|------|------|
| **マルチブラウザ対応** | Chromium、Firefox、WebKit（Safari）を1つのAPIで操作 |
| **自動待機（Auto-waiting）** | 要素が操作可能になるまで自動で待つ |
| **高速・安定** | ブラウザと直接通信するため信頼性が高い |
| **強力なツール** | コード生成、トレースビューア、UIモードなど |
| **TypeScript対応** | 型安全なテストコードが書ける |

### 他のE2Eテストツールとの比較

```
┌──────────────┬────────────┬────────────┬─────────────┐
│              │ Playwright │ Cypress    │ Selenium    │
├──────────────┼────────────┼────────────┼─────────────┤
│ 開発元       │ Microsoft  │ Cypress社  │ コミュニティ│
│ 言語         │ TS/JS/     │ JS/TS      │ 多言語      │
│              │ Python/C#  │            │             │
│ ブラウザ     │ 3種対応    │ Chromium系 │ 全対応      │
│              │            │ +Firefox   │             │
│ 速度         │ 高速       │ 高速       │ 中程度      │
│ 自動待機     │ ○         │ ○         │ △          │
│ 並列実行     │ ○         │ ○（有料） │ ○          │
│ モバイル対応 │ ○         │ △         │ ○          │
└──────────────┴────────────┴────────────┴─────────────┘
```

---

## 2. 開発環境のセットアップ

### 必要なもの

- **Node.js**（v18以上推奨）：[https://nodejs.org/](https://nodejs.org/)
- **テキストエディタ**：VS Code推奨（Playwright拡張機能あり）
- **ターミナル**

### プロジェクトの作成

```bash
# 新しいディレクトリを作成
mkdir my-playwright-tests
cd my-playwright-tests

# Playwrightをセットアップ
npm init playwright@latest
```

セットアップ中に以下の質問が表示されます。

```
✔ Do you want to use TypeScript or JavaScript? · TypeScript
✔ Where to put your end-to-end tests? · tests
✔ Add a GitHub Actions workflow? · false
✔ Install Playwright Browsers? · true
```

> **ポイント**: 「Install Playwright Browsers?」では `true` を選びます。Playwright専用のブラウザ（Chromium、Firefox、WebKit）がダウンロードされます。

### プロジェクトの構造

```
my-playwright-tests/
├── node_modules/
├── tests/                    # テストファイルを置く場所
│   └── example.spec.ts       # サンプルテスト
├── tests-examples/           # 追加サンプル（参考用）
│   └── demo-todo-app.spec.ts
├── playwright.config.ts      # Playwrightの設定ファイル
├── package.json
├── package-lock.json
└── tsconfig.json
```

### 設定ファイル（playwright.config.ts）の概要

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // テストファイルの場所
  testDir: './tests',

  // テストの最大実行時間（ミリ秒）
  timeout: 30000,

  // テスト失敗時にリトライする回数
  retries: 0,

  // テストレポートの形式
  reporter: 'html',

  // 全テスト共通の設定
  use: {
    // テスト対象のURL
    baseURL: 'http://localhost:3000',

    // 失敗時にスクリーンショットを撮る
    screenshot: 'only-on-failure',

    // 操作のトレースを記録する
    trace: 'on-first-retry',
  },

  // テストするブラウザの設定
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
});
```

---

## 3. 最初のテストを書く

### テストファイルの作成

`tests/first.spec.ts` を作成します。

```typescript
import { test, expect } from '@playwright/test';

test('Playwrightの公式サイトにアクセスする', async ({ page }) => {
  // 1. ページに移動
  await page.goto('https://playwright.dev/');

  // 2. タイトルに "Playwright" が含まれることを確認
  await expect(page).toHaveTitle(/Playwright/);

  // 3. "Get started" リンクが表示されていることを確認
  const getStarted = page.getByRole('link', { name: 'Get started' });
  await expect(getStarted).toBeVisible();
});
```

### コードの解説

```
┌──────────────────────────────────────────────────────────┐
│ import { test, expect } from '@playwright/test';         │
│                                                          │
│ test('テスト名', async ({ page }) => {                   │
│   │                      │                               │
│   │                      └── page: ブラウザのページ      │
│   │                          （タブ）を操作する          │
│   │                          オブジェクト                │
│   └── テストの説明                                       │
│                                                          │
│   await page.goto('URL');        ← ページに移動          │
│   await expect(page).toHaveTitle(/regex/);               │
│   │     │              │                                 │
│   │     │              └── マッチャー                    │
│   │     └── アサーション対象                             │
│   └── 非同期なので await が必要                          │
│ });                                                      │
└──────────────────────────────────────────────────────────┘
```

### テストの実行

```bash
# すべてのテストを実行
npx playwright test

# 特定のファイルだけ実行
npx playwright test tests/first.spec.ts

# ブラウザの画面を見ながら実行（headed モード）
npx playwright test --headed

# 特定のブラウザだけで実行
npx playwright test --project=chromium
```

### 実行結果の例

```
Running 3 tests using 3 workers

  ✓ [chromium] › tests/first.spec.ts:3:5 › Playwrightの公式サイトにアクセスする (2.1s)
  ✓ [firefox] › tests/first.spec.ts:3:5 › Playwrightの公式サイトにアクセスする (3.4s)
  ✓ [webkit] › tests/first.spec.ts:3:5 › Playwrightの公式サイトにアクセスする (2.8s)

  3 passed (5.2s)
```

3つのブラウザで同じテストが並列に実行され、すべて成功しました。

---

## 4. テストの基本構造

### `test` 関数

テストを定義する関数です。テスト名とテスト本体を受け取ります。

```typescript
import { test, expect } from '@playwright/test';

// 基本的なテスト
test('テスト名', async ({ page }) => {
  // テストの内容
});

// テストをグループ化
test.describe('ログイン機能', () => {
  test('正しい情報でログインできる', async ({ page }) => {
    // ...
  });

  test('間違ったパスワードでエラーが表示される', async ({ page }) => {
    // ...
  });
});
```

### `page` オブジェクト

`page` はブラウザのタブ（ページ）を操作するためのオブジェクトです。テストのたびに新しいページが作成されます。

```typescript
test('pageの基本操作', async ({ page }) => {
  // ページ遷移
  await page.goto('https://example.com');

  // 要素のクリック
  await page.getByRole('button', { name: '送信' }).click();

  // テキスト入力
  await page.getByLabel('名前').fill('太郎');

  // スクリーンショット
  await page.screenshot({ path: 'screenshot.png' });
});
```

### `expect` 関数

テストの検証（アサーション）を行います。Playwrightのアサーションは自動で再試行されます。

```typescript
test('アサーションの例', async ({ page }) => {
  await page.goto('https://example.com');

  // ページのタイトルを検証
  await expect(page).toHaveTitle('Example Domain');

  // ページのURLを検証
  await expect(page).toHaveURL('https://example.com/');

  // 要素のテキストを検証
  const heading = page.getByRole('heading');
  await expect(heading).toHaveText('Example Domain');

  // 要素が表示されていることを検証
  await expect(heading).toBeVisible();
});
```

---

## 5. 便利なツール

### UIモード（インタラクティブなテスト実行）

```bash
npx playwright test --ui
```

UIモードでは、テストの実行状況をリアルタイムに確認でき、各ステップの画面を視覚的に確認できます。

### テストレポート

```bash
# テスト実行後にレポートを表示
npx playwright show-report
```

HTMLレポートが開き、テスト結果の詳細（成功/失敗、スクリーンショット、実行時間）を確認できます。

### コード生成（Codegen）

実際にブラウザを操作して、テストコードを自動生成できます。

```bash
npx playwright codegen https://example.com
```

ブラウザが開き、操作するとリアルタイムでテストコードが生成されます。初心者が「どうコードを書けばいいか」を学ぶのに最適なツールです。

### VS Code拡張機能

「Playwright Test for VS Code」をインストールすると、以下が可能になります。

- テストの横に表示される再生ボタンで個別実行
- テストの成功/失敗がエディタ内に表示
- コード生成（Record new）
- デバッグ（ブレークポイント対応）

---

## 6. 実践：最初のテストスイート

ここまでの知識を使って、実用的なテストを書いてみましょう。

```typescript
// tests/example-site.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Example.com のテスト', () => {

  test('ページが正しく表示される', async ({ page }) => {
    // Example.comにアクセス
    await page.goto('https://example.com');

    // タイトルの確認
    await expect(page).toHaveTitle('Example Domain');

    // 見出しの確認
    const heading = page.getByRole('heading', { level: 1 });
    await expect(heading).toHaveText('Example Domain');

    // 説明文が表示されていることを確認
    const description = page.getByText('This domain is for use in illustrative examples');
    await expect(description).toBeVisible();
  });

  test('「More information...」リンクが正しく機能する', async ({ page }) => {
    await page.goto('https://example.com');

    // リンクが存在することを確認
    const link = page.getByRole('link', { name: 'More information...' });
    await expect(link).toBeVisible();

    // リンクのhref属性を確認
    await expect(link).toHaveAttribute('href', 'https://www.iana.org/domains/example');
  });

  test('ページのメタ情報が正しい', async ({ page }) => {
    await page.goto('https://example.com');

    // URLの確認
    await expect(page).toHaveURL('https://example.com/');

    // viewportの確認（レスポンシブ関連）
    const viewport = page.viewportSize();
    expect(viewport).not.toBeNull();
  });
});
```

### テストの実行と結果確認

```bash
# chromiumだけで実行し、結果を詳細表示
npx playwright test tests/example-site.spec.ts --project=chromium

# レポートを表示
npx playwright show-report
```

---

## まとめ

| 項目 | ポイント |
|------|---------|
| Playwright | Microsoft製のE2Eテストフレームワーク |
| セットアップ | `npm init playwright@latest` で開始 |
| テスト構造 | `test('名前', async ({ page }) => { ... })` |
| ページ操作 | `page.goto()`, `page.getByRole()`, `.click()`, `.fill()` |
| アサーション | `expect(page).toHaveTitle()`, `expect(要素).toBeVisible()` |
| 実行方法 | `npx playwright test` |
| 便利ツール | UIモード、Codegen、HTMLレポート |
| ブラウザ | Chromium、Firefox、WebKit の3種に対応 |

### 次の章では

ページ上の要素を見つけるための「**ロケーター**」について詳しく学びます。テストの品質はロケーターの選び方で大きく変わります。

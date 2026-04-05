# 第1章：Playwrightの基本とセットアップ 演習問題

---

## 基本問題

### 問題1：最初のテストを書く

Playwrightを使って、Playwrightの公式サイト（`https://playwright.dev/`）にアクセスし、ページタイトルに「Playwright」という文字列が含まれていることを検証するテストを作成してください。

**期待される結果:**
```
テストが成功（passed）すること
ページタイトルに "Playwright" が含まれていることが検証される
```

<details>
<summary>ヒント</summary>

`test` 関数と `expect` を `@playwright/test` からインポートします。`page.goto()` でページに移動し、`expect(page).toHaveTitle()` でタイトルを検証します。正規表現を使うと部分一致が簡単です。

</details>

<details>
<summary>解答例</summary>

```typescript
// test/example.spec.ts
import { test, expect } from '@playwright/test';

// Playwright公式サイトのタイトルを検証するテスト
test('Playwright公式サイトのタイトルを確認する', async ({ page }) => {
  // ページに移動
  await page.goto('https://playwright.dev/');

  // タイトルに "Playwright" が含まれることを検証（正規表現で部分一致）
  await expect(page).toHaveTitle(/Playwright/);
});
```

</details>

---

### 問題2：要素の可視性を確認する

`https://playwright.dev/` にアクセスし、以下の2つを検証するテストを作成してください。

1. 「Get started」というテキストを持つリンクが表示されていること
2. ページ内に `h1` 見出し要素が存在し、表示されていること

**期待される結果:**
```
2つのアサーションがどちらも成功（passed）すること
```

<details>
<summary>ヒント</summary>

`page.getByRole('link', { name: 'Get started' })` でリンクを取得できます。`h1` 要素は `page.locator('h1')` または `page.getByRole('heading', { level: 1 })` で取得できます。可視性の検証には `toBeVisible()` を使います。

</details>

<details>
<summary>解答例</summary>

```typescript
import { test, expect } from '@playwright/test';

test('Get startedリンクとh1見出しが表示されている', async ({ page }) => {
  await page.goto('https://playwright.dev/');

  // "Get started" リンクが表示されていることを確認
  const getStartedLink = page.getByRole('link', { name: 'Get started' });
  await expect(getStartedLink).toBeVisible();

  // h1見出しが表示されていることを確認
  const heading = page.getByRole('heading', { level: 1 });
  await expect(heading).toBeVisible();
});
```

</details>

---

### 問題3：ページ遷移のテスト

`https://playwright.dev/` にアクセスし、「Get started」リンクをクリックした後、URLに `/docs/intro` が含まれていることを検証するテストを作成してください。

**期待される結果:**
```
テストが成功し、遷移先URLに "/docs/intro" が含まれている
```

<details>
<summary>ヒント</summary>

リンクをクリックするには `click()` メソッドを使います。URLの検証には `expect(page).toHaveURL()` に正規表現を渡します。

</details>

<details>
<summary>解答例</summary>

```typescript
import { test, expect } from '@playwright/test';

test('Get startedリンクをクリックするとドキュメントページに遷移する', async ({ page }) => {
  // トップページにアクセス
  await page.goto('https://playwright.dev/');

  // "Get started" リンクをクリック
  await page.getByRole('link', { name: 'Get started' }).click();

  // 遷移先URLに "/docs/intro" が含まれることを検証
  await expect(page).toHaveURL(/.*\/docs\/intro/);
});
```

</details>

---

## 応用問題

### 問題4：テストスイートの構築

`test.describe` を使って「Playwrightトップページ」というテストスイートを作成し、以下の3つのテストをまとめてください。

1. ページタイトルの検証
2. メインの見出しテキストの検証
3. ナビゲーションバーにリンクが複数存在することの検証

**期待される結果:**
```
3つのテストがすべて成功する
テスト結果に "Playwrightトップページ" というグループ名が表示される
```

<details>
<summary>ヒント</summary>

`test.describe('グループ名', () => { ... })` でテストをグループ化します。ナビゲーションのリンク数を確認するには、ロケーターの `count()` メソッドを使います。

</details>

<details>
<summary>解答例</summary>

```typescript
import { test, expect } from '@playwright/test';

// test.describe でテストをグループ化
test.describe('Playwrightトップページ', () => {

  // テスト1: タイトルの検証
  test('ページタイトルにPlaywrightが含まれる', async ({ page }) => {
    await page.goto('https://playwright.dev/');
    await expect(page).toHaveTitle(/Playwright/);
  });

  // テスト2: メイン見出しの検証
  test('メインの見出しが表示される', async ({ page }) => {
    await page.goto('https://playwright.dev/');
    const heading = page.getByRole('heading', { level: 1 });
    await expect(heading).toBeVisible();
  });

  // テスト3: ナビゲーションリンクの検証
  test('ナビゲーションバーにリンクが存在する', async ({ page }) => {
    await page.goto('https://playwright.dev/');
    // ナビゲーション内のリンクを取得
    const navLinks = page.locator('nav a');
    // リンクが1つ以上存在することを確認
    const count = await navLinks.count();
    expect(count).toBeGreaterThan(0);
  });
});
```

</details>

---

### 問題5：複数ページの検証テスト

以下の2つのURLにそれぞれアクセスし、各ページのタイトルとURLが正しいことを検証するテストを作成してください。

- トップページ: `https://playwright.dev/`
- Docsページ: `https://playwright.dev/docs/intro`

各テストは独立して実行でき、テスト名からどのページをテストしているか分かるようにしてください。

**期待される結果:**
```
2つのテストがそれぞれ独立して成功する
各テストでタイトルとURLの検証がパスする
```

<details>
<summary>ヒント</summary>

テストごとに `page.goto()` を呼び出し、`toHaveTitle()` と `toHaveURL()` で検証します。テスト名を日本語で分かりやすくしましょう。

</details>

<details>
<summary>解答例</summary>

```typescript
import { test, expect } from '@playwright/test';

test.describe('Playwrightサイトの各ページ検証', () => {

  test('トップページのタイトルとURLを確認する', async ({ page }) => {
    await page.goto('https://playwright.dev/');

    // タイトルの検証
    await expect(page).toHaveTitle(/Playwright/);
    // URLの検証（トップページ）
    await expect(page).toHaveURL('https://playwright.dev/');
  });

  test('DocsページのタイトルとURLを確認する', async ({ page }) => {
    await page.goto('https://playwright.dev/docs/intro');

    // タイトルの検証（Docsページにもサイト名が含まれる）
    await expect(page).toHaveTitle(/Playwright/);
    // URLの検証
    await expect(page).toHaveURL(/.*\/docs\/intro/);
  });
});
```

</details>

---

### 問題6：テストの実行オプション

以下の各シナリオについて、`npx playwright test` コマンドのオプションを答えてください。

1. 特定のテストファイル `example.spec.ts` だけを実行する
2. Chromiumブラウザのみで実行する
3. テストをヘッドモード（ブラウザを表示して）で実行する
4. UI Modeでテストを実行する
5. テストを並列ではなく直列で実行する

**期待される結果:**
```
各シナリオに対応する正しいコマンドが記述されている
```

<details>
<summary>ヒント</summary>

`--project`、`--headed`、`--ui`、`--workers` などのオプションを確認しましょう。特定ファイルの指定はコマンドの引数として渡します。

</details>

<details>
<summary>解答例</summary>

```bash
# 1. 特定のテストファイルだけを実行
npx playwright test example.spec.ts

# 2. Chromiumブラウザのみで実行
npx playwright test --project=chromium

# 3. ヘッドモード（ブラウザ表示）で実行
npx playwright test --headed

# 4. UI Modeで実行
npx playwright test --ui

# 5. 直列（シリアル）で実行（ワーカー数を1にする）
npx playwright test --workers=1
```

</details>

---

## チャレンジ問題

### 問題7：codegenで生成したテストの改善

以下のコマンドでcodegenを起動し、Playwrightの公式サイトで「Get started」をクリックし、サイドバーのメニューを1つクリックする操作を記録してください。

```bash
npx playwright codegen https://playwright.dev/
```

記録されたコードを元に、以下の改善を行ったテストファイルを作成してください。

1. テスト名を日本語で分かりやすくする
2. `test.describe` でグループ化する
3. 各ステップの操作後にアサーションを追加する

**期待される結果:**
```
codegenで生成されたコードがベースになっている
テスト名が日本語で意味のある名前になっている
各操作後に適切なアサーション（URLやテキストの検証）が入っている
```

<details>
<summary>ヒント</summary>

codegenは操作を記録してコードを生成しますが、アサーションは自動では最小限しか入りません。ページ遷移後に `toHaveURL()` や `toBeVisible()` を手動で追加しましょう。

</details>

<details>
<summary>解答例</summary>

```typescript
import { test, expect } from '@playwright/test';

test.describe('Playwrightドキュメントのナビゲーション', () => {

  test('トップページからドキュメントを閲覧する', async ({ page }) => {
    // codegenで生成された操作をベースに改善

    // Step 1: トップページにアクセス
    await page.goto('https://playwright.dev/');
    // アサーション追加: タイトルの確認
    await expect(page).toHaveTitle(/Playwright/);

    // Step 2: Get startedリンクをクリック
    await page.getByRole('link', { name: 'Get started' }).click();
    // アサーション追加: ドキュメントページに遷移したことを確認
    await expect(page).toHaveURL(/.*\/docs\/intro/);

    // Step 3: サイドバーのメニュー項目をクリック（例: "Writing tests"）
    await page.getByRole('link', { name: 'Writing tests' }).click();
    // アサーション追加: 遷移先ページのURLを確認
    await expect(page).toHaveURL(/.*\/docs\/writing-tests/);
    // アサーション追加: ページの見出しが表示されていることを確認
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  });
});
```

</details>

---

### 問題8：複数ブラウザでのテスト実行

Playwright設定ファイル（`playwright.config.ts`）を確認し、以下の課題に取り組んでください。

1. デフォルトの設定で `npx playwright test` を実行し、どのブラウザでテストが実行されるかを確認する
2. Chromium、Firefox、WebKitそれぞれ単独でテストを実行するコマンドを記述する
3. テスト結果レポートを確認する方法を記述する

**期待される結果:**
```
Chromium、Firefox、WebKitの3ブラウザでテストが実行される
各ブラウザで個別にテストを実行するコマンドが分かる
HTMLレポートの表示方法が分かる
```

<details>
<summary>ヒント</summary>

`npx playwright test --project=<ブラウザ名>` で個別のブラウザを指定できます。テストレポートは `npx playwright show-report` で確認できます。

</details>

<details>
<summary>解答例</summary>

```bash
# 1. デフォルト設定で全ブラウザでテスト実行
npx playwright test
# → playwright.config.ts の projects 設定に基づき
#    Chromium, Firefox, WebKit の3ブラウザで実行される

# 2. 各ブラウザ個別に実行
# Chromiumのみ
npx playwright test --project=chromium

# Firefoxのみ
npx playwright test --project=firefox

# WebKitのみ
npx playwright test --project=webkit

# 3. HTMLレポートを表示
npx playwright show-report
# → デフォルトでは playwright-report/ フォルダのレポートが
#    ブラウザで開かれる
```

**補足: playwright.config.ts のprojects設定例:**

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
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

</details>

---

### 問題9：テストプロジェクトの初期化と設定確認

新しいディレクトリで `npm init playwright@latest` を実行し、以下を確認・記述してください。

1. 初期化後に生成されるファイル・フォルダの一覧
2. `playwright.config.ts` の主要な設定項目（5つ以上）の役割
3. サンプルテストファイルの内容を読み解き、何をテストしているか説明する

**期待される結果:**
```
生成されるファイル構成が正しく列挙されている
設定項目の役割が説明されている
サンプルテストの動作が日本語で説明されている
```

<details>
<summary>ヒント</summary>

`npm init playwright@latest` を実行すると対話形式でセットアップが進みます。TypeScript/JavaScript の選択、テストフォルダ名、GitHub Actions の設定などが聞かれます。

</details>

<details>
<summary>解答例</summary>

```
【1. 生成されるファイル・フォルダ一覧】

project-root/
├── playwright.config.ts      # Playwright設定ファイル
├── package.json              # プロジェクトの依存関係（@playwright/testが追加される）
├── package-lock.json         # 依存関係のロックファイル
├── tests/                    # テストフォルダ
│   └── example.spec.ts       # サンプルテストファイル
├── tests-examples/           # 追加のサンプル
│   └── demo-todo-app.spec.ts # ToDoアプリのテスト例
└── .github/                  # （選択した場合）GitHub Actionsワークフロー
    └── workflows/
        └── playwright.yml
```

```typescript
// 【2. playwright.config.ts の主要設定項目】

import { defineConfig } from '@playwright/test';

export default defineConfig({
  // testDir: テストファイルが置かれるディレクトリ
  testDir: './tests',

  // fullyParallel: テストを完全に並列で実行するか
  fullyParallel: true,

  // forbidOnly: CI環境で test.only が残っていたらエラーにする
  forbidOnly: !!process.env.CI,

  // retries: 失敗したテストの再試行回数
  retries: process.env.CI ? 2 : 0,

  // workers: 並列実行するワーカー数
  workers: process.env.CI ? 1 : undefined,

  // reporter: テスト結果のレポート形式
  reporter: 'html',

  // use: 全テスト共通の設定
  use: {
    // baseURL: テストで使用するベースURL
    baseURL: 'http://localhost:3000',
    // trace: テスト失敗時にトレースを記録
    trace: 'on-first-retry',
  },

  // projects: テスト対象のブラウザ設定
  projects: [
    // Chromium, Firefox, WebKit の設定
  ],
});
```

```
【3. サンプルテスト（example.spec.ts）の説明】

サンプルテストは Playwright 公式サイトに対して2つのテストを実行します：
- 1つ目: トップページにアクセスしてタイトルに "Playwright" が含まれることを確認
- 2つ目: "Get started" リンクをクリックしてドキュメントページに遷移することを確認
どちらも基本的なナビゲーションとアサーションのパターンを示しています。
```

</details>

# 第8章 CI/CDとE2Eテスト戦略 演習問題

---

## 基本問題

### 問題1：並列実行とワーカー数の設定

テストの実行速度を最適化するために、並列実行の設定を行ってください。

**要件：**
- `playwright.config.ts` でワーカー数を設定する
- ローカル環境ではCPUコア数の50%を使用する
- CI環境では2ワーカーに固定する
- 特定のテストファイルはシリアル実行（順序実行）にする

**期待される結果：**
```
ローカル: CPUコア数 × 50% のワーカーで並列実行
CI: 2ワーカーで並列実行
シリアルテスト: 指定したファイルのテストが順番に実行される
```

<details>
<summary>ヒント</summary>

`playwright.config.ts` の `workers` オプションで設定します。CI環境の判定は `process.env.CI` で行えます。

```typescript
export default defineConfig({
  workers: process.env.CI ? 2 : '50%',
});
```

テストファイル内でシリアル実行にするには `test.describe.serial()` を使います。

</details>

<details>
<summary>解答例</summary>

```typescript
// ========================================
// playwright.config.ts - 並列実行の設定
// ========================================
import { defineConfig } from '@playwright/test';

export default defineConfig({
  // ========================================
  // workers: 並列実行のワーカー数
  // CI環境では固定値、ローカルではCPU比率で指定
  // '50%' → CPUコア数の半分（例: 8コアなら4ワーカー）
  // ========================================
  workers: process.env.CI ? 2 : '50%',

  // ========================================
  // fullyParallel: trueにするとテストファイル内の
  // 各テストも並列実行される（デフォルトはfalse）
  // ========================================
  fullyParallel: true,

  // ========================================
  // テスト設定
  // ========================================
  use: {
    baseURL: 'https://example.com',
  },
});

// ========================================
// tests/order-flow.spec.ts - シリアル実行が必要なテスト
// 注文フローなど、順番に実行しないと正しく動かないテスト
// ========================================
import { test, expect } from '@playwright/test';

// ========================================
// test.describe.serial() でブロック内のテストを順番に実行
// 途中のテストが失敗すると残りはスキップされる
// ========================================
test.describe.serial('注文フロー（順序実行）', () => {
  test('Step1: 商品をカートに追加する', async ({ page }) => {
    await page.goto('/products');
    await page.getByRole('button', { name: 'カートに追加' }).first().click();
    await expect(page.getByTestId('cart-count')).toHaveText('1');
  });

  test('Step2: 決済情報を入力する', async ({ page }) => {
    await page.goto('/checkout');
    await page.getByLabel('カード番号').fill('4111111111111111');
    await page.getByRole('button', { name: '次へ' }).click();
    await expect(page).toHaveURL(/.*confirm/);
  });

  test('Step3: 注文を確定する', async ({ page }) => {
    await page.goto('/confirm');
    await page.getByRole('button', { name: '注文を確定する' }).click();
    await expect(page.getByText('ご注文ありがとうございます')).toBeVisible();
  });
});
```

**ポイント：**
- `fullyParallel: true` はテストファイル間だけでなく、ファイル内のテストも並列化します
- `test.describe.serial()` はDBの状態に依存するテストなど、順序が重要なケースで使います
- CI環境ではメモリやCPUの制約があるため、ワーカー数を抑えるのが一般的です

</details>

---

### 問題2：リトライの設定

テストの安定性を高めるために、リトライ（再試行）の設定を行ってください。

**要件：**
- CI環境では失敗したテストを2回リトライする
- ローカル環境ではリトライしない
- 特定のテストだけ個別にリトライ回数を設定する
- リトライ時にトレースを取得する設定を追加する

**期待される結果：**
```
CI: 失敗したテストが最大2回リトライされる
ローカル: リトライなし（即座に失敗として報告）
特定テスト: 個別のリトライ回数が適用される
```

<details>
<summary>ヒント</summary>

`retries` オプションでリトライ回数を設定します。`trace: 'on-first-retry'` でリトライ時のみトレースを記録できます。

```typescript
export default defineConfig({
  retries: process.env.CI ? 2 : 0,
  use: {
    trace: 'on-first-retry',
  },
});
```

</details>

<details>
<summary>解答例</summary>

```typescript
// ========================================
// playwright.config.ts - リトライ設定
// ========================================
import { defineConfig } from '@playwright/test';

export default defineConfig({
  // ========================================
  // retries: テスト失敗時の再試行回数
  // CI環境のみリトライを有効にする
  // ========================================
  retries: process.env.CI ? 2 : 0,

  use: {
    // ========================================
    // trace: トレースの記録タイミング
    // 'on-first-retry' → 最初のリトライ時のみ記録
    // 'on' → 常に記録（CI時間が長くなる）
    // 'retain-on-failure' → 失敗時のみ保持
    // ========================================
    trace: 'on-first-retry',

    // ========================================
    // screenshot: スクリーンショットの記録タイミング
    // 'only-on-failure' → 失敗時のみ
    // ========================================
    screenshot: 'only-on-failure',

    // ========================================
    // video: 動画の記録タイミング
    // 'retain-on-failure' → 失敗時のみ保持
    // ========================================
    video: 'retain-on-failure',
  },
});

// ========================================
// テストファイル内での個別リトライ設定
// ========================================
import { test, expect } from '@playwright/test';

// ========================================
// test.describe.configure() でテストグループ単位の設定
// ========================================
test.describe('外部API連携テスト', () => {
  // このグループのテストは3回リトライする
  test.describe.configure({ retries: 3 });

  test('外部APIからデータを取得する', async ({ page }) => {
    await page.goto('https://example.com/external-data');
    await expect(page.getByTestId('api-result')).toBeVisible({ timeout: 10000 });
  });
});

// ========================================
// 個別テストのリトライ回数を上書き
// ========================================
test('不安定なテスト（5回リトライ）', async ({ page }) => {
  // テスト単位でリトライ回数を指定
  test.info().annotations.push({ type: 'retries', description: '5' });

  await page.goto('https://example.com/flaky-feature');
  await expect(page.getByText('完了')).toBeVisible();
});
```

**ポイント：**
- リトライはテストの安定性向上に役立ちますが、根本原因の調査も必ず行いましょう
- `trace: 'on-first-retry'` はCI環境でのデバッグに非常に有効です
- `screenshot` と `video` も併用すると、失敗時の状況を詳しく把握できます

</details>

---

### 問題3：レポーターの設定

テスト結果を分かりやすく出力するために、複数のレポーターを設定してください。

**要件：**
- ローカル環境ではリスト形式で出力する
- CI環境ではHTML レポートとJUnit XML形式の両方を出力する
- HTMLレポートの出力先を `test-results/html-report` にする
- JUnit XMLの出力先を `test-results/junit.xml` にする

**期待される結果：**
```
ローカル: ターミナルにリスト形式で結果が表示される
CI: HTMLレポートとJUnit XMLファイルが生成される
```

<details>
<summary>ヒント</summary>

`reporter` オプションに配列で複数のレポーターを指定できます。

```typescript
reporter: [
  ['list'],
  ['html', { outputFolder: 'test-results/html-report' }],
  ['junit', { outputFile: 'test-results/junit.xml' }],
],
```

</details>

<details>
<summary>解答例</summary>

```typescript
// ========================================
// playwright.config.ts - レポーター設定
// ========================================
import { defineConfig } from '@playwright/test';

export default defineConfig({
  // ========================================
  // reporter: テスト結果の出力形式
  // 配列で複数のレポーターを同時に使用可能
  // ========================================
  reporter: process.env.CI
    ? [
        // ========================================
        // CI環境: 複数のレポーターを併用
        // ========================================

        // GitHub Actionsのログに進捗を表示
        ['github'],

        // HTMLレポート（ブラウザで閲覧可能な詳細レポート）
        ['html', {
          outputFolder: 'test-results/html-report',
          open: 'never',  // CIでは自動で開かない
        }],

        // JUnit XML（CIツールとの連携用）
        ['junit', {
          outputFile: 'test-results/junit.xml',
        }],
      ]
    : [
        // ========================================
        // ローカル環境: リスト形式でターミナルに表示
        // ========================================
        ['list'],
      ],

  // テスト結果の出力ディレクトリ
  outputDir: 'test-results',
});
```

```bash
# HTMLレポートをブラウザで開くコマンド
npx playwright show-report test-results/html-report
```

**ポイント：**
- `list` はターミナルでの確認に適した見やすい形式です
- `html` レポートはスクリーンショットやトレースも含む詳細なレポートを生成します
- `junit` 形式はJenkins、GitLab CI、GitHub Actionsなど多くのCIツールでサポートされています
- `github` レポーターはGitHub Actionsの場合にアノテーションとして表示されます

</details>

---

## 応用問題

### 問題4：GitHub Actionsワークフローの作成

PlaywrightのE2EテストをGitHub Actionsで自動実行するワークフローファイルを作成してください。

**要件：**
- プルリクエスト時とmainブランチへのpush時にテストを実行する
- Playwrightのブラウザを自動インストールする
- テスト失敗時にHTMLレポートをArtifactとしてアップロードする
- Node.js 20を使用する

**期待される結果：**
```
.github/workflows/playwright.yml が作成され、
PR時に自動でE2Eテストが実行される
```

<details>
<summary>ヒント</summary>

Playwrightは公式のGitHub Actionsセットアップ方法を提供しています。ブラウザのインストールは `npx playwright install --with-deps` で行います。

</details>

<details>
<summary>解答例</summary>

```yaml
# ========================================
# .github/workflows/playwright.yml
# Playwright E2Eテストの自動実行ワークフロー
# ========================================
name: Playwright E2E Tests

# ========================================
# トリガー条件
# ========================================
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  e2e-tests:
    # ========================================
    # 実行環境: Ubuntu最新版
    # Playwrightはubuntu-latestでの動作が推奨されている
    # ========================================
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      # ========================================
      # Step 1: リポジトリのチェックアウト
      # ========================================
      - uses: actions/checkout@v4

      # ========================================
      # Step 2: Node.jsのセットアップ
      # ========================================
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      # ========================================
      # Step 3: 依存パッケージのインストール
      # ========================================
      - name: Install dependencies
        run: npm ci

      # ========================================
      # Step 4: Playwrightブラウザのインストール
      # --with-deps でOSレベルの依存パッケージも同時にインストール
      # ========================================
      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      # ========================================
      # Step 5: E2Eテストの実行
      # ========================================
      - name: Run Playwright tests
        run: npx playwright test

      # ========================================
      # Step 6: テスト結果のアップロード（失敗時のみ）
      # HTMLレポートとトレースファイルをArtifactとして保存
      # ========================================
      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: playwright-report
          path: test-results/
          retention-days: 14
```

**ポイント：**
- `npx playwright install --with-deps` はブラウザバイナリとOS依存パッケージを同時にインストールします
- `if: ${{ !cancelled() }}` により、テスト失敗時もレポートがアップロードされます
- `retention-days` でArtifactの保持期間を設定できます（デフォルト90日）
- Playwright公式Dockerイメージ（`mcr.microsoft.com/playwright`）を使う方法もあります

</details>

---

### 問題5：マルチブラウザテストの設定

Chromium、Firefox、WebKitの3ブラウザでテストを実行し、さらにモバイルデバイスのエミュレーションも追加してください。

**要件：**
- Chromium、Firefox、WebKitの3ブラウザでデスクトップテストを実行する
- iPhone 14とPixel 7のエミュレーションも追加する
- 全プロジェクトが認証セットアップに依存する構成にする

**期待される結果：**
```
合計5つのプロジェクトでテストが実行される:
- Desktop Chrome, Desktop Firefox, Desktop Safari
- Mobile iPhone 14, Mobile Pixel 7
```

<details>
<summary>ヒント</summary>

`devices` からデバイスプロファイルをインポートして `use` に展開します。

```typescript
import { defineConfig, devices } from '@playwright/test';

projects: [
  { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  { name: 'Mobile Safari', use: { ...devices['iPhone 14'] } },
]
```

</details>

<details>
<summary>解答例</summary>

```typescript
// ========================================
// playwright.config.ts - マルチブラウザ設定
// ========================================
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : '50%',

  projects: [
    // ========================================
    // 認証セットアップ（全プロジェクト共通）
    // ========================================
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },

    // ========================================
    // デスクトップブラウザ
    // ========================================
    {
      name: 'Desktop Chrome',
      use: {
        ...devices['Desktop Chrome'],
        storageState: '.auth/user.json',
      },
      dependencies: ['setup'],
    },
    {
      name: 'Desktop Firefox',
      use: {
        ...devices['Desktop Firefox'],
        storageState: '.auth/user.json',
      },
      dependencies: ['setup'],
    },
    {
      name: 'Desktop Safari',
      use: {
        ...devices['Desktop Safari'],
        storageState: '.auth/user.json',
      },
      dependencies: ['setup'],
    },

    // ========================================
    // モバイルデバイスエミュレーション
    // ========================================
    {
      name: 'Mobile iPhone 14',
      use: {
        // ========================================
        // デバイスプロファイルにはviewport、userAgent、
        // hasTouch、isMobileなどが含まれている
        // ========================================
        ...devices['iPhone 14'],
        storageState: '.auth/user.json',
      },
      dependencies: ['setup'],
    },
    {
      name: 'Mobile Pixel 7',
      use: {
        ...devices['Pixel 7'],
        storageState: '.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
});
```

```typescript
// ========================================
// tests/responsive.spec.ts - レスポンシブ対応のテスト
// デバイスに応じてUIが変わることを検証
// ========================================
import { test, expect } from '@playwright/test';

test('ナビゲーションが適切に表示される', async ({ page, isMobile }) => {
  await page.goto('https://example.com');

  if (isMobile) {
    // ========================================
    // モバイル: ハンバーガーメニューが表示される
    // ========================================
    await expect(page.getByRole('button', { name: 'メニュー' })).toBeVisible();
    await expect(page.getByRole('navigation')).not.toBeVisible();

    // メニューボタンをタップして開く
    await page.getByRole('button', { name: 'メニュー' }).click();
    await expect(page.getByRole('navigation')).toBeVisible();
  } else {
    // ========================================
    // デスクトップ: ナビゲーションが常時表示される
    // ========================================
    await expect(page.getByRole('navigation')).toBeVisible();
    await expect(
      page.getByRole('button', { name: 'メニュー' })
    ).not.toBeVisible();
  }
});
```

**ポイント：**
- `devices` には100種類以上のデバイスプロファイルが定義されています
- `isMobile` fixtureでモバイル/デスクトップを判定してテスト内容を分岐できます
- クロスブラウザテストはCI環境で並列実行すると効率的です
- `npx playwright devices` で利用可能なデバイス一覧を確認できます

</details>

---

### 問題6：タグを使ったテストのフィルタリング

テストにタグを付けて、実行時に特定のタグのテストだけを実行する仕組みを構築してください。

**要件：**
- `@smoke`：スモークテスト（重要な基本機能のみ）
- `@regression`：リグレッションテスト（全機能）
- `@slow`：実行が遅いテスト
- コマンドラインからタグでフィルタリングして実行できるようにする

**期待される結果：**
```
npx playwright test --grep @smoke     → スモークテストのみ実行
npx playwright test --grep @regression → リグレッションテストのみ実行
npx playwright test --grep-invert @slow → 遅いテスト以外を実行
```

<details>
<summary>ヒント</summary>

テスト名にタグを含めるか、`test.describe()` のタイトルにタグを含めます。`--grep` オプションで正規表現フィルタリングができます。

```typescript
test('@smoke ログインできる', async ({ page }) => { ... });
```

</details>

<details>
<summary>解答例</summary>

```typescript
// ========================================
// tests/auth.spec.ts - タグ付きテスト
// ========================================
import { test, expect } from '@playwright/test';

// ========================================
// テスト名にタグを含める方法
// @タグ名 を test() の第1引数に含める
// ========================================
test('@smoke ログインページが表示される', async ({ page }) => {
  await page.goto('https://example.com/login');
  await expect(page.getByRole('heading', { name: 'ログイン' })).toBeVisible();
});

test('@smoke @regression ログインに成功する', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.getByLabel('メールアドレス').fill('test@example.com');
  await page.getByLabel('パスワード').fill('password123');
  await page.getByRole('button', { name: 'ログイン' }).click();
  await expect(page).toHaveURL(/.*dashboard/);
});

test('@regression パスワードリセットフローが動作する', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.getByRole('link', { name: 'パスワードをお忘れですか？' }).click();
  await page.getByLabel('メールアドレス').fill('test@example.com');
  await page.getByRole('button', { name: 'リセットメールを送信' }).click();
  await expect(page.getByText('メールを送信しました')).toBeVisible();
});

test('@slow @regression 大量データの読み込みテスト', async ({ page }) => {
  // 実行に時間がかかるテスト
  test.setTimeout(120000);
  await page.goto('https://example.com/large-data');
  await expect(page.getByTestId('data-table')).toBeVisible({ timeout: 60000 });
  const rows = page.locator('tbody tr');
  const count = await rows.count();
  expect(count).toBeGreaterThan(1000);
});

// ========================================
// describeレベルでタグを付ける方法
// ========================================
test.describe('@smoke 基本機能', () => {
  test('トップページが表示される', async ({ page }) => {
    await page.goto('https://example.com');
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  });

  test('検索が動作する', async ({ page }) => {
    await page.goto('https://example.com');
    await page.getByPlaceholder('検索').fill('テスト');
    await page.getByPlaceholder('検索').press('Enter');
    await expect(page.getByTestId('search-results')).toBeVisible();
  });
});
```

```bash
# スモークテストのみ実行
npx playwright test --grep @smoke

# リグレッションテストのみ実行
npx playwright test --grep @regression

# 遅いテストを除外して実行
npx playwright test --grep-invert @slow

# スモークかつリグレッションのテストを実行（AND条件）
npx playwright test --grep "(?=.*@smoke)(?=.*@regression)"
```

**ポイント：**
- `--grep` は正規表現なので、AND/OR条件も表現できます
- タグベースのフィルタリングはCI/CDパイプラインで段階的テスト実行に活用できます
- PRマージ前は `@smoke` のみ、デプロイ後は `@regression` のフル実行、といった運用が一般的です

</details>

---

## チャレンジ問題

### 問題7：シャーディングによるテスト分散実行

大量のテストを複数のCI並列ジョブに分散して実行する（シャーディング）設定を行ってください。

**要件：**
- GitHub Actionsのmatrix strategyで4つのシャードに分散する
- 各シャードのテスト結果を結合する
- 結合したHTMLレポートを生成する

**期待される結果：**
```
4つのジョブが並列に実行され、
それぞれがテスト全体の1/4を担当する
最後にレポートが結合される
```

<details>
<summary>ヒント</summary>

Playwrightの `--shard` オプションでテストを分割できます。

```bash
npx playwright test --shard=1/4   # 全4分割の1番目
npx playwright test --shard=2/4   # 全4分割の2番目
```

GitHub Actionsの `matrix` で並列ジョブを作成します。

</details>

<details>
<summary>解答例</summary>

```yaml
# ========================================
# .github/workflows/playwright-sharded.yml
# シャーディングによる分散テスト実行
# ========================================
name: Playwright Sharded Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # ========================================
  # Job 1: テストを4シャードに分散して実行
  # ========================================
  e2e-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    strategy:
      # ========================================
      # fail-fast: false → 1つのシャードが失敗しても
      # 他のシャードは継続実行する
      # ========================================
      fail-fast: false
      matrix:
        # 4つのシャードを定義
        shardIndex: [1, 2, 3, 4]
        shardTotal: [4]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      # ========================================
      # --shard オプションでテストを分割実行
      # matrix.shardIndex / matrix.shardTotal で
      # 各ジョブが担当する範囲が決まる
      # ========================================
      - name: Run Playwright tests (shard ${{ matrix.shardIndex }}/${{ matrix.shardTotal }})
        run: npx playwright test --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}

      # ========================================
      # 各シャードのテスト結果をアップロード
      # ========================================
      - name: Upload test results
        if: ${{ !cancelled() }}
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report-shard-${{ matrix.shardIndex }}
          path: test-results/
          retention-days: 7

      # ========================================
      # blob-reportをアップロード（レポート結合用）
      # ========================================
      - name: Upload blob report
        if: ${{ !cancelled() }}
        uses: actions/upload-artifact@v4
        with:
          name: blob-report-${{ matrix.shardIndex }}
          path: blob-report/
          retention-days: 1

  # ========================================
  # Job 2: 全シャードのレポートを結合
  # ========================================
  merge-reports:
    if: ${{ !cancelled() }}
    needs: [e2e-tests]
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      # ========================================
      # 全シャードのblob-reportをダウンロード
      # ========================================
      - name: Download blob reports
        uses: actions/download-artifact@v4
        with:
          path: all-blob-reports
          pattern: blob-report-*
          merge-multiple: true

      # ========================================
      # レポートを結合してHTMLレポートを生成
      # ========================================
      - name: Merge reports
        run: npx playwright merge-reports --reporter html ./all-blob-reports

      - name: Upload merged HTML report
        uses: actions/upload-artifact@v4
        with:
          name: playwright-merged-report
          path: playwright-report/
          retention-days: 14
```

```typescript
// ========================================
// playwright.config.ts - シャーディング用の設定
// blob レポーターを追加しておく
// ========================================
import { defineConfig } from '@playwright/test';

export default defineConfig({
  reporter: process.env.CI
    ? [['blob'], ['github']]  // blobレポーターでシャード結合用データを出力
    : [['list']],
  // ...
});
```

**ポイント：**
- シャーディングはテストスイートが大きくなったときに実行時間を短縮する有効な手段です
- `--shard=N/M` でPlaywrightが自動的にテストを均等に分割します
- `blob` レポーターはシャード結合用の中間データを出力します
- `merge-reports` コマンドで複数シャードの結果を1つのレポートにまとめられます

</details>

---

### 問題8：トレースビューアを使ったデバッグ

テスト失敗時のデバッグ方法として、トレースビューアの活用方法を理解し、設定を行ってください。

**要件：**
- リトライ時にトレースを記録する設定を行う
- テスト内でカスタムのトレースを手動で開始・停止する
- トレースファイルを開いてデバッグ情報を確認する方法を説明する

**期待される結果：**
```
テスト失敗時にtrace.zipが生成され、
Trace Viewerで以下の情報が確認できる:
- 各ステップのスクリーンショット
- ネットワークリクエスト
- コンソールログ
- DOMスナップショット
```

<details>
<summary>ヒント</summary>

トレースの設定は `playwright.config.ts` の `use.trace` で行います。手動でトレースを開始するには `page.context().tracing.start()` を使います。

</details>

<details>
<summary>解答例</summary>

```typescript
// ========================================
// playwright.config.ts - トレース設定
// ========================================
import { defineConfig } from '@playwright/test';

export default defineConfig({
  use: {
    // ========================================
    // trace の設定オプション:
    // 'off' - 記録しない
    // 'on' - 常に記録（CI時間が増加する）
    // 'on-first-retry' - 最初のリトライ時のみ記録（推奨）
    // 'retain-on-failure' - 失敗時のみファイルを保持
    // ========================================
    trace: 'on-first-retry',
  },
  retries: process.env.CI ? 2 : 0,
});

// ========================================
// tests/debug-example.spec.ts - 手動トレース制御
// ========================================
import { test, expect } from '@playwright/test';

test('手動でトレースを記録する', async ({ page, context }) => {
  // ========================================
  // 手動でトレースを開始
  // screenshots: ステップごとのスクリーンショット
  // snapshots: DOMスナップショット
  // sources: ソースコードの表示
  // ========================================
  await context.tracing.start({
    screenshots: true,
    snapshots: true,
    sources: true,
  });

  // テストの操作
  await page.goto('https://example.com/complex-form');
  await page.getByLabel('名前').fill('テスト太郎');
  await page.getByRole('button', { name: '送信' }).click();

  // ========================================
  // トレースを停止してファイルに保存
  // ========================================
  await context.tracing.stop({
    path: 'test-results/traces/manual-trace.zip',
  });
});

test('失敗を意図的に再現してトレースで調査する', async ({ page }) => {
  // ========================================
  // このテストが失敗すると、trace: 'on-first-retry' の設定により
  // リトライ時に自動でトレースが記録される
  // ========================================
  await page.goto('https://example.com/buggy-page');

  // ステップ情報を追加（トレースに表示される）
  await test.step('フォームに入力', async () => {
    await page.getByLabel('名前').fill('テスト太郎');
    await page.getByLabel('メール').fill('test@example.com');
  });

  await test.step('送信して結果を確認', async () => {
    await page.getByRole('button', { name: '送信' }).click();
    // このアサーションが失敗するとトレースに記録される
    await expect(page.getByText('送信完了')).toBeVisible();
  });
});
```

```bash
# ========================================
# トレースファイルの確認方法
# ========================================

# ローカルでTrace Viewerを開く
npx playwright show-trace test-results/traces/manual-trace.zip

# テスト実行時にトレースを常に記録
npx playwright test --trace on

# リトライ時のみ記録
npx playwright test --trace on-first-retry
```

**ポイント：**
- Trace Viewerではタイムライン上で各操作のスクリーンショットを確認できます
- ネットワークタブでAPIリクエスト/レスポンスの詳細が見られます
- `test.step()` でトレース内のステップを整理すると、大きなテストでも見通しが良くなります
- CIで生成されたトレースはArtifactからダウンロードして `show-trace` で開けます

</details>

---

### 問題9：フレイキーテストの検出と対策

不安定なテスト（フレイキーテスト）を検出し、対策を講じるための設定とテスト改善を行ってください。

**要件：**
- フレイキーテストの一般的なパターンを特定する
- 不安定なテストを改善するリファクタリングを行う
- `test.fixme()` と `test.slow()` を使ってテストを管理する

**期待される結果：**
```
不安定だったテストが安定して通るようになり、
未解決のテストは適切にマーク・管理されている
```

<details>
<summary>ヒント</summary>

フレイキーテストの主な原因：
1. ハードコードされた `waitForTimeout()`
2. 不安定なセレクタ（`nth-child` や動的クラス名）
3. テスト間の状態依存
4. タイミング依存のアサーション

</details>

<details>
<summary>解答例</summary>

```typescript
import { test, expect } from '@playwright/test';

// ========================================
// 悪い例：フレイキーになりやすいテスト
// ========================================
/*
test('BAD: 不安定なテスト', async ({ page }) => {
  await page.goto('https://example.com/dashboard');

  // NG: ハードコードされた待機時間（環境により不安定）
  await page.waitForTimeout(3000);

  // NG: 不安定なセレクタ（CSSクラスが変わると壊れる）
  await page.click('.css-1a2b3c > div:nth-child(3) > button');

  // NG: テキストの部分一致（表示が変わると壊れる）
  const text = await page.textContent('.result');
  expect(text).toContain('3');
});
*/

// ========================================
// 良い例：安定したテスト
// ========================================
test('GOOD: 安定したテスト', async ({ page }) => {
  await page.goto('https://example.com/dashboard');

  // ========================================
  // OK: 自動待機を活用する（waitForTimeoutを使わない）
  // expect() のアサーションは自動でリトライする
  // ========================================
  await expect(page.getByRole('heading', { name: 'ダッシュボード' })).toBeVisible();

  // ========================================
  // OK: アクセシブルなロケータを使う
  // getByRole, getByLabel, getByTestId は安定している
  // ========================================
  await page.getByRole('button', { name: '更新' }).click();

  // ========================================
  // OK: 具体的なアサーション
  // ========================================
  await expect(page.getByTestId('result-count')).toHaveText('3件');
});

// ========================================
// test.fixme(): 既知のバグがあるテストをスキップ
// テストは実行されないが、レポートに記録される
// ========================================
test.fixme('サーバーバグ#123の修正待ちテスト', async ({ page }) => {
  // このテストは現在サーバーのバグにより失敗する
  // バグ修正後に fixme を外して有効化する
  await page.goto('https://example.com/buggy-feature');
  await expect(page.getByText('正常動作')).toBeVisible();
});

// ========================================
// test.slow(): 実行が遅いテストにマークを付ける
// タイムアウトが3倍に延長される
// ========================================
test.slow('大量データの表示テスト', async ({ page }) => {
  // このテストは大量データの読み込みで時間がかかる
  await page.goto('https://example.com/large-dataset');
  await expect(page.getByTestId('data-loaded')).toBeVisible();
  const rows = page.locator('tbody tr');
  const count = await rows.count();
  expect(count).toBe(10000);
});

// ========================================
// テスト間の独立性を確保するパターン
// ========================================
test.describe('独立したテスト', () => {
  test.beforeEach(async ({ page }) => {
    // ========================================
    // 各テストの前にAPIをモックしてクリーンな状態にする
    // テスト間の状態依存を排除
    // ========================================
    await page.route('**/api/data', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ items: [], total: 0 }),
      });
    });
  });

  test('初期状態で空のリストが表示される', async ({ page }) => {
    await page.goto('https://example.com/items');
    await expect(page.getByText('データがありません')).toBeVisible();
  });
});
```

```bash
# ========================================
# フレイキーテストの検出コマンド
# ========================================

# 同じテストを10回繰り返して不安定さを検出
npx playwright test --repeat-each 10

# 失敗したテストだけを再実行
npx playwright test --last-failed
```

**ポイント：**
- フレイキーテストの最大の原因は「タイミング依存」です。`waitForTimeout()` の代わりに自動待機を活用しましょう
- `getByRole()`、`getByTestId()` などの安定したロケータを使うことで、UIの細かい変更に強いテストになります
- `test.fixme()` は既知のバグ待ちテスト、`test.skip()` は環境依存のスキップ、`test.slow()` は低速テストに使い分けます
- `--repeat-each` オプションでテストを複数回実行し、フレイキーテストを事前に検出できます
- テスト間の独立性を保つため、各テストは自分で必要な状態をセットアップするようにしましょう

</details>

---

### 問題10：包括的なテスト戦略の設計

ECサイトのE2Eテスト戦略を設計してください。テストの分類、実行タイミング、環境設定を含む包括的な戦略を作成します。

**要件：**
- テストピラミッドに基づくテスト配分を設計する
- CI/CDパイプラインの各段階で実行するテストを決める
- テスト環境（開発、ステージング、本番）ごとの設定を作成する
- テストの命名規則とディレクトリ構造を定義する

**期待される結果：**
```
[テスト戦略ドキュメント]
1. テスト分類と配分
2. CI/CDパイプラインでの実行計画
3. 環境別設定
4. プロジェクト構造
```

<details>
<summary>ヒント</summary>

テストピラミッド:
- 単体テスト（70%）：高速、多数
- 統合テスト（20%）：API、コンポーネント
- E2Eテスト（10%）：重要なユーザーフローのみ

CI/CDパイプラインでは、段階的にテストを実行します：
1. プッシュ時：リント + 単体テスト
2. PR時：+ スモークテスト（E2E）
3. マージ時：+ 全E2Eテスト
4. デプロイ後：+ 本番スモークテスト

</details>

<details>
<summary>解答例</summary>

```typescript
// ========================================
// playwright.config.ts - 環境別の包括的な設定
// ========================================
import { defineConfig, devices } from '@playwright/test';

// ========================================
// 環境変数からテスト対象のURLを決定
// ========================================
const baseURLMap: Record<string, string> = {
  development: 'http://localhost:3000',
  staging: 'https://staging.example.com',
  production: 'https://www.example.com',
};

const environment = process.env.TEST_ENV || 'development';
const baseURL = baseURLMap[environment];

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI, // CIでtest.onlyの使用を禁止
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : '50%',
  timeout: 30000,

  reporter: process.env.CI
    ? [['blob'], ['github'], ['junit', { outputFile: 'test-results/junit.xml' }]]
    : [['list']],

  use: {
    baseURL,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    // セットアップ
    { name: 'setup', testMatch: /.*\.setup\.ts/ },

    // ========================================
    // スモークテスト（PR時に実行）
    // 最重要フローのみ、Chromiumだけ
    // ========================================
    {
      name: 'smoke',
      testMatch: /.*\.smoke\.ts/,
      use: { ...devices['Desktop Chrome'], storageState: '.auth/user.json' },
      dependencies: ['setup'],
    },

    // ========================================
    // リグレッションテスト（マージ時に実行）
    // 全ブラウザで全テスト
    // ========================================
    {
      name: 'regression-chrome',
      testIgnore: /.*\.smoke\.ts/,
      use: { ...devices['Desktop Chrome'], storageState: '.auth/user.json' },
      dependencies: ['setup'],
    },
    {
      name: 'regression-firefox',
      testIgnore: /.*\.smoke\.ts/,
      use: { ...devices['Desktop Firefox'], storageState: '.auth/user.json' },
      dependencies: ['setup'],
    },
    {
      name: 'regression-webkit',
      testIgnore: /.*\.smoke\.ts/,
      use: { ...devices['Desktop Safari'], storageState: '.auth/user.json' },
      dependencies: ['setup'],
    },

    // ========================================
    // モバイルテスト（マージ時に実行）
    // ========================================
    {
      name: 'mobile',
      testMatch: /.*\.mobile\.ts/,
      use: { ...devices['iPhone 14'], storageState: '.auth/user.json' },
      dependencies: ['setup'],
    },
  ],
});
```

```
# ========================================
# プロジェクト構造と命名規則
# ========================================
e2e/
├── auth.setup.ts                    # 認証セットアップ
├── pages/                           # Page Objectクラス
│   ├── base-page.ts                 # 共通基底クラス
│   ├── login-page.ts
│   ├── product-page.ts
│   ├── cart-page.ts
│   └── checkout-page.ts
├── fixtures/                        # カスタムfixture
│   └── index.ts
├── test-data/                       # テストデータ
│   ├── users.json
│   └── products.json
├── tests/
│   ├── auth/
│   │   ├── login.smoke.ts           # @smoke: ログイン基本テスト
│   │   ├── login.spec.ts            # フルテスト
│   │   └── password-reset.spec.ts
│   ├── product/
│   │   ├── search.smoke.ts          # @smoke: 商品検索基本テスト
│   │   ├── search.spec.ts
│   │   ├── detail.spec.ts
│   │   └── filter.mobile.ts         # モバイル固有テスト
│   ├── cart/
│   │   ├── add-to-cart.smoke.ts
│   │   ├── cart-management.spec.ts
│   │   └── cart.mobile.ts
│   └── checkout/
│       ├── purchase.smoke.ts        # @smoke: 購入フロー基本テスト
│       ├── payment.spec.ts
│       └── shipping.spec.ts
└── utils/                           # ユーティリティ関数
    ├── test-helpers.ts
    └── api-helpers.ts
```

```yaml
# ========================================
# .github/workflows/e2e-strategy.yml
# 段階的テスト実行の戦略
# ========================================
name: E2E Test Strategy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # ========================================
  # Stage 1: PR時 - スモークテストのみ（高速）
  # ========================================
  smoke-tests:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'npm' }
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - name: Run smoke tests
        run: npx playwright test --project=smoke
      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: smoke-report
          path: test-results/

  # ========================================
  # Stage 2: mainマージ時 - フルリグレッション
  # ========================================
  regression-tests:
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    timeout-minutes: 30
    strategy:
      fail-fast: false
      matrix:
        project: [regression-chrome, regression-firefox, regression-webkit, mobile]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'npm' }
      - run: npm ci
      - run: npx playwright install --with-deps
      - name: Run regression tests (${{ matrix.project }})
        run: npx playwright test --project=${{ matrix.project }}
        env:
          TEST_ENV: staging
      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: report-${{ matrix.project }}
          path: test-results/
```

**ポイント：**
- テストピラミッドに基づき、E2Eテストは重要なユーザーフローに絞ります
- PR時はスモークテスト（2-3分）、マージ時はフルリグレッション（10-15分）と段階的に実行します
- ファイル命名規則（`.smoke.ts`、`.mobile.ts`）でテストの分類を明確にします
- `forbidOnly: !!process.env.CI` でCI環境での `test.only()` の誤コミットを防ぎます
- 環境変数 `TEST_ENV` でテスト対象の環境を切り替えます

</details>

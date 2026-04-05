# 第8章：CI/CDとE2Eテスト戦略

## この章のゴール

- 並列実行とリトライ設定でテストを高速化・安定化できる
- GitHub Actionsで Playwright テストを自動実行できる
- テストレポートの活用方法を理解する
- トレースビューアでデバッグできる
- テスト戦略の設計とベストプラクティスを把握する

---

## 1. 並列実行

### ワーカー数の設定

Playwrightはデフォルトで複数のテストを並列に実行します。

```typescript
// playwright.config.ts
export default defineConfig({
  // ワーカー数（並列プロセス数）
  workers: 4,           // 固定数

  // またはCPUコア数に応じて
  workers: '50%',       // CPUコアの50%
  // CIでは1、ローカルでは50%がデフォルト

  // テストファイル内のテストも並列実行
  fullyParallel: true,
});
```

```
┌────────────────────────────────────────────────────┐
│ workers: 4, fullyParallel: true の場合             │
├────────────────────────────────────────────────────┤
│                                                     │
│  Worker 1 ─── login.spec:テスト1 ─── テスト2 ───→  │
│  Worker 2 ─── login.spec:テスト3 ─── テスト4 ───→  │
│  Worker 3 ─── product.spec:テスト1 ─── テスト2 ──→ │
│  Worker 4 ─── product.spec:テスト3 ──────────────→  │
│                                                     │
│  → 4つのテストが同時に進行                          │
└────────────────────────────────────────────────────┘
```

### 並列実行時の注意

```typescript
// テストが順序に依存する場合は直列実行にする
test.describe.configure({ mode: 'serial' });

test.describe('注文フロー（順序が重要）', () => {
  test('ステップ1: カートに追加', async ({ page }) => { /* ... */ });
  test('ステップ2: 配送先を入力', async ({ page }) => { /* ... */ });
  test('ステップ3: 支払い', async ({ page }) => { /* ... */ });
});
```

---

## 2. リトライ設定

不安定なテスト（Flaky Test）に対処するため、失敗時にリトライできます。

```typescript
// playwright.config.ts
export default defineConfig({
  retries: 0,          // ローカル: リトライなし
  // CIではリトライを有効にするパターン
  retries: process.env.CI ? 2 : 0,
});
```

```
テスト実行の流れ（retries: 2 の場合）:
  1回目: テスト実行 → 失敗
  2回目: リトライ1 → 失敗
  3回目: リトライ2 → 成功 ✓（3回目で成功したと報告される）
```

### リトライ時のみトレースを記録

```typescript
export default defineConfig({
  use: {
    // 最初のリトライ時にトレースを記録
    trace: 'on-first-retry',

    // 失敗時のみスクリーンショット
    screenshot: 'only-on-failure',

    // 失敗時のみ動画を記録
    video: 'on-first-retry',
  },
});
```

---

## 3. テストレポート

### レポーターの種類

```typescript
// playwright.config.ts
export default defineConfig({
  // 単一のレポーター
  reporter: 'html',

  // 複数のレポーターを同時に使用
  reporter: [
    ['html', { open: 'never' }],    // HTMLレポート
    ['list'],                         // コンソール出力
    ['junit', { outputFile: 'results.xml' }],  // JUnit XML
  ],
});
```

| レポーター | 説明 | 用途 |
|-----------|------|------|
| `list` | コンソールに一行ずつ表示 | ローカル開発 |
| `dot` | 成功=`.`、失敗=`F` で簡潔表示 | CI |
| `html` | ブラウザで開けるHTMLレポート | 詳細な結果確認 |
| `json` | JSON形式で出力 | 他ツールとの連携 |
| `junit` | JUnit XML形式 | CI/CDツールとの連携 |

### HTMLレポートの表示

```bash
npx playwright show-report
```

HTMLレポートには以下が含まれます。

- テストの成功/失敗/スキップの一覧
- 各テストの実行時間
- 失敗時のスクリーンショット
- 失敗時のエラーメッセージとスタックトレース
- トレース情報（設定時）

---

## 4. トレースビューア

**トレースビューア** は、テスト実行の各ステップを時系列で可視化するデバッグツールです。

### トレースの記録

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    trace: 'on',              // 常に記録
    // trace: 'on-first-retry',  // リトライ時のみ（推奨）
    // trace: 'retain-on-failure', // 失敗時のみ保持
  },
});
```

### トレースの確認

```bash
# HTMLレポートからトレースを開く
npx playwright show-report

# または直接トレースファイルを開く
npx playwright show-trace trace.zip
```

### トレースビューアで確認できること

```
┌──────────────────────────────────────────────────────┐
│ Trace Viewer                                          │
├──────────────────────────────────────────────────────┤
│                                                       │
│ タイムライン:                                         │
│ ──●───●───●───●───●──✕── (各ステップの時刻)          │
│                                                       │
│ 各ステップの情報:                                     │
│ ├── アクション名（click, fill, goto...）              │
│ ├── 実行前のスクリーンショット                        │
│ ├── 実行後のスクリーンショット                        │
│ ├── ネットワークリクエスト                            │
│ ├── コンソールログ                                    │
│ └── DOMの状態                                         │
│                                                       │
│ → 「何が起きて、なぜ失敗したか」が一目でわかる        │
└──────────────────────────────────────────────────────┘
```

---

## 5. GitHub Actionsでの自動実行

### 基本的なワークフロー

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright Browsers
        run: npx playwright install --with-deps

      - name: Run Playwright tests
        run: npx playwright test

      - name: Upload test report
        uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

### シャーディング（大規模テストの分散実行）

テストが多い場合、複数のジョブに分散できます。

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        shard: [1/4, 2/4, 3/4, 4/4]  # 4分割

    steps:
      # ...（セットアップは同じ）
      - name: Run Playwright tests
        run: npx playwright test --shard=${{ matrix.shard }}
```

---

## 6. マルチブラウザ・デバイステスト

### ブラウザプロジェクトの設定

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  projects: [
    // デスクトップブラウザ
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

    // モバイルデバイス
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 13'] },
    },
  ],
});
```

```bash
# 特定のプロジェクトだけ実行
npx playwright test --project=chromium
npx playwright test --project="Mobile Chrome"
```

---

## 7. テスト戦略のベストプラクティス

### どこまでE2Eテストを書くか

```
┌──────────────────────────────────────────────────────┐
│ E2Eテストで検証すべきこと                             │
├──────────────────────────────────────────────────────┤
│ ✅ ユーザーの主要な操作フロー                        │
│    （ログイン、商品購入、登録など）                   │
│ ✅ クリティカルパス                                   │
│    （お金に関わる処理、認証フロー）                   │
│ ✅ ブラウザ固有の問題が起きやすい箇所                │
│                                                       │
│ ❌ 個々のバリデーションルール                         │
│    → ユニットテストで検証                             │
│ ❌ API のレスポンス形式                               │
│    → 統合テストで検証                                 │
│ ❌ CSSの細かいスタイル                                │
│    → ビジュアルリグレッションテストで検証             │
└──────────────────────────────────────────────────────┘
```

### テストの分類とタグ付け

```typescript
// 最重要テスト（デプロイ前に必ず実行）
test('ログインできる @smoke @critical', async ({ page }) => {});

// 主要機能テスト（PR ごとに実行）
test('商品を検索できる @regression', async ({ page }) => {});

// 網羅的テスト（夜間バッチで実行）
test('全ブラウザでレイアウトが崩れない @nightly', async ({ page }) => {});
```

```bash
# スモークテストだけ実行（デプロイ前の簡易チェック）
npx playwright test --grep @smoke

# 夜間バッチ以外を実行
npx playwright test --grep-invert @nightly
```

### Flaky Test（不安定なテスト）への対処

```
┌──────────────────────────────────────────────────────┐
│ Flaky Test の原因と対策                               │
├──────────────────────────────────────────────────────┤
│ 原因                    │ 対策                        │
├─────────────────────────┼────────────────────────────┤
│ タイミングの問題        │ 自動待機に任せる            │
│ （固定sleepを使用）     │ waitForTimeout() を削除     │
│                         │                             │
│ テスト間の依存          │ テストを独立させる          │
│ （データ共有）          │ 各テストで初期化            │
│                         │                             │
│ 外部APIの不安定さ      │ APIをモックする             │
│                         │ page.route() で差し替え     │
│                         │                             │
│ アニメーション          │ アニメーションを無効化      │
│                         │ page.emulateMedia()        │
│                         │                             │
│ ロケーターが不安定      │ getByRole/getByLabel を使う │
│                         │ CSSセレクターを避ける       │
└──────────────────────────────────────────────────────┘
```

---

## 8. 実践：本番に近い設定

```typescript
// playwright.config.ts（本番プロジェクト向け）
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30000,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,  // CIで test.only を禁止
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  reporter: process.env.CI
    ? [['html', { open: 'never' }], ['github']]
    : [['html'], ['list']],

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },

  projects: [
    // 認証セットアップ
    { name: 'setup', testMatch: /.*\.setup\.ts/ },

    // デスクトップ
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], storageState: '.auth/user.json' },
      dependencies: ['setup'],
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'], storageState: '.auth/user.json' },
      dependencies: ['setup'],
    },

    // モバイル
    {
      name: 'mobile',
      use: { ...devices['iPhone 13'], storageState: '.auth/user.json' },
      dependencies: ['setup'],
    },
  ],

  // テスト前にローカルサーバーを起動
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
```

---

## まとめ

| 項目 | ポイント |
|------|---------|
| 並列実行 | `workers` と `fullyParallel` で高速化 |
| リトライ | CIでは `retries: 2` で不安定なテストに対処 |
| レポーター | `html` + `list` / CI では `github` レポーター |
| トレースビューア | 失敗時の各ステップを視覚的にデバッグ |
| GitHub Actions | `playwright install --with-deps` でセットアップ |
| シャーディング | `--shard=1/4` でテストを分散実行 |
| マルチブラウザ | `projects` でChromium/Firefox/WebKit/モバイル |
| テスト戦略 | スモーク→リグレッション→ナイトリーの3層 |
| Flaky Test | 自動待機活用、APIモック、テスト独立性で対策 |
| webServer | `webServer` 設定でテスト前にサーバー自動起動 |

### この章のまとめ

全8章を通じて、Playwrightの基本から実務レベルの E2Eテスト戦略まで学びました。実際のプロジェクトでは、まずスモークテストから始めて徐々にカバレッジを広げていくのが現実的なアプローチです。

# 第7章：Page Object Modelとテスト設計

## この章のゴール

- Page Object Model（POM）パターンの概念と利点を理解する
- POMクラスを作成してテストコードの保守性を向上できる
- Fixtureを使ったテストのセットアップを理解する
- テストデータの管理方法を学ぶ
- テストの命名規則と構成のベストプラクティスを把握する

---

## 1. Page Object Model（POM）とは

**Page Object Model** は、ページごとの操作を**クラスにまとめる**デザインパターンです。テストコードからページの内部構造（HTML、ロケーター）を隠蔽します。

### POMなしの場合（問題点）

```typescript
// テスト1
test('ログインできる', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('メールアドレス').fill('user@example.com');
  await page.getByLabel('パスワード').fill('pass123');
  await page.getByRole('button', { name: 'ログイン' }).click();
});

// テスト2（同じロケーターが重複）
test('ログイン失敗', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('メールアドレス').fill('wrong@example.com');
  await page.getByLabel('パスワード').fill('wrong');
  await page.getByRole('button', { name: 'ログイン' }).click();
  await expect(page.getByText('メールアドレスまたはパスワードが違います')).toBeVisible();
});
```

**問題**: ラベルが「メールアドレス」→「Email」に変わったら、全テストを修正する必要がある。

### POMありの場合

```
┌─────────────────────────────────────────────────────┐
│  Page Object（ページの操作をカプセル化）             │
│                                                      │
│  ┌─────────────────┐   ┌──────────────────────┐    │
│  │  LoginPage       │   │  DashboardPage       │    │
│  │                  │   │                      │    │
│  │  - emailInput    │   │  - welcomeMessage    │    │
│  │  - passwordInput │   │  - logoutButton      │    │
│  │  - loginButton   │   │                      │    │
│  │                  │   │  + getUserName()      │    │
│  │  + login(e, p)   │   │  + logout()           │    │
│  │  + getError()    │   │                      │    │
│  └────────┬─────────┘   └──────────┬───────────┘    │
│           │                         │                │
│  ┌────────▼─────────────────────────▼───────────┐    │
│  │            テストコード                       │    │
│  │  loginPage.login('user@example.com', 'pass') │    │
│  │  expect(dashboardPage.getUserName())...       │    │
│  └──────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

---

## 2. POMクラスの作成

### ログインページのPOM

```typescript
// pages/login-page.ts
import { type Locator, type Page, expect } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('メールアドレス');
    this.passwordInput = page.getByLabel('パスワード');
    this.loginButton = page.getByRole('button', { name: 'ログイン' });
    this.errorMessage = page.locator('.error-message');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toHaveText(message);
  }
}
```

### ダッシュボードページのPOM

```typescript
// pages/dashboard-page.ts
import { type Locator, type Page, expect } from '@playwright/test';

export class DashboardPage {
  readonly page: Page;
  readonly welcomeMessage: Locator;
  readonly logoutButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.welcomeMessage = page.getByTestId('welcome-message');
    this.logoutButton = page.getByRole('button', { name: 'ログアウト' });
  }

  async expectWelcome(name: string) {
    await expect(this.welcomeMessage).toContainText(name);
  }

  async logout() {
    await this.logoutButton.click();
  }
}
```

### POMを使ったテスト

```typescript
// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login-page';
import { DashboardPage } from '../pages/dashboard-page';

test.describe('ログイン機能', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('正常にログインできる', async ({ page }) => {
    await loginPage.login('user@example.com', 'password123');

    const dashboard = new DashboardPage(page);
    await dashboard.expectWelcome('user');
  });

  test('パスワードが間違っている', async ({ page }) => {
    await loginPage.login('user@example.com', 'wrong');

    await loginPage.expectError('メールアドレスまたはパスワードが違います');
  });
});
```

---

## 3. Fixture（フィクスチャ）

**Fixture** は、テストのセットアップ（前準備）を再利用可能にする仕組みです。POMとFixtureを組み合わせると、テストがさらに簡潔になります。

### カスタムFixtureの定義

```typescript
// fixtures.ts
import { test as base } from '@playwright/test';
import { LoginPage } from './pages/login-page';
import { DashboardPage } from './pages/dashboard-page';

// カスタムFixture付きのtestを定義
type MyFixtures = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
};

export const test = base.extend<MyFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await use(loginPage);  // テストにloginPageを提供
  },

  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },
});

export { expect } from '@playwright/test';
```

### Fixtureを使ったテスト

```typescript
// tests/login.spec.ts
import { test, expect } from '../fixtures';

test('正常にログインできる', async ({ loginPage, dashboardPage }) => {
  await loginPage.login('user@example.com', 'password123');
  await dashboardPage.expectWelcome('user');
});

test('パスワードが間違っている', async ({ loginPage }) => {
  await loginPage.login('user@example.com', 'wrong');
  await loginPage.expectError('メールアドレスまたはパスワードが違います');
});
```

### ログイン済みのFixture

```typescript
// fixtures.ts に追加
export const test = base.extend<MyFixtures>({
  // ログイン済みの状態を提供するFixture
  authenticatedPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'password123');
    await use(page);
  },
});
```

---

## 4. テストデータの管理

### テストデータを外部ファイルに分離

```typescript
// test-data/users.ts
export const validUser = {
  email: 'user@example.com',
  password: 'password123',
  name: '田中太郎',
};

export const invalidUser = {
  email: 'wrong@example.com',
  password: 'wrongpass',
};

export const newUser = {
  username: 'new_user',
  email: 'new@example.com',
  password: 'NewP@ss456',
};
```

```typescript
// テストで使用
import { validUser, invalidUser } from '../test-data/users';

test('正常にログインできる', async ({ loginPage, dashboardPage }) => {
  await loginPage.login(validUser.email, validUser.password);
  await dashboardPage.expectWelcome(validUser.name);
});
```

### パラメータ化テスト

同じテストを異なるデータで繰り返し実行できます。

```typescript
const loginTestCases = [
  { email: '', password: 'pass', error: 'メールアドレスを入力してください' },
  { email: 'invalid', password: 'pass', error: 'メールアドレスの形式が正しくありません' },
  { email: 'user@example.com', password: '', error: 'パスワードを入力してください' },
  { email: 'user@example.com', password: 'ab', error: 'パスワードは8文字以上です' },
];

for (const tc of loginTestCases) {
  test(`バリデーション: ${tc.error}`, async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(tc.email, tc.password);
    await loginPage.expectError(tc.error);
  });
}
```

---

## 5. テストの設計ベストプラクティス

### プロジェクト構成

```
my-playwright-tests/
├── tests/                  # テストファイル
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── register.spec.ts
│   ├── dashboard/
│   │   └── dashboard.spec.ts
│   └── products/
│       ├── product-list.spec.ts
│       └── product-detail.spec.ts
├── pages/                  # Page Objectクラス
│   ├── login-page.ts
│   ├── dashboard-page.ts
│   └── product-page.ts
├── test-data/              # テストデータ
│   └── users.ts
├── fixtures.ts             # カスタムFixture
└── playwright.config.ts
```

### テストの命名規則

```typescript
// ✅ 良い命名 — 何をテストしているか明確
test.describe('商品検索', () => {
  test('キーワードに一致する商品が表示される', async ({ page }) => {});
  test('該当商品がない場合は「見つかりません」が表示される', async ({ page }) => {});
  test('検索欄を空で送信するとエラーメッセージが表示される', async ({ page }) => {});
});

// ❌ 悪い命名 — 何をテストしているか不明
test.describe('検索テスト', () => {
  test('テスト1', async ({ page }) => {});
  test('テスト2', async ({ page }) => {});
  test('テスト3', async ({ page }) => {});
});
```

### テストの独立性

```typescript
// ✅ 良い設計 — 各テストが独立している
test('商品Aを購入できる', async ({ page }) => {
  // セットアップから始める
  await setupProduct(page, { name: '商品A', price: 1000 });
  await loginAs(page, 'buyer');
  await purchaseProduct(page, '商品A');
  await expectPurchaseSuccess(page);
});

// ❌ 悪い設計 — テスト間に依存関係がある
test('商品Aを作成する', async ({ page }) => { /* ... */ });
test('商品Aを購入する（前のテストに依存）', async ({ page }) => { /* ... */ });
```

---

## 6. 認証状態の保存と再利用

毎回ログインするのは時間がかかるため、認証状態を保存して再利用できます。

### storageState を使う

```typescript
// auth.setup.ts — 認証のセットアップ
import { test as setup } from '@playwright/test';

setup('ログインして認証状態を保存', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('メール').fill('user@example.com');
  await page.getByLabel('パスワード').fill('password123');
  await page.getByRole('button', { name: 'ログイン' }).click();
  await page.waitForURL('/dashboard');

  // Cookie やローカルストレージを含む認証状態を保存
  await page.context().storageState({ path: '.auth/user.json' });
});
```

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    // 認証のセットアップ（最初に実行）
    { name: 'setup', testMatch: /.*\.setup\.ts/ },

    // テスト本体（認証済み状態で実行）
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: '.auth/user.json',  // 保存した認証状態を使う
      },
      dependencies: ['setup'],  // setup完了後に実行
    },
  ],
});
```

---

## まとめ

| 項目 | ポイント |
|------|---------|
| POM | ページの操作をクラスにまとめるデザインパターン |
| POMの利点 | ロケーターの変更が1箇所で済む。テストコードが読みやすい |
| Fixture | テストの前準備を再利用可能にする仕組み |
| テストデータ | 外部ファイルに分離して管理する |
| パラメータ化 | `for` ループで同じテストを異なるデータで実行 |
| 命名規則 | 「何をしたらどうなるか」を明確に書く |
| テストの独立性 | 各テストが他に依存しないこと |
| 認証の再利用 | `storageState` で認証状態を保存→再利用 |

### 次の章では

CI/CD での自動実行、並列実行の設定、レポートの活用など、**実践的なE2Eテスト戦略**について学びます。

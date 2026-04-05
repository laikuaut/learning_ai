# 第7章 Page Object Modelとテスト設計 演習問題

---

## 基本問題

### 問題1：シンプルなPage Objectクラスを作成する

ログインページ用のPage Objectクラスを作成してください。ページ内の要素へのアクセスとアクション（ログイン操作）をクラスにカプセル化します。

**要件：**
- `LoginPage` クラスを作成する
- メールアドレス入力、パスワード入力、ログインボタンのLocatorをプロパティとして定義する
- `login(email, password)` メソッドでログイン操作をまとめる
- `getErrorMessage()` メソッドでエラーメッセージを取得する

**期待される結果：**
```
LoginPageクラスを使って、テストコードがシンプルになる：
  const loginPage = new LoginPage(page);
  await loginPage.login('test@example.com', 'password123');
```

<details>
<summary>ヒント</summary>

Page ObjectクラスはコンストラクタでPlaywrightの `Page` オブジェクトを受け取り、各要素のLocatorをプロパティとして保持します。

```typescript
class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('メールアドレス');
  }
}
```

</details>

<details>
<summary>解答例</summary>

```typescript
// ========================================
// login-page.ts - ログインページのPage Object
// ========================================
import { type Page, type Locator, expect } from '@playwright/test';

export class LoginPage {
  // ========================================
  // プロパティ定義
  // readonly にすることで外部から変更できないようにする
  // ========================================
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    // ========================================
    // コンストラクタでLocatorを初期化
    // Locatorは作成時にはDOMにアクセスしない（遅延評価）
    // ========================================
    this.emailInput = page.getByLabel('メールアドレス');
    this.passwordInput = page.getByLabel('パスワード');
    this.loginButton = page.getByRole('button', { name: 'ログイン' });
    this.errorMessage = page.getByTestId('error-message');
  }

  // ========================================
  // ページへの遷移
  // ========================================
  async goto() {
    await this.page.goto('https://example.com/login');
  }

  // ========================================
  // ログイン操作をひとつのメソッドにまとめる
  // テストコードから呼ぶときはこのメソッドだけでOK
  // ========================================
  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  // ========================================
  // エラーメッセージの取得
  // ========================================
  async getErrorMessage(): Promise<string> {
    return await this.errorMessage.textContent() ?? '';
  }
}

// ========================================
// login.spec.ts - テストファイル
// ========================================
import { test, expect } from '@playwright/test';
import { LoginPage } from './login-page';

test('正しい認証情報でログインできる', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('test@example.com', 'password123');

  // ログイン後のダッシュボードに遷移することを確認
  await expect(page).toHaveURL(/.*dashboard/);
});

test('間違ったパスワードでエラーが表示される', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('test@example.com', 'wrongpassword');

  // エラーメッセージが表示されることを確認
  await expect(loginPage.errorMessage).toBeVisible();
  await expect(loginPage.errorMessage).toHaveText(
    'メールアドレスまたはパスワードが正しくありません'
  );
});
```

**ポイント：**
- Page Objectパターンにより、UI変更時の修正箇所がPage Objectクラスに集約されます
- Locatorはコンストラクタで定義しますが、実際のDOM操作はメソッド呼び出し時に行われます
- テストファイルにはUIの詳細（セレクタなど）が現れず、ビジネスロジックに集中できます

</details>

---

### 問題2：Page Objectを使ったテストの書き方

問題1で作成した `LoginPage` クラスを使い、以下の3つのテストケースを書いてください。

**要件：**
- テスト1：正しい認証情報でログインするとダッシュボードに遷移する
- テスト2：空のフォームで送信するとバリデーションエラーが表示される
- テスト3：5回連続でログインに失敗するとアカウントロックメッセージが表示される

**期待される結果：**
```
テスト1: URLが /dashboard に変わる
テスト2: 「メールアドレスは必須です」エラーが表示される
テスト3: 「アカウントがロックされました」メッセージが表示される
```

<details>
<summary>ヒント</summary>

`test.describe()` でグループ化し、`test.beforeEach()` でページ遷移を共通化すると、テストがすっきりします。

```typescript
test.describe('ログインページ', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('テスト名', async ({ page }) => {
    // loginPage を使ったテスト
  });
});
```

</details>

<details>
<summary>解答例</summary>

```typescript
import { test, expect } from '@playwright/test';
import { LoginPage } from './login-page';

test.describe('ログインページのテスト', () => {
  let loginPage: LoginPage;

  // ========================================
  // beforeEach で共通のセットアップを行う
  // 各テストの前にログインページに遷移する
  // ========================================
  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('正しい認証情報でダッシュボードに遷移する', async ({ page }) => {
    await loginPage.login('admin@example.com', 'correct-password');

    // ========================================
    // ログイン成功後のURL遷移を検証
    // ========================================
    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.getByRole('heading', { name: 'ダッシュボード' })).toBeVisible();
  });

  test('空のフォームで送信するとバリデーションエラーが表示される', async () => {
    // ========================================
    // 何も入力せずにログインボタンをクリック
    // ========================================
    await loginPage.loginButton.click();

    // バリデーションエラーが表示されることを確認
    await expect(loginPage.page.getByText('メールアドレスは必須です')).toBeVisible();
  });

  test('5回連続でログインに失敗するとロックされる', async () => {
    // ========================================
    // 5回連続で間違ったパスワードでログイン試行
    // ========================================
    for (let i = 0; i < 5; i++) {
      await loginPage.login('admin@example.com', 'wrong-password');
      // 毎回フォームをリセットする場合はページ再読み込み
      if (i < 4) {
        await loginPage.goto();
      }
    }

    // ========================================
    // アカウントロックメッセージが表示されることを確認
    // ========================================
    await expect(
      loginPage.page.getByText('アカウントがロックされました')
    ).toBeVisible();
  });
});
```

**ポイント：**
- `test.describe()` でテストをグループ化すると、関連するテストが整理されます
- `beforeEach` は各テストの独立性を保ちながら、共通処理を集約できます
- Page Objectを使うとテストコードの可読性が大幅に向上します

</details>

---

### 問題3：テストデータの外部ファイル管理

テストで使用するユーザーデータを外部のJSONファイルに切り出し、テストから読み込んで使う構成を作ってください。

**要件：**
- `test-data/users.json` にテストユーザーの情報を定義する
- テストファイルからJSONを読み込んで使用する
- 管理者ユーザーと一般ユーザーの2パターンのログインテストを書く

**期待される結果：**
```
テストデータがJSONファイルから読み込まれ、
管理者・一般ユーザーそれぞれのログインが正しく検証される
```

<details>
<summary>ヒント</summary>

TypeScriptでは `import` でJSONファイルを読み込めます（`tsconfig.json` に `resolveJsonModule: true` が必要）。

```typescript
import users from './test-data/users.json';
```

または `fs` モジュールで読み込むこともできます。

</details>

<details>
<summary>解答例</summary>

```json
// ========================================
// test-data/users.json - テストデータファイル
// テストに必要なユーザー情報を一元管理する
// ========================================
{
  "admin": {
    "email": "admin@example.com",
    "password": "admin-pass-123",
    "name": "管理者太郎",
    "role": "admin"
  },
  "normalUser": {
    "email": "user@example.com",
    "password": "user-pass-456",
    "name": "一般花子",
    "role": "user"
  },
  "invalidUser": {
    "email": "invalid@example.com",
    "password": "wrong-password",
    "name": "存在しないユーザー",
    "role": "none"
  }
}
```

```typescript
// ========================================
// login-with-data.spec.ts - テストデータを外部管理するテスト
// ========================================
import { test, expect } from '@playwright/test';
import { LoginPage } from './login-page';
import users from './test-data/users.json';

test.describe('テストデータを使ったログインテスト', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('管理者ユーザーでログインすると管理メニューが表示される', async ({ page }) => {
    // ========================================
    // JSONから管理者のデータを取得してログイン
    // ========================================
    const admin = users.admin;
    await loginPage.login(admin.email, admin.password);

    await expect(page).toHaveURL(/.*dashboard/);
    // 管理者には管理メニューが表示される
    await expect(page.getByRole('link', { name: '管理画面' })).toBeVisible();
  });

  test('一般ユーザーでログインすると管理メニューが表示されない', async ({ page }) => {
    // ========================================
    // JSONから一般ユーザーのデータを取得してログイン
    // ========================================
    const user = users.normalUser;
    await loginPage.login(user.email, user.password);

    await expect(page).toHaveURL(/.*dashboard/);
    // 一般ユーザーには管理メニューが非表示
    await expect(page.getByRole('link', { name: '管理画面' })).not.toBeVisible();
  });
});
```

**ポイント：**
- テストデータを外部ファイルに切り出すと、データの変更がテストコードに影響しません
- 環境ごと（開発・ステージング・本番）にデータファイルを切り替えることも可能です
- 機密情報（本番パスワードなど）はテストデータに含めず、環境変数を使ってください

</details>

---

## 応用問題

### 問題4：カスタムfixtureの作成

`LoginPage` のインスタンス化とページ遷移を毎回手動で行うのではなく、Playwrightのfixture機能を使って自動化してください。

**要件：**
- `loginPage` fixtureを定義する（`test.extend()` を使用）
- fixtureの中でLoginPageのインスタンス化とページ遷移を行う
- テストでは `loginPage` をそのまま引数として受け取って使う

**期待される結果：**
```
テストの引数にloginPageが渡され、
セットアップなしでloginPage.login()が呼べる
```

<details>
<summary>ヒント</summary>

`test.extend()` でカスタムfixtureを定義します。

```typescript
const test = baseTest.extend<{ loginPage: LoginPage }>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await use(loginPage);  // テストに渡す
  },
});
```

</details>

<details>
<summary>解答例</summary>

```typescript
// ========================================
// fixtures.ts - カスタムfixtureの定義
// ========================================
import { test as base } from '@playwright/test';
import { LoginPage } from './login-page';

// ========================================
// fixtureの型を定義
// テストで使うPage Objectをすべてここに列挙する
// ========================================
type MyFixtures = {
  loginPage: LoginPage;
};

// ========================================
// test.extend() でカスタムfixtureを追加
// base（標準のtest）を拡張して新しいtestを作る
// ========================================
export const test = base.extend<MyFixtures>({
  loginPage: async ({ page }, use) => {
    // セットアップ：Page Object作成 + ページ遷移
    const loginPage = new LoginPage(page);
    await loginPage.goto();

    // use() でテストにfixtureを渡す
    // use() の前がセットアップ、後がティアダウン
    await use(loginPage);

    // ティアダウン（必要であればここにクリーンアップ処理を書く）
  },
});

// expectもre-exportしておくと便利
export { expect } from '@playwright/test';

// ========================================
// login.spec.ts - fixtureを使ったテスト
// ========================================
import { test, expect } from './fixtures';

// ========================================
// loginPage が自動的にfixtureとして注入される
// 手動でのnew LoginPage()やgoto()は不要
// ========================================
test('正しい認証情報でログインできる', async ({ loginPage, page }) => {
  await loginPage.login('test@example.com', 'password123');
  await expect(page).toHaveURL(/.*dashboard/);
});

test('不正なパスワードでエラーになる', async ({ loginPage }) => {
  await loginPage.login('test@example.com', 'wrong');
  await expect(loginPage.errorMessage).toBeVisible();
});
```

**ポイント：**
- `test.extend()` でfixtureを定義すると、テストコードから定型的なセットアップが消えます
- `use()` の前後でセットアップ/ティアダウンが書けます
- 複数のPage Objectをfixtureとして定義し、必要なテストにだけ注入できます

</details>

---

### 問題5：パラメタライズドテスト

複数の入力パターンで同じテストを実行するパラメタライズドテストを書いてください。

**要件：**
- 検索機能に対して、複数の検索キーワードとそれぞれの期待件数でテストする
- テストデータ: `[{ keyword: 'JavaScript', count: 5 }, { keyword: 'Python', count: 3 }, { keyword: '存在しないキーワード', count: 0 }]`
- 各パターンでテストが実行され、結果件数が一致することを確認する

**期待される結果：**
```
テスト1: "JavaScript" → 5件
テスト2: "Python" → 3件
テスト3: "存在しないキーワード" → 0件
```

<details>
<summary>ヒント</summary>

配列の `forEach` や `for...of` で `test()` を動的に生成するか、テストデータを配列で定義してループします。

```typescript
const searchData = [
  { keyword: 'JavaScript', count: 5 },
  ...
];

for (const data of searchData) {
  test(`"${data.keyword}"で検索すると${data.count}件表示`, async ({ page }) => {
    // ...
  });
}
```

</details>

<details>
<summary>解答例</summary>

```typescript
import { test, expect } from '@playwright/test';

// ========================================
// テストデータを配列で定義
// ========================================
const searchTestCases = [
  { keyword: 'JavaScript', expectedCount: 5 },
  { keyword: 'Python', expectedCount: 3 },
  { keyword: 'TypeScript', expectedCount: 4 },
  { keyword: '存在しないキーワード', expectedCount: 0 },
];

test.describe('検索機能のパラメタライズドテスト', () => {
  // ========================================
  // for...of でテストデータごとにテストを生成
  // テスト名にパラメータを含めることで、どのケースかが分かる
  // ========================================
  for (const { keyword, expectedCount } of searchTestCases) {
    test(`"${keyword}"で検索すると${expectedCount}件表示される`, async ({ page }) => {
      await page.goto('https://example.com/search');

      // ========================================
      // 検索を実行
      // ========================================
      await page.getByPlaceholder('検索キーワード').fill(keyword);
      await page.getByRole('button', { name: '検索' }).click();

      // ========================================
      // 結果件数を検証
      // ========================================
      if (expectedCount === 0) {
        await expect(page.getByText('検索結果が見つかりませんでした')).toBeVisible();
      } else {
        const results = page.getByTestId('search-result');
        await expect(results).toHaveCount(expectedCount);
      }
    });
  }
});
```

**ポイント：**
- パラメタライズドテストにより、同じテストロジックを複数のデータで実行できます
- テスト名にパラメータを含めると、失敗時にどのケースかすぐに分かります
- `test.describe()` 内で `for` ループを使うとグループ化もできます

</details>

---

### 問題6：テストプロジェクトのディレクトリ構造を設計する

ECサイトのE2Eテストプロジェクトのディレクトリ構造を設計し、主要ファイルの雛形を作成してください。

**要件：**
- `pages/` ディレクトリにPage Objectクラスを配置する
- `fixtures/` ディレクトリにカスタムfixtureをまとめる
- `test-data/` ディレクトリにテストデータを配置する
- `tests/` ディレクトリにテストファイルを配置する
- 各ディレクトリの役割とファイル構成を説明する

**期待される結果：**
```
e2e/
├── playwright.config.ts
├── pages/
│   ├── login-page.ts
│   ├── product-page.ts
│   ├── cart-page.ts
│   └── checkout-page.ts
├── fixtures/
│   └── index.ts
├── test-data/
│   ├── users.json
│   └── products.json
└── tests/
    ├── auth.spec.ts
    ├── product.spec.ts
    ├── cart.spec.ts
    └── checkout.spec.ts
```

<details>
<summary>ヒント</summary>

Page Objectは機能単位（ページ単位）で分割し、fixtureファイルで統合するのがベストプラクティスです。テストファイルはユーザーシナリオ単位で分割しましょう。

</details>

<details>
<summary>解答例</summary>

```typescript
// ========================================
// pages/product-page.ts - 商品ページのPage Object
// ========================================
import { type Page, type Locator } from '@playwright/test';

export class ProductPage {
  readonly page: Page;
  readonly productList: Locator;
  readonly searchInput: Locator;
  readonly addToCartButton: Locator;
  readonly priceLabel: Locator;

  constructor(page: Page) {
    this.page = page;
    this.productList = page.getByTestId('product-list');
    this.searchInput = page.getByPlaceholder('商品を検索');
    this.addToCartButton = page.getByRole('button', { name: 'カートに追加' });
    this.priceLabel = page.getByTestId('product-price');
  }

  async goto() {
    await this.page.goto('https://example.com/products');
  }

  async searchProduct(keyword: string) {
    await this.searchInput.fill(keyword);
    await this.searchInput.press('Enter');
  }

  async addToCart(productName: string) {
    // 特定の商品の「カートに追加」ボタンをクリック
    const product = this.page.locator('.product-card', { hasText: productName });
    await product.getByRole('button', { name: 'カートに追加' }).click();
  }
}

// ========================================
// pages/cart-page.ts - カートページのPage Object
// ========================================
import { type Page, type Locator } from '@playwright/test';

export class CartPage {
  readonly page: Page;
  readonly cartItems: Locator;
  readonly totalPrice: Locator;
  readonly checkoutButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.cartItems = page.getByTestId('cart-item');
    this.totalPrice = page.getByTestId('total-price');
    this.checkoutButton = page.getByRole('button', { name: '購入手続きへ' });
  }

  async goto() {
    await this.page.goto('https://example.com/cart');
  }

  async getItemCount(): Promise<number> {
    return await this.cartItems.count();
  }

  async proceedToCheckout() {
    await this.checkoutButton.click();
  }
}

// ========================================
// fixtures/index.ts - 全fixtureを統合
// ========================================
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/login-page';
import { ProductPage } from '../pages/product-page';
import { CartPage } from '../pages/cart-page';

type Fixtures = {
  loginPage: LoginPage;
  productPage: ProductPage;
  cartPage: CartPage;
};

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },
  productPage: async ({ page }, use) => {
    const productPage = new ProductPage(page);
    await use(productPage);
  },
  cartPage: async ({ page }, use) => {
    const cartPage = new CartPage(page);
    await use(cartPage);
  },
});

export { expect } from '@playwright/test';

// ========================================
// tests/cart.spec.ts - カート機能のテスト
// ========================================
import { test, expect } from '../fixtures';

test.describe('カート機能', () => {
  test('商品をカートに追加できる', async ({ productPage, cartPage, page }) => {
    await productPage.goto();
    await productPage.addToCart('ワイヤレスマウス');

    await cartPage.goto();
    const count = await cartPage.getItemCount();
    expect(count).toBe(1);
    await expect(page.getByText('ワイヤレスマウス')).toBeVisible();
  });
});
```

**ポイント：**
- Page Objectはページ単位で1クラスにし、UIの詳細をカプセル化します
- fixtureは `fixtures/index.ts` に統合し、テストから1か所でインポートできるようにします
- テストデータはJSON/TSファイルに切り出し、テストコードとデータを分離します
- テストファイルはユーザーシナリオ単位で分割するのが一般的です

</details>

---

## チャレンジ問題

### 問題7：複数ページにまたがるPage Objectの設計

ECサイトの購入フロー（商品選択 → カート → 決済 → 完了）をPage Objectパターンで設計し、一連のシナリオテストを書いてください。

**要件：**
- `ProductPage`、`CartPage`、`CheckoutPage`、`CompletePage` の4つのPage Objectを作成する
- 各Page Objectにページ遷移メソッドを持たせ、遷移先のPage Objectを返す
- 購入フロー全体を1つのテストで書く

**期待される結果：**
```
商品選択 → カート確認 → 決済情報入力 → 注文完了
各ステップでPage Objectが切り替わり、一連のフローが検証される
```

<details>
<summary>ヒント</summary>

ページ遷移メソッドの戻り値として次のページのPage Objectを返すと、メソッドチェーンのように使えます。

```typescript
class CartPage {
  async proceedToCheckout(): Promise<CheckoutPage> {
    await this.checkoutButton.click();
    return new CheckoutPage(this.page);
  }
}
```

</details>

<details>
<summary>解答例</summary>

```typescript
// ========================================
// pages/product-list-page.ts
// ========================================
import { type Page, type Locator } from '@playwright/test';
import { CartPage } from './cart-page';

export class ProductListPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async goto() {
    await this.page.goto('https://example.com/products');
  }

  // ========================================
  // 商品をカートに追加し、カートページに遷移
  // 戻り値として CartPage を返す（ページ遷移の連鎖）
  // ========================================
  async addToCartAndGoToCart(productName: string): Promise<CartPage> {
    const product = this.page.locator('.product-card', { hasText: productName });
    await product.getByRole('button', { name: 'カートに追加' }).click();
    await this.page.getByRole('link', { name: 'カートを見る' }).click();
    return new CartPage(this.page);
  }
}

// ========================================
// pages/cart-page.ts
// ========================================
import { type Page, type Locator } from '@playwright/test';
import { CheckoutPage } from './checkout-page';

export class CartPage {
  readonly page: Page;
  readonly cartItems: Locator;
  readonly totalPrice: Locator;

  constructor(page: Page) {
    this.page = page;
    this.cartItems = page.getByTestId('cart-item');
    this.totalPrice = page.getByTestId('total-price');
  }

  // ========================================
  // 購入手続きへ進み、CheckoutPageを返す
  // ========================================
  async proceedToCheckout(): Promise<CheckoutPage> {
    await this.page.getByRole('button', { name: '購入手続きへ' }).click();
    return new CheckoutPage(this.page);
  }
}

// ========================================
// pages/checkout-page.ts
// ========================================
import { type Page } from '@playwright/test';
import { CompletePage } from './complete-page';

export class CheckoutPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async fillShippingInfo(name: string, address: string, phone: string) {
    await this.page.getByLabel('お名前').fill(name);
    await this.page.getByLabel('住所').fill(address);
    await this.page.getByLabel('電話番号').fill(phone);
  }

  async fillPaymentInfo(cardNumber: string, expiry: string, cvv: string) {
    await this.page.getByLabel('カード番号').fill(cardNumber);
    await this.page.getByLabel('有効期限').fill(expiry);
    await this.page.getByLabel('CVV').fill(cvv);
  }

  // ========================================
  // 注文確定して完了ページに遷移
  // ========================================
  async placeOrder(): Promise<CompletePage> {
    await this.page.getByRole('button', { name: '注文を確定する' }).click();
    return new CompletePage(this.page);
  }
}

// ========================================
// pages/complete-page.ts
// ========================================
import { type Page, type Locator } from '@playwright/test';

export class CompletePage {
  readonly page: Page;
  readonly orderNumber: Locator;
  readonly thankYouMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.orderNumber = page.getByTestId('order-number');
    this.thankYouMessage = page.getByText('ご注文ありがとうございます');
  }
}

// ========================================
// tests/purchase-flow.spec.ts - 購入フロー全体のテスト
// ========================================
import { test, expect } from '@playwright/test';
import { ProductListPage } from '../pages/product-list-page';

test('商品購入フローが正常に完了する', async ({ page }) => {
  // Step 1: 商品を選択してカートへ
  const productPage = new ProductListPage(page);
  await productPage.goto();
  const cartPage = await productPage.addToCartAndGoToCart('ワイヤレスイヤホン');

  // Step 2: カート内容を確認
  await expect(cartPage.cartItems).toHaveCount(1);
  await expect(cartPage.totalPrice).toContainText('8,980');

  // Step 3: 決済情報を入力
  const checkoutPage = await cartPage.proceedToCheckout();
  await checkoutPage.fillShippingInfo('テスト太郎', '東京都渋谷区1-1-1', '03-1234-5678');
  await checkoutPage.fillPaymentInfo('4111111111111111', '12/28', '123');

  // Step 4: 注文を確定
  const completePage = await checkoutPage.placeOrder();

  // Step 5: 完了画面を検証
  await expect(completePage.thankYouMessage).toBeVisible();
  await expect(completePage.orderNumber).toBeVisible();
});
```

**ポイント：**
- ページ遷移メソッドが次のPage Objectを返すことで、フローの流れが自然に読めます
- 各Page Objectが独立しているため、個別のテストにも再利用できます
- 実務では、テストデータ（商品名、住所など）もfixtureやJSONで管理するとメンテナンスしやすくなります

</details>

---

### 問題8：storageStateを使った認証状態の再利用

ログイン処理をテストごとに毎回行うのは時間がかかります。`storageState` を使ってログイン済みの状態を保存し、各テストで再利用する仕組みを作ってください。

**要件：**
- セットアップスクリプトでログインし、認証状態をファイルに保存する
- `playwright.config.ts` で `storageState` を設定し、各テストがログイン済み状態で開始されるようにする
- 個別のテストでは手動ログイン不要で、認証済みの状態でテストが実行されることを確認する

**期待される結果：**
```
1. セットアップでログインし .auth/user.json に状態を保存
2. 各テストはログイン済み状態で開始される
3. テスト実行時間が短縮される
```

<details>
<summary>ヒント</summary>

Playwrightの `setup` プロジェクトと `storageState` を組み合わせます。

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      dependencies: ['setup'],
      use: { storageState: '.auth/user.json' },
    },
  ],
});
```

</details>

<details>
<summary>解答例</summary>

```typescript
// ========================================
// auth.setup.ts - 認証セットアップスクリプト
// setupプロジェクトとして実行され、ログイン状態を保存する
// ========================================
import { test as setup, expect } from '@playwright/test';

const authFile = '.auth/user.json';

setup('ログインして認証状態を保存する', async ({ page }) => {
  // ========================================
  // 通常のログインフローを実行
  // ========================================
  await page.goto('https://example.com/login');
  await page.getByLabel('メールアドレス').fill('test@example.com');
  await page.getByLabel('パスワード').fill('password123');
  await page.getByRole('button', { name: 'ログイン' }).click();

  // ========================================
  // ログイン完了を待つ
  // ========================================
  await expect(page).toHaveURL(/.*dashboard/);

  // ========================================
  // storageState() でCookieとlocalStorageを保存
  // このファイルが後続のテストで読み込まれる
  // ========================================
  await page.context().storageState({ path: authFile });
});

// ========================================
// playwright.config.ts - storageStateの設定
// ========================================
import { defineConfig } from '@playwright/test';

export default defineConfig({
  projects: [
    // ========================================
    // setupプロジェクト：auth.setup.tsを実行
    // 他のプロジェクトに先立って実行される
    // ========================================
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },
    // ========================================
    // メインのテストプロジェクト
    // dependencies で setup の完了を待つ
    // storageState で保存した認証状態を使う
    // ========================================
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: '.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
});

// ========================================
// tests/dashboard.spec.ts - 認証済み状態のテスト
// ログイン処理なしで、いきなり認証済みページにアクセスできる
// ========================================
import { test, expect } from '@playwright/test';

test('ダッシュボードにアクセスできる（ログイン不要）', async ({ page }) => {
  // ========================================
  // storageStateにより既にログイン済み
  // 直接ダッシュボードにアクセスできる
  // ========================================
  await page.goto('https://example.com/dashboard');
  await expect(page.getByRole('heading', { name: 'ダッシュボード' })).toBeVisible();
  await expect(page.getByText('ようこそ')).toBeVisible();
});

test('プロフィールページにアクセスできる', async ({ page }) => {
  await page.goto('https://example.com/profile');
  // ログイン済みなのでプロフィール情報が表示される
  await expect(page.getByText('test@example.com')).toBeVisible();
});
```

**ポイント：**
- `storageState` はCookieとlocalStorageを保存・復元します（セッション情報やJWTトークンなど）
- `dependencies: ['setup']` により、setupプロジェクトが完了してからテストが始まります
- `.auth/` ディレクトリは `.gitignore` に追加し、バージョン管理に含めないでください
- 管理者と一般ユーザーなど、複数の認証状態を使い分けることも可能です

</details>

---

### 問題9：管理者と一般ユーザーの認証を使い分ける

管理者と一般ユーザーで異なる認証状態を用意し、テストごとに適切な認証状態を使い分ける設計を行ってください。

**要件：**
- `.auth/admin.json` と `.auth/user.json` の2つの認証状態を用意する
- 管理者用テストと一般ユーザー用テストで別の認証状態を使う
- `playwright.config.ts` でプロジェクトを分けて設定する

**期待される結果：**
```
管理者テスト: 管理画面にアクセスできる
一般ユーザーテスト: 管理画面にはアクセスできない（403エラー）
```

<details>
<summary>ヒント</summary>

`projects` 配列に複数のプロジェクトを定義し、それぞれ異なる `storageState` を指定します。

</details>

<details>
<summary>解答例</summary>

```typescript
// ========================================
// auth.setup.ts - 2つのユーザーの認証状態を保存
// ========================================
import { test as setup } from '@playwright/test';

setup('管理者でログイン', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.getByLabel('メールアドレス').fill('admin@example.com');
  await page.getByLabel('パスワード').fill('admin-password');
  await page.getByRole('button', { name: 'ログイン' }).click();
  await page.waitForURL(/.*dashboard/);
  // 管理者の認証状態を保存
  await page.context().storageState({ path: '.auth/admin.json' });
});

setup('一般ユーザーでログイン', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.getByLabel('メールアドレス').fill('user@example.com');
  await page.getByLabel('パスワード').fill('user-password');
  await page.getByRole('button', { name: 'ログイン' }).click();
  await page.waitForURL(/.*dashboard/);
  // 一般ユーザーの認証状態を保存
  await page.context().storageState({ path: '.auth/user.json' });
});

// ========================================
// playwright.config.ts - ロール別プロジェクト設定
// ========================================
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  projects: [
    // セットアップ（認証状態の準備）
    { name: 'setup', testMatch: /.*\.setup\.ts/ },

    // ========================================
    // 管理者用テスト
    // ========================================
    {
      name: 'admin-tests',
      testDir: './tests/admin',
      use: {
        ...devices['Desktop Chrome'],
        storageState: '.auth/admin.json',
      },
      dependencies: ['setup'],
    },

    // ========================================
    // 一般ユーザー用テスト
    // ========================================
    {
      name: 'user-tests',
      testDir: './tests/user',
      use: {
        ...devices['Desktop Chrome'],
        storageState: '.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
});

// ========================================
// tests/admin/admin-panel.spec.ts
// ========================================
import { test, expect } from '@playwright/test';

test('管理者は管理画面にアクセスできる', async ({ page }) => {
  await page.goto('https://example.com/admin');
  await expect(page.getByRole('heading', { name: '管理画面' })).toBeVisible();
  await expect(page.getByText('ユーザー管理')).toBeVisible();
});

// ========================================
// tests/user/access-control.spec.ts
// ========================================
import { test, expect } from '@playwright/test';

test('一般ユーザーは管理画面にアクセスできない', async ({ page }) => {
  await page.goto('https://example.com/admin');
  // 403エラーまたはリダイレクトされることを確認
  await expect(page.getByText('アクセス権限がありません')).toBeVisible();
});
```

**ポイント：**
- テストディレクトリ（`testDir`）をロールごとに分けると、権限の混同を防げます
- 同じプロジェクトでロールを切り替えたい場合は、テスト内で `storageState` を上書きすることも可能です
- CI環境では `.auth/` ディレクトリが毎回作り直されるため、認証情報の鮮度が保たれます

</details>

# 実践課題12：ECサイト E2Eテスト + CI/CD構築 ★5

> **難易度**: ★★★★★（総合）
> **前提知識**: 第1章〜第8章（全章）
> **課題の種類**: ミニプロジェクト
> **学習目標**: 複数ページにまたがるECサイトに対して、認証・商品操作・カート・購入フローの全体をカバーするE2Eテストスイートを構築し、CI/CDパイプラインで自動実行する戦略を設計・実装する

---

## 完成イメージ

ECサイトの主要ユーザーフローを網羅したテストスイートを構築します。

```
todo-e2e-tests/
├── pages/                    # Page Objectクラス群
│   ├── login-page.ts
│   ├── product-list-page.ts
│   ├── product-detail-page.ts
│   ├── cart-page.ts
│   └── checkout-page.ts
├── fixtures/
│   └── ec-fixtures.ts        # カスタムFixture（認証状態含む）
├── test-data/
│   ├── users.ts              # テストユーザーデータ
│   └── products.ts           # テスト商品データ
├── tests/
│   ├── auth.spec.ts           # 認証テスト
│   ├── product-browse.spec.ts # 商品閲覧テスト
│   ├── cart.spec.ts           # カート操作テスト
│   ├── checkout.spec.ts       # 購入フローテスト
│   └── cross-browser.spec.ts  # クロスブラウザテスト
├── playwright.config.ts       # マルチプロジェクト設定
└── .github/workflows/e2e.yml  # CI/CDワークフロー
```

```
Running 25 tests using 4 workers

  ✓ 認証 › 正しい情報でログインできる (1.2s)
  ✓ 認証 › 間違ったパスワードでエラーが表示される (0.9s)
  ✓ 商品閲覧 › 商品一覧が表示される (0.8s)
  ✓ 商品閲覧 › カテゴリでフィルタできる (1.0s)
  ✓ カート › 商品をカートに追加できる (1.1s)
  ✓ 購入 › 商品を購入して注文完了できる (2.3s)
  ... （25テストすべてパス）

  25 passed (15.2s)
```

---

## テスト対象のHTMLファイル

以下の4つのHTMLファイルを作成してください。

### login.html（ログインページ）

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>ログイン | ECショップ</title>
  <style>
    body { font-family: sans-serif; max-width: 400px; margin: 80px auto; padding: 0 20px; }
    h1 { text-align: center; }
    form { background: #f9f9f9; padding: 24px; border-radius: 8px; }
    label { display: block; margin-top: 12px; font-weight: bold; }
    input { width: 100%; padding: 10px; margin-top: 4px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    button { width: 100%; padding: 12px; margin-top: 20px; background: #0066cc; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 1em; }
    .error { color: red; margin-top: 12px; display: none; }
  </style>
</head>
<body>
  <h1>ログイン</h1>
  <form onsubmit="return handleLogin(event)">
    <label for="email">メールアドレス</label>
    <input id="email" type="email" placeholder="email@example.com">
    <label for="password">パスワード</label>
    <input id="password" type="password" placeholder="パスワード">
    <button type="submit">ログイン</button>
    <p class="error" id="login-error"></p>
  </form>

  <script>
    const VALID_USER = { email: 'user@example.com', password: 'Password123', name: '田中太郎' };

    function handleLogin(e) {
      e.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      const errorEl = document.getElementById('login-error');

      if (!email || !password) {
        errorEl.textContent = 'メールアドレスとパスワードを入力してください';
        errorEl.style.display = 'block';
        return false;
      }

      if (email === VALID_USER.email && password === VALID_USER.password) {
        localStorage.setItem('auth', JSON.stringify({ email: VALID_USER.email, name: VALID_USER.name }));
        window.location.href = 'products.html';
      } else {
        errorEl.textContent = 'メールアドレスまたはパスワードが間違っています';
        errorEl.style.display = 'block';
      }
      return false;
    }
  </script>
</body>
</html>
```

### products.html（商品一覧ページ）

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>商品一覧 | ECショップ</title>
  <style>
    body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
    header { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 2px solid #333; margin-bottom: 20px; }
    header .user-info { display: flex; align-items: center; gap: 12px; }
    .cart-link { background: #0066cc; color: white; padding: 8px 16px; border-radius: 4px; text-decoration: none; }
    .cart-badge { background: red; color: white; border-radius: 50%; padding: 2px 8px; font-size: 0.8em; margin-left: 4px; }
    .categories { display: flex; gap: 8px; margin-bottom: 16px; }
    .categories button { padding: 6px 16px; border: 1px solid #ddd; border-radius: 20px; background: white; cursor: pointer; }
    .categories button.active { background: #0066cc; color: white; }
    .product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
    .product-card { border: 1px solid #ddd; border-radius: 8px; padding: 16px; }
    .product-card h3 { margin: 0 0 8px; }
    .product-card .price { font-size: 1.2em; font-weight: bold; color: #cc3300; }
    .product-card .category-tag { display: inline-block; background: #eee; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; margin: 4px 0; }
    .product-card button { width: 100%; padding: 8px; margin-top: 8px; background: #0066cc; color: white; border: none; border-radius: 4px; cursor: pointer; }
    .product-card button:disabled { background: #999; cursor: not-allowed; }
    .toast { position: fixed; top: 20px; right: 20px; background: #4caf50; color: white; padding: 12px 24px; border-radius: 4px; display: none; z-index: 100; }
    .toast.show { display: block; }
  </style>
</head>
<body>
  <header>
    <h1>ECショップ</h1>
    <div class="user-info">
      <span id="user-name"></span>
      <a href="cart.html" class="cart-link">カート<span class="cart-badge" id="cart-count">0</span></a>
      <button onclick="logout()" style="border:none;background:none;cursor:pointer;color:#666;">ログアウト</button>
    </div>
  </header>

  <div class="categories" role="group" aria-label="カテゴリフィルター">
    <button class="active" onclick="filterCategory('')" data-category="">すべて</button>
    <button onclick="filterCategory('electronics')" data-category="electronics">家電</button>
    <button onclick="filterCategory('books')" data-category="books">書籍</button>
    <button onclick="filterCategory('clothing')" data-category="clothing">衣類</button>
  </div>

  <div class="product-grid" id="product-grid"></div>
  <div class="toast" id="toast"></div>

  <script>
    const products = [
      { id: 1, name: 'ワイヤレスイヤホン', price: 3980, category: 'electronics', stock: 5 },
      { id: 2, name: 'Bluetooth スピーカー', price: 5480, category: 'electronics', stock: 3 },
      { id: 3, name: 'USB-C ケーブル', price: 980, category: 'electronics', stock: 10 },
      { id: 4, name: 'モバイルバッテリー', price: 2980, category: 'electronics', stock: 0 },
      { id: 5, name: 'JavaScript入門', price: 2800, category: 'books', stock: 8 },
      { id: 6, name: 'TypeScript実践ガイド', price: 3200, category: 'books', stock: 5 },
      { id: 7, name: 'コットンTシャツ', price: 1980, category: 'clothing', stock: 15 },
      { id: 8, name: 'デニムジャケット', price: 8900, category: 'clothing', stock: 2 },
    ];

    let currentCategory = '';

    function checkAuth() {
      const auth = localStorage.getItem('auth');
      if (!auth) { window.location.href = 'login.html'; return; }
      const user = JSON.parse(auth);
      document.getElementById('user-name').textContent = user.name;
    }

    function getCart() {
      return JSON.parse(localStorage.getItem('cart') || '[]');
    }

    function updateCartBadge() {
      const cart = getCart();
      document.getElementById('cart-count').textContent = cart.reduce((sum, item) => sum + item.qty, 0);
    }

    function addToCart(productId) {
      const product = products.find(p => p.id === productId);
      if (!product || product.stock === 0) return;

      const cart = getCart();
      const existing = cart.find(item => item.id === productId);
      if (existing) {
        existing.qty++;
      } else {
        cart.push({ id: product.id, name: product.name, price: product.price, qty: 1 });
      }
      localStorage.setItem('cart', JSON.stringify(cart));
      updateCartBadge();

      const toast = document.getElementById('toast');
      toast.textContent = `${product.name}をカートに追加しました`;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2000);
    }

    function filterCategory(cat) {
      currentCategory = cat;
      document.querySelectorAll('.categories button').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.category === cat);
      });
      renderProducts();
    }

    function renderProducts() {
      const filtered = currentCategory ? products.filter(p => p.category === currentCategory) : products;
      const categoryNames = { electronics: '家電', books: '書籍', clothing: '衣類' };
      document.getElementById('product-grid').innerHTML = filtered.map(p => `
        <div class="product-card" data-testid="product-card" data-product-id="${p.id}">
          <h3>${p.name}</h3>
          <span class="category-tag">${categoryNames[p.category]}</span>
          <p class="price">¥${p.price.toLocaleString()}</p>
          <p>${p.stock > 0 ? `残り${p.stock}個` : '<span style="color:red">品切れ</span>'}</p>
          <button onclick="addToCart(${p.id})" ${p.stock === 0 ? 'disabled' : ''}>
            ${p.stock > 0 ? 'カートに追加' : '品切れ'}
          </button>
        </div>
      `).join('');
    }

    function logout() {
      localStorage.removeItem('auth');
      window.location.href = 'login.html';
    }

    checkAuth();
    updateCartBadge();
    renderProducts();
  </script>
</body>
</html>
```

### cart.html（カートページ）

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>カート | ECショップ</title>
  <style>
    body { font-family: sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
    h1 { border-bottom: 2px solid #333; padding-bottom: 12px; }
    .cart-item { display: flex; justify-content: space-between; align-items: center; padding: 16px; border: 1px solid #eee; border-radius: 4px; margin-bottom: 8px; }
    .cart-item .name { font-weight: bold; }
    .cart-item .qty-controls { display: flex; align-items: center; gap: 8px; }
    .cart-item .qty-controls button { padding: 4px 10px; cursor: pointer; }
    .cart-item .remove-btn { color: red; border: none; background: none; cursor: pointer; }
    .empty-cart { text-align: center; color: #999; padding: 40px; }
    .cart-summary { background: #f5f5f5; padding: 20px; border-radius: 8px; margin-top: 20px; }
    .cart-summary .total { font-size: 1.3em; font-weight: bold; }
    .checkout-btn { display: block; width: 100%; padding: 14px; margin-top: 16px; background: #cc3300; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 1.1em; }
    .checkout-btn:disabled { background: #999; cursor: not-allowed; }
    a { color: #0066cc; }
  </style>
</head>
<body>
  <h1>ショッピングカート</h1>
  <div id="cart-items"></div>
  <p class="empty-cart" id="empty-cart" style="display:none;">カートは空です。<br><a href="products.html">商品を探す</a></p>

  <div class="cart-summary" id="cart-summary" style="display:none;">
    <p>小計: <span id="subtotal"></span></p>
    <p>送料: <span id="shipping"></span></p>
    <p class="total">合計: <span id="total"></span></p>
    <button class="checkout-btn" onclick="checkout()">レジに進む</button>
  </div>

  <p><a href="products.html">買い物を続ける</a></p>

  <script>
    function checkAuth() {
      if (!localStorage.getItem('auth')) window.location.href = 'login.html';
    }

    function getCart() { return JSON.parse(localStorage.getItem('cart') || '[]'); }
    function saveCart(cart) { localStorage.setItem('cart', JSON.stringify(cart)); }

    function updateQty(productId, delta) {
      const cart = getCart();
      const item = cart.find(i => i.id === productId);
      if (item) {
        item.qty += delta;
        if (item.qty <= 0) {
          const idx = cart.indexOf(item);
          cart.splice(idx, 1);
        }
      }
      saveCart(cart);
      renderCart();
    }

    function removeItem(productId) {
      const cart = getCart().filter(i => i.id !== productId);
      saveCart(cart);
      renderCart();
    }

    function renderCart() {
      const cart = getCart();
      const itemsEl = document.getElementById('cart-items');
      const emptyEl = document.getElementById('empty-cart');
      const summaryEl = document.getElementById('cart-summary');

      if (cart.length === 0) {
        itemsEl.innerHTML = '';
        emptyEl.style.display = 'block';
        summaryEl.style.display = 'none';
        return;
      }

      emptyEl.style.display = 'none';
      summaryEl.style.display = 'block';

      itemsEl.innerHTML = cart.map(item => `
        <div class="cart-item" data-testid="cart-item">
          <div>
            <span class="name">${item.name}</span>
            <span class="item-price">¥${item.price.toLocaleString()}</span>
          </div>
          <div class="qty-controls">
            <button onclick="updateQty(${item.id}, -1)" aria-label="数量を減らす">-</button>
            <span data-testid="item-qty">${item.qty}</span>
            <button onclick="updateQty(${item.id}, 1)" aria-label="数量を増やす">+</button>
            <button class="remove-btn" onclick="removeItem(${item.id})">削除</button>
          </div>
        </div>
      `).join('');

      const subtotal = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
      const shipping = subtotal >= 5000 ? 0 : 500;
      document.getElementById('subtotal').textContent = `¥${subtotal.toLocaleString()}`;
      document.getElementById('shipping').textContent = shipping === 0 ? '無料' : `¥${shipping}`;
      document.getElementById('total').textContent = `¥${(subtotal + shipping).toLocaleString()}`;
    }

    function checkout() {
      window.location.href = 'checkout.html';
    }

    checkAuth();
    renderCart();
  </script>
</body>
</html>
```

### checkout.html（注文確定ページ）

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>注文確定 | ECショップ</title>
  <style>
    body { font-family: sans-serif; max-width: 500px; margin: 0 auto; padding: 20px; }
    h1 { border-bottom: 2px solid #333; padding-bottom: 12px; }
    label { display: block; margin-top: 12px; font-weight: bold; }
    input { width: 100%; padding: 10px; margin-top: 4px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    .order-summary { background: #f5f5f5; padding: 16px; border-radius: 8px; margin: 20px 0; }
    .order-summary .total { font-size: 1.2em; font-weight: bold; }
    button { width: 100%; padding: 14px; margin-top: 16px; background: #cc3300; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 1.1em; }
    .success-page { text-align: center; display: none; }
    .success-page h2 { color: #2e7d32; }
    .error-msg { color: red; margin-top: 4px; display: none; }
  </style>
</head>
<body>
  <div id="checkout-form-page">
    <h1>注文情報の入力</h1>

    <div class="order-summary" id="order-summary"></div>

    <form onsubmit="return placeOrder(event)">
      <h2>配送先</h2>
      <label for="address">住所</label>
      <input id="address" type="text" placeholder="東京都渋谷区...">
      <p class="error-msg" id="address-error">住所を入力してください</p>

      <label for="phone">電話番号</label>
      <input id="phone" type="tel" placeholder="090-XXXX-XXXX">
      <p class="error-msg" id="phone-error">電話番号を入力してください</p>

      <h2>お支払い</h2>
      <label for="card-number">カード番号</label>
      <input id="card-number" type="text" placeholder="XXXX XXXX XXXX XXXX">
      <p class="error-msg" id="card-error">カード番号を入力してください</p>

      <button type="submit">注文を確定する</button>
    </form>
  </div>

  <div class="success-page" id="success-page">
    <h2>注文が完了しました！</h2>
    <p>注文番号: <strong id="order-number"></strong></p>
    <p>ご注文ありがとうございました。</p>
    <p><a href="products.html">買い物を続ける</a></p>
  </div>

  <script>
    function checkAuth() {
      if (!localStorage.getItem('auth')) window.location.href = 'login.html';
    }

    function renderOrderSummary() {
      const cart = JSON.parse(localStorage.getItem('cart') || '[]');
      if (cart.length === 0) { window.location.href = 'products.html'; return; }

      const subtotal = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
      const shipping = subtotal >= 5000 ? 0 : 500;
      const total = subtotal + shipping;

      document.getElementById('order-summary').innerHTML = `
        <p>商品数: ${cart.reduce((s, i) => s + i.qty, 0)}点</p>
        <p>小計: ¥${subtotal.toLocaleString()}</p>
        <p>送料: ${shipping === 0 ? '無料' : `¥${shipping}`}</p>
        <p class="total">合計: ¥${total.toLocaleString()}</p>
      `;
    }

    function placeOrder(e) {
      e.preventDefault();
      let hasError = false;

      const address = document.getElementById('address').value.trim();
      const phone = document.getElementById('phone').value.trim();
      const card = document.getElementById('card-number').value.trim();

      document.querySelectorAll('.error-msg').forEach(el => el.style.display = 'none');

      if (!address) { document.getElementById('address-error').style.display = 'block'; hasError = true; }
      if (!phone) { document.getElementById('phone-error').style.display = 'block'; hasError = true; }
      if (!card) { document.getElementById('card-error').style.display = 'block'; hasError = true; }

      if (!hasError) {
        // 注文確定
        const orderNumber = 'ORD-' + Date.now();
        localStorage.removeItem('cart');
        document.getElementById('checkout-form-page').style.display = 'none';
        document.getElementById('success-page').style.display = 'block';
        document.getElementById('order-number').textContent = orderNumber;
      }
      return false;
    }

    checkAuth();
    renderOrderSummary();
  </script>
</body>
</html>
```

---

## 課題の要件

### 1. Page Objectクラス（5ファイル）
- `LoginPage`: ログイン操作と検証
- `ProductListPage`: 商品一覧表示、カテゴリフィルター、カート追加
- `CartPage`: カート操作（数量変更、削除）、合計金額検証
- `CheckoutPage`: 注文情報入力、注文確定
- 各クラスのコンストラクタで認証チェック用の共通処理を含めない（Fixtureで管理）

### 2. カスタムFixture
- 認証済み状態を `storageState` または `localStorage` で管理
- テストの独立性を担保（各テスト前にカートをクリア）

### 3. テストファイル（4ファイル以上）
- **auth.spec.ts**: ログイン成功/失敗、ログアウト
- **product-browse.spec.ts**: 商品表示、カテゴリフィルター、品切れ商品
- **cart.spec.ts**: カート追加/削除/数量変更、合計金額、送料計算
- **checkout.spec.ts**: 購入フロー全体、バリデーション

### 4. CI/CD設定
- `playwright.config.ts` のマルチプロジェクト設定
- GitHub Actionsワークフロー

---

## 解答例

<details>
<summary>解答例（初心者向け ─ 基本的なPOM + テスト）</summary>

### Page Object: LoginPage

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
    this.errorMessage = page.locator('#login-error');
  }

  async goto(basePath: string) {
    await this.page.goto(`file://${basePath}/login.html`);
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toBeVisible();
    await expect(this.errorMessage).toHaveText(message);
  }
}
```

### Page Object: ProductListPage

```typescript
// pages/product-list-page.ts
import { type Locator, type Page, expect } from '@playwright/test';

export class ProductListPage {
  readonly page: Page;
  readonly userName: Locator;
  readonly cartBadge: Locator;
  readonly productCards: Locator;
  readonly toast: Locator;

  constructor(page: Page) {
    this.page = page;
    this.userName = page.locator('#user-name');
    this.cartBadge = page.locator('#cart-count');
    this.productCards = page.getByTestId('product-card');
    this.toast = page.locator('#toast');
  }

  async goto(basePath: string) {
    await this.page.goto(`file://${basePath}/products.html`);
  }

  async filterByCategory(category: string) {
    const filterName = { '': 'すべて', electronics: '家電', books: '書籍', clothing: '衣類' }[category];
    await this.page.getByRole('group', { name: 'カテゴリフィルター' })
      .getByRole('button', { name: filterName }).click();
  }

  async addToCart(productName: string) {
    const card = this.productCards.filter({ hasText: productName });
    await card.getByRole('button', { name: 'カートに追加' }).click();
  }

  async expectProductCount(count: number) {
    await expect(this.productCards).toHaveCount(count);
  }

  async expectCartBadge(count: number) {
    await expect(this.cartBadge).toHaveText(String(count));
  }

  async expectToast(message: string) {
    await expect(this.toast).toBeVisible();
    await expect(this.toast).toContainText(message);
  }

  async expectUserName(name: string) {
    await expect(this.userName).toHaveText(name);
  }

  async logout() {
    await this.page.getByRole('button', { name: 'ログアウト' }).click();
  }
}
```

### Page Object: CartPage

```typescript
// pages/cart-page.ts
import { type Locator, type Page, expect } from '@playwright/test';

export class CartPage {
  readonly page: Page;
  readonly cartItems: Locator;
  readonly emptyCart: Locator;
  readonly subtotal: Locator;
  readonly shipping: Locator;
  readonly total: Locator;
  readonly checkoutButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.cartItems = page.getByTestId('cart-item');
    this.emptyCart = page.locator('#empty-cart');
    this.subtotal = page.locator('#subtotal');
    this.shipping = page.locator('#shipping');
    this.total = page.locator('#total');
    this.checkoutButton = page.getByRole('button', { name: 'レジに進む' });
  }

  async goto(basePath: string) {
    await this.page.goto(`file://${basePath}/cart.html`);
  }

  async increaseQty(index: number) {
    await this.cartItems.nth(index).getByLabel('数量を増やす').click();
  }

  async decreaseQty(index: number) {
    await this.cartItems.nth(index).getByLabel('数量を減らす').click();
  }

  async removeItem(index: number) {
    await this.cartItems.nth(index).getByRole('button', { name: '削除' }).click();
  }

  async proceedToCheckout() {
    await this.checkoutButton.click();
  }

  async expectItemCount(count: number) {
    await expect(this.cartItems).toHaveCount(count);
  }

  async expectEmpty() {
    await expect(this.emptyCart).toBeVisible();
  }

  async expectTotal(amount: string) {
    await expect(this.total).toHaveText(amount);
  }

  async expectShipping(text: string) {
    await expect(this.shipping).toHaveText(text);
  }

  async expectItemQty(index: number, qty: string) {
    await expect(this.cartItems.nth(index).getByTestId('item-qty')).toHaveText(qty);
  }
}
```

### Page Object: CheckoutPage

```typescript
// pages/checkout-page.ts
import { type Locator, type Page, expect } from '@playwright/test';

export class CheckoutPage {
  readonly page: Page;
  readonly addressInput: Locator;
  readonly phoneInput: Locator;
  readonly cardInput: Locator;
  readonly submitButton: Locator;
  readonly successPage: Locator;
  readonly orderNumber: Locator;

  constructor(page: Page) {
    this.page = page;
    this.addressInput = page.getByLabel('住所');
    this.phoneInput = page.getByLabel('電話番号');
    this.cardInput = page.getByLabel('カード番号');
    this.submitButton = page.getByRole('button', { name: '注文を確定する' });
    this.successPage = page.locator('#success-page');
    this.orderNumber = page.locator('#order-number');
  }

  async goto(basePath: string) {
    await this.page.goto(`file://${basePath}/checkout.html`);
  }

  async fillShipping(address: string, phone: string) {
    await this.addressInput.fill(address);
    await this.phoneInput.fill(phone);
  }

  async fillPayment(cardNumber: string) {
    await this.cardInput.fill(cardNumber);
  }

  async placeOrder() {
    await this.submitButton.click();
  }

  async expectOrderSuccess() {
    await expect(this.successPage).toBeVisible();
    await expect(this.orderNumber).not.toBeEmpty();
  }

  async expectValidationError(fieldId: string) {
    await expect(this.page.locator(`#${fieldId}`)).toBeVisible();
  }
}
```

### カスタムFixture

```typescript
// fixtures/ec-fixtures.ts
import { test as base } from '@playwright/test';
import path from 'path';
import { LoginPage } from '../pages/login-page';
import { ProductListPage } from '../pages/product-list-page';
import { CartPage } from '../pages/cart-page';
import { CheckoutPage } from '../pages/checkout-page';

const BASE_PATH = path.resolve(__dirname, '..');

type EcFixtures = {
  basePath: string;
  loginPage: LoginPage;
  productListPage: ProductListPage;
  cartPage: CartPage;
  checkoutPage: CheckoutPage;
  authenticatedPage: ProductListPage;
};

export const test = base.extend<EcFixtures>({
  basePath: BASE_PATH,

  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto(BASE_PATH);
    await use(loginPage);
  },

  productListPage: async ({ page }, use) => {
    await use(new ProductListPage(page));
  },

  cartPage: async ({ page }, use) => {
    await use(new CartPage(page));
  },

  checkoutPage: async ({ page }, use) => {
    await use(new CheckoutPage(page));
  },

  // 認証済み + カートクリア状態
  authenticatedPage: async ({ page }, use) => {
    // 認証情報をセット
    await page.goto(`file://${BASE_PATH}/login.html`);
    await page.evaluate(() => {
      localStorage.setItem('auth', JSON.stringify({ email: 'user@example.com', name: '田中太郎' }));
      localStorage.removeItem('cart');
    });
    await page.goto(`file://${BASE_PATH}/products.html`);
    const productPage = new ProductListPage(page);
    await use(productPage);
  },
});

export { expect } from '@playwright/test';
```

### 認証テスト

```typescript
// tests/auth.spec.ts
// 学べる内容：認証フローのE2Eテスト
// 実行方法：npx playwright test tests/auth.spec.ts --project=chromium

import { test, expect } from '../fixtures/ec-fixtures';

test.describe('認証', () => {

  test('正しい情報でログインできる', async ({ loginPage, page }) => {
    await loginPage.login('user@example.com', 'Password123');
    await expect(page).toHaveURL(/products\.html/);
  });

  test('間違ったパスワードでエラーが表示される', async ({ loginPage }) => {
    await loginPage.login('user@example.com', 'wrong');
    await loginPage.expectError('メールアドレスまたはパスワードが間違っています');
  });

  test('空入力でエラーが表示される', async ({ loginPage }) => {
    await loginPage.login('', '');
    await loginPage.expectError('メールアドレスとパスワードを入力してください');
  });

  test('ログアウトするとログインページに戻る', async ({ authenticatedPage, page }) => {
    await authenticatedPage.expectUserName('田中太郎');
    await authenticatedPage.logout();
    await expect(page).toHaveURL(/login\.html/);
  });
});
```

### 商品閲覧テスト

```typescript
// tests/product-browse.spec.ts
import { test, expect } from '../fixtures/ec-fixtures';

test.describe('商品閲覧', () => {

  test('全商品が表示される', async ({ authenticatedPage }) => {
    await authenticatedPage.expectProductCount(8);
  });

  test('ユーザー名が表示される', async ({ authenticatedPage }) => {
    await authenticatedPage.expectUserName('田中太郎');
  });

  test('カテゴリでフィルタできる', async ({ authenticatedPage }) => {
    await authenticatedPage.filterByCategory('electronics');
    await authenticatedPage.expectProductCount(4);

    await authenticatedPage.filterByCategory('books');
    await authenticatedPage.expectProductCount(2);

    await authenticatedPage.filterByCategory('');
    await authenticatedPage.expectProductCount(8);
  });

  test('商品をカートに追加するとバッジが更新される', async ({ authenticatedPage }) => {
    await authenticatedPage.addToCart('USB-C ケーブル');
    await authenticatedPage.expectCartBadge(1);
    await authenticatedPage.expectToast('USB-C ケーブルをカートに追加しました');
  });

  test('品切れ商品はカートに追加できない', async ({ authenticatedPage, page }) => {
    const card = authenticatedPage.productCards.filter({ hasText: 'モバイルバッテリー' });
    const button = card.getByRole('button');
    await expect(button).toBeDisabled();
    await expect(button).toHaveText('品切れ');
  });
});
```

### カートテスト

```typescript
// tests/cart.spec.ts
import { test, expect } from '../fixtures/ec-fixtures';

test.describe('カート操作', () => {

  test('空のカートで空メッセージが表示される', async ({ authenticatedPage, cartPage, basePath, page }) => {
    await cartPage.goto(basePath);
    await cartPage.expectEmpty();
  });

  test('商品をカートに追加して確認できる', async ({ authenticatedPage, cartPage, basePath, page }) => {
    await authenticatedPage.addToCart('USB-C ケーブル');
    await cartPage.goto(basePath);
    await cartPage.expectItemCount(1);
  });

  test('数量を増減できる', async ({ authenticatedPage, cartPage, basePath, page }) => {
    await authenticatedPage.addToCart('USB-C ケーブル');
    await cartPage.goto(basePath);

    await cartPage.increaseQty(0);
    await cartPage.expectItemQty(0, '2');

    await cartPage.decreaseQty(0);
    await cartPage.expectItemQty(0, '1');
  });

  test('商品を削除できる', async ({ authenticatedPage, cartPage, basePath }) => {
    await authenticatedPage.addToCart('USB-C ケーブル');
    await cartPage.goto(basePath);

    await cartPage.removeItem(0);
    await cartPage.expectEmpty();
  });

  test('5000円以上で送料無料になる', async ({ authenticatedPage, cartPage, basePath, page }) => {
    // Bluetooth スピーカー ¥5,480
    await authenticatedPage.addToCart('Bluetooth スピーカー');
    await cartPage.goto(basePath);

    await cartPage.expectShipping('無料');
    await cartPage.expectTotal('¥5,480');
  });

  test('5000円未満で送料500円がかかる', async ({ authenticatedPage, cartPage, basePath, page }) => {
    // USB-C ケーブル ¥980
    await authenticatedPage.addToCart('USB-C ケーブル');
    await cartPage.goto(basePath);

    await cartPage.expectShipping('¥500');
    await cartPage.expectTotal('¥1,480');
  });
});
```

### 購入フローテスト

```typescript
// tests/checkout.spec.ts
import { test, expect } from '../fixtures/ec-fixtures';

test.describe('購入フロー', () => {

  test('商品を購入して注文完了できる', async ({ authenticatedPage, cartPage, checkoutPage, basePath, page }) => {
    // 商品をカートに追加
    await authenticatedPage.addToCart('ワイヤレスイヤホン');

    // カートに移動
    await cartPage.goto(basePath);
    await cartPage.expectItemCount(1);
    await cartPage.proceedToCheckout();

    // 注文情報を入力
    await checkoutPage.fillShipping('東京都渋谷区1-1-1', '090-1234-5678');
    await checkoutPage.fillPayment('4111111111111111');
    await checkoutPage.placeOrder();

    // 注文完了を確認
    await checkoutPage.expectOrderSuccess();
  });

  test('住所が未入力でバリデーションエラー', async ({ authenticatedPage, cartPage, checkoutPage, basePath }) => {
    await authenticatedPage.addToCart('USB-C ケーブル');
    await cartPage.goto(basePath);
    await cartPage.proceedToCheckout();

    // 住所を空にして送信
    await checkoutPage.fillPayment('4111111111111111');
    await checkoutPage.fillShipping('', '090-1234-5678');
    await checkoutPage.placeOrder();

    await checkoutPage.expectValidationError('address-error');
  });

  test('全項目が空でバリデーションエラー', async ({ authenticatedPage, cartPage, checkoutPage, basePath }) => {
    await authenticatedPage.addToCart('USB-C ケーブル');
    await cartPage.goto(basePath);
    await cartPage.proceedToCheckout();

    await checkoutPage.placeOrder();

    await checkoutPage.expectValidationError('address-error');
    await checkoutPage.expectValidationError('phone-error');
    await checkoutPage.expectValidationError('card-error');
  });
});
```

</details>

<details>
<summary>解答例（改良版 ─ CI/CD設定とテスト戦略）</summary>

### playwright.config.ts

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 15000,
  expect: { timeout: 5000 },
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: [
    ['list'],
    ['html', { open: 'never' }],
    ...(process.env.CI ? [['github' as const]] : []),
  ],
  use: {
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
    video: 'on-first-retry',
  },
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
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 13'] },
    },
  ],
});
```

### GitHub Actions ワークフロー

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  e2e-test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        project: [chromium, firefox, webkit]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps ${{ matrix.project }}

      - name: Run tests
        run: npx playwright test --project=${{ matrix.project }}

      - name: Upload report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report-${{ matrix.project }}
          path: playwright-report/
          retention-days: 14

      - name: Upload traces
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: test-traces-${{ matrix.project }}
          path: test-results/
          retention-days: 7
```

### テスト戦略の設計ドキュメント

```typescript
/**
 * E2Eテスト戦略
 *
 * 1. テストの分類
 *    - @smoke: 最重要パス（ログイン→商品閲覧→カート追加→購入）
 *    - @regression: 全機能の網羅テスト
 *    - @edge: エッジケース・境界値テスト
 *
 * 2. 実行タイミング
 *    - PR作成時: @smoke テストのみ（高速フィードバック）
 *    - main マージ時: @smoke + @regression
 *    - 定期実行（毎日深夜）: 全テスト（@edge含む）
 *
 * 3. ブラウザ戦略
 *    - PR時: Chromiumのみ
 *    - main時: Chromium + Firefox + WebKit
 *    - モバイル: 週次で実行
 *
 * 4. テストデータ戦略
 *    - localStorage を使って認証・カートの状態を管理
 *    - 各テスト前にlocalStorageをクリアして独立性を担保
 *    - テストデータは test-data/ に外出しして一元管理
 */
```

**初心者向けとの違い:**
- マルチブラウザ（Chromium/Firefox/WebKit）+ モバイル端末のテスト設定
- GitHub Actionsでブラウザごとに並列実行（`matrix`戦略）
- 失敗時のトレースとスクリーンショットをアーティファクトとして保存
- テスト戦略を明文化し、実行タイミングとスコープを定義
- `@smoke`/`@regression`/`@edge` のタグ分類で実行対象を制御

</details>

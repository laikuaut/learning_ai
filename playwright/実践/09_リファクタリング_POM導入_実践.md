# 実践課題09：リファクタリング ─ Page Object Model導入 ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第2章（ロケーター）、第4章（アサーション）、第7章（Page Object Modelとテスト設計）
> **課題の種類**: リファクタリング
> **学習目標**: 「動くが保守しにくい」テストコードをPage Object Model（POM）パターンで書き直し、保守性・再利用性を向上させる力を養う

---

## 課題の説明

以下は「ブログアプリのE2Eテストスイート」です。**テスト自体は正しく動作します**が、以下の問題を抱えています。

- ロケーターがテストのあちこちに散らばっている
- 同じ操作が複数のテストにコピー＆ペーストされている
- UIが変更されたとき、全テストを修正する必要がある
- テストの意図がロケーターの詳細に埋もれて読みにくい

**このテストコードをPage Object Modelで段階的にリファクタリングしてください。**

### ゴール

1. **ステップ1**: ロケーターをPage Objectクラスに集約する
2. **ステップ2**: 操作メソッドを追加して重複を排除する
3. **ステップ3**: カスタムFixtureを導入してテストをさらに簡潔にする

---

## テスト対象のHTMLファイル

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>ブログアプリ</title>
  <style>
    body { font-family: sans-serif; max-width: 700px; margin: 40px auto; padding: 0 20px; }
    nav { display: flex; gap: 16px; padding: 12px 0; border-bottom: 2px solid #333; margin-bottom: 20px; }
    nav a { text-decoration: none; color: #333; font-weight: bold; }
    .post { border: 1px solid #ddd; padding: 16px; margin: 12px 0; border-radius: 8px; }
    .post h2 { margin-top: 0; }
    .post .meta { color: #666; font-size: 0.9em; }
    .post .actions { margin-top: 12px; }
    .post .actions button { margin-right: 8px; padding: 4px 12px; cursor: pointer; }
    form { max-width: 500px; }
    form label { display: block; margin-top: 12px; font-weight: bold; }
    form input, form textarea { width: 100%; padding: 8px; margin-top: 4px; box-sizing: border-box; }
    form textarea { height: 150px; }
    form button { margin-top: 16px; padding: 8px 24px; background: #0066cc; color: white; border: none; border-radius: 4px; cursor: pointer; }
    .message { padding: 12px; margin: 12px 0; border-radius: 4px; }
    .message.success { background: #e8f5e9; color: #2e7d32; }
    .message.error { background: #ffeaea; color: #c62828; }
    #page-title { display: none; }
  </style>
</head>
<body>
  <nav>
    <a href="#" onclick="showPage('list')">記事一覧</a>
    <a href="#" onclick="showPage('new')">新規作成</a>
  </nav>

  <div id="list-page">
    <h1>記事一覧</h1>
    <div id="post-list"></div>
  </div>

  <div id="new-page" style="display:none;">
    <h1>新規記事作成</h1>
    <form id="post-form" onsubmit="return createPost(event)">
      <label for="post-title">タイトル</label>
      <input id="post-title" type="text" placeholder="記事のタイトル">

      <label for="post-author">著者名</label>
      <input id="post-author" type="text" placeholder="著者名を入力">

      <label for="post-body">本文</label>
      <textarea id="post-body" placeholder="記事の本文を入力"></textarea>

      <button type="submit">公開する</button>
    </form>
    <p class="message error" id="form-error" style="display:none;"></p>
  </div>

  <div id="detail-page" style="display:none;">
    <h1 id="detail-title"></h1>
    <p class="meta" id="detail-meta"></p>
    <div id="detail-body"></div>
    <button onclick="showPage('list')">一覧に戻る</button>
  </div>

  <p class="message success" id="success-msg" style="display:none;"></p>

  <span id="page-title"></span>

  <script>
    let posts = [
      { id: 1, title: 'Playwrightの始め方', author: '田中太郎', body: 'PlaywrightはMicrosoft製のE2Eテストフレームワークです。', date: '2024-04-01' },
      { id: 2, title: 'TypeScriptの基礎', author: '佐藤花子', body: 'TypeScriptはJavaScriptに型システムを追加した言語です。', date: '2024-03-15' },
    ];
    let nextId = 3;

    function showPage(page) {
      document.getElementById('list-page').style.display = page === 'list' ? 'block' : 'none';
      document.getElementById('new-page').style.display = page === 'new' ? 'block' : 'none';
      document.getElementById('detail-page').style.display = page === 'detail' ? 'block' : 'none';
      document.getElementById('page-title').textContent = page;
      if (page === 'list') renderPosts();
    }

    function renderPosts() {
      const list = document.getElementById('post-list');
      list.innerHTML = posts.map(p => `
        <div class="post" data-testid="post-card">
          <h2>${p.title}</h2>
          <p class="meta">著者: ${p.author} | ${p.date}</p>
          <p>${p.body.substring(0, 50)}...</p>
          <div class="actions">
            <button onclick="showDetail(${p.id})">詳細</button>
            <button onclick="deletePost(${p.id})">削除</button>
          </div>
        </div>
      `).join('');
    }

    function showDetail(id) {
      const post = posts.find(p => p.id === id);
      if (!post) return;
      document.getElementById('detail-title').textContent = post.title;
      document.getElementById('detail-meta').textContent = `著者: ${post.author} | ${post.date}`;
      document.getElementById('detail-body').textContent = post.body;
      showPage('detail');
    }

    function deletePost(id) {
      posts = posts.filter(p => p.id !== id);
      showSuccess('記事を削除しました');
      renderPosts();
    }

    function createPost(e) {
      e.preventDefault();
      const title = document.getElementById('post-title').value.trim();
      const author = document.getElementById('post-author').value.trim();
      const body = document.getElementById('post-body').value.trim();

      if (!title || !author || !body) {
        document.getElementById('form-error').textContent = 'すべての項目を入力してください';
        document.getElementById('form-error').style.display = 'block';
        return false;
      }

      posts.push({ id: nextId++, title, author, body, date: new Date().toISOString().split('T')[0] });
      document.getElementById('post-form').reset();
      document.getElementById('form-error').style.display = 'none';
      showSuccess('記事を公開しました');
      showPage('list');
      return false;
    }

    function showSuccess(msg) {
      const el = document.getElementById('success-msg');
      el.textContent = msg;
      el.style.display = 'block';
      setTimeout(() => el.style.display = 'none', 3000);
    }

    renderPosts();
  </script>
</body>
</html>
```

---

## リファクタリング対象のテストコード

```typescript
// tests/blog-before-refactor.spec.ts
// 動作するが保守性が低いコード。POMで書き直してください。

import { test, expect } from '@playwright/test';
import path from 'path';

const TEST_PAGE = path.resolve(__dirname, '../blog-app.html');

test.describe('ブログアプリ', () => {

  test('記事一覧が表示される', async ({ page }) => {
    await page.goto(`file://${TEST_PAGE}`);
    const posts = page.locator('[data-testid="post-card"]');
    await expect(posts).toHaveCount(2);
    await expect(posts.first().locator('h2')).toHaveText('Playwrightの始め方');
    await expect(posts.nth(1).locator('h2')).toHaveText('TypeScriptの基礎');
  });

  test('記事の詳細を表示できる', async ({ page }) => {
    await page.goto(`file://${TEST_PAGE}`);
    await page.locator('[data-testid="post-card"]').first().locator('button:has-text("詳細")').click();
    await expect(page.locator('#detail-title')).toHaveText('Playwrightの始め方');
    await expect(page.locator('#detail-meta')).toContainText('田中太郎');
    await expect(page.locator('#detail-body')).toContainText('Microsoft製');
  });

  test('詳細から一覧に戻れる', async ({ page }) => {
    await page.goto(`file://${TEST_PAGE}`);
    await page.locator('[data-testid="post-card"]').first().locator('button:has-text("詳細")').click();
    await expect(page.locator('#detail-page')).toBeVisible();
    await page.locator('button:has-text("一覧に戻る")').click();
    await expect(page.locator('#list-page')).toBeVisible();
  });

  test('新しい記事を作成できる', async ({ page }) => {
    await page.goto(`file://${TEST_PAGE}`);
    await page.locator('nav a:has-text("新規作成")').click();
    await page.locator('#post-title').fill('テスト記事');
    await page.locator('#post-author').fill('テスト著者');
    await page.locator('#post-body').fill('これはテスト記事の本文です。');
    await page.locator('button[type="submit"]').click();
    await expect(page.locator('#success-msg')).toBeVisible();
    await expect(page.locator('#success-msg')).toHaveText('記事を公開しました');
    const posts = page.locator('[data-testid="post-card"]');
    await expect(posts).toHaveCount(3);
  });

  test('入力不備で記事作成するとエラーになる', async ({ page }) => {
    await page.goto(`file://${TEST_PAGE}`);
    await page.locator('nav a:has-text("新規作成")').click();
    await page.locator('#post-title').fill('タイトルだけ');
    await page.locator('button[type="submit"]').click();
    await expect(page.locator('#form-error')).toBeVisible();
    await expect(page.locator('#form-error')).toHaveText('すべての項目を入力してください');
  });

  test('記事を削除できる', async ({ page }) => {
    await page.goto(`file://${TEST_PAGE}`);
    const posts = page.locator('[data-testid="post-card"]');
    await expect(posts).toHaveCount(2);
    await posts.first().locator('button:has-text("削除")').click();
    await expect(posts).toHaveCount(1);
    await expect(page.locator('#success-msg')).toHaveText('記事を削除しました');
  });
});
```

---

## ステップガイド

<details>
<summary>ステップ1：Page Objectクラスを作る</summary>

まず、記事一覧ページのPOMクラスを作ります。

```typescript
// pages/post-list-page.ts
import { type Locator, type Page, expect } from '@playwright/test';

export class PostListPage {
  readonly page: Page;
  readonly posts: Locator;

  constructor(page: Page) {
    this.page = page;
    this.posts = page.getByTestId('post-card');
  }

  async expectPostCount(count: number) {
    await expect(this.posts).toHaveCount(count);
  }

  // ...メソッドを追加していく
}
```

</details>

<details>
<summary>ステップ2：テストコードからPOMを使う</summary>

```typescript
test('記事一覧が表示される', async ({ page }) => {
  await page.goto(`file://${TEST_PAGE}`);
  const listPage = new PostListPage(page);
  await listPage.expectPostCount(2);
});
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け ─ 基本的なPOMクラス）</summary>

### POMクラス

```typescript
// pages/post-list-page.ts
import { type Locator, type Page, expect } from '@playwright/test';

export class PostListPage {
  readonly page: Page;
  readonly posts: Locator;
  readonly successMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.posts = page.getByTestId('post-card');
    this.successMessage = page.locator('#success-msg');
  }

  async goto(filePath: string) {
    await this.page.goto(`file://${filePath}`);
  }

  async expectPostCount(count: number) {
    await expect(this.posts).toHaveCount(count);
  }

  async expectPostTitle(index: number, title: string) {
    await expect(this.posts.nth(index).locator('h2')).toHaveText(title);
  }

  async clickDetail(index: number) {
    await this.posts.nth(index).getByRole('button', { name: '詳細' }).click();
  }

  async clickDelete(index: number) {
    await this.posts.nth(index).getByRole('button', { name: '削除' }).click();
  }

  async navigateToNewPost() {
    await this.page.getByRole('link', { name: '新規作成' }).click();
  }

  async expectSuccess(message: string) {
    await expect(this.successMessage).toBeVisible();
    await expect(this.successMessage).toHaveText(message);
  }
}
```

```typescript
// pages/post-detail-page.ts
import { type Locator, type Page, expect } from '@playwright/test';

export class PostDetailPage {
  readonly page: Page;
  readonly title: Locator;
  readonly meta: Locator;
  readonly body: Locator;
  readonly backButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.title = page.locator('#detail-title');
    this.meta = page.locator('#detail-meta');
    this.body = page.locator('#detail-body');
    this.backButton = page.getByRole('button', { name: '一覧に戻る' });
  }

  async expectTitle(title: string) {
    await expect(this.title).toHaveText(title);
  }

  async expectAuthor(author: string) {
    await expect(this.meta).toContainText(author);
  }

  async expectBodyContains(text: string) {
    await expect(this.body).toContainText(text);
  }

  async goBackToList() {
    await this.backButton.click();
  }
}
```

```typescript
// pages/new-post-page.ts
import { type Locator, type Page, expect } from '@playwright/test';

export class NewPostPage {
  readonly page: Page;
  readonly titleInput: Locator;
  readonly authorInput: Locator;
  readonly bodyInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.titleInput = page.getByLabel('タイトル');
    this.authorInput = page.getByLabel('著者名');
    this.bodyInput = page.getByLabel('本文');
    this.submitButton = page.getByRole('button', { name: '公開する' });
    this.errorMessage = page.locator('#form-error');
  }

  async createPost(title: string, author: string, body: string) {
    await this.titleInput.fill(title);
    await this.authorInput.fill(author);
    await this.bodyInput.fill(body);
    await this.submitButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toBeVisible();
    await expect(this.errorMessage).toHaveText(message);
  }
}
```

### POMを使ったテスト

```typescript
// tests/blog-with-pom.spec.ts
// 学べる内容：POMパターンによるテストの保守性向上
// 実行方法：npx playwright test tests/blog-with-pom.spec.ts --project=chromium

import { test, expect } from '@playwright/test';
import path from 'path';
import { PostListPage } from '../pages/post-list-page';
import { PostDetailPage } from '../pages/post-detail-page';
import { NewPostPage } from '../pages/new-post-page';

const TEST_PAGE = path.resolve(__dirname, '../blog-app.html');

test.describe('ブログアプリ（POM版）', () => {
  let listPage: PostListPage;

  test.beforeEach(async ({ page }) => {
    listPage = new PostListPage(page);
    await listPage.goto(TEST_PAGE);
  });

  test('記事一覧が表示される', async ({ page }) => {
    await listPage.expectPostCount(2);
    await listPage.expectPostTitle(0, 'Playwrightの始め方');
    await listPage.expectPostTitle(1, 'TypeScriptの基礎');
  });

  test('記事の詳細を表示できる', async ({ page }) => {
    await listPage.clickDetail(0);

    const detailPage = new PostDetailPage(page);
    await detailPage.expectTitle('Playwrightの始め方');
    await detailPage.expectAuthor('田中太郎');
    await detailPage.expectBodyContains('Microsoft製');
  });

  test('詳細から一覧に戻れる', async ({ page }) => {
    await listPage.clickDetail(0);

    const detailPage = new PostDetailPage(page);
    await detailPage.goBackToList();

    await expect(page.locator('#list-page')).toBeVisible();
  });

  test('新しい記事を作成できる', async ({ page }) => {
    await listPage.navigateToNewPost();

    const newPostPage = new NewPostPage(page);
    await newPostPage.createPost('テスト記事', 'テスト著者', 'これはテスト記事の本文です。');

    await listPage.expectSuccess('記事を公開しました');
    await listPage.expectPostCount(3);
  });

  test('入力不備で記事作成するとエラーになる', async ({ page }) => {
    await listPage.navigateToNewPost();

    const newPostPage = new NewPostPage(page);
    await newPostPage.createPost('タイトルだけ', '', '');

    await newPostPage.expectError('すべての項目を入力してください');
  });

  test('記事を削除できる', async ({ page }) => {
    await listPage.expectPostCount(2);
    await listPage.clickDelete(0);
    await listPage.expectPostCount(1);
    await listPage.expectSuccess('記事を削除しました');
  });
});
```

</details>

<details>
<summary>解答例（改良版 ─ カスタムFixtureの導入）</summary>

### カスタムFixture

```typescript
// fixtures.ts
import { test as base } from '@playwright/test';
import path from 'path';
import { PostListPage } from './pages/post-list-page';
import { PostDetailPage } from './pages/post-detail-page';
import { NewPostPage } from './pages/new-post-page';

const TEST_PAGE = path.resolve(__dirname, 'blog-app.html');

type BlogFixtures = {
  listPage: PostListPage;
  detailPage: PostDetailPage;
  newPostPage: NewPostPage;
};

export const test = base.extend<BlogFixtures>({
  listPage: async ({ page }, use) => {
    const listPage = new PostListPage(page);
    await listPage.goto(TEST_PAGE);
    await use(listPage);
  },

  detailPage: async ({ page }, use) => {
    await use(new PostDetailPage(page));
  },

  newPostPage: async ({ page }, use) => {
    await use(new NewPostPage(page));
  },
});

export { expect } from '@playwright/test';
```

### Fixtureを使ったテスト

```typescript
// tests/blog-with-fixture.spec.ts
// 改良版：カスタムFixtureで更に簡潔に
// 実行方法：npx playwright test tests/blog-with-fixture.spec.ts --project=chromium

import { test, expect } from '../fixtures';

test.describe('ブログアプリ（Fixture版）', () => {

  test('記事一覧が表示される', async ({ listPage }) => {
    await listPage.expectPostCount(2);
    await listPage.expectPostTitle(0, 'Playwrightの始め方');
    await listPage.expectPostTitle(1, 'TypeScriptの基礎');
  });

  test('記事の詳細を表示して一覧に戻れる', async ({ listPage, detailPage }) => {
    await listPage.clickDetail(0);

    await detailPage.expectTitle('Playwrightの始め方');
    await detailPage.expectAuthor('田中太郎');

    await detailPage.goBackToList();
    await listPage.expectPostCount(2);
  });

  test('新しい記事を作成できる', async ({ listPage, newPostPage }) => {
    await listPage.navigateToNewPost();
    await newPostPage.createPost('テスト記事', 'テスト著者', 'テスト本文です。');

    await listPage.expectSuccess('記事を公開しました');
    await listPage.expectPostCount(3);
  });

  test('入力不備でエラーになる', async ({ listPage, newPostPage }) => {
    await listPage.navigateToNewPost();
    await newPostPage.createPost('タイトルだけ', '', '');
    await newPostPage.expectError('すべての項目を入力してください');
  });

  test('記事を削除できる', async ({ listPage }) => {
    await listPage.clickDelete(0);
    await listPage.expectPostCount(1);
    await listPage.expectSuccess('記事を削除しました');
  });
});
```

**初心者向けとの違い:**
- カスタムFixtureにより、各テストの引数でPOMインスタンスを直接受け取れる
- `beforeEach` でのセットアップが不要（Fixtureが自動でページ遷移まで行う）
- テスト本体がさらに短く、意図が明確
- POMインスタンスの生成がFixtureに一元化されているため、パスの変更なども1箇所で済む

**リファクタリングの効果まとめ:**

| 項目 | リファクタリング前 | POM版 | Fixture版 |
|---|---|---|---|
| ロケーターの管理場所 | テスト内に散在 | POMクラスに集約 | POMクラスに集約 |
| 操作の重複 | 各テストにコピペ | メソッドで再利用 | メソッドで再利用 |
| UI変更時の修正箇所 | 全テスト | POMクラスのみ | POMクラスのみ |
| テストの読みやすさ | ロケーターが混在 | POMメソッド名で意図が明確 | さらに簡潔 |
| セットアップの管理 | beforeEach | beforeEach | Fixtureに内包 |

</details>

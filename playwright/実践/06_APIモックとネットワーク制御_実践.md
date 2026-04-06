# 実践課題06：APIモックとネットワーク制御 ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第4章（アサーション）、第5章（フォーム操作）、第6章（待機処理とネットワーク制御）
> **課題の種類**: ミニプロジェクト
> **学習目標**: APIリクエストのモック（差し替え）、レスポンスのインターセプト、ネットワークの待機処理を使いこなし、外部APIに依存しない安定したテストを書ける

---

## 完成イメージ

ユーザー一覧を表示するWebアプリに対して、APIレスポンスをモックしたテストを書きます。

```
Running 5 tests using 3 workers

  ✓ APIモック › ユーザー一覧がモックデータで表示される (0.9s)
  ✓ APIモック › APIエラー時にエラーメッセージが表示される (0.8s)
  ✓ APIモック › 空のデータで「ユーザーがいません」が表示される (0.7s)
  ✓ ネットワーク待機 › データ読み込み中にローディングが表示される (1.0s)
  ✓ リクエスト検証 › 検索時に正しいクエリパラメータが送信される (1.1s)

  5 passed (3.2s)
```

---

## テスト対象のHTMLファイル

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>ユーザー管理</title>
  <style>
    body { font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; }
    .loading { color: #666; font-style: italic; }
    .error { color: red; padding: 12px; background: #ffeaea; border-radius: 4px; }
    .user-card { border: 1px solid #ddd; padding: 12px; margin: 8px 0; border-radius: 8px; }
    .user-card h3 { margin: 0 0 4px 0; }
    .user-card p { margin: 0; color: #666; }
    .search-box { margin: 16px 0; }
    .search-box input { padding: 8px; width: 250px; }
    .search-box button { padding: 8px 16px; }
    .empty { color: #999; text-align: center; padding: 24px; }
  </style>
</head>
<body>
  <h1>ユーザー管理</h1>

  <div class="search-box">
    <input id="search" type="text" placeholder="名前で検索">
    <button onclick="searchUsers()">検索</button>
  </div>

  <div id="content">
    <p class="loading" id="loading">読み込み中...</p>
  </div>

  <script>
    const API_BASE = '/api/users';

    async function loadUsers() {
      const content = document.getElementById('content');
      const loading = document.getElementById('loading');
      loading.style.display = 'block';

      try {
        const res = await fetch(API_BASE);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const users = await res.json();
        loading.style.display = 'none';

        if (users.length === 0) {
          content.innerHTML = '<p class="empty">ユーザーがいません</p>';
          return;
        }

        content.innerHTML = users.map(u => `
          <div class="user-card" data-testid="user-card">
            <h3>${u.name}</h3>
            <p>${u.email}</p>
          </div>
        `).join('');
      } catch (e) {
        loading.style.display = 'none';
        content.innerHTML = `<p class="error">データの読み込みに失敗しました: ${e.message}</p>`;
      }
    }

    async function searchUsers() {
      const query = document.getElementById('search').value;
      const content = document.getElementById('content');

      try {
        const res = await fetch(`${API_BASE}?q=${encodeURIComponent(query)}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const users = await res.json();

        if (users.length === 0) {
          content.innerHTML = `<p class="empty">「${query}」に一致するユーザーがいません</p>`;
          return;
        }

        content.innerHTML = users.map(u => `
          <div class="user-card" data-testid="user-card">
            <h3>${u.name}</h3>
            <p>${u.email}</p>
          </div>
        `).join('');
      } catch (e) {
        content.innerHTML = `<p class="error">検索に失敗しました: ${e.message}</p>`;
      }
    }

    // ページ読み込み時にAPIを呼ぶ
    loadUsers();
  </script>
</body>
</html>
```

---

## 課題の要件

1. `page.route()` で `/api/users` へのリクエストをモックし、ユーザー一覧が表示されることを検証する
2. APIが500エラーを返した場合に、エラーメッセージが表示されることを検証する
3. APIが空配列を返した場合に、「ユーザーがいません」が表示されることを検証する
4. `page.waitForResponse()` を使って、API呼び出しの完了を待ってから検証する
5. 検索時に正しいクエリパラメータ（`?q=...`）が送信されることを検証する

---

## ステップガイド

<details>
<summary>ステップ1：page.route()でモックする</summary>

```typescript
// APIレスポンスをモックする
await page.route('**/api/users', async (route) => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([
      { name: '田中太郎', email: 'tanaka@example.com' },
      { name: '佐藤花子', email: 'sato@example.com' },
    ]),
  });
});
```

</details>

<details>
<summary>ステップ2：エラーレスポンスをモックする</summary>

```typescript
await page.route('**/api/users', async (route) => {
  await route.fulfill({
    status: 500,
    contentType: 'application/json',
    body: JSON.stringify({ error: 'Internal Server Error' }),
  });
});
```

</details>

<details>
<summary>ステップ3：リクエストのURLを検証する</summary>

```typescript
// リクエストの監視を開始
const requestPromise = page.waitForRequest('**/api/users**');

// 検索を実行
await page.getByPlaceholder('名前で検索').fill('田中');
await page.getByRole('button', { name: '検索' }).click();

// リクエストURLを検証
const request = await requestPromise;
expect(request.url()).toContain('q=%E7%94%B0%E4%B8%AD'); // "田中" のURLエンコード
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```typescript
// tests/api-mock.spec.ts
// 学べる内容：APIモック、ネットワーク待機、リクエスト検証
// 実行方法：npx playwright test tests/api-mock.spec.ts --project=chromium

import { test, expect } from '@playwright/test';
import path from 'path';

const TEST_PAGE = path.resolve(__dirname, '../user-management.html');

// テスト用のモックデータ
const mockUsers = [
  { name: '田中太郎', email: 'tanaka@example.com' },
  { name: '佐藤花子', email: 'sato@example.com' },
  { name: '鈴木一郎', email: 'suzuki@example.com' },
];

test.describe('APIモック', () => {

  test('ユーザー一覧がモックデータで表示される', async ({ page }) => {
    // APIをモック（ページ移動の前にセット）
    await page.route('**/api/users', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(mockUsers),
      });
    });

    // ページを開く
    await page.goto(`file://${TEST_PAGE}`);

    // ユーザーカードが3つ表示される
    const cards = page.getByTestId('user-card');
    await expect(cards).toHaveCount(3);

    // 各ユーザーの名前が表示されている
    await expect(cards.nth(0).getByRole('heading')).toHaveText('田中太郎');
    await expect(cards.nth(1).getByRole('heading')).toHaveText('佐藤花子');
    await expect(cards.nth(2).getByRole('heading')).toHaveText('鈴木一郎');
  });

  test('APIエラー時にエラーメッセージが表示される', async ({ page }) => {
    // 500エラーをモック
    await page.route('**/api/users', async (route) => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal Server Error' }),
      });
    });

    await page.goto(`file://${TEST_PAGE}`);

    // エラーメッセージの検証
    const error = page.locator('.error');
    await expect(error).toBeVisible();
    await expect(error).toContainText('データの読み込みに失敗しました');
  });

  test('空のデータで「ユーザーがいません」が表示される', async ({ page }) => {
    // 空配列を返す
    await page.route('**/api/users', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([]),
      });
    });

    await page.goto(`file://${TEST_PAGE}`);

    // 空メッセージの検証
    await expect(page.locator('.empty')).toBeVisible();
    await expect(page.locator('.empty')).toHaveText('ユーザーがいません');
  });
});

test.describe('ネットワーク待機', () => {

  test('データ読み込み中にローディングが表示される', async ({ page }) => {
    // レスポンスを遅延させる
    await page.route('**/api/users', async (route) => {
      // 1秒遅延
      await new Promise(resolve => setTimeout(resolve, 1000));
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(mockUsers),
      });
    });

    await page.goto(`file://${TEST_PAGE}`);

    // ローディング表示を確認
    await expect(page.locator('#loading')).toBeVisible();

    // データ読み込み完了後、ローディングが消える
    await expect(page.locator('#loading')).toBeHidden();

    // ユーザーが表示される
    await expect(page.getByTestId('user-card')).toHaveCount(3);
  });
});

test.describe('リクエスト検証', () => {

  test('検索時に正しいクエリパラメータが送信される', async ({ page }) => {
    // 初期ロードのモック
    await page.route('**/api/users', async (route) => {
      const url = new URL(route.request().url(), 'http://localhost');
      const query = url.searchParams.get('q');

      if (query) {
        // 検索結果のモック
        const filtered = mockUsers.filter(u => u.name.includes(query));
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify(filtered),
        });
      } else {
        // 初期ロード
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify(mockUsers),
        });
      }
    });

    await page.goto(`file://${TEST_PAGE}`);

    // 検索を実行
    await page.getByPlaceholder('名前で検索').fill('田中');

    // リクエストの監視を開始
    const requestPromise = page.waitForRequest(req =>
      req.url().includes('/api/users') && req.url().includes('q=')
    );

    await page.getByRole('button', { name: '検索' }).click();

    // リクエストを検証
    const request = await requestPromise;
    expect(request.url()).toContain('q=');

    // 検索結果の検証
    await expect(page.getByTestId('user-card')).toHaveCount(1);
    await expect(page.getByTestId('user-card').getByRole('heading')).toHaveText('田中太郎');
  });
});
```

</details>

<details>
<summary>解答例（改良版 ─ モックのヘルパー関数化）</summary>

```typescript
// tests/api-mock-advanced.spec.ts
// 改良版：モックをヘルパー関数に切り出して再利用性を向上
// 実行方法：npx playwright test tests/api-mock-advanced.spec.ts --project=chromium

import { test, expect, Page } from '@playwright/test';
import path from 'path';

const TEST_PAGE = path.resolve(__dirname, '../user-management.html');

// --- モック用ヘルパー ---

interface User {
  name: string;
  email: string;
}

/** ユーザーAPIの成功レスポンスをモックする */
async function mockUsersApi(page: Page, users: User[]) {
  await page.route('**/api/users', async (route) => {
    const url = new URL(route.request().url(), 'http://localhost');
    const query = url.searchParams.get('q');

    const filtered = query
      ? users.filter(u => u.name.includes(query) || u.email.includes(query))
      : users;

    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(filtered),
    });
  });
}

/** ユーザーAPIのエラーレスポンスをモックする */
async function mockUsersApiError(page: Page, status: number) {
  await page.route('**/api/users', async (route) => {
    await route.fulfill({
      status,
      contentType: 'application/json',
      body: JSON.stringify({ error: `HTTP ${status} Error` }),
    });
  });
}

/** ユーザーAPIの遅延レスポンスをモックする */
async function mockUsersApiDelayed(page: Page, users: User[], delayMs: number) {
  await page.route('**/api/users', async (route) => {
    await new Promise(resolve => setTimeout(resolve, delayMs));
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(users),
    });
  });
}

// --- テストデータ ---
const testUsers: User[] = [
  { name: '田中太郎', email: 'tanaka@example.com' },
  { name: '佐藤花子', email: 'sato@example.com' },
  { name: '鈴木一郎', email: 'suzuki@example.com' },
];

// --- テスト ---

test.describe('正常系', () => {

  test('ユーザー一覧が表示される', async ({ page }) => {
    await mockUsersApi(page, testUsers);
    await page.goto(`file://${TEST_PAGE}`);

    const cards = page.getByTestId('user-card');
    await expect(cards).toHaveCount(3);

    // 全ユーザーの名前を一括検証
    const names = await cards.locator('h3').allTextContents();
    expect(names).toEqual(['田中太郎', '佐藤花子', '鈴木一郎']);
  });

  test('検索でフィルタされた結果が表示される', async ({ page }) => {
    await mockUsersApi(page, testUsers);
    await page.goto(`file://${TEST_PAGE}`);

    // 初期ロード完了を待つ
    await expect(page.getByTestId('user-card')).toHaveCount(3);

    // 検索実行
    await page.getByPlaceholder('名前で検索').fill('佐藤');
    const responsePromise = page.waitForResponse('**/api/users**');
    await page.getByRole('button', { name: '検索' }).click();
    await responsePromise;

    await expect(page.getByTestId('user-card')).toHaveCount(1);
  });
});

test.describe('異常系', () => {

  // パラメータ化テスト：さまざまなHTTPエラー
  const errorCases = [
    { status: 400, description: 'Bad Request' },
    { status: 403, description: 'Forbidden' },
    { status: 500, description: 'Internal Server Error' },
    { status: 503, description: 'Service Unavailable' },
  ];

  for (const tc of errorCases) {
    test(`HTTP ${tc.status}でエラーメッセージが表示される`, async ({ page }) => {
      await mockUsersApiError(page, tc.status);
      await page.goto(`file://${TEST_PAGE}`);

      await expect(page.locator('.error')).toBeVisible();
      await expect(page.locator('.error')).toContainText('失敗しました');
    });
  }
});

test.describe('UX検証', () => {

  test('ローディング→データ表示の遷移が正しい', async ({ page }) => {
    await mockUsersApiDelayed(page, testUsers, 1500);
    await page.goto(`file://${TEST_PAGE}`);

    // ローディング中
    await expect(page.locator('#loading')).toBeVisible();
    await expect(page.getByTestId('user-card')).toHaveCount(0);

    // データ表示後
    await expect(page.getByTestId('user-card')).toHaveCount(3);
    await expect(page.locator('#loading')).toBeHidden();
  });
});
```

**初心者向けとの違い:**
- モックをヘルパー関数に分離し、テストごとのセットアップが簡潔
- `allTextContents()` で全要素のテキストを一括取得して検証
- パラメータ化テストで複数のHTTPステータスコードをテスト
- `waitForResponse` を使ってAPIレスポンスの完了を確実に待機
- モックの中でURLパラメータを解析して検索機能をシミュレート

</details>

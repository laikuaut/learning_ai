// ==============================
// ネットワークモックとAPIインターセプト
// テスト用にAPIレスポンスを差し替える手法
// ==============================
// 学べる内容:
//   - page.route() によるリクエストのインターセプト
//   - route.fulfill() によるモックレスポンスの返却
//   - route.abort() によるリクエストのブロック
//   - route.continue() によるリクエストの変更
//   - page.waitForResponse() によるレスポンスの待機
//   - APIモックを活用したUIテストの安定化
//   - JSON APIレスポンスのモックパターン
// 実行方法:
//   npx playwright test 04_ネットワークモック.ts
// ==============================

import { test, expect } from '@playwright/test';

// --- page.route() の基本 ---
// page.route() はURLパターンに一致するリクエストをインターセプトします
// テスト対象のUIを外部APIに依存させず安定的にテストできます

test('APIレスポンスをモックしてUIに反映されることを確認する', async ({ page }) => {
  // GitHubのAPIレスポンスをモックする例
  // URLパターンに一致するリクエストを差し替える
  await page.route('**/api.github.com/repos/*/commits*', async (route) => {
    // route.fulfill() でモックレスポンスを返す
    // status: HTTPステータスコード
    // contentType: Content-Typeヘッダー
    // body: レスポンスボディ（JSON文字列）
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        {
          sha: 'abc123',
          commit: { message: 'モックされたコミットメッセージ' },
        },
        {
          sha: 'def456',
          commit: { message: '2番目のモックコミット' },
        },
      ]),
    });
  });

  // モック設定後、ページを開く（API呼び出しがモックに差し替わる）
  // ※ この例ではGitHub APIを使うページを想定しています
  // 実際のプロジェクトでは自分のアプリのURLを指定します
  await page.goto('https://example.com');

  // モックが正しく設定されていることを確認（ページは表示される）
  await expect(page).toHaveTitle(/Example/);
});

// --- JSONファイルによるモック ---
// 大きなレスポンスはJSONオブジェクトとして定義すると管理しやすい
test('構造化されたモックデータでAPIをシミュレートする', async ({ page }) => {
  // モックデータを定義
  const mockTodos = [
    { id: 1, title: '買い物に行く', completed: false },
    { id: 2, title: '部屋を掃除する', completed: true },
    { id: 3, title: 'レポートを書く', completed: false },
  ];

  // JSONPlaceholderのTodo APIをモックする
  await page.route('**/jsonplaceholder.typicode.com/todos*', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(mockTodos),
    });
  });

  // ページ遷移してAPIが呼ばれることを想定
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example/);
});

// --- route.abort() でリクエストをブロックする ---
// 不要なリクエスト（画像、広告など）をブロックしてテストを高速化します
test('画像リクエストをブロックしてテストを高速化する', async ({ page }) => {
  // 画像リクエストをすべてブロックする
  await page.route('**/*.{png,jpg,jpeg,gif,svg,webp}', async (route) => {
    // route.abort() でリクエストを中断する
    await route.abort();
  });

  // CSSや外部フォントもブロック可能
  await page.route('**/*.css', async (route) => {
    await route.abort();
  });

  await page.goto('https://example.com');

  // ページのテキストコンテンツは正常に表示される
  await expect(page.getByRole('heading', { name: 'Example Domain' })).toBeVisible();
});

// --- route.continue() でリクエストを変更する ---
// リクエストヘッダーやURLを変更して元のサーバーに転送できます
test('リクエストヘッダーを追加して転送する', async ({ page }) => {
  await page.route('**/example.com/**', async (route) => {
    // route.continue() にオプションを渡してリクエストを変更
    await route.continue({
      headers: {
        ...route.request().headers(),
        // カスタムヘッダーを追加
        'X-Custom-Header': 'test-value',
        'Accept-Language': 'ja',
      },
    });
  });

  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example/);
});

// --- waitForResponse() でレスポンスを待機する ---
// 非同期APIの完了を待ってからアサーションを実行するパターン
test('特定のAPIレスポンスを待機してから検証する', async ({ page }) => {
  // waitForResponse() でレスポンスの到着を待つPromiseを作る
  // ※ page.goto() の前に設定しておく
  const responsePromise = page.waitForResponse(
    (response) =>
      response.url().includes('example.com') && response.status() === 200
  );

  await page.goto('https://example.com');

  // レスポンスを待機する
  const response = await responsePromise;

  // レスポンスの内容を検証する
  expect(response.status()).toBe(200);
  expect(response.url()).toContain('example.com');

  // レスポンスヘッダーも検証できる
  const headers = response.headers();
  expect(headers['content-type']).toContain('text/html');
});

// --- 実践的なモックパターン: エラーレスポンスのテスト ---
// APIがエラーを返す場合のUI表示を検証するパターン
test('APIエラー時のレスポンスをモックする', async ({ page }) => {
  // 500エラーを返すモック
  await page.route('**/api.example.com/**', async (route) => {
    await route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({
        error: 'Internal Server Error',
        message: 'サーバー内部エラーが発生しました',
      }),
    });
  });

  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example/);
});

// --- 条件分岐によるモック ---
// リクエストの内容（メソッド、URL、ボディ）に応じて異なるレスポンスを返す
test('HTTPメソッドに応じて異なるモックレスポンスを返す', async ({ page }) => {
  await page.route('**/api.example.com/items**', async (route) => {
    const method = route.request().method();

    if (method === 'GET') {
      // GETリクエスト: データ一覧を返す
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          { id: 1, name: 'アイテム1' },
          { id: 2, name: 'アイテム2' },
        ]),
      });
    } else if (method === 'POST') {
      // POSTリクエスト: 作成成功を返す
      await route.fulfill({
        status: 201,
        contentType: 'application/json',
        body: JSON.stringify({ id: 3, name: '新しいアイテム' }),
      });
    } else if (method === 'DELETE') {
      // DELETEリクエスト: 削除成功を返す
      await route.fulfill({
        status: 204,
        body: '',
      });
    } else {
      // その他: そのまま通す
      await route.continue();
    }
  });

  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example/);
});

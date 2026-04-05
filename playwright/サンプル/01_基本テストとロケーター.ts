// ==============================
// 基本テストとロケーター
// Playwrightの基本機能を学ぶ入門サンプル
// ==============================
// 学べる内容:
//   - test() によるテストケースの定義
//   - expect() によるアサーション
//   - page.goto() によるページ遷移
//   - getByRole() によるロール指定のロケーター
//   - getByText() によるテキスト指定のロケーター
//   - toBeVisible() で要素の表示確認
//   - toHaveTitle() でページタイトルの検証
//   - toHaveURL() でURLの検証
//   - locator() によるCSSセレクタの使用
// 実行方法:
//   npx playwright test 01_基本テストとロケーター.ts
// ==============================

import { test, expect } from '@playwright/test';

// --- テストケースの基本構造 ---
// test() 関数でテストケースを定義します
// 第1引数: テスト名（わかりやすい日本語でOK）
// 第2引数: テスト本体の非同期関数（page オブジェクトを受け取る）
test('example.com のページタイトルを検証する', async ({ page }) => {
  // page.goto() でURLに遷移する
  // await を忘れるとテストが不安定になるので注意
  await page.goto('https://example.com');

  // toHaveTitle() でページのタイトルを検証する
  // 正規表現も使用可能（部分一致に便利）
  await expect(page).toHaveTitle(/Example Domain/);
});

// --- ロケーターの基本: getByRole ---
// getByRole() はアクセシビリティロールで要素を探す推奨の方法です
// ボタン、リンク、見出しなど、意味的な役割で要素を特定できます
test('見出しが正しく表示されていることを確認する', async ({ page }) => {
  await page.goto('https://example.com');

  // heading ロールで見出し要素を取得
  // name オプションでテキスト内容を指定して絞り込み
  const heading = page.getByRole('heading', { name: 'Example Domain' });

  // toBeVisible() で要素が画面に表示されていることを確認
  await expect(heading).toBeVisible();
});

// --- getByText によるテキスト検索 ---
// getByText() はページ上のテキスト内容で要素を探します
// 完全一致と部分一致の両方に対応しています
test('ページ内の説明テキストが存在することを確認する', async ({ page }) => {
  await page.goto('https://example.com');

  // getByText() でテキストを含む要素を探す
  // 部分一致させたい場合は正規表現を使う
  const description = page.getByText('This domain is for use in illustrative examples');

  // テキストが画面上に見えていることを検証
  await expect(description).toBeVisible();
});

// --- リンクの検証 ---
// リンクは getByRole('link') で取得するのがベストプラクティスです
test('More information リンクが存在し正しいURLを持つことを確認する', async ({ page }) => {
  await page.goto('https://example.com');

  // リンク要素をロールとテキストで特定する
  const link = page.getByRole('link', { name: 'More information...' });

  // リンクが表示されていることを確認
  await expect(link).toBeVisible();

  // toHaveAttribute() で href 属性を検証
  // リンク先URLが正しいかチェックする
  await expect(link).toHaveAttribute('href', 'https://www.iana.org/domains/example');
});

// --- URLの検証 ---
// ページ遷移後のURLを検証する方法を学びます
test('現在のURLを検証する', async ({ page }) => {
  await page.goto('https://example.com');

  // toHaveURL() でURLを検証する
  // 正規表現での部分一致も可能
  await expect(page).toHaveURL('https://example.com/');

  // 正規表現を使ったURL検証の例
  await expect(page).toHaveURL(/example\.com/);
});

// --- CSSセレクタによるロケーター ---
// locator() を使うと従来のCSSセレクタで要素を特定できます
// getByRole() が使えない場合の代替手段として知っておくと便利です
test('CSSセレクタで要素を取得する', async ({ page }) => {
  await page.goto('https://example.com');

  // locator() にCSSセレクタを渡して要素を取得
  const paragraph = page.locator('p');

  // count() で要素数を取得して検証
  // example.com には2つの <p> タグがある
  await expect(paragraph).toHaveCount(2);

  // first を使って最初の要素を取得
  await expect(paragraph.first()).toBeVisible();
});

// --- test.describe でテストをグループ化 ---
// 関連するテストをまとめると、テスト結果が見やすくなります
test.describe('example.com の総合検証', () => {
  // beforeEach で各テスト前に共通処理を実行
  // ページ遷移など、全テストに共通する処理をここに書く
  test.beforeEach(async ({ page }) => {
    await page.goto('https://example.com');
  });

  test('ページタイトルが正しいこと', async ({ page }) => {
    await expect(page).toHaveTitle('Example Domain');
  });

  test('メイン見出しが表示されていること', async ({ page }) => {
    await expect(page.getByRole('heading', { level: 1 })).toHaveText('Example Domain');
  });

  test('ナビゲーションリンクが機能すること', async ({ page }) => {
    // リンクをクリックして遷移を確認
    const link = page.getByRole('link', { name: 'More information...' });
    await link.click();

    // 遷移先のURLを検証（リダイレクトの可能性があるので正規表現で）
    await expect(page).toHaveURL(/iana\.org/);
  });
});

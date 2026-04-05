// ==============================
// TodoMVCアプリ完全テストスイート
// CRUD操作を網羅する実践的なE2Eテスト
// ==============================
// 学べる内容:
//   - test.describe() によるテストのグループ化
//   - test.beforeEach() による共通セットアップ
//   - CRUD（作成・読取・更新・削除）の一連のテスト
//   - フィルター機能のテスト
//   - dblclick() によるダブルクリック操作
//   - nth() による要素のインデックス指定
//   - .not アサーションの反転
//   - 実務的なテスト設計パターン
// 実行方法:
//   npx playwright test 03_TodoMVCアプリテスト.ts
// ==============================

import { test, expect, Page } from '@playwright/test';

const TODO_APP_URL = 'https://demo.playwright.dev/todomvc';

// --- ヘルパー関数 ---
// テストコードでも重複を減らすためにヘルパー関数を作るのがベストプラクティス
// 複数のテストで使い回す操作はヘルパーにまとめる

/**
 * Todoアイテムを追加するヘルパー関数
 * @param page - Playwrightのページオブジェクト
 * @param text - 追加するTodoのテキスト
 */
async function addTodo(page: Page, text: string): Promise<void> {
  const input = page.getByPlaceholder('What needs to be done?');
  await input.fill(text);
  await input.press('Enter');
}

// --- Create（作成）テスト ---
test.describe('Todo作成', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(TODO_APP_URL);
  });

  test('新しいTodoを追加できる', async ({ page }) => {
    await addTodo(page, '新しいタスク');

    const todoItems = page.locator('.todo-list li');
    await expect(todoItems).toHaveCount(1);
    await expect(todoItems.first()).toContainText('新しいタスク');
  });

  test('複数のTodoを順番に追加できる', async ({ page }) => {
    const items = ['最初のタスク', '次のタスク', '最後のタスク'];

    for (const item of items) {
      await addTodo(page, item);
    }

    const todoItems = page.locator('.todo-list li');
    await expect(todoItems).toHaveCount(3);
    await expect(todoItems).toHaveText(items);
  });

  test('空文字のTodoは追加されない', async ({ page }) => {
    const input = page.getByPlaceholder('What needs to be done?');
    await input.fill('');
    await input.press('Enter');

    // Todoリストが表示されないことを確認
    await expect(page.locator('.todo-list li')).toHaveCount(0);
  });
});

// --- Read（読取）・表示テスト ---
test.describe('Todo表示', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(TODO_APP_URL);
    // テストデータを事前に投入する
    await addTodo(page, 'タスクA');
    await addTodo(page, 'タスクB');
    await addTodo(page, 'タスクC');
  });

  test('残りアイテム数が正しく表示される', async ({ page }) => {
    await expect(page.locator('.todo-count')).toContainText('3 items left');
  });

  test('各Todoのテキストが正しく表示される', async ({ page }) => {
    const items = page.locator('.todo-list li');
    // nth() でインデックス指定して個別に検証する
    await expect(items.nth(0)).toContainText('タスクA');
    await expect(items.nth(1)).toContainText('タスクB');
    await expect(items.nth(2)).toContainText('タスクC');
  });
});

// --- Update（更新）テスト ---
test.describe('Todo更新', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(TODO_APP_URL);
    await addTodo(page, '編集前のタスク');
    await addTodo(page, 'そのままのタスク');
  });

  test('Todoを完了状態に切り替えられる', async ({ page }) => {
    const firstItem = page.locator('.todo-list li').nth(0);
    const checkbox = firstItem.getByRole('checkbox');

    // 完了にする
    await checkbox.check();
    await expect(firstItem).toHaveClass(/completed/);
    await expect(page.locator('.todo-count')).toContainText('1 item left');
  });

  test('完了状態を元に戻せる', async ({ page }) => {
    const firstItem = page.locator('.todo-list li').nth(0);
    const checkbox = firstItem.getByRole('checkbox');

    // 完了にしてから元に戻す
    await checkbox.check();
    await checkbox.uncheck();

    // .not で「completedクラスを持たないこと」を検証
    await expect(firstItem).not.toHaveClass(/completed/);
    await expect(page.locator('.todo-count')).toContainText('2 items left');
  });

  test('ダブルクリックでTodoを編集できる', async ({ page }) => {
    const firstItem = page.locator('.todo-list li').nth(0);

    // dblclick() でダブルクリックして編集モードに入る
    await firstItem.locator('label').dblclick();

    // 編集用の入力フィールドが表示される
    const editInput = firstItem.locator('.edit');
    await editInput.fill('編集後のタスク');
    await editInput.press('Enter');

    // 編集内容が反映されることを検証
    await expect(firstItem).toContainText('編集後のタスク');
  });

  test('全Todoを一括で完了にできる', async ({ page }) => {
    // 「toggle-all」チェックボックスで全選択
    await page.locator('.toggle-all').check({ force: true });

    // 全アイテムにcompletedクラスがあることを検証
    const items = page.locator('.todo-list li');
    for (let i = 0; i < 2; i++) {
      await expect(items.nth(i)).toHaveClass(/completed/);
    }

    // 残りアイテム数が0になること
    await expect(page.locator('.todo-count')).toContainText('0 items left');
  });
});

// --- Delete（削除）テスト ---
test.describe('Todo削除', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(TODO_APP_URL);
    await addTodo(page, '削除するタスク');
    await addTodo(page, '残すタスク');
  });

  test('個別のTodoを削除できる', async ({ page }) => {
    const firstItem = page.locator('.todo-list li').nth(0);

    // 削除ボタンはホバー時に表示されるので、hover() してから click()
    await firstItem.hover();
    await firstItem.getByRole('button', { name: '×' }).click();

    const items = page.locator('.todo-list li');
    await expect(items).toHaveCount(1);
    await expect(items.first()).toContainText('残すタスク');
  });

  test('完了済みを一括削除できる', async ({ page }) => {
    // 1つ目を完了にする
    await page.locator('.todo-list li').nth(0).getByRole('checkbox').check();

    // 「Clear completed」で完了済みを削除
    await page.getByRole('button', { name: 'Clear completed' }).click();

    await expect(page.locator('.todo-list li')).toHaveCount(1);
    await expect(page.locator('.todo-list li').first()).toContainText('残すタスク');
  });
});

// --- Filter（フィルター）テスト ---
test.describe('Todoフィルター', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(TODO_APP_URL);
    await addTodo(page, '未完了タスク');
    await addTodo(page, '完了タスク');
    // 2つ目を完了にする
    await page.locator('.todo-list li').nth(1).getByRole('checkbox').check();
  });

  test('「Active」フィルターで未完了のみ表示する', async ({ page }) => {
    await page.getByRole('link', { name: 'Active' }).click();

    const items = page.locator('.todo-list li');
    await expect(items).toHaveCount(1);
    await expect(items.first()).toContainText('未完了タスク');
  });

  test('「Completed」フィルターで完了済みのみ表示する', async ({ page }) => {
    await page.getByRole('link', { name: 'Completed' }).click();

    const items = page.locator('.todo-list li');
    await expect(items).toHaveCount(1);
    await expect(items.first()).toContainText('完了タスク');
  });

  test('「All」フィルターで全件表示に戻す', async ({ page }) => {
    // まずActiveフィルターを適用
    await page.getByRole('link', { name: 'Active' }).click();
    await expect(page.locator('.todo-list li')).toHaveCount(1);

    // Allフィルターで全件に戻す
    await page.getByRole('link', { name: 'All' }).click();
    await expect(page.locator('.todo-list li')).toHaveCount(2);
  });
});

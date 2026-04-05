// ==============================
// フォーム操作とアサーション
// TodoMVCアプリを使ったフォーム操作の基本
// ==============================
// 学べる内容:
//   - fill() によるテキスト入力
//   - click() によるクリック操作
//   - check() / uncheck() によるチェックボックス操作
//   - press() によるキーボード入力（Enter等）
//   - toHaveValue() で入力値の検証
//   - toBeChecked() でチェック状態の検証
//   - toHaveCount() で要素数の検証
//   - toHaveClass() でCSSクラスの検証
//   - toContainText() でテキスト内容の検証
// 実行方法:
//   npx playwright test 02_フォーム操作とアサーション.ts
// ==============================

import { test, expect } from '@playwright/test';

// TodoMVCアプリのURL（Playwrightが公式に提供するデモアプリ）
const TODO_APP_URL = 'https://demo.playwright.dev/todomvc';

// --- fill() と press() による入力操作 ---
// fill() はテキストフィールドに値を入力する基本メソッドです
// press() はキーボードのキーを送信します
test('テキストフィールドにTodoを入力してEnterで追加する', async ({ page }) => {
  await page.goto(TODO_APP_URL);

  // 入力フィールドをプレースホルダーテキストで特定
  const input = page.getByPlaceholder('What needs to be done?');

  // fill() で入力フィールドにテキストを設定
  // 既存の値はクリアされてから入力される
  await input.fill('Playwrightを学ぶ');

  // toHaveValue() で入力フィールドの現在値を検証
  await expect(input).toHaveValue('Playwrightを学ぶ');

  // press('Enter') でEnterキーを押してTodoを追加
  await input.press('Enter');

  // Todoが追加されたことを確認
  // .todo-list li で一覧のアイテムを取得
  const todoItems = page.locator('.todo-list li');
  await expect(todoItems).toHaveCount(1);
  await expect(todoItems.first()).toContainText('Playwrightを学ぶ');

  // 入力後、フィールドがクリアされていることを検証
  await expect(input).toHaveValue('');
});

// --- 複数アイテムの追加と検証 ---
// 繰り返し操作のパターンを学びます
test('複数のTodoを追加して一覧を検証する', async ({ page }) => {
  await page.goto(TODO_APP_URL);

  const input = page.getByPlaceholder('What needs to be done?');

  // 複数のTodoを追加する
  const todos = ['朝のジョギング', '本を読む', 'レポートを書く'];

  for (const todo of todos) {
    await input.fill(todo);
    await input.press('Enter');
  }

  // toHaveCount() で追加された数を検証
  const todoItems = page.locator('.todo-list li');
  await expect(todoItems).toHaveCount(3);

  // 各Todoのテキスト内容を検証
  // toHaveText() は配列を渡すと全要素を順番に検証できる
  await expect(todoItems).toHaveText(todos);
});

// --- check() / click() によるチェックボックス操作 ---
// Todoの完了状態を切り替える操作を学びます
test('Todoの完了チェックボックスを操作する', async ({ page }) => {
  await page.goto(TODO_APP_URL);

  // まずTodoを追加する
  const input = page.getByPlaceholder('What needs to be done?');
  await input.fill('テストを書く');
  await input.press('Enter');

  // チェックボックスをクリックしてTodoを完了にする
  // getByRole('checkbox') でチェックボックスを取得
  const checkbox = page.locator('.todo-list li').getByRole('checkbox');
  await checkbox.check();

  // toBeChecked() でチェック状態を検証
  await expect(checkbox).toBeChecked();

  // 完了したTodoに 'completed' クラスが付与されることを検証
  // toHaveClass() でCSSクラスを確認
  await expect(page.locator('.todo-list li')).toHaveClass(/completed/);

  // チェックを外して未完了に戻す
  await checkbox.uncheck();
  await expect(checkbox).not.toBeChecked();
});

// --- click() によるボタン操作 ---
// 完了済みTodoの削除操作を学びます
test('完了済みTodoを一括削除する', async ({ page }) => {
  await page.goto(TODO_APP_URL);

  const input = page.getByPlaceholder('What needs to be done?');

  // 3つのTodoを追加
  await input.fill('タスクA');
  await input.press('Enter');
  await input.fill('タスクB');
  await input.press('Enter');
  await input.fill('タスクC');
  await input.press('Enter');

  // 最初のTodoを完了にする
  const firstCheckbox = page.locator('.todo-list li').nth(0).getByRole('checkbox');
  await firstCheckbox.check();

  // 「Clear completed」ボタンをクリック
  // click() はクリック操作の基本メソッド
  await page.getByRole('button', { name: 'Clear completed' }).click();

  // 完了したTodoが削除され、2つだけ残ることを検証
  const todoItems = page.locator('.todo-list li');
  await expect(todoItems).toHaveCount(2);

  // 残ったTodoの内容を検証
  await expect(todoItems).toHaveText(['タスクB', 'タスクC']);
});

// --- 複合的なフォーム操作 ---
// 残りアイテム数の表示を検証するテスト
test('Todo追加・完了に応じて残りアイテム数が更新される', async ({ page }) => {
  await page.goto(TODO_APP_URL);

  const input = page.getByPlaceholder('What needs to be done?');

  // Todoを3つ追加
  for (const text of ['買い物', '掃除', '料理']) {
    await input.fill(text);
    await input.press('Enter');
  }

  // 残りアイテム数の表示を検証
  // toContainText() はテキストの部分一致で検証する
  const todoCount = page.locator('.todo-count');
  await expect(todoCount).toContainText('3 items left');

  // 1つ完了にすると残りが2になる
  await page.locator('.todo-list li').nth(0).getByRole('checkbox').check();
  await expect(todoCount).toContainText('2 items left');

  // さらに1つ完了にすると残りが1になる
  await page.locator('.todo-list li').nth(1).getByRole('checkbox').check();
  await expect(todoCount).toContainText('1 item left');
});

// ==============================
// Page Object Model（POM）パターン
// テストの保守性を高める設計パターン
// ==============================
// 学べる内容:
//   - Page Object Model（POM）の考え方
//   - POMクラスの設計と実装
//   - コンストラクタでのロケーター初期化
//   - メソッドによる操作のカプセル化
//   - POMクラスをテストで使う方法
//   - テストコードの可読性と保守性の向上
//   - 複数のテストでPOMを再利用するパターン
// 実行方法:
//   npx playwright test 05_PageObjectModel.ts
// ==============================

import { test, expect, Page, Locator } from '@playwright/test';

// =============================================
// Page Object クラスの定義
// =============================================

/**
 * TodoPage クラス - TodoMVCアプリのページオブジェクト
 *
 * POMの基本原則:
 *   1. ページの要素（ロケーター）をクラスのプロパティとして定義
 *   2. ページ上の操作をメソッドとしてカプセル化
 *   3. テストコードはPOMのメソッドだけを呼び出す
 *   4. UIの変更があってもPOMクラスだけ修正すればOK
 */
class TodoPage {
  // --- ページオブジェクトとロケーターの定義 ---
  // readonly で外部から変更されないようにする
  readonly page: Page;
  readonly inputField: Locator;
  readonly todoItems: Locator;
  readonly todoCount: Locator;
  readonly clearCompletedButton: Locator;
  readonly toggleAllCheckbox: Locator;
  readonly filterAll: Locator;
  readonly filterActive: Locator;
  readonly filterCompleted: Locator;

  /**
   * コンストラクタでロケーターを初期化する
   * ロケーターの定義を一箇所に集約することで、
   * セレクタの変更時に修正箇所が1つで済む
   */
  constructor(page: Page) {
    this.page = page;
    this.inputField = page.getByPlaceholder('What needs to be done?');
    this.todoItems = page.locator('.todo-list li');
    this.todoCount = page.locator('.todo-count');
    this.clearCompletedButton = page.getByRole('button', { name: 'Clear completed' });
    this.toggleAllCheckbox = page.locator('.toggle-all');
    this.filterAll = page.getByRole('link', { name: 'All' });
    this.filterActive = page.getByRole('link', { name: 'Active' });
    this.filterCompleted = page.getByRole('link', { name: 'Completed' });
  }

  // --- ページ操作メソッド ---
  // 各操作をわかりやすいメソッド名でカプセル化する

  /** TodoMVCアプリを開く */
  async goto(): Promise<void> {
    await this.page.goto('https://demo.playwright.dev/todomvc');
  }

  /** 新しいTodoを追加する */
  async addTodo(text: string): Promise<void> {
    await this.inputField.fill(text);
    await this.inputField.press('Enter');
  }

  /** 複数のTodoをまとめて追加する */
  async addTodos(texts: string[]): Promise<void> {
    for (const text of texts) {
      await this.addTodo(text);
    }
  }

  /** 指定インデックスのTodoを完了にする（0始まり） */
  async completeTodo(index: number): Promise<void> {
    await this.todoItems.nth(index).getByRole('checkbox').check();
  }

  /** 指定インデックスのTodoを未完了に戻す（0始まり） */
  async uncompleteTodo(index: number): Promise<void> {
    await this.todoItems.nth(index).getByRole('checkbox').uncheck();
  }

  /** 指定インデックスのTodoを削除する */
  async deleteTodo(index: number): Promise<void> {
    const item = this.todoItems.nth(index);
    await item.hover();
    await item.getByRole('button', { name: '×' }).click();
  }

  /** 指定インデックスのTodoを編集する */
  async editTodo(index: number, newText: string): Promise<void> {
    const item = this.todoItems.nth(index);
    await item.locator('label').dblclick();
    const editInput = item.locator('.edit');
    await editInput.fill(newText);
    await editInput.press('Enter');
  }

  /** 完了済みTodoを一括削除する */
  async clearCompleted(): Promise<void> {
    await this.clearCompletedButton.click();
  }

  /** 全Todoを一括で完了にする */
  async toggleAll(): Promise<void> {
    await this.toggleAllCheckbox.check({ force: true });
  }

  // --- アサーション用メソッド ---
  // 検証もPOMにまとめることで、テストコードがより簡潔になる

  /** Todoの件数を検証する */
  async expectTodoCount(count: number): Promise<void> {
    await expect(this.todoItems).toHaveCount(count);
  }

  /** 残りアイテム数の表示を検証する */
  async expectRemainingCount(text: string): Promise<void> {
    await expect(this.todoCount).toContainText(text);
  }

  /** 指定インデックスのTodoのテキストを検証する */
  async expectTodoText(index: number, text: string): Promise<void> {
    await expect(this.todoItems.nth(index)).toContainText(text);
  }

  /** 指定インデックスのTodoが完了状態かを検証する */
  async expectTodoCompleted(index: number): Promise<void> {
    await expect(this.todoItems.nth(index)).toHaveClass(/completed/);
  }

  /** 指定インデックスのTodoが未完了状態かを検証する */
  async expectTodoNotCompleted(index: number): Promise<void> {
    await expect(this.todoItems.nth(index)).not.toHaveClass(/completed/);
  }
}

// =============================================
// POMクラスを使ったテスト
// =============================================
// テストコードがシンプルで読みやすくなっていることに注目

test.describe('TodoMVC - Page Object Modelパターン', () => {
  let todoPage: TodoPage;

  // beforeEach でPOMインスタンスを作成し、ページを開く
  test.beforeEach(async ({ page }) => {
    todoPage = new TodoPage(page);
    await todoPage.goto();
  });

  test('Todoの追加と表示確認', async () => {
    // POMのメソッドを使って操作する
    // 内部のセレクタや操作手順を知らなくてもテストが書ける
    await todoPage.addTodo('Playwrightを学ぶ');
    await todoPage.addTodo('POMパターンを理解する');

    await todoPage.expectTodoCount(2);
    await todoPage.expectTodoText(0, 'Playwrightを学ぶ');
    await todoPage.expectTodoText(1, 'POMパターンを理解する');
    await todoPage.expectRemainingCount('2 items left');
  });

  test('Todoの完了と未完了の切り替え', async () => {
    await todoPage.addTodos(['タスクA', 'タスクB', 'タスクC']);

    // 完了にする
    await todoPage.completeTodo(1);
    await todoPage.expectTodoCompleted(1);
    await todoPage.expectRemainingCount('2 items left');

    // 未完了に戻す
    await todoPage.uncompleteTodo(1);
    await todoPage.expectTodoNotCompleted(1);
    await todoPage.expectRemainingCount('3 items left');
  });

  test('Todoの編集', async () => {
    await todoPage.addTodo('編集前のテキスト');

    await todoPage.editTodo(0, '編集後のテキスト');
    await todoPage.expectTodoText(0, '編集後のテキスト');
  });

  test('完了済みTodoの一括削除', async () => {
    await todoPage.addTodos(['残すタスク', '削除するタスク', '残すタスク2']);

    // 2番目のTodoだけ完了にして一括削除
    await todoPage.completeTodo(1);
    await todoPage.clearCompleted();

    await todoPage.expectTodoCount(2);
    await todoPage.expectTodoText(0, '残すタスク');
    await todoPage.expectTodoText(1, '残すタスク2');
  });

  test('フィルター機能の検証', async () => {
    await todoPage.addTodos(['未完了タスク', '完了タスク']);
    await todoPage.completeTodo(1);

    // Activeフィルター
    await todoPage.filterActive.click();
    await todoPage.expectTodoCount(1);
    await todoPage.expectTodoText(0, '未完了タスク');

    // Completedフィルター
    await todoPage.filterCompleted.click();
    await todoPage.expectTodoCount(1);
    await todoPage.expectTodoText(0, '完了タスク');

    // Allフィルター
    await todoPage.filterAll.click();
    await todoPage.expectTodoCount(2);
  });
});

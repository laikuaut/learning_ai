# 実践課題11：ToDoアプリ E2Eテスト完全版 ★5

> **難易度**: ★★★★★（総合）
> **前提知識**: 第1章〜第8章（全章）
> **課題の種類**: ミニプロジェクト
> **学習目標**: 実務レベルのToDoアプリに対して、POM・Fixture・APIモック・パラメータ化テスト・テスト戦略を統合した本格的なE2Eテストスイートを構築する

---

## 完成イメージ

以下のような構成のテストプロジェクトを作成します。

```
todo-e2e-tests/
├── pages/
│   └── todo-page.ts           # Page Objectクラス
├── fixtures/
│   └── todo-fixtures.ts       # カスタムFixture
├── test-data/
│   └── todos.ts               # テストデータ
├── tests/
│   ├── todo-crud.spec.ts      # CRUD操作テスト
│   ├── todo-filter.spec.ts    # フィルター・ソートテスト
│   ├── todo-persistence.spec.ts  # データ永続化テスト
│   └── todo-edge-cases.spec.ts   # エッジケーステスト
└── playwright.config.ts
```

```
Running 20 tests using 4 workers

  ✓ CRUD › タスクを追加できる (0.8s)
  ✓ CRUD › タスクを編集できる (1.0s)
  ✓ CRUD › タスクを削除できる (0.9s)
  ✓ CRUD › タスクを完了にできる (0.8s)
  ... （20テストすべてパス）

  20 passed (8.5s)
```

---

## テスト対象のHTMLファイル

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>ToDo アプリ</title>
  <style>
    * { box-sizing: border-box; }
    body { font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; background: #fafafa; }
    h1 { text-align: center; color: #333; }
    .input-area { display: flex; gap: 8px; margin-bottom: 20px; }
    .input-area input { flex: 1; padding: 10px; border: 2px solid #ddd; border-radius: 4px; font-size: 1em; }
    .input-area button { padding: 10px 20px; background: #0066cc; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 1em; }
    .filters { display: flex; gap: 8px; margin-bottom: 16px; }
    .filters button { padding: 6px 16px; border: 1px solid #ddd; border-radius: 20px; background: white; cursor: pointer; }
    .filters button.active { background: #0066cc; color: white; border-color: #0066cc; }
    .todo-item { display: flex; align-items: center; padding: 12px; background: white; border: 1px solid #eee; border-radius: 4px; margin-bottom: 8px; }
    .todo-item.done .todo-text { text-decoration: line-through; color: #999; }
    .todo-item input[type="checkbox"] { margin-right: 12px; width: 18px; height: 18px; }
    .todo-text { flex: 1; font-size: 1em; }
    .todo-text.editing { display: none; }
    .edit-input { flex: 1; padding: 4px 8px; font-size: 1em; border: 1px solid #0066cc; border-radius: 4px; display: none; }
    .edit-input.editing { display: block; }
    .todo-actions button { margin-left: 8px; padding: 4px 8px; border: none; cursor: pointer; border-radius: 4px; }
    .btn-edit { background: #f0f0f0; }
    .btn-delete { background: #ffeaea; color: #cc3333; }
    .btn-save { background: #e8f5e9; color: #2e7d32; display: none; }
    .btn-save.editing { display: inline; }
    .btn-edit.editing { display: none; }
    .stats { text-align: center; color: #666; margin-top: 16px; }
    .clear-completed { background: none; border: none; color: #cc3333; cursor: pointer; text-decoration: underline; margin-top: 8px; }
    .empty-state { text-align: center; color: #999; padding: 40px; }
    .error-msg { color: red; font-size: 0.9em; margin: 4px 0; display: none; }
  </style>
</head>
<body>
  <h1>ToDo アプリ</h1>

  <div class="input-area">
    <input id="todo-input" type="text" placeholder="新しいタスクを入力" aria-label="新しいタスク">
    <button id="add-btn" onclick="addTodo()">追加</button>
  </div>
  <p class="error-msg" id="error-msg"></p>

  <div class="filters" role="group" aria-label="フィルター">
    <button class="active" onclick="setFilter('all')" data-filter="all">すべて</button>
    <button onclick="setFilter('active')" data-filter="active">未完了</button>
    <button onclick="setFilter('done')" data-filter="done">完了済み</button>
  </div>

  <div id="todo-list"></div>
  <p class="empty-state" id="empty-state" style="display:none;">タスクがありません</p>

  <div class="stats" id="stats"></div>
  <div style="text-align:center;">
    <button class="clear-completed" id="clear-completed" onclick="clearCompleted()" style="display:none;">完了済みを一括削除</button>
  </div>

  <script>
    let todos = [];
    let nextId = 1;
    let currentFilter = 'all';

    // LocalStorage からの復元
    function loadFromStorage() {
      try {
        const saved = localStorage.getItem('todos');
        if (saved) {
          todos = JSON.parse(saved);
          nextId = todos.length > 0 ? Math.max(...todos.map(t => t.id)) + 1 : 1;
        }
      } catch (e) { /* ignore */ }
    }

    function saveToStorage() {
      localStorage.setItem('todos', JSON.stringify(todos));
    }

    function addTodo() {
      const input = document.getElementById('todo-input');
      const text = input.value.trim();
      const errorEl = document.getElementById('error-msg');

      if (!text) {
        errorEl.textContent = 'タスクを入力してください';
        errorEl.style.display = 'block';
        return;
      }

      if (text.length > 100) {
        errorEl.textContent = 'タスクは100文字以内で入力してください';
        errorEl.style.display = 'block';
        return;
      }

      if (todos.some(t => t.text === text)) {
        errorEl.textContent = '同じタスクが既に存在します';
        errorEl.style.display = 'block';
        return;
      }

      errorEl.style.display = 'none';
      todos.push({ id: nextId++, text, done: false, createdAt: new Date().toISOString() });
      input.value = '';
      saveToStorage();
      render();
    }

    function toggleTodo(id) {
      const todo = todos.find(t => t.id === id);
      if (todo) todo.done = !todo.done;
      saveToStorage();
      render();
    }

    function deleteTodo(id) {
      todos = todos.filter(t => t.id !== id);
      saveToStorage();
      render();
    }

    function startEdit(id) {
      const item = document.querySelector(`[data-todo-id="${id}"]`);
      item.querySelector('.todo-text').classList.add('editing');
      item.querySelector('.edit-input').classList.add('editing');
      item.querySelector('.btn-edit').classList.add('editing');
      item.querySelector('.btn-save').classList.add('editing');
      const input = item.querySelector('.edit-input');
      input.value = todos.find(t => t.id === id).text;
      input.focus();
    }

    function saveEdit(id) {
      const item = document.querySelector(`[data-todo-id="${id}"]`);
      const newText = item.querySelector('.edit-input').value.trim();
      if (newText) {
        const todo = todos.find(t => t.id === id);
        if (todo) todo.text = newText;
        saveToStorage();
      }
      render();
    }

    function setFilter(filter) {
      currentFilter = filter;
      document.querySelectorAll('.filters button').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.filter === filter);
      });
      render();
    }

    function clearCompleted() {
      todos = todos.filter(t => !t.done);
      saveToStorage();
      render();
    }

    function render() {
      let filtered = todos;
      if (currentFilter === 'active') filtered = todos.filter(t => !t.done);
      if (currentFilter === 'done') filtered = todos.filter(t => t.done);

      const list = document.getElementById('todo-list');
      const emptyState = document.getElementById('empty-state');

      if (filtered.length === 0) {
        list.innerHTML = '';
        emptyState.style.display = 'block';
      } else {
        emptyState.style.display = 'none';
        list.innerHTML = filtered.map(t => `
          <div class="todo-item ${t.done ? 'done' : ''}" data-testid="todo-item" data-todo-id="${t.id}">
            <input type="checkbox" ${t.done ? 'checked' : ''} onchange="toggleTodo(${t.id})" aria-label="完了にする">
            <span class="todo-text">${t.text}</span>
            <input class="edit-input" type="text" aria-label="タスクを編集">
            <div class="todo-actions">
              <button class="btn-edit" onclick="startEdit(${t.id})">編集</button>
              <button class="btn-save" onclick="saveEdit(${t.id})">保存</button>
              <button class="btn-delete" onclick="deleteTodo(${t.id})">削除</button>
            </div>
          </div>
        `).join('');
      }

      // 統計
      const total = todos.length;
      const doneCount = todos.filter(t => t.done).length;
      const activeCount = total - doneCount;
      document.getElementById('stats').textContent = `全${total}件（未完了: ${activeCount}件 / 完了: ${doneCount}件）`;

      // 完了済み一括削除ボタン
      document.getElementById('clear-completed').style.display = doneCount > 0 ? 'inline' : 'none';
    }

    loadFromStorage();
    render();
  </script>
</body>
</html>
```

---

## 課題の要件

以下のファイルをすべて作成してください。

### 1. Page Objectクラス（`pages/todo-page.ts`）
- タスクの追加、編集、削除、完了の操作メソッド
- フィルター切り替え、一括削除の操作メソッド
- 各種検証メソッド（件数、テキスト、統計表示など）

### 2. カスタムFixture（`fixtures/todo-fixtures.ts`）
- TodoPage を自動でセットアップ
- LocalStorage をクリアしてから開始（テストの独立性を担保）

### 3. テストデータ（`test-data/todos.ts`）
- テストで使う定型タスクデータ

### 4. テストファイル（4ファイル）
- **CRUD操作**: 追加・編集・削除・完了のトグル
- **フィルター**: すべて / 未完了 / 完了済み、完了済み一括削除
- **データ永続化**: LocalStorage への保存・復元
- **エッジケース**: 空文字、100文字超、重複タスク、空リスト状態

---

## ステップガイド

<details>
<summary>ステップ1：Page Objectから作る</summary>

まずロケーターを洗い出し、操作メソッドと検証メソッドを分けて定義します。

```typescript
export class TodoPage {
  readonly todoInput: Locator;
  readonly addButton: Locator;
  readonly todoItems: Locator;
  // ...

  async addTodo(text: string) { /* ... */ }
  async toggleTodo(index: number) { /* ... */ }
  async deleteTodo(index: number) { /* ... */ }
  // ...
}
```

</details>

<details>
<summary>ステップ2：Fixtureを定義する</summary>

```typescript
export const test = base.extend<{ todoPage: TodoPage }>({
  todoPage: async ({ page }, use) => {
    // LocalStorageをクリア
    await page.goto(`file://${TEST_PAGE}`);
    await page.evaluate(() => localStorage.clear());
    await page.reload();
    const todoPage = new TodoPage(page);
    await use(todoPage);
  },
});
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

### Page Object

```typescript
// pages/todo-page.ts
import { type Locator, type Page, expect } from '@playwright/test';

export class TodoPage {
  readonly page: Page;
  readonly todoInput: Locator;
  readonly addButton: Locator;
  readonly todoItems: Locator;
  readonly errorMessage: Locator;
  readonly emptyState: Locator;
  readonly stats: Locator;
  readonly clearCompletedButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.todoInput = page.getByLabel('新しいタスク');
    this.addButton = page.getByRole('button', { name: '追加' });
    this.todoItems = page.getByTestId('todo-item');
    this.errorMessage = page.locator('#error-msg');
    this.emptyState = page.locator('#empty-state');
    this.stats = page.locator('#stats');
    this.clearCompletedButton = page.locator('#clear-completed');
  }

  // --- 操作メソッド ---

  async addTodo(text: string) {
    await this.todoInput.fill(text);
    await this.addButton.click();
  }

  async toggleTodo(index: number) {
    await this.todoItems.nth(index).getByLabel('完了にする').check();
  }

  async untoggleTodo(index: number) {
    await this.todoItems.nth(index).getByLabel('完了にする').uncheck();
  }

  async deleteTodo(index: number) {
    await this.todoItems.nth(index).getByRole('button', { name: '削除' }).click();
  }

  async editTodo(index: number, newText: string) {
    await this.todoItems.nth(index).getByRole('button', { name: '編集' }).click();
    const editInput = this.todoItems.nth(index).getByLabel('タスクを編集');
    await editInput.fill(newText);
    await this.todoItems.nth(index).getByRole('button', { name: '保存' }).click();
  }

  async setFilter(filter: 'all' | 'active' | 'done') {
    const filterNames = { all: 'すべて', active: '未完了', done: '完了済み' };
    await this.page.getByRole('group', { name: 'フィルター' })
      .getByRole('button', { name: filterNames[filter] }).click();
  }

  async clearCompleted() {
    await this.clearCompletedButton.click();
  }

  // --- 検証メソッド ---

  async expectTodoCount(count: number) {
    await expect(this.todoItems).toHaveCount(count);
  }

  async expectTodoText(index: number, text: string) {
    await expect(this.todoItems.nth(index).locator('.todo-text')).toHaveText(text);
  }

  async expectTodoDone(index: number) {
    await expect(this.todoItems.nth(index)).toHaveClass(/done/);
  }

  async expectTodoActive(index: number) {
    await expect(this.todoItems.nth(index)).not.toHaveClass(/done/);
  }

  async expectEmptyState() {
    await expect(this.emptyState).toBeVisible();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toBeVisible();
    await expect(this.errorMessage).toHaveText(message);
  }

  async expectStats(text: string | RegExp) {
    await expect(this.stats).toHaveText(text);
  }

  async expectClearCompletedVisible() {
    await expect(this.clearCompletedButton).toBeVisible();
  }

  async expectClearCompletedHidden() {
    await expect(this.clearCompletedButton).toBeHidden();
  }
}
```

### カスタムFixture

```typescript
// fixtures/todo-fixtures.ts
import { test as base } from '@playwright/test';
import path from 'path';
import { TodoPage } from '../pages/todo-page';

const TEST_PAGE = path.resolve(__dirname, '../todo-app.html');

type TodoFixtures = {
  todoPage: TodoPage;
};

export const test = base.extend<TodoFixtures>({
  todoPage: async ({ page }, use) => {
    await page.goto(`file://${TEST_PAGE}`);
    // LocalStorageをクリアしてテストの独立性を担保
    await page.evaluate(() => localStorage.clear());
    await page.reload();
    const todoPage = new TodoPage(page);
    await use(todoPage);
  },
});

export { expect } from '@playwright/test';
```

### テストデータ

```typescript
// test-data/todos.ts
export const sampleTodos = [
  '牛乳を買う',
  'レポートを書く',
  'メールを返す',
  'ジョギングする',
  '本を読む',
];

export const longText = 'あ'.repeat(101); // 101文字（上限超え）
export const maxText = 'あ'.repeat(100);  // 100文字（上限ちょうど）
```

### CRUD操作テスト

```typescript
// tests/todo-crud.spec.ts
// 学べる内容：CRUD操作のE2Eテスト、POM活用
// 実行方法：npx playwright test tests/todo-crud.spec.ts --project=chromium

import { test, expect } from '../fixtures/todo-fixtures';
import { sampleTodos } from '../test-data/todos';

test.describe('CRUD操作', () => {

  test('タスクを追加できる', async ({ todoPage }) => {
    await todoPage.addTodo('牛乳を買う');
    await todoPage.expectTodoCount(1);
    await todoPage.expectTodoText(0, '牛乳を買う');
    await todoPage.expectStats('全1件（未完了: 1件 / 完了: 0件）');
  });

  test('複数のタスクを追加できる', async ({ todoPage }) => {
    for (const todo of sampleTodos) {
      await todoPage.addTodo(todo);
    }
    await todoPage.expectTodoCount(5);
    await todoPage.expectStats(/全5件/);
  });

  test('タスクを完了にできる', async ({ todoPage }) => {
    await todoPage.addTodo('完了するタスク');
    await todoPage.toggleTodo(0);
    await todoPage.expectTodoDone(0);
    await todoPage.expectStats('全1件（未完了: 0件 / 完了: 1件）');
  });

  test('完了を解除できる', async ({ todoPage }) => {
    await todoPage.addTodo('トグルタスク');
    await todoPage.toggleTodo(0);
    await todoPage.expectTodoDone(0);

    await todoPage.untoggleTodo(0);
    await todoPage.expectTodoActive(0);
  });

  test('タスクを編集できる', async ({ todoPage }) => {
    await todoPage.addTodo('元のタスク');
    await todoPage.editTodo(0, '編集後のタスク');
    await todoPage.expectTodoText(0, '編集後のタスク');
  });

  test('タスクを削除できる', async ({ todoPage }) => {
    await todoPage.addTodo('削除するタスク');
    await todoPage.addTodo('残すタスク');
    await todoPage.expectTodoCount(2);

    await todoPage.deleteTodo(0);
    await todoPage.expectTodoCount(1);
    await todoPage.expectTodoText(0, '残すタスク');
  });
});
```

### フィルターテスト

```typescript
// tests/todo-filter.spec.ts
import { test, expect } from '../fixtures/todo-fixtures';

test.describe('フィルター機能', () => {

  test.beforeEach(async ({ todoPage }) => {
    // 3つのタスクを追加し、1つを完了にする
    await todoPage.addTodo('未完了タスク1');
    await todoPage.addTodo('完了タスク');
    await todoPage.addTodo('未完了タスク2');
    await todoPage.toggleTodo(1);
  });

  test('「すべて」で全タスクが表示される', async ({ todoPage }) => {
    await todoPage.setFilter('all');
    await todoPage.expectTodoCount(3);
  });

  test('「未完了」で未完了タスクだけ表示される', async ({ todoPage }) => {
    await todoPage.setFilter('active');
    await todoPage.expectTodoCount(2);
    await todoPage.expectTodoText(0, '未完了タスク1');
    await todoPage.expectTodoText(1, '未完了タスク2');
  });

  test('「完了済み」で完了タスクだけ表示される', async ({ todoPage }) => {
    await todoPage.setFilter('done');
    await todoPage.expectTodoCount(1);
    await todoPage.expectTodoText(0, '完了タスク');
  });

  test('完了済みを一括削除できる', async ({ todoPage }) => {
    await todoPage.expectClearCompletedVisible();
    await todoPage.clearCompleted();
    await todoPage.expectTodoCount(2);
    await todoPage.expectClearCompletedHidden();
    await todoPage.expectStats('全2件（未完了: 2件 / 完了: 0件）');
  });
});
```

### データ永続化テスト

```typescript
// tests/todo-persistence.spec.ts
import { test, expect } from '../fixtures/todo-fixtures';

test.describe('データ永続化（LocalStorage）', () => {

  test('タスクがリロード後も保持される', async ({ todoPage, page }) => {
    await todoPage.addTodo('永続化テスト');
    await todoPage.toggleTodo(0);

    // ページをリロード
    await page.reload();

    // リロード後も状態が保持される
    const reloadedPage = new (await import('../pages/todo-page')).TodoPage(page);
    await reloadedPage.expectTodoCount(1);
    await reloadedPage.expectTodoText(0, '永続化テスト');
    await reloadedPage.expectTodoDone(0);
  });

  test('削除がリロード後も反映される', async ({ todoPage, page }) => {
    await todoPage.addTodo('タスクA');
    await todoPage.addTodo('タスクB');
    await todoPage.deleteTodo(0);

    await page.reload();

    const reloadedPage = new (await import('../pages/todo-page')).TodoPage(page);
    await reloadedPage.expectTodoCount(1);
    await reloadedPage.expectTodoText(0, 'タスクB');
  });
});
```

### エッジケーステスト

```typescript
// tests/todo-edge-cases.spec.ts
import { test, expect } from '../fixtures/todo-fixtures';
import { longText, maxText } from '../test-data/todos';

test.describe('エッジケース', () => {

  test('空文字でタスクを追加するとエラーになる', async ({ todoPage }) => {
    await todoPage.addTodo('');
    await todoPage.expectError('タスクを入力してください');
    await todoPage.expectTodoCount(0);
  });

  test('101文字以上でエラーになる', async ({ todoPage }) => {
    await todoPage.addTodo(longText);
    await todoPage.expectError('タスクは100文字以内で入力してください');
  });

  test('100文字ちょうどは追加できる', async ({ todoPage }) => {
    await todoPage.addTodo(maxText);
    await todoPage.expectTodoCount(1);
  });

  test('重複タスクはエラーになる', async ({ todoPage }) => {
    await todoPage.addTodo('重複テスト');
    await todoPage.addTodo('重複テスト');
    await todoPage.expectError('同じタスクが既に存在します');
    await todoPage.expectTodoCount(1);
  });

  test('タスクがないときは空状態が表示される', async ({ todoPage }) => {
    await todoPage.expectEmptyState();
    await todoPage.expectStats('全0件（未完了: 0件 / 完了: 0件）');
  });

  test('全タスクを削除すると空状態に戻る', async ({ todoPage }) => {
    await todoPage.addTodo('タスク1');
    await todoPage.addTodo('タスク2');
    await todoPage.deleteTodo(0);
    await todoPage.deleteTodo(0);
    await todoPage.expectEmptyState();
  });
});
```

</details>

<details>
<summary>解答例（改良版 ─ テスト戦略とCI設定を追加）</summary>

改良版では、以下を追加します。

### playwright.config.ts

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 10000,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: [
    ['html', { open: 'never' }],
    ['list'],
  ],
  use: {
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
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
      name: 'mobile',
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
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7
```

### テストのタグ付けと優先度管理

```typescript
// tests/todo-crud.spec.ts（改良版）
import { test, expect } from '../fixtures/todo-fixtures';

// 高優先度テスト（CI毎回実行）
test.describe('CRUD操作 @critical', () => {

  test('タスクの追加→完了→削除の一連の流れ', async ({ todoPage }) => {
    // 追加
    await todoPage.addTodo('統合テスト');
    await todoPage.expectTodoCount(1);

    // 完了
    await todoPage.toggleTodo(0);
    await todoPage.expectTodoDone(0);

    // 削除
    await todoPage.deleteTodo(0);
    await todoPage.expectEmptyState();
  });
});

// 回帰テスト（週次実行など）
test.describe('回帰テスト @regression', () => {

  test('10件のタスクを追加して全操作が正常に動作する', async ({ todoPage }) => {
    // 10件追加
    for (let i = 1; i <= 10; i++) {
      await todoPage.addTodo(`タスク${i}`);
    }
    await todoPage.expectTodoCount(10);

    // 5件を完了にする
    for (let i = 0; i < 5; i++) {
      await todoPage.toggleTodo(i);
    }
    await todoPage.expectStats('全10件（未完了: 5件 / 完了: 5件）');

    // フィルター切り替え
    await todoPage.setFilter('done');
    await todoPage.expectTodoCount(5);

    await todoPage.setFilter('active');
    await todoPage.expectTodoCount(5);

    // 完了済み一括削除
    await todoPage.setFilter('all');
    await todoPage.clearCompleted();
    await todoPage.expectTodoCount(5);
  });
});
```

**初心者向けとの違い:**
- `playwright.config.ts` でマルチブラウザ + モバイル端末のテスト設定
- CI環境ではリトライ回数を増やし、ワーカー数を調整
- GitHub Actionsワークフローでレポートをアーティファクトとして保存
- テストのタグ（`@critical`、`@regression`）で優先度を分離
- 統合テスト（一連の流れテスト）で実務に近いシナリオをカバー

</details>

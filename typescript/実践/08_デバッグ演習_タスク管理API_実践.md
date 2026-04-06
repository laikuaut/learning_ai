# 実践課題08：デバッグ演習 ─ タスク管理API型定義 ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第1章〜第7章（基本型、インターフェース、関数の型、ユニオン型、ジェネリクス、列挙型、型ガード）
> **課題の種類**: デバッグ
> **学習目標**: 型エラーを含むコードを読み解き、TypeScriptのコンパイルエラーメッセージを正しく理解して修正する力を養う

---

## 課題の説明

以下の「タスク管理APIの型定義と処理ロジック」には **10個の型エラー** が埋め込まれています。
コードをTypeScriptコンパイラに通し、エラーメッセージを手がかりにすべてのバグを見つけて修正してください。

### 進め方

1. 下のバグ入りコードをファイルに保存する（`task_api_buggy.ts`）
2. `npx tsc --noEmit task_api_buggy.ts` または `npx ts-node task_api_buggy.ts` でエラーを確認する
3. 1つずつバグを修正し、再コンパイルする
4. すべてのエラーが解消され、正常に実行できれば完了

### 正常実行時の出力

```
--- 全タスク ---
[1] 📋 API設計書の作成 (high/todo)
    担当: 田中太郎  期限: 2026-05-01
[2] 📋 ユニットテスト追加 (medium/in_progress)
    担当: 佐藤花子  期限: 2026-04-20
[3] 📋 ドキュメント更新 (low/done)
    担当: 鈴木一郎  期限: 2026-04-15

--- 進行中タスク ---
[2] ユニットテスト追加 (佐藤花子)

--- タスクの更新 ---
[1] API設計書の作成: todo → in_progress

--- 優先度別集計 ---
high: 1件
medium: 1件
low: 1件

--- 期限切れタスク ---
[2] ユニットテスト追加 (期限: 2026-04-20)
[3] ドキュメント更新 (期限: 2026-04-15)
```

---

## バグ入りコード

以下のコードをそのまま `task_api_buggy.ts` として保存してください。

```typescript
// タスク管理APIの型定義と処理ロジック（バグ入り版）
// このコードには10個の型エラーが含まれています。すべて修正してください。

// --- 列挙型と型定義 ---

enum Priority {
  High = "high",
  Medium = "medium",
  Low = "low",
}

enum Status {
  Todo = "todo",
  InProgress = "in_progress",
  Done = "done",
}

interface Task {
  id: number;
  title: string;
  priority: Priority;
  status: Status;
  assignee: string;
  deadline: string;
  tags: string[];
}

// バグ1: 戻り値の型が間違っている
function createTask(
  id: number,
  title: string,
  priority: Priority,
  assignee: string,
  deadline: string,
  tags: string[]
): string {
  return {
    id,
    title,
    priority,
    status: Status.Todo,
    assignee,
    deadline,
    tags,
  };
}

// バグ2: ジェネリクスの制約が足りない
function findById<T>(items: T[], id: number): T | undefined {
  return items.find((item) => item.id === id);
}

// バグ3: ユニオン型の扱いが間違っている
type TaskFilter = 
  | { type: "priority"; value: Priority }
  | { type: "status"; value: Status }
  | { type: "assignee"; value: string };

function filterTasks(tasks: Task[], filter: TaskFilter): Task[] {
  if (filter.type === "priority") {
    return tasks.filter((t) => t.priority === filter.value);
  }
  if (filter.type === "status") {
    return tasks.filter((t) => t.status === filter.value);
  }
  if (filter.type === "assignee") {
    // filter.value は string のはずだが...
    return tasks.filter((t) => t.assignee === filter.value.toUpperCase());
  }
  return tasks;
}

// バグ4: Partial の使い方が間違っている
function updateTask(task: Task, updates: Partial<Task>): Task {
  const updated: Task = { ...task, ...updates };
  // idは変更不可にしたい
  updated.id = updates.id;
  return updated;
}

// バグ5: 配列メソッドの型が合わない
function getTaskTitles(tasks: Task[]): number[] {
  return tasks.map((task) => task.title);
}

// バグ6: 型ガードの戻り値型が間違っている
function isOverdue(task: Task, today: string): boolean {
  return task.deadline < today && task.status !== Status.Done;
}

function getOverdueTasks(tasks: Task[], today: string): string[] {
  return tasks.filter((task) => isOverdue(task, today));
}

// バグ7: Record型の使い方が間違っている
function countByPriority(tasks: Task[]): Record<Priority, number> {
  const counts: Record<string, number> = {};
  for (const task of tasks) {
    counts[task.priority] = (counts[task.priority] || 0) + 1;
  }
  return counts;
}

// バグ8: インターフェースの実装が不完全
interface Displayable {
  display(): string;
}

class TaskDisplay implements Displayable {
  constructor(private task: Task) {}

  getTitle(): string {
    return this.task.title;
  }
}

// バグ9: オプショナルプロパティの安全でないアクセス
interface TaskSearchOptions {
  keyword?: string;
  maxResults?: number;
}

function searchTasks(tasks: Task[], options: TaskSearchOptions): Task[] {
  const keyword: string = options.keyword;
  const filtered = tasks.filter(
    (t) => t.title.includes(keyword) || t.assignee.includes(keyword)
  );
  return filtered.slice(0, options.maxResults);
}

// バグ10: ジェネリック関数の型パラメータが間違っている
function groupBy<T, K extends string>(
  items: T[],
  keyFn: (item: T) => K
): Record<K, T[]> {
  const result = {} as Record<K, T[]>;
  for (const item of items) {
    const key = keyFn(item);
    if (!result[key]) {
      result[key] = [];
    }
    result[key].push(item);
  }
  return result;
}

// --- メイン処理 ---
const tasks: Task[] = [
  createTask(1, "API設計書の作成", Priority.High, "田中太郎", "2026-05-01", ["設計", "API"]),
  createTask(2, "ユニットテスト追加", Priority.Medium, "佐藤花子", "2026-04-20", ["テスト"]),
  createTask(3, "ドキュメント更新", Priority.Low, "鈴木一郎", "2026-04-15", ["ドキュメント"]),
];

// 全タスク表示
console.log("--- 全タスク ---");
for (const task of tasks) {
  console.log(`[${task.id}] 📋 ${task.title} (${task.priority}/${task.status})`);
  console.log(`    担当: ${task.assignee}  期限: ${task.deadline}`);
}

// 進行中タスクのフィルタ
console.log("\n--- 進行中タスク ---");
// タスク2を進行中に更新してからフィルタ
tasks[1] = updateTask(tasks[1], { status: Status.InProgress });
const inProgress = filterTasks(tasks, { type: "status", value: Status.InProgress });
for (const task of inProgress) {
  console.log(`[${task.id}] ${task.title} (${task.assignee})`);
}

// タスク更新
console.log("\n--- タスクの更新 ---");
const task1 = findById(tasks, 1);
if (task1) {
  const updated = updateTask(task1, { status: Status.InProgress });
  console.log(`[${updated.id}] ${updated.title}: ${task1.status} → ${updated.status}`);
}

// 優先度別集計
console.log("\n--- 優先度別集計 ---");
const priorityCounts = countByPriority(tasks);
console.log(`high: ${priorityCounts[Priority.High] || 0}件`);
console.log(`medium: ${priorityCounts[Priority.Medium] || 0}件`);
console.log(`low: ${priorityCounts[Priority.Low] || 0}件`);

// 期限切れタスク
console.log("\n--- 期限切れタスク ---");
const today = "2026-04-25";
const overdue = getOverdueTasks(tasks, today);
for (const task of overdue) {
  console.log(`[${task.id}] ${task.title} (期限: ${task.deadline})`);
}
```

---

## バグの一覧と解説

<details>
<summary>バグ1：createTask の戻り値型</summary>

**エラー内容**: `Type '{ id: number; title: string; ... }' is not assignable to type 'string'`

**原因**: 戻り値の型が `string` になっているが、実際にはオブジェクトを返している。

**修正**:
```typescript
// 修正前
function createTask(...): string {

// 修正後
function createTask(...): Task {
```

**学びのポイント**: 戻り値の型注釈は実際に返す値と一致させる必要があります。TypeScriptは実装と型注釈の不一致を検出してくれます。

</details>

<details>
<summary>バグ2：findById のジェネリクス制約</summary>

**エラー内容**: `Property 'id' does not exist on type 'T'`

**原因**: `T` に制約がないため、`item.id` にアクセスできない。

**修正**:
```typescript
// 修正前
function findById<T>(items: T[], id: number): T | undefined {

// 修正後
function findById<T extends { id: number }>(items: T[], id: number): T | undefined {
```

**学びのポイント**: ジェネリクスの型パラメータにプロパティアクセスする場合は、`extends` で制約を付ける必要があります。

</details>

<details>
<summary>バグ3：filterTasks の assignee フィルタ</summary>

**エラー内容**: 実行時に意図しない動作（大文字変換してしまう）

**原因**: `filter.value.toUpperCase()` で検索値を大文字に変換しているため、一致しなくなる。これは型エラーではなくロジックバグです。

**修正**:
```typescript
// 修正前
return tasks.filter((t) => t.assignee === filter.value.toUpperCase());

// 修正後
return tasks.filter((t) => t.assignee === filter.value);
```

**学びのポイント**: TypeScriptは型の正しさを保証しますが、ロジックの正しさまでは保証しません。型が正しくてもバグは起こり得ます。

</details>

<details>
<summary>バグ4：updateTask の id 上書き</summary>

**エラー内容**: `Type 'number | undefined' is not assignable to type 'number'`

**原因**: `updates.id` は `Partial<Task>` なので `number | undefined` 型。それを `number` 型のプロパティに代入しようとしている。また、意図としてはidを変更不可にしたいのに、`updates.id` を代入している。

**修正**:
```typescript
// 修正前
updated.id = updates.id;

// 修正後
updated.id = task.id; // 元のidを維持する
```

**学びのポイント**: `Partial<T>` はすべてのプロパティをオプショナルにするため、各プロパティが `T[K] | undefined` になります。

</details>

<details>
<summary>バグ5：getTaskTitles の戻り値型</summary>

**エラー内容**: `Type 'string[]' is not assignable to type 'number[]'`

**原因**: `task.title` は `string` なので `map` の結果は `string[]` だが、戻り値型が `number[]` になっている。

**修正**:
```typescript
// 修正前
function getTaskTitles(tasks: Task[]): number[] {

// 修正後
function getTaskTitles(tasks: Task[]): string[] {
```

</details>

<details>
<summary>バグ6：getOverdueTasks の戻り値型</summary>

**エラー内容**: `Type 'Task[]' is not assignable to type 'string[]'`

**原因**: `filter` は `Task[]` を返すが、関数の戻り値型が `string[]` になっている。

**修正**:
```typescript
// 修正前
function getOverdueTasks(tasks: Task[], today: string): string[] {

// 修正後
function getOverdueTasks(tasks: Task[], today: string): Task[] {
```

</details>

<details>
<summary>バグ7：countByPriority の初期値</summary>

**エラー内容**: `Record<Priority, number>` の戻り値型に対して、すべてのキーが揃っていない可能性がある。

**原因**: `Record<Priority, number>` は3つのキー（`high`, `medium`, `low`）がすべて存在することを要求するが、空のオブジェクトから始めているため、タスクが存在しない優先度のカウントが欠落する。内部の型が `Record<string, number>` で互換性がない。

**修正**:
```typescript
// 修正前
const counts: Record<string, number> = {};

// 修正後
const counts: Record<Priority, number> = {
  [Priority.High]: 0,
  [Priority.Medium]: 0,
  [Priority.Low]: 0,
};
```

</details>

<details>
<summary>バグ8：TaskDisplay の display メソッド欠落</summary>

**エラー内容**: `Class 'TaskDisplay' incorrectly implements interface 'Displayable'. Property 'display' is missing`

**原因**: `Displayable` インターフェースの `display()` メソッドが実装されていない。

**修正**:
```typescript
class TaskDisplay implements Displayable {
  constructor(private task: Task) {}

  // display メソッドを追加
  display(): string {
    return `[${this.task.id}] ${this.task.title} (${this.task.priority})`;
  }

  getTitle(): string {
    return this.task.title;
  }
}
```

</details>

<details>
<summary>バグ9：オプショナルプロパティの安全でないアクセス</summary>

**エラー内容**: `Type 'string | undefined' is not assignable to type 'string'`

**原因**: `options.keyword` は `string | undefined` だが、`const keyword: string` に代入しようとしている。

**修正**:
```typescript
// 修正前
const keyword: string = options.keyword;

// 修正後
const keyword: string = options.keyword ?? "";
```

**学びのポイント**: オプショナルプロパティ（`?`）は `undefined` になる可能性があるため、デフォルト値を提供するか、`undefined` チェックが必要です。Nullish Coalescing演算子（`??`）が便利です。

</details>

<details>
<summary>バグ10：groupBy は正しい（ダミーバグ）</summary>

**解説**: 実はバグ10の `groupBy` 関数自体には型エラーはありません。ただし、メイン処理で `getOverdueTasks` の戻り値を `string[]` として使おうとしている部分で間接的にエラーが発生します（バグ6の修正で解消）。

型エラーが10個と言いましたが、バグ3はロジックバグであり、コンパイラでは検出できません。コンパイルエラーは9つ、ロジックバグが1つ、合計10個のバグが存在します。

**学びのポイント**: デバッグでは「コンパイルエラー」と「ロジックエラー」の両方に注意が必要です。TypeScriptの型システムはコンパイルエラーを防ぎますが、ロジックの正しさまでは保証しません。

</details>

---

## 修正完了版

<details>
<summary>修正済みコード（全体）</summary>

```typescript
// タスク管理APIの型定義と処理ロジック（修正済み版）
// 実行方法：npx ts-node task_api_fixed.ts

enum Priority {
  High = "high",
  Medium = "medium",
  Low = "low",
}

enum Status {
  Todo = "todo",
  InProgress = "in_progress",
  Done = "done",
}

interface Task {
  id: number;
  title: string;
  priority: Priority;
  status: Status;
  assignee: string;
  deadline: string;
  tags: string[];
}

// バグ1修正: 戻り値型を Task に
function createTask(
  id: number,
  title: string,
  priority: Priority,
  assignee: string,
  deadline: string,
  tags: string[]
): Task {
  return { id, title, priority, status: Status.Todo, assignee, deadline, tags };
}

// バグ2修正: ジェネリクスに制約を追加
function findById<T extends { id: number }>(items: T[], id: number): T | undefined {
  return items.find((item) => item.id === id);
}

type TaskFilter =
  | { type: "priority"; value: Priority }
  | { type: "status"; value: Status }
  | { type: "assignee"; value: string };

function filterTasks(tasks: Task[], filter: TaskFilter): Task[] {
  if (filter.type === "priority") {
    return tasks.filter((t) => t.priority === filter.value);
  }
  if (filter.type === "status") {
    return tasks.filter((t) => t.status === filter.value);
  }
  if (filter.type === "assignee") {
    // バグ3修正: toUpperCase() を削除
    return tasks.filter((t) => t.assignee === filter.value);
  }
  return tasks;
}

// バグ4修正: 元のidを維持
function updateTask(task: Task, updates: Partial<Task>): Task {
  const updated: Task = { ...task, ...updates };
  updated.id = task.id;
  return updated;
}

// バグ5修正: 戻り値型を string[] に
function getTaskTitles(tasks: Task[]): string[] {
  return tasks.map((task) => task.title);
}

function isOverdue(task: Task, today: string): boolean {
  return task.deadline < today && task.status !== Status.Done;
}

// バグ6修正: 戻り値型を Task[] に
function getOverdueTasks(tasks: Task[], today: string): Task[] {
  return tasks.filter((task) => isOverdue(task, today));
}

// バグ7修正: 初期値を全キーで定義
function countByPriority(tasks: Task[]): Record<Priority, number> {
  const counts: Record<Priority, number> = {
    [Priority.High]: 0,
    [Priority.Medium]: 0,
    [Priority.Low]: 0,
  };
  for (const task of tasks) {
    counts[task.priority] = counts[task.priority] + 1;
  }
  return counts;
}

// バグ8修正: display メソッドを追加
interface Displayable {
  display(): string;
}

class TaskDisplay implements Displayable {
  constructor(private task: Task) {}

  display(): string {
    return `[${this.task.id}] ${this.task.title} (${this.task.priority})`;
  }

  getTitle(): string {
    return this.task.title;
  }
}

// バグ9修正: Nullish Coalescing でデフォルト値を提供
interface TaskSearchOptions {
  keyword?: string;
  maxResults?: number;
}

function searchTasks(tasks: Task[], options: TaskSearchOptions): Task[] {
  const keyword: string = options.keyword ?? "";
  const filtered = tasks.filter(
    (t) => t.title.includes(keyword) || t.assignee.includes(keyword)
  );
  return filtered.slice(0, options.maxResults);
}

function groupBy<T, K extends string>(
  items: T[],
  keyFn: (item: T) => K
): Record<K, T[]> {
  const result = {} as Record<K, T[]>;
  for (const item of items) {
    const key = keyFn(item);
    if (!result[key]) {
      result[key] = [];
    }
    result[key].push(item);
  }
  return result;
}

// --- メイン処理 ---
const tasks: Task[] = [
  createTask(1, "API設計書の作成", Priority.High, "田中太郎", "2026-05-01", ["設計", "API"]),
  createTask(2, "ユニットテスト追加", Priority.Medium, "佐藤花子", "2026-04-20", ["テスト"]),
  createTask(3, "ドキュメント更新", Priority.Low, "鈴木一郎", "2026-04-15", ["ドキュメント"]),
];

console.log("--- 全タスク ---");
for (const task of tasks) {
  console.log(`[${task.id}] 📋 ${task.title} (${task.priority}/${task.status})`);
  console.log(`    担当: ${task.assignee}  期限: ${task.deadline}`);
}

console.log("\n--- 進行中タスク ---");
tasks[1] = updateTask(tasks[1], { status: Status.InProgress });
const inProgress = filterTasks(tasks, { type: "status", value: Status.InProgress });
for (const task of inProgress) {
  console.log(`[${task.id}] ${task.title} (${task.assignee})`);
}

console.log("\n--- タスクの更新 ---");
const task1 = findById(tasks, 1);
if (task1) {
  const updated = updateTask(task1, { status: Status.InProgress });
  console.log(`[${updated.id}] ${updated.title}: ${task1.status} → ${updated.status}`);
}

console.log("\n--- 優先度別集計 ---");
const priorityCounts = countByPriority(tasks);
console.log(`high: ${priorityCounts[Priority.High]}件`);
console.log(`medium: ${priorityCounts[Priority.Medium]}件`);
console.log(`low: ${priorityCounts[Priority.Low]}件`);

console.log("\n--- 期限切れタスク ---");
const today = "2026-04-25";
const overdue = getOverdueTasks(tasks, today);
for (const task of overdue) {
  console.log(`[${task.id}] ${task.title} (期限: ${task.deadline})`);
}
```

</details>

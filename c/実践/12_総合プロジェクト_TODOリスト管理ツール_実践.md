# 実践課題12：総合プロジェクト ─ TODOリスト管理ツール ★5

> **難易度**: ★★★★★（総合）
> **前提知識**: 第1章〜第8章（全範囲）
> **課題の種類**: ミニプロジェクト
> **学習目標**: C言語の全知識（変数・制御構造・配列・文字列・関数・ポインタ・構造体・ファイル操作）を総合的に活用し、実用的なCLIアプリケーションを設計・実装する

---

## 完成イメージ

```
===== TODO リスト管理ツール =====
データファイル: todo.dat

コマンド一覧:
  add    - タスクを追加
  list   - タスク一覧を表示
  done   - タスクを完了にする
  undone - タスクを未完了に戻す
  delete - タスクを削除
  edit   - タスクを編集
  search - タスクを検索
  sort   - タスクをソート
  stats  - 統計情報を表示
  save   - ファイルに保存
  load   - ファイルから読み込み
  quit   - 終了

> add
タスク名: レポートを書く
優先度 (1:低 2:中 3:高): 3
期限 (YYYY-MM-DD, 空でスキップ): 2026-04-10
追加しました: [#1] レポートを書く [高] 期限:2026-04-10

> list

--- TODOリスト (3件) ---
 #  状態  優先度  期限        タスク名
-----------------------------------------------------
 1. [ ]   [高]    2026-04-10  レポートを書く
 2. [ ]   [中]    2026-04-15  買い物に行く
 3. [x]   [低]    (なし)      部屋を掃除する

> done 1
タスク #1 を完了にしました: レポートを書く

> stats

--- 統計情報 ---
総タスク数: 3
  完了    : 2 (66.7%)
  未完了  : 1 (33.3%)
優先度別:
  高: 1件 (完了1)
  中: 1件 (完了0)
  低: 1件 (完了1)
```

---

## 課題の要件

### データ構造

各タスクは以下の情報を持ちます。

| フィールド | 型 | 説明 |
|---|---|---|
| id | int | タスクID（自動採番） |
| title | char[100] | タスク名 |
| priority | int | 優先度（1:低、2:中、3:高） |
| done | int | 完了フラグ（0:未完了、1:完了） |
| deadline | char[11] | 期限（YYYY-MM-DD 形式、空なら "(なし)"） |

### 機能一覧

1. **add** ─ タスクの追加（タスク名・優先度・期限を入力）
2. **list** ─ 全タスクの一覧表示（表形式）
3. **done / undone** ─ 完了状態の切り替え
4. **delete** ─ タスクの削除
5. **edit** ─ タスク名や優先度の変更
6. **search** ─ キーワードによるタスク検索
7. **sort** ─ 優先度順・期限順・状態順でのソート
8. **stats** ─ 統計情報の表示
9. **save / load** ─ ファイルへの保存と読み込み
10. **quit** ─ プログラムの終了

### 技術要件

- 動的メモリ確保（`malloc` / `realloc` / `free`）を使ってタスク数の上限をなくす
- 構造体でタスクを管理する
- 関数でモジュール化する（`main` は30行以内を目標）
- ファイル保存はCSV形式またはカスタム形式
- 不正な入力に対して適切なエラーメッセージを出す

---

## ステップガイド

<details>
<summary>ステップ1：データ構造を設計する</summary>

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TITLE_LEN 100
#define DATE_LEN 11
#define LINE_LEN 256

typedef struct {
    int id;
    char title[TITLE_LEN];
    int priority;   /* 1:低, 2:中, 3:高 */
    int done;        /* 0:未完了, 1:完了 */
    char deadline[DATE_LEN];
} Task;

typedef struct {
    Task *tasks;
    int count;
    int capacity;
    int next_id;
} TodoList;
```

</details>

<details>
<summary>ステップ2：リストの初期化と動的拡張</summary>

```c
#define INITIAL_CAPACITY 8

TodoList *todo_create(void) {
    TodoList *list = (TodoList *)malloc(sizeof(TodoList));
    if (list == NULL) return NULL;
    list->tasks = (Task *)malloc(sizeof(Task) * INITIAL_CAPACITY);
    if (list->tasks == NULL) {
        free(list);
        return NULL;
    }
    list->count = 0;
    list->capacity = INITIAL_CAPACITY;
    list->next_id = 1;
    return list;
}

/* 容量が足りなければ自動拡張 */
int todo_ensure_capacity(TodoList *list) {
    if (list->count < list->capacity) return 1;
    int new_cap = list->capacity * 2;
    Task *new_tasks = (Task *)realloc(list->tasks, sizeof(Task) * new_cap);
    if (new_tasks == NULL) return 0;
    list->tasks = new_tasks;
    list->capacity = new_cap;
    return 1;
}
```

</details>

<details>
<summary>ステップ3：コマンド解析のメインループ</summary>

```c
int main(void) {
    TodoList *list = todo_create();
    char cmd[LINE_LEN];

    printf("===== TODO リスト管理ツール =====\n");
    show_help();

    while (1) {
        printf("\n> ");
        fgets(cmd, sizeof(cmd), stdin);
        cmd[strcspn(cmd, "\n")] = '\0';

        if (strcmp(cmd, "quit") == 0) {
            break;
        } else if (strcmp(cmd, "add") == 0) {
            todo_add(list);
        } else if (strcmp(cmd, "list") == 0) {
            todo_list(list);
        }
        /* ... 他のコマンドも同様 ... */
    }

    todo_destroy(list);
    return 0;
}
```

</details>

<details>
<summary>ステップ4：ソート機能を実装する</summary>

`qsort` 標準ライブラリ関数を使うのが効率的です。

```c
/* 優先度の降順（高→低）でソート */
int compare_by_priority(const void *a, const void *b) {
    const Task *ta = (const Task *)a;
    const Task *tb = (const Task *)b;
    return tb->priority - ta->priority;  /* 降順 */
}

void todo_sort(TodoList *list, const char *key) {
    if (strcmp(key, "priority") == 0) {
        qsort(list->tasks, list->count, sizeof(Task), compare_by_priority);
    }
    /* ... 他のソートキーも同様 ... */
}
```

</details>

<details>
<summary>ステップ5：ファイル保存と読み込み</summary>

CSV形式で保存する場合、タスク名にカンマが含まれる可能性を考慮して、タブ区切り（TSV）またはパイプ区切りを使うのが安全です。

```c
int todo_save(const TodoList *list, const char *filename) {
    FILE *fp = fopen(filename, "w");
    if (fp == NULL) return 0;

    fprintf(fp, "%d\n", list->next_id);  /* 次のID */
    for (int i = 0; i < list->count; i++) {
        fprintf(fp, "%d|%s|%d|%d|%s\n",
                list->tasks[i].id,
                list->tasks[i].title,
                list->tasks[i].priority,
                list->tasks[i].done,
                list->tasks[i].deadline);
    }
    fclose(fp);
    return 1;
}
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け ─ 基本機能版）</summary>

```c
/*
 * TODOリスト管理ツール（基本版）
 * 学べる内容：構造体、動的メモリ、ファイルI/O、文字列操作、関数設計
 * コンパイル：gcc -o todo todo.c
 * 実行：./todo
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* --- 定数 --- */
#define TITLE_LEN 100
#define DATE_LEN 11
#define LINE_LEN 256
#define INITIAL_CAPACITY 8
#define FILENAME "todo.dat"

/* --- データ構造 --- */

typedef struct {
    int id;
    char title[TITLE_LEN];
    int priority;
    int done;
    char deadline[DATE_LEN];
} Task;

typedef struct {
    Task *tasks;
    int count;
    int capacity;
    int next_id;
} TodoList;

/* --- 優先度ラベル --- */

const char *priority_label(int p) {
    switch (p) {
        case 1: return "低";
        case 2: return "中";
        case 3: return "高";
        default: return "?";
    }
}

/* --- リスト管理 --- */

TodoList *todo_create(void) {
    TodoList *list = (TodoList *)malloc(sizeof(TodoList));
    if (list == NULL) return NULL;
    list->tasks = (Task *)malloc(sizeof(Task) * INITIAL_CAPACITY);
    if (list->tasks == NULL) {
        free(list);
        return NULL;
    }
    list->count = 0;
    list->capacity = INITIAL_CAPACITY;
    list->next_id = 1;
    return list;
}

void todo_destroy(TodoList *list) {
    if (list != NULL) {
        free(list->tasks);
        free(list);
    }
}

int todo_ensure_capacity(TodoList *list) {
    if (list->count < list->capacity) return 1;
    int new_cap = list->capacity * 2;
    Task *new_tasks = (Task *)realloc(list->tasks, sizeof(Task) * new_cap);
    if (new_tasks == NULL) {
        printf("エラー: メモリ拡張に失敗しました。\n");
        return 0;
    }
    list->tasks = new_tasks;
    list->capacity = new_cap;
    return 1;
}

/* --- IDからインデックスを検索 --- */

int find_index_by_id(const TodoList *list, int id) {
    int i;
    for (i = 0; i < list->count; i++) {
        if (list->tasks[i].id == id) return i;
    }
    return -1;
}

/* --- タスク追加 --- */

void todo_add(TodoList *list) {
    char line[LINE_LEN];

    if (!todo_ensure_capacity(list)) return;

    Task *t = &list->tasks[list->count];
    t->id = list->next_id++;

    printf("タスク名: ");
    fgets(t->title, TITLE_LEN, stdin);
    t->title[strcspn(t->title, "\n")] = '\0';
    if (strlen(t->title) == 0) {
        printf("タスク名が空です。追加をキャンセルしました。\n");
        list->next_id--;
        return;
    }

    printf("優先度 (1:低 2:中 3:高): ");
    fgets(line, sizeof(line), stdin);
    if (sscanf(line, "%d", &t->priority) != 1 || t->priority < 1 || t->priority > 3) {
        t->priority = 2;
    }

    printf("期限 (YYYY-MM-DD, 空でスキップ): ");
    fgets(line, sizeof(line), stdin);
    line[strcspn(line, "\n")] = '\0';
    if (strlen(line) > 0 && strlen(line) <= 10) {
        strncpy(t->deadline, line, DATE_LEN - 1);
        t->deadline[DATE_LEN - 1] = '\0';
    } else {
        strcpy(t->deadline, "");
    }

    t->done = 0;
    list->count++;
    printf("追加しました: [#%d] %s [%s] 期限:%s\n",
           t->id, t->title, priority_label(t->priority),
           strlen(t->deadline) > 0 ? t->deadline : "(なし)");
}

/* --- 一覧表示 --- */

void todo_list(const TodoList *list) {
    int i;
    if (list->count == 0) {
        printf("タスクがありません。\n");
        return;
    }

    printf("\n--- TODOリスト (%d件) ---\n", list->count);
    printf(" #  状態  優先度  期限        タスク名\n");
    printf("-----------------------------------------------------\n");
    for (i = 0; i < list->count; i++) {
        const Task *t = &list->tasks[i];
        printf("%2d. [%s]   [%s]    %-10s  %s\n",
               t->id,
               t->done ? "x" : " ",
               priority_label(t->priority),
               strlen(t->deadline) > 0 ? t->deadline : "(なし)    ",
               t->title);
    }
}

/* --- 完了・未完了の切り替え --- */

void todo_set_done(TodoList *list, int done_flag) {
    char line[LINE_LEN];
    int id, idx;

    printf("タスク番号: ");
    fgets(line, sizeof(line), stdin);
    if (sscanf(line, "%d", &id) != 1) {
        printf("数字を入力してください。\n");
        return;
    }

    idx = find_index_by_id(list, id);
    if (idx < 0) {
        printf("タスク #%d が見つかりません。\n", id);
        return;
    }

    list->tasks[idx].done = done_flag;
    printf("タスク #%d を%sにしました: %s\n",
           id,
           done_flag ? "完了" : "未完了",
           list->tasks[idx].title);
}

/* --- 削除 --- */

void todo_delete(TodoList *list) {
    char line[LINE_LEN];
    int id, idx, i;

    printf("削除するタスク番号: ");
    fgets(line, sizeof(line), stdin);
    if (sscanf(line, "%d", &id) != 1) {
        printf("数字を入力してください。\n");
        return;
    }

    idx = find_index_by_id(list, id);
    if (idx < 0) {
        printf("タスク #%d が見つかりません。\n", id);
        return;
    }

    printf("「%s」を削除しますか？ (y/n): ", list->tasks[idx].title);
    fgets(line, sizeof(line), stdin);
    if (line[0] != 'y' && line[0] != 'Y') {
        printf("キャンセルしました。\n");
        return;
    }

    for (i = idx; i < list->count - 1; i++) {
        list->tasks[i] = list->tasks[i + 1];
    }
    list->count--;
    printf("削除しました。\n");
}

/* --- 検索 --- */

void todo_search(const TodoList *list) {
    char keyword[TITLE_LEN];
    int i, found = 0;

    printf("検索キーワード: ");
    fgets(keyword, sizeof(keyword), stdin);
    keyword[strcspn(keyword, "\n")] = '\0';

    for (i = 0; i < list->count; i++) {
        if (strstr(list->tasks[i].title, keyword) != NULL) {
            const Task *t = &list->tasks[i];
            printf("  #%d [%s] [%s] %s - %s\n",
                   t->id,
                   t->done ? "x" : " ",
                   priority_label(t->priority),
                   strlen(t->deadline) > 0 ? t->deadline : "(なし)",
                   t->title);
            found++;
        }
    }
    if (found == 0) {
        printf("見つかりませんでした。\n");
    } else {
        printf("%d 件見つかりました。\n", found);
    }
}

/* --- ソート --- */

int cmp_priority(const void *a, const void *b) {
    return ((const Task *)b)->priority - ((const Task *)a)->priority;
}

int cmp_deadline(const void *a, const void *b) {
    const Task *ta = (const Task *)a;
    const Task *tb = (const Task *)b;
    /* 期限なしは後ろに */
    if (strlen(ta->deadline) == 0 && strlen(tb->deadline) == 0) return 0;
    if (strlen(ta->deadline) == 0) return 1;
    if (strlen(tb->deadline) == 0) return -1;
    return strcmp(ta->deadline, tb->deadline);
}

int cmp_done(const void *a, const void *b) {
    return ((const Task *)a)->done - ((const Task *)b)->done;
}

void todo_sort(TodoList *list) {
    char line[LINE_LEN];

    printf("ソート基準 (1:優先度 2:期限 3:状態): ");
    fgets(line, sizeof(line), stdin);

    switch (line[0]) {
        case '1':
            qsort(list->tasks, list->count, sizeof(Task), cmp_priority);
            printf("優先度順にソートしました。\n");
            break;
        case '2':
            qsort(list->tasks, list->count, sizeof(Task), cmp_deadline);
            printf("期限順にソートしました。\n");
            break;
        case '3':
            qsort(list->tasks, list->count, sizeof(Task), cmp_done);
            printf("状態順にソートしました。\n");
            break;
        default:
            printf("無効な選択です。\n");
            break;
    }
}

/* --- 統計情報 --- */

void todo_stats(const TodoList *list) {
    int i;
    int done_count = 0;
    int prio_count[4] = {0};      /* [1]:低, [2]:中, [3]:高 */
    int prio_done_count[4] = {0};

    if (list->count == 0) {
        printf("タスクがありません。\n");
        return;
    }

    for (i = 0; i < list->count; i++) {
        if (list->tasks[i].done) done_count++;
        int p = list->tasks[i].priority;
        if (p >= 1 && p <= 3) {
            prio_count[p]++;
            if (list->tasks[i].done) prio_done_count[p]++;
        }
    }

    int undone = list->count - done_count;
    printf("\n--- 統計情報 ---\n");
    printf("総タスク数: %d\n", list->count);
    printf("  完了    : %d (%.1f%%)\n", done_count,
           (double)done_count / list->count * 100);
    printf("  未完了  : %d (%.1f%%)\n", undone,
           (double)undone / list->count * 100);
    printf("優先度別:\n");
    printf("  高: %d件 (完了%d)\n", prio_count[3], prio_done_count[3]);
    printf("  中: %d件 (完了%d)\n", prio_count[2], prio_done_count[2]);
    printf("  低: %d件 (完了%d)\n", prio_count[1], prio_done_count[1]);
}

/* --- ファイル保存 --- */

int todo_save(const TodoList *list, const char *filename) {
    FILE *fp = fopen(filename, "w");
    int i;
    if (fp == NULL) {
        printf("エラー: ファイルを開けませんでした: %s\n", filename);
        return 0;
    }
    fprintf(fp, "%d\n", list->next_id);
    for (i = 0; i < list->count; i++) {
        const Task *t = &list->tasks[i];
        fprintf(fp, "%d|%s|%d|%d|%s\n",
                t->id, t->title, t->priority, t->done, t->deadline);
    }
    fclose(fp);
    printf("%s に %d 件保存しました。\n", filename, list->count);
    return 1;
}

/* --- ファイル読み込み --- */

int todo_load(TodoList *list, const char *filename) {
    FILE *fp = fopen(filename, "r");
    char line[LINE_LEN];
    if (fp == NULL) {
        printf("ファイルが見つかりません: %s\n", filename);
        return 0;
    }

    /* 既存データをクリア */
    list->count = 0;

    /* 次のID */
    if (fgets(line, sizeof(line), fp) != NULL) {
        sscanf(line, "%d", &list->next_id);
    }

    while (fgets(line, sizeof(line), fp) != NULL) {
        line[strcspn(line, "\n")] = '\0';
        if (!todo_ensure_capacity(list)) break;

        Task *t = &list->tasks[list->count];
        /* パイプ区切りでパース */
        if (sscanf(line, "%d|%[^|]|%d|%d|%[^\n]",
                   &t->id, t->title, &t->priority, &t->done, t->deadline) >= 4) {
            /* deadline が空の場合の処理 */
            if (sscanf(line, "%d|%[^|]|%d|%d|%[^\n]",
                       &t->id, t->title, &t->priority, &t->done, t->deadline) < 5) {
                strcpy(t->deadline, "");
            }
            list->count++;
        }
    }

    fclose(fp);
    printf("%s から %d 件読み込みました。\n", filename, list->count);
    return 1;
}

/* --- ヘルプ表示 --- */

void show_help(void) {
    printf("\nコマンド一覧:\n");
    printf("  add    - タスクを追加\n");
    printf("  list   - タスク一覧を表示\n");
    printf("  done   - タスクを完了にする\n");
    printf("  undone - タスクを未完了に戻す\n");
    printf("  delete - タスクを削除\n");
    printf("  search - タスクを検索\n");
    printf("  sort   - タスクをソート\n");
    printf("  stats  - 統計情報を表示\n");
    printf("  save   - ファイルに保存\n");
    printf("  load   - ファイルから読み込み\n");
    printf("  help   - コマンド一覧を表示\n");
    printf("  quit   - 終了\n");
}

/* --- メイン --- */

int main(void) {
    TodoList *list = todo_create();
    char cmd[LINE_LEN];

    if (list == NULL) {
        printf("エラー: 初期化に失敗しました。\n");
        return 1;
    }

    printf("===== TODO リスト管理ツール =====\n");
    printf("データファイル: %s\n", FILENAME);
    show_help();

    while (1) {
        printf("\n> ");
        fgets(cmd, sizeof(cmd), stdin);
        cmd[strcspn(cmd, "\n")] = '\0';

        if (strcmp(cmd, "quit") == 0 || strcmp(cmd, "q") == 0) {
            printf("終了します。\n");
            break;
        } else if (strcmp(cmd, "add") == 0) {
            todo_add(list);
        } else if (strcmp(cmd, "list") == 0 || strcmp(cmd, "ls") == 0) {
            todo_list(list);
        } else if (strcmp(cmd, "done") == 0) {
            todo_set_done(list, 1);
        } else if (strcmp(cmd, "undone") == 0) {
            todo_set_done(list, 0);
        } else if (strcmp(cmd, "delete") == 0 || strcmp(cmd, "del") == 0) {
            todo_delete(list);
        } else if (strcmp(cmd, "search") == 0) {
            todo_search(list);
        } else if (strcmp(cmd, "sort") == 0) {
            todo_sort(list);
        } else if (strcmp(cmd, "stats") == 0) {
            todo_stats(list);
        } else if (strcmp(cmd, "save") == 0) {
            todo_save(list, FILENAME);
        } else if (strcmp(cmd, "load") == 0) {
            todo_load(list, FILENAME);
        } else if (strcmp(cmd, "help") == 0) {
            show_help();
        } else if (strlen(cmd) > 0) {
            printf("不明なコマンドです: %s\n", cmd);
            printf("'help' でコマンド一覧を表示します。\n");
        }
    }

    todo_destroy(list);
    return 0;
}
```

</details>

<details>
<summary>解答例（改良版 ─ コマンド引数対応＆カラー出力）</summary>

コマンドに引数を直接指定できるようにし、ANSI エスケープコード（ANSI escape code）でカラー出力を追加したバージョンです。

```c
/*
 * TODOリスト管理ツール（改良版）
 * 学べる内容：コマンドパーサー、ANSIカラー出力、コマンド引数処理
 * コンパイル：gcc -o todo2 todo2.c
 * 実行：./todo2
 *
 * 使い方: "done 3" のようにコマンドと引数を1行で入力可能
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TITLE_LEN 100
#define DATE_LEN 11
#define LINE_LEN 256
#define INITIAL_CAPACITY 8
#define FILENAME "todo.dat"

/* ANSIカラーコード */
#define COLOR_RESET   "\033[0m"
#define COLOR_RED     "\033[31m"
#define COLOR_GREEN   "\033[32m"
#define COLOR_YELLOW  "\033[33m"
#define COLOR_CYAN    "\033[36m"
#define COLOR_DIM     "\033[2m"

typedef struct {
    int id;
    char title[TITLE_LEN];
    int priority;
    int done;
    char deadline[DATE_LEN];
} Task;

typedef struct {
    Task *tasks;
    int count;
    int capacity;
    int next_id;
} TodoList;

/* --- コマンド解析 --- */

typedef struct {
    char command[32];
    char arg[LINE_LEN];
} ParsedCommand;

ParsedCommand parse_input(const char *input) {
    ParsedCommand pc;
    memset(&pc, 0, sizeof(pc));

    /* 最初の空白で分割 */
    const char *space = strchr(input, ' ');
    if (space == NULL) {
        strncpy(pc.command, input, sizeof(pc.command) - 1);
    } else {
        int cmd_len = (int)(space - input);
        if (cmd_len >= (int)sizeof(pc.command)) cmd_len = sizeof(pc.command) - 1;
        strncpy(pc.command, input, cmd_len);
        /* 引数部分（先頭の空白をスキップ） */
        while (*space == ' ') space++;
        strncpy(pc.arg, space, sizeof(pc.arg) - 1);
    }
    return pc;
}

/* --- 優先度のカラー表示 --- */

const char *priority_color_label(int p) {
    switch (p) {
        case 1: return COLOR_DIM "[低]" COLOR_RESET;
        case 2: return COLOR_YELLOW "[中]" COLOR_RESET;
        case 3: return COLOR_RED "[高]" COLOR_RESET;
        default: return "[?]";
    }
}

/* --- リスト管理（基本版と同一のため省略）--- */

TodoList *todo_create(void) {
    TodoList *list = (TodoList *)malloc(sizeof(TodoList));
    if (list == NULL) return NULL;
    list->tasks = (Task *)malloc(sizeof(Task) * INITIAL_CAPACITY);
    if (list->tasks == NULL) { free(list); return NULL; }
    list->count = 0;
    list->capacity = INITIAL_CAPACITY;
    list->next_id = 1;
    return list;
}

void todo_destroy(TodoList *list) {
    if (list) { free(list->tasks); free(list); }
}

int todo_ensure_capacity(TodoList *list) {
    if (list->count < list->capacity) return 1;
    int new_cap = list->capacity * 2;
    Task *nt = (Task *)realloc(list->tasks, sizeof(Task) * new_cap);
    if (nt == NULL) return 0;
    list->tasks = nt;
    list->capacity = new_cap;
    return 1;
}

int find_index_by_id(const TodoList *list, int id) {
    int i;
    for (i = 0; i < list->count; i++) {
        if (list->tasks[i].id == id) return i;
    }
    return -1;
}

/* --- done コマンド（引数対応版）--- */

void todo_set_done_cmd(TodoList *list, const char *arg, int done_flag) {
    char line[LINE_LEN];
    int id, idx;

    if (strlen(arg) > 0) {
        /* 引数から直接IDを取得 */
        sscanf(arg, "%d", &id);
    } else {
        printf("タスク番号: ");
        fgets(line, sizeof(line), stdin);
        if (sscanf(line, "%d", &id) != 1) {
            printf("数字を入力してください。\n");
            return;
        }
    }

    idx = find_index_by_id(list, id);
    if (idx < 0) {
        printf("タスク #%d が見つかりません。\n", id);
        return;
    }

    list->tasks[idx].done = done_flag;
    printf("%sタスク #%d を%sにしました: %s%s\n",
           done_flag ? COLOR_GREEN : COLOR_YELLOW,
           id,
           done_flag ? "完了" : "未完了",
           list->tasks[idx].title,
           COLOR_RESET);
}

/* --- カラー付き一覧表示 --- */

void todo_list_color(const TodoList *list) {
    int i;
    if (list->count == 0) {
        printf("タスクがありません。\n");
        return;
    }

    printf("\n--- TODOリスト (%d件) ---\n", list->count);
    printf(" #  状態  優先度  期限        タスク名\n");
    printf("-----------------------------------------------------\n");
    for (i = 0; i < list->count; i++) {
        const Task *t = &list->tasks[i];
        if (t->done) {
            printf(COLOR_DIM);
        }
        printf("%2d. [%s]   %s    %-10s  %s",
               t->id,
               t->done ? COLOR_GREEN "x" COLOR_RESET : " ",
               priority_color_label(t->priority),
               strlen(t->deadline) > 0 ? t->deadline : "(なし)    ",
               t->title);
        if (t->done) {
            printf(COLOR_RESET);
        }
        printf("\n");
    }
}

int main(void) {
    TodoList *list = todo_create();
    char input[LINE_LEN];

    if (list == NULL) { printf("初期化失敗\n"); return 1; }

    printf(COLOR_CYAN "===== TODO リスト管理ツール（改良版）=====" COLOR_RESET "\n");
    printf("'help' でコマンド一覧を表示\n");
    printf("'done 3' のようにコマンドと引数を1行で入力できます\n");

    while (1) {
        printf("\n" COLOR_CYAN "> " COLOR_RESET);
        fgets(input, sizeof(input), stdin);
        input[strcspn(input, "\n")] = '\0';
        if (strlen(input) == 0) continue;

        ParsedCommand pc = parse_input(input);

        if (strcmp(pc.command, "quit") == 0 || strcmp(pc.command, "q") == 0) {
            printf("終了します。\n");
            break;
        } else if (strcmp(pc.command, "list") == 0 || strcmp(pc.command, "ls") == 0) {
            todo_list_color(list);
        } else if (strcmp(pc.command, "done") == 0) {
            todo_set_done_cmd(list, pc.arg, 1);
        } else if (strcmp(pc.command, "undone") == 0) {
            todo_set_done_cmd(list, pc.arg, 0);
        }
        /* ... 他のコマンドも同様に pc.arg を活用 ... */
    }

    todo_destroy(list);
    return 0;
}
```

**初心者向けとの違い:**
- コマンドと引数を1行で入力可能 → `done 3` のように効率的に操作できる
- `ParsedCommand` 構造体でコマンドパーサーを分離 → コマンド追加が容易
- ANSIカラーコードで視覚的に分かりやすい → 優先度や完了状態が一目で判別可能
- `COLOR_DIM` で完了タスクをグレーアウト → 未完了タスクに集中しやすい

> **注意**: ANSIカラーコードは多くのターミナルで動作しますが、Windows のコマンドプロンプト（レガシーモード）では動作しない場合があります。Windows Terminal や Git Bash では正常に表示されます。

</details>

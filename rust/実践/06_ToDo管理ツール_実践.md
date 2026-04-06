# 実践課題06：ToDo管理ツール ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第4章（ベクタと文字列）、第5章（関数とクロージャ）、第6章（構造体と列挙型）
> **課題の種類**: ミニプロジェクト
> **学習目標**: 構造体と列挙型を使ったデータモデル設計を実践し、メソッドでCRUD操作を実装する

---

## 完成イメージ

```
===== ToDo管理ツール =====

[1]追加 [2]一覧 [3]完了 [4]削除 [5]フィルタ [6]統計 [7]終了
操作: 1
タイトル: Rustの勉強
優先度 (1:低 2:中 3:高): 3
「Rustの勉強」を追加しました。(優先度: 高)

[1]追加 [2]一覧 [3]完了 [4]削除 [5]フィルタ [6]統計 [7]終了
操作: 2

--- ToDo一覧 ---
 1. [ ] Rustの勉強          (高)
 2. [ ] 買い物              (中)
 3. [x] メール返信          (低)

[1]追加 [2]一覧 [3]完了 [4]削除 [5]フィルタ [6]統計 [7]終了
操作: 5
フィルタ (1:未完了のみ 2:完了のみ 3:高優先度): 1

--- 未完了のタスク ---
 1. [ ] Rustの勉強          (高)
 2. [ ] 買い物              (中)

[1]追加 [2]一覧 [3]完了 [4]削除 [5]フィルタ [6]統計 [7]終了
操作: 6

--- 統計 ---
総タスク数: 3
未完了: 2
完了: 1
高優先度（未完了）: 1
```

---

## 課題の要件

1. タスクはタイトル・優先度（高/中/低）・完了状態を持つ
2. 以下のメニュー操作を実装する：
   - **追加**: タイトルと優先度を入力してタスク登録
   - **一覧**: 全タスクを番号付きで表示
   - **完了**: 指定番号のタスクを完了にする
   - **削除**: 指定番号のタスクを削除する
   - **フィルタ**: 条件に合うタスクだけを表示する
   - **統計**: タスクの集計情報を表示する
   - **終了**: プログラムを終了する
3. 優先度は列挙型（enum）で定義する
4. タスクは構造体（struct）で定義し、メソッドを実装する

---

## ステップガイド

<details>
<summary>ステップ1：データモデルを定義する</summary>

優先度を列挙型で、タスクを構造体で定義します。

```rust
/// 優先度（priority）を表す列挙型
enum Priority {
    Low,
    Medium,
    High,
}

/// タスクを表す構造体
struct Task {
    title: String,
    priority: Priority,
    done: bool,
}
```

</details>

<details>
<summary>ステップ2：構造体にメソッドを実装する</summary>

`impl` ブロックで表示用のメソッドを追加します。

```rust
impl Priority {
    fn label(&self) -> &'static str {
        match self {
            Priority::Low => "低",
            Priority::Medium => "中",
            Priority::High => "高",
        }
    }
}

impl Task {
    fn new(title: String, priority: Priority) -> Task {
        Task { title, priority, done: false }
    }

    fn status_icon(&self) -> &'static str {
        if self.done { "[x]" } else { "[ ]" }
    }
}
```

</details>

<details>
<summary>ステップ3：フィルタ処理にクロージャを活用する</summary>

`Vec::iter().filter()` にクロージャを渡してフィルタリングします。

```rust
let incomplete: Vec<&Task> = tasks.iter().filter(|t| !t.done).collect();
let high_priority: Vec<&Task> = tasks.iter().filter(|t| {
    matches!(t.priority, Priority::High) && !t.done
}).collect();
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```rust
// ToDo管理ツール
// 学べる内容：構造体、列挙型、Vec、match、メソッド
// 実行方法：rustc main.rs && ./main

use std::io;
use std::io::Write;

enum Priority {
    Low,
    Medium,
    High,
}

impl Priority {
    fn label(&self) -> &'static str {
        match self {
            Priority::Low => "低",
            Priority::Medium => "中",
            Priority::High => "高",
        }
    }

    fn from_input(input: &str) -> Option<Priority> {
        match input {
            "1" => Some(Priority::Low),
            "2" => Some(Priority::Medium),
            "3" => Some(Priority::High),
            _ => None,
        }
    }
}

struct Task {
    title: String,
    priority: Priority,
    done: bool,
}

impl Task {
    fn new(title: String, priority: Priority) -> Task {
        Task {
            title,
            priority,
            done: false,
        }
    }

    fn status_icon(&self) -> &'static str {
        if self.done {
            "[x]"
        } else {
            "[ ]"
        }
    }

    fn display(&self, index: usize) {
        println!(
            " {}. {} {:<20} ({})",
            index,
            self.status_icon(),
            self.title,
            self.priority.label()
        );
    }
}

fn read_input(prompt: &str) -> String {
    print!("{}", prompt);
    io::stdout().flush().unwrap();
    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("入力エラー");
    input.trim().to_string()
}

fn main() {
    println!("===== ToDo管理ツール =====");

    let mut tasks: Vec<Task> = Vec::new();

    loop {
        println!("\n[1]追加 [2]一覧 [3]完了 [4]削除 [5]フィルタ [6]統計 [7]終了");
        let choice = read_input("操作: ");

        match choice.as_str() {
            "1" => {
                // 追加
                let title = read_input("タイトル: ");
                let priority_input = read_input("優先度 (1:低 2:中 3:高): ");
                match Priority::from_input(&priority_input) {
                    Some(priority) => {
                        println!(
                            "「{}」を追加しました。(優先度: {})",
                            title,
                            priority.label()
                        );
                        tasks.push(Task::new(title, priority));
                    }
                    None => println!("無効な優先度です。"),
                }
            }
            "2" => {
                // 一覧
                if tasks.is_empty() {
                    println!("タスクがありません。");
                    continue;
                }
                println!("\n--- ToDo一覧 ---");
                for (i, task) in tasks.iter().enumerate() {
                    task.display(i + 1);
                }
            }
            "3" => {
                // 完了にする
                if tasks.is_empty() {
                    println!("タスクがありません。");
                    continue;
                }
                let num_str = read_input("完了にする番号: ");
                match num_str.parse::<usize>() {
                    Ok(num) if num >= 1 && num <= tasks.len() => {
                        tasks[num - 1].done = true;
                        println!("「{}」を完了にしました。", tasks[num - 1].title);
                    }
                    _ => println!("無効な番号です。"),
                }
            }
            "4" => {
                // 削除
                if tasks.is_empty() {
                    println!("タスクがありません。");
                    continue;
                }
                let num_str = read_input("削除する番号: ");
                match num_str.parse::<usize>() {
                    Ok(num) if num >= 1 && num <= tasks.len() => {
                        let removed = tasks.remove(num - 1);
                        println!("「{}」を削除しました。", removed.title);
                    }
                    _ => println!("無効な番号です。"),
                }
            }
            "5" => {
                // フィルタ
                let filter = read_input("フィルタ (1:未完了のみ 2:完了のみ 3:高優先度): ");
                let filtered: Vec<(usize, &Task)> = tasks
                    .iter()
                    .enumerate()
                    .filter(|(_, t)| match filter.as_str() {
                        "1" => !t.done,
                        "2" => t.done,
                        "3" => matches!(t.priority, Priority::High) && !t.done,
                        _ => true,
                    })
                    .collect();

                let label = match filter.as_str() {
                    "1" => "未完了のタスク",
                    "2" => "完了のタスク",
                    "3" => "高優先度（未完了）のタスク",
                    _ => "全タスク",
                };

                if filtered.is_empty() {
                    println!("{}はありません。", label);
                } else {
                    println!("\n--- {} ---", label);
                    for (i, (_, task)) in filtered.iter().enumerate() {
                        task.display(i + 1);
                    }
                }
            }
            "6" => {
                // 統計
                let total = tasks.len();
                let done_count = tasks.iter().filter(|t| t.done).count();
                let incomplete = total - done_count;
                let high_incomplete = tasks
                    .iter()
                    .filter(|t| matches!(t.priority, Priority::High) && !t.done)
                    .count();

                println!("\n--- 統計 ---");
                println!("総タスク数: {}", total);
                println!("未完了: {}", incomplete);
                println!("完了: {}", done_count);
                println!("高優先度（未完了）: {}", high_incomplete);
            }
            "7" => {
                println!("終了します。");
                break;
            }
            _ => println!("無効な操作です。"),
        }
    }
}
```

</details>

<details>
<summary>解答例（改良版 ─ TodoAppに機能を集約）</summary>

```rust
// ToDo管理ツール（改良版）
// 管理ロジックを構造体に集約したバージョン
// 実行方法：rustc main.rs && ./main

use std::io;
use std::io::Write;

#[derive(Clone)]
enum Priority {
    Low,
    Medium,
    High,
}

impl Priority {
    fn label(&self) -> &'static str {
        match self {
            Priority::Low => "低",
            Priority::Medium => "中",
            Priority::High => "高",
        }
    }

    fn from_input(input: &str) -> Option<Priority> {
        match input {
            "1" => Some(Priority::Low),
            "2" => Some(Priority::Medium),
            "3" => Some(Priority::High),
            _ => None,
        }
    }
}

struct Task {
    title: String,
    priority: Priority,
    done: bool,
}

impl Task {
    fn new(title: String, priority: Priority) -> Task {
        Task { title, priority, done: false }
    }

    fn format_line(&self, index: usize) -> String {
        let icon = if self.done { "[x]" } else { "[ ]" };
        format!(
            " {}. {} {:<20} ({})",
            index,
            icon,
            self.title,
            self.priority.label()
        )
    }
}

/// ToDo管理のロジックをまとめた構造体
struct TodoApp {
    tasks: Vec<Task>,
}

impl TodoApp {
    fn new() -> TodoApp {
        TodoApp { tasks: Vec::new() }
    }

    fn add(&mut self, title: String, priority: Priority) {
        println!("「{}」を追加しました。(優先度: {})", title, priority.label());
        self.tasks.push(Task::new(title, priority));
    }

    fn show_all(&self) {
        if self.tasks.is_empty() {
            println!("タスクがありません。");
            return;
        }
        println!("\n--- ToDo一覧 ---");
        for (i, task) in self.tasks.iter().enumerate() {
            println!("{}", task.format_line(i + 1));
        }
    }

    fn complete(&mut self, num: usize) -> Result<(), String> {
        if num < 1 || num > self.tasks.len() {
            return Err("無効な番号です。".to_string());
        }
        self.tasks[num - 1].done = true;
        println!("「{}」を完了にしました。", self.tasks[num - 1].title);
        Ok(())
    }

    fn delete(&mut self, num: usize) -> Result<(), String> {
        if num < 1 || num > self.tasks.len() {
            return Err("無効な番号です。".to_string());
        }
        let removed = self.tasks.remove(num - 1);
        println!("「{}」を削除しました。", removed.title);
        Ok(())
    }

    fn filter_and_show(&self, filter_type: &str) {
        let (label, predicate): (&str, Box<dyn Fn(&&Task) -> bool>) = match filter_type {
            "1" => ("未完了のタスク", Box::new(|t: &&Task| !t.done)),
            "2" => ("完了のタスク", Box::new(|t: &&Task| t.done)),
            "3" => (
                "高優先度（未完了）のタスク",
                Box::new(|t: &&Task| matches!(t.priority, Priority::High) && !t.done),
            ),
            _ => {
                println!("無効なフィルタです。");
                return;
            }
        };

        let filtered: Vec<&Task> = self.tasks.iter().filter(predicate).collect();

        if filtered.is_empty() {
            println!("{}はありません。", label);
        } else {
            println!("\n--- {} ---", label);
            for (i, task) in filtered.iter().enumerate() {
                println!("{}", task.format_line(i + 1));
            }
        }
    }

    fn show_stats(&self) {
        let total = self.tasks.len();
        let done = self.tasks.iter().filter(|t| t.done).count();
        let high_incomplete = self
            .tasks
            .iter()
            .filter(|t| matches!(t.priority, Priority::High) && !t.done)
            .count();

        println!("\n--- 統計 ---");
        println!("総タスク数: {}", total);
        println!("未完了: {}", total - done);
        println!("完了: {}", done);
        println!("高優先度（未完了）: {}", high_incomplete);
    }
}

fn read_input(prompt: &str) -> String {
    print!("{}", prompt);
    io::stdout().flush().unwrap();
    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("入力エラー");
    input.trim().to_string()
}

fn main() {
    println!("===== ToDo管理ツール =====");
    let mut app = TodoApp::new();

    loop {
        println!("\n[1]追加 [2]一覧 [3]完了 [4]削除 [5]フィルタ [6]統計 [7]終了");
        let choice = read_input("操作: ");

        match choice.as_str() {
            "1" => {
                let title = read_input("タイトル: ");
                let p = read_input("優先度 (1:低 2:中 3:高): ");
                match Priority::from_input(&p) {
                    Some(priority) => app.add(title, priority),
                    None => println!("無効な優先度です。"),
                }
            }
            "2" => app.show_all(),
            "3" => {
                let n = read_input("完了にする番号: ");
                if let Ok(num) = n.parse::<usize>() {
                    if let Err(e) = app.complete(num) {
                        println!("{}", e);
                    }
                } else {
                    println!("数値を入力してください。");
                }
            }
            "4" => {
                let n = read_input("削除する番号: ");
                if let Ok(num) = n.parse::<usize>() {
                    if let Err(e) = app.delete(num) {
                        println!("{}", e);
                    }
                } else {
                    println!("数値を入力してください。");
                }
            }
            "5" => {
                let f = read_input("フィルタ (1:未完了のみ 2:完了のみ 3:高優先度): ");
                app.filter_and_show(&f);
            }
            "6" => app.show_stats(),
            "7" => {
                println!("終了します。");
                break;
            }
            _ => println!("無効な操作です。"),
        }
    }
}
```

**初心者向けとの違い:**
- `TodoApp` 構造体にすべての操作を集約 → `main()` が薄くシンプルに
- `Result` 型でエラーを呼び出し元に返す設計 → エラー処理の責務が明確
- `Box<dyn Fn>` でクロージャを変数に格納し、フィルタロジックを動的に切り替え
- `format_line()` で表示フォーマットを一元化 → 表示変更が1箇所で済む

</details>

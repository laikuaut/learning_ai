# 実践課題11：CLIタスク管理アプリ ★5

> **難易度**: ★★★★★（総合）
> **前提知識**: 第1章〜第8章（全章の知識を総合的に活用）
> **課題の種類**: ミニプロジェクト（実務レベル）
> **学習目標**: Rustの全知識を組み合わせ、ファイル永続化・カスタムエラー型・モジュール分割を含む実践的なCLIアプリを設計・実装する

---

## 完成イメージ

```
===== タスク管理アプリ =====
データファイル: tasks.csv

[1]追加 [2]一覧 [3]完了 [4]未完了に戻す [5]削除 [6]検索 [7]ソート [8]統計 [9]エクスポート [0]終了
操作: 1
タイトル: Rustの所有権を復習する
カテゴリ (1:仕事 2:勉強 3:プライベート): 2
優先度 (1:低 2:中 3:高): 3
期限 (例: 2024-04-30, 空欄でスキップ): 2024-04-15
タスク「Rustの所有権を復習する」を追加しました。[ID: 1]

操作: 2
--- タスク一覧 (全3件) ---
 ID  状態  優先度  カテゴリ    期限        タイトル
  1  [ ]   ★★★  勉強       2024-04-15  Rustの所有権を復習する
  2  [x]   ★☆☆  仕事       2024-04-20  週報を書く
  3  [ ]   ★★☆  プライベート  --          部屋の掃除

操作: 7
ソート基準 (1:優先度 2:期限 3:カテゴリ 4:状態): 1

--- タスク一覧 (優先度順, 全3件) ---
 ID  状態  優先度  カテゴリ    期限        タイトル
  1  [ ]   ★★★  勉強       2024-04-15  Rustの所有権を復習する
  3  [ ]   ★★☆  プライベート  --          部屋の掃除
  2  [x]   ★☆☆  仕事       2024-04-20  週報を書く

操作: 8
--- 統計 ---
全タスク: 3件
  完了: 1件 (33.3%)
  未完了: 2件 (66.7%)
カテゴリ別:
  仕事: 1件 (完了: 1)
  勉強: 1件 (完了: 0)
  プライベート: 1件 (完了: 0)

操作: 9
tasks_export.csv に3件のタスクをエクスポートしました。

操作: 0
データを保存しました。終了します。
```

---

## 課題の要件

### 基本機能
1. タスクの追加（タイトル・カテゴリ・優先度・期限）
2. タスク一覧の表示
3. タスクの完了/未完了の切り替え
4. タスクの削除
5. タスクの検索（タイトル・カテゴリで部分一致）
6. ソート（優先度・期限・カテゴリ・状態）
7. 統計情報の表示
8. CSV形式でのエクスポート

### 技術要件
- 各タスクにユニークなID（自動採番）を付与する
- CSVファイルにデータを保存・読み込みする（永続化）
- カスタムエラー型を定義し、`Result` でエラーを伝播する
- 列挙型でカテゴリ・優先度・状態を型安全に管理する
- 構造体とメソッドでデータモデルを設計する

---

## ステップガイド

<details>
<summary>ステップ1：データモデルを定義する</summary>

```rust
use std::fmt;

#[derive(Clone, PartialEq)]
enum Category {
    Work,
    Study,
    Personal,
}

impl Category {
    fn label(&self) -> &'static str {
        match self {
            Category::Work => "仕事",
            Category::Study => "勉強",
            Category::Personal => "プライベート",
        }
    }

    fn from_input(s: &str) -> Option<Category> {
        match s {
            "1" => Some(Category::Work),
            "2" => Some(Category::Study),
            "3" => Some(Category::Personal),
            _ => None,
        }
    }

    fn to_csv(&self) -> &'static str {
        match self {
            Category::Work => "work",
            Category::Study => "study",
            Category::Personal => "personal",
        }
    }

    fn from_csv(s: &str) -> Option<Category> {
        match s {
            "work" => Some(Category::Work),
            "study" => Some(Category::Study),
            "personal" => Some(Category::Personal),
            _ => None,
        }
    }
}

#[derive(Clone, PartialEq, PartialOrd, Ord, Eq)]
enum Priority {
    Low,
    Medium,
    High,
}

struct Task {
    id: u32,
    title: String,
    category: Category,
    priority: Priority,
    deadline: Option<String>,
    done: bool,
}
```

</details>

<details>
<summary>ステップ2：カスタムエラー型を定義する</summary>

複数のエラー種別を統一的に扱うため、カスタムエラー型を作ります。

```rust
enum AppError {
    IoError(std::io::Error),
    ParseError(String),
    NotFound(String),
    InvalidInput(String),
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AppError::IoError(e) => write!(f, "IOエラー: {}", e),
            AppError::ParseError(msg) => write!(f, "解析エラー: {}", msg),
            AppError::NotFound(msg) => write!(f, "見つかりません: {}", msg),
            AppError::InvalidInput(msg) => write!(f, "無効な入力: {}", msg),
        }
    }
}

impl From<std::io::Error> for AppError {
    fn from(error: std::io::Error) -> AppError {
        AppError::IoError(error)
    }
}
```

</details>

<details>
<summary>ステップ3：ファイル永続化を実装する</summary>

CSV形式でタスクを保存・読み込みします。

```rust
use std::fs;

fn save_to_csv(tasks: &[Task], filename: &str) -> Result<(), AppError> {
    let mut content = String::from("id,title,category,priority,deadline,done\n");
    for task in tasks {
        let deadline = task.deadline.as_deref().unwrap_or("");
        content.push_str(&format!(
            "{},{},{},{},{},{}\n",
            task.id,
            task.title,
            task.category.to_csv(),
            task.priority.to_csv(),
            deadline,
            task.done
        ));
    }
    fs::write(filename, content)?;
    Ok(())
}
```

</details>

<details>
<summary>ステップ4：TaskManagerに操作を集約する</summary>

```rust
struct TaskManager {
    tasks: Vec<Task>,
    next_id: u32,
    filename: String,
}

impl TaskManager {
    fn new(filename: &str) -> TaskManager {
        TaskManager {
            tasks: Vec::new(),
            next_id: 1,
            filename: filename.to_string(),
        }
    }

    fn add(&mut self, title: String, category: Category, priority: Priority, deadline: Option<String>) -> u32 {
        let id = self.next_id;
        self.next_id += 1;
        self.tasks.push(Task { id, title, category, priority, deadline, done: false });
        id
    }

    // ... 他の操作メソッド
}
```

</details>

---

## 解答例

<details>
<summary>解答例（完全版）</summary>

```rust
// CLIタスク管理アプリ
// 学べる内容：構造体、列挙型、Result、カスタムエラー型、ファイルI/O、CSV解析
// 実行方法：rustc task_manager.rs && ./task_manager

use std::collections::HashMap;
use std::fmt;
use std::fs;
use std::io;
use std::io::Write;

// ==================== エラー型 ====================

enum AppError {
    IoError(io::Error),
    ParseError(String),
    NotFound(String),
    InvalidInput(String),
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AppError::IoError(e) => write!(f, "IOエラー: {}", e),
            AppError::ParseError(msg) => write!(f, "解析エラー: {}", msg),
            AppError::NotFound(msg) => write!(f, "見つかりません: {}", msg),
            AppError::InvalidInput(msg) => write!(f, "無効な入力: {}", msg),
        }
    }
}

impl From<io::Error> for AppError {
    fn from(error: io::Error) -> AppError {
        AppError::IoError(error)
    }
}

// ==================== データモデル ====================

#[derive(Clone, PartialEq)]
enum Category {
    Work,
    Study,
    Personal,
}

impl Category {
    fn label(&self) -> &'static str {
        match self {
            Category::Work => "仕事",
            Category::Study => "勉強",
            Category::Personal => "プライベート",
        }
    }

    fn from_input(s: &str) -> Option<Category> {
        match s {
            "1" => Some(Category::Work),
            "2" => Some(Category::Study),
            "3" => Some(Category::Personal),
            _ => None,
        }
    }

    fn to_csv(&self) -> &'static str {
        match self {
            Category::Work => "work",
            Category::Study => "study",
            Category::Personal => "personal",
        }
    }

    fn from_csv(s: &str) -> Option<Category> {
        match s {
            "work" => Some(Category::Work),
            "study" => Some(Category::Study),
            "personal" => Some(Category::Personal),
            _ => None,
        }
    }
}

#[derive(Clone, PartialEq, Eq, PartialOrd, Ord)]
enum Priority {
    Low = 1,
    Medium = 2,
    High = 3,
}

impl Priority {
    fn label(&self) -> &'static str {
        match self {
            Priority::Low => "★☆☆",
            Priority::Medium => "★★☆",
            Priority::High => "★★★",
        }
    }

    fn from_input(s: &str) -> Option<Priority> {
        match s {
            "1" => Some(Priority::Low),
            "2" => Some(Priority::Medium),
            "3" => Some(Priority::High),
            _ => None,
        }
    }

    fn to_csv(&self) -> &'static str {
        match self {
            Priority::Low => "low",
            Priority::Medium => "medium",
            Priority::High => "high",
        }
    }

    fn from_csv(s: &str) -> Option<Priority> {
        match s {
            "low" => Some(Priority::Low),
            "medium" => Some(Priority::Medium),
            "high" => Some(Priority::High),
            _ => None,
        }
    }
}

struct Task {
    id: u32,
    title: String,
    category: Category,
    priority: Priority,
    deadline: Option<String>,
    done: bool,
}

impl Task {
    fn display_line(&self) {
        let status = if self.done { "[x]" } else { "[ ]" };
        let deadline = match &self.deadline {
            Some(d) => d.as_str(),
            None => "--",
        };
        println!(
            " {:>3}  {}  {}  {:<12} {:<10}  {}",
            self.id,
            status,
            self.priority.label(),
            self.category.label(),
            deadline,
            self.title
        );
    }

    fn to_csv_line(&self) -> String {
        let deadline = match &self.deadline {
            Some(d) => d.clone(),
            None => String::new(),
        };
        format!(
            "{},{},{},{},{},{}",
            self.id, self.title, self.category.to_csv(),
            self.priority.to_csv(), deadline, self.done
        )
    }

    fn from_csv_line(line: &str) -> Result<Task, AppError> {
        let parts: Vec<&str> = line.splitn(6, ',').collect();
        if parts.len() != 6 {
            return Err(AppError::ParseError(format!("不正なCSV行: {}", line)));
        }

        let id: u32 = parts[0]
            .parse()
            .map_err(|_| AppError::ParseError("IDの解析エラー".to_string()))?;
        let title = parts[1].to_string();
        let category = Category::from_csv(parts[2])
            .ok_or_else(|| AppError::ParseError(format!("不明なカテゴリ: {}", parts[2])))?;
        let priority = Priority::from_csv(parts[3])
            .ok_or_else(|| AppError::ParseError(format!("不明な優先度: {}", parts[3])))?;
        let deadline = if parts[4].is_empty() {
            None
        } else {
            Some(parts[4].to_string())
        };
        let done: bool = parts[5]
            .parse()
            .map_err(|_| AppError::ParseError("完了状態の解析エラー".to_string()))?;

        Ok(Task {
            id,
            title,
            category,
            priority,
            deadline,
            done,
        })
    }
}

// ==================== タスクマネージャ ====================

struct TaskManager {
    tasks: Vec<Task>,
    next_id: u32,
    filename: String,
}

impl TaskManager {
    fn new(filename: &str) -> TaskManager {
        TaskManager {
            tasks: Vec::new(),
            next_id: 1,
            filename: filename.to_string(),
        }
    }

    fn load(&mut self) -> Result<(), AppError> {
        let content = match fs::read_to_string(&self.filename) {
            Ok(c) => c,
            Err(e) if e.kind() == io::ErrorKind::NotFound => return Ok(()),
            Err(e) => return Err(AppError::IoError(e)),
        };

        let mut max_id: u32 = 0;
        for (i, line) in content.lines().enumerate() {
            if i == 0 {
                continue; // ヘッダ行をスキップ
            }
            if line.trim().is_empty() {
                continue;
            }
            let task = Task::from_csv_line(line)?;
            if task.id > max_id {
                max_id = task.id;
            }
            self.tasks.push(task);
        }
        self.next_id = max_id + 1;
        Ok(())
    }

    fn save(&self) -> Result<(), AppError> {
        let mut content = String::from("id,title,category,priority,deadline,done\n");
        for task in &self.tasks {
            content.push_str(&task.to_csv_line());
            content.push('\n');
        }
        fs::write(&self.filename, content)?;
        Ok(())
    }

    fn add(
        &mut self,
        title: String,
        category: Category,
        priority: Priority,
        deadline: Option<String>,
    ) -> u32 {
        let id = self.next_id;
        self.next_id += 1;
        self.tasks.push(Task {
            id,
            title,
            category,
            priority,
            deadline,
            done: false,
        });
        id
    }

    fn find_index_by_id(&self, id: u32) -> Option<usize> {
        self.tasks.iter().position(|t| t.id == id)
    }

    fn toggle_done(&mut self, id: u32, done: bool) -> Result<(), AppError> {
        let index = self
            .find_index_by_id(id)
            .ok_or_else(|| AppError::NotFound(format!("ID {} のタスク", id)))?;
        self.tasks[index].done = done;
        Ok(())
    }

    fn delete(&mut self, id: u32) -> Result<String, AppError> {
        let index = self
            .find_index_by_id(id)
            .ok_or_else(|| AppError::NotFound(format!("ID {} のタスク", id)))?;
        let removed = self.tasks.remove(index);
        Ok(removed.title)
    }

    fn search(&self, keyword: &str) -> Vec<&Task> {
        self.tasks
            .iter()
            .filter(|t| t.title.contains(keyword) || t.category.label().contains(keyword))
            .collect()
    }

    fn sorted_tasks(&self, sort_by: &str) -> Vec<&Task> {
        let mut sorted: Vec<&Task> = self.tasks.iter().collect();
        match sort_by {
            "1" => sorted.sort_by(|a, b| b.priority.cmp(&a.priority)),
            "2" => sorted.sort_by(|a, b| {
                let da = a.deadline.as_deref().unwrap_or("9999-99-99");
                let db = b.deadline.as_deref().unwrap_or("9999-99-99");
                da.cmp(db)
            }),
            "3" => sorted.sort_by(|a, b| a.category.label().cmp(b.category.label())),
            "4" => sorted.sort_by_key(|t| t.done),
            _ => {}
        }
        sorted
    }

    fn show_stats(&self) {
        let total = self.tasks.len();
        if total == 0 {
            println!("タスクがありません。");
            return;
        }

        let done_count = self.tasks.iter().filter(|t| t.done).count();
        let incomplete = total - done_count;

        println!("\n--- 統計 ---");
        println!("全タスク: {}件", total);
        println!(
            "  完了: {}件 ({:.1}%)",
            done_count,
            done_count as f64 / total as f64 * 100.0
        );
        println!(
            "  未完了: {}件 ({:.1}%)",
            incomplete,
            incomplete as f64 / total as f64 * 100.0
        );

        // カテゴリ別
        let mut cat_stats: HashMap<String, (usize, usize)> = HashMap::new();
        for task in &self.tasks {
            let entry = cat_stats
                .entry(task.category.label().to_string())
                .or_insert((0, 0));
            entry.0 += 1;
            if task.done {
                entry.1 += 1;
            }
        }

        println!("カテゴリ別:");
        let mut sorted_cats: Vec<(&String, &(usize, usize))> = cat_stats.iter().collect();
        sorted_cats.sort_by(|a, b| b.1 .0.cmp(&a.1 .0));
        for (cat, (count, done)) in sorted_cats {
            println!("  {}: {}件 (完了: {})", cat, count, done);
        }
    }

    fn export(&self, filename: &str) -> Result<usize, AppError> {
        let mut content = String::from("id,title,category,priority,deadline,done\n");
        for task in &self.tasks {
            content.push_str(&task.to_csv_line());
            content.push('\n');
        }
        fs::write(filename, content)?;
        Ok(self.tasks.len())
    }
}

// ==================== 入力ヘルパー ====================

fn read_input(prompt: &str) -> String {
    print!("{}", prompt);
    io::stdout().flush().unwrap();
    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("入力エラー");
    input.trim().to_string()
}

fn read_u32(prompt: &str) -> Result<u32, AppError> {
    let input = read_input(prompt);
    input
        .parse()
        .map_err(|_| AppError::InvalidInput("整数を入力してください。".to_string()))
}

fn show_task_list(tasks: &[&Task], header: &str) {
    println!("\n--- {} (全{}件) ---", header, tasks.len());
    println!(
        " {:>3}  {:^4}  {:^5}  {:<12} {:<10}  {}",
        "ID", "状態", "優先度", "カテゴリ", "期限", "タイトル"
    );
    for task in tasks {
        task.display_line();
    }
}

// ==================== メイン ====================

fn main() {
    let data_file = "tasks.csv";
    println!("===== タスク管理アプリ =====");
    println!("データファイル: {}", data_file);

    let mut manager = TaskManager::new(data_file);

    // ファイルからロード
    match manager.load() {
        Ok(()) => {}
        Err(e) => println!("警告: データ読み込みエラー: {}", e),
    }

    loop {
        println!(
            "\n[1]追加 [2]一覧 [3]完了 [4]未完了に戻す [5]削除 [6]検索 [7]ソート [8]統計 [9]エクスポート [0]終了"
        );
        let choice = read_input("操作: ");

        match choice.as_str() {
            "1" => {
                let title = read_input("タイトル: ");
                if title.is_empty() {
                    println!("タイトルを入力してください。");
                    continue;
                }
                let cat_input = read_input("カテゴリ (1:仕事 2:勉強 3:プライベート): ");
                let category = match Category::from_input(&cat_input) {
                    Some(c) => c,
                    None => {
                        println!("無効なカテゴリです。");
                        continue;
                    }
                };
                let pri_input = read_input("優先度 (1:低 2:中 3:高): ");
                let priority = match Priority::from_input(&pri_input) {
                    Some(p) => p,
                    None => {
                        println!("無効な優先度です。");
                        continue;
                    }
                };
                let deadline_input =
                    read_input("期限 (例: 2024-04-30, 空欄でスキップ): ");
                let deadline = if deadline_input.is_empty() {
                    None
                } else {
                    Some(deadline_input)
                };

                let id = manager.add(title.clone(), category, priority, deadline);
                println!("タスク「{}」を追加しました。[ID: {}]", title, id);
            }
            "2" => {
                if manager.tasks.is_empty() {
                    println!("タスクがありません。");
                    continue;
                }
                let tasks: Vec<&Task> = manager.tasks.iter().collect();
                show_task_list(&tasks, "タスク一覧");
            }
            "3" => {
                match read_u32("完了にするタスクID: ") {
                    Ok(id) => match manager.toggle_done(id, true) {
                        Ok(()) => println!("タスク [ID: {}] を完了にしました。", id),
                        Err(e) => println!("{}", e),
                    },
                    Err(e) => println!("{}", e),
                }
            }
            "4" => {
                match read_u32("未完了に戻すタスクID: ") {
                    Ok(id) => match manager.toggle_done(id, false) {
                        Ok(()) => println!("タスク [ID: {}] を未完了に戻しました。", id),
                        Err(e) => println!("{}", e),
                    },
                    Err(e) => println!("{}", e),
                }
            }
            "5" => {
                match read_u32("削除するタスクID: ") {
                    Ok(id) => match manager.delete(id) {
                        Ok(title) => println!("タスク「{}」を削除しました。", title),
                        Err(e) => println!("{}", e),
                    },
                    Err(e) => println!("{}", e),
                }
            }
            "6" => {
                let keyword = read_input("検索キーワード: ");
                let results = manager.search(&keyword);
                if results.is_empty() {
                    println!("見つかりませんでした。");
                } else {
                    show_task_list(&results, "検索結果");
                }
            }
            "7" => {
                let sort_key =
                    read_input("ソート基準 (1:優先度 2:期限 3:カテゴリ 4:状態): ");
                let sorted = manager.sorted_tasks(&sort_key);
                let label = match sort_key.as_str() {
                    "1" => "タスク一覧 (優先度順)",
                    "2" => "タスク一覧 (期限順)",
                    "3" => "タスク一覧 (カテゴリ順)",
                    "4" => "タスク一覧 (状態順)",
                    _ => "タスク一覧",
                };
                show_task_list(&sorted, label);
            }
            "8" => manager.show_stats(),
            "9" => {
                let export_file = "tasks_export.csv";
                match manager.export(export_file) {
                    Ok(count) => {
                        println!("{} に{}件のタスクをエクスポートしました。", export_file, count)
                    }
                    Err(e) => println!("エクスポートエラー: {}", e),
                }
            }
            "0" => {
                match manager.save() {
                    Ok(()) => println!("データを保存しました。終了します。"),
                    Err(e) => println!("保存エラー: {} 終了します。", e),
                }
                break;
            }
            _ => println!("無効な操作です。"),
        }
    }
}
```

</details>

<details>
<summary>設計のポイント解説</summary>

### 1. カスタムエラー型 `AppError`

複数のエラー種別（IO、パース、検索、入力）を1つの型にまとめ、`?` 演算子で伝播できるようにしています。`From<io::Error>` の実装により、`fs::write()` や `fs::read_to_string()` のエラーが自動的に `AppError` に変換されます。

### 2. CSV永続化

`Task::to_csv_line()` と `Task::from_csv_line()` をペアで実装し、保存と読み込みの整合性を保っています。`splitn(6, ',')` で最大6分割にしているのは、タイトルにカンマが含まれた場合の安全策です。

### 3. IDベースの管理

配列のインデックスではなくIDで管理することで、削除後にインデックスがずれる問題を回避しています。`find_index_by_id()` でIDからインデックスを解決します。

### 4. ソート戦略

`sorted_tasks()` は元のデータを変更せず、参照のベクタをソートして返します。これにより元データの順序を保ちつつ、異なる基準で表示できます。

### 5. `Option<String>` による期限管理

期限が任意（optional）であることを `Option<String>` で表現しています。ソート時は `unwrap_or("9999-99-99")` で期限なしのタスクを末尾に配置しています。

</details>

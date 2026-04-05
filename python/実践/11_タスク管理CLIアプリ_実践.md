# 実践課題11：タスク管理CLIアプリケーション ★5

> **難易度**: ★★★★★（総合）
> **前提知識**: 第1章〜第11章（全章の知識を総合的に活用）
> **課題の種類**: ミニプロジェクト（総合設計）
> **学習目標**: これまで学んだ全知識を統合し、実務レベルのCLIアプリケーションを設計・実装する

---

## 完成イメージ

```
===== タスク管理アプリ =====

[メニュー]
1. タスク追加     5. 優先度変更
2. タスク一覧     6. 統計表示
3. タスク完了     7. ファイル保存
4. タスク検索     8. ファイル読込
                  9. 終了

操作: 1
タスク名: レポート作成
期限 (YYYY-MM-DD): 2024-04-10
優先度 (1:低 2:中 3:高): 3
カテゴリ: 仕事
「レポート作成」を追加しました。（優先度:高）

操作: 2

--- タスク一覧 ---
 [未完了] 優先度順
 1. [高] レポート作成        期限:2024-04-10  カテゴリ:仕事    ⚠ 期限超過
 2. [中] 買い物              期限:2024-04-15  カテゴリ:生活    残り5日
 3. [低] 本を読む            期限:なし        カテゴリ:趣味

 [完了済み]
 ✓ プレゼン資料作成  (完了日:2024-04-03)

操作: 6

--- 統計 ---
合計: 4件 (未完了:3 / 完了:1)
完了率: 25.0%

カテゴリ別:
  仕事: 2件
  生活: 1件
  趣味: 1件

優先度別:
  高: 1件
  中: 1件
  低: 1件

期限超過タスク: 1件
  - レポート作成 (期限:2024-04-10)
```

---

## 課題の要件

### 必須機能

1. **タスク追加**: 名前・期限（任意）・優先度・カテゴリを入力
2. **タスク一覧**: 未完了を優先度順で表示、完了済みは別セクション
3. **タスク完了**: 番号指定で完了にする（完了日を記録）
4. **タスク検索**: キーワード・カテゴリ・優先度でフィルタ
5. **優先度変更**: 番号指定で優先度を変更
6. **統計表示**: 合計・完了率・カテゴリ別・優先度別・期限超過
7. **ファイル保存/読込**: JSON形式でタスクデータを永続化

### 設計要件

- **クラスを使うこと**: `Task` クラスと `TaskManager` クラスを設計する
- **エラー処理**: 不正入力でクラッシュしないこと
- **期限管理**: `datetime` モジュールで期限超過を判定する
- **ソート**: 優先度順（高→低）で一覧表示する

---

## ステップガイド

<details>
<summary>ステップ1：Task クラスを設計する</summary>

タスク1件のデータと振る舞いをクラスにまとめます。

```python
from datetime import datetime, date


class Task:
    PRIORITY_MAP = {1: "低", 2: "中", 3: "高"}

    def __init__(self, name, deadline=None, priority=2, category="未分類"):
        self.name = name
        self.deadline = deadline    # date型 または None
        self.priority = priority    # 1, 2, 3
        self.category = category
        self.done = False
        self.done_date = None
        self.created = date.today()

    def complete(self):
        """タスクを完了にする"""
        self.done = True
        self.done_date = date.today()

    def is_overdue(self):
        """期限超過かどうか"""
        if self.deadline and not self.done:
            return date.today() > self.deadline
        return False

    def priority_label(self):
        return self.PRIORITY_MAP.get(self.priority, "中")
```

</details>

<details>
<summary>ステップ2：TaskManager クラスを設計する</summary>

タスクの集合を管理し、各操作を提供します。

```python
class TaskManager:
    def __init__(self):
        self.tasks = []

    def add(self, task):
        self.tasks.append(task)

    def get_incomplete(self):
        """未完了タスクを優先度降順で返す"""
        incomplete = [t for t in self.tasks if not t.done]
        return sorted(incomplete, key=lambda t: t.priority, reverse=True)

    def get_completed(self):
        return [t for t in self.tasks if t.done]
```

</details>

<details>
<summary>ステップ3：JSON保存/読込を実装する</summary>

`json` モジュールで辞書のリストとして保存します。
`date` 型はJSON化できないので、文字列に変換します。

```python
import json

def save_tasks(self, filename):
    data = []
    for task in self.tasks:
        data.append({
            "name": task.name,
            "deadline": str(task.deadline) if task.deadline else None,
            "priority": task.priority,
            "category": task.category,
            "done": task.done,
            "done_date": str(task.done_date) if task.done_date else None,
        })
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

</details>

<details>
<summary>ステップ4：メインループを作る</summary>

入力のバリデーションとエラーハンドリングを丁寧に行います。

```python
def safe_int_input(prompt, valid_range=None):
    """安全な数値入力"""
    while True:
        try:
            value = int(input(prompt))
            if valid_range and value not in valid_range:
                print(f"{min(valid_range)}〜{max(valid_range)}で入力してください。")
                continue
            return value
        except ValueError:
            print("数字を入力してください。")
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け ─ 段階的に構築）</summary>

```python
# タスク管理CLIアプリケーション
# 学べる内容：クラス設計、ファイルI/O（JSON）、日付操作、エラー処理、総合設計

import json
import os
from datetime import date


class Task:
    """タスク1件を表すクラス"""

    PRIORITY_MAP = {1: "低", 2: "中", 3: "高"}

    def __init__(self, name, deadline=None, priority=2, category="未分類"):
        self.name = name
        self.deadline = deadline
        self.priority = priority
        self.category = category
        self.done = False
        self.done_date = None

    def complete(self):
        """タスクを完了にする"""
        self.done = True
        self.done_date = date.today()

    def is_overdue(self):
        """期限超過かどうか"""
        if self.deadline and not self.done:
            return date.today() > self.deadline
        return False

    def priority_label(self):
        """優先度のラベルを返す"""
        return self.PRIORITY_MAP.get(self.priority, "中")

    def deadline_str(self):
        """期限の表示文字列を返す"""
        if not self.deadline:
            return "なし"
        return str(self.deadline)

    def status_str(self):
        """残日数や期限超過の表示を返す"""
        if not self.deadline or self.done:
            return ""
        diff = (self.deadline - date.today()).days
        if diff < 0:
            return "⚠ 期限超過"
        elif diff == 0:
            return "⚠ 今日が期限"
        else:
            return f"残り{diff}日"

    def format(self, index):
        """整形して表示する"""
        status = self.status_str()
        return (f" {index}. [{self.priority_label()}] {self.name:<16}"
                f"期限:{self.deadline_str():<12} カテゴリ:{self.category:<8} {status}")

    def to_dict(self):
        """辞書に変換する（保存用）"""
        return {
            "name": self.name,
            "deadline": str(self.deadline) if self.deadline else None,
            "priority": self.priority,
            "category": self.category,
            "done": self.done,
            "done_date": str(self.done_date) if self.done_date else None,
        }

    @classmethod
    def from_dict(cls, data):
        """辞書からTaskを生成する（読込用）"""
        task = cls(
            name=data["name"],
            deadline=date.fromisoformat(data["deadline"]) if data["deadline"] else None,
            priority=data["priority"],
            category=data["category"],
        )
        task.done = data["done"]
        task.done_date = date.fromisoformat(data["done_date"]) if data["done_date"] else None
        return task


class TaskManager:
    """タスクの集合を管理するクラス"""

    def __init__(self):
        self.tasks = []

    def add(self, task):
        """タスクを追加する"""
        self.tasks.append(task)

    def get_incomplete(self):
        """未完了タスクを優先度降順で返す"""
        incomplete = [t for t in self.tasks if not t.done]
        return sorted(incomplete, key=lambda t: t.priority, reverse=True)

    def get_completed(self):
        """完了済みタスクを返す"""
        return [t for t in self.tasks if t.done]

    def search(self, keyword=None, category=None, priority=None):
        """条件に一致するタスクを検索する"""
        results = self.tasks
        if keyword:
            results = [t for t in results if keyword in t.name]
        if category:
            results = [t for t in results if t.category == category]
        if priority:
            results = [t for t in results if t.priority == priority]
        return results

    def get_overdue(self):
        """期限超過のタスクを返す"""
        return [t for t in self.tasks if t.is_overdue()]

    def stats(self):
        """統計情報を辞書で返す"""
        total = len(self.tasks)
        completed = len(self.get_completed())

        # カテゴリ別集計
        cat_counts = {}
        for task in self.tasks:
            cat_counts[task.category] = cat_counts.get(task.category, 0) + 1

        # 優先度別集計
        pri_counts = {}
        for task in self.get_incomplete():
            label = task.priority_label()
            pri_counts[label] = pri_counts.get(label, 0) + 1

        return {
            "total": total,
            "completed": completed,
            "incomplete": total - completed,
            "rate": round(completed / total * 100, 1) if total > 0 else 0,
            "by_category": cat_counts,
            "by_priority": pri_counts,
            "overdue": self.get_overdue(),
        }

    def save(self, filename):
        """JSONファイルに保存する"""
        data = [task.to_dict() for task in self.tasks]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, filename):
        """JSONファイルから読み込む"""
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.tasks = [Task.from_dict(item) for item in data]


# ==================== ユーティリティ関数 ====================

def safe_int_input(prompt, valid_range=None):
    """安全に整数を入力させる"""
    while True:
        try:
            value = int(input(prompt))
            if valid_range and not (min(valid_range) <= value <= max(valid_range)):
                print(f"{min(valid_range)}〜{max(valid_range)}で入力してください。")
                continue
            return value
        except ValueError:
            print("数字を入力してください。")


def input_date(prompt):
    """日付を入力させる（空欄可）"""
    while True:
        s = input(prompt)
        if s == "":
            return None
        try:
            return date.fromisoformat(s)
        except ValueError:
            print("YYYY-MM-DD 形式で入力してください（空欄でスキップ）。")


# ==================== メニュー操作 ====================

def menu_add(manager):
    """タスク追加"""
    name = input("タスク名: ")
    if not name:
        print("タスク名を入力してください。")
        return
    deadline = input_date("期限 (YYYY-MM-DD, 空欄でスキップ): ")
    priority = safe_int_input("優先度 (1:低 2:中 3:高): ", range(1, 4))
    category = input("カテゴリ: ") or "未分類"

    task = Task(name, deadline, priority, category)
    manager.add(task)
    print(f"「{name}」を追加しました。（優先度:{task.priority_label()}）")


def menu_list(manager):
    """タスク一覧"""
    incomplete = manager.get_incomplete()
    completed = manager.get_completed()

    if not incomplete and not completed:
        print("タスクがありません。")
        return

    print("\n--- タスク一覧 ---")
    if incomplete:
        print(" [未完了] 優先度順")
        for i, task in enumerate(incomplete, 1):
            print(task.format(i))

    if completed:
        print("\n [完了済み]")
        for task in completed:
            print(f" ✓ {task.name}  (完了日:{task.done_date})")


def menu_complete(manager):
    """タスク完了"""
    incomplete = manager.get_incomplete()
    if not incomplete:
        print("未完了のタスクがありません。")
        return

    print("\n未完了タスク:")
    for i, task in enumerate(incomplete, 1):
        print(f" {i}. {task.name}")

    num = safe_int_input("完了にする番号: ", range(1, len(incomplete) + 1))
    task = incomplete[num - 1]
    task.complete()
    print(f"「{task.name}」を完了にしました。")


def menu_search(manager):
    """タスク検索"""
    print("検索条件を入力（空欄でスキップ）:")
    keyword = input("  キーワード: ") or None
    category = input("  カテゴリ: ") or None

    pri_input = input("  優先度 (1:低 2:中 3:高): ")
    priority = int(pri_input) if pri_input in ("1", "2", "3") else None

    results = manager.search(keyword, category, priority)
    if results:
        print(f"\n--- 検索結果 ({len(results)}件) ---")
        for i, task in enumerate(results, 1):
            status = "✓" if task.done else " "
            print(f" {status} {task.name:<16} [{task.priority_label()}] カテゴリ:{task.category}")
    else:
        print("条件に一致するタスクがありません。")


def menu_change_priority(manager):
    """優先度変更"""
    incomplete = manager.get_incomplete()
    if not incomplete:
        print("未完了のタスクがありません。")
        return

    for i, task in enumerate(incomplete, 1):
        print(f" {i}. [{task.priority_label()}] {task.name}")

    num = safe_int_input("変更する番号: ", range(1, len(incomplete) + 1))
    task = incomplete[num - 1]
    new_pri = safe_int_input(f"新しい優先度 (現在:{task.priority_label()}, 1:低 2:中 3:高): ", range(1, 4))
    task.priority = new_pri
    print(f"「{task.name}」の優先度を「{task.priority_label()}」に変更しました。")


def menu_stats(manager):
    """統計表示"""
    if not manager.tasks:
        print("タスクがありません。")
        return

    s = manager.stats()
    print(f"\n--- 統計 ---")
    print(f"合計: {s['total']}件 (未完了:{s['incomplete']} / 完了:{s['completed']})")
    print(f"完了率: {s['rate']}%")

    print("\nカテゴリ別:")
    for cat, count in s["by_category"].items():
        print(f"  {cat}: {count}件")

    if s["by_priority"]:
        print("\n優先度別（未完了）:")
        for pri, count in s["by_priority"].items():
            print(f"  {pri}: {count}件")

    overdue = s["overdue"]
    if overdue:
        print(f"\n期限超過タスク: {len(overdue)}件")
        for task in overdue:
            print(f"  - {task.name} (期限:{task.deadline})")


def menu_save(manager):
    """ファイル保存"""
    filename = "tasks.json"
    try:
        manager.save(filename)
        print(f"{filename} に保存しました。({len(manager.tasks)}件)")
    except OSError as e:
        print(f"保存に失敗しました: {e}")


def menu_load(manager):
    """ファイル読込"""
    filename = "tasks.json"
    try:
        manager.load(filename)
        print(f"{filename} から読み込みました。({len(manager.tasks)}件)")
    except FileNotFoundError:
        print(f"{filename} が見つかりません。")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"ファイルの形式が不正です: {e}")


# ==================== メインループ ====================

def main():
    manager = TaskManager()

    print("===== タスク管理アプリ =====")

    menu_items = {
        "1": ("タスク追加", menu_add),
        "2": ("タスク一覧", menu_list),
        "3": ("タスク完了", menu_complete),
        "4": ("タスク検索", menu_search),
        "5": ("優先度変更", menu_change_priority),
        "6": ("統計表示", menu_stats),
        "7": ("ファイル保存", menu_save),
        "8": ("ファイル読込", menu_load),
    }

    while True:
        print("\n[メニュー]")
        for key, (label, _) in menu_items.items():
            print(f" {key}. {label}", end="")
            if key in ("4", "8"):
                print()
        print("  9. 終了")

        choice = input("\n操作: ")

        if choice == "9":
            print("お疲れさまでした！")
            break
        elif choice in menu_items:
            menu_items[choice][1](manager)
        else:
            print("1〜9の番号を入力してください。")


if __name__ == "__main__":
    main()
```

</details>

<details>
<summary>解答例（改良版 ─ ジェネレータ＋内包表記の活用）</summary>

改良版では、初心者向けコードをベースに以下のポイントを内包表記・ジェネレータで書き直します。
全体のリライトではなく、**差分として学ぶべきテクニック** を紹介します。

```python
# --- TaskManager の改良ポイント ---

class TaskManager:
    # ... 省略（基本構造は同じ） ...

    def get_incomplete(self):
        """内包表記 + sorted のワンライナー"""
        return sorted(
            (t for t in self.tasks if not t.done),
            key=lambda t: t.priority,
            reverse=True,
        )

    def stats(self):
        """内包表記で集計を簡潔に"""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.done)

        # カテゴリ別集計をワンパスで
        cat_counts = {}
        pri_counts = {}
        for t in self.tasks:
            cat_counts[t.category] = cat_counts.get(t.category, 0) + 1
            if not t.done:
                label = t.priority_label()
                pri_counts[label] = pri_counts.get(label, 0) + 1

        return {
            "total": total,
            "completed": completed,
            "incomplete": total - completed,
            "rate": round(completed / total * 100, 1) if total else 0,
            "by_category": cat_counts,
            "by_priority": pri_counts,
            "overdue": [t for t in self.tasks if t.is_overdue()],
        }

    def save(self, filename):
        """リスト内包表記でシリアライズ"""
        data = [t.to_dict() for t in self.tasks]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, filename):
        """リスト内包表記でデシリアライズ"""
        with open(filename, "r", encoding="utf-8") as f:
            self.tasks = [Task.from_dict(d) for d in json.load(f)]
```

**学べるテクニック:**
- `sorted()` にジェネレータ式を直接渡す → 中間リスト不要
- `sum(1 for ...)` で条件付きカウント → `len([x for x in ...])` より省メモリ
- 1つの `for` ループで複数の辞書を同時集計 → ループ回数を削減

</details>

# 実践課題04：Git連携とコミット操作 ★2

> **難易度**: ★★☆☆☆（基礎）
> **前提知識**: 第1章〜第3章（環境構築、基本操作、ファイル操作）、第4章（Git連携とバージョン管理）
> **課題の種類**: ミニプロジェクト
> **学習目標**: Claude Codeを使ったGit操作（初期化、コミット、ブランチ作成、差分確認）を一通り体験し、AIによるコミットメッセージ自動生成を活用する

---

## 完成イメージ

以下のGit操作をClaude Code経由で実行し、クリーンなコミット履歴を作成します。

```
$ git log --oneline
abc1234 feat: Add delete functionality to todo app
def5678 feat: Add basic todo list implementation
ghi9012 Initial commit: project setup with README
```

操作の流れ:
```
> このプロジェクトをGitリポジトリとして初期化してください

> README.mdとsrc/の全ファイルをコミットしてください

> /commit
（Claude Codeが変更内容を分析して適切なコミットメッセージを生成）

> feature/delete-todo ブランチを作成して、TODOの削除機能を追加してください

> 変更の差分を見せてください
```

---

## 課題の要件

1. プロジェクトディレクトリをGitリポジトリとして初期化する
2. ファイルをステージングしてコミットする（Claude Codeに依頼）
3. `/commit`コマンドでAI生成のコミットメッセージを使う
4. 新しいブランチを作成して機能を追加する
5. `git diff`で変更内容を確認する
6. ブランチをマージする
7. コミット履歴を確認する

---

## ステップガイド

<details>
<summary>ステップ1：プロジェクトの準備とGit初期化</summary>

```bash
# プロジェクトディレクトリを作成
mkdir -p ~/claude-code-practice/task04
cd ~/claude-code-practice/task04

# 簡単なプロジェクトを用意
cat > README.md << 'EOF'
# TODO App
シンプルなTODOリストアプリケーション
EOF

mkdir -p src
cat > src/todo.py << 'EOF'
class TodoList:
    def __init__(self):
        self.todos = []

    def add(self, task):
        self.todos.append({"task": task, "done": False})
        print(f"追加: {task}")

    def show(self):
        if not self.todos:
            print("TODOはありません")
            return
        for i, todo in enumerate(self.todos, 1):
            status = "x" if todo["done"] else " "
            print(f"  [{status}] {i}. {todo['task']}")


if __name__ == "__main__":
    app = TodoList()
    app.add("Pythonを勉強する")
    app.add("Claude Codeを使いこなす")
    app.show()
EOF

# Claude Codeを起動
claude
```

対話モードで:
```
> このプロジェクトをGitリポジトリとして初期化して、.gitignoreも作成してください
```

</details>

<details>
<summary>ステップ2：初回コミット</summary>

```
# Claude Codeに初回コミットを依頼
> すべてのファイルをステージングして、初回コミットしてください。
> コミットメッセージは「Initial commit: project setup with README」にしてください
```

または `/commit` コマンドを使う方法:
```
# まず手動でステージング
> git add -A を実行してください

# /commitでAI生成メッセージを使用
> /commit
```

</details>

<details>
<summary>ステップ3：ブランチ作成と機能追加</summary>

```
# ブランチ作成
> feature/delete-todo という名前で新しいブランチを作成して切り替えてください

# 機能追加を依頼
> src/todo.pyのTodoListクラスに、delete メソッドを追加してください。
> 番号を指定してTODOを削除する機能です。
> 無効な番号の場合はエラーメッセージを表示してください。
```

</details>

<details>
<summary>ステップ4：差分確認とコミット</summary>

```
# 変更差分を確認
> 現在の変更内容を差分で見せてください

# コミット
> /commit

# mainブランチにマージ
> mainブランチに切り替えて、feature/delete-todoブランチをマージしてください

# 履歴確認
> コミット履歴を見せてください
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）── 1コマンドずつ確認</summary>

```bash
# 準備
mkdir -p ~/claude-code-practice/task04
cd ~/claude-code-practice/task04
# （ファイル作成は上記ステップ1参照）

claude
```

```
# 1. Git初期化
> このディレクトリをGitリポジトリとして初期化してください

# 2. .gitignore作成
> .gitignoreファイルを作成してください。__pycache__、*.pyc、.envを除外してください

# 3. 初回コミット
> すべてのファイルをgit addして、「Initial commit: project setup with README」というメッセージでコミットしてください

# 4. ブランチ作成
> feature/delete-todo ブランチを作成して切り替えてください

# 5. 機能追加
> src/todo.pyにdeleteメソッドを追加してください。
> 番号でTODOを削除する機能です。

# 6. 差分確認
> 変更内容を git diff で見せてください

# 7. コミット
> /commit

# 8. マージ
> mainブランチに切り替えて、feature/delete-todoをマージしてください

# 9. 履歴確認
> git log --oneline を実行してください
```

</details>

<details>
<summary>解答例（改良版）── 実務に近いGitワークフロー</summary>

実務では、より細かいコミット粒度とブランチ戦略が求められます。

```
# 1. 初期化と初回コミット（まとめて依頼）
> このプロジェクトをGitリポジトリとして初期化し、
> .gitignoreを作成して、Initial commitを作ってください。
> .gitignoreには __pycache__、*.pyc、.env、.venv、*.log を含めてください。

# 2. ブランチ作成＋機能追加＋テスト
> feature/delete-todoブランチを作成し、以下の変更を行ってください：
> - src/todo.pyにdeleteメソッドを追加（番号指定で削除、バリデーション付き）
> - src/todo.pyにtoggle_doneメソッドを追加（完了/未完了の切り替え）
> - メインの実行部分にdelete機能のデモも追加

# 3. コミットを分割（良い習慣）
> delete機能だけをステージングしてコミットしてください。
> その後、toggle_done機能を別のコミットとしてコミットしてください。

# 4. マージとクリーンアップ
> mainブランチにマージして、feature/delete-todoブランチを削除してください
```

**初心者向けとの違い:**
- 初心者向けは全変更を1コミットにまとめていますが、改良版では機能単位でコミットを分割しています
- 機能単位のコミットは、後でgit bisectやrevertが使いやすくなります
- ブランチの作成→開発→マージ→削除という一連のフローは、実務でのGitフロー（Git Flow）やGitHubフロー（GitHub Flow）の基本です

</details>

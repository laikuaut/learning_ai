# 第8章：高度なGit操作とトラブルシューティング - 演習問題

---

## 問題1：git stash で作業を一時退避する（基本）

以下の手順を実行して、`git stash` の使い方を練習してください。

1. 新しいリポジトリを作成し、`main.txt` を作成してコミットする
2. `main.txt` を編集する（コミットはしない）
3. `git stash` で変更を一時退避する
4. ワーキングツリーがクリーンになったことを確認する
5. `git stash pop` で変更を復元する

**期待される出力例（手順4）：**
```
$ git status
On branch main
nothing to commit, working tree clean
```

**期待される出力例（手順5）：**
```
$ git stash pop
On branch main
Changes not staged for commit:
  modified:   main.txt
Dropped refs/stash@{0} (xxxxxxx)
```

<details>
<summary>ヒント</summary>

`git stash` は未コミットの変更をスタックに退避します。`git stash list` で一覧、`git stash pop` で復元と削除、`git stash apply` で復元のみができます。

</details>

<details>
<summary>解答例</summary>

```bash
# 1. リポジトリ作成と初期コミット
mkdir stash-practice && cd stash-practice
git init -b main
echo "最初の内容" > main.txt
git add main.txt
git commit -m "feat: main.txt を追加"

# 2. ファイルを編集（コミットしない）
echo "作業中の変更" >> main.txt

# 3. stash で一時退避
git stash
# Saved working directory and index state WIP on main: xxxxxxx feat: main.txt を追加

# 4. クリーンな状態を確認
git status
# nothing to commit, working tree clean

# 5. stash から復元
git stash pop
# Changes not staged for commit: modified: main.txt

# 変更が戻っていることを確認
cat main.txt
# 最初の内容
# 作業中の変更
```

</details>

---

## 問題2：git revert でコミットを安全に取り消す（基本）

以下の手順を実行して、`git revert` の使い方を練習してください。

1. 新しいリポジトリを作成する
2. 3つのコミットを作成する（ファイルA追加 → ファイルB追加 → ファイルC追加）
3. 2番目のコミット（ファイルB追加）を `git revert` で取り消す
4. `git log --oneline` で履歴を確認する

**期待される出力例（手順4）：**
```
$ git log --oneline
xxxxxxx Revert "feat: ファイルBを追加"
xxxxxxx feat: ファイルCを追加
xxxxxxx feat: ファイルBを追加
xxxxxxx feat: ファイルAを追加
```

<details>
<summary>ヒント</summary>

`git revert <コミットハッシュ>` で指定したコミットを打ち消す新しいコミットを作成します。`git log --oneline` でコミットハッシュを確認してから実行しましょう。

</details>

<details>
<summary>解答例</summary>

```bash
# 1. リポジトリ作成
mkdir revert-practice && cd revert-practice
git init -b main

# 2. 3つのコミットを作成
echo "ファイルA" > a.txt
git add a.txt
git commit -m "feat: ファイルAを追加"

echo "ファイルB" > b.txt
git add b.txt
git commit -m "feat: ファイルBを追加"

echo "ファイルC" > c.txt
git add c.txt
git commit -m "feat: ファイルCを追加"

# 3. 2番目のコミットを revert（ハッシュを確認してから実行）
# git log --oneline でハッシュを確認
git revert HEAD~1 --no-edit
# HEAD~1 は「HEADの1つ前のコミット」を意味する

# 4. 履歴を確認
git log --oneline
# b.txt が削除された revert コミットが追加されている

# ファイル確認（b.txt が消えている）
ls
# a.txt  c.txt
```

</details>

---

## 問題3：git stash にメッセージをつけて管理する（基本）

複数の作業を `git stash` で管理する練習をしてください。

1. リポジトリを作成し、初期コミットを行う
2. 機能Aの作業中の変更を `git stash push -m "機能Aの作業中"` で退避する
3. 機能Bの作業中の変更を `git stash push -m "機能Bの作業中"` で退避する
4. `git stash list` で一覧を確認する
5. 機能Aの変更のみを復元する

**期待される出力例（手順4）：**
```
$ git stash list
stash@{0}: On main: 機能Bの作業中
stash@{1}: On main: 機能Aの作業中
```

<details>
<summary>ヒント</summary>

`git stash push -m "メッセージ"` でメッセージ付きの stash を作成できます。特定の stash を復元するには `git stash apply stash@{番号}` を使います。`pop` ではなく `apply` を使うと、stash を残したまま復元できます。

</details>

<details>
<summary>解答例</summary>

```bash
# 1. リポジトリ作成と初期コミット
mkdir stash-multi && cd stash-multi
git init -b main
echo "初期内容" > app.txt
git add app.txt
git commit -m "feat: 初期ファイルを追加"

# 2. 機能Aの作業を退避
echo "機能Aの変更" >> app.txt
git stash push -m "機能Aの作業中"

# 3. 機能Bの作業を退避
echo "機能Bの変更" >> app.txt
git stash push -m "機能Bの作業中"

# 4. stash 一覧を確認
git stash list
# stash@{0}: On main: 機能Bの作業中
# stash@{1}: On main: 機能Aの作業中

# 5. 機能A（stash@{1}）を復元
git stash apply stash@{1}

# 確認
cat app.txt
# 初期内容
# 機能Aの変更
```

</details>

---

## 問題4：git bisect でバグ混入コミットを特定する（応用）

以下のシナリオで `git bisect` を使ってバグが混入したコミットを特定してください。

1. 新しいリポジトリを作成する
2. 5つのコミットを順番に作成する（各コミットでファイルに1行追加）
3. 3番目のコミットで意図的に「バグ」を混入させる（例：`BUG` という文字列を含める）
4. `git bisect` を使って、バグが混入したコミットを特定する

**期待される手順：**
```
$ git bisect start
$ git bisect bad          # 現在のHEADはバグあり
$ git bisect good <最初のコミットハッシュ>  # 最初のコミットはバグなし
# Gitが中間のコミットをチェックアウトする
$ git bisect bad          # または good（ファイルの内容を確認して判断）
# ... 繰り返し ...
# バグ混入コミットが特定される
$ git bisect reset        # 元のHEADに戻る
```

<details>
<summary>ヒント</summary>

`git bisect` は二分探索でバグ混入コミットを特定します。`git bisect start` → `bad`/`good` を指定 → Gitが自動でチェックアウトするコミットを確認して `bad` か `good` を報告、を繰り返します。自動化するには `git bisect run <スクリプト>` が使えます。

</details>

<details>
<summary>解答例</summary>

```bash
# 1. リポジトリ作成
mkdir bisect-practice && cd bisect-practice
git init -b main

# 2-3. 5つのコミットを作成（3番目にバグ混入）
echo "行1: 正常なコード" > app.txt
git add app.txt
git commit -m "feat: 初期コード"

echo "行2: 正常な追加" >> app.txt
git add app.txt
git commit -m "feat: 機能追加1"

echo "行3: BUG - ここにバグが混入" >> app.txt  # バグ混入！
git add app.txt
git commit -m "feat: 機能追加2"

echo "行4: 正常な追加" >> app.txt
git add app.txt
git commit -m "feat: 機能追加3"

echo "行5: 正常な追加" >> app.txt
git add app.txt
git commit -m "feat: 機能追加4"

# 最初のコミットハッシュを取得
FIRST_COMMIT=$(git log --reverse --format="%H" | head -1)

# 4. git bisect で自動的にバグ混入コミットを特定
git bisect start
git bisect bad              # 現在のHEADにはバグがある
git bisect good "$FIRST_COMMIT"  # 最初のコミットにはバグがない

# 自動化: grep で BUG を検索するスクリプトで判定
git bisect run grep -q "BUG" app.txt
# → バグ混入コミット（"feat: 機能追加2"）が特定される

# bisect 終了
git bisect reset
```

</details>

---

## 問題5：git reflog で誤操作から復旧する（応用）

以下のシナリオで `git reflog` を使って誤って削除したコミットを復旧してください。

1. リポジトリを作成し、3つのコミットを作成する
2. `git reset --hard HEAD~2` で最新2つのコミットを「削除」する
3. `git reflog` で操作履歴を確認する
4. `git reset --hard` で削除したコミットを復旧する

**期待される流れ：**
```
$ git log --oneline
xxxxxxx 3つ目のコミット
xxxxxxx 2つ目のコミット
xxxxxxx 1つ目のコミット

$ git reset --hard HEAD~2
HEAD is now at xxxxxxx 1つ目のコミット

$ git reflog
xxxxxxx HEAD@{0}: reset: moving to HEAD~2
xxxxxxx HEAD@{1}: commit: 3つ目のコミット
xxxxxxx HEAD@{2}: commit: 2つ目のコミット
xxxxxxx HEAD@{3}: commit (initial): 1つ目のコミット

$ git reset --hard HEAD@{1}
HEAD is now at xxxxxxx 3つ目のコミット
```

<details>
<summary>ヒント</summary>

`git reflog` はHEADの移動履歴を記録しています。`git reset --hard` でコミットが消えたように見えても、実際にはコミットオブジェクトはまだ存在しています。`git reflog` でハッシュを見つけて `git reset --hard <ハッシュ>` で復旧できます。

</details>

<details>
<summary>解答例</summary>

```bash
# 1. リポジトリ作成と3つのコミット
mkdir reflog-practice && cd reflog-practice
git init -b main

echo "1つ目" > file.txt
git add file.txt
git commit -m "feat: 1つ目のコミット"

echo "2つ目" >> file.txt
git add file.txt
git commit -m "feat: 2つ目のコミット"

echo "3つ目" >> file.txt
git add file.txt
git commit -m "feat: 3つ目のコミット"

# 現在の状態を確認
git log --oneline
# xxxxxxx feat: 3つ目のコミット
# xxxxxxx feat: 2つ目のコミット
# xxxxxxx feat: 1つ目のコミット

# 2. 誤って reset --hard してしまった！
git reset --hard HEAD~2
# HEAD is now at xxxxxxx feat: 1つ目のコミット

git log --oneline
# xxxxxxx feat: 1つ目のコミット（2つ消えた！）

# 3. reflog で操作履歴を確認
git reflog
# xxxxxxx HEAD@{0}: reset: moving to HEAD~2
# xxxxxxx HEAD@{1}: commit: feat: 3つ目のコミット  ← これを復旧したい
# xxxxxxx HEAD@{2}: commit: feat: 2つ目のコミット
# xxxxxxx HEAD@{3}: commit (initial): feat: 1つ目のコミット

# 4. 復旧（HEAD@{1} のハッシュを指定）
git reset --hard HEAD@{1}
# HEAD is now at xxxxxxx feat: 3つ目のコミット

# 復旧を確認
git log --oneline
# xxxxxxx feat: 3つ目のコミット
# xxxxxxx feat: 2つ目のコミット
# xxxxxxx feat: 1つ目のコミット
```

</details>

---

## 問題6：複合トラブルシューティング（チャレンジ）

以下の複合的なトラブルシューティングシナリオに挑戦してください。

### シナリオ

あなたはチーム開発中に以下の状況に陥りました。

1. `feature/login` ブランチで作業中に、急ぎの `hotfix/security` 対応が必要になった
2. 現在の作業を退避して hotfix ブランチを作成・修正・コミットする
3. hotfix を `main` にマージする
4. `feature/login` に戻って作業を再開する
5. `main` の hotfix 変更を `feature/login` に取り込む（rebase を使用）
6. 途中で `feature/login` の不要なコミットを発見したので `git revert` で取り消す

**実行すべき手順をすべて書き出し、実際にコマンドを実行してください。**

<details>
<summary>ヒント</summary>

手順の流れ：
1. `git stash push -m "login機能の作業中"` で現在の変更を退避
2. `git switch main` → `git switch -c hotfix/security` でブランチ作成
3. 修正してコミット → `git switch main` → `git merge hotfix/security`
4. `git switch feature/login` → `git stash pop` で作業復元
5. `git rebase main` で hotfix の変更を取り込む
6. `git revert <不要コミットのハッシュ>` で取り消し

</details>

<details>
<summary>解答例</summary>

```bash
# === 準備 ===
mkdir complex-practice && cd complex-practice
git init -b main

# 初期コミット
echo "アプリケーション v1.0" > app.txt
git add app.txt
git commit -m "feat: 初期リリース"

# feature/login ブランチで作業開始
git switch -c feature/login

echo "ログイン画面" > login.txt
git add login.txt
git commit -m "feat: ログイン画面を追加"

echo "認証ロジック" > auth.txt
git add auth.txt
git commit -m "feat: 認証ロジックを追加"

# デバッグ用の不要コミット（後で revert する）
echo "debug: テスト用" > debug.txt
git add debug.txt
git commit -m "chore: デバッグファイルを追加"

# さらに作業中（未コミット）
echo "パスワードリセット機能" >> login.txt

# === 1. 急ぎの hotfix 対応が必要に！ ===
# 現在の未コミット変更を退避
git stash push -m "login機能のパスワードリセット作業中"

# === 2. hotfix ブランチで修正 ===
git switch main
git switch -c hotfix/security

echo "セキュリティパッチ適用済み" >> app.txt
git add app.txt
git commit -m "fix: セキュリティ脆弱性を修正"

# === 3. main にマージ ===
git switch main
git merge hotfix/security
# Fast-forward マージ

# hotfix ブランチを削除
git branch -d hotfix/security

# === 4. feature/login に戻って作業再開 ===
git switch feature/login
git stash pop
# パスワードリセットの変更が復元される

# === 5. main の変更を rebase で取り込む ===
# まず未コミット変更をコミット
git add login.txt
git commit -m "feat: パスワードリセット機能を追加"

# rebase で main の hotfix を取り込む
git rebase main
# feature/login のコミットが main の最新の上に再配置される

# === 6. 不要なデバッグコミットを revert ===
# 不要コミットのハッシュを確認
git log --oneline
# debug.txt を追加したコミットを見つける

# revert で取り消し（ハッシュは git log で確認）
DEBUG_COMMIT=$(git log --oneline --all | grep "デバッグ" | awk '{print $1}')
git revert "$DEBUG_COMMIT" --no-edit

# === 最終確認 ===
git log --oneline --graph
# きれいな履歴になっていることを確認

echo ""
echo "=== ファイル一覧 ==="
ls
# app.txt  auth.txt  login.txt（debug.txt は revert で削除済み）
```

</details>

# 第8章：高度なGit操作とトラブルシューティング

## この章のゴール

- `git stash`、`git cherry-pick`、`git revert` など応用コマンドを使いこなせるようになる
- `git reset` の3つのモード（`--soft`、`--mixed`、`--hard`）の違いを正確に理解する
- `git reflog` や `git bisect` でトラブルを調査・復旧できるようになる
- タグ、サブモジュール、`.gitattributes` を適切に活用できるようになる
- よくあるトラブルに対処できるようになる

---

## 1. git stash — 作業の一時退避

`git stash`（スタッシュ）は、作業中の変更を一時的に退避させるコマンドです。ブランチを切り替えたいが、まだコミットしたくないときに使います。

```bash
# 作業中の変更を退避
git stash

# メッセージ付きで退避（何の作業か後でわかる）
git stash save "ログイン画面のCSS調整中"

# 退避した一覧を確認
git stash list
# stash@{0}: On feature/login: ログイン画面のCSS調整中

# 退避した変更を復元（スタッシュは残る）
git stash apply

# 退避した変更を復元して削除（スタッシュを消す）
git stash pop

# 特定のスタッシュを復元 / 削除
git stash apply stash@{1}
git stash drop stash@{0}
```

### よくある間違い
- `git stash` したことを忘れてしまう。`git stash list` で定期的に確認しましょう
- 未追跡ファイル（untracked file）は `git stash` では退避されません。`git stash -u` を使いましょう

### ポイントまとめ
- `stash` は「今の作業を一旦棚に上げる」機能です
- `apply` は残す、`pop` は消す、の違いを覚えておきましょう

---

## 2. git cherry-pick — 特定コミットの取り込み

`git cherry-pick`（チェリーピック）は、別のブランチから特定のコミットだけを現在のブランチに取り込むコマンドです。

```
  取り込み前:
  main     ●───●───●
  feature  ●───A───B───C───D

  cherry-pick B を実行:
  main     ●───●───●───B'
  feature  ●───A───B───C───D
                   ↑
              このコミットだけ取り込む
```

```bash
# 特定のコミットを現在のブランチに取り込む
git cherry-pick abc1234

# 複数のコミットを取り込む
git cherry-pick abc1234 def5678

# コミットせずに変更だけ取り込む（手動で調整したい場合）
git cherry-pick --no-commit abc1234

# コンフリクトが起きた場合
git cherry-pick abc1234
# CONFLICT と表示されたら...
# ファイルを編集してコンフリクトを解消
git add .
git cherry-pick --continue

# cherry-pickを中止したい場合
git cherry-pick --abort
```

### ポイントまとめ
- cherry-pick は「つまみ食い」です。必要なコミットだけを選んで取り込めます
- ホットフィックスを他のブランチにも適用したい場合に便利です

---

## 3. git revert vs git reset

コミットを取り消す方法は2つあります。それぞれの違いを正確に理解しましょう。

```
  git revert（打ち消しコミットを作る）= 安全

  変更前:  A ── B ── C
  revert C: A ── B ── C ── C'（Cを打ち消す新コミット）
  → 履歴は残る。チームで共有済みのコミットに使う

  git reset（コミット自体を消す）= 注意が必要

  変更前:  A ── B ── C
  reset B: A ── B
  → 履歴から消える。まだプッシュしていないコミットに使う
```

```bash
# revert: 指定コミットの変更を打ち消す新しいコミットを作成
git revert abc1234

# 直前のコミットを取り消す
git revert HEAD

# 複数コミットをまとめてrevert
git revert HEAD~3..HEAD

# reset: コミットを取り消す（後述の3モード参照）
git reset --soft HEAD~1
```

### よくある間違い
- プッシュ済みのコミットに `git reset` を使ってしまう。チームメンバーの履歴と矛盾するため、プッシュ済みなら `git revert` を使いましょう
- `git revert` がマージコミットに対しては特別な手順が必要なことを知らない。`-m 1` オプションが必要です

### ポイントまとめ
- **revert** = 安全。打ち消しコミットを作る。プッシュ済みに使う
- **reset** = 注意。履歴を消す。ローカルのみに使う

---

## 4. git reset の3つのモード

`git reset` には `--soft`、`--mixed`（デフォルト）、`--hard` の3つのモードがあります。

```
  コミット: A ── B ── C（HEAD）

  git reset --soft B
  ┌──────────────┬──────────────────┬──────────────────┐
  │  コミット履歴 │ ステージング     │ 作業ディレクトリ │
  │  A ── B      │ Cの変更が残る    │ Cの変更が残る    │
  └──────────────┴──────────────────┴──────────────────┘
  → コミットだけ取り消し。変更はステージングに残る

  git reset --mixed B（デフォルト）
  ┌──────────────┬──────────────────┬──────────────────┐
  │  コミット履歴 │ ステージング     │ 作業ディレクトリ │
  │  A ── B      │ クリア           │ Cの変更が残る    │
  └──────────────┴──────────────────┴──────────────────┘
  → コミットとステージングを取り消し。変更はファイルに残る

  git reset --hard B
  ┌──────────────┬──────────────────┬──────────────────┐
  │  コミット履歴 │ ステージング     │ 作業ディレクトリ │
  │  A ── B      │ クリア           │ クリア           │
  └──────────────┴──────────────────┴──────────────────┘
  → 全て取り消し。変更が完全に消える（危険）
```

```bash
# soft: コミットを取り消し、変更はステージングに残す
# → コミットメッセージを書き直したいとき
git reset --soft HEAD~1

# mixed（デフォルト）: コミットとステージングを取り消し
# → addからやり直したいとき
git reset HEAD~1

# hard: 全て取り消し（変更が完全に消える）
# → 全てなかったことにしたいとき（慎重に！）
git reset --hard HEAD~1
```

### よくある間違い
- `--hard` を気軽に使ってしまう。変更が完全に消えるため、本当に不要な場合だけ使いましょう
- `git reset` と `git checkout` を混同する。reset はHEADを動かし、checkout はブランチを切り替えます

### ポイントまとめ
- `--soft`：コミットだけ戻す（ステージング・作業ディレクトリはそのまま）
- `--mixed`：コミットとステージングを戻す（作業ディレクトリはそのまま）
- `--hard`：全て戻す（変更が消える。取り消し不可）

---

## 5. git reflog — 操作履歴から復旧する

`git reflog`（リフログ）は、HEADの移動履歴を記録しています。`git reset --hard` で消してしまったコミットも、reflogから復旧できます。

```bash
# reflogを確認
git reflog
# abc1234 HEAD@{0}: reset: moving to HEAD~1
# def5678 HEAD@{1}: commit: feat: 重要な機能を追加
# 789abcd HEAD@{2}: commit: fix: バグ修正

# 消してしまったコミットを復旧
git reset --hard def5678

# reflogは約90日間保持されます
```

```
  復旧の流れ:
  A ── B ── C  →(reset --hard A)→  A  →(reflogでCのSHAを確認)→  A ── B ── C
```

### ポイントまとめ
- reflogは「Gitの操作のアンドゥ」です。間違えても焦らずreflogを確認しましょう
- ただしreflogはローカルのみの記録です。リモートには残りません

---

## 6. git bisect — バグの原因コミットを特定する

`git bisect`（バイセクト）は、二分探索（binary search）でバグが混入したコミットを自動で特定するコマンドです。

```
  100コミットから手動なら最大100回、bisectなら log2(100) ≒ 7回で特定！

  ●──●──●──●──●──●──●──●──●──●
  OK                          NG
        ↓ bisect（二分探索）
     ●──●──●
     OK    NG
        ↓
       ●──●
       OK NG ← ここでバグが入った！
```

```bash
# bisectを開始して、現在は「バグあり」、v1.0.0は「正常」と伝える
git bisect start
git bisect bad
git bisect good v1.0.0

# Gitが中間のコミットをチェックアウトするので、テストして結果を伝える
git bisect good   # 正常なら
git bisect bad    # バグありなら
# → 原因コミットが特定されたら終了
git bisect reset

# テストスクリプトで自動化もできる
git bisect start HEAD v1.0.0
git bisect run python test_script.py
```

### ポイントまとめ
- bisectは大量のコミットから効率的にバグの原因を特定できます
- テストスクリプトがあれば `git bisect run` で完全自動化できます

---

## 7. git tag — バージョンの目印

タグ（tag）はコミットに名前を付ける機能です。リリースバージョンの管理に使います。

```bash
# 注釈付きタグ（annotated tag）— こちらが推奨
git tag -a v1.0.0 -m "初回リリース"

# タグ一覧を表示
git tag

# タグをリモートにプッシュ
git push origin v1.0.0

# タグを削除（ローカル＋リモート）
git tag -d v1.0.0
git push origin --delete v1.0.0
```

### ポイントまとめ
- リリース時には注釈付きタグ（`-a`）を使うのがベストプラクティスです
- セマンティックバージョニング（Semantic Versioning）の `vX.Y.Z` 形式が一般的です

---

## 8. git submodule — リポジトリの中にリポジトリ

`git submodule`（サブモジュール）は、あるリポジトリの中に別のリポジトリを組み込む仕組みです。

```bash
# サブモジュールを追加
git submodule add https://github.com/example/shared-lib.git libs/shared-lib

# サブモジュールを含むリポジトリをクローン
git clone --recurse-submodules https://github.com/example/main-repo.git

# 既にクローン済みの場合、サブモジュールを初期化・取得
git submodule update --init
```

### よくある間違い
- `git clone` しただけではサブモジュールの中身は取得されません。`--recurse-submodules` を付けましょう

### ポイントまとめ
- サブモジュールは共有ライブラリを複数プロジェクトで使い回す際に便利です
- 運用が複雑になるため、パッケージマネージャで代替できる場合はそちらを検討しましょう

---

## 9. .gitattributes と git blame

`.gitattributes` は改行コード（line ending）やバイナリ判定をリポジトリ単位で統一するファイルです。

```bash
# .gitattributes の例
* text=auto
*.py text eol=lf
*.bat text eol=crlf
*.png binary
```

`git blame` はファイルの各行の最終変更者を確認するコマンドです。

```bash
git blame src/app.py
# abc1234 (田中太郎 2025-12-01  1) def main():
# def5678 (佐藤花子 2025-12-05  2)     print("Hello")

# 特定の行範囲だけ表示
git blame -L 10,20 src/app.py
```

### ポイントまとめ
- `.gitattributes` でチーム全体の改行コードを統一し、差分ノイズを防ぎましょう
- `git blame` は犯人探しではなく、変更の経緯を理解するために使うツールです

---

## 10. トラブルシューティング集

### 間違えてコミットしてしまった

```bash
# 直前のコミットメッセージを修正（まだプッシュしていない場合）
git commit --amend -m "正しいメッセージ"

# 直前のコミットにファイルを追加し忘れた
git add forgotten_file.py
git commit --amend --no-edit
```

### 間違えてプッシュしてしまった

```bash
# revertで打ち消しコミットを作る（安全）
git revert HEAD
git push origin main
# 機密情報の場合はパスワード変更が最優先。履歴削除にはBFG Repo-Cleanerを使う
```

### コンフリクトが起きた

```bash
git merge feature/login
# CONFLICT (content): Merge conflict in src/auth.py
# ファイルを開き、<<<, ===, >>> マーカーを削除して正しい内容に修正
git add src/auth.py
git commit -m "merge: コンフリクトを解消"
```

### 大きなファイルをコミットしてしまった

```bash
git reset --soft HEAD~1
git rm --cached large_file.zip
echo "large_file.zip" >> .gitignore
git add .
git commit -m "chore: 大きなファイルを除外"
```

### 間違えたブランチで作業してしまった

```bash
# 未コミット → stashで退避して移動
git stash
git checkout correct-branch
git stash pop

# コミット済み → cherry-pickで移動
git checkout correct-branch
git cherry-pick abc1234
git checkout wrong-branch
git reset --hard HEAD~1
```

### よくある間違い
- パニックになって `git reset --hard` を連発する。まずは `git reflog` で状況を確認しましょう
- `.gitignore` に追加しても、既にコミット済みのファイルは追跡され続けます。`git rm --cached` で追跡を外す必要があります

### ポイントまとめ
- ほとんどのGitのミスは復旧可能です。`git reflog` が最後の砦です
- プッシュ済みのコミットには `revert`、ローカルのみなら `reset` を使い分けましょう
- 機密情報をプッシュした場合は、Git操作だけでなく**パスワード変更が最優先**です

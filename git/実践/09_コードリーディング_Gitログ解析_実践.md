# 実践課題09：コードリーディング ─ Gitログ解析 ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第2章（基本操作）、第3章（ブランチとマージ）、第7章（チーム開発ワークフロー）、第8章（高度なGit操作）
> **課題の種類**: コードリーディング
> **学習目標**: git log の出力を正確に読み取り、チーム開発の履歴からプロジェクトの状況を把握する力を養う

---

## 課題の説明

以下は、架空のチーム開発プロジェクト「TaskBoard」の Git 履歴です。
この履歴を読んで、後に続く **10個の設問** に答えてください。

**実際にコマンドを実行する必要はありません。履歴を読み解く力を鍛える課題です。**

---

## 読解対象の Git 履歴

### git log --oneline --graph --all

```
*   m9n0o1p (HEAD -> main) Merge pull request #15 from feature/notification
|\
| * k7l8m9n (feature/notification) feat: プッシュ通知の送信処理を実装
| * i5j6k7l feat: 通知設定画面を追加
| * g3h4i5j feat: 通知モデルを作成
|/
*   e1f2g3h Merge pull request #14 from fix/login-bug
|\
| * c9d0e1f (fix/login-bug) fix: セッションタイムアウト後の再ログインが失敗する問題を修正
|/
*   a7b8c9d Merge pull request #13 from feature/task-filter
|\
| * y5z6a7b feat: タスク一覧にフィルター機能を追加
| * w3x4y5z feat: フィルターUIコンポーネントを作成
|/
*   u1v2w3x Merge pull request #12 from feature/dashboard
|\
| *   s9t0u1v Merge branch 'main' into feature/dashboard
| |\
| |/
|/|
* | q7r8s9t hotfix: 本番環境のCSRF対策漏れを緊急修正
| * o5p6q7r feat: ダッシュボードにグラフ表示を追加
| * m3n4o5p feat: ダッシュボードのレイアウトを作成
|/
* k1l2m3n v1.0.0 リリース
* i9j0k1l chore: CI/CD パイプラインを設定
* g7h8i9j feat: ユーザー認証機能を実装
* e5f6g7h 初回コミット：プロジェクトの骨格を作成
```

### git log --format="%h %an %ad %s" --date=short（抜粋）

```
m9n0o1p 山田太郎 2024-04-12 Merge pull request #15 from feature/notification
k7l8m9n 佐藤花子 2024-04-11 feat: プッシュ通知の送信処理を実装
i5j6k7l 佐藤花子 2024-04-10 feat: 通知設定画面を追加
g3h4i5j 佐藤花子 2024-04-09 feat: 通知モデルを作成
e1f2g3h 山田太郎 2024-04-08 Merge pull request #14 from fix/login-bug
c9d0e1f 田中一郎 2024-04-07 fix: セッションタイムアウト後の再ログインが失敗する問題を修正
a7b8c9d 山田太郎 2024-04-05 Merge pull request #13 from feature/task-filter
y5z6a7b 鈴木次郎 2024-04-04 feat: タスク一覧にフィルター機能を追加
w3x4y5z 鈴木次郎 2024-04-03 feat: フィルターUIコンポーネントを作成
u1v2w3x 山田太郎 2024-04-02 Merge pull request #12 from feature/dashboard
s9t0u1v 佐藤花子 2024-04-01 Merge branch 'main' into feature/dashboard
q7r8s9t 山田太郎 2024-03-31 hotfix: 本番環境のCSRF対策漏れを緊急修正
o5p6q7r 佐藤花子 2024-03-30 feat: ダッシュボードにグラフ表示を追加
m3n4o5p 佐藤花子 2024-03-29 feat: ダッシュボードのレイアウトを作成
k1l2m3n 山田太郎 2024-03-28 v1.0.0 リリース
i9j0k1l 田中一郎 2024-03-25 chore: CI/CD パイプラインを設定
g7h8i9j 田中一郎 2024-03-20 feat: ユーザー認証機能を実装
e5f6g7h 山田太郎 2024-03-15 初回コミット：プロジェクトの骨格を作成
```

### git shortlog -s -n

```
     6  山田太郎
     6  佐藤花子
     4  田中一郎
     2  鈴木次郎
```

---

## 設問

以下の10問に答えてください。

### Q1. このプロジェクトのチームメンバーは何人ですか？

<details>
<summary>解答</summary>

**4人** です（山田太郎、佐藤花子、田中一郎、鈴木次郎）。

`git shortlog -s -n` の出力から、コミットした人が4名いることがわかります。

</details>

### Q2. v1.0.0 リリース後に作成されたプルリクエストは何件ですか？

<details>
<summary>解答</summary>

**4件** です（PR #12, #13, #14, #15）。

`k1l2m3n v1.0.0 リリース` の後に、4つのマージコミット（Merge pull request）があります。

</details>

### Q3. 佐藤花子さんが担当した機能は何ですか？

<details>
<summary>解答</summary>

**ダッシュボード機能**（PR #12）と**通知機能**（PR #15）の2つです。

佐藤花子さんのコミットを追うと：
- `m3n4o5p` ダッシュボードのレイアウトを作成
- `o5p6q7r` ダッシュボードにグラフ表示を追加
- `s9t0u1v` Merge branch 'main' into feature/dashboard
- `g3h4i5j` 通知モデルを作成
- `i5j6k7l` 通知設定画面を追加
- `k7l8m9n` プッシュ通知の送信処理を実装

</details>

### Q4. hotfix コミット `q7r8s9t` はなぜ発生しましたか？また、これによって何が起きましたか？

<details>
<summary>解答</summary>

**本番環境のCSRF対策に漏れがあったため**、緊急修正（hotfix）が行われました。

これにより、佐藤花子さんの `feature/dashboard` ブランチで `main` ブランチの取り込み（`Merge branch 'main' into feature/dashboard`）が発生しています。ダッシュボード開発中に `main` が先に進んだため、最新の `main` を取り込む必要があったのです。

</details>

### Q5. `feature/dashboard` ブランチのグラフが複雑になっている理由を説明してください。

<details>
<summary>解答</summary>

`feature/dashboard` ブランチの開発中に、`main` ブランチに hotfix コミット（`q7r8s9t`）がマージされたためです。

時系列：
1. `feature/dashboard` で開発開始（3/29, 3/30）
2. `main` に hotfix が入る（3/31）
3. `feature/dashboard` 内で `main` を取り込む（`s9t0u1v`: Merge branch 'main' into feature/dashboard）（4/1）
4. `main` に `feature/dashboard` をマージ（`u1v2w3x`）（4/2）

これにより、グラフ上でクロスする「たすき掛け」のような形になっています。

</details>

### Q6. マージを担当しているのは誰ですか？この人の役割は何だと推測できますか？

<details>
<summary>解答</summary>

**山田太郎さん** がすべてのプルリクエストのマージを行っています。

山田太郎さんは **テックリード（Tech Lead）またはリポジトリのメンテナー** だと推測できます。理由：
- すべてのPRマージを担当している
- 初回コミット（プロジェクト作成）を行っている
- v1.0.0 リリースのタグ付けを行っている
- 緊急の hotfix も自ら対応している

</details>

### Q7. PR #13（タスクフィルター機能）と PR #14（ログインバグ修正）は同時に開発されていた可能性がありますか？

<details>
<summary>解答</summary>

**可能性はあります**が、日付から見ると**順番に作業された可能性が高い**です。

- 鈴木次郎: フィルターUIを4/3に、機能実装を4/4に完了
- 田中一郎: ログインバグ修正を4/7に完了

PR #13 のマージ（4/5）後に PR #14 の作業（4/7）なので、順番に処理された可能性が高いですが、田中一郎さんが4/5以前からバグ調査を始めていた可能性もあります。

</details>

### Q8. 以下のコマンドの出力結果を予測してください。

```bash
git log --oneline main..feature/notification
```

<details>
<summary>解答</summary>

このコマンドは「main に含まれず、feature/notification にだけ含まれるコミット」を表示します。ただし、`feature/notification` は既に main にマージされているため、**何も表示されません**。

もしマージ前に実行していたら、以下が表示されたはずです：
```
k7l8m9n feat: プッシュ通知の送信処理を実装
i5j6k7l feat: 通知設定画面を追加
g3h4i5j feat: 通知モデルを作成
```

</details>

### Q9. このプロジェクトで使われている開発ワークフローは何ですか？

<details>
<summary>解答</summary>

**GitHub Flow** です。

根拠：
- `main` ブランチ1本がベースになっている（`develop` ブランチがない）
- 機能ごとにブランチを作成している（`feature/xxx`, `fix/xxx`）
- プルリクエストを通じてマージしている
- 緊急修正は `hotfix` として直接 `main` にコミットしている

Git Flow であれば `develop` ブランチや `release` ブランチが存在するはずですが、それらがないため GitHub Flow と判断できます。

</details>

### Q10. このプロジェクトの改善点を3つ挙げてください。

<details>
<summary>解答</summary>

1. **hotfix のプロセス改善**: `q7r8s9t` は直接 `main` にコミットされています。緊急でもPRを通すルールにすべきです（レビューなしの変更は危険）。

2. **ブランチの削除**: `feature/notification` と `fix/login-bug` がグラフ上にまだ残っています。マージ済みのブランチは速やかに削除すべきです。

3. **コミットの粒度の統一**: 鈴木次郎さんのPR #13 は2コミット（UI作成 + 機能実装）で適切ですが、田中一郎さんのPR #14 は1コミットだけです。修正内容によりますが、テストの追加なども別コミットにするとレビューしやすくなります。

</details>

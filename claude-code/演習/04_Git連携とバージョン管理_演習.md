# 第4章：Git連携とバージョン管理 - 演習問題

---

## 基本問題

### 問題1：安全ルールの理解

Claude CodeのGit操作における安全ルールについて、以下の操作が「許可される（○）」か「禁止される（×）」か答えてください。

1. 新しいコミットの作成
2. `main`ブランチへのforce push
3. `--no-verify`フラグでpre-commitフックをスキップ
4. 特定のファイルを指定してステージング
5. `git reset --hard`（ユーザーの明示的な指示なし）
6. featureブランチの作成と切り替え

**期待される解答：**
```
1. ___
2. ___
3. ___
4. ___
5. ___
6. ___
```

<details>
<summary>ヒント</summary>

Claude Codeは「破壊的な操作」を避ける設計になっています。データの消失リスクがある操作は原則禁止です。

</details>

<details>
<summary>解答例</summary>

```
1. ○ （コミットの作成は標準的な操作であり、常に許可されます）
2. × （main/masterブランチへのforce pushは禁止されています）
3. × （--no-verifyでフックをスキップすることは禁止されています）
4. ○ （git add . よりも具体的なファイル指定が推奨されます）
5. × （明示的な指示がない限り、reset --hardは実行しません）
6. ○ （ブランチの作成と切り替えは安全な操作です）
```

</details>

---

### 問題2：コミット作成の手順

Claude Codeが `/commit` コマンドでコミットを作成する際の手順を、正しい順番に並べ替えてください。

A. コミットメッセージを自動生成する
B. `git status`で変更ファイルを確認する
C. ユーザーの承認後にコミットを実行する
D. `git diff`で変更内容を分析する
E. `git log`で過去のコミットスタイルを確認する

**期待される解答：**
```
1番目: ___
2番目: ___
3番目: ___
4番目: ___
5番目: ___
```

<details>
<summary>ヒント</summary>

まず現状把握 → 分析 → メッセージ生成 → 実行の流れです。

</details>

<details>
<summary>解答例</summary>

```
1番目: B （git statusで変更ファイルを確認）
2番目: D （git diffで変更内容を分析）
3番目: E （git logで過去のコミットスタイルを確認）
4番目: A （変更内容に基づいてコミットメッセージを自動生成）
5番目: C （ユーザーの承認後にコミットを実行）
```

この順番で、変更内容を正確に把握し、リポジトリのスタイルに合ったコミットメッセージを生成します。

</details>

---

### 問題3：コミットメッセージの穴埋め

以下の変更内容に対して、適切なコミットメッセージの1行目を考えてください。

**変更1:** ログインフォームにメールアドレスのバリデーションを追加した
**変更2:** ユーザー一覧APIのN+1クエリ問題を修正した
**変更3:** テスト用のモックデータを更新した

**期待される解答：**
```
変更1: ___
変更2: ___
変更3: ___
```

<details>
<summary>ヒント</summary>

コミットメッセージの1行目は「何をしたか」を簡潔に表現します。英語の場合は動詞で始めるのが慣例です（Add, Fix, Update等）。

</details>

<details>
<summary>解答例</summary>

```
変更1: Add email validation to login form
変更2: Fix N+1 query issue in user list API
変更3: Update mock data for tests
```

- **Add**: 新しい機能や機能の追加
- **Fix**: バグの修正
- **Update**: 既存のものの更新・改善

日本語の場合：
```
変更1: ログインフォームにメールバリデーションを追加
変更2: ユーザー一覧APIのN+1クエリ問題を修正
変更3: テスト用モックデータを更新
```

</details>

---

## 応用問題

### 問題4：ブランチ戦略

以下のタスクに対して、適切なブランチ名を設計してください。Conventional Branch Naming（feature/xxx, fix/xxx, docs/xxx等）を使用します。

1. ユーザー登録機能の追加
2. ログインページの表示崩れの修正
3. APIドキュメントの更新
4. データベース接続処理のリファクタリング
5. セキュリティ脆弱性の緊急修正

**期待される解答：**
```
1. ___
2. ___
3. ___
4. ___
5. ___
```

<details>
<summary>ヒント</summary>

- `feature/`: 新機能
- `fix/`: バグ修正
- `docs/`: ドキュメント
- `refactor/`: リファクタリング
- `hotfix/`: 緊急修正

</details>

<details>
<summary>解答例</summary>

```
1. feature/user-registration
   （新機能の追加なのでfeature/を使用）

2. fix/login-page-layout
   （UIの表示崩れはバグ修正なのでfix/を使用）

3. docs/update-api-documentation
   （ドキュメントの更新なのでdocs/を使用）

4. refactor/database-connection
   （機能変更なしのコード改善なのでrefactor/を使用）

5. hotfix/security-vulnerability
   （緊急性のあるセキュリティ修正なのでhotfix/を使用）
```

</details>

---

### 問題5：コンフリクト解決シナリオ

以下のコンフリクトが発生しました。Claude Codeにどのようなプロンプトを出して解決しますか？

**状況：**
`feature/user-profile` ブランチで `src/models/User.ts` を編集中。`main`ブランチをマージしたところ、以下のコンフリクトが発生。

```
<<<<<<< HEAD
interface User {
  id: number;
  name: string;
  email: string;
  profileImage: string;
}
=======
interface User {
  id: number;
  name: string;
  email: string;
  role: "admin" | "user";
}
>>>>>>> main
```

Claude Codeにどのような指示を出しますか？

<details>
<summary>ヒント</summary>

- 両方の変更を保持したい場合が多いです
- どちらの変更を優先するか、または両方取り込むかを明確に指示しましょう

</details>

<details>
<summary>解答例</summary>

```
> src/models/User.ts でマージコンフリクトが発生しています。
> 両方の変更を取り込んでください。
> HEAD側の profileImage フィールドと、
> main側の role フィールドの両方を含む
> User インターフェースにしてください。
```

解決後のコード：
```typescript
interface User {
  id: number;
  name: string;
  email: string;
  profileImage: string;
  role: "admin" | "user";
}
```

ポイント：
- 「両方の変更を取り込む」と明確に指示する
- 具体的にどのフィールドを残すか伝えるとより確実
- 解決後はテストを実行して動作確認する

</details>

---

## チャレンジ問題

### 問題6：PRワークフロー設計

新機能「商品検索のフィルタリング機能」を開発するワークフローをClaude Codeを使って設計してください。以下の手順をClaude Codeへのプロンプト形式で記述してください。

1. ブランチの作成
2. 実装（APIとフロントエンド）
3. テストの作成と実行
4. コミット
5. PRの作成

**期待される解答：** 各ステップのプロンプトを記述

<details>
<summary>ヒント</summary>

- ブランチ名は機能を表す名前にする
- 実装は段階的に（APIから始めるのが一般的）
- テストは実装と合わせて作成
- PRにはSummaryとTest planを含める

</details>

<details>
<summary>解答例</summary>

```
Step 1: ブランチ作成
> feature/product-search-filter というブランチを作成して
> 切り替えてください

Step 2: API実装
> 商品検索APIにフィルタリング機能を追加してください。
> GET /api/products にクエリパラメータとして
> category, minPrice, maxPrice, sortBy を追加して、
> 条件に合った商品をフィルタリングして返すようにしてください。

Step 3: フロントエンド実装
> 商品一覧ページにフィルタリングUIを追加してください。
> カテゴリ選択（ドロップダウン）、価格帯（最小・最大入力）、
> 並び順（セレクトボックス）を配置し、APIと連携してください。

Step 4: テスト作成と実行
> 商品検索フィルタリングのテストを作成してください。
> APIのテスト（各フィルタ条件の正常系と異常系）と
> フロントエンドのコンポーネントテストを含めてください。
> 作成後、全テストを実行してください。

Step 5: コミット
> /commit

Step 6: PR作成
> この変更でmainブランチに対するプルリクエストを
> 作成してください。商品検索のフィルタリング機能追加
> について説明を含めてください。
```

</details>

---

### 問題7：Git操作の安全性判断

以下の各シナリオで、Claude Codeはどのように対応すべきですか？「そのまま実行」「ユーザーに確認」「拒否」のいずれかを選び、理由を述べてください。

1. ユーザーが「git push --force origin main」を依頼した
2. ユーザーが「この変更をコミットして」と依頼した（変更にはsrc/app.tsと.envファイルが含まれる）
3. ユーザーが「developブランチの変更を取り消して、mainと同じ状態にして」と依頼した
4. ユーザーが「featureブランチを作成してpushして」と依頼した

<details>
<summary>ヒント</summary>

- mainへのforce pushは最も危険な操作の1つです
- .envファイルにはAPI キーなどの機密情報が含まれることが多いです
- 変更の取り消しは破壊的操作です
- ブランチ作成とpushは比較的安全な操作です

</details>

<details>
<summary>解答例</summary>

```
1. 拒否（警告を表示）
   理由: mainブランチへのforce pushは他の開発者の作業を
   破壊する可能性があり、Claude Codeの安全ルールで
   明示的に禁止されています。別の方法を提案します。

2. ユーザーに確認
   理由: .envファイルにはAPIキーやデータベースの認証情報など
   の機密情報が含まれている可能性があります。.envファイルを
   コミットに含めるべきではないことをユーザーに警告し、
   src/app.tsのみをコミットすることを提案します。

3. ユーザーに確認
   理由: ブランチの変更を取り消す（reset --hard等）は
   破壊的な操作であり、コミットされていない変更が失われます。
   本当に実行してよいか確認し、影響範囲を説明します。

4. そのまま実行（確認あり）
   理由: featureブランチの作成とpushは比較的安全な操作です。
   ただし、ツール実行の確認は通常通り求められます。
```

</details>

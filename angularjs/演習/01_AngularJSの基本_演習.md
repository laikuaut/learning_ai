# 第1章: AngularJSの基本 - 演習問題

> この演習は「01_AngularJSの基本_教材.md」に対応しています。

---

## 演習1-1（基本）: シンプルな挨拶アプリ

### 問題

`ng-app` ディレクティブとAngularJSの式（Expression）を使って、以下の要件を満たすHTMLページを作成してください。

- AngularJS 1.8.3 のCDNを読み込む
- `ng-app` でAngularJSアプリケーションを有効化する
- AngularJSの式 `{{ }}` を使って「こんにちは、AngularJSの世界へようこそ！」と表示する
- 式の中で簡単な計算（例：`1 + 2`）の結果も表示する

### 期待される出力

```
こんにちは、AngularJSの世界へようこそ！
1 + 2 = 3
```

<details>
<summary>ヒント</summary>

- `ng-app` はAngularJSがページを管理するための開始点です。`<html>` タグまたは `<div>` タグに付与します。
- AngularJSの式は `{{ 式 }}` の形式で記述します。文字列や数値の計算が使えます。

</details>

<details>
<summary>解答例</summary>

```html
<!DOCTYPE html>
<html ng-app>
<head>
  <meta charset="UTF-8">
  <title>演習1-1: シンプルな挨拶アプリ</title>
  <!-- AngularJS 1.8.3 CDN を読み込む -->
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js"></script>
</head>
<body>
  <!-- AngularJSの式で文字列を表示 -->
  <h1>{{ 'こんにちは、AngularJSの世界へようこそ！' }}</h1>

  <!-- AngularJSの式で計算結果を表示 -->
  <p>1 + 2 = {{ 1 + 2 }}</p>
</body>
</html>
```

**解説:**

- `ng-app` を `<html>` タグに付与することで、ページ全体がAngularJSの管理下に入ります。
- `{{ }}` 内に文字列リテラルや数値計算を記述すると、AngularJSが評価して結果をDOMに反映します。
- `ng-app` に名前を指定しない場合は、モジュールなしで基本的な式評価が使えます。

</details>

---

## 演習1-2（基本）: コントローラーとスコープ変数

### 問題

AngularJSのコントローラーを使って、以下の自己紹介情報を表示するアプリを作成してください。

- モジュール名: `myApp`
- コントローラー名: `ProfileController`
- `$scope` に以下のプロパティを設定する:
  - `name`: 自分の名前（任意）
  - `age`: 年齢（任意の数値）
  - `hobby`: 趣味（任意の文字列）
  - `message`: 「AngularJSの学習を始めました！」

### 期待される出力

```
自己紹介
名前: 田中太郎
年齢: 25歳
趣味: プログラミング
メッセージ: AngularJSの学習を始めました！
```

<details>
<summary>ヒント</summary>

- `angular.module('モジュール名', [])` でモジュールを作成します。
- `.controller('コントローラー名', function($scope) { ... })` でコントローラーを定義します。
- HTML側では `ng-app="モジュール名"` と `ng-controller="コントローラー名"` を指定します。

</details>

<details>
<summary>解答例</summary>

```html
<!DOCTYPE html>
<html ng-app="myApp">
<head>
  <meta charset="UTF-8">
  <title>演習1-2: コントローラーとスコープ変数</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js"></script>
</head>
<body ng-controller="ProfileController">

  <h1>自己紹介</h1>
  <!-- $scopeのプロパティを式で表示 -->
  <p>名前: {{ name }}</p>
  <p>年齢: {{ age }}歳</p>
  <p>趣味: {{ hobby }}</p>
  <p>メッセージ: {{ message }}</p>

  <script>
    // モジュールを作成（第2引数の空配列は依存モジュールのリスト）
    var app = angular.module('myApp', []);

    // コントローラーを定義し、$scopeにデータを設定する
    app.controller('ProfileController', function($scope) {
      $scope.name = '田中太郎';       // 名前
      $scope.age = 25;                // 年齢
      $scope.hobby = 'プログラミング'; // 趣味
      $scope.message = 'AngularJSの学習を始めました！'; // メッセージ
    });
  </script>
</body>
</html>
```

**解説:**

- `angular.module('myApp', [])` の第2引数 `[]` は依存モジュールのリストです。空配列を渡すことで新しいモジュールを**作成**します（引数なしだと既存モジュールの**参照**になります）。
- `$scope` はコントローラーとビュー（HTML）をつなぐオブジェクトです。`$scope` に設定したプロパティは、対応する `ng-controller` の範囲内で `{{ }}` を使って参照できます。

</details>

---

## 演習1-3（応用）: シンプルな電卓アプリ

### 問題

`ng-model` とAngularJSの式を使って、以下の機能を持つ電卓アプリを作成してください。

- 2つの数値入力フィールドを用意する（`ng-model` を使用）
- 四則演算（加算・減算・乗算・除算）の結果をリアルタイムに表示する
- コントローラー名: `CalcController`
- ゼロ除算の場合は「計算できません」と表示する

### 期待される出力（数値に10と3を入力した場合）

```
シンプル電卓
数値1: [10]
数値2: [3]

計算結果:
10 + 3 = 13
10 - 3 = 7
10 × 3 = 30
10 ÷ 3 = 3.3333333333333335
```

<details>
<summary>ヒント</summary>

- `ng-model` でinput要素の値をスコープ変数にバインドします。
- `type="number"` を使うと数値入力になります。
- `ng-init` で初期値を設定できます。
- ゼロ除算のチェックには三項演算子 `条件 ? 値1 : 値2` が使えます。

</details>

<details>
<summary>解答例</summary>

```html
<!DOCTYPE html>
<html ng-app="myApp">
<head>
  <meta charset="UTF-8">
  <title>演習1-3: シンプルな電卓アプリ</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js"></script>
  <style>
    body { font-family: sans-serif; margin: 20px; }
    .result { margin-top: 15px; padding: 10px; background: #f0f0f0; border-radius: 5px; }
    input { width: 100px; padding: 5px; margin: 5px 0; }
  </style>
</head>
<body ng-controller="CalcController">

  <h1>シンプル電卓</h1>

  <!-- ng-modelで入力値をスコープ変数にバインド -->
  <p>数値1: <input type="number" ng-model="num1"></p>
  <p>数値2: <input type="number" ng-model="num2"></p>

  <div class="result">
    <h3>計算結果:</h3>
    <!-- 四則演算の結果を式で表示 -->
    <p>{{ num1 }} + {{ num2 }} = {{ num1 + num2 }}</p>
    <p>{{ num1 }} - {{ num2 }} = {{ num1 - num2 }}</p>
    <p>{{ num1 }} &times; {{ num2 }} = {{ num1 * num2 }}</p>
    <!-- ゼロ除算チェック -->
    <p>{{ num1 }} &divide; {{ num2 }} = {{ num2 === 0 ? '計算できません' : num1 / num2 }}</p>
  </div>

  <script>
    var app = angular.module('myApp', []);

    app.controller('CalcController', function($scope) {
      // 初期値を設定する
      $scope.num1 = 10;
      $scope.num2 = 3;
    });
  </script>
</body>
</html>
```

**解説:**

- `ng-model="num1"` により、input要素の値と `$scope.num1` が双方向にバインドされます。入力を変更すると、即座に計算結果が更新されます。
- AngularJSの式内で三項演算子を使うことで、条件分岐を実現できます。
- `type="number"` にすることで、入力値が数値として扱われ、文字列連結ではなく数値計算が行われます。

</details>

---

## 演習1-4（応用）: 複数コントローラーのデータ共有

### 問題

2つのコントローラーを使って、以下の機能を実装してください。

- `HeaderController`: アプリのタイトルとログインユーザー名を管理する
- `ContentController`: メインコンテンツ（商品リスト）を管理する
- 各コントローラーのスコープが独立していることを確認できるようにする
- `$rootScope` を使って、アプリ全体で共有するデータ（アプリバージョン）を設定する

### 期待される出力

```
ショッピングアプリ（v1.0）
ようこそ、田中さん

商品一覧:
- りんご: 150円
- バナナ: 100円
- みかん: 200円

アプリバージョン: v1.0
```

<details>
<summary>ヒント</summary>

- 複数の `ng-controller` を別々のHTML要素に適用することで、異なるコントローラーを使い分けられます。
- `$rootScope` はすべてのスコープの親であり、アプリ全体で共有するデータを保持できます。
- 商品データは配列にして `ng-repeat` で繰り返し表示すると便利です。

</details>

<details>
<summary>解答例</summary>

```html
<!DOCTYPE html>
<html ng-app="myApp">
<head>
  <meta charset="UTF-8">
  <title>演習1-4: 複数コントローラー</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js"></script>
  <style>
    body { font-family: sans-serif; margin: 20px; }
    .header { background: #3498db; color: white; padding: 10px 15px; border-radius: 5px; }
    .content { margin-top: 15px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
  </style>
</head>
<body>

  <!-- HeaderController の範囲 -->
  <div class="header" ng-controller="HeaderController">
    <h1>{{ title }}（{{ $root.appVersion }}）</h1>
    <p>ようこそ、{{ userName }}さん</p>
  </div>

  <!-- ContentController の範囲 -->
  <div class="content" ng-controller="ContentController">
    <h2>商品一覧:</h2>
    <ul>
      <!-- ng-repeatで商品リストを繰り返し表示 -->
      <li ng-repeat="product in products">
        {{ product.name }}: {{ product.price }}円
      </li>
    </ul>
    <!-- $rootScopeの値はどのコントローラーからもアクセスできる -->
    <p>アプリバージョン: {{ $root.appVersion }}</p>
  </div>

  <script>
    var app = angular.module('myApp', []);

    // アプリ起動時に$rootScopeに共有データを設定する
    app.run(function($rootScope) {
      $rootScope.appVersion = 'v1.0'; // 全コントローラーから参照可能
    });

    // ヘッダー用コントローラー
    app.controller('HeaderController', function($scope) {
      $scope.title = 'ショッピングアプリ'; // このスコープ内でのみ有効
      $scope.userName = '田中';            // このスコープ内でのみ有効
    });

    // コンテンツ用コントローラー
    app.controller('ContentController', function($scope) {
      // 商品データを配列で管理する
      $scope.products = [
        { name: 'りんご', price: 150 },
        { name: 'バナナ', price: 100 },
        { name: 'みかん', price: 200 }
      ];
    });
  </script>
</body>
</html>
```

**解説:**

- 各コントローラーは独立した `$scope` を持ちます。`HeaderController` の `title` や `userName` は `ContentController` からはアクセスできません。
- `$rootScope` はすべてのスコープの最上位の親です。`app.run()` で設定すると、アプリ起動時に実行されます。
- ビューでは `$root.appVersion` として `$rootScope` のプロパティにアクセスできます。
- ただし、`$rootScope` の多用はグローバル変数と同様の問題を引き起こすため、実務ではサービスを使ったデータ共有が推奨されます。

</details>

---

## 演習1-5（チャレンジ）: 動的プロフィールカードアプリ

### 問題

AngularJSのデータバインディングを活用して、リアルタイムにプレビューが更新されるプロフィールカードアプリを作成してください。

#### 要件

1. 入力フォーム（左側または上部）に以下のフィールドを用意する:
   - 名前（テキスト入力）
   - 肩書き（テキスト入力）
   - 自己紹介文（テキストエリア）
   - スキル（カンマ区切りのテキスト入力）
   - テーマカラー（`select` で3色から選択）

2. プロフィールカードのプレビュー（右側または下部）:
   - 入力内容がリアルタイムに反映される
   - テーマカラーの変更がカードの背景色に反映される
   - スキルはカンマで分割してバッジ風に表示する
   - 名前が未入力の場合は「名前を入力してください」と表示する

3. 入力文字数のカウントを表示する（名前・自己紹介文）

### 期待される出力（入力時）

```
--- 入力フォーム ---
名前: [山田花子] (4/20文字)
肩書き: [フロントエンドエンジニア]
自己紹介: [Webアプリケーション開発が得意です。] (18/200文字)
スキル: [HTML,CSS,JavaScript,AngularJS]
テーマカラー: [ブルー ▼]

--- プレビュー ---
┌──────────────────────┐
│    山田花子           │
│    フロントエンドエンジニア │
│                      │
│ Webアプリケーション    │
│ 開発が得意です。      │
│                      │
│ [HTML] [CSS]         │
│ [JavaScript]         │
│ [AngularJS]          │
└──────────────────────┘
```

<details>
<summary>ヒント</summary>

- スキルの分割には `split(',')` メソッドを使います。AngularJSの式内やコントローラーの関数で処理できます。
- テーマカラーの切り替えは `ng-style` または `ng-class` で実装できます。
- 文字数カウントは `変数.length` で取得できます。
- 未入力チェックには `ng-if` や `ng-show` が使えます。
- `ng-maxlength` で最大文字数の制限も加えてみましょう。

</details>

<details>
<summary>解答例</summary>

```html
<!DOCTYPE html>
<html ng-app="myApp">
<head>
  <meta charset="UTF-8">
  <title>演習1-5: 動的プロフィールカード</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js"></script>
  <style>
    body { font-family: sans-serif; margin: 20px; }
    .container { display: flex; gap: 30px; flex-wrap: wrap; }
    .form-section { flex: 1; min-width: 300px; }
    .preview-section { flex: 1; min-width: 300px; }
    .form-group { margin-bottom: 12px; }
    .form-group label { display: block; font-weight: bold; margin-bottom: 4px; }
    .form-group input, .form-group textarea, .form-group select {
      width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px;
    }
    .char-count { font-size: 12px; color: #888; }

    /* プロフィールカードのスタイル */
    .profile-card {
      border-radius: 10px; padding: 25px; color: white;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2); max-width: 350px;
    }
    .profile-card h2 { margin: 0 0 5px 0; }
    .profile-card .title { font-size: 14px; opacity: 0.9; margin-bottom: 15px; }
    .profile-card .bio { font-size: 14px; line-height: 1.6; margin-bottom: 15px;
      border-top: 1px solid rgba(255,255,255,0.3); padding-top: 15px; }
    .skill-badge {
      display: inline-block; background: rgba(255,255,255,0.25);
      padding: 3px 10px; border-radius: 12px; font-size: 12px; margin: 2px 4px 2px 0;
    }
    .placeholder { font-style: italic; opacity: 0.7; }
  </style>
</head>
<body ng-controller="ProfileCardController">

  <h1>動的プロフィールカード</h1>

  <div class="container">
    <!-- 入力フォーム -->
    <div class="form-section">
      <h2>入力フォーム</h2>

      <div class="form-group">
        <label>名前</label>
        <input type="text" ng-model="profile.name" maxlength="20" placeholder="名前を入力">
        <!-- 文字数カウントを表示 -->
        <span class="char-count">{{ (profile.name || '').length }}/20文字</span>
      </div>

      <div class="form-group">
        <label>肩書き</label>
        <input type="text" ng-model="profile.title" placeholder="肩書きを入力">
      </div>

      <div class="form-group">
        <label>自己紹介</label>
        <textarea ng-model="profile.bio" rows="3" maxlength="200" placeholder="自己紹介を入力"></textarea>
        <span class="char-count">{{ (profile.bio || '').length }}/200文字</span>
      </div>

      <div class="form-group">
        <label>スキル（カンマ区切り）</label>
        <input type="text" ng-model="profile.skillsText" placeholder="例: HTML,CSS,JavaScript">
      </div>

      <div class="form-group">
        <label>テーマカラー</label>
        <!-- select要素でテーマカラーを選択 -->
        <select ng-model="profile.theme">
          <option value="#3498db">ブルー</option>
          <option value="#2ecc71">グリーン</option>
          <option value="#e74c3c">レッド</option>
        </select>
      </div>
    </div>

    <!-- プレビュー -->
    <div class="preview-section">
      <h2>プレビュー</h2>
      <!-- ng-styleでテーマカラーを動的に適用 -->
      <div class="profile-card" ng-style="{ 'background-color': profile.theme }">

        <!-- 名前が入力されていない場合はプレースホルダーを表示 -->
        <h2 ng-if="profile.name">{{ profile.name }}</h2>
        <h2 ng-if="!profile.name" class="placeholder">名前を入力してください</h2>

        <div class="title">{{ profile.title || '肩書き未設定' }}</div>

        <!-- 自己紹介文 -->
        <div class="bio" ng-if="profile.bio">{{ profile.bio }}</div>

        <!-- スキルバッジ: カンマで分割して表示 -->
        <div ng-if="profile.skillsText">
          <span class="skill-badge"
                ng-repeat="skill in getSkills()">
            {{ skill }}
          </span>
        </div>
      </div>
    </div>
  </div>

  <script>
    var app = angular.module('myApp', []);

    app.controller('ProfileCardController', function($scope) {
      // プロフィールデータの初期値を設定する
      // オブジェクトにまとめることで管理しやすくなる
      $scope.profile = {
        name: '山田花子',
        title: 'フロントエンドエンジニア',
        bio: 'Webアプリケーション開発が得意です。',
        skillsText: 'HTML,CSS,JavaScript,AngularJS',
        theme: '#3498db' // デフォルトはブルー
      };

      // スキル文字列をカンマで分割して配列として返す関数
      $scope.getSkills = function() {
        if (!$scope.profile.skillsText) {
          return [];
        }
        // カンマで分割し、各要素の前後の空白を除去する
        return $scope.profile.skillsText.split(',').map(function(skill) {
          return skill.trim();
        }).filter(function(skill) {
          return skill.length > 0; // 空文字を除外する
        });
      };
    });
  </script>
</body>
</html>
```

**解説:**

- **データバインディング**: `ng-model` で入力値と `$scope.profile` のプロパティを双方向バインドしています。入力を変更すると、プレビューがリアルタイムに更新されます。
- **ng-style**: `ng-style="{ 'background-color': profile.theme }"` でテーマカラーを動的に適用しています。`select` の値が変わると即座に色が変わります。
- **ng-if**: 条件に応じてDOM要素の表示/非表示を切り替えています。`ng-show` との違いは、`ng-if` はDOMから完全に削除する点です。
- **関数のバインド**: `getSkills()` 関数を `ng-repeat` で使用し、カンマ区切りの文字列を配列に変換しています。AngularJSのダイジェストサイクルにより、入力が変わるたびに関数が再評価されます。
- **プロパティをオブジェクトにまとめる**: `$scope.profile` のようにオブジェクトにまとめることで、後の章で学ぶスコープ継承の問題（プリミティブ値の問題）を回避できます。

</details>

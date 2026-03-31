# 第1章 AngularJSの基本

## この章のゴール

- AngularJSとは何か、Angular（2+）との違いを理解する
- CDNを使ったAngularJSの導入方法を習得する
- `ng-app`ディレクティブとモジュールの概念を理解する
- コントローラー（Controller）と`$scope`の基本を理解する
- 式展開 `{{ }}` とデータバインディング（Data Binding）の基礎を身につける
- `ng-model`による双方向バインディング（Two-way Data Binding）を体験する
- ブラウザで動作する最初のAngularJSアプリケーションを作成する

---

## 1. AngularJSとは

### 1.1 AngularJSの概要

AngularJS（アンギュラージェイエス）は、Googleが2010年に公開したオープンソースのJavaScriptフレームワーク（Framework）です。HTMLを拡張して、動的なWebアプリケーション（Single Page Application / SPA）を構築するために設計されました。

```
+---------------------------------------------------+
|  AngularJSの歴史年表                                |
+---------------------------------------------------+
|  2010年  AngularJS 1.0 公開（Google）               |
|  2014年  Angular 2 発表（完全な別フレームワーク）      |
|  2016年  Angular 2 正式リリース                     |
|  2018年  AngularJS LTS（長期サポート）モードへ移行     |
|  2021年  AngularJS LTS 終了                        |
|  現在    レガシーシステムの保守で依然として使用中       |
+---------------------------------------------------+
```

### 1.2 AngularJS（1.x）と Angular（2+）の違い

AngularJSとAngularは**名前が似ていますが、まったく別のフレームワーク**です。以下の表で主な違いを整理します。

| 項目 | AngularJS（1.x） | Angular（2+） |
|------|------------------|--------------|
| 言語 | JavaScript | TypeScript |
| アーキテクチャ | MVC / MVVM | コンポーネントベース |
| データバインディング | 双方向（$scope） | 単方向＋双方向 |
| ビルドツール | 不要（CDNで動作） | 必要（CLI） |
| モバイル対応 | 限定的 | ネイティブ対応 |
| 学習コスト | 比較的低い | 比較的高い |

> **なぜ今AngularJSを学ぶのか？**
> 企業の既存システム（レガシーシステム）にはAngularJS製のものがまだ多く存在します。保守・移行のためにAngularJSの知識が求められる場面があります。

### ポイントまとめ
- AngularJSはGoogleが開発したJavaScriptフレームワーク
- Angular（2+）とは**別物**である
- ビルドツール不要でCDNだけで始められる手軽さが特長
- レガシーシステムの保守で現在も需要がある

---

## 2. 環境構築（CDNベース）

AngularJSはCDN（Content Delivery Network）からスクリプトを読み込むだけで使えます。Node.jsやビルドツールは不要です。

### 2.1 最小構成のHTMLファイル

```html
<!DOCTYPE html>
<html ng-app>
<head>
  <meta charset="UTF-8">
  <title>AngularJS はじめの一歩</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js"></script>
</head>
<body>

  <h1>{{ "Hello" + " AngularJS!" }}</h1>

</body>
</html>
```

このファイルをブラウザで開くと、`Hello AngularJS!` と表示されます。

### 2.2 セットアップの仕組み

```
+------------------------------------------------------+
|  HTMLファイルの読み込み                                 |
|                                                      |
|  1. ブラウザがHTMLを読み込む                            |
|  2. <script> タグで angular.min.js を取得              |
|  3. AngularJS が ng-app を見つける                     |
|  4. ng-app 以下のHTMLをAngularJSが管理（コンパイル）     |
|  5. {{ }} 式が評価されて画面に表示                      |
+------------------------------------------------------+
```

> **よくある間違い**
> `<script>` タグを `<body>` の閉じタグ直前に置くと、`ng-app` の処理前にHTMLが表示され、一瞬 `{{ }}` がそのまま見えることがあります。`<head>` 内に配置するか、後述する `ng-cloak` を使って回避しましょう。

### ポイントまとめ
- CDNのURLは `https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js`
- `<script>` タグを1行追加するだけでAngularJSが使える
- ビルドツールは不要で、HTMLファイルをブラウザで開くだけで動作する

---

## 3. ng-appディレクティブとモジュール

### 3.1 ng-appディレクティブ（Directive）

ディレクティブ（Directive）とは、HTMLの属性や要素を拡張するAngularJS独自の仕組みです。`ng-app` はその中でも最も基本的なディレクティブで、**AngularJSアプリケーションのルート要素**を指定します。

```html
<!-- パターン1: html要素に指定（ページ全体がAngularJS管理下） -->
<html ng-app="myApp">

<!-- パターン2: 特定の要素に指定（その要素内だけがAngularJS管理下） -->
<div ng-app="myApp">
  <!-- ここだけAngularJSが有効 -->
</div>
```

### 3.2 モジュール（Module）

モジュール（Module）は、AngularJSアプリケーションを構成する**コンテナ**です。コントローラー、サービス、フィルターなどを登録する場所になります。

```javascript
// モジュールを定義する（第2引数は依存モジュールの配列）
var app = angular.module('myApp', []);
```

```
+---------------------------------------------+
|  angular.module('myApp', [])                |
|                                             |
|  'myApp'  → モジュール名                     |
|  []       → 依存する他モジュールのリスト       |
|             空配列 = 依存なし（新規作成）       |
+---------------------------------------------+
```

> **よくある間違い**
> `angular.module('myApp')` のように第2引数を省略すると、**既存モジュールの取得**になります。新しくモジュールを作るときは必ず `angular.module('myApp', [])` と空配列を渡してください。
>
> ```javascript
> // 新規作成（第2引数あり）
> var app = angular.module('myApp', []);
>
> // 既存モジュールの取得（第2引数なし）
> var app = angular.module('myApp');
> ```

### 3.3 完全な例：モジュールの定義

```html
<!DOCTYPE html>
<html ng-app="myApp">
<head>
  <meta charset="UTF-8">
  <title>モジュール定義の例</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js"></script>
  <script>
    // モジュールを定義
    var app = angular.module('myApp', []);
  </script>
</head>
<body>
  <p>AngularJSモジュール「myApp」が動作しています。</p>
  <p>計算結果: {{ 10 + 20 }}</p>
</body>
</html>
```

### ポイントまとめ
- `ng-app` はAngularJSが管理する範囲を指定するディレクティブ
- `angular.module('名前', [])` でモジュールを新規作成する
- 第2引数の `[]` を忘れると新規作成ではなく取得になるので注意
- 1つのHTMLページには原則として1つの `ng-app` を配置する

---

## 4. コントローラーと$scope

### 4.1 コントローラー（Controller）とは

コントローラー（Controller）は、ビュー（View = HTML）に表示するデータやロジック（ビジネスロジック）を定義する場所です。MVC（Model-View-Controller）パターンの「C」に相当します。

```
+---------------------------------------------------+
|              MVC パターン                           |
|                                                   |
|  +----------+    +----------+    +----------+     |
|  |  Model   | ←→ |Controller| ←→ |   View   |    |
|  | (データ)  |    | (ロジック)|    |  (HTML)   |    |
|  +----------+    +----------+    +----------+     |
|                       ↑                           |
|                    $scope                          |
|              （ModelとViewの橋渡し）                  |
+---------------------------------------------------+
```

### 4.2 $scope（スコープ）

`$scope`（スコープ）は、コントローラーとビューの間でデータを共有するためのオブジェクトです。コントローラー内で `$scope` にプロパティやメソッドを追加すると、HTMLテンプレート内からアクセスできます。

```html
<!DOCTYPE html>
<html ng-app="myApp">
<head>
  <meta charset="UTF-8">
  <title>コントローラーの基本</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js"></script>
  <script>
    var app = angular.module('myApp', []);

    // コントローラーを定義
    app.controller('MainController', function($scope) {
      $scope.title = 'AngularJS入門';
      $scope.message = 'コントローラーからのメッセージです。';
      $scope.year = 2026;
    });
  </script>
</head>
<body ng-controller="MainController">

  <h1>{{ title }}</h1>
  <p>{{ message }}</p>
  <p>現在の年: {{ year }}</p>

</body>
</html>
```

### 4.3 $scopeにメソッドを追加する

`$scope` にはデータだけでなく、関数（メソッド）も追加できます。

```html
<!DOCTYPE html>
<html ng-app="myApp">
<head>
  <meta charset="UTF-8">
  <title>$scopeのメソッド</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js"></script>
  <script>
    var app = angular.module('myApp', []);

    app.controller('CalcController', function($scope) {
      $scope.price = 1000;
      $scope.quantity = 1;

      // 合計金額を計算するメソッド
      $scope.getTotal = function() {
        return $scope.price * $scope.quantity;
      };

      // 税込金額を計算するメソッド
      $scope.getTaxIncluded = function() {
        return Math.floor($scope.getTotal() * 1.1);
      };
    });
  </script>
</head>
<body ng-controller="CalcController">

  <h2>料金計算</h2>
  <p>単価: {{ price }} 円</p>
  <p>数量: {{ quantity }}</p>
  <p>合計: {{ getTotal() }} 円</p>
  <p>税込: {{ getTaxIncluded() }} 円</p>

</body>
</html>
```

### 4.4 依存性注入（Dependency Injection / DI）

AngularJSのコントローラー関数の引数に `$scope` と書くだけで、AngularJSが自動的に `$scope` オブジェクトを渡してくれます。この仕組みを**依存性注入（Dependency Injection / DI）**と呼びます。

```javascript
// AngularJSが引数名を見て、適切なオブジェクトを注入する
app.controller('MyController', function($scope, $http) {
  // $scope と $http が自動的に渡される
});
```

> **よくある間違い**
> JavaScriptを圧縮（Minify）すると引数名が変わり、DIが壊れます。本番環境では配列記法を使いましょう。
>
> ```javascript
> // 圧縮に対応した配列記法（推奨）
> app.controller('MyController', ['$scope', '$http', function($scope, $http) {
>   // 文字列の順序と引数の順序を一致させる
> }]);
> ```

### ポイントまとめ
- コントローラーはデータとロジックを定義する場所
- `$scope` はコントローラーとビュー（HTML）を橋渡しするオブジェクト
- `$scope` にプロパティを追加すると `{{ }}` でHTMLに表示できる
- `$scope` にメソッドを追加すると `{{ メソッド名() }}` で呼び出せる
- JavaScriptの圧縮対策として配列記法を使うのがベストプラクティス

---

## 5. 式展開 {{ }} とデータバインディング

### 5.1 式展開（Expression）

AngularJSの式展開（Expression）`{{ }}` は、HTMLテンプレート内でJavaScriptの式を評価して結果を表示する仕組みです。

```html
<!-- 文字列結合 -->
<p>{{ "こんにちは、" + "世界！" }}</p>

<!-- 算術演算 -->
<p>{{ 100 * 3 + 50 }}</p>

<!-- 三項演算子 -->
<p>{{ score >= 60 ? "合格" : "不合格" }}</p>

<!-- オブジェクトのプロパティ -->
<p>{{ user.name }}</p>

<!-- 配列の要素 -->
<p>{{ items[0] }}</p>
```

> **よくある間違い**
> AngularJSの式では `if`、`for`、`while` などの**制御構文は使えません**。条件分岐には三項演算子を、繰り返しには `ng-repeat` ディレクティブを使います。
>
> ```html
> <!-- NG: if文は使えない -->
> <p>{{ if (x > 0) { "正" } }}</p>
>
> <!-- OK: 三項演算子を使う -->
> <p>{{ x > 0 ? "正" : "負" }}</p>
> ```

### 5.2 データバインディング（Data Binding）の基本

データバインディング（Data Binding）とは、モデル（データ）とビュー（HTML）を自動的に同期する仕組みです。AngularJSでは、`$scope` のデータが変わると、HTMLの表示も自動的に更新されます。

```
+-------------------------------------------+
|  データバインディングの流れ                    |
|                                           |
|  $scope.name = "太郎"                      |
|       ↓ 自動同期                           |
|  <p>{{ name }}</p>  →  <p>太郎</p>         |
|                                           |
|  $scope.name = "花子" に変更               |
|       ↓ 自動同期                           |
|  <p>{{ name }}</p>  →  <p>花子</p>         |
+-------------------------------------------+
```

### 5.3 完全な例：式展開のデモ

```html
<!DOCTYPE html>
<html ng-app="myApp">
<head>
  <meta charset="UTF-8">
  <title>式展開デモ</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js"></script>
  <script>
    var app = angular.module('myApp', []);

    app.controller('ExprController', function($scope) {
      $scope.name = '山田太郎';
      $scope.age = 25;
      $scope.scores = [85, 92, 78, 95, 88];
      $scope.user = {
        email: 'yamada@example.com',
        role: '管理者'
      };
    });
  </script>
</head>
<body ng-controller="ExprController">

  <h2>式展開の例</h2>

  <!-- 変数の表示 -->
  <p>名前: {{ name }}</p>
  <p>年齢: {{ age }} 歳</p>

  <!-- 計算 -->
  <p>10年後: {{ age + 10 }} 歳</p>

  <!-- 文字列結合 -->
  <p>{{ name + "さん、こんにちは！" }}</p>

  <!-- 三項演算子 -->
  <p>{{ age >= 20 ? "成人" : "未成年" }}</p>

  <!-- オブジェクトのプロパティ -->
  <p>メール: {{ user.email }}</p>
  <p>権限: {{ user.role }}</p>

  <!-- 配列 -->
  <p>最初のスコア: {{ scores[0] }}</p>
  <p>スコア数: {{ scores.length }}</p>

</body>
</html>
```

### ポイントまとめ
- `{{ }}` で `$scope` のデータや式の結果をHTMLに表示できる
- 文字列結合、算術演算、三項演算子、オブジェクトのプロパティアクセスが使える
- `if` / `for` などの制御構文は使えない
- データが変わると表示も自動的に更新される（データバインディング）

---

## 6. ng-modelによる双方向バインディング入門

### 6.1 ng-modelとは

`ng-model` ディレクティブは、フォーム要素（`<input>`, `<select>`, `<textarea>`）と `$scope` のプロパティを**双方向にバインド**します。

```
+---------------------------------------------------+
|  双方向バインディング（Two-way Data Binding）         |
|                                                   |
|  $scope.name ←――→ <input ng-model="name">         |
|                                                   |
|  ・入力欄に文字を打つ → $scope.name が更新           |
|  ・$scope.name を変更 → 入力欄の値が更新             |
|                                                   |
|  どちらが変わっても、もう片方に即座に反映される         |
+---------------------------------------------------+
```

### 6.2 基本的な使い方

```html
<!DOCTYPE html>
<html ng-app="myApp">
<head>
  <meta charset="UTF-8">
  <title>ng-model 基本</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js"></script>
  <script>
    var app = angular.module('myApp', []);

    app.controller('FormController', function($scope) {
      $scope.name = '';
      $scope.age = 20;
    });
  </script>
</head>
<body ng-controller="FormController">

  <h2>自己紹介フォーム</h2>

  <label>名前: </label>
  <input type="text" ng-model="name" placeholder="名前を入力">
  <br><br>

  <label>年齢: </label>
  <input type="number" ng-model="age" min="0" max="150">
  <br><br>

  <h3>プレビュー（リアルタイム反映）</h3>
  <p>名前: {{ name || "(未入力)" }}</p>
  <p>年齢: {{ age }} 歳</p>
  <p>{{ age >= 20 ? "お酒が飲めます" : "お酒はまだ飲めません" }}</p>

</body>
</html>
```

入力欄に文字を打つと、プレビュー部分がリアルタイムで更新されます。これが双方向バインディングの力です。

### 6.3 さまざまなフォーム要素との連携

```html
<!DOCTYPE html>
<html ng-app="myApp">
<head>
  <meta charset="UTF-8">
  <title>ng-model フォーム要素</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js"></script>
  <script>
    var app = angular.module('myApp', []);

    app.controller('SurveyController', function($scope) {
      $scope.name = '';
      $scope.gender = '';
      $scope.prefecture = '';
      $scope.comment = '';
      $scope.agree = false;
    });
  </script>
</head>
<body ng-controller="SurveyController">

  <h2>アンケートフォーム</h2>

  <label>名前: </label>
  <input type="text" ng-model="name">
  <br><br>

  <label>性別: </label>
  <label><input type="radio" ng-model="gender" value="male"> 男性</label>
  <label><input type="radio" ng-model="gender" value="female"> 女性</label>
  <label><input type="radio" ng-model="gender" value="other"> その他</label>
  <br><br>

  <label>都道府県: </label>
  <select ng-model="prefecture">
    <option value="">-- 選択してください --</option>
    <option value="tokyo">東京都</option>
    <option value="osaka">大阪府</option>
    <option value="fukuoka">福岡県</option>
  </select>
  <br><br>

  <label>コメント: </label><br>
  <textarea ng-model="comment" rows="3" cols="40" placeholder="ご自由にどうぞ"></textarea>
  <br><br>

  <label>
    <input type="checkbox" ng-model="agree"> 利用規約に同意する
  </label>
  <br><br>

  <h3>入力内容の確認</h3>
  <ul>
    <li>名前: {{ name || "(未入力)" }}</li>
    <li>性別: {{ gender || "(未選択)" }}</li>
    <li>都道府県: {{ prefecture || "(未選択)" }}</li>
    <li>コメント: {{ comment || "(未入力)" }}</li>
    <li>同意: {{ agree ? "同意済み" : "未同意" }}</li>
  </ul>

</body>
</html>
```

### ポイントまとめ
- `ng-model` はフォーム要素と `$scope` を双方向にバインドするディレクティブ
- `<input>`, `<select>`, `<textarea>`, `<input type="checkbox">`, `<input type="radio">` で使える
- ユーザーの入力が即座に `$scope` に反映され、`{{ }}` の表示もリアルタイムで更新される
- フォームのプレビュー機能などをコードなしで実現できる

---

## 7. 最初の完全なAngularJSアプリケーション

ここまで学んだことを組み合わせて、実用的なアプリケーションを作ってみましょう。

### 7.1 ToDoリスト（簡易版）

```html
<!DOCTYPE html>
<html ng-app="todoApp">
<head>
  <meta charset="UTF-8">
  <title>ToDoリスト - AngularJS</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js"></script>
  <style>
    body {
      font-family: sans-serif;
      max-width: 500px;
      margin: 40px auto;
      padding: 0 20px;
    }
    .done {
      text-decoration: line-through;
      color: #999;
    }
    ul { list-style: none; padding: 0; }
    li {
      padding: 8px 0;
      border-bottom: 1px solid #eee;
    }
    input[type="text"] {
      padding: 8px;
      width: 300px;
    }
    button {
      padding: 8px 16px;
      cursor: pointer;
    }
    .stats {
      margin-top: 16px;
      color: #666;
      font-size: 14px;
    }
  </style>
  <script>
    var app = angular.module('todoApp', []);

    app.controller('TodoController', ['$scope', function($scope) {
      // ToDoリストの初期データ
      $scope.todos = [
        { text: 'AngularJSの基本を学ぶ', done: true },
        { text: 'コントローラーを理解する', done: false },
        { text: 'データバインディングを試す', done: false }
      ];

      // 新しいタスクのテキスト
      $scope.newTodoText = '';

      // タスクを追加する
      $scope.addTodo = function() {
        if ($scope.newTodoText.trim() === '') return;

        $scope.todos.push({
          text: $scope.newTodoText,
          done: false
        });
        $scope.newTodoText = ''; // 入力欄をクリア
      };

      // タスクを削除する
      $scope.removeTodo = function(index) {
        $scope.todos.splice(index, 1);
      };

      // 残りのタスク数を返す
      $scope.remaining = function() {
        var count = 0;
        for (var i = 0; i < $scope.todos.length; i++) {
          if (!$scope.todos[i].done) {
            count++;
          }
        }
        return count;
      };
    }]);
  </script>
</head>
<body ng-controller="TodoController">

  <h1>ToDoリスト</h1>

  <!-- タスク追加フォーム -->
  <input type="text" ng-model="newTodoText" placeholder="新しいタスクを入力">
  <button ng-click="addTodo()">追加</button>

  <!-- タスク一覧 -->
  <ul>
    <li ng-repeat="todo in todos">
      <input type="checkbox" ng-model="todo.done">
      <span ng-class="{ done: todo.done }">{{ todo.text }}</span>
      <button ng-click="removeTodo($index)" style="float:right; font-size:12px;">削除</button>
    </li>
  </ul>

  <!-- 統計情報 -->
  <p class="stats">
    全 {{ todos.length }} 件中、残り {{ remaining() }} 件
  </p>

</body>
</html>
```

このアプリケーションでは以下の機能が動作します：

1. テキストを入力して「追加」ボタンでタスクを追加
2. チェックボックスで完了・未完了を切り替え（取り消し線が付く）
3. 「削除」ボタンでタスクを削除
4. 残りのタスク数がリアルタイムで更新

### 7.2 アプリケーション構造の解説

```
+-------------------------------------------------------+
|  ToDoアプリの構造                                       |
|                                                       |
|  ng-app="todoApp"                                     |
|    └── angular.module('todoApp', [])                  |
|          └── TodoController                           |
|                ├── $scope.todos（データ）               |
|                ├── $scope.newTodoText（入力値）          |
|                ├── $scope.addTodo()（追加処理）          |
|                ├── $scope.removeTodo()（削除処理）       |
|                └── $scope.remaining()（残数計算）        |
|                                                       |
|  HTML側                                               |
|    ├── ng-model="newTodoText"（入力欄）                  |
|    ├── ng-click="addTodo()"（追加ボタン）                |
|    ├── ng-repeat="todo in todos"（リスト表示）           |
|    ├── ng-model="todo.done"（チェックボックス）           |
|    ├── ng-class="{ done: todo.done }"（スタイル切替）    |
|    └── ng-click="removeTodo($index)"（削除ボタン）       |
+-------------------------------------------------------+
```

> **よくある間違い**
> `ng-repeat` 内で `$index` を使うとき、`$` を忘れがちです。`index` ではなく `$index` と書きましょう。これはAngularJSが提供する特別な変数です。

### ポイントまとめ
- モジュール → コントローラー → ビュー の順で構築する
- `ng-click` でボタンのクリックイベントを処理できる
- `ng-repeat` で配列の各要素を繰り返し表示できる
- `ng-class` でCSSクラスを動的に切り替えられる
- `$scope` のデータが変わるとHTMLが自動的に更新される

---

## 第1章のまとめ

| 学んだこと | キーワード |
|-----------|-----------|
| AngularJSとは | JavaScript フレームワーク、SPA |
| 環境構築 | CDN、`<script>` タグ |
| アプリのルート | `ng-app` ディレクティブ |
| モジュール定義 | `angular.module('名前', [])` |
| コントローラー | `app.controller()`, `$scope` |
| 式展開 | `{{ }}` |
| 双方向バインディング | `ng-model` |
| 依存性注入 | DI、配列記法 |

次の章では、データバインディングと `$scope` の仕組みをさらに深く掘り下げます。`$watch`、`$apply`、`$digest` サイクルなど、AngularJSの内部動作を理解することで、より効率的なアプリケーションを作れるようになります。

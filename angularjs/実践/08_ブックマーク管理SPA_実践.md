# 実践課題08：ブックマーク管理SPA ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第4章（フィルターとサービス）、第5章（カスタムディレクティブ）、第7章（ルーティング）
> **課題の種類**: ミニプロジェクト
> **学習目標**: `ngRoute` によるルーティング（Routing）設定、`$routeParams` によるパラメータ受け渡し、サービスでのデータ共有を組み合わせたマルチページSPAを構築する

---

## 完成イメージ

ブックマーク一覧、カテゴリ別表示、ブックマーク詳細・編集ができるSPAです。

```
┌─────────────────────────────────────────────┐
│  [一覧] [カテゴリ] [追加]  ← ナビゲーション   │
├─────────────────────────────────────────────┤
│                                             │
│  #/home（一覧ページ）                        │
│  検索: [________]                            │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │ ● MDN Web Docs          [技術]  [詳細]│   │
│  │ ● Qiita                 [技術]  [詳細]│   │
│  │ ● YouTube               [動画]  [詳細]│   │
│  │ ● Amazon                [買物]  [詳細]│   │
│  └──────────────────────────────────────┘   │
│                                             │
│  #/detail/1（詳細ページ）                     │
│  ┌──────────────────────────────────────┐   │
│  │ MDN Web Docs                         │   │
│  │ URL: https://developer.mozilla.org   │   │
│  │ カテゴリ: 技術                        │   │
│  │ メモ: Web技術のリファレンス            │   │
│  │ [編集] [削除] [戻る]                  │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## 課題の要件

1. `ngRoute` で3つのルート（一覧 / 詳細 / 追加・編集）を設定する
2. ブックマークデータをサービス（`factory`）で一元管理する
3. 一覧ページでキーワード検索・カテゴリ絞り込みができる
4. 詳細ページで `$routeParams` からIDを受け取り、該当データを表示する
5. 追加・編集ページでフォームバリデーション付きの入力フォームを表示する
6. ナビゲーションリンクで各ページを遷移できる
7. `$location` でプログラム的なページ遷移を行う

---

## ステップガイド

<details>
<summary>ステップ1：ngRoute の導入とルート定義</summary>

ngRouteは別モジュールなのでCDNを追加します。

```html
<script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular-route.min.js"></script>
```

```javascript
var app = angular.module('bookmarkApp', ['ngRoute']);

app.config(function($routeProvider) {
  $routeProvider
    .when('/home', {
      template: '...一覧テンプレート...',
      controller: 'HomeCtrl'
    })
    .when('/detail/:id', {
      template: '...詳細テンプレート...',
      controller: 'DetailCtrl'
    })
    .when('/add', {
      template: '...追加テンプレート...',
      controller: 'AddCtrl'
    })
    .otherwise({ redirectTo: '/home' });
});
```

</details>

<details>
<summary>ステップ2：データ管理サービスを作る</summary>

```javascript
app.factory('BookmarkService', function() {
  var bookmarks = [ /* 初期データ */ ];
  var nextId = 5;
  return {
    getAll: function() { return bookmarks; },
    getById: function(id) {
      return bookmarks.find(function(b) { return b.id === id; });
    },
    add: function(bookmark) { /* ... */ },
    update: function(id, data) { /* ... */ },
    remove: function(id) { /* ... */ }
  };
});
```

</details>

<details>
<summary>ステップ3：$routeParams でIDを受け取る</summary>

```javascript
app.controller('DetailCtrl', function($scope, $routeParams, BookmarkService) {
  var id = parseInt($routeParams.id);
  $scope.bookmark = BookmarkService.getById(id);
});
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```html
<!DOCTYPE html>
<html ng-app="bookmarkApp">
<head>
  <meta charset="UTF-8">
  <title>ブックマーク管理</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js"></script>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular-route.min.js"></script>
  <style>
    body { font-family: sans-serif; background: #f5f5f5; margin: 0; padding: 0; }
    .navbar { background: #1976d2; padding: 12px 20px; display: flex; gap: 16px; align-items: center; }
    .navbar a { color: white; text-decoration: none; font-size: 14px; padding: 6px 12px; border-radius: 6px; }
    .navbar a:hover { background: rgba(255,255,255,0.15); }
    .navbar a.active { background: rgba(255,255,255,0.25); font-weight: bold; }
    .navbar .title { font-size: 18px; font-weight: bold; color: white; margin-right: auto; }
    .container { max-width: 600px; margin: 20px auto; padding: 0 20px; }
    .search { width: 100%; padding: 10px 12px; border: 1px solid #ddd; border-radius: 8px;
              font-size: 14px; margin-bottom: 12px; box-sizing: border-box; }
    .filters { display: flex; gap: 6px; margin-bottom: 16px; flex-wrap: wrap; }
    .chip { padding: 4px 12px; border: 1px solid #ddd; border-radius: 14px; background: white;
            cursor: pointer; font-size: 12px; }
    .chip.on { background: #1976d2; color: white; border-color: #1976d2; }
    .list-item { display: flex; align-items: center; padding: 12px 16px; background: white;
                 border-radius: 8px; margin-bottom: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
    .list-item .dot { width: 10px; height: 10px; border-radius: 50%; margin-right: 12px; }
    .list-item .info { flex: 1; }
    .list-item .name { font-weight: bold; font-size: 14px; }
    .list-item .url { color: #888; font-size: 12px; }
    .tag { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px; color: white; margin-left: 8px; }
    .detail-btn { padding: 5px 12px; background: #e3f2fd; color: #1976d2; border: none;
                  border-radius: 6px; cursor: pointer; font-size: 12px; }
    .card { background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .card h2 { margin-top: 0; }
    .card .field { margin-bottom: 12px; }
    .card .field-label { font-weight: bold; font-size: 13px; color: #555; margin-bottom: 2px; }
    .card .field-value { font-size: 14px; }
    .card .field-value a { color: #1976d2; }
    .btn { padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; margin-right: 6px; }
    .btn-primary { background: #1976d2; color: white; }
    .btn-danger { background: #f44336; color: white; }
    .btn-default { background: #eee; color: #555; }
    .form-group { margin-bottom: 14px; }
    .form-group label { display: block; font-weight: bold; font-size: 13px; margin-bottom: 4px; }
    .form-group input, .form-group select, .form-group textarea {
      width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; box-sizing: border-box; }
    .form-group textarea { height: 60px; resize: vertical; }
    .form-group .error { color: #f44336; font-size: 12px; margin-top: 2px; }
    .empty { text-align: center; color: #ccc; padding: 40px; }
    .cat-tech { background: #2196f3; }
    .cat-video { background: #f44336; }
    .cat-shop { background: #ff9800; }
    .cat-news { background: #4caf50; }
    .cat-other { background: #9e9e9e; }
    .dot-tech { background: #2196f3; }
    .dot-video { background: #f44336; }
    .dot-shop { background: #ff9800; }
    .dot-news { background: #4caf50; }
    .dot-other { background: #9e9e9e; }
  </style>
</head>
<body>

  <!-- ナビゲーション -->
  <div class="navbar">
    <span class="title">Bookmarks</span>
    <a href="#!/home">一覧</a>
    <a href="#!/add">追加</a>
  </div>

  <!-- ルーティングビュー -->
  <div class="container">
    <div ng-view></div>
  </div>

  <!-- 一覧テンプレート -->
  <script type="text/ng-template" id="home.html">
    <input class="search" type="text" ng-model="search" placeholder="キーワードで検索...">
    <div class="filters">
      <span class="chip" ng-class="{'on': category === 'all'}" ng-click="category = 'all'">すべて</span>
      <span class="chip" ng-class="{'on': category === c}" ng-click="category = c"
            ng-repeat="c in categories">{{ c }}</span>
    </div>
    <div class="list-item" ng-repeat="b in bookmarks | filter:search | filter:catFilter track by b.id">
      <div class="dot" ng-class="getDotClass(b.category)"></div>
      <div class="info">
        <div class="name">{{ b.name }}</div>
        <div class="url">{{ b.url }}</div>
      </div>
      <span class="tag" ng-class="getTagClass(b.category)">{{ b.category }}</span>
      <button class="detail-btn" ng-click="goDetail(b.id)" style="margin-left: 8px;">詳細</button>
    </div>
    <div class="empty" ng-if="(bookmarks | filter:search | filter:catFilter).length === 0">
      ブックマークが見つかりません
    </div>
  </script>

  <!-- 詳細テンプレート -->
  <script type="text/ng-template" id="detail.html">
    <div class="card" ng-if="bookmark">
      <h2>{{ bookmark.name }}</h2>
      <div class="field">
        <div class="field-label">URL</div>
        <div class="field-value"><a ng-href="{{ bookmark.url }}" target="_blank">{{ bookmark.url }}</a></div>
      </div>
      <div class="field">
        <div class="field-label">カテゴリ</div>
        <div class="field-value">
          <span class="tag" ng-class="getTagClass(bookmark.category)">{{ bookmark.category }}</span>
        </div>
      </div>
      <div class="field">
        <div class="field-label">メモ</div>
        <div class="field-value">{{ bookmark.memo || 'なし' }}</div>
      </div>
      <div class="field">
        <div class="field-label">追加日</div>
        <div class="field-value">{{ bookmark.createdAt }}</div>
      </div>
      <div style="margin-top: 16px;">
        <button class="btn btn-primary" ng-click="goEdit()">編集</button>
        <button class="btn btn-danger" ng-click="remove()">削除</button>
        <button class="btn btn-default" ng-click="goBack()">戻る</button>
      </div>
    </div>
    <div class="empty" ng-if="!bookmark">ブックマークが見つかりません</div>
  </script>

  <!-- 追加・編集テンプレート -->
  <script type="text/ng-template" id="form.html">
    <div class="card">
      <h2>{{ isEdit ? 'ブックマークを編集' : '新しいブックマークを追加' }}</h2>
      <form name="bmForm" ng-submit="save()" novalidate>
        <div class="form-group">
          <label>名前 *</label>
          <input type="text" name="name" ng-model="formData.name" required placeholder="サイト名">
          <div class="error" ng-show="bmForm.name.$dirty && bmForm.name.$error.required">名前は必須です</div>
        </div>
        <div class="form-group">
          <label>URL *</label>
          <input type="url" name="url" ng-model="formData.url" required placeholder="https://example.com">
          <div class="error" ng-show="bmForm.url.$dirty && bmForm.url.$error.required">URLは必須です</div>
          <div class="error" ng-show="bmForm.url.$dirty && bmForm.url.$error.url">正しいURLを入力してください</div>
        </div>
        <div class="form-group">
          <label>カテゴリ *</label>
          <select ng-model="formData.category" required>
            <option value="">選択してください</option>
            <option ng-repeat="c in categories" value="{{ c }}">{{ c }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>メモ</label>
          <textarea ng-model="formData.memo" placeholder="メモ（任意）"></textarea>
        </div>
        <button type="submit" class="btn btn-primary" ng-disabled="bmForm.$invalid">
          {{ isEdit ? '更新' : '追加' }}
        </button>
        <button type="button" class="btn btn-default" ng-click="cancel()">キャンセル</button>
      </form>
    </div>
  </script>

  <script>
    var app = angular.module('bookmarkApp', ['ngRoute']);

    // ルーティング設定
    app.config(function($routeProvider) {
      $routeProvider
        .when('/home', {
          templateUrl: 'home.html',
          controller: 'HomeCtrl'
        })
        .when('/detail/:id', {
          templateUrl: 'detail.html',
          controller: 'DetailCtrl'
        })
        .when('/add', {
          templateUrl: 'form.html',
          controller: 'FormCtrl'
        })
        .when('/edit/:id', {
          templateUrl: 'form.html',
          controller: 'FormCtrl'
        })
        .otherwise({ redirectTo: '/home' });
    });

    // データ管理サービス
    app.factory('BookmarkService', function() {
      var nextId = 5;
      var bookmarks = [
        { id: 1, name: 'MDN Web Docs', url: 'https://developer.mozilla.org', category: '技術', memo: 'Web技術の公式リファレンス', createdAt: '2024-01-15' },
        { id: 2, name: 'Qiita', url: 'https://qiita.com', category: '技術', memo: 'エンジニア向け技術情報共有サイト', createdAt: '2024-02-10' },
        { id: 3, name: 'YouTube', url: 'https://www.youtube.com', category: '動画', memo: '動画プラットフォーム', createdAt: '2024-03-05' },
        { id: 4, name: 'Amazon', url: 'https://www.amazon.co.jp', category: '買物', memo: 'オンラインショッピング', createdAt: '2024-04-20' }
      ];

      return {
        getAll: function() { return bookmarks; },
        getById: function(id) {
          for (var i = 0; i < bookmarks.length; i++) {
            if (bookmarks[i].id === id) return bookmarks[i];
          }
          return null;
        },
        add: function(data) {
          var bookmark = angular.copy(data);
          bookmark.id = nextId++;
          bookmark.createdAt = new Date().toISOString().split('T')[0];
          bookmarks.push(bookmark);
          return bookmark;
        },
        update: function(id, data) {
          var bm = this.getById(id);
          if (bm) {
            bm.name = data.name;
            bm.url = data.url;
            bm.category = data.category;
            bm.memo = data.memo;
          }
          return bm;
        },
        remove: function(id) {
          for (var i = 0; i < bookmarks.length; i++) {
            if (bookmarks[i].id === id) {
              bookmarks.splice(i, 1);
              return true;
            }
          }
          return false;
        },
        getCategories: function() {
          return ['技術', '動画', '買物', 'ニュース', 'その他'];
        }
      };
    });

    // カテゴリの色分けヘルパー
    app.factory('CategoryHelper', function() {
      var tagMap = { '技術': 'cat-tech', '動画': 'cat-video', '買物': 'cat-shop', 'ニュース': 'cat-news' };
      var dotMap = { '技術': 'dot-tech', '動画': 'dot-video', '買物': 'dot-shop', 'ニュース': 'dot-news' };
      return {
        getTagClass: function(cat) { return tagMap[cat] || 'cat-other'; },
        getDotClass: function(cat) { return dotMap[cat] || 'dot-other'; }
      };
    });

    // 一覧コントローラ
    app.controller('HomeCtrl', function($scope, $location, BookmarkService, CategoryHelper) {
      $scope.bookmarks = BookmarkService.getAll();
      $scope.categories = BookmarkService.getCategories();
      $scope.category = 'all';
      $scope.catFilter = {};
      $scope.search = '';

      $scope.$watch('category', function(cat) {
        $scope.catFilter = (cat === 'all') ? {} : { category: cat };
      });

      $scope.getTagClass = CategoryHelper.getTagClass;
      $scope.getDotClass = CategoryHelper.getDotClass;

      $scope.goDetail = function(id) {
        $location.path('/detail/' + id);
      };
    });

    // 詳細コントローラ
    app.controller('DetailCtrl', function($scope, $routeParams, $location, BookmarkService, CategoryHelper) {
      var id = parseInt($routeParams.id);
      $scope.bookmark = BookmarkService.getById(id);
      $scope.getTagClass = CategoryHelper.getTagClass;

      $scope.goEdit = function() {
        $location.path('/edit/' + id);
      };

      $scope.remove = function() {
        if (confirm('削除しますか？')) {
          BookmarkService.remove(id);
          $location.path('/home');
        }
      };

      $scope.goBack = function() {
        $location.path('/home');
      };
    });

    // 追加・編集コントローラ
    app.controller('FormCtrl', function($scope, $routeParams, $location, BookmarkService) {
      $scope.categories = BookmarkService.getCategories();
      $scope.isEdit = !!$routeParams.id;
      $scope.formData = {};

      if ($scope.isEdit) {
        var existing = BookmarkService.getById(parseInt($routeParams.id));
        if (existing) {
          $scope.formData = angular.copy(existing);
        }
      }

      $scope.save = function() {
        if ($scope.bmForm.$valid) {
          if ($scope.isEdit) {
            BookmarkService.update(parseInt($routeParams.id), $scope.formData);
          } else {
            BookmarkService.add($scope.formData);
          }
          $location.path('/home');
        }
      };

      $scope.cancel = function() {
        $location.path('/home');
      };
    });
  </script>

</body>
</html>
```

</details>

<details>
<summary>解答例（改良版 ─ Controller As + resolve + お気に入り機能）</summary>

```html
<!DOCTYPE html>
<html ng-app="bookmarkApp">
<head>
  <meta charset="UTF-8">
  <title>ブックマーク管理（改良版）</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js"></script>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular-route.min.js"></script>
  <style>
    body { font-family: sans-serif; background: #f0f2f5; margin: 0; }
    .nav { background: #1565c0; padding: 0 20px; display: flex; align-items: center; height: 50px; }
    .nav .logo { font-size: 18px; font-weight: bold; color: white; margin-right: auto; }
    .nav a { color: rgba(255,255,255,0.85); text-decoration: none; font-size: 13px; padding: 6px 14px;
             border-radius: 6px; margin-left: 4px; transition: background 0.2s; }
    .nav a:hover { background: rgba(255,255,255,0.15); }
    .wrap { max-width: 620px; margin: 20px auto; padding: 0 20px; }
    .search { width: 100%; padding: 10px 14px; border: 1px solid #ddd; border-radius: 8px;
              font-size: 14px; margin-bottom: 12px; box-sizing: border-box; }
    .search:focus { border-color: #1976d2; outline: none; }
    .chips { display: flex; gap: 6px; margin-bottom: 16px; flex-wrap: wrap; }
    .chip { padding: 4px 12px; border: 1px solid #ddd; border-radius: 14px; background: white;
            cursor: pointer; font-size: 12px; transition: all 0.2s; }
    .chip:hover { background: #e3f2fd; }
    .chip.on { background: #1976d2; color: white; border-color: #1976d2; }
    .item { display: flex; align-items: center; padding: 14px 16px; background: white;
            border-radius: 10px; margin-bottom: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.04);
            transition: transform 0.15s; cursor: pointer; }
    .item:hover { transform: translateX(4px); box-shadow: 0 2px 10px rgba(0,0,0,0.08); }
    .item .dot { width: 8px; height: 8px; border-radius: 50%; margin-right: 12px; flex-shrink: 0; }
    .item .info { flex: 1; min-width: 0; }
    .item .name { font-weight: bold; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .item .url { color: #888; font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .tag { padding: 2px 8px; border-radius: 10px; font-size: 11px; color: white; white-space: nowrap; }
    .fav-btn { background: none; border: none; font-size: 18px; cursor: pointer; margin-left: 8px; }
    .card { background: white; border-radius: 14px; padding: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
    .card h2 { margin-top: 0; }
    .field { margin-bottom: 14px; }
    .field-label { font-weight: bold; font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 2px; }
    .field-value { font-size: 14px; }
    .field-value a { color: #1976d2; }
    .btn { padding: 8px 18px; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; margin-right: 6px; transition: opacity 0.2s; }
    .btn:hover { opacity: 0.85; }
    .btn-p { background: #1976d2; color: white; }
    .btn-d { background: #f44336; color: white; }
    .btn-g { background: #eee; color: #555; }
    .fg { margin-bottom: 14px; }
    .fg label { display: block; font-weight: bold; font-size: 13px; margin-bottom: 4px; }
    .fg input, .fg select, .fg textarea {
      width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; box-sizing: border-box; }
    .fg input.ng-dirty.ng-invalid { border-color: #f44336; }
    .fg textarea { height: 60px; }
    .fg .err { color: #f44336; font-size: 12px; margin-top: 2px; }
    .empty { text-align: center; color: #ccc; padding: 40px; }
    .count { color: #888; font-size: 13px; margin-bottom: 8px; }
    .c-tech { background: #1976d2; } .c-vid { background: #e53935; } .c-shop { background: #f57c00; }
    .c-news { background: #388e3c; } .c-etc { background: #757575; }
    .d-tech { background: #1976d2; } .d-vid { background: #e53935; } .d-shop { background: #f57c00; }
    .d-news { background: #388e3c; } .d-etc { background: #757575; }
  </style>
</head>
<body>

  <div class="nav">
    <span class="logo">Bookmarks</span>
    <a href="#!/home">一覧</a>
    <a href="#!/favorites">お気に入り</a>
    <a href="#!/add">追加</a>
  </div>

  <div class="wrap">
    <div ng-view></div>
  </div>

  <!-- テンプレート: 一覧 -->
  <script type="text/ng-template" id="home.html">
    <input class="search" ng-model="vm.search" placeholder="キーワードで検索..."
           ng-model-options="{ debounce: 200 }">
    <div class="chips">
      <span class="chip" ng-class="{'on': vm.cat === ''}" ng-click="vm.cat = ''">すべて</span>
      <span class="chip" ng-repeat="c in vm.categories" ng-class="{'on': vm.cat === c}"
            ng-click="vm.cat = c">{{ c }}</span>
    </div>
    <div class="count">{{ vm.filtered().length }} / {{ vm.bookmarks.length }}件</div>
    <div class="item" ng-repeat="b in vm.filtered() track by b.id" ng-click="vm.goDetail(b.id)">
      <div class="dot" ng-class="vm.dotClass(b.category)"></div>
      <div class="info">
        <div class="name">{{ b.name }}</div>
        <div class="url">{{ b.url }}</div>
      </div>
      <span class="tag" ng-class="vm.tagClass(b.category)">{{ b.category }}</span>
      <button class="fav-btn" ng-click="vm.toggleFav(b, $event)">{{ b.favorite ? '★' : '☆' }}</button>
    </div>
    <div class="empty" ng-if="vm.filtered().length === 0">ブックマークが見つかりません</div>
  </script>

  <!-- テンプレート: お気に入り -->
  <script type="text/ng-template" id="favorites.html">
    <h2>お気に入り</h2>
    <div class="item" ng-repeat="b in vm.favorites track by b.id" ng-click="vm.goDetail(b.id)">
      <div class="dot" ng-class="vm.dotClass(b.category)"></div>
      <div class="info">
        <div class="name">{{ b.name }}</div>
        <div class="url">{{ b.url }}</div>
      </div>
      <span class="tag" ng-class="vm.tagClass(b.category)">{{ b.category }}</span>
    </div>
    <div class="empty" ng-if="vm.favorites.length === 0">お気に入りはまだありません</div>
  </script>

  <!-- テンプレート: 詳細 -->
  <script type="text/ng-template" id="detail.html">
    <div class="card" ng-if="vm.bookmark">
      <h2>{{ vm.bookmark.name }}</h2>
      <div class="field">
        <div class="field-label">URL</div>
        <div class="field-value"><a ng-href="{{ vm.bookmark.url }}" target="_blank">{{ vm.bookmark.url }}</a></div>
      </div>
      <div class="field">
        <div class="field-label">カテゴリ</div>
        <div class="field-value"><span class="tag" ng-class="vm.tagClass(vm.bookmark.category)">{{ vm.bookmark.category }}</span></div>
      </div>
      <div class="field">
        <div class="field-label">メモ</div>
        <div class="field-value">{{ vm.bookmark.memo || 'なし' }}</div>
      </div>
      <div class="field">
        <div class="field-label">追加日</div>
        <div class="field-value">{{ vm.bookmark.createdAt }}</div>
      </div>
      <div style="margin-top: 16px;">
        <button class="btn btn-p" ng-click="vm.edit()">編集</button>
        <button class="btn btn-d" ng-click="vm.remove()">削除</button>
        <button class="btn btn-g" ng-click="vm.back()">戻る</button>
      </div>
    </div>
  </script>

  <!-- テンプレート: フォーム -->
  <script type="text/ng-template" id="form.html">
    <div class="card">
      <h2>{{ vm.isEdit ? '編集' : '新規追加' }}</h2>
      <form name="vm.bmForm" ng-submit="vm.save()" novalidate>
        <div class="fg">
          <label>名前 *</label>
          <input type="text" name="name" ng-model="vm.data.name" required placeholder="サイト名">
          <div class="err" ng-show="vm.bmForm.name.$dirty && vm.bmForm.name.$error.required">必須です</div>
        </div>
        <div class="fg">
          <label>URL *</label>
          <input type="url" name="url" ng-model="vm.data.url" required placeholder="https://...">
          <div class="err" ng-show="vm.bmForm.url.$dirty && vm.bmForm.url.$error.required">必須です</div>
          <div class="err" ng-show="vm.bmForm.url.$dirty && vm.bmForm.url.$error.url">正しいURLを入力してください</div>
        </div>
        <div class="fg">
          <label>カテゴリ *</label>
          <select ng-model="vm.data.category" ng-options="c for c in vm.categories" required>
            <option value="">選択</option>
          </select>
        </div>
        <div class="fg">
          <label>メモ</label>
          <textarea ng-model="vm.data.memo" placeholder="メモ（任意）"></textarea>
        </div>
        <button type="submit" class="btn btn-p" ng-disabled="vm.bmForm.$invalid">
          {{ vm.isEdit ? '更新' : '追加' }}
        </button>
        <button type="button" class="btn btn-g" ng-click="vm.cancel()">キャンセル</button>
      </form>
    </div>
  </script>

  <script>
    var app = angular.module('bookmarkApp', ['ngRoute']);

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider
        .when('/home', { templateUrl: 'home.html', controller: 'HomeCtrl', controllerAs: 'vm' })
        .when('/favorites', { templateUrl: 'favorites.html', controller: 'FavCtrl', controllerAs: 'vm' })
        .when('/detail/:id', { templateUrl: 'detail.html', controller: 'DetailCtrl', controllerAs: 'vm' })
        .when('/add', { templateUrl: 'form.html', controller: 'FormCtrl', controllerAs: 'vm' })
        .when('/edit/:id', { templateUrl: 'form.html', controller: 'FormCtrl', controllerAs: 'vm' })
        .otherwise({ redirectTo: '/home' });
    }]);

    // サービス
    app.factory('BookmarkService', function() {
      var nextId = 5;
      var bms = [
        { id: 1, name: 'MDN Web Docs', url: 'https://developer.mozilla.org', category: '技術', memo: 'Web技術の公式リファレンス', createdAt: '2024-01-15', favorite: true },
        { id: 2, name: 'Qiita', url: 'https://qiita.com', category: '技術', memo: 'エンジニア向け技術情報', createdAt: '2024-02-10', favorite: false },
        { id: 3, name: 'YouTube', url: 'https://www.youtube.com', category: '動画', memo: '動画プラットフォーム', createdAt: '2024-03-05', favorite: true },
        { id: 4, name: 'Amazon', url: 'https://www.amazon.co.jp', category: '買物', memo: 'ショッピング', createdAt: '2024-04-20', favorite: false }
      ];
      var cats = ['技術', '動画', '買物', 'ニュース', 'その他'];
      var tagMap = { '技術': 'c-tech', '動画': 'c-vid', '買物': 'c-shop', 'ニュース': 'c-news' };
      var dotMap = { '技術': 'd-tech', '動画': 'd-vid', '買物': 'd-shop', 'ニュース': 'd-news' };

      return {
        all: function() { return bms; },
        get: function(id) { return bms.find(function(b) { return b.id === id; }); },
        favorites: function() { return bms.filter(function(b) { return b.favorite; }); },
        add: function(d) { d = angular.copy(d); d.id = nextId++; d.createdAt = new Date().toISOString().slice(0,10); d.favorite = false; bms.push(d); },
        update: function(id, d) { var b = this.get(id); if (b) { b.name=d.name; b.url=d.url; b.category=d.category; b.memo=d.memo; } },
        remove: function(id) { var i = bms.findIndex(function(b){return b.id===id;}); if(i>=0) bms.splice(i,1); },
        cats: function() { return cats; },
        tagClass: function(c) { return tagMap[c] || 'c-etc'; },
        dotClass: function(c) { return dotMap[c] || 'd-etc'; }
      };
    });

    app.controller('HomeCtrl', ['$location', 'BookmarkService', function($location, BS) {
      var vm = this;
      vm.bookmarks = BS.all();
      vm.categories = BS.cats();
      vm.search = '';
      vm.cat = '';
      vm.tagClass = BS.tagClass;
      vm.dotClass = BS.dotClass;
      vm.filtered = function() {
        return vm.bookmarks.filter(function(b) {
          if (vm.cat && b.category !== vm.cat) return false;
          if (vm.search && b.name.toLowerCase().indexOf(vm.search.toLowerCase()) === -1) return false;
          return true;
        });
      };
      vm.goDetail = function(id) { $location.path('/detail/' + id); };
      vm.toggleFav = function(b, $event) { $event.stopPropagation(); b.favorite = !b.favorite; };
    }]);

    app.controller('FavCtrl', ['$location', 'BookmarkService', function($location, BS) {
      var vm = this;
      vm.favorites = BS.favorites();
      vm.tagClass = BS.tagClass;
      vm.dotClass = BS.dotClass;
      vm.goDetail = function(id) { $location.path('/detail/' + id); };
    }]);

    app.controller('DetailCtrl', ['$routeParams', '$location', 'BookmarkService', function($routeParams, $location, BS) {
      var vm = this;
      vm.bookmark = BS.get(parseInt($routeParams.id));
      vm.tagClass = BS.tagClass;
      vm.edit = function() { $location.path('/edit/' + $routeParams.id); };
      vm.remove = function() { if(confirm('削除しますか？')){ BS.remove(parseInt($routeParams.id)); $location.path('/home'); }};
      vm.back = function() { $location.path('/home'); };
    }]);

    app.controller('FormCtrl', ['$routeParams', '$location', 'BookmarkService', function($routeParams, $location, BS) {
      var vm = this;
      vm.categories = BS.cats();
      vm.isEdit = !!$routeParams.id;
      vm.data = vm.isEdit ? angular.copy(BS.get(parseInt($routeParams.id))) : {};
      vm.save = function() {
        if (vm.bmForm.$valid) {
          if (vm.isEdit) BS.update(parseInt($routeParams.id), vm.data);
          else BS.add(vm.data);
          $location.path('/home');
        }
      };
      vm.cancel = function() { $location.path('/home'); };
    }]);
  </script>

</body>
</html>
```

**初心者向けとの違い:**
- `controllerAs: 'vm'` をルート定義に記載し、Controller As 構文をルーティングと組み合わせ
- お気に入り機能（星マーク）とお気に入り専用ページを追加
- 明示的な DI アノテーション `['$location', function($location) {...}]` でミニファイ安全
- 検索のデバウンス処理（`ng-model-options`）でパフォーマンス改善
- カテゴリ・色分けのロジックをサービスに集約してDRY原則を実践
- `$event.stopPropagation()` で星クリックが行クリック（詳細遷移）と競合しないように制御

</details>

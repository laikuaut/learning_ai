# 実践課題11：設計課題 ─ 大学Webサイトの情報設計 ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第1章〜第8章（すべての章）
> **課題の種類**: 設計課題
> **学習目標**: 要件からHTML構造を設計する力を養う。適切なセマンティック要素の選択、見出し階層の設計、アクセシビリティへの配慮を実践的に学ぶ

---

## 課題の説明

あなたは架空の「テクノロジー大学」のWebサイトリニューアルプロジェクトにHTML担当として参加しています。以下の要件を読み、トップページのHTML構造を設計・実装してください。

**この課題では、CSSでの見た目よりもHTML構造の設計が評価ポイントです。**

---

## 要件

### ページに必要な要素

1. **ヘッダー**
   - 大学名とロゴ（画像）
   - グローバルナビゲーション（受験生の方、在学生の方、卒業生の方、企業の方、アクセス）
   - 検索フォーム

2. **メインビジュアル**
   - キャッチコピーと画像
   - CTAボタン（資料請求、オープンキャンパス予約）

3. **お知らせセクション**
   - お知らせ一覧（最新5件、日付・カテゴリ・タイトル）
   - カテゴリは「重要」「イベント」「学事」「その他」の4種

4. **学部紹介セクション**
   - 4つの学部（情報工学部、デザイン学部、経営学部、医療情報学部）
   - 各学部に画像、学部名、簡単な説明、「詳しく見る」リンク

5. **イベント情報セクション**
   - 直近のオープンキャンパスの日時と場所
   - 予約フォーム（名前、メール、参加希望日の選択、高校名）

6. **数字で見る大学**
   - 学生数、教員数、就職率、学部数などの統計情報

7. **サイドバー**
   - 重要なお知らせバナー
   - SNSリンク
   - パンフレット請求への誘導

8. **フッター**
   - 大学の住所・連絡先
   - サイトマップ的なリンク群
   - プライバシーポリシーなどの法的リンク

### 設計上の制約

- HTML5のセマンティック要素を適切に使うこと
- 見出し階層（h1〜h4）を正しく設計すること（h1はページに1つ）
- アクセシビリティに配慮すること（ARIA属性、alt属性、label要素）
- フォームにはバリデーションを設定すること
- `<time>` タグで日付を構造化すること
- ナビゲーションには `aria-label` を設定すること

---

## ステップガイド

<details>
<summary>ステップ1：見出し階層を設計する</summary>

まず、ページ全体の見出し階層を紙やテキストで書き出しましょう。

```
h1: テクノロジー大学
├── h2: お知らせ
├── h2: 学部紹介
│   ├── h3: 情報工学部
│   ├── h3: デザイン学部
│   ├── h3: 経営学部
│   └── h3: 医療情報学部
├── h2: イベント情報
│   └── h3: オープンキャンパス予約フォーム
├── h2: 数字で見るテクノロジー大学
├── h2: 重要なお知らせ（aside内）
├── h2: SNS（aside内）
```

h1 → h2 → h3 の順番を守り、階層を飛ばさないことが重要です。

</details>

<details>
<summary>ステップ2：各セクションに使う要素を選ぶ</summary>

| セクション | 主要な要素 | 理由 |
|---|---|---|
| ヘッダー | `<header>`, `<nav>`, `<form>` | ページ全体のヘッダーとナビゲーション |
| メインビジュアル | `<section>`, `<figure>`, `<a>` | 独立したセクション、CTA |
| お知らせ | `<section>`, `<dl>` or `<ul>` | 日付と内容のペア |
| 学部紹介 | `<section>`, `<article>`, `<figure>` | 各学部は独立したコンテンツ |
| イベント | `<section>`, `<form>`, `<fieldset>` | フォームを含むセクション |
| 統計情報 | `<section>`, `<dl>` | 数値と説明のペア |
| サイドバー | `<aside>`, `<section>` | 補足的なコンテンツ |
| フッター | `<footer>`, `<nav>`, `<address>` | ページ全体のフッター |

</details>

<details>
<summary>ステップ3：お知らせの構造を設計する</summary>

お知らせは「日付・カテゴリ・タイトル」のセットです。いくつかの選択肢があります。

**選択肢A：定義リスト（dl）**
```html
<dl>
  <dt><time datetime="2026-04-05">2026年4月5日</time> [重要]</dt>
  <dd><a href="#">入学式の日程変更について</a></dd>
</dl>
```

**選択肢B：順序なしリスト（ul）**
```html
<ul>
  <li>
    <time datetime="2026-04-05">2026年4月5日</time>
    <span>重要</span>
    <a href="#">入学式の日程変更について</a>
  </li>
</ul>
```

どちらも正解ですが、この場合はリスト（ul）の方が自然です。日付とタイトルは「定義と説明」の関係ではないためです。

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="テクノロジー大学は、IT・デザイン・経営・医療情報の4学部を持つ総合大学です。">
  <meta property="og:title" content="テクノロジー大学">
  <meta property="og:description" content="テクノロジーで未来を創る。4学部で学ぶ次世代の人材育成。">
  <meta property="og:type" content="website">
  <title>テクノロジー大学</title>
</head>
<body>
  <!-- ヘッダー -->
  <header>
    <h1>
      <img src="https://via.placeholder.com/40x40/003366/FFF?text=TU" alt="" width="40" height="40">
      テクノロジー大学
    </h1>
    <nav aria-label="グローバルナビゲーション">
      <ul>
        <li><a href="#">受験生の方</a></li>
        <li><a href="#">在学生の方</a></li>
        <li><a href="#">卒業生の方</a></li>
        <li><a href="#">企業の方</a></li>
        <li><a href="#">アクセス</a></li>
      </ul>
    </nav>
    <form action="/search" method="get" role="search">
      <label for="search">サイト内検索：</label>
      <input type="search" id="search" name="q" placeholder="キーワードで検索">
      <button type="submit">検索</button>
    </form>
  </header>

  <main>
    <!-- メインビジュアル -->
    <section aria-label="メインビジュアル">
      <figure>
        <img src="https://via.placeholder.com/800x400/1a73e8/FFF?text=Technology+University"
             alt="テクノロジー大学キャンパスの全景" width="800" height="400">
      </figure>
      <h2>テクノロジーで未来を創る</h2>
      <p>2027年度入学 出願受付中</p>
      <p>
        <a href="#">資料請求はこちら</a>
        <a href="#">オープンキャンパス予約</a>
      </p>
    </section>

    <!-- お知らせ -->
    <section aria-labelledby="news-heading">
      <h2 id="news-heading">お知らせ</h2>
      <ul>
        <li>
          <time datetime="2026-04-05">2026年4月5日</time>
          <span>[重要]</span>
          <a href="#">入学式の日程変更について</a>
        </li>
        <li>
          <time datetime="2026-04-03">2026年4月3日</time>
          <span>[イベント]</span>
          <a href="#">春のオープンキャンパス開催のお知らせ</a>
        </li>
        <li>
          <time datetime="2026-04-01">2026年4月1日</time>
          <span>[学事]</span>
          <a href="#">2026年度前期授業開始日について</a>
        </li>
        <li>
          <time datetime="2026-03-28">2026年3月28日</time>
          <span>[その他]</span>
          <a href="#">図書館の開館時間変更のお知らせ</a>
        </li>
        <li>
          <time datetime="2026-03-25">2026年3月25日</time>
          <span>[重要]</span>
          <a href="#">2026年度入学手続きの締め切りについて</a>
        </li>
      </ul>
      <p><a href="#">お知らせ一覧へ &rarr;</a></p>
    </section>

    <!-- 学部紹介 -->
    <section aria-labelledby="faculty-heading">
      <h2 id="faculty-heading">学部紹介</h2>

      <article>
        <figure>
          <img src="https://via.placeholder.com/200x150/4a90d9/FFF?text=IT"
               alt="情報工学部のイメージ：プログラミングの授業風景" width="200" height="150">
        </figure>
        <h3>情報工学部</h3>
        <p>AI、セキュリティ、ソフトウェア工学を中心に、次世代のIT人材を育成します。</p>
        <p><a href="#">詳しく見る &rarr;</a></p>
      </article>

      <article>
        <figure>
          <img src="https://via.placeholder.com/200x150/e74c3c/FFF?text=Design"
               alt="デザイン学部のイメージ：デザイン制作の授業風景" width="200" height="150">
        </figure>
        <h3>デザイン学部</h3>
        <p>UI/UXデザインからグラフィックまで、デジタル時代のクリエイターを育成します。</p>
        <p><a href="#">詳しく見る &rarr;</a></p>
      </article>

      <article>
        <figure>
          <img src="https://via.placeholder.com/200x150/2ecc71/FFF?text=Business"
               alt="経営学部のイメージ：グループワークの風景" width="200" height="150">
        </figure>
        <h3>経営学部</h3>
        <p>テクノロジーとビジネスの融合。DX時代の経営リーダーを育成します。</p>
        <p><a href="#">詳しく見る &rarr;</a></p>
      </article>

      <article>
        <figure>
          <img src="https://via.placeholder.com/200x150/9b59b6/FFF?text=Medical"
               alt="医療情報学部のイメージ：医療情報システムの実習風景" width="200" height="150">
        </figure>
        <h3>医療情報学部</h3>
        <p>医療とITの架け橋。医療情報技師や診療情報管理士を目指せます。</p>
        <p><a href="#">詳しく見る &rarr;</a></p>
      </article>
    </section>

    <!-- イベント情報 -->
    <section aria-labelledby="event-heading">
      <h2 id="event-heading">イベント情報</h2>
      <p>オープンキャンパス開催日：<time datetime="2026-05-18">2026年5月18日（日）</time> 10:00〜16:00</p>
      <p>会場：テクノロジー大学 メインキャンパス（東京都八王子市）</p>

      <h3>オープンキャンパス予約フォーム</h3>
      <form action="#" method="post">
        <fieldset>
          <legend>参加者情報</legend>

          <p>
            <label for="oc-name">お名前 *：</label><br>
            <input type="text" id="oc-name" name="name" required autocomplete="name">
          </p>

          <p>
            <label for="oc-email">メールアドレス *：</label><br>
            <input type="email" id="oc-email" name="email" required autocomplete="email">
          </p>

          <p>
            <label for="oc-date">参加希望日 *：</label><br>
            <select id="oc-date" name="date" required>
              <option value="">選択してください</option>
              <option value="2026-05-18">2026年5月18日（日）</option>
              <option value="2026-06-15">2026年6月15日（日）</option>
              <option value="2026-07-20">2026年7月20日（日）</option>
            </select>
          </p>

          <p>
            <label for="oc-school">高校名：</label><br>
            <input type="text" id="oc-school" name="school" placeholder="例：○○高等学校">
          </p>
        </fieldset>

        <p>
          <button type="submit">予約する</button>
        </p>
      </form>
    </section>

    <!-- 数字で見る大学 -->
    <section aria-labelledby="numbers-heading">
      <h2 id="numbers-heading">数字で見るテクノロジー大学</h2>
      <dl>
        <dt>学生数</dt>
        <dd>3,200名</dd>

        <dt>教員数</dt>
        <dd>180名</dd>

        <dt>就職率</dt>
        <dd>98.5%</dd>

        <dt>学部数</dt>
        <dd>4学部</dd>

        <dt>クラブ・サークル数</dt>
        <dd>85団体</dd>
      </dl>
    </section>
  </main>

  <!-- サイドバー -->
  <aside aria-label="サイドバー">
    <section>
      <h2>重要なお知らせ</h2>
      <p><a href="#">台風接近に伴う休講情報</a></p>
    </section>

    <section>
      <h2>SNS</h2>
      <ul>
        <li><a href="#" target="_blank" rel="noopener noreferrer">X (Twitter)</a></li>
        <li><a href="#" target="_blank" rel="noopener noreferrer">Instagram</a></li>
        <li><a href="#" target="_blank" rel="noopener noreferrer">YouTube</a></li>
      </ul>
    </section>

    <section>
      <h2>パンフレット請求</h2>
      <p>2027年度版パンフレットを無料でお届けします。</p>
      <p><a href="#">パンフレットを請求する</a></p>
    </section>
  </aside>

  <!-- フッター -->
  <footer>
    <address>
      テクノロジー大学<br>
      〒192-0001 東京都八王子市テクノ町1-1-1<br>
      TEL: <a href="tel:0426001234">042-600-1234</a><br>
      E-mail: <a href="mailto:info@techuniv.example.ac.jp">info@techuniv.example.ac.jp</a>
    </address>

    <nav aria-label="フッターナビゲーション">
      <ul>
        <li><a href="#">大学概要</a></li>
        <li><a href="#">学部・大学院</a></li>
        <li><a href="#">入試情報</a></li>
        <li><a href="#">キャンパスライフ</a></li>
        <li><a href="#">就職支援</a></li>
        <li><a href="#">研究活動</a></li>
      </ul>
    </nav>

    <nav aria-label="法的情報">
      <ul>
        <li><a href="#">プライバシーポリシー</a></li>
        <li><a href="#">利用規約</a></li>
        <li><a href="#">サイトマップ</a></li>
        <li><a href="#">お問い合わせ</a></li>
      </ul>
    </nav>

    <p><small>&copy; 2026 テクノロジー大学. All rights reserved.</small></p>
  </footer>
</body>
</html>
```

</details>

<details>
<summary>解答例（改良版 ─ 設計ポイント解説付き）</summary>

改良版では、初心者向けのコードに以下の設計改善を加えています。

**1. ロゴ画像の `alt` 属性の使い方**

```html
<!-- ロゴ画像がテキストの隣にある場合、alt="" で装飾的画像として扱う -->
<h1>
  <img src="logo.png" alt="" width="40" height="40">
  テクノロジー大学
</h1>

<!-- ロゴ画像だけの場合（テキストがない場合）、alt にテキストを入れる -->
<h1>
  <img src="logo.png" alt="テクノロジー大学" width="200" height="60">
</h1>
```

**2. お知らせカテゴリのマークアップ**

```html
<!-- より構造的なマークアップ（data属性を活用） -->
<li>
  <time datetime="2026-04-05">2026年4月5日</time>
  <span data-category="important" aria-label="カテゴリ：重要">重要</span>
  <a href="#">入学式の日程変更について</a>
</li>
```

`data-category` はCSSでスタイリングするときのフックになります。

**3. CTAボタンのマークアップ**

```html
<!-- リンクだがボタンとして見せたい場合 -->
<a href="/request" role="button">資料請求はこちら</a>

<!-- role="button" を付けると、スクリーンリーダーが「ボタン」と読み上げる -->
<!-- ただし、ページ遷移する場合は role="button" は不要（リンクのまま） -->

<!-- 正しい使い分け -->
<a href="/request">資料請求はこちら</a>        <!-- ページ遷移 → リンクのまま -->
<button onclick="openModal()">オンライン相談</button>  <!-- 動的操作 → button -->
```

**4. 統計情報のよりリッチなマークアップ**

```html
<section aria-labelledby="numbers-heading">
  <h2 id="numbers-heading">数字で見るテクノロジー大学</h2>
  <dl>
    <div>
      <dt>学生数</dt>
      <dd><data value="3200">3,200</data>名</dd>
    </div>
    <div>
      <dt>就職率</dt>
      <dd><data value="98.5">98.5</data>%</dd>
    </div>
  </dl>
</section>
```

`<data>` 要素は人間向けのテキストとマシンリーダブルな値を併記できます。`<dl>` 内の `<div>` はCSSでのスタイリングのためのラッパーとして仕様上許可されています。

**5. スキップリンクの追加**

```html
<body>
  <!-- キーボードユーザー向け：ナビゲーションを飛ばしてメインコンテンツへ -->
  <a href="#main-content" class="skip-link">メインコンテンツへスキップ</a>

  <header>...</header>
  <nav>...</nav>

  <main id="main-content">
    ...
  </main>
</body>
```

```css
.skip-link {
  position: absolute;
  top: -100px;
  left: 0;
  background: #003366;
  color: white;
  padding: 8px 16px;
  z-index: 100;
}
.skip-link:focus {
  top: 0;  /* Tabキーでフォーカスしたときだけ表示 */
}
```

スキップリンク（skip link）は、キーボードだけで操作するユーザーがナビゲーションを飛ばしてメインコンテンツに直接アクセスできるようにする仕組みです。多くの政府系サイトや大企業サイトで導入されています。

</details>

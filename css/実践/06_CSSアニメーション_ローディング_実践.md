# 実践課題06：CSSアニメーション ─ ローディングスピナー集 ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第1章（CSSの基本）、第6章（アニメーション）
> **課題の種類**: ミニプロジェクト
> **学習目標**: `@keyframes`・`animation`・`transform` を組み合わせて、実用的なローディングインジケータを複数パターン作る

---

## 完成イメージ

ブラウザで開くと、4種類のローディングスピナー（loading spinner）が並んで動作します。

```
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│         │  │         │  │         │  │         │
│  ◎回転  │  │ ●●● 点滅│  │  ─バー  │  │ ◯パルス │
│         │  │         │  │         │  │         │
│ スピナー │  │ ドット   │  │ プログレス│  │ パルス  │
└─────────┘  └─────────┘  └─────────┘  └─────────┘
```

---

## 課題の要件

1. 4種類のローディングアニメーションを作る
   - **スピナー**: 円がくるくる回転する
   - **ドット**: 3つの点が交互にバウンスする
   - **プログレスバー**: バーが左から右に伸びて繰り返す
   - **パルス**: 円がふわっと広がって消える
2. すべて `@keyframes` と `animation` プロパティで実装する
3. 外部ライブラリは使わない
4. HTMLとCSSだけで動作する（JavaScriptは不要）

---

## ステップガイド

<details>
<summary>ステップ1：@keyframes の基本を確認する</summary>

`@keyframes` でアニメーションの各段階を定義し、`animation` で適用します。

```css
@keyframes spin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

.spinner {
  animation: spin 1s linear infinite;
}
```

- `1s` → 1回の周期
- `linear` → 一定速度
- `infinite` → 無限に繰り返す

</details>

<details>
<summary>ステップ2：ドットアニメーションの作り方</summary>

3つの点に同じアニメーションを付け、`animation-delay` で開始タイミングをずらします。

```css
.dot:nth-child(1) { animation-delay: 0s; }
.dot:nth-child(2) { animation-delay: 0.15s; }
.dot:nth-child(3) { animation-delay: 0.3s; }
```

</details>

<details>
<summary>ステップ3：パルスアニメーションの作り方</summary>

`scale` と `opacity` を組み合わせて広がりながら消えるエフェクトを作ります。

```css
@keyframes pulse {
  0%   { transform: scale(1);   opacity: 1; }
  100% { transform: scale(2.5); opacity: 0; }
}
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ローディングスピナー集</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: sans-serif;
      background-color: #1a1a2e;
      color: #ffffff;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      gap: 60px;
      padding: 40px;
    }

    h1 {
      font-size: 24px;
      font-weight: 300;
    }

    .loaders {
      display: flex;
      gap: 80px;
      flex-wrap: wrap;
      justify-content: center;
    }

    .loader-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 20px;
    }

    .loader-label {
      font-size: 13px;
      color: #aaaaaa;
    }

    /* ===== 1. スピナー ===== */
    .spinner {
      width: 48px;
      height: 48px;
      border: 4px solid rgba(255, 255, 255, 0.2);
      border-top-color: #4a90d9;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }

    @keyframes spin {
      from { transform: rotate(0deg); }
      to   { transform: rotate(360deg); }
    }

    /* ===== 2. ドット ===== */
    .dots {
      display: flex;
      gap: 8px;
    }

    .dot {
      width: 14px;
      height: 14px;
      background-color: #4a90d9;
      border-radius: 50%;
      animation: bounce 0.6s ease-in-out infinite alternate;
    }

    .dot:nth-child(2) {
      animation-delay: 0.15s;
    }

    .dot:nth-child(3) {
      animation-delay: 0.3s;
    }

    @keyframes bounce {
      from { transform: translateY(0); }
      to   { transform: translateY(-16px); }
    }

    /* ===== 3. プログレスバー ===== */
    .progress-track {
      width: 120px;
      height: 6px;
      background-color: rgba(255, 255, 255, 0.1);
      border-radius: 3px;
      overflow: hidden;
    }

    .progress-bar {
      width: 40%;
      height: 100%;
      background-color: #4a90d9;
      border-radius: 3px;
      animation: progress 1.2s ease-in-out infinite;
    }

    @keyframes progress {
      0%   { transform: translateX(-100%); }
      50%  { transform: translateX(200%); }
      100% { transform: translateX(-100%); }
    }

    /* ===== 4. パルス ===== */
    .pulse-container {
      position: relative;
      width: 48px;
      height: 48px;
    }

    .pulse-circle {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 20px;
      height: 20px;
      background-color: #4a90d9;
      border-radius: 50%;
    }

    .pulse-ring {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 20px;
      height: 20px;
      border: 3px solid #4a90d9;
      border-radius: 50%;
      animation: pulse 1.5s ease-out infinite;
    }

    @keyframes pulse {
      0% {
        width: 20px;
        height: 20px;
        opacity: 1;
      }
      100% {
        width: 60px;
        height: 60px;
        opacity: 0;
      }
    }
  </style>
</head>
<body>
  <h1>ローディングスピナー集</h1>

  <div class="loaders">
    <!-- 1. スピナー -->
    <div class="loader-item">
      <div class="spinner"></div>
      <span class="loader-label">スピナー</span>
    </div>

    <!-- 2. ドット -->
    <div class="loader-item">
      <div class="dots">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
      </div>
      <span class="loader-label">ドット</span>
    </div>

    <!-- 3. プログレスバー -->
    <div class="loader-item">
      <div class="progress-track">
        <div class="progress-bar"></div>
      </div>
      <span class="loader-label">プログレス</span>
    </div>

    <!-- 4. パルス -->
    <div class="loader-item">
      <div class="pulse-container">
        <div class="pulse-ring"></div>
        <div class="pulse-circle"></div>
      </div>
      <span class="loader-label">パルス</span>
    </div>
  </div>
</body>
</html>
```

</details>

<details>
<summary>解答例（改良版 ─ より滑らかで多彩なバリエーション）</summary>

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ローディングスピナー集（改良版）</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: "Helvetica Neue", Arial, sans-serif;
      background-color: #0f0f23;
      color: #ffffff;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      gap: 48px;
      padding: 40px;
    }

    h1 {
      font-size: 28px;
      font-weight: 300;
      letter-spacing: 2px;
    }

    .loaders {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 60px;
    }

    .loader-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 24px;
      min-width: 120px;
      min-height: 100px;
      justify-content: center;
    }

    .loader-label {
      font-size: 12px;
      color: #666666;
      letter-spacing: 1px;
      text-transform: uppercase;
    }

    /* ===== 1. グラデーションスピナー ===== */
    .spinner {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: conic-gradient(
        from 0deg,
        transparent 0%,
        #4a90d9 70%,
        transparent 70%
      );
      animation: spin 0.8s linear infinite;
      position: relative;
    }

    .spinner::after {
      content: "";
      position: absolute;
      top: 4px;
      left: 4px;
      right: 4px;
      bottom: 4px;
      background-color: #0f0f23;
      border-radius: 50%;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    /* ===== 2. ウェーブドット ===== */
    .dots {
      display: flex;
      gap: 6px;
      align-items: center;
      height: 48px;
    }

    .dot {
      width: 10px;
      height: 10px;
      background-color: #4a90d9;
      border-radius: 50%;
      animation: wave 1.2s ease-in-out infinite;
    }

    .dot:nth-child(2) { animation-delay: 0.1s; }
    .dot:nth-child(3) { animation-delay: 0.2s; }
    .dot:nth-child(4) { animation-delay: 0.3s; }
    .dot:nth-child(5) { animation-delay: 0.4s; }

    @keyframes wave {
      0%, 60%, 100% {
        transform: translateY(0) scale(1);
        opacity: 0.4;
      }
      30% {
        transform: translateY(-16px) scale(1.2);
        opacity: 1;
      }
    }

    /* ===== 3. シマーバー ===== */
    .progress-track {
      width: 140px;
      height: 4px;
      background-color: rgba(255, 255, 255, 0.06);
      border-radius: 2px;
      overflow: hidden;
    }

    .progress-bar {
      width: 50%;
      height: 100%;
      background: linear-gradient(90deg, #4a90d9, #667eea, #764ba2);
      border-radius: 2px;
      animation: shimmer 1.5s ease-in-out infinite;
    }

    @keyframes shimmer {
      0%   { transform: translateX(-150%); }
      100% { transform: translateX(300%); }
    }

    /* ===== 4. 多重パルス ===== */
    .pulse-container {
      position: relative;
      width: 48px;
      height: 48px;
    }

    .pulse-core {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 12px;
      height: 12px;
      background-color: #4a90d9;
      border-radius: 50%;
      animation: core-beat 1.5s ease-in-out infinite;
    }

    @keyframes core-beat {
      0%, 100% { transform: translate(-50%, -50%) scale(1); }
      50%      { transform: translate(-50%, -50%) scale(1.3); }
    }

    .pulse-ring {
      position: absolute;
      top: 50%;
      left: 50%;
      width: 12px;
      height: 12px;
      border: 2px solid #4a90d9;
      border-radius: 50%;
      animation: ring-expand 1.5s ease-out infinite;
    }

    .pulse-ring:nth-child(2) {
      animation-delay: 0.5s;
    }

    .pulse-ring:nth-child(3) {
      animation-delay: 1s;
    }

    @keyframes ring-expand {
      0% {
        transform: translate(-50%, -50%) scale(1);
        opacity: 0.8;
      }
      100% {
        transform: translate(-50%, -50%) scale(5);
        opacity: 0;
      }
    }
  </style>
</head>
<body>
  <h1>Loading Spinners</h1>

  <div class="loaders">
    <div class="loader-item">
      <div class="spinner"></div>
      <span class="loader-label">Spinner</span>
    </div>

    <div class="loader-item">
      <div class="dots">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
      </div>
      <span class="loader-label">Wave</span>
    </div>

    <div class="loader-item">
      <div class="progress-track">
        <div class="progress-bar"></div>
      </div>
      <span class="loader-label">Shimmer</span>
    </div>

    <div class="loader-item">
      <div class="pulse-container">
        <div class="pulse-ring"></div>
        <div class="pulse-ring"></div>
        <div class="pulse-ring"></div>
        <div class="pulse-core"></div>
      </div>
      <span class="loader-label">Pulse</span>
    </div>
  </div>
</body>
</html>
```

**初心者向けとの違い:**
- `conic-gradient` でスピナーの色がなめらかに変化（最新のCSS技法）
- ドットを5つに増やし、ウェーブ状のアニメーションに変更
- プログレスバーにグラデーションを使ったシマー（shimmer）エフェクト
- パルスを3重リングにし、`animation-delay` でずらして波紋のように表現
- `scale` と `opacity` を組み合わせた、より有機的な動き

</details>

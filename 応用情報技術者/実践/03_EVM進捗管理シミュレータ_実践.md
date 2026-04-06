# 実践課題03：EVM進捗管理シミュレータ ★2

> **難易度**: ★★☆☆☆（基礎）
> **前提知識**: 第7章（プロジェクトマネジメント応用）
> **課題の種類**: Pythonコーディング / 計算演習
> **学習目標**: EVM（Earned Value Management）の指標を正確に計算し、プロジェクトの健全性を判断できるようになる

---

## 完成イメージ

```
===== EVM進捗管理シミュレータ =====

プロジェクト全体予算 BAC（万円）: 1000
計画出来高 PV（万円）: 600
達成出来高 EV（万円）: 500
実コスト AC（万円）: 550

========== 分析結果 ==========

--- 差異分析 ---
SV（スケジュール差異）= 500 - 600 = -100.0万円 → 遅延
CV（コスト差異）      = 500 - 550 = -50.0万円  → 超過

--- 効率指数 ---
SPI（スケジュール効率）= 500 / 600 = 0.833 → スケジュール遅延（83.3%の効率）
CPI（コスト効率）      = 500 / 550 = 0.909 → コスト超過（90.9%の効率）

--- 完了予測 ---
EAC（完了時総コスト）= 1000 / 0.909 = 1100.0万円
ETC（残作業コスト）  = 1100.0 - 550 = 550.0万円
VAC（完了時コスト差異）= 1000 - 1100.0 = -100.0万円

[総合判定] スケジュール遅延かつコスト超過。是正措置が必要です。
```

---

## 課題の要件

1. BAC、PV、EV、ACの4値をユーザーから入力で受け取る
2. SV、CV、SPI、CPIを計算して表示する
3. EAC、ETC、VACの完了予測を計算して表示する
4. 各指標の正負から状況を判定し、メッセージを表示する
5. 0除算を適切にハンドリングする

---

## 背景知識の確認

```
┌─────────────────────────────────────┐
│            EVMの指標体系             │
│                                     │
│ [基本値]                            │
│  PV: Planned Value（計画出来高）     │
│  EV: Earned Value（達成出来高）      │
│  AC: Actual Cost（実コスト）         │
│                                     │
│ [差異分析]                           │
│  SV = EV - PV   （正:前倒し/負:遅延）│
│  CV = EV - AC   （正:予算内/負:超過）│
│                                     │
│ [効率指数]                           │
│  SPI = EV / PV  （1超:前倒し）       │
│  CPI = EV / AC  （1超:予算内）       │
│                                     │
│ [完了予測]                           │
│  EAC = BAC / CPI                    │
│  ETC = EAC - AC                     │
│  VAC = BAC - EAC                    │
└─────────────────────────────────────┘
```

---

## ステップガイド

<details>
<summary>ステップ1：入力を受け取る</summary>

```python
bac = float(input("プロジェクト全体予算 BAC（万円）: "))
pv = float(input("計画出来高 PV（万円）: "))
ev = float(input("達成出来高 EV（万円）: "))
ac = float(input("実コスト AC（万円）: "))
```

</details>

<details>
<summary>ステップ2：差異分析を行う</summary>

```python
sv = ev - pv
cv = ev - ac

sv_status = "前倒し" if sv >= 0 else "遅延"
cv_status = "予算内" if cv >= 0 else "超過"

print(f"SV = {ev} - {pv} = {sv:.1f}万円 → {sv_status}")
print(f"CV = {ev} - {ac} = {cv:.1f}万円 → {cv_status}")
```

</details>

<details>
<summary>ステップ3：効率指数と完了予測を計算する</summary>

CPI が 0 の場合（EV=0）は除算エラーになるため、ガードが必要です。

```python
if pv > 0:
    spi = ev / pv
if ac > 0:
    cpi = ev / ac
if cpi > 0:
    eac = bac / cpi
    etc = eac - ac
    vac = bac - eac
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```python
# EVM進捗管理シミュレータ
# 学べる内容：EVMの指標計算、プロジェクトの健全性判断
# 実行方法：python evm_simulator.py

print("===== EVM進捗管理シミュレータ =====\n")

# --- 入力 ---
bac = float(input("プロジェクト全体予算 BAC（万円）: "))
pv = float(input("計画出来高 PV（万円）: "))
ev = float(input("達成出来高 EV（万円）: "))
ac = float(input("実コスト AC（万円）: "))

print("\n========== 分析結果 ==========")

# --- 差異分析 ---
print("\n--- 差異分析 ---")
sv = ev - pv
cv = ev - ac
sv_msg = "前倒し" if sv >= 0 else "遅延"
cv_msg = "予算内" if cv >= 0 else "超過"
print(f"SV（スケジュール差異）= {ev} - {pv} = {sv:.1f}万円 → {sv_msg}")
print(f"CV（コスト差異）      = {ev} - {ac} = {cv:.1f}万円  → {cv_msg}")

# --- 効率指数 ---
print("\n--- 効率指数 ---")
if pv > 0:
    spi = ev / pv
    spi_msg = "スケジュール前倒し" if spi >= 1.0 else "スケジュール遅延"
    print(f"SPI（スケジュール効率）= {ev} / {pv} = {spi:.3f} → {spi_msg}（{spi*100:.1f}%の効率）")
else:
    print("SPI: PV=0のため計算不可")
    spi = 0

if ac > 0:
    cpi = ev / ac
    cpi_msg = "コスト効率良好" if cpi >= 1.0 else "コスト超過"
    print(f"CPI（コスト効率）      = {ev} / {ac} = {cpi:.3f} → {cpi_msg}（{cpi*100:.1f}%の効率）")
else:
    print("CPI: AC=0のため計算不可")
    cpi = 0

# --- 完了予測 ---
print("\n--- 完了予測 ---")
if cpi > 0:
    eac = bac / cpi
    etc = eac - ac
    vac = bac - eac
    print(f"EAC（完了時総コスト）= {bac} / {cpi:.3f} = {eac:.1f}万円")
    print(f"ETC（残作業コスト）  = {eac:.1f} - {ac} = {etc:.1f}万円")
    print(f"VAC（完了時コスト差異）= {bac} - {eac:.1f} = {vac:.1f}万円")
else:
    print("CPI=0のため完了予測は計算できません。")

# --- 総合判定 ---
print()
if sv >= 0 and cv >= 0:
    print("[総合判定] プロジェクトは順調です。このペースを維持しましょう。")
elif sv >= 0 and cv < 0:
    print("[総合判定] スケジュールは順調ですが、コストが超過しています。コスト管理を強化してください。")
elif sv < 0 and cv >= 0:
    print("[総合判定] コストは予算内ですが、スケジュールが遅延しています。リソース追加を検討してください。")
else:
    print("[総合判定] スケジュール遅延かつコスト超過。是正措置が必要です。")
```

</details>

<details>
<summary>解答例（改良版 ─ 月次推移トラッキング付き）</summary>

```python
# EVM進捗管理シミュレータ（改良版）
# 学べる内容：EVM指標計算、月次推移の追跡、傾向分析
# 実行方法：python evm_advanced.py

def calc_evm(bac, pv, ev, ac):
    """EVM指標を一括計算して辞書で返す"""
    result = {"bac": bac, "pv": pv, "ev": ev, "ac": ac}
    result["sv"] = ev - pv
    result["cv"] = ev - ac
    result["spi"] = ev / pv if pv > 0 else 0
    result["cpi"] = ev / ac if ac > 0 else 0
    result["eac"] = bac / result["cpi"] if result["cpi"] > 0 else float("inf")
    result["etc"] = result["eac"] - ac
    result["vac"] = bac - result["eac"]
    return result

def status_icon(value):
    """正負に応じたアイコンを返す"""
    return "○" if value >= 0 else "×"

# --- メイン ---
print("===== EVM月次トラッキング =====\n")

bac = float(input("プロジェクト全体予算 BAC（万円）: "))
months = int(input("トラッキングする月数: "))

records = []
for m in range(1, months + 1):
    print(f"\n--- 第{m}月 ---")
    pv = float(input(f"  PV（万円）: "))
    ev = float(input(f"  EV（万円）: "))
    ac = float(input(f"  AC（万円）: "))
    records.append(calc_evm(bac, pv, ev, ac))

# --- 月次推移表 ---
print("\n========== 月次推移レポート ==========")
print(f"{'月':>3} | {'PV':>7} | {'EV':>7} | {'AC':>7} | {'SPI':>5} | {'CPI':>5} | {'SV':>8} | {'CV':>8}")
print("-" * 70)
for i, r in enumerate(records, 1):
    print(f"{i:3d} | {r['pv']:7.0f} | {r['ev']:7.0f} | {r['ac']:7.0f} | "
          f"{r['spi']:5.2f} | {r['cpi']:5.2f} | "
          f"{r['sv']:+8.0f}{status_icon(r['sv'])} | {r['cv']:+8.0f}{status_icon(r['cv'])}")

# --- 最新月の完了予測 ---
latest = records[-1]
print(f"\n--- 完了予測（最新月ベース） ---")
print(f"EAC = {latest['eac']:.0f}万円（予算{bac:.0f}万円に対して{latest['vac']:+.0f}万円）")

# --- 傾向分析 ---
if len(records) >= 2:
    prev_cpi = records[-2]["cpi"]
    curr_cpi = latest["cpi"]
    if curr_cpi > prev_cpi:
        print("\n[傾向] CPIが改善傾向です。コスト管理施策が効果を上げています。")
    elif curr_cpi < prev_cpi:
        print("\n[傾向] CPIが悪化傾向です。追加のコスト削減策が必要です。")
    else:
        print("\n[傾向] CPIに変化なし。継続的なモニタリングを続けてください。")
```

**初心者向けとの違い:**
- 複数月のデータを入力し、推移を一覧表示できる
- SPIとCPIの推移から傾向を分析する機能を追加
- 関数化により、計算ロジックの再利用性を高めている
- 月次レポート形式でプロジェクト管理の実務に近い出力を実現

</details>

---

## 確認問題

以下のプロジェクトデータでEVM分析を行い、プログラムの出力と照合してみましょう。

**問題:** BAC=2,000万円、PV=800万円、EV=720万円、AC=900万円

| 指標 | 計算 | 値 |
|------|------|-----|
| SV | 720-800 | -80万円（遅延） |
| CV | 720-900 | -180万円（超過） |
| SPI | 720/800 | 0.900 |
| CPI | 720/900 | 0.800 |
| EAC | 2000/0.8 | 2,500万円 |
| VAC | 2000-2500 | -500万円 |

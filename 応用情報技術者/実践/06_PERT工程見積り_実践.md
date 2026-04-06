# 実践課題06：PERT法による工程見積り ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第1章（応用数学と離散数学）、第7章（プロジェクトマネジメント応用）
> **課題の種類**: 計算演習 / Pythonコーディング
> **学習目標**: PERT法の三点見積り・クリティカルパス・余裕時間の計算を統合的に行い、プロジェクトスケジュールの分析ができるようになる

---

## 完成イメージ

```
===== PERT工程分析ツール =====

作業数を入力: 6

作業A:
  楽観値(O): 2
  最可能値(M): 4
  悲観値(P): 6
  先行作業（カンマ区切り、なければEnter）: 

作業B:
  楽観値(O): 3
  最可能値(M): 5
  悲観値(P): 13
  先行作業: A
...

========== 分析結果 ==========

--- 期待値と分散 ---
作業  | O  | M  | P  | 期待値te | 分散σ²
------+----+----+----+----------+-------
A     |  2 |  4 |  6 |     4.00 |  0.44
B     |  3 |  5 | 13 |     6.00 |  2.78
...

--- クリティカルパス ---
パス: A → C → E → F
期待所要日数: 22.00日
合計分散: 4.89
標準偏差: 2.21日

--- 各作業の余裕時間 ---
作業  | ES    | EF    | LS    | LF    | フロート | クリティカル
------+-------+-------+-------+-------+---------+----------
A     |  0.00 |  4.00 |  0.00 |  4.00 |    0.00 | ★
B     |  4.00 | 10.00 |  6.00 | 12.00 |    2.00 |
...
```

---

## 課題の要件

1. 各作業の楽観値（O）、最可能値（M）、悲観値（P）を入力で受け取る
2. PERT法で期待値 te = (O + 4M + P) / 6 と分散 σ² = ((P - O) / 6)² を計算する
3. 作業の依存関係からクリティカルパスを求める
4. 各作業の最早開始（ES）、最早完了（EF）、最遅開始（LS）、最遅完了（LF）を計算する
5. フロート（余裕時間）= LS - ES を計算し、フロート=0の作業をクリティカルパスとして表示する

---

## 背景知識の確認

```
PERT法の三点見積り:
  期待値:  te = (O + 4M + P) / 6
  分散:    σ² = ((P - O) / 6)²

    ※ O: 楽観値（Optimistic）
    ※ M: 最可能値（Most likely）
    ※ P: 悲観値（Pessimistic）

クリティカルパスの求め方:
  1. 前進計算（Forward Pass）: ES, EF を求める
     ES = 先行作業のEFの最大値（開始作業は0）
     EF = ES + te

  2. 後退計算（Backward Pass）: LS, LF を求める
     LF = 後続作業のLSの最小値（最終作業のLF = EF）
     LS = LF - te

  3. フロート = LS - ES（= LF - EF）
     フロート = 0 の作業がクリティカルパス上の作業
```

---

## ステップガイド

<details>
<summary>ステップ1：データ構造を設計する</summary>

各作業の情報を辞書で管理します。

```python
tasks = {}
# 例: tasks["A"] = {"o": 2, "m": 4, "p": 6, "predecessors": [], "te": 4.0, "var": 0.44}
```

</details>

<details>
<summary>ステップ2：期待値と分散を計算する</summary>

```python
for name, task in tasks.items():
    task["te"] = (task["o"] + 4 * task["m"] + task["p"]) / 6
    task["var"] = ((task["p"] - task["o"]) / 6) ** 2
```

</details>

<details>
<summary>ステップ3：前進計算（ES, EF）</summary>

作業をトポロジカルソート順に処理します。先行作業がない作業から開始します。

```python
# 先行作業なし → ES = 0
# 先行作業あり → ES = max(先行作業のEF)
# EF = ES + te
```

</details>

<details>
<summary>ステップ4：後退計算（LS, LF）</summary>

最終作業から逆順に処理します。

```python
# 後続作業なし → LF = プロジェクト完了時刻
# 後続作業あり → LF = min(後続作業のLS)
# LS = LF - te
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```python
# PERT工程分析ツール
# 学べる内容：PERT法、三点見積り、クリティカルパス、フロート計算
# 実行方法：python pert_analysis.py

print("===== PERT工程分析ツール =====\n")

# --- 入力 ---
n = int(input("作業数を入力: "))
tasks = {}
task_names = []

for i in range(n):
    name = input(f"\n作業名（例: A）: ").strip()
    task_names.append(name)
    o = float(input(f"  楽観値(O): "))
    m = float(input(f"  最可能値(M): "))
    p = float(input(f"  悲観値(P): "))
    pred_input = input(f"  先行作業（カンマ区切り、なければEnter）: ").strip()
    predecessors = [x.strip() for x in pred_input.split(",") if x.strip()]

    te = (o + 4 * m + p) / 6
    var = ((p - o) / 6) ** 2

    tasks[name] = {
        "o": o, "m": m, "p": p,
        "predecessors": predecessors,
        "te": te, "var": var,
        "es": 0, "ef": 0, "ls": 0, "lf": 0,
    }

# --- 前進計算 ---
# トポロジカルソート（簡易版：先行作業が処理済みの作業から順に処理）
processed = set()
order = []
while len(order) < len(task_names):
    for name in task_names:
        if name not in processed:
            if all(p in processed for p in tasks[name]["predecessors"]):
                order.append(name)
                processed.add(name)

for name in order:
    task = tasks[name]
    if task["predecessors"]:
        task["es"] = max(tasks[p]["ef"] for p in task["predecessors"])
    else:
        task["es"] = 0
    task["ef"] = task["es"] + task["te"]

# --- 後退計算 ---
# プロジェクト完了時刻
project_end = max(tasks[name]["ef"] for name in task_names)

# 後続作業のマップを作成
successors = {name: [] for name in task_names}
for name in task_names:
    for pred in tasks[name]["predecessors"]:
        successors[pred].append(name)

for name in reversed(order):
    task = tasks[name]
    if not successors[name]:
        task["lf"] = project_end
    else:
        task["lf"] = min(tasks[s]["ls"] for s in successors[name])
    task["ls"] = task["lf"] - task["te"]

# --- 結果表示 ---
print("\n========== 分析結果 ==========")

# 期待値と分散
print("\n--- 期待値と分散 ---")
print(f"{'作業':<6} | {'O':>4} | {'M':>4} | {'P':>4} | {'期待値te':>8} | {'分散σ²':>7}")
print("-" * 50)
for name in order:
    t = tasks[name]
    print(f"{name:<6} | {t['o']:4.0f} | {t['m']:4.0f} | {t['p']:4.0f} | {t['te']:8.2f} | {t['var']:7.2f}")

# フロートとクリティカルパス
print(f"\n--- 各作業の余裕時間 ---")
print(f"{'作業':<6} | {'ES':>6} | {'EF':>6} | {'LS':>6} | {'LF':>6} | {'フロート':>8} | クリティカル")
print("-" * 65)

critical_tasks = []
for name in order:
    t = tasks[name]
    float_time = t["ls"] - t["es"]
    is_critical = "★" if abs(float_time) < 0.001 else ""
    if is_critical:
        critical_tasks.append(name)
    print(f"{name:<6} | {t['es']:6.2f} | {t['ef']:6.2f} | {t['ls']:6.2f} | {t['lf']:6.2f} | {float_time:8.2f} | {is_critical}")

# クリティカルパス
print(f"\n--- クリティカルパス ---")
print(f"パス: {' → '.join(critical_tasks)}")
total_te = sum(tasks[name]["te"] for name in critical_tasks)
total_var = sum(tasks[name]["var"] for name in critical_tasks)
print(f"期待所要日数: {total_te:.2f}日")
print(f"合計分散: {total_var:.2f}")
print(f"標準偏差: {total_var**0.5:.2f}日")
```

</details>

<details>
<summary>解答例（改良版 ─ 確率計算＆ガントチャート付き）</summary>

```python
# PERT工程分析ツール（改良版）
# 学べる内容：PERT法、正規分布による確率計算、ガントチャート表示
# 実行方法：python pert_advanced.py

import math

def pert_estimate(o, m, p):
    """三点見積りの期待値と分散を計算"""
    te = (o + 4 * m + p) / 6
    var = ((p - o) / 6) ** 2
    return te, var

def normal_cdf(x):
    """標準正規分布の累積分布関数（近似）"""
    # Abramowitz and Stegun の近似式
    if x < 0:
        return 1 - normal_cdf(-x)
    t = 1 / (1 + 0.2316419 * x)
    d = 0.3989422804014327  # 1/sqrt(2*pi)
    p = d * math.exp(-x * x / 2) * (
        0.319381530 * t - 0.356563782 * t**2 +
        1.781477937 * t**3 - 1.821255978 * t**4 +
        1.330274429 * t**5
    )
    return 1 - p

def topological_sort(tasks, task_names):
    """トポロジカルソート"""
    processed = set()
    order = []
    while len(order) < len(task_names):
        for name in task_names:
            if name not in processed:
                if all(p in processed for p in tasks[name]["predecessors"]):
                    order.append(name)
                    processed.add(name)
    return order

# --- サンプルデータ（手入力の代わり） ---
print("===== PERT工程分析ツール（改良版） =====\n")

# プリセットデータを使用するか選択
use_preset = input("プリセットデータを使用しますか？(y/n): ").strip().lower()

if use_preset == "y":
    task_data = [
        ("A", 2, 4, 6, []),
        ("B", 3, 5, 13, ["A"]),
        ("C", 4, 6, 8, ["A"]),
        ("D", 1, 3, 5, ["B"]),
        ("E", 5, 7, 15, ["C"]),
        ("F", 2, 4, 6, ["D", "E"]),
    ]
else:
    task_data = []
    n = int(input("作業数: "))
    for i in range(n):
        name = input(f"\n作業名: ").strip()
        o = float(input(f"  楽観値(O): "))
        m = float(input(f"  最可能値(M): "))
        p = float(input(f"  悲観値(P): "))
        pred_input = input(f"  先行作業（カンマ区切り）: ").strip()
        preds = [x.strip() for x in pred_input.split(",") if x.strip()]
        task_data.append((name, o, m, p, preds))

tasks = {}
task_names = []
for name, o, m, p, preds in task_data:
    task_names.append(name)
    te, var = pert_estimate(o, m, p)
    tasks[name] = {
        "o": o, "m": m, "p": p,
        "predecessors": preds, "te": te, "var": var,
        "es": 0, "ef": 0, "ls": 0, "lf": 0,
    }

# --- 前進・後退計算 ---
order = topological_sort(tasks, task_names)

for name in order:
    t = tasks[name]
    t["es"] = max((tasks[p]["ef"] for p in t["predecessors"]), default=0)
    t["ef"] = t["es"] + t["te"]

project_end = max(tasks[n]["ef"] for n in task_names)

successors = {n: [] for n in task_names}
for n in task_names:
    for p in tasks[n]["predecessors"]:
        successors[p].append(n)

for name in reversed(order):
    t = tasks[name]
    t["lf"] = min((tasks[s]["ls"] for s in successors[name]), default=project_end)
    t["ls"] = t["lf"] - t["te"]

# --- クリティカルパスの特定 ---
critical = [n for n in order if abs(tasks[n]["ls"] - tasks[n]["es"]) < 0.001]

# --- 結果表示 ---
print("\n========== 分析結果 ==========")

print(f"\n--- スケジュール詳細 ---")
print(f"{'作業':<4} | {'te':>5} | {'ES':>5} | {'EF':>5} | {'LS':>5} | {'LF':>5} | {'余裕':>5} | CP")
print("-" * 55)
for name in order:
    t = tasks[name]
    fl = t["ls"] - t["es"]
    cp = "★" if name in critical else ""
    print(f"{name:<4} | {t['te']:5.1f} | {t['es']:5.1f} | {t['ef']:5.1f} | "
          f"{t['ls']:5.1f} | {t['lf']:5.1f} | {fl:5.1f} | {cp}")

print(f"\nクリティカルパス: {' → '.join(critical)}")
total_te = sum(tasks[n]["te"] for n in critical)
total_var = sum(tasks[n]["var"] for n in critical)
sigma = total_var ** 0.5
print(f"期待所要日数: {total_te:.1f}日  標準偏差: {sigma:.2f}日")

# --- 納期達成確率の計算 ---
print(f"\n--- 納期達成確率 ---")
for deadline in [total_te - 2, total_te, total_te + 2, total_te + 4]:
    z = (deadline - total_te) / sigma if sigma > 0 else 0
    prob = normal_cdf(z)
    print(f"  {deadline:.0f}日以内に完了する確率: {prob*100:.1f}%")

# --- 簡易ガントチャート ---
print(f"\n--- ガントチャート ---")
max_time = int(project_end) + 1
for name in order:
    t = tasks[name]
    bar_start = int(t["es"])
    bar_end = int(t["ef"])
    cp_mark = "★" if name in critical else " "
    bar = " " * bar_start + "█" * (bar_end - bar_start)
    print(f"{name}{cp_mark} |{bar}")
scale = "   |" + "".join([f"{i:<5}" for i in range(0, max_time, 5)])
print(scale)
```

**初心者向けとの違い:**
- 正規分布の近似関数を使い、指定納期での完了確率を計算
- 簡易ガントチャートでスケジュールを視覚化
- プリセットデータによる即時実行機能で動作確認が容易
- トポロジカルソートを独立関数にして見通しを改善

</details>

---

## 確認問題

以下のプロジェクトデータで手計算し、プログラムの出力と照合してください。

| 作業 | O | M | P | 先行作業 | te | σ² |
|------|---|---|---|---------|-----|-----|
| A | 1 | 2 | 3 | - | 2.0 | 0.11 |
| B | 2 | 3 | 10 | A | 4.0 | 1.78 |
| C | 3 | 5 | 7 | A | 5.0 | 0.44 |
| D | 1 | 4 | 7 | B,C | 4.0 | 1.00 |

クリティカルパスは A → C → D（合計11.0日）、A → B → D（合計10.0日）のうち、長い方の A → C → D です。

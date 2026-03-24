# ==============================
# EVM計算ツール
# 応用情報技術者：プロジェクトマネジメント
# ==============================
# 学べる内容:
#   - EVM（Earned Value Management）の基本概念
#   - PV（計画価値）/ EV（出来高）/ AC（実コスト）
#   - SV（スケジュール差異）/ CV（コスト差異）
#   - SPI（スケジュール効率指数）/ CPI（コスト効率指数）
#   - EAC（完成時総コスト見積）/ ETC（残作業コスト見積）
#   - VAC（完成時コスト差異）
#   - 進捗状況の視覚的な表示
#   - 応用情報技術者試験のプロジェクトマネジメント問題への対応力
#
# 実行方法:
#   python 02_EVM計算ツール.py
# ==============================


class EVMCalculator:
    """EVM（アーンドバリューマネジメント）計算ツールです

    プロジェクトのコスト・スケジュールのパフォーマンスを
    定量的に測定・予測します
    """

    def __init__(self, project_name, bac):
        """
        project_name: プロジェクト名
        bac: BAC（Budget at Completion: 完成時総予算）
        """
        self.project_name = project_name
        self.bac = bac
        self.periods = []  # 各期間のデータ

    def add_period(self, period_name, pv, ev, ac):
        """期間のデータを追加します

        pv: PV（Planned Value: 計画価値）- その時点までに完了する予定だった作業の予算
        ev: EV（Earned Value: 出来高）- 実際に完了した作業の予算上の価値
        ac: AC（Actual Cost: 実コスト）- 実際にかかったコスト
        """
        self.periods.append({
            "name": period_name,
            "PV": pv,
            "EV": ev,
            "AC": ac,
        })

    def calculate_sv(self, ev, pv):
        """SV（Schedule Variance: スケジュール差異）を計算します
        SV = EV - PV
        正: 予定より進んでいます / 負: 予定より遅れています
        """
        return ev - pv

    def calculate_cv(self, ev, ac):
        """CV（Cost Variance: コスト差異）を計算します
        CV = EV - AC
        正: 予算内です / 負: 予算超過です
        """
        return ev - ac

    def calculate_spi(self, ev, pv):
        """SPI（Schedule Performance Index: スケジュール効率指数）を計算します
        SPI = EV / PV
        >1: 予定より進んでいます / <1: 予定より遅れています
        """
        if pv == 0:
            return 0
        return ev / pv

    def calculate_cpi(self, ev, ac):
        """CPI（Cost Performance Index: コスト効率指数）を計算します
        CPI = EV / AC
        >1: 予算効率が良いです / <1: 予算超過です
        """
        if ac == 0:
            return 0
        return ev / ac

    def calculate_eac(self, ac, ev, method="cpi"):
        """EAC（Estimate at Completion: 完成時総コスト見積）を計算します

        method:
        - "cpi": 現在のCPIが続くと仮定 → EAC = BAC / CPI
        - "typical": 典型的な手法 → EAC = AC + (BAC - EV)
        - "combined": CPI+SPI考慮 → EAC = AC + (BAC - EV) / (CPI × SPI)
        """
        cpi = self.calculate_cpi(ev, ac)
        if method == "cpi":
            if cpi == 0:
                return float("inf")
            return self.bac / cpi
        elif method == "typical":
            return ac + (self.bac - ev)
        elif method == "combined":
            pv = None
            for p in self.periods:
                if p["EV"] == ev:
                    pv = p["PV"]
                    break
            if pv is None:
                pv = ev  # フォールバック
            spi = self.calculate_spi(ev, pv)
            if cpi * spi == 0:
                return float("inf")
            return ac + (self.bac - ev) / (cpi * spi)
        return 0

    def calculate_etc(self, eac, ac):
        """ETC（Estimate to Complete: 残作業コスト見積）を計算します
        ETC = EAC - AC
        """
        return eac - ac

    def calculate_vac(self, eac):
        """VAC（Variance at Completion: 完成時コスト差異）を計算します
        VAC = BAC - EAC
        正: 予算内で完了予定 / 負: 予算超過予定
        """
        return self.bac - eac

    def calculate_percent_complete(self, ev):
        """完了率を計算します
        完了率 = EV / BAC × 100
        """
        if self.bac == 0:
            return 0
        return (ev / self.bac) * 100

    def calculate_percent_spent(self, ac):
        """予算消費率を計算します
        消費率 = AC / BAC × 100
        """
        if self.bac == 0:
            return 0
        return (ac / self.bac) * 100

    def analyze_period(self, period_idx=-1):
        """指定期間の分析結果を表示します"""
        if not self.periods:
            print("  ※ データがありません。")
            return

        period = self.periods[period_idx]
        pv = period["PV"]
        ev = period["EV"]
        ac = period["AC"]

        sv = self.calculate_sv(ev, pv)
        cv = self.calculate_cv(ev, ac)
        spi = self.calculate_spi(ev, pv)
        cpi = self.calculate_cpi(ev, ac)
        eac = self.calculate_eac(ac, ev, "cpi")
        etc = self.calculate_etc(eac, ac)
        vac = self.calculate_vac(eac)
        pct_complete = self.calculate_percent_complete(ev)
        pct_spent = self.calculate_percent_spent(ac)

        print(f"\n  {'='*55}")
        print(f"  プロジェクト: {self.project_name}")
        print(f"  分析期間: {period['name']}")
        print(f"  {'='*55}")

        # 基本指標
        print(f"\n  ■ 基本指標")
        print(f"    BAC（完成時総予算）:     {self.bac:>12,.0f} 万円")
        print(f"    PV （計画価値）:         {pv:>12,.0f} 万円")
        print(f"    EV （出来高）:           {ev:>12,.0f} 万円")
        print(f"    AC （実コスト）:         {ac:>12,.0f} 万円")

        # 差異分析
        print(f"\n  ■ 差異分析")
        sv_status = "予定通り" if sv == 0 else ("進んでいます" if sv > 0 else "遅れています")
        cv_status = "予算通り" if cv == 0 else ("予算内です" if cv > 0 else "予算超過です")
        print(f"    SV（スケジュール差異）:  {sv:>+12,.0f} 万円 → {sv_status}")
        print(f"    CV（コスト差異）:        {cv:>+12,.0f} 万円 → {cv_status}")

        # 効率指数
        print(f"\n  ■ 効率指数")
        spi_status = "順調" if spi >= 1.0 else "遅延"
        cpi_status = "良好" if cpi >= 1.0 else "超過"
        print(f"    SPI（スケジュール効率）: {spi:>12.3f}      → {spi_status}")
        print(f"    CPI（コスト効率）:       {cpi:>12.3f}      → {cpi_status}")

        # 予測
        print(f"\n  ■ 完成時予測")
        print(f"    EAC（完成時総コスト）:   {eac:>12,.0f} 万円")
        print(f"    ETC（残作業コスト）:     {etc:>12,.0f} 万円")
        print(f"    VAC（完成時コスト差異）: {vac:>+12,.0f} 万円")

        # 進捗
        print(f"\n  ■ 進捗状況")
        print(f"    作業完了率:   {pct_complete:>6.1f}%")
        print(f"    予算消費率:   {pct_spent:>6.1f}%")

        # バーグラフ
        bar_width = 40
        pv_bar = int(pv / self.bac * bar_width)
        ev_bar = int(ev / self.bac * bar_width)
        ac_bar = int(ac / self.bac * bar_width)
        print(f"\n  ■ 視覚的な比較")
        print(f"    PV: [{'#' * pv_bar}{'-' * (bar_width - pv_bar)}] {pv:,.0f}")
        print(f"    EV: [{'#' * ev_bar}{'-' * (bar_width - ev_bar)}] {ev:,.0f}")
        print(f"    AC: [{'#' * ac_bar}{'-' * (bar_width - ac_bar)}] {ac:,.0f}")

        # 総合判定
        print(f"\n  ■ 総合判定")
        if spi >= 1.0 and cpi >= 1.0:
            print("    → スケジュール・コストともに良好です。この調子で進めましょう。")
        elif spi >= 1.0 and cpi < 1.0:
            print("    → スケジュールは順調ですが、コスト管理に注意が必要です。")
        elif spi < 1.0 and cpi >= 1.0:
            print("    → コストは予算内ですが、スケジュールの挽回策が必要です。")
        else:
            print("    → スケジュール・コストともに問題があります。是正措置が急務です。")

        return {
            "SV": sv, "CV": cv, "SPI": spi, "CPI": cpi,
            "EAC": eac, "ETC": etc, "VAC": vac,
        }

    def show_trend(self):
        """期間ごとのトレンドを表示します"""
        if len(self.periods) < 2:
            print("  ※ トレンド表示には2期間以上のデータが必要です。")
            return

        print(f"\n  ━━━ EVM トレンド分析: {self.project_name} ━━━")
        print(f"  BAC = {self.bac:,.0f} 万円")

        # ヘッダー
        print(f"\n    {'期間':<8} {'PV':>8} {'EV':>8} {'AC':>8} "
              f"{'SV':>8} {'CV':>8} {'SPI':>6} {'CPI':>6}")
        print("    " + "-" * 72)

        for period in self.periods:
            pv = period["PV"]
            ev = period["EV"]
            ac = period["AC"]
            sv = self.calculate_sv(ev, pv)
            cv = self.calculate_cv(ev, ac)
            spi = self.calculate_spi(ev, pv)
            cpi = self.calculate_cpi(ev, ac)

            print(f"    {period['name']:<8} {pv:>8,.0f} {ev:>8,.0f} {ac:>8,.0f} "
                  f"{sv:>+8,.0f} {cv:>+8,.0f} {spi:>6.3f} {cpi:>6.3f}")

        # SPIとCPIのグラフ
        print(f"\n  ■ SPI トレンド（1.0が基準）")
        for period in self.periods:
            spi = self.calculate_spi(period["EV"], period["PV"])
            bar_len = int(spi * 20)
            baseline = 20  # 1.0の位置
            bar = " " * min(bar_len, baseline) + "#" * abs(bar_len - baseline)
            marker = "|" if bar_len == baseline else ""
            print(f"    {period['name']:<8} {spi:.3f} {'#' * bar_len}")

        print(f"    {'基準':>8}       {'|' + '-' * 19}")

        print(f"\n  ■ CPI トレンド（1.0が基準）")
        for period in self.periods:
            cpi = self.calculate_cpi(period["EV"], period["AC"])
            bar_len = int(cpi * 20)
            print(f"    {period['name']:<8} {cpi:.3f} {'#' * bar_len}")

        print(f"    {'基準':>8}       {'|' + '-' * 19}")

    def show_eac_comparison(self):
        """EACの各手法による比較を表示します"""
        if not self.periods:
            return

        latest = self.periods[-1]
        ev = latest["EV"]
        ac = latest["AC"]

        print(f"\n  ■ EAC計算手法の比較")
        methods = [
            ("CPI継続", "cpi", "現在のCPI効率が続くと仮定"),
            ("残作業=予算", "typical", "残作業は予算通りに進むと仮定"),
            ("CPI×SPI", "combined", "効率低下が続くと仮定（最悪ケース）"),
        ]

        print(f"    {'手法':<14} {'EAC':>12} {'VAC':>12} {'仮定'}")
        print("    " + "-" * 60)
        for name, method, desc in methods:
            eac = self.calculate_eac(ac, ev, method)
            vac = self.calculate_vac(eac)
            print(f"    {name:<14} {eac:>12,.0f} {vac:>+12,.0f} {desc}")


def show_evm_formulas():
    """EVM の計算式一覧を表示します"""
    print("""
  ━━━ EVM 計算式一覧（試験頻出！） ━━━

  ■ 基本用語
    BAC = Budget at Completion（完成時総予算）
    PV  = Planned Value（計画価値）= 計画した作業の予算
    EV  = Earned Value（出来高）= 完了した作業の予算上の価値
    AC  = Actual Cost（実コスト）= 実際にかかったコスト

  ■ 差異指標（Variance）
    SV = EV - PV   （スケジュール差異）
    CV = EV - AC   （コスト差異）
    ※ 正なら良好、負なら問題あり

  ■ 効率指数（Index）
    SPI = EV / PV  （スケジュール効率指数）
    CPI = EV / AC  （コスト効率指数）
    ※ 1.0以上なら良好、1.0未満なら問題あり

  ■ 完成時予測
    EAC = BAC / CPI          （完成時総コスト見積：CPI継続仮定）
    EAC = AC + (BAC - EV)    （完成時総コスト見積：残作業は予算通り仮定）
    ETC = EAC - AC           （残作業コスト見積）
    VAC = BAC - EAC          （完成時コスト差異）

  ■ 覚え方のコツ
    - SV/CV: EV から引く（EV - PV, EV - AC）
    - SPI/CPI: EV で割る（EV/PV, EV/AC）
    - 「EVが中心」と覚えましょう!
""")


# ============================================================
# 対話モード
# ============================================================

def interactive_mode():
    """対話型のEVM計算ツールです"""
    print("\n" + "=" * 55)
    print("  EVM計算ツール - 対話モード")
    print("=" * 55)
    print("  操作を選んでください:")
    print("    1. 新しいプロジェクトを分析")
    print("    2. クイック計算（PV, EV, AC入力）")
    print("    3. 計算式一覧を表示")
    print("    0. 終了")
    print("-" * 55)

    while True:
        choice = input("\n  選択 (0-3): ").strip()

        if choice == "0":
            print("  EVM計算ツールを終了します。")
            break

        elif choice == "1":
            name = input("  プロジェクト名: ").strip() or "プロジェクト"
            try:
                bac = float(input("  BAC（完成時総予算、万円）: "))
                calc = EVMCalculator(name, bac)

                print("  期間データを入力します（空行で終了）:")
                period_num = 1
                while True:
                    period_name = input(f"  期間名 [{period_num}月目]: ").strip()
                    if not period_name:
                        if period_num == 1:
                            period_name = f"{period_num}月目"
                        else:
                            break
                    if period_num == 1 and not period_name:
                        period_name = f"{period_num}月目"

                    try:
                        pv = float(input(f"    PV（計画価値）: "))
                        ev = float(input(f"    EV（出来高）: "))
                        ac = float(input(f"    AC（実コスト）: "))
                        calc.add_period(period_name, pv, ev, ac)
                        period_num += 1
                    except ValueError:
                        print("    ※ 数値を入力してください。")

                if calc.periods:
                    calc.analyze_period()
                    if len(calc.periods) > 1:
                        calc.show_trend()
                    calc.show_eac_comparison()
            except ValueError:
                print("  ※ 正しい数値を入力してください。")

        elif choice == "2":
            try:
                bac = float(input("  BAC（完成時総予算）: "))
                pv = float(input("  PV（計画価値）: "))
                ev = float(input("  EV（出来高）: "))
                ac = float(input("  AC（実コスト）: "))

                calc = EVMCalculator("クイック計算", bac)
                calc.add_period("現時点", pv, ev, ac)
                calc.analyze_period()
                calc.show_eac_comparison()
            except ValueError:
                print("  ※ 正しい数値を入力してください。")

        elif choice == "3":
            show_evm_formulas()

        else:
            print("  ※ 0-3の番号を入力してください。")


# === デモンストレーション ===
print("=" * 55)
print("  EVM計算ツール")
print("  ～ プロジェクトの健全性を数値で把握しよう ～")
print("=" * 55)

# 計算式一覧
show_evm_formulas()

# --- デモ1: 基本的なEVM分析 ---
print("\n━━━ デモ1: 基本的なEVM分析 ━━━")
print("  シナリオ: 10ヶ月、予算1000万円のシステム開発プロジェクト")

calc1 = EVMCalculator("社内システム開発", 1000)
calc1.add_period("3ヶ月目", pv=300, ev=250, ac=280)
calc1.analyze_period()
calc1.show_eac_comparison()

# --- デモ2: 各パターンの分析 ---
print("\n\n━━━ デモ2: 4つのプロジェクト状態パターン ━━━")

patterns = [
    ("パターンA: 順調", 500, 520, 480,
     "スケジュール前倒し & コスト削減 → 理想的な状態です"),
    ("パターンB: 遅延・予算内", 500, 400, 450,
     "スケジュール遅延 & コスト余裕あり → 人員追加を検討しましょう"),
    ("パターンC: 順調・超過", 500, 510, 600,
     "スケジュール順調 & コスト超過 → コスト管理を見直しましょう"),
    ("パターンD: 危険", 500, 350, 550,
     "スケジュール遅延 & コスト超過 → 是正措置が急務です"),
]

for name, pv, ev, ac, description in patterns:
    print(f"\n  ■ {name}")
    print(f"    説明: {description}")
    calc = EVMCalculator(name, 1000)
    calc.add_period("中間", pv, ev, ac)

    sv = calc.calculate_sv(ev, pv)
    cv = calc.calculate_cv(ev, ac)
    spi = calc.calculate_spi(ev, pv)
    cpi = calc.calculate_cpi(ev, ac)
    eac = calc.calculate_eac(ac, ev, "cpi")

    print(f"    PV={pv}, EV={ev}, AC={ac}")
    print(f"    SV={sv:+.0f}, CV={cv:+.0f}, SPI={spi:.3f}, CPI={cpi:.3f}")
    print(f"    EAC={eac:,.0f}万円 (BAC=1000万円)")

# --- デモ3: トレンド分析 ---
print("\n\n━━━ デモ3: 月次トレンド分析 ━━━")
calc3 = EVMCalculator("Webリニューアル", 2400)
monthly_data = [
    ("1月", 200, 180, 190),
    ("2月", 400, 350, 380),
    ("3月", 700, 600, 680),
    ("4月", 1000, 850, 960),
    ("5月", 1300, 1150, 1300),
    ("6月", 1600, 1400, 1580),
]
for name, pv, ev, ac in monthly_data:
    calc3.add_period(name, pv, ev, ac)

calc3.show_trend()
calc3.analyze_period()
calc3.show_eac_comparison()

# --- 試験問題パターン ---
print("\n\n━━━ 試験で出題される典型的な計算パターン ━━━")
print("""
  ■ パターン1: EACの計算
    問: BAC=800万円、EV=400万円、AC=500万円のとき、EACは？
    解: CPI = EV/AC = 400/500 = 0.8
        EAC = BAC/CPI = 800/0.8 = 1000万円

  ■ パターン2: 完了予定日の判断
    問: SPI=0.8のプロジェクト、計画10ヶ月。完了見込みは？
    解: 予想完了期間 = 計画期間 / SPI = 10 / 0.8 = 12.5ヶ月
        → 2.5ヶ月遅延の見込み

  ■ パターン3: SVとCVの正負判定
    問: PV=600, EV=500, AC=550 → 進捗と予算の状況は？
    解: SV = 500-600 = -100 → スケジュール遅延
        CV = 500-550 = -50  → コスト超過

  ■ 覚え方のまとめ
    EV が基準（中心）！
    SV/CV → EVから引く
    SPI/CPI → EVで割る
    正/1.0以上 → 良好
    負/1.0未満 → 問題あり
""")

# --- 対話モード ---
interactive_mode()

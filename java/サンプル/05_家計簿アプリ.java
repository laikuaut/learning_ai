/**
 * ============================================
 *   家計簿アプリ
 * ============================================
 *
 * 【学べる内容】
 *   - ArrayList によるデータ管理
 *   - HashMap によるキーと値のマッピング
 *   - 例外処理（try-catch）の実践
 *   - 日付の扱い（LocalDate, DateTimeFormatter）
 *   - 列挙型（enum）の使い方
 *   - 文字列フォーマットによる帳票出力
 *   - メニュー駆動型プログラムの設計
 *   - クラスの設計とカプセル化
 *
 * 【実行方法】
 *   javac 05_家計簿アプリ.java
 *   java HouseholdBudget
 */

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

// ================================================================
//  列挙型（enum）: 取引の種類を定義
//  enumは決められた値だけを取る型（タイプセーフ）
// ================================================================
enum TransactionType {
    INCOME("収入"),    // 収入
    EXPENSE("支出");   // 支出

    // enumにもフィールドとメソッドを定義できる
    private final String label;

    TransactionType(String label) {
        this.label = label;
    }

    public String getLabel() {
        return label;
    }
}

// ================================================================
//  取引（Transaction）クラス: 1件の収支を表す
// ================================================================
class Transaction {
    // フィールド（private = カプセル化）
    private LocalDate date;            // 日付
    private TransactionType type;      // 種類（収入/支出）
    private String category;           // カテゴリ
    private int amount;                // 金額
    private String memo;               // メモ

    // コンストラクタ
    public Transaction(LocalDate date, TransactionType type,
                       String category, int amount, String memo) {
        this.date = date;
        this.type = type;
        this.category = category;
        this.amount = amount;
        this.memo = memo;
    }

    // --- ゲッターメソッド（getter）: フィールドを安全に取得 ---
    public LocalDate getDate() { return date; }
    public TransactionType getType() { return type; }
    public String getCategory() { return category; }
    public int getAmount() { return amount; }
    public String getMemo() { return memo; }

    // 日付を文字列にフォーマットして返す
    public String getFormattedDate() {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy/MM/dd");
        return date.format(formatter);
    }

    // 表示用の文字列を返す
    @Override
    public String toString() {
        String sign = (type == TransactionType.INCOME) ? "+" : "-";
        return String.format("%s | %s | %-6s | %s%,d円 | %s",
                getFormattedDate(), type.getLabel(), category,
                sign, amount, memo);
    }
}

// ================================================================
//  メインクラス: 家計簿アプリ
// ================================================================
public class HouseholdBudget {

    // 全取引を保存するリスト
    static ArrayList<Transaction> transactions = new ArrayList<>();

    // カテゴリの選択肢
    static final String[] INCOME_CATEGORIES = {"給料", "副業", "お小遣い", "投資", "その他"};
    static final String[] EXPENSE_CATEGORIES = {"食費", "交通費", "住居費", "光熱費", "通信費",
                                                 "娯楽費", "衣服費", "医療費", "教育費", "その他"};

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("╔══════════════════════════════════════╗");
        System.out.println("║        家計簿アプリ v1.0             ║");
        System.out.println("╚══════════════════════════════════════╝");
        System.out.println();

        // サンプルデータを登録
        addSampleData();

        boolean running = true;
        while (running) {
            displayMenu();
            System.out.print("選択してください (1-7): ");
            String choice = scanner.nextLine().trim();

            switch (choice) {
                case "1":
                    addTransaction(scanner, TransactionType.INCOME);
                    break;
                case "2":
                    addTransaction(scanner, TransactionType.EXPENSE);
                    break;
                case "3":
                    viewAllTransactions();
                    break;
                case "4":
                    showSummary();
                    break;
                case "5":
                    showCategoryBreakdown();
                    break;
                case "6":
                    showMonthlyReport();
                    break;
                case "7":
                    running = false;
                    System.out.println("\nアプリを終了します。お金の管理、頑張りましょう！");
                    break;
                default:
                    System.out.println("\n※ 1〜7の番号を入力してください。");
            }
        }

        scanner.close();
    }

    /**
     * メニューを表示する
     */
    static void displayMenu() {
        System.out.println("\n┌──────────── メニュー ────────────┐");
        System.out.println("│  1. 収入を記録する               │");
        System.out.println("│  2. 支出を記録する               │");
        System.out.println("│  3. 全取引を表示する             │");
        System.out.println("│  4. 収支サマリーを表示           │");
        System.out.println("│  5. カテゴリ別の内訳を表示       │");
        System.out.println("│  6. 月別レポートを表示           │");
        System.out.println("│  7. 終了                         │");
        System.out.println("└──────────────────────────────────┘");
    }

    /**
     * サンプルデータを追加する
     */
    static void addSampleData() {
        LocalDate today = LocalDate.now();
        LocalDate lastMonth = today.minusMonths(1);

        // 先月のデータ
        transactions.add(new Transaction(lastMonth.withDayOfMonth(25),
                TransactionType.INCOME, "給料", 250000, "月給"));
        transactions.add(new Transaction(lastMonth.withDayOfMonth(3),
                TransactionType.EXPENSE, "住居費", 80000, "家賃"));
        transactions.add(new Transaction(lastMonth.withDayOfMonth(10),
                TransactionType.EXPENSE, "食費", 35000, "食料品"));
        transactions.add(new Transaction(lastMonth.withDayOfMonth(15),
                TransactionType.EXPENSE, "光熱費", 12000, "電気・ガス"));

        // 今月のデータ
        transactions.add(new Transaction(today.withDayOfMonth(1),
                TransactionType.INCOME, "給料", 250000, "月給"));
        transactions.add(new Transaction(today.withDayOfMonth(2),
                TransactionType.INCOME, "副業", 30000, "フリーランス案件"));
        transactions.add(new Transaction(today.withDayOfMonth(3),
                TransactionType.EXPENSE, "住居費", 80000, "家賃"));
        transactions.add(new Transaction(today.withDayOfMonth(5),
                TransactionType.EXPENSE, "食費", 8500, "スーパー"));
        transactions.add(new Transaction(today.withDayOfMonth(8),
                TransactionType.EXPENSE, "交通費", 5000, "定期券"));
        transactions.add(new Transaction(today.withDayOfMonth(10),
                TransactionType.EXPENSE, "娯楽費", 3000, "映画鑑賞"));

        System.out.printf("サンプルデータ %d 件を登録しました。%n", transactions.size());
    }

    /**
     * 取引を追加する
     *
     * @param scanner 入力用Scanner
     * @param type    取引種類（収入/支出）
     */
    static void addTransaction(Scanner scanner, TransactionType type) {
        System.out.printf("%n--- %sの記録 ---%n", type.getLabel());

        // --- 日付の入力 ---
        System.out.print("日付を入力 (yyyy/MM/dd) [空欄で今日]: ");
        String dateStr = scanner.nextLine().trim();
        LocalDate date;

        if (dateStr.isEmpty()) {
            date = LocalDate.now();
        } else {
            try {
                // DateTimeFormatter で文字列を日付に変換
                DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy/MM/dd");
                date = LocalDate.parse(dateStr, formatter);
            } catch (DateTimeParseException e) {
                System.out.println("※ 日付の形式が正しくありません。（例: 2026/03/29）");
                return;
            }
        }

        // --- カテゴリの選択 ---
        String[] categories = (type == TransactionType.INCOME)
                ? INCOME_CATEGORIES : EXPENSE_CATEGORIES;

        System.out.println("カテゴリを選んでください:");
        for (int i = 0; i < categories.length; i++) {
            System.out.printf("  %d. %s%n", i + 1, categories[i]);
        }
        System.out.print("番号: ");

        int catIndex;
        try {
            catIndex = Integer.parseInt(scanner.nextLine().trim()) - 1;
        } catch (NumberFormatException e) {
            System.out.println("※ 数値を入力してください。");
            return;
        }

        if (catIndex < 0 || catIndex >= categories.length) {
            System.out.println("※ 正しい番号を入力してください。");
            return;
        }
        String category = categories[catIndex];

        // --- 金額の入力 ---
        System.out.print("金額（円）: ");
        int amount;
        try {
            amount = Integer.parseInt(scanner.nextLine().trim());
            if (amount <= 0) {
                System.out.println("※ 正の数を入力してください。");
                return;
            }
        } catch (NumberFormatException e) {
            System.out.println("※ 数値を入力してください。");
            return;
        }

        // --- メモの入力 ---
        System.out.print("メモ（任意）: ");
        String memo = scanner.nextLine().trim();
        if (memo.isEmpty()) {
            memo = "-";
        }

        // --- 取引を作成してリストに追加 ---
        Transaction transaction = new Transaction(date, type, category, amount, memo);
        transactions.add(transaction);

        System.out.printf("%n%sを記録しました: %s / %s / %,d円%n",
                type.getLabel(), transaction.getFormattedDate(), category, amount);
    }

    /**
     * 全取引を表示する
     */
    static void viewAllTransactions() {
        System.out.println("\n=== 全取引一覧 ===");

        if (transactions.isEmpty()) {
            System.out.println("取引が記録されていません。");
            return;
        }

        System.out.println("─".repeat(65));
        System.out.printf("%-12s | %-4s | %-6s | %10s | %s%n",
                "日付", "種別", "カテゴリ", "金額", "メモ");
        System.out.println("─".repeat(65));

        for (Transaction t : transactions) {
            System.out.println(t);
        }

        System.out.println("─".repeat(65));
        System.out.printf("合計 %d 件%n", transactions.size());
    }

    /**
     * 収支サマリーを表示する
     */
    static void showSummary() {
        System.out.println("\n=== 収支サマリー ===");

        int totalIncome = 0;
        int totalExpense = 0;

        // 全取引を走査して収入と支出を集計
        for (Transaction t : transactions) {
            if (t.getType() == TransactionType.INCOME) {
                totalIncome += t.getAmount();
            } else {
                totalExpense += t.getAmount();
            }
        }

        int balance = totalIncome - totalExpense;

        System.out.println("┌──────────────────────────────┐");
        System.out.printf("│  総収入  : %,12d 円    │%n", totalIncome);
        System.out.printf("│  総支出  : %,12d 円    │%n", totalExpense);
        System.out.println("├──────────────────────────────┤");

        // 残高に応じて表示を変える
        if (balance >= 0) {
            System.out.printf("│  残高    : +%,11d 円 ◎ │%n", balance);
        } else {
            System.out.printf("│  残高    : %,12d 円 × │%n", balance);
        }
        System.out.println("└──────────────────────────────┘");

        // 貯蓄率の計算
        if (totalIncome > 0) {
            double savingRate = (double) balance / totalIncome * 100;
            System.out.printf("  貯蓄率: %.1f%%%n", savingRate);
            if (savingRate >= 20) {
                System.out.println("  → 素晴らしい貯蓄率です！");
            } else if (savingRate >= 10) {
                System.out.println("  → まずまずの貯蓄率です。");
            } else if (savingRate >= 0) {
                System.out.println("  → もう少し節約を心がけましょう。");
            } else {
                System.out.println("  → 支出が収入を超えています。見直しが必要です。");
            }
        }
    }

    /**
     * カテゴリ別の内訳を表示する
     * HashMapを使ってカテゴリごとの合計を集計
     */
    static void showCategoryBreakdown() {
        System.out.println("\n=== カテゴリ別内訳 ===");

        // HashMap: カテゴリ名をキー、合計金額を値として格納
        HashMap<String, Integer> incomeByCategory = new HashMap<>();
        HashMap<String, Integer> expenseByCategory = new HashMap<>();
        int totalExpense = 0;

        // 全取引をカテゴリ別に集計
        for (Transaction t : transactions) {
            HashMap<String, Integer> map = (t.getType() == TransactionType.INCOME)
                    ? incomeByCategory : expenseByCategory;

            // getOrDefault: キーがなければデフォルト値（0）を返す
            int current = map.getOrDefault(t.getCategory(), 0);
            map.put(t.getCategory(), current + t.getAmount());

            if (t.getType() == TransactionType.EXPENSE) {
                totalExpense += t.getAmount();
            }
        }

        // --- 収入の内訳 ---
        System.out.println("\n【収入の内訳】");
        if (incomeByCategory.isEmpty()) {
            System.out.println("  収入の記録がありません。");
        } else {
            // Map.Entry で HashMap のキーと値のペアを取得
            for (Map.Entry<String, Integer> entry : incomeByCategory.entrySet()) {
                System.out.printf("  %-8s : %,10d 円%n",
                        entry.getKey(), entry.getValue());
            }
        }

        // --- 支出の内訳（棒グラフ付き）---
        System.out.println("\n【支出の内訳】");
        if (expenseByCategory.isEmpty()) {
            System.out.println("  支出の記録がありません。");
        } else {
            for (Map.Entry<String, Integer> entry : expenseByCategory.entrySet()) {
                int amount = entry.getValue();
                // 割合を計算してグラフ化
                double ratio = (totalExpense > 0) ? (double) amount / totalExpense * 100 : 0;
                int barLen = (int) (ratio / 5); // 5%ごとに1ブロック
                String bar = "█".repeat(barLen);

                System.out.printf("  %-8s : %,10d 円 (%5.1f%%) %s%n",
                        entry.getKey(), amount, ratio, bar);
            }
        }
    }

    /**
     * 月別レポートを表示する
     */
    static void showMonthlyReport() {
        System.out.println("\n=== 月別レポート ===");

        if (transactions.isEmpty()) {
            System.out.println("取引が記録されていません。");
            return;
        }

        // 月ごとの収入・支出を集計するHashMap
        // キー: "yyyy/MM" 形式の文字列
        HashMap<String, int[]> monthlyData = new HashMap<>();
        DateTimeFormatter monthFormatter = DateTimeFormatter.ofPattern("yyyy/MM");

        for (Transaction t : transactions) {
            String monthKey = t.getDate().format(monthFormatter);

            // computeIfAbsent: キーがなければ新しい配列を作成
            int[] amounts = monthlyData.computeIfAbsent(monthKey, k -> new int[2]);

            if (t.getType() == TransactionType.INCOME) {
                amounts[0] += t.getAmount();  // [0] = 収入
            } else {
                amounts[1] += t.getAmount();  // [1] = 支出
            }
        }

        // 月ごとの結果を表示
        System.out.println("─".repeat(55));
        System.out.printf("%-10s | %12s | %12s | %12s%n",
                "月", "収入", "支出", "残高");
        System.out.println("─".repeat(55));

        for (Map.Entry<String, int[]> entry : monthlyData.entrySet()) {
            int income = entry.getValue()[0];
            int expense = entry.getValue()[1];
            int balance = income - expense;

            String balanceStr = (balance >= 0)
                    ? String.format("+%,d", balance)
                    : String.format("%,d", balance);

            System.out.printf("%-10s | %,10d円 | %,10d円 | %10s円%n",
                    entry.getKey(), income, expense, balanceStr);
        }

        System.out.println("─".repeat(55));
    }
}

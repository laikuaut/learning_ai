/**
 * ============================================
 *   成績管理システム
 * ============================================
 *
 * 【学べる内容】
 *   - 配列（array）と ArrayList の使い方
 *   - メソッド（method）の定義・引数・戻り値
 *   - for ループ・拡張for文（for-each）
 *   - 条件分岐（if-else, switch）
 *   - 文字列のフォーマット出力
 *   - メニュー方式のプログラム設計
 *   - Collections クラスの活用
 *
 * 【実行方法】
 *   javac 02_成績管理システム.java
 *   java GradeManager
 */

import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

public class GradeManager {

    // ========== フィールド（クラス変数） ==========
    // 学生の名前を格納するリスト
    static ArrayList<String> studentNames = new ArrayList<>();
    // 学生の点数を格納するリスト（名前と同じインデックスで対応）
    static ArrayList<Integer> studentScores = new ArrayList<>();

    // ========== メインメソッド ==========
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("╔══════════════════════════════════════╗");
        System.out.println("║       成績管理システム v1.0          ║");
        System.out.println("╚══════════════════════════════════════╝");
        System.out.println();

        // サンプルデータを登録（デモ用）
        addSampleData();

        // メニューループ: ユーザーが「6」を入力するまで繰り返す
        boolean running = true;
        while (running) {
            displayMenu();
            System.out.print("選択してください (1-6): ");
            String choice = scanner.nextLine().trim();

            // switch文で選択に応じた処理を実行
            switch (choice) {
                case "1":
                    addStudent(scanner);
                    break;
                case "2":
                    viewAllStudents();
                    break;
                case "3":
                    showStatistics();
                    break;
                case "4":
                    findTopStudent();
                    break;
                case "5":
                    searchStudent(scanner);
                    break;
                case "6":
                    running = false;
                    System.out.println("\nシステムを終了します。お疲れさまでした！");
                    break;
                default:
                    System.out.println("\n※ 1〜6の数字を入力してください。");
            }
        }

        scanner.close();
    }

    /**
     * メニューを表示するメソッド
     */
    static void displayMenu() {
        System.out.println("\n┌──────────── メニュー ────────────┐");
        System.out.println("│  1. 学生を追加する               │");
        System.out.println("│  2. 全学生の成績を表示           │");
        System.out.println("│  3. 統計情報を表示               │");
        System.out.println("│  4. 最高得点者を表示             │");
        System.out.println("│  5. 学生を検索する               │");
        System.out.println("│  6. 終了                         │");
        System.out.println("└──────────────────────────────────┘");
    }

    /**
     * サンプルデータを追加するメソッド
     */
    static void addSampleData() {
        // 配列を使ってサンプルデータを定義
        String[] names = {"田中太郎", "鈴木花子", "佐藤次郎", "山田美咲", "高橋一郎"};
        int[] scores = {85, 92, 78, 95, 88};

        // 拡張for文（for-each）ではなく、インデックスが必要なので通常のfor文を使用
        for (int i = 0; i < names.length; i++) {
            studentNames.add(names[i]);
            studentScores.add(scores[i]);
        }

        System.out.printf("サンプルデータ %d 件を登録しました。%n", names.length);
    }

    /**
     * 学生を追加するメソッド
     *
     * @param scanner 入力用Scannerオブジェクト
     */
    static void addStudent(Scanner scanner) {
        System.out.println("\n--- 学生の追加 ---");

        System.out.print("学生の名前: ");
        String name = scanner.nextLine().trim();

        // 名前が空でないかチェック
        if (name.isEmpty()) {
            System.out.println("※ 名前を入力してください。");
            return; // メソッドを早期リターン
        }

        System.out.print("点数 (0-100): ");
        int score;
        try {
            score = Integer.parseInt(scanner.nextLine().trim());
        } catch (NumberFormatException e) {
            // 数値でない入力への対処
            System.out.println("※ 数値を入力してください。");
            return;
        }

        // 点数の範囲チェック
        if (score < 0 || score > 100) {
            System.out.println("※ 0〜100の範囲で入力してください。");
            return;
        }

        // ArrayListに追加
        studentNames.add(name);
        studentScores.add(score);

        System.out.printf("%s さん（%d 点）を登録しました。%n", name, score);
    }

    /**
     * 全学生の成績を一覧表示するメソッド
     */
    static void viewAllStudents() {
        System.out.println("\n--- 全学生の成績一覧 ---");

        // データがない場合のチェック
        if (studentNames.isEmpty()) {
            System.out.println("※ 登録されている学生がいません。");
            return;
        }

        // テーブルヘッダー
        System.out.println("┌────┬──────────┬──────┬──────┐");
        System.out.println("│ No │  名前    │ 点数 │ 評価 │");
        System.out.println("├────┼──────────┼──────┼──────┤");

        // 拡張for文は使えない（インデックスが必要なため）ので通常のforを使用
        for (int i = 0; i < studentNames.size(); i++) {
            String name = studentNames.get(i);
            int score = studentScores.get(i);
            String grade = getGrade(score);

            // printf でフォーマット出力
            System.out.printf("│ %2d │ %-8s │ %3d  │  %s  │%n",
                    i + 1, name, score, grade);
        }

        System.out.println("└────┴──────────┴──────┴──────┘");
        System.out.printf("登録人数: %d 名%n", studentNames.size());
    }

    /**
     * 統計情報を表示するメソッド
     */
    static void showStatistics() {
        System.out.println("\n--- 統計情報 ---");

        if (studentScores.isEmpty()) {
            System.out.println("※ データがありません。");
            return;
        }

        // 平均点を計算
        double average = calculateAverage();
        // 最高点と最低点を取得（Collectionsクラスの便利メソッド）
        int maxScore = Collections.max(studentScores);
        int minScore = Collections.min(studentScores);

        // 評価ごとの人数を数える
        int countA = 0, countB = 0, countC = 0, countD = 0, countF = 0;
        for (int score : studentScores) {  // 拡張for文（for-each）
            switch (getGrade(score)) {
                case "A": countA++; break;
                case "B": countB++; break;
                case "C": countC++; break;
                case "D": countD++; break;
                case "F": countF++; break;
            }
        }

        System.out.printf("  受験者数 : %d 名%n", studentScores.size());
        System.out.printf("  平均点   : %.1f 点%n", average);
        System.out.printf("  最高点   : %d 点%n", maxScore);
        System.out.printf("  最低点   : %d 点%n", minScore);
        System.out.printf("  点数幅   : %d 点%n", maxScore - minScore);
        System.out.println();
        System.out.println("  【評価別人数】");
        System.out.printf("    A (90-100): %d 名  ", countA);
        printBar(countA, studentScores.size());
        System.out.printf("    B (80-89) : %d 名  ", countB);
        printBar(countB, studentScores.size());
        System.out.printf("    C (70-79) : %d 名  ", countC);
        printBar(countC, studentScores.size());
        System.out.printf("    D (60-69) : %d 名  ", countD);
        printBar(countD, studentScores.size());
        System.out.printf("    F (0-59)  : %d 名  ", countF);
        printBar(countF, studentScores.size());
    }

    /**
     * 簡易棒グラフを表示する
     */
    static void printBar(int count, int total) {
        int barLength = (total > 0) ? (count * 20 / total) : 0;
        System.out.println("█".repeat(barLength));
    }

    /**
     * 最高得点者を表示するメソッド
     */
    static void findTopStudent() {
        System.out.println("\n--- 最高得点者 ---");

        if (studentScores.isEmpty()) {
            System.out.println("※ データがありません。");
            return;
        }

        int maxScore = Collections.max(studentScores);

        System.out.printf("最高点: %d 点%n", maxScore);
        System.out.println("該当者:");

        // 最高点の学生が複数いる場合を考慮
        for (int i = 0; i < studentScores.size(); i++) {
            if (studentScores.get(i) == maxScore) {
                System.out.printf("  ★ %s さん%n", studentNames.get(i));
            }
        }
    }

    /**
     * 名前で学生を検索するメソッド
     *
     * @param scanner 入力用Scannerオブジェクト
     */
    static void searchStudent(Scanner scanner) {
        System.out.println("\n--- 学生検索 ---");
        System.out.print("検索する名前（部分一致）: ");
        String keyword = scanner.nextLine().trim();

        if (keyword.isEmpty()) {
            System.out.println("※ キーワードを入力してください。");
            return;
        }

        boolean found = false;
        for (int i = 0; i < studentNames.size(); i++) {
            // String.contains() で部分一致検索
            if (studentNames.get(i).contains(keyword)) {
                if (!found) {
                    System.out.println("検索結果:");
                    found = true;
                }
                System.out.printf("  %s : %d 点 (%s)%n",
                        studentNames.get(i),
                        studentScores.get(i),
                        getGrade(studentScores.get(i)));
            }
        }

        if (!found) {
            System.out.printf("「%s」に一致する学生は見つかりませんでした。%n", keyword);
        }
    }

    // ========== ユーティリティメソッド ==========

    /**
     * 平均点を計算して返すメソッド
     *
     * @return 平均点（double型）
     */
    static double calculateAverage() {
        int sum = 0;
        // 拡張for文で全要素を合計
        for (int score : studentScores) {
            sum += score;
        }
        // int同士の割り算は小数が切り捨てられるため、doubleにキャスト
        return (double) sum / studentScores.size();
    }

    /**
     * 点数から評価（グレード）を返すメソッド
     *
     * @param score 点数（0-100）
     * @return 評価文字列
     */
    static String getGrade(int score) {
        if (score >= 90) return "A";
        else if (score >= 80) return "B";
        else if (score >= 70) return "C";
        else if (score >= 60) return "D";
        else return "F";
    }
}

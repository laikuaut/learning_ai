/**
 * ============================================
 *   自己紹介カード生成プログラム
 * ============================================
 *
 * 【学べる内容】
 *   - 変数（variable）とデータ型（data type）の基本
 *   - 文字列（String）、整数（int）の扱い方
 *   - Scanner クラスによるキーボード入力
 *   - printf によるフォーマット出力
 *   - 文字列の連結と操作
 *   - メソッド（method）の定義と呼び出し
 *
 * 【実行方法】
 *   javac 01_自己紹介カード.java
 *   java SelfIntroductionCard
 */

import java.util.Scanner;

public class SelfIntroductionCard {

    // ========== 定数の定義 ==========
    // カードの幅（文字数）
    static final int CARD_WIDTH = 48;
    // 罫線に使う文字
    static final String BORDER_CHAR = "=";
    static final String SIDE_CHAR = "|";

    // ========== メインメソッド ==========
    public static void main(String[] args) {

        // Scannerオブジェクトを作成してキーボード入力を受け取る準備
        Scanner scanner = new Scanner(System.in);

        // --- プログラムの開始メッセージ ---
        System.out.println("╔══════════════════════════════════════════╗");
        System.out.println("║     自己紹介カード ジェネレーター        ║");
        System.out.println("╚══════════════════════════════════════════╝");
        System.out.println();

        // --- ユーザーから情報を入力してもらう ---
        // String型: 文字列を格納するデータ型
        System.out.print("お名前を入力してください: ");
        String name = scanner.nextLine();

        // int型: 整数を格納するデータ型
        System.out.print("年齢を入力してください: ");
        int age = Integer.parseInt(scanner.nextLine());

        System.out.print("趣味を入力してください: ");
        String hobby = scanner.nextLine();

        System.out.print("好きな食べ物を入力してください: ");
        String food = scanner.nextLine();

        System.out.print("今年の目標を入力してください: ");
        String goal = scanner.nextLine();

        System.out.print("一言メッセージを入力してください: ");
        String message = scanner.nextLine();

        System.out.println();

        // --- 自己紹介カードを表示 ---
        displayCard(name, age, hobby, food, goal, message);

        // --- おまけ: プロフィールサマリー ---
        displaySummary(name, age, hobby);

        // Scannerを閉じる（リソースの解放）
        scanner.close();
    }

    /**
     * 自己紹介カードを罫線付きで表示するメソッド
     *
     * @param name    名前
     * @param age     年齢
     * @param hobby   趣味
     * @param food    好きな食べ物
     * @param goal    目標
     * @param message 一言メッセージ
     */
    static void displayCard(String name, int age, String hobby,
                            String food, String goal, String message) {

        // 上部の罫線を表示
        printBorder();

        // タイトル行を中央揃えで表示
        printCentered("★ 自己紹介カード ★");

        // 区切り線
        printSeparator();

        // 各項目をフォーマットして表示
        // printf の書式指定子:
        //   %s  = 文字列（String）
        //   %d  = 整数（decimal/integer）
        //   %-Ns = 左揃え（N文字分の幅を確保）
        printLine(String.format("  名前     : %s", name));
        printLine(String.format("  年齢     : %d 歳", age));
        printLine(String.format("  趣味     : %s", hobby));
        printLine(String.format("  好きな食べ物 : %s", food));

        // 区切り線
        printSeparator();

        // 目標とメッセージ
        printLine("  【今年の目標】");
        printLine(String.format("    %s", goal));
        printLine("");
        printLine("  【一言メッセージ】");
        printLine(String.format("    %s", message));

        // 下部の罫線を表示
        printBorder();
    }

    /**
     * プロフィールサマリーを表示するメソッド
     * printf のさまざまな書式を紹介
     */
    static void displaySummary(String name, int age, String hobby) {
        System.out.println();
        System.out.println("--- プロフィールサマリー ---");

        // printf: フォーマット付き出力（改行は自動では入らないので \n が必要）
        System.out.printf("名前: %s さん%n", name);
        System.out.printf("年齢: %d 歳（あと %d 年で %d 歳）%n",
                age, (10 - age % 10), age + (10 - age % 10));

        // 文字列の長さを取得
        System.out.printf("名前の文字数: %d 文字%n", name.length());

        // 文字列を大文字に変換（英語の場合有効）
        System.out.printf("名前（大文字）: %s%n", name.toUpperCase());

        // boolean型: 真偽値を格納するデータ型
        boolean isAdult = age >= 18;
        System.out.printf("成人かどうか: %b%n", isAdult);

        // double型: 小数を格納するデータ型
        double halfAge = age / 2.0;
        System.out.printf("年齢の半分: %.1f 歳%n", halfAge);

        System.out.println();
        System.out.printf("%s さん、素敵な自己紹介カードができました！%n", name);
    }

    // ========== カード描画用のヘルパーメソッド ==========

    /**
     * 上下の罫線を表示する
     */
    static void printBorder() {
        // String.repeat() で文字を繰り返す（Java 11以降）
        System.out.println("+" + "-".repeat(CARD_WIDTH - 2) + "+");
    }

    /**
     * 区切り線を表示する
     */
    static void printSeparator() {
        System.out.println("|" + ".".repeat(CARD_WIDTH - 2) + "|");
    }

    /**
     * テキストを中央揃えで表示する
     *
     * @param text 表示するテキスト
     */
    static void printCentered(String text) {
        // 中央に配置するために左側のパディングを計算
        int padding = (CARD_WIDTH - 2 - text.length()) / 2;
        // パディングが負にならないようにする
        if (padding < 0) padding = 0;

        String paddedText = " ".repeat(padding) + text;
        printLine(paddedText);
    }

    /**
     * カードの1行を左右の罫線付きで表示する
     *
     * @param content 行の内容
     */
    static void printLine(String content) {
        // コンテンツの長さに応じて右側を空白で埋める
        int contentWidth = CARD_WIDTH - 2; // 左右の "|" の分を引く
        if (content.length() > contentWidth) {
            content = content.substring(0, contentWidth);
        }
        // %-Ns で左揃え・N文字幅を指定
        System.out.printf("|%-" + contentWidth + "s|%n", content);
    }
}

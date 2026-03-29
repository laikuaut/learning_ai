/**
 * ============================================
 *   図形計算ツール（OOP版）
 * ============================================
 *
 * 【学べる内容】
 *   - インターフェース（interface）の定義と実装
 *   - 抽象クラス（abstract class）の使い方
 *   - 継承（inheritance）とオーバーライド
 *   - ポリモーフィズム（polymorphism）の実践
 *   - クラスの設計とコンストラクタ
 *   - Math クラスの数学関数（PI, sqrt, pow）
 *   - ArrayList による多態的なオブジェクト管理
 *
 * 【実行方法】
 *   javac 04_図形計算ツール.java
 *   java ShapeCalculator
 */

import java.util.ArrayList;
import java.util.Scanner;

// ================================================================
//  インターフェース（interface）: 図形が持つべき機能を定義
//  インターフェースは「何ができるか」を宣言する設計図
// ================================================================
interface Shape {
    /**
     * 面積を計算して返す
     * @return 面積（double型）
     */
    double area();

    /**
     * 周囲の長さを計算して返す
     * @return 周囲の長さ（double型）
     */
    double perimeter();

    /**
     * 図形の名前を返す
     * @return 図形名（String型）
     */
    String getName();

    /**
     * 図形の情報を文字列で返す
     * @return 情報文字列
     */
    String getInfo();
}

// ================================================================
//  抽象クラス（abstract class）: 共通処理をまとめた基底クラス
//  直接インスタンス化はできない（newできない）
// ================================================================
abstract class AbstractShape implements Shape {

    // 図形の名前（全サブクラス共通のフィールド）
    protected String name;

    // コンストラクタ: オブジェクト生成時に呼ばれる
    public AbstractShape(String name) {
        this.name = name;
    }

    // getName は全サブクラスで共通なのでここで実装
    @Override
    public String getName() {
        return name;
    }

    /**
     * 図形の計算結果を見やすく表示する共通メソッド
     */
    public void display() {
        System.out.println("┌──────────────────────────────┐");
        System.out.printf("│  図形: %-22s│%n", getName());
        System.out.println("├──────────────────────────────┤");
        System.out.printf("│  %s%n", getInfo());
        System.out.printf("│  面積    : %10.2f%n", area());
        System.out.printf("│  周囲の長さ: %8.2f%n", perimeter());
        System.out.println("└──────────────────────────────┘");
    }
}

// ================================================================
//  円（Circle）クラス: AbstractShape を継承
// ================================================================
class Circle extends AbstractShape {

    // フィールド（メンバ変数）
    private double radius;  // 半径

    // コンストラクタ
    public Circle(double radius) {
        // super() で親クラスのコンストラクタを呼ぶ
        super("円（Circle）");
        this.radius = radius;
    }

    // 面積 = π × 半径²
    @Override
    public double area() {
        return Math.PI * Math.pow(radius, 2);
    }

    // 周囲 = 2 × π × 半径
    @Override
    public double perimeter() {
        return 2 * Math.PI * radius;
    }

    @Override
    public String getInfo() {
        return String.format("半径: %.2f", radius);
    }
}

// ================================================================
//  長方形（Rectangle）クラス
// ================================================================
class Rectangle extends AbstractShape {

    private double width;   // 幅
    private double height;  // 高さ

    public Rectangle(double width, double height) {
        super("長方形（Rectangle）");
        this.width = width;
        this.height = height;
    }

    // 面積 = 幅 × 高さ
    @Override
    public double area() {
        return width * height;
    }

    // 周囲 = (幅 + 高さ) × 2
    @Override
    public double perimeter() {
        return (width + height) * 2;
    }

    @Override
    public String getInfo() {
        return String.format("幅: %.2f, 高さ: %.2f", width, height);
    }

    // 長方形独自のメソッド: 対角線の長さ
    public double diagonal() {
        return Math.sqrt(Math.pow(width, 2) + Math.pow(height, 2));
    }
}

// ================================================================
//  三角形（Triangle）クラス
// ================================================================
class Triangle extends AbstractShape {

    private double sideA;  // 辺a
    private double sideB;  // 辺b
    private double sideC;  // 辺c

    public Triangle(double sideA, double sideB, double sideC) {
        super("三角形（Triangle）");
        this.sideA = sideA;
        this.sideB = sideB;
        this.sideC = sideC;
    }

    /**
     * 三角形が成立するかチェックするメソッド
     * 三角不等式: どの2辺の和も残り1辺より大きい
     */
    public boolean isValid() {
        return (sideA + sideB > sideC) &&
               (sideB + sideC > sideA) &&
               (sideA + sideC > sideB);
    }

    // 面積: ヘロンの公式を使用
    // s = (a + b + c) / 2
    // 面積 = √(s × (s-a) × (s-b) × (s-c))
    @Override
    public double area() {
        double s = (sideA + sideB + sideC) / 2.0;
        return Math.sqrt(s * (s - sideA) * (s - sideB) * (s - sideC));
    }

    // 周囲 = a + b + c
    @Override
    public double perimeter() {
        return sideA + sideB + sideC;
    }

    @Override
    public String getInfo() {
        return String.format("辺a: %.2f, 辺b: %.2f, 辺c: %.2f",
                sideA, sideB, sideC);
    }
}

// ================================================================
//  正方形（Square）クラス: Rectangle を継承（継承の連鎖）
// ================================================================
class Square extends Rectangle {

    public Square(double side) {
        // 正方形は幅と高さが同じ長方形
        super(side, side);
        // 名前を上書き
        this.name = "正方形（Square）";
    }
}

// ================================================================
//  メインクラス: 図形計算ツールの実行
// ================================================================
public class ShapeCalculator {

    // 作成した図形を保存するリスト（ポリモーフィズム）
    // Shape型のリストに、Circle も Rectangle も Triangle も格納できる
    static ArrayList<AbstractShape> shapes = new ArrayList<>();

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("╔══════════════════════════════════════╗");
        System.out.println("║      図形計算ツール（OOP版）         ║");
        System.out.println("╚══════════════════════════════════════╝");
        System.out.println();

        boolean running = true;
        while (running) {
            displayMenu();
            System.out.print("選択してください (1-6): ");
            String choice = scanner.nextLine().trim();

            switch (choice) {
                case "1":
                    createCircle(scanner);
                    break;
                case "2":
                    createRectangle(scanner);
                    break;
                case "3":
                    createTriangle(scanner);
                    break;
                case "4":
                    createSquare(scanner);
                    break;
                case "5":
                    showAllShapes();
                    break;
                case "6":
                    running = false;
                    System.out.println("\nツールを終了します。");
                    break;
                default:
                    System.out.println("\n※ 1〜6の番号を入力してください。");
            }
        }

        scanner.close();
    }

    /**
     * メニューを表示するメソッド
     */
    static void displayMenu() {
        System.out.println("\n┌──────────── メニュー ────────────┐");
        System.out.println("│  1. 円を計算する                 │");
        System.out.println("│  2. 長方形を計算する             │");
        System.out.println("│  3. 三角形を計算する             │");
        System.out.println("│  4. 正方形を計算する             │");
        System.out.println("│  5. 全図形の一覧を表示           │");
        System.out.println("│  6. 終了                         │");
        System.out.println("└──────────────────────────────────┘");
    }

    /**
     * 円を作成するメソッド
     */
    static void createCircle(Scanner scanner) {
        System.out.println("\n--- 円の計算 ---");
        System.out.print("半径を入力してください: ");
        double radius = readPositiveDouble(scanner);
        if (radius <= 0) return;

        Circle circle = new Circle(radius);
        circle.display();
        shapes.add(circle);
        System.out.println("※ 図形リストに追加しました。");
    }

    /**
     * 長方形を作成するメソッド
     */
    static void createRectangle(Scanner scanner) {
        System.out.println("\n--- 長方形の計算 ---");
        System.out.print("幅を入力してください: ");
        double width = readPositiveDouble(scanner);
        if (width <= 0) return;

        System.out.print("高さを入力してください: ");
        double height = readPositiveDouble(scanner);
        if (height <= 0) return;

        Rectangle rect = new Rectangle(width, height);
        rect.display();

        // Rectangle独自のメソッドも使える
        System.out.printf("  対角線の長さ: %.2f%n", rect.diagonal());

        shapes.add(rect);
        System.out.println("※ 図形リストに追加しました。");
    }

    /**
     * 三角形を作成するメソッド
     */
    static void createTriangle(Scanner scanner) {
        System.out.println("\n--- 三角形の計算 ---");
        System.out.print("辺aの長さ: ");
        double a = readPositiveDouble(scanner);
        if (a <= 0) return;

        System.out.print("辺bの長さ: ");
        double b = readPositiveDouble(scanner);
        if (b <= 0) return;

        System.out.print("辺cの長さ: ");
        double c = readPositiveDouble(scanner);
        if (c <= 0) return;

        Triangle tri = new Triangle(a, b, c);

        // 三角形が成立するかチェック
        if (!tri.isValid()) {
            System.out.println("※ その3辺では三角形を作れません。");
            System.out.println("  （三角不等式: どの2辺の和も残り1辺より大きい必要があります）");
            return;
        }

        tri.display();
        shapes.add(tri);
        System.out.println("※ 図形リストに追加しました。");
    }

    /**
     * 正方形を作成するメソッド
     */
    static void createSquare(Scanner scanner) {
        System.out.println("\n--- 正方形の計算 ---");
        System.out.print("一辺の長さを入力してください: ");
        double side = readPositiveDouble(scanner);
        if (side <= 0) return;

        Square square = new Square(side);
        square.display();
        shapes.add(square);
        System.out.println("※ 図形リストに追加しました。");
    }

    /**
     * 全図形の一覧を表示するメソッド
     * ポリモーフィズムの実例: 同じ display() メソッドを呼ぶが、
     * 実際に実行されるのは各クラスの実装
     */
    static void showAllShapes() {
        System.out.println("\n=== 作成した図形の一覧 ===");

        if (shapes.isEmpty()) {
            System.out.println("まだ図形が作成されていません。");
            return;
        }

        double totalArea = 0;
        double totalPerimeter = 0;

        // ポリモーフィズム: AbstractShape型の変数で、
        // Circle, Rectangle, Triangle, Square のどれでも扱える
        for (int i = 0; i < shapes.size(); i++) {
            AbstractShape shape = shapes.get(i);
            System.out.printf("\n【図形 %d】%n", i + 1);
            shape.display();
            totalArea += shape.area();
            totalPerimeter += shape.perimeter();
        }

        // サマリー表示
        System.out.println("\n=== サマリー ===");
        System.out.printf("  図形の数    : %d 個%n", shapes.size());
        System.out.printf("  面積の合計  : %.2f%n", totalArea);
        System.out.printf("  周囲の合計  : %.2f%n", totalPerimeter);

        // 面積が最大の図形を見つける
        AbstractShape largest = shapes.get(0);
        for (AbstractShape shape : shapes) {
            if (shape.area() > largest.area()) {
                largest = shape;
            }
        }
        System.out.printf("  最大面積の図形: %s（面積: %.2f）%n",
                largest.getName(), largest.area());
    }

    /**
     * 正の小数を読み取るユーティリティメソッド
     * 例外処理（try-catch）で不正な入力に対応
     *
     * @param scanner 入力用Scanner
     * @return 読み取った正の数値。エラー時は -1
     */
    static double readPositiveDouble(Scanner scanner) {
        try {
            double value = Double.parseDouble(scanner.nextLine().trim());
            if (value <= 0) {
                System.out.println("※ 正の数を入力してください。");
                return -1;
            }
            return value;
        } catch (NumberFormatException e) {
            System.out.println("※ 数値を入力してください。");
            return -1;
        }
    }
}

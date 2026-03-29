/**
 * ============================================
 *   じゃんけんゲーム
 * ============================================
 *
 * 【学べる内容】
 *   - Random クラスによる乱数生成
 *   - Scanner クラスによるユーザー入力
 *   - while ループ・do-while ループ
 *   - 条件分岐（if-else, switch）
 *   - メソッドの定義と戻り値
 *   - 配列（array）の基本操作
 *   - 文字列比較（equals メソッド）
 *
 * 【実行方法】
 *   javac 03_じゃんけんゲーム.java
 *   java JankenGame
 */

import java.util.Random;
import java.util.Scanner;

public class JankenGame {

    // ========== 定数の定義 ==========
    // じゃんけんの手を表す定数（配列のインデックスとしても使用）
    static final int GU = 0;      // グー
    static final int CHOKI = 1;   // チョキ
    static final int PA = 2;      // パー

    // 手の名前を格納する配列
    static final String[] HAND_NAMES = {"グー ✊", "チョキ ✌", "パー ✋"};

    // アスキーアート（手の表示用）
    static final String[] HAND_ART = {
        "  ✊ グー  ",
        "  ✌ チョキ ",
        "  ✋ パー  "
    };

    // ========== 戦績を記録する変数 ==========
    static int wins = 0;      // 勝ち数
    static int losses = 0;    // 負け数
    static int draws = 0;     // 引き分け数

    // ========== メインメソッド ==========
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();

        // --- タイトル表示 ---
        System.out.println("╔══════════════════════════════════════╗");
        System.out.println("║     じゃんけんゲーム v1.0            ║");
        System.out.println("║     ～コンピュータと対決！～         ║");
        System.out.println("╚══════════════════════════════════════╝");
        System.out.println();

        // --- プレイヤー名の入力 ---
        System.out.print("あなたの名前を入力してください: ");
        String playerName = scanner.nextLine().trim();
        if (playerName.isEmpty()) {
            playerName = "プレイヤー";
        }

        System.out.printf("\n%s さん、じゃんけんで勝負しましょう！%n%n", playerName);

        // --- ゲームループ ---
        boolean playing = true;
        while (playing) {
            // 1回のじゃんけんを実行
            playOneRound(scanner, random, playerName);

            // 続けるかどうか確認
            System.out.print("\nもう一度遊びますか？ (はい/いいえ): ");
            String answer = scanner.nextLine().trim();

            // equalsIgnoreCase: 大文字・小文字を区別しない比較
            if (answer.equals("いいえ") || answer.equalsIgnoreCase("no")) {
                playing = false;
            }
            System.out.println();
        }

        // --- 最終結果を表示 ---
        displayFinalResult(playerName);

        scanner.close();
    }

    /**
     * じゃんけん1回分の処理を行うメソッド
     *
     * @param scanner    入力用Scanner
     * @param random     乱数生成用Randomオブジェクト
     * @param playerName プレイヤーの名前
     */
    static void playOneRound(Scanner scanner, Random random, String playerName) {
        // --- 手の選択メニューを表示 ---
        System.out.println("┌─────────────────────┐");
        System.out.println("│  手を選んでください  │");
        System.out.println("│  1. グー ✊          │");
        System.out.println("│  2. チョキ ✌        │");
        System.out.println("│  3. パー ✋          │");
        System.out.println("└─────────────────────┘");
        System.out.print("番号を入力 (1-3): ");

        // --- プレイヤーの手を取得 ---
        int playerHand;
        try {
            playerHand = Integer.parseInt(scanner.nextLine().trim()) - 1;
        } catch (NumberFormatException e) {
            System.out.println("※ 1〜3の数字を入力してください。");
            return;
        }

        // 入力値の範囲チェック
        if (playerHand < GU || playerHand > PA) {
            System.out.println("※ 1〜3の数字を入力してください。");
            return;
        }

        // --- コンピュータの手をランダムに決定 ---
        // random.nextInt(3) は 0, 1, 2 のいずれかを返す
        int computerHand = random.nextInt(3);

        // --- じゃんけんの演出 ---
        System.out.println();
        System.out.println("じゃん... けん... ポン！");
        System.out.println();

        // --- 手の表示 ---
        System.out.printf("  %s の手: %s%n", playerName, HAND_NAMES[playerHand]);
        System.out.printf("  コンピュータ: %s%n", HAND_NAMES[computerHand]);
        System.out.println();

        // --- 勝敗判定 ---
        int result = judge(playerHand, computerHand);

        // switch文で結果に応じたメッセージを表示
        switch (result) {
            case 1:
                System.out.println("  ★★★ あなたの勝ち！ ★★★");
                wins++;
                break;
            case -1:
                System.out.println("  ×× あなたの負け... ××");
                losses++;
                break;
            case 0:
                System.out.println("  △△ 引き分け △△");
                draws++;
                break;
        }

        // --- 現在の戦績を表示 ---
        displayCurrentStats();
    }

    /**
     * じゃんけんの勝敗を判定するメソッド
     *
     * @param player   プレイヤーの手（0:グー, 1:チョキ, 2:パー）
     * @param computer コンピュータの手
     * @return 1:プレイヤーの勝ち, -1:負け, 0:引き分け
     */
    static int judge(int player, int computer) {
        // 同じ手なら引き分け
        if (player == computer) {
            return 0;
        }

        // じゃんけんの勝ちパターン:
        //   グー(0)はチョキ(1)に勝つ
        //   チョキ(1)はパー(2)に勝つ
        //   パー(2)はグー(0)に勝つ
        // 数学的に: (player - computer + 3) % 3 == 1 なら勝ち
        if ((player - computer + 3) % 3 == 1) {
            return 1;  // 勝ち
        } else {
            return -1; // 負け
        }
    }

    /**
     * 現在の戦績を表示するメソッド
     */
    static void displayCurrentStats() {
        int total = wins + losses + draws;
        System.out.println();
        System.out.printf("  【戦績】%d戦 %d勝 %d敗 %d分%n",
                total, wins, losses, draws);

        // 勝率の計算（引き分けを除く）
        if (wins + losses > 0) {
            double winRate = (double) wins / (wins + losses) * 100;
            System.out.printf("  【勝率】%.1f%%%n", winRate);
        }
    }

    /**
     * 最終結果を表示するメソッド
     *
     * @param playerName プレイヤーの名前
     */
    static void displayFinalResult(String playerName) {
        int total = wins + losses + draws;

        System.out.println("╔══════════════════════════════════════╗");
        System.out.println("║          最終結果                    ║");
        System.out.println("╚══════════════════════════════════════╝");
        System.out.println();

        if (total == 0) {
            System.out.println("1回も遊びませんでした。また来てね！");
            return;
        }

        System.out.printf("  プレイヤー: %s%n", playerName);
        System.out.printf("  総対戦数  : %d 回%n", total);
        System.out.println();

        // --- 棒グラフで戦績を視覚化 ---
        System.out.println("  【戦績グラフ】");
        System.out.printf("  勝ち (%2d): %s%n", wins, "■".repeat(wins));
        System.out.printf("  負け (%2d): %s%n", losses, "□".repeat(losses));
        System.out.printf("  引分 (%2d): %s%n", draws, "△".repeat(draws));
        System.out.println();

        // --- 勝率の計算と表示 ---
        if (wins + losses > 0) {
            double winRate = (double) wins / (wins + losses) * 100;
            System.out.printf("  勝率: %.1f%%%n", winRate);
        }

        // --- 総合評価（if-elseの連鎖）---
        System.out.println();
        System.out.print("  総合評価: ");
        if (wins > losses * 2) {
            System.out.println("★★★ じゃんけんマスター！ ★★★");
        } else if (wins > losses) {
            System.out.println("★★ なかなかの腕前です！ ★★");
        } else if (wins == losses) {
            System.out.println("★ 互角の戦いでした！ ★");
        } else {
            System.out.println("次はきっと勝てます！頑張って！");
        }

        System.out.println();
        System.out.println("遊んでくれてありがとうございました！");
    }
}

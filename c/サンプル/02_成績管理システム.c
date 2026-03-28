/*
 * ============================================================
 *  成績管理システム
 * ============================================================
 *
 *  【学べる内容】
 *    - 配列の宣言と操作
 *    - for / while による繰り返し処理
 *    - if-else による条件分岐
 *    - 関数の定義と呼び出し
 *    - 平均・最大・最小の求め方
 *
 *  【実行方法】
 *    gcc -o output 02_成績管理システム.c && ./output
 *
 * ============================================================
 */

#include <stdio.h>
#include <string.h>

#define MAX_STUDENTS 50   /* 最大生徒数 */
#define MAX_NAME     32   /* 名前の最大文字数 */

/* --- 関数プロトタイプ --- */
double calc_average(const int scores[], int count);
int    find_max(const int scores[], int count);
int    find_min(const int scores[], int count);
char   get_grade(int score);
void   print_report(const char names[][MAX_NAME], const int scores[], int count);

/* ===== メイン関数 ===== */
int main(void)
{
    char names[MAX_STUDENTS][MAX_NAME];  /* 生徒の名前 */
    int  scores[MAX_STUDENTS];           /* 各生徒の点数 */
    int  count = 0;                      /* 登録人数 */
    int  choice;

    printf("==========================================\n");
    printf("        成績管理システム\n");
    printf("==========================================\n");

    /* --- メニューループ --- */
    while (1) {
        printf("\n--- メニュー ---\n");
        printf("  1. 生徒の成績を登録\n");
        printf("  2. 成績一覧を表示\n");
        printf("  3. 統計情報を表示\n");
        printf("  4. 終了\n");
        printf("選択してください (1-4): ");

        if (scanf("%d", &choice) != 1) {
            /* 数値以外が入力された場合 */
            while (getchar() != '\n');
            printf("※ 1〜4 の数字を入力してください。\n");
            continue;
        }
        while (getchar() != '\n');

        switch (choice) {
        /* ---------- 1. 成績登録 ---------- */
        case 1:
            if (count >= MAX_STUDENTS) {
                printf("※ これ以上登録できません（最大 %d 人）。\n", MAX_STUDENTS);
                break;
            }
            printf("名前を入力してください: ");
            scanf("%31[^\n]", names[count]);
            while (getchar() != '\n');

            printf("点数を入力してください (0-100): ");
            scanf("%d", &scores[count]);
            while (getchar() != '\n');

            if (scores[count] < 0 || scores[count] > 100) {
                printf("※ 点数は 0〜100 の範囲で入力してください。登録をキャンセルしました。\n");
                break;
            }

            printf(">> %s さん（%d 点）を登録しました。\n",
                   names[count], scores[count]);
            count++;
            break;

        /* ---------- 2. 一覧表示 ---------- */
        case 2:
            if (count == 0) {
                printf("※ まだ生徒が登録されていません。\n");
                break;
            }
            print_report(names, scores, count);
            break;

        /* ---------- 3. 統計情報 ---------- */
        case 3:
            if (count == 0) {
                printf("※ まだ生徒が登録されていません。\n");
                break;
            }
            {
                double avg = calc_average(scores, count);
                int    max = find_max(scores, count);
                int    min = find_min(scores, count);

                printf("\n========== 統計情報 ==========\n");
                printf("  登録人数 : %d 人\n", count);
                printf("  平均点   : %.1f 点\n", avg);
                printf("  最高点   : %d 点\n", max);
                printf("  最低点   : %d 点\n", min);

                /* 成績分布 */
                int grade_count[5] = {0}; /* A, B, C, D, F */
                for (int i = 0; i < count; i++) {
                    switch (get_grade(scores[i])) {
                    case 'A': grade_count[0]++; break;
                    case 'B': grade_count[1]++; break;
                    case 'C': grade_count[2]++; break;
                    case 'D': grade_count[3]++; break;
                    case 'F': grade_count[4]++; break;
                    }
                }
                printf("\n  --- 成績分布 ---\n");
                printf("  A (90-100) : %d 人\n", grade_count[0]);
                printf("  B (80-89)  : %d 人\n", grade_count[1]);
                printf("  C (70-79)  : %d 人\n", grade_count[2]);
                printf("  D (60-69)  : %d 人\n", grade_count[3]);
                printf("  F ( 0-59)  : %d 人\n", grade_count[4]);
                printf("==============================\n");
            }
            break;

        /* ---------- 4. 終了 ---------- */
        case 4:
            printf("成績管理システムを終了します。\n");
            return 0;

        default:
            printf("※ 1〜4 の数字を入力してください。\n");
            break;
        }
    }

    return 0;
}

/* ===== 平均点を計算する関数 ===== */
double calc_average(const int scores[], int count)
{
    int sum = 0;
    for (int i = 0; i < count; i++) {
        sum += scores[i];
    }
    return (double)sum / count;   /* int → double へキャスト */
}

/* ===== 最高点を求める関数 ===== */
int find_max(const int scores[], int count)
{
    int max = scores[0];
    for (int i = 1; i < count; i++) {
        if (scores[i] > max) {
            max = scores[i];
        }
    }
    return max;
}

/* ===== 最低点を求める関数 ===== */
int find_min(const int scores[], int count)
{
    int min = scores[0];
    for (int i = 1; i < count; i++) {
        if (scores[i] < min) {
            min = scores[i];
        }
    }
    return min;
}

/* ===== 点数から成績（A〜F）を返す関数 ===== */
char get_grade(int score)
{
    if (score >= 90) return 'A';
    if (score >= 80) return 'B';
    if (score >= 70) return 'C';
    if (score >= 60) return 'D';
    return 'F';
}

/* ===== 成績レポートを表示する関数 ===== */
void print_report(const char names[][MAX_NAME], const int scores[], int count)
{
    printf("\n+------+------------------+------+------+\n");
    printf("| No.  | 名前             | 点数 | 評価 |\n");
    printf("+------+------------------+------+------+\n");

    for (int i = 0; i < count; i++) {
        char grade = get_grade(scores[i]);
        printf("| %4d | %-16s | %4d |   %c  |\n",
               i + 1, names[i], scores[i], grade);
    }

    printf("+------+------------------+------+------+\n");
}

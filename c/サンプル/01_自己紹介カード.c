/*
 * ============================================================
 *  自己紹介カード生成プログラム
 * ============================================================
 *
 *  【学べる内容】
 *    - 変数とデータ型（int, float, double, char配列）
 *    - printf によるフォーマット出力
 *    - scanf による対話的入力
 *    - 算術演算（四則演算、型変換）
 *    - 文字列の基本的な扱い
 *
 *  【実行方法】
 *    gcc -o output 01_自己紹介カード.c && ./output
 *
 * ============================================================
 */

#include <stdio.h>
#include <string.h>

/* --- カードを罫線で囲んで表示する補助関数 --- */
void print_border(void)
{
    printf("+");
    for (int i = 0; i < 48; i++) {
        printf("-");
    }
    printf("+\n");
}

void print_line(const char *label, const char *value)
{
    /* ラベルと値を左寄せで表示（全体幅 46 文字） */
    printf("| %-44s |\n", "");  /* 空行代わりにスキップしてもよい */
    char buf[128];
    snprintf(buf, sizeof(buf), "%s: %s", label, value);
    printf("| %-46s |\n", buf);
}

void print_line_int(const char *label, int value)
{
    char buf[128];
    snprintf(buf, sizeof(buf), "%s: %d", label, value);
    printf("| %-46s |\n", buf);
}

void print_line_float(const char *label, double value)
{
    char buf[128];
    snprintf(buf, sizeof(buf), "%s: %.1f", label, value);
    printf("| %-46s |\n", buf);
}

int main(void)
{
    /* ===== 変数の宣言 ===== */
    char   name[64];          /* 名前（文字列） */
    int    age;               /* 年齢（整数） */
    double height_cm;         /* 身長（小数） */
    double weight_kg;         /* 体重（小数） */
    char   hobby[64];         /* 趣味（文字列） */
    char   goal[128];         /* 今年の目標（文字列） */

    int    current_year = 2026;  /* 現在の年 */

    /* ===== 対話的に情報を入力してもらう ===== */
    printf("====================================\n");
    printf("   自己紹介カード作成プログラム\n");
    printf("====================================\n\n");

    printf("名前を入力してください: ");
    scanf("%63[^\n]", name);          /* 空白を含む文字列を読み取る */
    while (getchar() != '\n');        /* 入力バッファをクリア */

    printf("年齢を入力してください: ");
    scanf("%d", &age);
    while (getchar() != '\n');

    printf("身長（cm）を入力してください: ");
    scanf("%lf", &height_cm);
    while (getchar() != '\n');

    printf("体重（kg）を入力してください: ");
    scanf("%lf", &weight_kg);
    while (getchar() != '\n');

    printf("趣味を入力してください: ");
    scanf("%63[^\n]", hobby);
    while (getchar() != '\n');

    printf("今年の目標を入力してください: ");
    scanf("%127[^\n]", goal);
    while (getchar() != '\n');

    /* ===== 計算（算術演算の例） ===== */
    int    birth_year   = current_year - age;              /* 生まれ年 */
    double height_m     = height_cm / 100.0;               /* 身長を m に変換 */
    double bmi          = weight_kg / (height_m * height_m); /* BMI 計算 */

    /* BMI による体型判定（条件分岐の例） */
    const char *bmi_category;
    if (bmi < 18.5) {
        bmi_category = "低体重";
    } else if (bmi < 25.0) {
        bmi_category = "普通体重";
    } else if (bmi < 30.0) {
        bmi_category = "肥満(1度)";
    } else {
        bmi_category = "肥満(2度以上)";
    }

    /* ===== カードを表示 ===== */
    printf("\n");
    print_border();

    /* タイトル行（中央寄せ風） */
    printf("|            ** 自己紹介カード **            |\n");

    print_border();

    print_line("名前", name);
    print_line_int("年齢", age);
    print_line_int("生まれ年（推定）", birth_year);

    /* 身長・体重 */
    char buf[128];
    snprintf(buf, sizeof(buf), "%.1f cm", height_cm);
    print_line("身長", buf);

    snprintf(buf, sizeof(buf), "%.1f kg", weight_kg);
    print_line("体重", buf);

    /* BMI */
    snprintf(buf, sizeof(buf), "%.1f (%s)", bmi, bmi_category);
    print_line("BMI", buf);

    print_line("趣味", hobby);
    print_line("今年の目標", goal);

    print_border();

    /* ===== おまけ：データ型のサイズを表示 ===== */
    printf("\n--- 使用したデータ型のサイズ（sizeof）---\n");
    printf("  char   : %zu バイト\n", sizeof(char));
    printf("  int    : %zu バイト\n", sizeof(int));
    printf("  float  : %zu バイト\n", sizeof(float));
    printf("  double : %zu バイト\n", sizeof(double));
    printf("  name[] : %zu バイト（char x 64）\n", sizeof(name));

    printf("\nプログラムを終了します。\n");
    return 0;
}

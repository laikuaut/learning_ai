/*
 * ============================================================
 *  ファイルで家計簿（household budget）
 * ============================================================
 *
 *  【学べる内容】
 *    - ファイル操作（fopen, fprintf, fscanf, fclose）
 *    - CSV形式の読み書き
 *    - 構造体（struct）の定義と配列
 *    - 文字列操作（strcpy, strcmp, fgets）
 *    - メニュー駆動型プログラムの設計
 *    - カテゴリ別集計ロジック
 *
 *  【実行方法】
 *    gcc -o kakeibo 05_ファイルで家計簿.c && ./kakeibo
 *
 *  【プログラムの概要】
 *    支出（日付・カテゴリ・金額・メモ）を登録し、一覧表示や
 *    カテゴリ別集計ができる家計簿プログラムです。
 *    データはCSVファイル（kakeibo.csv）に自動保存・読込されます。
 *
 * ============================================================
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/* ---- 定数定義 ---- */
#define MAX_EXPENSES   500    /* 最大登録件数 */
#define DATE_LEN       16     /* 日付の最大長（例：2026-03-28） */
#define CATEGORY_LEN   32     /* カテゴリの最大長 */
#define MEMO_LEN       64     /* メモの最大長 */
#define FILENAME       "kakeibo.csv"  /* 保存ファイル名 */

/* ---- 支出構造体 ---- */
typedef struct {
    char date[DATE_LEN];          /* 日付 */
    char category[CATEGORY_LEN];  /* カテゴリ */
    int  amount;                  /* 金額（円） */
    char memo[MEMO_LEN];          /* メモ */
} Expense;

/* ---- グローバル変数 ---- */
Expense expenses[MAX_EXPENSES];   /* 支出データ配列 */
int expense_count = 0;            /* 現在の登録件数 */

/* ---- 関数プロトタイプ ---- */
void show_menu(void);
void add_expense(void);
void list_expenses(void);
void summary_by_category(void);
int  save_to_file(void);
int  load_from_file(void);
void trim_newline(char *str);

/* ===========================================================
 *  メイン関数
 * =========================================================== */
int main(void)
{
    int choice;

    printf("=========================================\n");
    printf("   家計簿プログラム（CSV ファイル保存）\n");
    printf("=========================================\n\n");

    /* 起動時にファイルからデータを読み込む */
    load_from_file();

    do {
        show_menu();
        printf("選択 > ");
        if (scanf("%d", &choice) != 1) {
            /* 数値以外の入力をスキップ */
            while (getchar() != '\n')
                ;
            printf("\n※ 数字で入力してください。\n\n");
            continue;
        }
        /* 改行を消費 */
        while (getchar() != '\n')
            ;

        switch (choice) {
            case 1:
                add_expense();
                break;
            case 2:
                list_expenses();
                break;
            case 3:
                summary_by_category();
                break;
            case 4:
                save_to_file();
                printf("\nデータを保存しました。\n");
                break;
            case 0:
                save_to_file();
                printf("\nデータを保存しました。終了します。\n");
                break;
            default:
                printf("\n※ 0〜4 の番号を入力してください。\n\n");
                break;
        }
    } while (choice != 0);

    return 0;
}

/* ===========================================================
 *  メニュー表示
 * =========================================================== */
void show_menu(void)
{
    printf("\n----- メニュー -----\n");
    printf("  1. 支出を追加\n");
    printf("  2. 支出一覧を表示\n");
    printf("  3. カテゴリ別集計\n");
    printf("  4. データを保存\n");
    printf("  0. 保存して終了\n");
    printf("--------------------\n");
}

/* ===========================================================
 *  支出を追加する
 * =========================================================== */
void add_expense(void)
{
    Expense *e;

    if (expense_count >= MAX_EXPENSES) {
        printf("\n※ 登録上限（%d件）に達しています。\n", MAX_EXPENSES);
        return;
    }

    e = &expenses[expense_count];

    printf("\n--- 支出の追加 ---\n");

    printf("日付（例：2026-03-28）> ");
    fgets(e->date, DATE_LEN, stdin);
    trim_newline(e->date);

    printf("カテゴリ（食費/交通費/光熱費/娯楽/日用品/その他）> ");
    fgets(e->category, CATEGORY_LEN, stdin);
    trim_newline(e->category);

    printf("金額（円）> ");
    if (scanf("%d", &e->amount) != 1 || e->amount < 0) {
        printf("※ 正しい金額を入力してください。追加をキャンセルします。\n");
        while (getchar() != '\n')
            ;
        return;
    }
    while (getchar() != '\n')
        ;

    printf("メモ（任意・空欄可）> ");
    fgets(e->memo, MEMO_LEN, stdin);
    trim_newline(e->memo);

    expense_count++;
    printf("\n=> 支出を追加しました（現在 %d 件）。\n", expense_count);
}

/* ===========================================================
 *  支出一覧を表示する
 * =========================================================== */
void list_expenses(void)
{
    int i;
    int total = 0;

    if (expense_count == 0) {
        printf("\n※ まだ支出が登録されていません。\n");
        return;
    }

    printf("\n===== 支出一覧（%d件）=====\n", expense_count);
    printf("%-4s %-12s %-10s %10s  %s\n",
           "No.", "日付", "カテゴリ", "金額", "メモ");
    printf("------------------------------------------------------\n");

    for (i = 0; i < expense_count; i++) {
        printf("%-4d %-12s %-10s %10d円  %s\n",
               i + 1,
               expenses[i].date,
               expenses[i].category,
               expenses[i].amount,
               expenses[i].memo);
        total += expenses[i].amount;
    }

    printf("------------------------------------------------------\n");
    printf("合計: %d円\n", total);
}

/* ===========================================================
 *  カテゴリ別集計を表示する
 * =========================================================== */
void summary_by_category(void)
{
    /* カテゴリ名と合計金額・件数を保持する構造体 */
    typedef struct {
        char name[CATEGORY_LEN];
        int  total;
        int  count;
    } CategorySummary;

    CategorySummary cats[MAX_EXPENSES];
    int cat_count = 0;
    int i, j;
    int found;
    int grand_total = 0;

    if (expense_count == 0) {
        printf("\n※ まだ支出が登録されていません。\n");
        return;
    }

    /* カテゴリごとに集計 */
    for (i = 0; i < expense_count; i++) {
        found = 0;
        for (j = 0; j < cat_count; j++) {
            if (strcmp(cats[j].name, expenses[i].category) == 0) {
                cats[j].total += expenses[i].amount;
                cats[j].count++;
                found = 1;
                break;
            }
        }
        if (!found) {
            strcpy(cats[cat_count].name, expenses[i].category);
            cats[cat_count].total = expenses[i].amount;
            cats[cat_count].count = 1;
            cat_count++;
        }
        grand_total += expenses[i].amount;
    }

    /* 結果表示 */
    printf("\n===== カテゴリ別集計 =====\n");
    printf("%-12s %10s %6s %8s\n", "カテゴリ", "合計", "件数", "割合");
    printf("------------------------------------------\n");

    for (i = 0; i < cat_count; i++) {
        double ratio = 0.0;
        if (grand_total > 0) {
            ratio = (double)cats[i].total / grand_total * 100.0;
        }
        printf("%-12s %10d円 %4d件 %6.1f%%\n",
               cats[i].name,
               cats[i].total,
               cats[i].count,
               ratio);
    }

    printf("------------------------------------------\n");
    printf("総合計: %d円（%d件）\n", grand_total, expense_count);
}

/* ===========================================================
 *  CSVファイルにデータを保存する
 * =========================================================== */
int save_to_file(void)
{
    FILE *fp;
    int i;

    fp = fopen(FILENAME, "w");
    if (fp == NULL) {
        printf("※ ファイル '%s' を開けませんでした。\n", FILENAME);
        return -1;
    }

    /* ヘッダー行 */
    fprintf(fp, "日付,カテゴリ,金額,メモ\n");

    /* データ行 */
    for (i = 0; i < expense_count; i++) {
        fprintf(fp, "%s,%s,%d,%s\n",
                expenses[i].date,
                expenses[i].category,
                expenses[i].amount,
                expenses[i].memo);
    }

    fclose(fp);
    return 0;
}

/* ===========================================================
 *  CSVファイルからデータを読み込む
 * =========================================================== */
int load_from_file(void)
{
    FILE *fp;
    char line[256];
    int loaded = 0;

    fp = fopen(FILENAME, "r");
    if (fp == NULL) {
        /* ファイルが無い場合は新規扱い（エラーではない） */
        printf("※ 保存ファイルが見つかりません。新規で開始します。\n");
        return 0;
    }

    /* ヘッダー行を読み飛ばす */
    if (fgets(line, sizeof(line), fp) == NULL) {
        fclose(fp);
        return 0;
    }

    /* データ行を1行ずつ解析 */
    while (fgets(line, sizeof(line), fp) != NULL) {
        if (expense_count >= MAX_EXPENSES) {
            printf("※ 読み込み上限に達しました。\n");
            break;
        }

        trim_newline(line);

        /* 空行はスキップ */
        if (line[0] == '\0') {
            continue;
        }

        /* カンマ区切りで分割する */
        {
            char *token;
            char *rest = line;
            int field = 0;
            Expense *e = &expenses[expense_count];

            /* 各フィールドを初期化 */
            e->date[0] = '\0';
            e->category[0] = '\0';
            e->amount = 0;
            e->memo[0] = '\0';

            while ((token = strtok(rest, ",")) != NULL) {
                rest = NULL;  /* strtok の仕様：2回目以降は NULL を渡す */
                switch (field) {
                    case 0:
                        strncpy(e->date, token, DATE_LEN - 1);
                        e->date[DATE_LEN - 1] = '\0';
                        break;
                    case 1:
                        strncpy(e->category, token, CATEGORY_LEN - 1);
                        e->category[CATEGORY_LEN - 1] = '\0';
                        break;
                    case 2:
                        e->amount = atoi(token);
                        break;
                    case 3:
                        strncpy(e->memo, token, MEMO_LEN - 1);
                        e->memo[MEMO_LEN - 1] = '\0';
                        break;
                }
                field++;
            }

            /* 最低限、日付とカテゴリがあればデータとして採用 */
            if (e->date[0] != '\0' && e->category[0] != '\0') {
                expense_count++;
                loaded++;
            }
        }
    }

    fclose(fp);
    printf("=> %s から %d 件のデータを読み込みました。\n", FILENAME, loaded);
    return loaded;
}

/* ===========================================================
 *  文字列末尾の改行を除去する
 * =========================================================== */
void trim_newline(char *str)
{
    int len = (int)strlen(str);
    while (len > 0 && (str[len - 1] == '\n' || str[len - 1] == '\r')) {
        str[len - 1] = '\0';
        len--;
    }
}

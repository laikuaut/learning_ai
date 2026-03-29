/*
 * ============================================================
 *  ポインタで学ぶソートアルゴリズム
 * ============================================================
 *
 *  【学べる内容】
 *    - ポインタの基礎（アドレス、間接参照）
 *    - ポインタを使った配列操作
 *    - バブルソートの仕組み
 *    - 選択ソートの仕組み
 *    - ソートの過程をステップごとに可視化
 *
 *  【実行方法】
 *    gcc -o output 03_ポインタで学ぶソート.c && ./output
 *
 * ============================================================
 */

#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>

#define MAX_SIZE 20  /* 配列の最大要素数 */

/* --- 関数プロトタイプ --- */
void print_array(const int *arr, int size);
void print_array_highlight(const int *arr, int size, int idx1, int idx2);
void swap(int *a, int *b);
void bubble_sort(int *arr, int size, int show_steps);
void selection_sort(int *arr, int size, int show_steps);
void copy_array(const int *src, int *dst, int size);
void fill_random(int *arr, int size, int max_val);

int main(void)
{
    int original[MAX_SIZE];  /* 元データ（保存用） */
    int work[MAX_SIZE];      /* ソート用の作業配列 */
    int size = 0;
    int choice;

    srand((unsigned int)time(NULL));

    printf("============================================\n");
    printf("   ポインタで学ぶソートアルゴリズム\n");
    printf("============================================\n");

    /* --- ポインタの基礎を表示 --- */
    printf("\n--- ポインタの基礎 ---\n");
    int sample = 42;
    int *ptr = &sample;
    printf("  変数 sample の値   : %d\n", sample);
    printf("  変数 sample のアドレス: %p\n", (void *)&sample);
    printf("  ポインタ ptr の値   : %p （sample のアドレス）\n", (void *)ptr);
    printf("  *ptr（間接参照）    : %d （sample の値と同じ）\n", *ptr);

    printf("\n  ポインタを使って値を変更します...\n");
    *ptr = 100;
    printf("  *ptr = 100; を実行 → sample = %d\n", sample);
    printf("  → ポインタ経由で元の変数の値が変わりました！\n");

    /* --- データ入力 --- */
    printf("\n--- データ入力 ---\n");
    printf("要素数を入力してください (2-%d): ", MAX_SIZE);
    scanf("%d", &size);
    while (getchar() != '\n');

    if (size < 2 || size > MAX_SIZE) {
        printf("※ 範囲外のため、8 に設定します。\n");
        size = 8;
    }

    printf("データの入力方法を選んでください:\n");
    printf("  1. 手動入力\n");
    printf("  2. ランダム生成\n");
    printf("選択 (1-2): ");
    scanf("%d", &choice);
    while (getchar() != '\n');

    if (choice == 1) {
        printf("整数を %d 個入力してください（スペース区切り）: ", size);
        for (int i = 0; i < size; i++) {
            scanf("%d", &original[i]);
        }
        while (getchar() != '\n');
    } else {
        fill_random(original, size, 99);
        printf("ランダム生成されたデータ: ");
        print_array(original, size);
    }

    /* --- メニューループ --- */
    while (1) {
        printf("\n--- メニュー ---\n");
        printf("  1. バブルソート（ステップ表示あり）\n");
        printf("  2. 選択ソート（ステップ表示あり）\n");
        printf("  3. バブルソート（結果のみ）\n");
        printf("  4. 選択ソート（結果のみ）\n");
        printf("  5. 新しいデータをランダム生成\n");
        printf("  6. 終了\n");
        printf("選択 (1-6): ");

        if (scanf("%d", &choice) != 1) {
            while (getchar() != '\n');
            printf("※ 数字を入力してください。\n");
            continue;
        }
        while (getchar() != '\n');

        switch (choice) {
        case 1:
            printf("\n========== バブルソート（ステップ表示）==========\n");
            copy_array(original, work, size);
            printf("初期状態: ");
            print_array(work, size);
            bubble_sort(work, size, 1);
            printf("ソート結果: ");
            print_array(work, size);
            break;

        case 2:
            printf("\n========== 選択ソート（ステップ表示）==========\n");
            copy_array(original, work, size);
            printf("初期状態: ");
            print_array(work, size);
            selection_sort(work, size, 1);
            printf("ソート結果: ");
            print_array(work, size);
            break;

        case 3:
            copy_array(original, work, size);
            bubble_sort(work, size, 0);
            printf("バブルソート結果: ");
            print_array(work, size);
            break;

        case 4:
            copy_array(original, work, size);
            selection_sort(work, size, 0);
            printf("選択ソート結果: ");
            print_array(work, size);
            break;

        case 5:
            fill_random(original, size, 99);
            printf("新しいデータ: ");
            print_array(original, size);
            break;

        case 6:
            printf("プログラムを終了します。\n");
            return 0;

        default:
            printf("※ 1〜6 の数字を入力してください。\n");
            break;
        }
    }

    return 0;
}

/* ===== 配列を表示する関数 ===== */
void print_array(const int *arr, int size)
{
    printf("[");
    for (int i = 0; i < size; i++) {
        if (i > 0) printf(", ");
        printf("%d", *(arr + i));  /* ポインタ演算で要素にアクセス */
    }
    printf("]\n");
}

/* ===== 配列を表示（指定インデックスを強調）===== */
void print_array_highlight(const int *arr, int size, int idx1, int idx2)
{
    printf("  [");
    for (int i = 0; i < size; i++) {
        if (i > 0) printf(", ");
        if (i == idx1 || i == idx2) {
            printf("(%d)", *(arr + i));  /* カッコで囲んで強調 */
        } else {
            printf(" %d ", *(arr + i));
        }
    }
    printf("]\n");
}

/* ===== ポインタを使った値の交換 ===== */
void swap(int *a, int *b)
{
    /*
     * ポインタ a, b はそれぞれ交換したい変数のアドレスを受け取る。
     * *a, *b で間接参照して値を交換する。
     */
    int temp = *a;
    *a = *b;
    *b = temp;
}

/* ===== バブルソート（ポインタ版）===== */
void bubble_sort(int *arr, int size, int show_steps)
{
    int step = 0;
    int swapped;

    for (int i = 0; i < size - 1; i++) {
        swapped = 0;
        for (int j = 0; j < size - 1 - i; j++) {
            /* ポインタ演算で隣り合う要素を比較 */
            if (*(arr + j) > *(arr + j + 1)) {
                swap(arr + j, arr + j + 1);  /* ポインタを渡して交換 */
                swapped = 1;
                step++;

                if (show_steps) {
                    printf("  ステップ %d: [%d] と [%d] を交換 → ", step, j, j + 1);
                    print_array_highlight(arr, size, j, j + 1);
                }
            }
        }
        /* 交換が起きなければソート完了 */
        if (!swapped) break;
    }

    if (show_steps) {
        printf("  合計交換回数: %d 回\n", step);
    }
}

/* ===== 選択ソート（ポインタ版）===== */
void selection_sort(int *arr, int size, int show_steps)
{
    int step = 0;

    for (int i = 0; i < size - 1; i++) {
        /* 未ソート部分から最小値を探す */
        int min_idx = i;
        for (int j = i + 1; j < size; j++) {
            if (*(arr + j) < *(arr + min_idx)) {
                min_idx = j;
            }
        }

        /* 最小値が現在位置と異なれば交換 */
        if (min_idx != i) {
            swap(arr + i, arr + min_idx);
            step++;

            if (show_steps) {
                printf("  ステップ %d: 位置 %d の最小値 %d と位置 %d を交換 → ",
                       step, min_idx, *(arr + i), i);
                print_array_highlight(arr, size, i, min_idx);
            }
        }
    }

    if (show_steps) {
        printf("  合計交換回数: %d 回\n", step);
    }
}

/* ===== 配列のコピー ===== */
void copy_array(const int *src, int *dst, int size)
{
    for (int i = 0; i < size; i++) {
        *(dst + i) = *(src + i);  /* ポインタ演算でコピー */
    }
}

/* ===== ランダムデータ生成 ===== */
void fill_random(int *arr, int size, int max_val)
{
    for (int i = 0; i < size; i++) {
        *(arr + i) = rand() % (max_val + 1);
    }
}

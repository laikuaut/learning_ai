/*
 * ============================================================
 *  構造体で住所録（アドレス帳）
 * ============================================================
 *
 *  【学べる内容】
 *    - 構造体（struct）の定義と使い方
 *    - 構造体の配列
 *    - 文字列操作（strcpy, strcmp, strstr）
 *    - 関数への構造体の渡し方（ポインタ渡し）
 *    - メニュー駆動型プログラムの設計
 *
 *  【実行方法】
 *    gcc -o output 04_構造体で住所録.c && ./output
 *
 *  【プログラムの概要】
 *    連絡先（名前・電話番号・メールアドレス）を登録・一覧表示・
 *    検索・削除できるシンプルなアドレス帳プログラムです。
 *    構造体の配列を使ってデータを管理します。
 *
 * ============================================================
 */

#include <stdio.h>
#include <string.h>

#define MAX_CONTACTS 50   /* 最大登録件数 */
#define NAME_LEN     64   /* 名前の最大長 */
#define PHONE_LEN    20   /* 電話番号の最大長 */
#define EMAIL_LEN    64   /* メールアドレスの最大長 */

/* ===== 構造体の定義 ===== */
/*
 * 構造体（struct）は、複数の異なるデータ型をひとまとめにできる仕組みです。
 * ここでは「連絡先」を表す構造体を定義しています。
 */
typedef struct {
    char name[NAME_LEN];     /* 名前 */
    char phone[PHONE_LEN];   /* 電話番号 */
    char email[EMAIL_LEN];   /* メールアドレス */
} Contact;

/* --- 関数プロトタイプ --- */
void show_menu(void);
int  add_contact(Contact contacts[], int *count);
void list_contacts(const Contact contacts[], int count);
void search_contacts(const Contact contacts[], int count);
int  delete_contact(Contact contacts[], int *count);
void print_contact(const Contact *c, int index);
void print_separator(void);

/* ===== メイン関数 ===== */
int main(void)
{
    Contact contacts[MAX_CONTACTS];  /* 構造体の配列 */
    int count = 0;                   /* 登録件数 */
    int choice;

    printf("╔══════════════════════════════════════╗\n");
    printf("║       住所録（アドレス帳）           ║\n");
    printf("╚══════════════════════════════════════╝\n");

    /* --- メインループ --- */
    while (1) {
        show_menu();
        printf("選択してください (1-5): ");

        if (scanf("%d", &choice) != 1) {
            while (getchar() != '\n');
            printf("※ 1〜5 の数字を入力してください。\n");
            continue;
        }
        while (getchar() != '\n');  /* 入力バッファをクリア */

        switch (choice) {
        case 1:
            add_contact(contacts, &count);
            break;
        case 2:
            list_contacts(contacts, count);
            break;
        case 3:
            search_contacts(contacts, count);
            break;
        case 4:
            delete_contact(contacts, &count);
            break;
        case 5:
            printf("\n住所録を終了します。ご利用ありがとうございました。\n");
            return 0;
        default:
            printf("※ 1〜5 の数字を入力してください。\n");
            break;
        }
    }

    return 0;
}

/* ===== メニュー表示 ===== */
void show_menu(void)
{
    printf("\n--- メニュー ---\n");
    printf("  1. 連絡先を追加\n");
    printf("  2. 連絡先一覧を表示\n");
    printf("  3. 連絡先を検索\n");
    printf("  4. 連絡先を削除\n");
    printf("  5. 終了\n");
}

/* ===== 連絡先の追加 ===== */
int add_contact(Contact contacts[], int *count)
{
    if (*count >= MAX_CONTACTS) {
        printf("※ これ以上登録できません（最大 %d 件）。\n", MAX_CONTACTS);
        return 0;
    }

    Contact *new_contact = &contacts[*count];
    /*
     * ポインタを使って配列の要素にアクセスしています。
     * &contacts[*count] は contacts 配列の *count 番目の要素のアドレスです。
     */

    printf("\n--- 連絡先の追加 ---\n");

    printf("名前を入力してください: ");
    scanf("%63[^\n]", new_contact->name);
    while (getchar() != '\n');
    /*
     * 構造体のメンバには「.」演算子でアクセスします。
     * ポインタ経由の場合は「->」演算子を使います。
     * new_contact->name  は  (*new_contact).name  と同じ意味です。
     */

    printf("電話番号を入力してください: ");
    scanf("%19[^\n]", new_contact->phone);
    while (getchar() != '\n');

    printf("メールアドレスを入力してください: ");
    scanf("%63[^\n]", new_contact->email);
    while (getchar() != '\n');

    (*count)++;

    printf("\n>> 連絡先を登録しました！\n");
    print_contact(new_contact, *count);

    return 1;
}

/* ===== 連絡先一覧の表示 ===== */
void list_contacts(const Contact contacts[], int count)
{
    if (count == 0) {
        printf("\n※ 登録されている連絡先はありません。\n");
        return;
    }

    printf("\n========== 連絡先一覧（%d 件）==========\n", count);
    print_separator();

    for (int i = 0; i < count; i++) {
        print_contact(&contacts[i], i + 1);
    }

    print_separator();
}

/* ===== 連絡先の検索 ===== */
void search_contacts(const Contact contacts[], int count)
{
    if (count == 0) {
        printf("\n※ 登録されている連絡先はありません。\n");
        return;
    }

    char keyword[NAME_LEN];
    int found = 0;

    printf("\n--- 連絡先の検索 ---\n");
    printf("検索キーワードを入力してください: ");
    scanf("%63[^\n]", keyword);
    while (getchar() != '\n');

    printf("\n検索結果（キーワード: \"%s\"）:\n", keyword);
    print_separator();

    for (int i = 0; i < count; i++) {
        /*
         * strstr() は文字列の中に部分文字列が含まれるか検索します。
         * 見つかった場合はその位置のポインタ、見つからない場合は NULL を返します。
         */
        if (strstr(contacts[i].name, keyword) != NULL ||
            strstr(contacts[i].phone, keyword) != NULL ||
            strstr(contacts[i].email, keyword) != NULL) {
            print_contact(&contacts[i], i + 1);
            found++;
        }
    }

    if (found == 0) {
        printf("  該当する連絡先はありませんでした。\n");
    } else {
        printf("  %d 件見つかりました。\n", found);
    }
    print_separator();
}

/* ===== 連絡先の削除 ===== */
int delete_contact(Contact contacts[], int *count)
{
    if (*count == 0) {
        printf("\n※ 登録されている連絡先はありません。\n");
        return 0;
    }

    int num;

    /* まず一覧を表示 */
    list_contacts(contacts, *count);

    printf("削除する番号を入力してください (1-%d): ", *count);
    if (scanf("%d", &num) != 1) {
        while (getchar() != '\n');
        printf("※ 正しい番号を入力してください。\n");
        return 0;
    }
    while (getchar() != '\n');

    if (num < 1 || num > *count) {
        printf("※ 範囲外の番号です。\n");
        return 0;
    }

    int idx = num - 1;  /* 配列のインデックスに変換（0始まり） */

    printf("\n以下の連絡先を削除します:\n");
    print_contact(&contacts[idx], num);

    /*
     * 削除処理: 削除対象より後ろの要素を1つずつ前にずらす。
     * 配列では中間の要素を直接削除できないため、
     * このように「詰める」操作が必要です。
     */
    for (int i = idx; i < *count - 1; i++) {
        contacts[i] = contacts[i + 1];
        /*
         * 構造体は代入演算子（=）でまるごとコピーできます。
         * メンバを1つずつコピーする必要はありません。
         */
    }
    (*count)--;

    printf(">> 削除しました。現在の登録件数: %d 件\n", *count);
    return 1;
}

/* ===== 1件の連絡先を表示する関数 ===== */
void print_contact(const Contact *c, int index)
{
    printf("  [%d] 名前: %s\n", index, c->name);
    printf("      電話: %s\n", c->phone);
    printf("      メール: %s\n", c->email);
    printf("\n");
}

/* ===== 区切り線を表示する関数 ===== */
void print_separator(void)
{
    printf("------------------------------------------\n");
}

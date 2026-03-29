/**
 * ============================================================
 * アドレス帳アプリ（Address Book Application）
 * ============================================================
 *
 * 【学べる内容】
 *   - クラス（class）の定義とカプセル化
 *   - コンストラクタとメンバ関数
 *   - ファイル入出力（fstream）
 *   - std::vector によるデータ管理
 *   - 文字列操作（find, substr）
 *   - 例外処理の基本的な考え方
 *   - const メンバ関数、const 参照
 *
 * 【実行方法】
 *   g++ -std=c++17 04_アドレス帳アプリ.cpp -o address_book && ./address_book
 *
 * 【テーマ】
 *   連絡先情報を登録・検索・削除・ファイル保存できる
 *   アドレス帳アプリケーションです。
 *   クラス設計とファイルI/Oの実践的な使い方を学びます。
 * ============================================================
 */

#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <algorithm>
#include <iomanip>
#include <limits>
#include <sstream>

using namespace std;

// === 連絡先を表すクラス ===
class Contact {
private:
    string name_;      // 名前
    string phone_;     // 電話番号
    string email_;     // メールアドレス
    string address_;   // 住所
    string memo_;      // メモ

public:
    // デフォルトコンストラクタ
    Contact() = default;

    // パラメータ付きコンストラクタ
    Contact(const string& name, const string& phone,
            const string& email, const string& address,
            const string& memo)
        : name_(name), phone_(phone), email_(email),
          address_(address), memo_(memo) {}

    // ゲッター（const メンバ関数 = オブジェクトを変更しない）
    const string& getName()    const { return name_; }
    const string& getPhone()   const { return phone_; }
    const string& getEmail()   const { return email_; }
    const string& getAddress() const { return address_; }
    const string& getMemo()    const { return memo_; }

    // セッター
    void setPhone(const string& phone)     { phone_ = phone; }
    void setEmail(const string& email)     { email_ = email; }
    void setAddress(const string& address) { address_ = address; }
    void setMemo(const string& memo)       { memo_ = memo; }

    // 連絡先の詳細を表示するメンバ関数
    void display() const {
        cout << "+-------------------------------+" << endl;
        cout << "| Name:    " << setw(20) << left << name_    << "|" << endl;
        cout << "| Phone:   " << setw(20) << left << phone_   << "|" << endl;
        cout << "| Email:   " << setw(20) << left << email_   << "|" << endl;
        cout << "| Address: " << setw(20) << left << address_ << "|" << endl;
        cout << "| Memo:    " << setw(20) << left << memo_    << "|" << endl;
        cout << "+-------------------------------+" << endl;
    }

    // 1行の概要を表示
    void displaySummary(int index) const {
        cout << "  " << setw(3) << right << index << ". "
             << setw(15) << left << name_
             << " | " << setw(15) << left << phone_
             << " | " << email_ << endl;
    }

    // ファイル保存用の文字列に変換（タブ区切り）
    string serialize() const {
        return name_ + "\t" + phone_ + "\t" + email_ + "\t"
               + address_ + "\t" + memo_;
    }

    // タブ区切り文字列からオブジェクトを復元する静的メンバ関数
    static Contact deserialize(const string& line) {
        vector<string> fields;
        stringstream ss(line);
        string field;

        // タブ区切りで分割
        while (getline(ss, field, '\t')) {
            fields.push_back(field);
        }

        // フィールドが足りない場合は空文字で補完
        while (fields.size() < 5) {
            fields.push_back("");
        }

        return Contact(fields[0], fields[1], fields[2],
                       fields[3], fields[4]);
    }

    // キーワードが含まれるかチェック（検索用）
    bool matches(const string& keyword) const {
        // 全フィールドで部分一致検索
        return name_.find(keyword) != string::npos
            || phone_.find(keyword) != string::npos
            || email_.find(keyword) != string::npos
            || address_.find(keyword) != string::npos
            || memo_.find(keyword) != string::npos;
    }
};

// === アドレス帳全体を管理するクラス ===
class AddressBook {
private:
    vector<Contact> contacts_;  // 連絡先のリスト
    string filename_;           // 保存先ファイル名
    bool modified_;             // 未保存の変更があるか

public:
    // コンストラクタ（保存先ファイル名を指定）
    explicit AddressBook(const string& filename)
        : filename_(filename), modified_(false) {}

    // 連絡先の件数を返す
    size_t size() const { return contacts_.size(); }

    // 未保存の変更があるか
    bool isModified() const { return modified_; }

    // === 連絡先の追加 ===
    void addContact() {
        cout << endl;
        cout << "--- Add New Contact ---" << endl;

        string name, phone, email, address, memo;

        cout << "Name: ";
        getline(cin, name);

        if (name.empty()) {
            cout << "Name is required. Cancelled." << endl;
            return;
        }

        cout << "Phone: ";
        getline(cin, phone);

        cout << "Email: ";
        getline(cin, email);

        cout << "Address: ";
        getline(cin, address);

        cout << "Memo: ";
        getline(cin, memo);

        contacts_.emplace_back(name, phone, email, address, memo);
        modified_ = true;

        cout << "Added \"" << name << "\" successfully." << endl;
    }

    // === 全連絡先の一覧表示 ===
    void listAll() const {
        if (contacts_.empty()) {
            cout << "Address book is empty." << endl;
            return;
        }

        cout << endl;
        cout << "--- All Contacts (" << contacts_.size() << ") ---" << endl;
        cout << "  " << setw(3) << right << "#" << "  "
             << setw(15) << left << "Name"
             << " | " << setw(15) << left << "Phone"
             << " | " << "Email" << endl;
        cout << string(60, '-') << endl;

        for (size_t i = 0; i < contacts_.size(); i++) {
            contacts_[i].displaySummary(static_cast<int>(i + 1));
        }
    }

    // === 連絡先の詳細表示 ===
    void showDetail() const {
        if (contacts_.empty()) {
            cout << "Address book is empty." << endl;
            return;
        }

        listAll();
        cout << endl;
        cout << "Enter number to view detail (0 to cancel): ";
        int idx;
        cin >> idx;
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        if (idx < 1 || idx > static_cast<int>(contacts_.size())) {
            if (idx != 0) cout << "Invalid number." << endl;
            return;
        }

        cout << endl;
        contacts_[idx - 1].display();
    }

    // === 連絡先の検索 ===
    void searchContacts() const {
        cout << endl;
        cout << "Search keyword: ";
        string keyword;
        getline(cin, keyword);

        if (keyword.empty()) {
            cout << "Please enter a keyword." << endl;
            return;
        }

        // マッチした連絡先を収集
        vector<pair<int, const Contact*>> results;
        for (size_t i = 0; i < contacts_.size(); i++) {
            if (contacts_[i].matches(keyword)) {
                results.push_back({static_cast<int>(i + 1), &contacts_[i]});
            }
        }

        if (results.empty()) {
            cout << "No contacts found for \"" << keyword << "\"." << endl;
        } else {
            cout << "Found " << results.size() << " contact(s):" << endl;
            cout << string(60, '-') << endl;
            for (const auto& [idx, contact] : results) {
                contact->displaySummary(idx);
            }
        }
    }

    // === 連絡先の編集 ===
    void editContact() {
        if (contacts_.empty()) {
            cout << "Address book is empty." << endl;
            return;
        }

        listAll();
        cout << endl;
        cout << "Enter number to edit (0 to cancel): ";
        int idx;
        cin >> idx;
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        if (idx < 1 || idx > static_cast<int>(contacts_.size())) {
            if (idx != 0) cout << "Invalid number." << endl;
            return;
        }

        Contact& c = contacts_[idx - 1];
        cout << endl;
        c.display();
        cout << "(Press Enter to keep current value)" << endl;

        string input;

        cout << "Phone [" << c.getPhone() << "]: ";
        getline(cin, input);
        if (!input.empty()) c.setPhone(input);

        cout << "Email [" << c.getEmail() << "]: ";
        getline(cin, input);
        if (!input.empty()) c.setEmail(input);

        cout << "Address [" << c.getAddress() << "]: ";
        getline(cin, input);
        if (!input.empty()) c.setAddress(input);

        cout << "Memo [" << c.getMemo() << "]: ";
        getline(cin, input);
        if (!input.empty()) c.setMemo(input);

        modified_ = true;
        cout << "Updated successfully." << endl;
    }

    // === 連絡先の削除 ===
    void deleteContact() {
        if (contacts_.empty()) {
            cout << "Address book is empty." << endl;
            return;
        }

        listAll();
        cout << endl;
        cout << "Enter number to delete (0 to cancel): ";
        int idx;
        cin >> idx;
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        if (idx < 1 || idx > static_cast<int>(contacts_.size())) {
            if (idx != 0) cout << "Invalid number." << endl;
            return;
        }

        string name = contacts_[idx - 1].getName();

        // 確認プロンプト
        cout << "Delete \"" << name << "\"? (y/n): ";
        char confirm;
        cin >> confirm;
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        if (confirm == 'y' || confirm == 'Y') {
            contacts_.erase(contacts_.begin() + (idx - 1));
            modified_ = true;
            cout << "Deleted \"" << name << "\"." << endl;
        } else {
            cout << "Cancelled." << endl;
        }
    }

    // === ファイルに保存 ===
    void saveToFile() {
        ofstream ofs(filename_);
        if (!ofs) {
            cout << "Error: Could not open file for writing." << endl;
            return;
        }

        for (const auto& c : contacts_) {
            ofs << c.serialize() << "\n";
        }

        ofs.close();
        modified_ = false;
        cout << "Saved " << contacts_.size()
             << " contacts to \"" << filename_ << "\"." << endl;
    }

    // === ファイルから読み込み ===
    void loadFromFile() {
        ifstream ifs(filename_);
        if (!ifs) {
            cout << "No saved data found (\"" << filename_ << "\")." << endl;
            return;
        }

        contacts_.clear();
        string line;
        while (getline(ifs, line)) {
            if (!line.empty()) {
                contacts_.push_back(Contact::deserialize(line));
            }
        }

        ifs.close();
        modified_ = false;
        cout << "Loaded " << contacts_.size()
             << " contacts from \"" << filename_ << "\"." << endl;
    }

    // === 名前順にソート ===
    void sortByName() {
        sort(contacts_.begin(), contacts_.end(),
             [](const Contact& a, const Contact& b) {
                 return a.getName() < b.getName();
             });
        modified_ = true;
        cout << "Sorted by name." << endl;
    }
};

// === メインメニューの表示 ===
void showMenu() {
    cout << endl;
    cout << "==============================" << endl;
    cout << "     Address Book App" << endl;
    cout << "==============================" << endl;
    cout << "  1. Add contact" << endl;
    cout << "  2. List all contacts" << endl;
    cout << "  3. View detail" << endl;
    cout << "  4. Search" << endl;
    cout << "  5. Edit contact" << endl;
    cout << "  6. Delete contact" << endl;
    cout << "  7. Sort by name" << endl;
    cout << "  8. Save to file" << endl;
    cout << "  9. Load from file" << endl;
    cout << "  0. Exit" << endl;
    cout << "------------------------------" << endl;
    cout << "Choice: ";
}

int main() {
    // アドレス帳オブジェクトの作成（保存先ファイル名を指定）
    AddressBook book("address_book.txt");

    cout << "=== Address Book App ===" << endl;
    cout << "Load existing data? (y/n): ";
    char loadChoice;
    cin >> loadChoice;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    if (loadChoice == 'y' || loadChoice == 'Y') {
        book.loadFromFile();
    }

    // メインループ
    while (true) {
        showMenu();

        int choice;
        cin >> choice;
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        switch (choice) {
            case 1: book.addContact();      break;
            case 2: book.listAll();          break;
            case 3: book.showDetail();       break;
            case 4: book.searchContacts();   break;
            case 5: book.editContact();      break;
            case 6: book.deleteContact();    break;
            case 7: book.sortByName();       break;
            case 8: book.saveToFile();       break;
            case 9: book.loadFromFile();     break;
            case 0: {
                // 未保存の変更がある場合は確認
                if (book.isModified()) {
                    cout << "Unsaved changes exist. Save before exit? (y/n): ";
                    char save;
                    cin >> save;
                    if (save == 'y' || save == 'Y') {
                        book.saveToFile();
                    }
                }
                cout << "Goodbye!" << endl;
                return 0;
            }
            default:
                cout << "Invalid choice." << endl;
        }
    }

    return 0;
}

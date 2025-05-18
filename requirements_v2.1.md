
# 📚 図書貸出CLIシステム 要件定義（ver.2.0）

---

## 🧭 1. システム目的

- CLIで図書の貸出・返却・検索・管理を行うシステムを構築する。
- ユーザーのロールに応じた機能制御（RBAC）を行う。
- 将来的にCSV → DB、CLI → Web化を想定し、柔軟な設計を採用。

---

## 👥 2. ユーザー種別（ロール）

| ロール | 概要 |
|--------|------|
| admin | システム管理者。常に1名。全機能使用可能。 |
| librarian | 図書館員。貸出・返却・登録・検索などが可能。 |
| user | 一般利用者。自身の情報や貸出状況の確認が可能。 |
| guest | ログイン不要。書籍検索のみ可。 |

---

## 🔐 3. 権限とロール管理

- 管理者は図書館員に権限譲渡可（降格される）。常に1名。
- 降格された管理者は特定期間内に復帰可（緊急時）。
- 一般ユーザー ⇄ 図書館員：昇格・降格可。
- 管理者 → 一般ユーザー：不可。

---

## 🛠️ 4. 起動・初期化（system_boot.py）

- users.csv が存在しない場合、初期化モードへ。
- 初期管理者：`USR00001` / `admin12345`。
- `--reset-admin` により管理者パスワードをリセット可（他データは保持）。
- 提供機能：
  - ログイン（login.py）
  - 書籍検索（未定義）

---

## 🔐 5. ログイン処理（login.py）

- 初回時、初期IDとパスワードを表示。
- ログイン成功後、パスワード変更（change_pass.py）を促す。
- 認証情報は auth.py 経由で main_menu.py に渡す。

---

## 📋 6. メインメニュー（main_menu.py）

| Fキー | 機能 | モジュール | 備考 |
|-------|------|------------|------|
| F1 | 貸出 | borrow.py | 利用者ID → 書籍ID。Uキーでユーザー検索可 |
| F2 | 返却 | return_book.py | 書籍IDを複数入力 |
| F3 | 書籍検索 | search.py | 書籍を条件検索 |
| F4 | ユーザー検索 | user_search.py | 管理者・図書館員用全機能 |
| F8 | システム情報 | 未実装 | 書籍数、利用者数等 |
| F12 | ログアウト | logout.py | メニューへ戻る |

---

## 👤 7. ユーザー管理機能（user_search.py）

### 登録情報：
- id, name, DOB, phone, zipcode, address
- status（内部用・非表示）
- remarks（備考、内部用・非表示）

### 利用停止：
- active: bool（Falseで停止）
- suspend_until: date | null（n日後に自動復帰）

### 操作（admin/librarian）：
- ユーザー登録・検索・詳細閲覧・編集・削除
- ロール昇格／降格
- 利用停止／再開（期限付き／無期限）

### 呼び出し元が貸出時：
- 利用者検索＋ID返却のみ可能

---

## 📕 8. 書籍情報（books.csv）

- id: `BK000001`
- isbn, title, author, publisher, published_date
- ndc, location
- registered_date, updated_date
- remarks（備考）

---

## 📁 書籍ステータス（正規化）

- book_status.csv で book_id + status_code を管理
- status_definitions.json でコードを定義
- 空欄は "A01: 貸出可" とみなす

---

## 🔢 ID管理方針

- ID形式：`USR00001` / `BK000001`
- チェックデジット：使用しない（バーコード作成時のみ内部使用）

---

## 🔒 パスワード管理

- 暗号化（SHA-256など）
- 初期パスワードは admin12345
- 初回ログイン時に変更を促す

---

## 📁 構成例（軽量 MVC）
## ✅ ディレクトリ構成（最小MVC風 + CLI主体）

```
library_system/
├── system_boot.py         # 起動スクリプト（main相当）
├── config.py              # パス・初期値などの設定
│
├── controller/            # 処理の本体（CLIでもWebでも共通化しやすい）
│   ├── login.py
│   ├── main_menu.py
│   ├── borrow.py
│   ├── return_book.py
│   ├── search.py
│   └── user_manage.py     # 登録・検索・編集など
│
├── model/                 # データ構造＆簡単なロジック保持
│   ├── user_model.py
│   ├── book_model.py
│   └── borrow_model.py
│
├── db/                    # CSVの読み書き、ID生成など
│   ├── csv_accessor.py
│   ├── id_manager.py
│   └── status_lookup.py
│
├── view/                  # CLI表示・入力処理（あくまで分離意識程度）
│   ├── login_view.py
│   ├── menu_view.py
│   └── user_view.py
│
├── data/                  # データファイル群
│   ├── users.csv
│   ├── books.csv
│   ├── borrowed.csv
│   ├── book_status.csv
│   ├── id_counter.json
│   └── status_definitions.json
│
└── temp/                  # 一時ファイルなど（必要な場合のみ）
    └── selected_user.txt
```

## ✅ 設計方針のポイント

| 項目 | 内容 |
|------|------|
| シンプルさ | 個人開発向け、管理しやすく軽量 |
| 拡張性 | 将来的なWeb化や機能追加に耐えられる構造 |
| 分離意識 | View（入出力）とロジック、データ定義の明確な分離 |
| テスト | テスト不要方針により、`tests/` ディレクトリは不要 |

## ✅ 今後の開発優先ステップ（例）

1. `config.py`：初期設定・パス類の一元管理
2. `system_boot.py`：初期化チェックとメニュー表示
3. `controller/user_manage.py`：検索・登録・削除から実装開始


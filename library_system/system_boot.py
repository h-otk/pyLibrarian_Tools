
# users.csv が存在しない場合、初期化モードへ。
# 初期管理者：USR00001 / admin12345。
# --reset-admin により管理者パスワードをリセット可（他データは保持）。
# 提供機能：

# ログイン（login.py）
# 書籍検索（未定義）

from library_system.config import USER_CSV_PATH
import os

if not os.path.exists(USER_CSV_PATH):
    # ユーザー管理CSVがなければ作成
    with open(USER_CSV_PATH, "w", encoding="utf-8") as f:
        f.write("id,name,DOB,phone,zipcode,address,status,remarks\n")

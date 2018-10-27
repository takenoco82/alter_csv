# alter_csv

## 使い方
``` sh
# 項目を追加する
python alter_csv.py add "path/to/users.csv" new_col_name

# 項目を追加する: デフォルト値を指定
python alter_csv.py add "path/to/users.csv" new_col_name --default 1

# 項目を追加する: 追加する位置を指定
python alter_csv.py add "path/to/users.csv" new_col_name --first
python alter_csv.py add "path/to/users.csv" new_col_name --after col_name

# 項目を削除する
python alter_csv.py drop "path/to/users.csv" col_name

# 項目名を変更する
python alter_csv.py change "path/to/users.csv" old_col_name new_col_name

# findで検索したファイルに対して項目を追加する
find . -name "*users.csv" | xargs -I {} python alter_csv.py add {} new_col_name
```

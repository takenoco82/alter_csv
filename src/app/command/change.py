from argparse import Namespace

from pandas.core.frame import DataFrame

from app.command.sub_command import SubCommand
from app.error.column_already_exists_error import ColumnAlreadyExistsError
from app.error.column_not_found_error import ColumnNotFoundError


class Change(SubCommand):
    def __init__(self, args: Namespace) -> None:
        super().__init__(args)
        self.old_column = args.old_column
        self.new_column = args.new_column

    def process(self, df: DataFrame) -> DataFrame:
        headers = list(df.columns.values)

        # 入力チェック
        if self.old_column not in headers:
            message = "column `{}` is not found".format(self.old_column)
            raise ColumnNotFoundError(message)
        if self.old_column == self.new_column:
            # 同じ名前の場合は変更せずにそのまま返却する
            return df
        if self.new_column in headers:
            message = "column `{}` already exist".format(self.new_column)
            raise ColumnAlreadyExistsError(message)

        # 項目の追加
        df[self.new_column] = df[self.old_column]

        # 出力する項目
        new_headers = headers[:]
        i = headers.index(self.old_column)
        new_headers[i] = self.new_column

        return df[new_headers]

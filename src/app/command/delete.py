from argparse import Namespace

from pandas.core.frame import DataFrame

from app.command.sub_command import SubCommand
from app.error.column_not_found_error import ColumnNotFoundError


class Delete(SubCommand):
    def __init__(self, args: Namespace) -> None:
        super().__init__(args)
        self.column = args.column

    def process(self, df: DataFrame) -> DataFrame:
        headers = list(df.columns.values)

        # 入力チェック
        if self.column not in headers:
            message = "column `{}` is not found".format(self.column)
            raise ColumnNotFoundError(message)

        # 出力する項目
        new_headers = headers[:]
        i = headers.index(self.column)
        new_headers.pop(i)

        return df[new_headers]

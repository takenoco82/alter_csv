from argparse import Namespace

import pandas
from pandas.core.frame import DataFrame

from app.command.sub_command import SubCommand
from app.error.column_not_found_error import ColumnNotFoundError


class Delete(SubCommand):
    def __init__(self, args: Namespace) -> None:
        self.file = args.file
        self.delimiter = self.get_delimiter(args.file)
        self.column = args.column

    def execute(self):
        before = pandas.read_csv(self.file, sep=self.delimiter, dtype=str)
        after = self.process(before)
        after.to_csv(self.file, sep=self.delimiter, index=False)

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

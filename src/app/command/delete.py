from argparse import Namespace

import pandas

from app.command.sub_command import SubCommand
from app.error.column_not_found_error import ColumnNotFoundError


class Delete(SubCommand):
    def __init__(self, args: Namespace) -> None:
        self.file = args.file
        self.delimiter = self.get_delimiter(args.file)
        self.column = args.column

    def execute(self):
        df = pandas.read_csv(self.file, sep=self.delimiter, dtype=str)

        # 入力チェック
        headers = list(df.columns.values)
        if self.column not in headers:
            message = "column `{}` is not found".format(self.column)
            raise ColumnNotFoundError(message)

        # 出力する項目
        new_headers = headers[:]
        i = headers.index(self.column)
        new_headers.pop(i)

        df[new_headers].to_csv(self.file, sep=self.delimiter, index=False)

from argparse import Namespace

import pandas

from app.command.sub_command import SubCommand
from app.error.column_already_exists_error import ColumnAlreadyExistsError
from app.error.column_not_found_error import ColumnNotFoundError


class Add(SubCommand):
    def __init__(self, args: Namespace) -> None:
        self.file = args.file
        self.delimiter = self.get_delimiter(args.file)
        self.column = args.column
        self.default = args.default
        self.first = args.first
        self.after = args.after

    def execute(self):
        df = pandas.read_csv(self.file, sep=self.delimiter, dtype=str)

        # 入力チェック
        headers = list(df.columns.values)
        if self.column in headers:
            message = "column `{}` already exist".format(self.column)
            raise ColumnAlreadyExistsError(message)
        if self.after and self.after not in headers:
            message = "column `{}` is not found".format(self.after)
            raise ColumnNotFoundError(message)

        # 項目の追加
        df[self.column] = self.default

        # 出力する項目
        new_headers = headers[:]
        if self.first:
            new_headers.insert(0, self.column)
        elif self.after:
            i = headers.index(self.after)
            new_headers.insert(i + 1, self.column)
        else:
            new_headers.append(self.column)

        df[new_headers].to_csv(self.file, sep=self.delimiter, index=False)

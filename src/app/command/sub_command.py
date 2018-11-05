import os
import re
from argparse import Namespace

import pandas
from pandas.core.frame import DataFrame

from app.error.unsupported_file_error import UnsupportedFileError


class SubCommand(object):
    def __init__(self, args: Namespace) -> None:
        self.file = args.file
        self.delimiter = self.get_delimiter(args.file)

    def execute(self):
        before = self.read()
        after = self.process(before)
        self.write(after)

    def read(self) -> DataFrame:
        return pandas.read_csv(self.file, sep=self.delimiter, dtype=str)

    def write(self, df: DataFrame):
        df.to_csv(self.file, sep=self.delimiter, index=False)

    def process(self, df: DataFrame) -> DataFrame:
        raise NotImplementedError

    @classmethod
    def get_delimiter(cls, filepath: str) -> str:
        extention = os.path.splitext(filepath)[1]
        if re.match("\\.csv", extention, re.IGNORECASE):
            return ","
        elif re.match("\\.tsv", extention, re.IGNORECASE):
            return "\t"
        raise UnsupportedFileError("extention `{}` is unsupported".format(extention))

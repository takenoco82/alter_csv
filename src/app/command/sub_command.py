import os
import re

from app.error.unsupported_file_error import UnsupportedFileError


class SubCommand(object):
    def execute(self):
        raise NotImplementedError

    @classmethod
    def get_delimiter(cls, filepath: str) -> str:
        extention = os.path.splitext(filepath)[1]
        if re.match("\\.csv", extention, re.IGNORECASE):
            return ","
        elif re.match("\\.tsv", extention, re.IGNORECASE):
            return "\t"
        raise UnsupportedFileError("extention `{}` is unsupported".format(extention))

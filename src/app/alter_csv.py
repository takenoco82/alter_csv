import argparse
import os
import re
import sys
from argparse import Namespace
from logging import DEBUG, basicConfig, getLogger

import pandas

# ログ出力設定
formatter = "%(asctime)s [%(levelname)-5s] %(message)s"
basicConfig(level=DEBUG, format=formatter)
logger = getLogger(__name__)


class UnsupportedFileError(Exception):
    pass


class ColumnNotFoundError(Exception):
    pass


class ColumnAlreadyExistsError(Exception):
    pass


def _delimiter(filepath: str) -> str:
    extention = os.path.splitext(filepath)[1]
    if re.match("\\.csv", extention, re.IGNORECASE):
        return ","
    elif re.match("\\.tsv", extention, re.IGNORECASE):
        return "\t"
    raise UnsupportedFileError("extention `{}` is unsupported".format(extention))


def command_add(args: Namespace):
    filepath = args.file
    delimiter = _delimiter(filepath)
    df = pandas.read_csv(filepath, sep=delimiter, dtype=str)

    new_column = args.column
    after = args.after

    # 入力チェック
    headers = list(df.columns.values)
    if new_column in headers:
        message = "column `{}` already exist".format(new_column)
        raise ColumnAlreadyExistsError(message)
    if after and after not in headers:
        message = "column `{}` is not found".format(after)
        raise ColumnNotFoundError(message)

    # 項目の追加
    df[new_column] = args.default

    # 出力する項目
    new_headers = headers[:]
    if args.first:
        new_headers.insert(0, new_column)
    elif after:
        i = headers.index(after)
        new_headers.insert(i + 1, new_column)
    else:
        new_headers.append(new_column)

    df[new_headers].to_csv(args.file, sep=delimiter, index=False)


def command_delete(args: Namespace):
    filepath = args.file
    delimiter = _delimiter(filepath)
    df = pandas.read_csv(filepath, sep=delimiter, dtype=str)

    target_column = args.column

    # 入力チェック
    headers = list(df.columns.values)
    if target_column not in headers:
        message = "column `{}` is not found".format(target_column)
        raise ColumnNotFoundError(message)

    # 出力する項目
    new_headers = headers[:]
    i = headers.index(target_column)
    new_headers.pop(i)

    df[new_headers].to_csv(args.file, sep=delimiter, index=False)


def command_change(args: Namespace):
    filepath = args.file
    delimiter = _delimiter(filepath)
    df = pandas.read_csv(filepath, sep=delimiter, dtype=str)

    old_column = args.old_column
    new_column = args.new_column

    # 入力チェック
    headers = list(df.columns.values)
    if old_column not in headers:
        message = "column `{}` is not found".format(old_column)
        raise ColumnNotFoundError(message)
    if new_column in headers:
        message = "column `{}` already exist".format(new_column)
        raise ColumnAlreadyExistsError(message)

    # 項目の追加
    df[new_column] = df[old_column]

    # 出力する項目
    new_headers = headers[:]
    i = headers.index(old_column)
    new_headers[i] = new_column

    df[new_headers].to_csv(args.file, sep=delimiter, index=False)


def parse_args(args) -> Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name', help="sub-commnad help")

    # addコマンド
    parser_add = subparsers.add_parser("add", help="see `add -h`")
    parser_add.add_argument("file", type=str, help="target file path")
    parser_add.add_argument("column", type=str, help="new column name")
    parser_add.add_argument("--default", type=str, help="default value of new column", default=None)
    group = parser_add.add_mutually_exclusive_group()
    group.add_argument("--first", action="store_true")
    group.add_argument("--after", type=str)
    parser_add.set_defaults(handler=command_add)

    # deleteコマンド
    parser_delete = subparsers.add_parser("delete", help="see `delete -h`")
    parser_delete.add_argument("file", type=str, help="target file path")
    parser_delete.add_argument("column", type=str, help="column you want to delete")
    parser_delete.set_defaults(handler=command_delete)

    # changeコマンド
    parser_change = subparsers.add_parser("change", help="see `change -h`")
    parser_change.add_argument("file", type=str, help="target file path")
    parser_change.add_argument("old_column", type=str, help="old column name")
    parser_change.add_argument("new_column", type=str, help="new column name")
    parser_change.set_defaults(handler=command_change)

    # 未定義のサブコマンドが引数に指定されていた場合、ここでSystemExit例外がraiseされる
    return parser.parse_args(args)


def main():
    logger.info("start")
    try:
        args = parse_args(sys.argv[1:])
        # ここまできたら handlerがないことはありえない
        args.handler(args)
    except (UnsupportedFileError, FileNotFoundError, ColumnNotFoundError, ColumnAlreadyExistsError) as e:
        logger.error(e)
        sys.exit(1)

    logger.info("end")
    sys.exit(0)


if __name__ == '__main__':
    main()

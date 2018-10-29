import argparse
import sys
from argparse import Namespace
from logging import DEBUG, basicConfig, getLogger

from app.command.add import Add
from app.command.delete import Delete
from app.command.change import Change

from app.error.column_already_exists_error import ColumnAlreadyExistsError
from app.error.column_not_found_error import ColumnNotFoundError
from app.error.unsupported_file_error import UnsupportedFileError


# ログ出力設定
formatter = "%(asctime)s [%(levelname)-5s] %(message)s"
basicConfig(level=DEBUG, format=formatter)
logger = getLogger(__name__)


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
    parser_add.set_defaults(handler=Add)

    # deleteコマンド
    parser_delete = subparsers.add_parser("delete", help="see `delete -h`")
    parser_delete.add_argument("file", type=str, help="target file path")
    parser_delete.add_argument("column", type=str, help="column you want to delete")
    parser_delete.set_defaults(handler=Delete)

    # changeコマンド
    parser_change = subparsers.add_parser("change", help="see `change -h`")
    parser_change.add_argument("file", type=str, help="target file path")
    parser_change.add_argument("old_column", type=str, help="old column name")
    parser_change.add_argument("new_column", type=str, help="new column name")
    parser_change.set_defaults(handler=Change)

    # 未定義のサブコマンドが引数に指定されていた場合、ここでSystemExit例外がraiseされる
    return parser.parse_args(args)


def main():
    logger.info("start")
    try:
        args = parse_args(sys.argv[1:])
        logger.debug("args={}".format(args))
        # ここまできたら handlerがないことはありえない
        subcommand = args.handler(args)
        subcommand.execute()
    except (UnsupportedFileError, FileNotFoundError, ColumnNotFoundError, ColumnAlreadyExistsError) as e:
        logger.error(e)
        sys.exit(1)

    logger.info("end")
    sys.exit(0)


if __name__ == '__main__':
    main()

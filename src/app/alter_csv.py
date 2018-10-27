import argparse
import sys
from argparse import Namespace


def command_add(args: Namespace):
    # TODO 未実装
    print("add {}".format(args))


def command_delete(args: Namespace):
    # TODO 未実装
    print("delete {}".format(args))


def command_change(args: Namespace):
    # TODO 未実装
    print("change {}".format(args))


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
    args = parse_args(sys.argv[1:])
    # ここまできたら handlerがないことはありえない
    args.handler(args)


if __name__ == '__main__':
    main()

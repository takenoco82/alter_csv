import unittest

from parameterized import param, parameterized

from app import alter_csv
from app.command.add import Add
from app.command.change import Change
from app.command.delete import Delete


class TestAlterCsv(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @parameterized.expand([
        # add 必須パラメータのみ
        param(
            "add",
            input=("add", "filepath", "new_col_name"),
            expected={
                "file": "filepath",
                "column": "new_col_name",
                "default": None,
                "first": False,
                "after": None,
                "handler": Add
            }
        ),
        # add defaultあり
        param(
            "add default",
            input=("add", "filepath", "new_col_name", "--default", "1"),
            expected={
                "file": "filepath",
                "column": "new_col_name",
                "default": "1",
                "first": False,
                "after": None,
            }
        ),
        # add firstあり
        param(
            "add first",
            input=("add", "filepath", "new_col_name", "--first"),
            expected={
                "file": "filepath",
                "column": "new_col_name",
                "default": None,
                "first": True,
                "after": None,
            }
        ),
        # add afterあり
        param(
            "add after",
            input=("add", "filepath", "new_col_name", "--after", "username"),
            expected={
                "file": "filepath",
                "column": "new_col_name",
                "default": None,
                "first": False,
                "after": "username",
            }
        ),
        # add default, afterあり
        param(
            "add default after",
            input=("add", "filepath", "new_col_name", "--default", "1", "--after", "username"),
            expected={
                "file": "filepath",
                "column": "new_col_name",
                "default": "1",
                "first": False,
                "after": "username",
            }
        ),
        # delete 必須パラメータのみ
        param(
            "delete",
            input=("delete", "filepath", "col_name"),
            expected={
                "file": "filepath",
                "column": "col_name",
                "handler": Delete
            }
        ),
        # change 必須パラメータのみ
        param(
            "change",
            input=("change", "filepath", "old_col_name", "new_col_name"),
            expected={
                "file": "filepath",
                "old_column": "old_col_name",
                "new_column": "new_col_name",
                "handler": Change
            }
        ),
    ])
    def test_parse_args_normal(self, _, input, expected):
        args = alter_csv.parse_args(input)
        # 項目の値を確認
        for attr, expected_value in expected.items():
            self.assertEqual(getattr(args, attr), expected_value)

    @parameterized.expand([
        # 不明なサブコマンド
        param(
            "unknown subcommand",
            input=("commit")
        ),
        # add 必須パラメータなし file
        param(
            "add required file",
            input=("add")
        ),
        # add 必須パラメータなし column
        param(
            "add required column",
            input=("add", "filepath")
        ),
        # add 不明な引数
        param(
            "add unknown arg",
            input=("add", "filepath", "new_col_name", "--last")
        ),
        # add default値なし
        param(
            "add default no value",
            input=("add", "filepath", "new_col_name", "--default"),
        ),
        # add after値なし
        param(
            "add after no value",
            input=("add", "filepath", "new_col_name", "--after"),
        ),
        # add first, afterあり
        param(
            "add both first after",
            input=("add", "filepath", "new_col_name", "--first", "--after", "username"),
        ),
        # delete 必須パラメータなし file
        param(
            "delete required file",
            input=("delete")
        ),
        # delete 必須パラメータなし column
        param(
            "delete required column",
            input=("delete", "filepath")
        ),
        # delete 不明な引数
        param(
            "delete unknown arg",
            input=("delete", "filepath", "col_name", "--first")
        ),
        # change 必須パラメータなし file
        param(
            "change required file",
            input=("change")
        ),
        # change 必須パラメータなし old_column
        param(
            "change required old_column",
            input=("change", "filepath")
        ),
        # change 必須パラメータなし new_column
        param(
            "change required new_column",
            input=("change", "filepath", "old_col_name")
        ),
        # change 不明な引数
        param(
            "change unknown arg",
            input=("change", "filepath", "old_col_name", "new_col_name", "--first")
        ),
    ])
    def test_parse_args_exception(self, _, input):
        # SystemExit例外がraiseされることを確認
        with self.assertRaises(SystemExit):
            alter_csv.parse_args(input)


if __name__ == '__main__':
    unittest.main()

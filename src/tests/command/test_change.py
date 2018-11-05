import unittest

from parameterized import param, parameterized

from argparse import Namespace
from pandas.core.frame import DataFrame

from app.command.change import Change
from app.error.column_already_exists_error import ColumnAlreadyExistsError
from app.error.column_not_found_error import ColumnNotFoundError


class TestChange(unittest.TestCase):
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
        # 正常系
        param(
            "username",
            input={
                "file": "src/tests/data/test_commnad.csv",
                "old_column": "username",
                "new_column": "user_name",
            },
            expected=DataFrame({
                'user_id': ['1', '2', '3'],
                'user_name': ['username1', 'username2', 'username3']})
        ),
        # 同じ名前に変更 user_id → user_id
        param(
            "same name",
            input={
                "file": "src/tests/data/test_commnad.csv",
                "old_column": "user_id",
                "new_column": "user_id",
            },
            expected=DataFrame({
                'user_id': ['1', '2', '3'],
                'username': ['username1', 'username2', 'username3']})
        ),
    ])
    def test_procee_normal(self, _, input, expected):
        sub_command = Change(Namespace(**input))
        df = sub_command.read()
        actual = sub_command.process(df)
        self.assertTrue(actual.equals(expected), "actual={}".format(actual))

    @parameterized.expand([
        # 存在しない項目を変更しようとした
        param(
            "column_not_found",
            input={
                "file": "src/tests/data/test_commnad.csv",
                "old_column": "old_col",  # NG
                "new_column": "new_col",
            },
            expected=ColumnNotFoundError
        ),
        # 既に存在する項目名に変更しようとした
        param(
            "column_already_exist",
            input={
                "file": "src/tests/data/test_commnad.csv",
                "old_column": "username",
                "new_column": "user_id",  # NG
            },
            expected=ColumnAlreadyExistsError
        ),
    ])
    def test_procee_exception(self, _, input, expected):
        sub_command = Change(Namespace(**input))
        df = sub_command.read()
        with self.assertRaises(expected):
            sub_command.process(df)


if __name__ == '__main__':
    unittest.main()

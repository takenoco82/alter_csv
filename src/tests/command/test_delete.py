import unittest

from parameterized import param, parameterized

from argparse import Namespace
from pandas.core.frame import DataFrame

from app.command.delete import Delete
from app.error.column_not_found_error import ColumnNotFoundError


class TestDelete(unittest.TestCase):
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
                "column": "username",
            },
            expected=DataFrame({
                'user_id': ['1', '2', '3']})
        ),
    ])
    def test_procee_normal(self, _, input, expected):
        sub_command = Delete(Namespace(**input))
        df = sub_command.read()
        actual = sub_command.process(df)
        self.assertTrue(actual.equals(expected), "actual={}".format(actual))

    @parameterized.expand([
        # 存在しない項目を削除しようとした
        param(
            "column_not_found",
            input={
                "file": "src/tests/data/test_commnad.csv",
                "column": "hoge",  # NG
            },
            expected=ColumnNotFoundError
        ),
    ])
    def test_procee_exception(self, _, input, expected):
        sub_command = Delete(Namespace(**input))
        df = sub_command.read()
        with self.assertRaises(expected):
            sub_command.process(df)


if __name__ == '__main__':
    unittest.main()

import unittest
from argparse import Namespace

from pandas.core.frame import DataFrame
from parameterized import param, parameterized

from app.command.sub_command import SubCommand
from app.error.unsupported_file_error import UnsupportedFileError


class TestSubCommand(unittest.TestCase):
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

    # ファイル名に対応するデリミタ
    @parameterized.expand([
        param(
            "csv",
            input="src/tests/data/users.csv",
            expected=","
        ),
        param(
            "CSV",
            input="src/tests/data/users.CSV",
            expected=","
        ),
        param(
            "tsv",
            input="src/tests/data/users.tsv",
            expected="\t"
        ),
        param(
            "TSV",
            input="src/tests/data/users.TSV",
            expected="\t"
        ),
    ])
    def test_get_delimiter_normal(self, _, input, expected):
        actual = SubCommand.get_delimiter(input)
        self.assertEqual(actual, expected)

    # 拡張子が csv, tsv 以外の場合 UnsupportedFileError が raise される
    def test_get_delimiter_exception(self):
        input = "src/tests/data/users.txt"
        with self.assertRaises(UnsupportedFileError):
            SubCommand.get_delimiter(input)

    @parameterized.expand([
        # csv
        param(
            "csv",
            input={
                "file": "src/tests/data/test_read.csv",
            },
            expected=DataFrame({
                'user_id': ['1', '2'],
                'username': ['username1', None],
                'phone': ['012345678901', None],
                'height': ['170.5', None],
                'address': ['住所', None],
                'note': ['delimiter,あり', None]})
        ),
        # tsv
        param(
            "tsv",
            input={
                "file": "src/tests/data/test_read.tsv",
            },
            expected=DataFrame({
                'user_id': ['1', '2'],
                'username': ['username1', None],
                'phone': ['012345678901', None],
                'height': ['170.5', None],
                'address': ['住所', None],
                'note': ['delimiter	あり', None]})
        ),
    ])
    def test_read(self, _, input, expected):
        sub_command = SubCommand(Namespace(**input))
        actual = sub_command.read()
        self.assertTrue(actual.equals(expected), "actual={}".format(actual))

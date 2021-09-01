import unittest

from modules.util import delete_unused_char_for_dir_name


class TestUtil(unittest.TestCase):
    def test_delete_unused_char_for_dir_name(self):
        """Windowsディレクトリ名に使えない文字を削除する関数のテスト"""
        origin_str = "💎グランブルーファンタジー/GRANBLUE FANTASY：1章完結💎"
        actual = delete_unused_char_for_dir_name(origin_str)
        expected = "💎グランブルーファンタジー_GRANBLUE FANTASY_1章完結💎"
        self.assertEqual(actual, expected)

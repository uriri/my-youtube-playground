import tempfile
import unittest
from pathlib import Path

from modules.util import delete_unused_char_for_dir_name, download_thumbnails


class TestUtil(unittest.TestCase):
    def test_delete_unused_char_for_dir_name(self):
        """Windowsディレクトリ名に使えない文字を削除する関数のテスト"""
        origin_str = "💎グランブルーファンタジー/GRANBLUE FANTASY：1章完結💎"
        actual = delete_unused_char_for_dir_name(origin_str)
        expected = "💎グランブルーファンタジー_GRANBLUE FANTASY_1章完結💎"
        self.assertEqual(actual, expected)

    def test_download_thumbnails(self):
        download_list = {
            "title": "💎グランブルーファンタジー/GRANBLUE FANTASY：1章完結💎",
            "videos": [
                {
                    "title": "【#１】初めての！！！グランブルーファンタジー！！！【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/iwjlQI4rkKA/sddefault.jpg",
                },
                {
                    "title": "【#２】はじめてのぐらぶるっ！初めてのガチャピン！！【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/v4ePgw3qMZo/sddefault.jpg",
                },
                {
                    "title": "【#３】なんか新ガチャが来るらしいぞ！！！！！：GRANBLUE FANTASY【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/zHFC_ZKUITM/sddefault.jpg",
                },
                {
                    "title": "【#４】ガチャピンとムックに会いたいグランブルーファンタジースバル：GRANBLUE FANTASY【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/OLd5osYw8_g/sddefault.jpg",
                },
                {
                    "title": "【#５】明かされる最推しの過去？！：GRANBLUE FANTASY【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/G3oe0xYs9DQ/sddefault.jpg",
                },
                {
                    "title": "【#６】霧の島ガロンゾ？いくちゅば！！：GRANBLUE FANTASY【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/ujtn9sZdcWQ/sddefault.jpg",
                },
                {
                    "title": "【#７】明かされるラカムの過去！？：GRANBLUE FANTASY【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/2AaCaCoRMB0/sddefault.jpg",
                },
                {
                    "title": "【#８】黒騎士逮捕ってマジ？：GRANBLUE FANTASY【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/qUB3ps86mOE/sddefault.jpg",
                },
                {
                    "title": "【#９】頼む…服を着ててくれ…ラビ島編！：GRANBLUE FANTASY【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/pGdfRRUGbzI/sddefault.jpg",
                },
                {
                    "title": "【#生スバル】グリームニルガチャ：GRANBLUE FANTASY【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/L9TxWjDrZoM/sddefault.jpg",
                },
                {
                    "title": "【♯10】オルキスちゃんを救いたい：GRANBLUE FANTASY【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/F6n6x-8ZBBU/sddefault.jpg",
                },
                {
                    "title": "【♯12】お覚悟！！！フリーシア&マリス！！！！：GRANBLUE FANTASY【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/zrIDw5iR2x0/sddefault.jpg",
                },
                {
                    "title": "【♯13】グラブル100連ガチャ！：GRANBLUE FANTASY【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/3m9OsJ3n3gQ/sddefault.jpg",
                },
                {
                    "title": "【♯14】とりまトッポブで！スバル！！！！：GRANBLUE FANTASY【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/UhlKk6lxUOw/sddefault.jpg",
                },
                {
                    "title": "【♯15】リーシャと共に！！おひさし本編：GRANBLUE FANTASY【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/dNM_iJCGRDQ/sddefault.jpg",
                },
                {
                    "title": "【#16】1章終盤！第三勢力登場？！なんだおめえら！！！！/gran blue fantasy【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/9Z81DQCERtU/sddefault.jpg",
                },
                {
                    "title": "【#17】グラブル第一章！完結！！！！！：granblue fantasy story【ホロライブ/大空スバル】",
                    "thumbnail_url": "https://i.ytimg.com/vi/8J30L8myCKc/sddefault.jpg",
                },
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_dir = Path(temp_dir)
            print(tmp_dir, tmp_dir.is_dir())
            download_thumbnails(base_path=tmp_dir, download_list=download_list)
            expected_dir = tmp_dir / "💎グランブルーファンタジー_GRANBLUE FANTASY_1章完結💎"
            self.assertTrue(expected_dir.exists())  # プレイリスト名のディレクトリがあるか

            expected_files = [
                "【#１】初めての！！！グランブルーファンタジー！！！【ホロライブ_大空スバル】.jpg",
                "【#２】はじめてのぐらぶるっ！初めてのガチャピン！！【ホロライブ_大空スバル】.jpg",
                "【#３】なんか新ガチャが来るらしいぞ！！！！！_GRANBLUE FANTASY【ホロライブ_大空スバル】.jpg",
                "【#４】ガチャピンとムックに会いたいグランブルーファンタジースバル_GRANBLUE FANTASY【ホロライブ_大空スバル】.jpg",
                "【#５】明かされる最推しの過去？！_GRANBLUE FANTASY【ホロライブ_大空スバル】.jpg",
                "【#６】霧の島ガロンゾ？いくちゅば！！_GRANBLUE FANTASY【ホロライブ_大空スバル】.jpg",
                "【#７】明かされるラカムの過去！？_GRANBLUE FANTASY【ホロライブ_大空スバル】.jpg",
                "【#８】黒騎士逮捕ってマジ？_GRANBLUE FANTASY【ホロライブ_大空スバル】.jpg",
                "【#９】頼む…服を着ててくれ…ラビ島編！_GRANBLUE FANTASY【ホロライブ_大空スバル】.jpg",
                "【#生スバル】グリームニルガチャ_GRANBLUE FANTASY【ホロライブ_大空スバル】.jpg",
                "【♯10】オルキスちゃんを救いたい_GRANBLUE FANTASY【ホロライブ_大空スバル】.jpg",
                "【♯12】お覚悟！！！フリーシア&マリス！！！！_GRANBLUE FANTASY【ホロライブ_大空スバル】.jpg",
                "【♯13】グラブル100連ガチャ！_GRANBLUE FANTASY【ホロライブ_大空スバル】.jpg",
                "【♯14】とりまトッポブで！スバル！！！！_GRANBLUE FANTASY【ホロライブ_大空スバル】.jpg",
                "【♯15】リーシャと共に！！おひさし本編_GRANBLUE FANTASY【ホロライブ_大空スバル】.jpg",
                "【#16】1章終盤！第三勢力登場？！なんだおめえら！！！！_gran blue fantasy【ホロライブ_大空スバル】.jpg",
                "【#17】グラブル第一章！完結！！！！！_granblue fantasy story【ホロライブ_大空スバル】.jpg",
            ]
            for expected_file in expected_files:
                with self.subTest(f"{expected_file} is not exist"):
                    expected = expected_dir / expected_file
                    self.assertTrue(expected.exists())

import unittest

from modules.youtube_api import YoutubeAPIUtil, YouTubeAPIRepository


class YouTubeAPIRepositoryMock(YouTubeAPIRepository):
    def _get_resource(self, resource):
        if resource["mode"] == "get_channel_id":
            return {
                "items": [
                    {
                        "snippet": {
                            "title": resource["channel_name"],
                            "channelId": "abcdefg1234567",
                        },
                    }
                ]
            }


class TestYoutubeAPI(unittest.TestCase):
    def setUp(self):
        self.youtube_api_util = YoutubeAPIUtil(api_repo=YouTubeAPIRepositoryMock())

    def test_mock_func(self):
        resource = {"mode": "get_channel_id", "channel_name": "Mock Channel"}
        api_factory = YouTubeAPIRepositoryMock()
        actual = api_factory._get_resource(resource=resource)
        expected = {
            "items": [
                {
                    "snippet": {
                        "title": "Mock Channel",
                        "channelId": "abcdefg1234567",
                    },
                }
            ]
        }
        self.assertEqual(actual, expected)

    def test_get_channel_id(self):
        """チャンネルIDを取得するテスト"""
        channel_name = "Mock Channel"
        actual = self.youtube_api_util.get_channel_id_from_channel_name(channel_name)
        expected = "abcdefg1234567"
        self.assertEqual(actual, expected)

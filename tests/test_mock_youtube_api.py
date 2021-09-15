import unittest
from unittest.mock import patch

from modules.youtube_api import YoutubeAPIUtil


def _get_resource_from_mock(cls, resource):
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


@patch.object(YoutubeAPIUtil, "_get_resource_from_api", new=_get_resource_from_mock)
class TestYoutubeAPI(unittest.TestCase):
    def test_mock_func(self):
        youtube_api_util = YoutubeAPIUtil(api_key="")
        resource = {"mode": "get_channel_id", "channel_name": "Mock Channel"}
        actual = youtube_api_util._get_resource_from_api(resource=resource)
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
        youtube_api_util = YoutubeAPIUtil(api_key="")
        actual = youtube_api_util.get_channel_id_from_channel_name(channel_name)
        expected = "abcdefg1234567"
        self.assertEqual(actual, expected)

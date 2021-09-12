import unittest
from unittest.mock import MagicMock, Mock, patch

from modules.youtube_api import Playlist, YoutubeAPIUtil


def _get_resource_from_mock(cls, resource):
    return {
        "items": [
            {
                "snippet": {
                    "title": "Subaru Ch. 大空スバル",
                    "channelId": "UCvzGlP9oQwU--Y0r9id_jnA",
                },
            }
        ]
    }


class TestYoutubeAPI(unittest.TestCase):
    def test_func(self):
        with patch.object(
            YoutubeAPIUtil, "_get_resource_from_api", new=_get_resource_from_mock
        ):
            youtube_api_util = YoutubeAPIUtil(api_key="")
            actual = youtube_api_util._get_resource_from_api(resource={})
            expected = {
                "items": [
                    {
                        "snippet": {
                            "title": "Subaru Ch. 大空スバル",
                            "channelId": "UCvzGlP9oQwU--Y0r9id_jnA",
                        },
                    }
                ]
            }
            self.assertEqual(actual, expected)

    def test_get_channel_id(self):
        """チャンネルIDを取得するテスト"""
        with patch.object(
            YoutubeAPIUtil, "_get_resource_from_api", new=_get_resource_from_mock
        ):
            channel_name = "Subaru Ch. 大空スバル"
            youtube_api_util = YoutubeAPIUtil(api_key="")
            actual = youtube_api_util.get_channel_id_from_channel_name(channel_name)
            expected = "UCvzGlP9oQwU--Y0r9id_jnA"
            self.assertEqual(actual, expected)

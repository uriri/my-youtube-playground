import unittest

from modules.models import Playlist, Thumbnail, ThumbnailList
from modules.youtube_api.repository import YouTubeAPIRepository
from modules.youtube_api.util import YoutubeAPIUtil


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
        elif resource["mode"] == "get_playlists_on_channel":
            if resource["next_token"] == "":
                return {
                    "nextPageToken": "ABC",
                    "items": [
                        {
                            "id": f"id{x}",
                            "snippet": {
                                "title": f"playlist{x}",
                                "channelId": resource["channel_id"],
                            },
                        }
                        for x in range(1, 4)
                    ],
                }
            elif resource["next_token"] == "ABC":
                return {
                    "items": [
                        {
                            "id": "id4",
                            "snippet": {
                                "title": "playlist4",
                                "channelId": resource["channel_id"],
                            },
                        }
                    ]
                }
        elif resource["mode"] == "generate_thumbnail_list":
            if resource["next_token"] == "":
                return {
                    "nextPageToken": "ABC",
                    "items": [
                        {
                            "snippet": {
                                "title": f"title{x}",
                                "thumbnails": {"default": {"url": f"url{x}"}},
                            },
                        }
                        for x in range(1, 4)
                    ],
                }
            elif resource["next_token"] == "ABC":
                return {
                    "items": [
                        {
                            "snippet": {
                                "title": "title4",
                                "thumbnails": {"default": {"url": "url4"}},
                            },
                        }
                    ],
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
        """???????????????ID????????????????????????"""
        channel_name = "Mock Channel"
        actual = self.youtube_api_util.get_channel_id_from_channel_name(channel_name)
        expected = "abcdefg1234567"
        self.assertEqual(actual, expected)

    def test_get_playlists_on_channel(self):
        """??????????????????????????????????????????????????????????????????"""
        channel_id = "abcdefg1234567"
        actual = sorted(
            list(self.youtube_api_util.get_playlists_on_channel(channel_id)),
            key=lambda x: x.id_,
        )
        expected = sorted(
            [
                Playlist(title="playlist1", id_="id1"),
                Playlist(title="playlist2", id_="id2"),
                Playlist(title="playlist3", id_="id3"),
                Playlist(title="playlist4", id_="id4"),
            ],
            key=lambda x: x.id_,
        )
        self.assertEqual(actual, expected)

    def test_generate_thumbnail_list(self):
        """?????????????????????????????????????????????URL?????????????????????????????????"""
        playlist = Playlist(title="playlist1", id_="id1")
        actual = self.youtube_api_util.generate_thumbnail_list(playlist=playlist)
        expected = ThumbnailList(
            title="playlist1",
            videos=[
                Thumbnail(title="title1", thumbnail_url="url1"),
                Thumbnail(title="title2", thumbnail_url="url2"),
                Thumbnail(title="title3", thumbnail_url="url3"),
                Thumbnail(title="title4", thumbnail_url="url4"),
            ],
        )
        self.assertEqual(actual, expected)

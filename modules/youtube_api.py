from typing import Iterator, Tuple

from apiclient.discovery import build


class YoutubeAPIUtil:
    def __init__(self, api_key):
        self.youtube_api_key = api_key

    def get_channel_id_from_channel_name(self, channel_name: str) -> str:
        """チャンネル名からチャンネルIDを取得する

        Args:
            channel_name (str): チャンネル名（正式名称）

        Returns:
            str: チャンネルID
        """
        with build("youtube", "v3", developerKey=self.youtube_api_key) as youbute:
            search_response = (
                youbute.search()
                .list(part="snippet", q=channel_name, type="channel", maxResults=2)
                .execute()
            )
            for item in search_response["items"]:
                title = item["snippet"]["title"]
                if title == channel_name:
                    id_ = item["snippet"]["channelId"]
                    return id_

    def get_playlists_on_channel(self, channel_id: str) -> Iterator[Tuple[str, str]]:
        """チャンネルに存在するプレイリスト（再生回数上位5つ）を取得

        Args:
            channel_id (str): チャンネルID

        Yields:
            Iterator[Tuple[str, str]]: (プレイリストタイトル, プレイリストID)
        """

        with build("youtube", "v3", developerKey=self.youtube_api_key) as youbute:
            search_response = (
                youbute.search()
                .list(
                    part="snippet",
                    channelId=channel_id,
                    type="playlist",
                    order="videoCount",
                )
                .execute()
            )

            for item in search_response["items"]:
                title = item["snippet"]["title"]
                id_ = item["id"]["playlistId"]
                yield (title, id_)

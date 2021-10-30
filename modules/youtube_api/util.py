from typing import Iterator, List, Tuple

from modules.models import Playlist, Thumbnail, ThumbnailList

from .repository import YouTubeAPIRepository


class YoutubeAPIUtil:
    def __init__(self, api_repo: YouTubeAPIRepository):
        self.api_repo = api_repo

    def get_channel_id_from_channel_name(self, channel_name: str) -> str:
        """チャンネル名からチャンネルIDを取得する

        Args:
            channel_name (str): チャンネル名（正式名称）

        Returns:
            str: チャンネルID
        """
        resource = {"mode": "get_channel_id", "channel_name": channel_name}
        search_response = self.api_repo._get_resource(resource)
        for item in search_response["items"]:
            title = item["snippet"]["title"]
            if title == channel_name:
                id_ = item["snippet"]["channelId"]
                return id_

    def _fetch_playlists_on_channel(
        self, channel_id: str, next_token: str = ""
    ) -> Tuple[str, List[Playlist]]:
        """チャネル内のプレイリスト取得

        Args:
            channel_id (str): チャネルID
            next_token (str): YouTubeAPI 次ページ取得トークン

        Returns:
            Tuple[str, List[Playlist]]: 次ページ取得トークン, プレイリスト[タイトル, ID]
        """
        resource = {
            "mode": "get_playlists_on_channel",
            "channel_id": channel_id,
            "next_token": next_token,
        }
        search_response = self.api_repo._get_resource(resource)

        next_token = search_response.get("nextPageToken")
        playlists = [
            Playlist(title=item["snippet"]["title"], id_=item["id"])
            for item in search_response["items"]
        ]

        return next_token, playlists

    def get_playlists_on_channel(self, channel_id: str) -> Iterator[Playlist]:
        """チャンネルに存在するプレイリストを全件取得

        Args:
            channel_id (str): チャンネルID

        Returns:
            Iterator[Playlist]: (プレイリストタイトル, プレイリストID)
        """

        next_token, playlists = self._fetch_playlists_on_channel(channel_id)

        while True:
            if next_token is None:
                break

            next_token, tmp_plist = self._fetch_playlists_on_channel(
                channel_id, next_token
            )
            playlists.extend(tmp_plist)

        return playlists

    def _fetch_playlist_items(
        self, playlist_id: str, next_token: str = ""
    ) -> Tuple[str, List[Thumbnail]]:
        """プレイリスト内の動画サムネイルを取得

        Args:
            playlist_id (str): プレイリストID
            next_token (str): YouTubeAPI 次ページ取得トークン

        Returns:
            Tuple[str, List[Thumbnail]]: 次ページ取得トークン, [動画タイトル, サムネイルURL]
        """
        resource = {
            "mode": "generate_thumbnail_list",
            "playlist_id": playlist_id,
            "next_token": next_token,
        }
        search_response = self.api_repo._get_resource(resource)

        next_token = search_response.get("nextPageToken")
        videos = [
            Thumbnail(
                title=video["snippet"]["title"],
                thumbnail_url=video["snippet"]["thumbnails"]["default"]["url"],
            )
            for video in search_response["items"]
        ]

        return next_token, videos

    def generate_thumbnail_list(self, playlist: Playlist) -> ThumbnailList:
        """プレイリスト内の動画サムネイルリストを作成

        Args:
            playlist (Playlist): プレイリストタイトル, プレイリストID

        Returns:
            ThumbnailList: プレイリスト内の動画サムネイルリスト
        """
        next_token, videos = self._fetch_playlist_items(playlist.id_)

        while True:
            if next_token is None:
                break

            next_token, tmp_videos = self._fetch_playlist_items(
                playlist.id_, next_token
            )
            videos.extend(tmp_videos)

        thumbnail_list = ThumbnailList(title=playlist.title, videos=videos)

        return thumbnail_list

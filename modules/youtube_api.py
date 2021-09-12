from typing import Iterator, Tuple, List, TypedDict, NamedTuple

from apiclient.discovery import build


class Playlist(NamedTuple):
    title: str
    id_: str


class Thumbnail(TypedDict):
    title: str
    thumbnail_url: str


class ThumbnailList(TypedDict):
    title: str
    videos: List[Thumbnail]


class YoutubeAPIUtil:
    def __init__(self, api_key):
        self.youtube_api_key = api_key

    def _get_resource_from_api(self, resource):
        with build("youtube", "v3", developerKey=self.youtube_api_key) as youbute:
            if resource["mode"] == "get_channel_id":
                search_response = (
                    youbute.search()
                    .list(
                        part="snippet",
                        q=resource["channel_name"],
                        type="channel",
                        maxResults=2,
                    )
                    .execute()
                )
        return search_response

    def get_channel_id_from_channel_name(self, channel_name: str) -> str:
        """チャンネル名からチャンネルIDを取得する

        Args:
            channel_name (str): チャンネル名（正式名称）

        Returns:
            str: チャンネルID
        """
        resource = {"mode": "get_channel_id", "channel_name": channel_name}
        search_response = self._get_resource_from_api(resource)
        for item in search_response["items"]:
            title = item["snippet"]["title"]
            if title == channel_name:
                id_ = item["snippet"]["channelId"]
                return id_

    def get_playlists_on_channel(self, channel_id: str) -> Iterator[Playlist]:
        """チャンネルに存在するプレイリスト（再生回数上位5つ）を取得

        Args:
            channel_id (str): チャンネルID

        Yields:
            Iterator[Playlist]: (プレイリストタイトル, プレイリストID)
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
                yield Playlist(title=title, id_=id_)

    def _fetch_playlists(self):
        pass

    def generatet_playlists_thumbnail_list_on_channel(
        self, channel_id: str
    ) -> ThumbnailList:
        """チャンネルに存在するプレイリストのサムネイルリストを作成

        Args:
            channel_id (str): チャンネルID

        Yields:
            Iterator[Playlist]: (プレイリストタイトル, プレイリストID)
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
                yield Playlist(title=title, id_=id_)

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
        with build("youtube", "v3", developerKey=self.youtube_api_key) as youbute:
            search_response = (
                youbute.playlistItems()
                .list(
                    part="snippet",
                    playlistId=playlist_id,
                    pageToken=next_token,
                )
                .execute()
            )

            next_token = search_response.get("nextPageToken")
            videos = [
                {
                    "title": video["snippet"]["title"],
                    "thumbnail_url": video["snippet"]["thumbnails"]["standard"]["url"],
                }
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

        thumbnail_list: ThumbnailList = {"title": playlist.title, "videos": videos}

        return thumbnail_list

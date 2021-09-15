from abc import ABC, abstractmethod

from apiclient.discovery import build


class YouTubeAPIRepository(ABC):
    @abstractmethod
    def _get_resource_from_api(self, resource):
        raise NotImplementedError


class YouTubeAPIRepositoryImpl(YouTubeAPIRepository):
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
            elif resource["mode"] == "get_playlists_on_channel":
                search_response = (
                    youbute.search()
                    .list(
                        part="snippet",
                        channelId=resource["channel_id"],
                        type="playlist",
                        order="videoCount",
                        pageToken=resource["next_token"],
                    )
                    .execute()
                )
            elif resource["mode"] == "generate_thumbnail_list":
                search_response = (
                    youbute.playlistItems()
                    .list(
                        part="snippet",
                        playlistId=resource["playlist_id"],
                        pageToken=resource["next_token"],
                    )
                    .execute()
                )
        return search_response

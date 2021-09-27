from pathlib import Path

from modules.util import download_thumbnails
from modules.youtube_api import YouTubeAPIRepository, YoutubeAPIUtil


class SaveThumbnailService:
    def __init__(self, youtube_api_repo: YouTubeAPIRepository):
        self.youtube_api_util = YoutubeAPIUtil(api_repo=youtube_api_repo)

    def save_thumbnails_group_by_playlist(self, channel_name: str, base_path: Path):
        channel_id = self.youtube_api_util.get_channel_id_from_channel_name(
            channel_name=channel_name
        )
        playlists = self.youtube_api_util.get_playlists_on_channel(
            channel_id=channel_id
        )
        for playlist in playlists:
            download_list = self.youtube_api_util.generate_thumbnail_list(
                playlist=playlist
            )
            download_thumbnails(base_path=base_path, download_list=download_list)

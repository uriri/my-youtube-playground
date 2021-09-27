from typing import Final
from pathlib import Path

from modules.application import SaveThumbnailService
from modules.youtube_api import YouTubeAPIRepositoryImpl

from modules.util import get_api_key_from_config


if __name__ == "__main__":
    conf = get_api_key_from_config()
    YOUTUBE_API_KEY: Final = conf["youtube_data_v3"]
    channel_name: Final = conf["download_thumbnail"]["channel_name"]
    save_dst_dir: Final = conf["download_thumbnail"]["save_dst_dir"]

    youtube_api_repo = YouTubeAPIRepositoryImpl(api_key=YOUTUBE_API_KEY)
    service = SaveThumbnailService(youtube_api_repo)

    service.save_thumbnails_group_by_playlist(channel_name, Path(save_dst_dir))

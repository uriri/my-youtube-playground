import json
import urllib.error
import urllib.request
from pathlib import Path

from modules.models import ThumbnailList


def get_api_key_from_config():

    with open("secrets/api_key.json", "r", encoding="utf-8") as f:
        conf = json.load(f)
    return conf


def delete_unused_char_for_dir_name(origin_str: str) -> str:
    """Windowsディレクトリ名で使用できない文字を_に変換する

    Args:
        origin_str (str): 変換元文字列

    Returns:
        str: 変換後文字列
    """
    return origin_str.translate(
        str.maketrans(
            {
                "\\": "_",
                "/": "_",
                ":": "_",
                "：": "_",
                "*": "_",
                '"': "_",
                ">": "_",
                "<": "_",
                "|": "_",
            }
        )
    )


def download_thumbnails(base_path: Path, download_list: ThumbnailList) -> None:
    playlist_name = download_list["title"]
    save_dir = base_path / delete_unused_char_for_dir_name(playlist_name)
    save_dir.mkdir()

    videos = download_list["videos"]

    for video in videos:
        title = delete_unused_char_for_dir_name(video["title"])
        url = video["thumbnail_url"]

        download_file = save_dir / ".".join([title, "jpg"])
        try:
            with urllib.request.urlopen(url) as thumbnail:
                data = thumbnail.read()
                with open(download_file, mode="wb") as local_file:
                    local_file.write(data)
        except urllib.error.URLError as e:
            print(e)

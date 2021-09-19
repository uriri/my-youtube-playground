from typing import List, NamedTuple


class Playlist(NamedTuple):
    title: str
    id_: str


class Thumbnail(NamedTuple):
    title: str
    thumbnail_url: str


class ThumbnailList(NamedTuple):
    title: str
    videos: List[Thumbnail]

from typing import List, TypedDict, NamedTuple


class Playlist(NamedTuple):
    title: str
    id_: str


class Thumbnail(TypedDict):
    title: str
    thumbnail_url: str


class ThumbnailList(TypedDict):
    title: str
    videos: List[Thumbnail]

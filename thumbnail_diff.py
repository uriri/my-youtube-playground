# %%

from typing import Final
from pathlib import Path

import cv2
import numpy as np

from modules.util import get_api_key_from_config

conf = get_api_key_from_config()
YOUTUBE_API_KEY: Final = conf["youtube_data_v3"]
channel_name: Final = conf["download_thumbnail"]["channel_name"]
save_dst_dir: Final = Path(conf["download_thumbnail"]["save_dst_dir"])

# %%

for playlist_dir in save_dst_dir.iterdir():
    print(playlist_dir)
    for thumbnail in playlist_dir.glob("*"):
        img = cv2.imdecode(np.fromfile(thumbnail, np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow("frame", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        break
    break

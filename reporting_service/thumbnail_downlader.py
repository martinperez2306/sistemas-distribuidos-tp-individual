import logging
import requests

from dependencies.commons.video import Video
THUMBNAILS_STORAGE = "/root/reporting_service/thumbnails"
THUMBNAILS_EXTENSION = ".png"

class ThumbnailDownloader:
    def __init__(self):
        pass

    def download(self, video: Video):
        url = video.thumbnail_link
        logging.info("Download Thumbnail URL [{}]".format(url))
        r = requests.get(url, allow_redirects=True) 
        path = THUMBNAILS_STORAGE + "/" + video.id + THUMBNAILS_EXTENSION
        with open(path, 'wb') as f:
            f.write(r.content)

    
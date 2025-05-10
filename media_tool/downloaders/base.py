import os
from media_tool.config import Config

config = Config()

class BaseDownloader:
    def __init__(self, download_dir=None):
        self.config = config or Config()
        self.download_dir = download_dir or self.config.DOWNLOAD_DIR
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
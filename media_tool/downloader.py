from media_tool.config import Config

class BaseDownloader:
    def __init__(self, download_dir=None, config=None):
        self.config = config or Config()
        self.download_dir = download_dir or self.config.DOWNLOAD_DIR
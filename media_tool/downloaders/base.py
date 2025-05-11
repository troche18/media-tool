import os
from media_tool.config import Config


class BaseDownloader:
    """共通ダウンローダー基底クラス。

    - Config を自動ロードしてユーザー設定を反映
    - download_dir が未指定の場合は Config.DOWNLOAD_DIR
    - ディレクトリが存在しない場合は自動生成
    """

    def __init__(self, download_dir: str | None = None, *, config: Config | None = None) -> None:
        # 設定を 1 度だけロードして共有
        self.config: Config = config or Config()
        self.config.load(self.config.CONFIG_PATH)

        # 保存先ディレクトリ
        self.download_dir: str = download_dir or self.config.DOWNLOAD_DIR
        os.makedirs(self.download_dir, exist_ok=True)

import os
import yt_dlp
from media_tool.downloaders.base import BaseDownloader
from media_tool.converter import Converter, SUPPORTED_FORMATS as CONVERT_FORMATS


class YouTubeDownloader(BaseDownloader):
    """YouTube 用ダウンローダー。必要に応じて自動で形式変換を行う"""

    def download(self, url: str, output_format: str | None = None) -> str:
        # ダウンロード
        ydl_opts = {
            "outtmpl": os.path.join(self.download_dir, "%(title)s.%(ext)s"),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        # 変換不要ならそのまま返す
        if not output_format:
            return file_path

        output_format = output_format.lower()
        if output_format not in CONVERT_FORMATS:
            raise ValueError(
                f"Unsupported convert format: {output_format}. Supported: {', '.join(CONVERT_FORMATS)}"
            )

        # 同じ設定を共有して変換
        converter = Converter(self.config)
        new_file_path = converter.convert_to_format(file_path, output_format)
        os.remove(file_path)
        return new_file_path

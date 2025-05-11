import os
import yt_dlp
from media_tool.downloaders.base import BaseDownloader
from media_tool.converter import Converter, SUPPORTED_FORMATS as CONVERT_FORMATS
from media_tool.config import Config


class NicoNicoDownloader(BaseDownloader):
    """
    ニコニコ動画専用ダウンローダー。フローは YouTubeDownloader と同様。
    """

    def download(self, url: str, output_format: str | None = None) -> str:
        ydl_opts = {
            "outtmpl": os.path.join(self.download_dir, "%(title)s.%(ext)s"),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        self._set_file_timestamp(file_path)

        if output_format:
            output_format = output_format.lower()
            if output_format not in CONVERT_FORMATS:
                raise ValueError(
                    f"Unsupported convert format: {output_format}. "
                    f"Supported formats: {', '.join(CONVERT_FORMATS)}"
                )
            converter = Converter(Config())
            new_file_path =  converter.convert_to_format(file_path, output_format)
            os.remove(file_path)
            return new_file_path

        return file_path
    
    def _set_file_timestamp(self, file_path, timestamp=None):
        """
        指定されたファイルの atime と mtime を変更する
        :param file_path: 対象ファイルのパス
        :param timestamp: 時刻（None の場合は現在時刻）
        """
        if timestamp is None:
            from time import time
            timestamp = time()
        else:
            import time
            timestamp = time.mktime(timestamp.timetuple())

        try:
            os.utime(file_path, (timestamp, timestamp))
            print(f"[INFO] ファイルのタイムスタンプを変更しました: {file_path}")
        except Exception as e:
            print(f"[ERROR] タイムスタンプの変更に失敗しました: {e}")
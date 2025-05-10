import os
import yt_dlp
from media_tool.downloaders.base import BaseDownloader

SUPPORTED_FORMATS = {
    "3gp":   "bestvideo[ext=3gp]+bestaudio[ext=3gp]/best",
    "aac":   "bestaudio[ext=m4a]/best",
    "flv":   "bestvideo[ext=flv]+bestaudio[ext=flv]/best",
    "m4a":   "bestaudio[ext=m4a]/best",
    "mp3":   "bestaudio[ext=mp3]/best",
    "mp4":   "bestvideo+bestaudio/best",
    "ogg":   "bestaudio[ext=ogg]/best",
    "wav":   "bestaudio[ext=wav]/best",
    "webm":  "bestvideo[ext=webm]+bestaudio[ext=webm]/best",
}

DOWNLOAD_FORMATS = list(SUPPORTED_FORMATS.keys())

class YouTubeDownloader(BaseDownloader):
    def download(self, url, format="mp4"):
        if format not in SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {format}. Supported formats are: {', '.join(SUPPORTED_FORMATS)}")
        ydl_opts = {
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'format': SUPPORTED_FORMATS[format],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # ← 直接 YoutubeDL を使う
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        
        # ダウンロード後にタイムスタンプを変更
        self._set_file_timestamp(file_path)

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
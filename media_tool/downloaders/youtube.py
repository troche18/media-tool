import os
import yt_dlp
from typing import Final

from media_tool.downloaders.base import BaseDownloader
from media_tool.converter import Converter, AUDIO_ONLY_FORMATS, VIDEO_FORMATS

DOWNLOAD_FORMATS: Final[list[str]] = sorted(AUDIO_ONLY_FORMATS | VIDEO_FORMATS)

class YouTubeDownloader(BaseDownloader):
    def download(self, url: str, *, output_format: str | None = None) -> list[str] | str:
        fmt = (output_format or "mp4").lower()
        ydl_opts: dict = {"outtmpl": os.path.join(self.download_dir, "%(title)s.%(ext)s")}

        # フォーマット指定
        if fmt in VIDEO_FORMATS:
            ydl_opts.update({"format": "bestvideo+bestaudio/best"})
        else:
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": fmt,
                    "preferredquality": "0",
                }],
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        # プレイリスト判定
        if info.get("_type") == "playlist" or "entries" in info:
            paths: list[str] = []
            for entry in info["entries"]:
                title = entry.get("title", "video")
                # 動画 vs 音声で拡張子決定
                ext = entry.get("ext", fmt) if fmt in VIDEO_FORMATS else fmt
                path = os.path.join(self.download_dir, f"{title}.{ext}")

                # 変換処理
                if ext.lower() != fmt:
                    converter = Converter(self.config)
                    converted = converter.convert_to_format(path, fmt)
                    try: os.remove(path)
                    except FileNotFoundError: pass
                    path = converted

                print(f"[INFO] Downloaded: {path}")
                paths.append(path)
            return paths

        # 単一動画
        title = info.get("title", "video")
        ext = info.get("ext", fmt) if fmt in VIDEO_FORMATS else fmt
        downloaded_path = os.path.join(self.download_dir, f"{title}.{ext}")

        # 変換
        if ext.lower() != fmt:
            converter = Converter(self.config)
            converted = converter.convert_to_format(downloaded_path, fmt)
            try: os.remove(downloaded_path)
            except FileNotFoundError: pass
            downloaded_path = converted

        print(f"[INFO] Downloaded: {downloaded_path}")
        return downloaded_path

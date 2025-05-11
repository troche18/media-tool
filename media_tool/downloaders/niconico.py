import os
import yt_dlp
from typing import Final

from media_tool.downloaders.base import BaseDownloader
from media_tool.converter import Converter, AUDIO_ONLY_FORMATS, VIDEO_FORMATS

DOWNLOAD_FORMATS: Final[list[str]] = sorted(AUDIO_ONLY_FORMATS | VIDEO_FORMATS)

class NicoNicoDownloader(BaseDownloader):
    def download(self, url: str, *, output_format: str | None = None) -> list[str] | str:
        fmt = (output_format or "mp4").lower()
        ydl_opts: dict = {"outtmpl": os.path.join(self.download_dir, "%(title)s.%(ext)s")}
        # ニコニコ用オプション例（必要なら追加）
        # ydl_opts["some_niconico_option"] = ...

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        # プレイリスト or マルチビデオ判定
        if info.get("_type") in ("playlist", "multi_video") or "entries" in info:
            paths: list[str] = []
            for entry in info["entries"]:
                title = entry.get("title", "video")
                ext = entry.get("ext", fmt) if fmt in VIDEO_FORMATS else fmt
                path = os.path.join(self.download_dir, f"{title}.{ext}")

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

        if ext.lower() != fmt:
            converter = Converter(self.config)
            converted = converter.convert_to_format(downloaded_path, fmt)
            try: os.remove(downloaded_path)
            except FileNotFoundError: pass
            downloaded_path = converted

        print(f"[INFO] Downloaded: {downloaded_path}")
        return downloaded_path

import os
import yt_dlp
from typing import Final

from media_tool.downloaders.base import BaseDownloader
from media_tool.converter import Converter, AUDIO_ONLY_FORMATS, VIDEO_FORMATS

# ───────────────────────────────────────────────
# サポートフォーマット一覧
# ───────────────────────────────────────────────
DOWNLOAD_FORMATS: Final[list[str]] = sorted(AUDIO_ONLY_FORMATS | VIDEO_FORMATS)


class YouTubeDownloader(BaseDownloader):
    """YouTube 用ダウンローダー（要フォーマット変換対応版）

    - VIDEO_FORMATS: 可能な限り直接取得し、異なる場合は Converter で変換
    - AUDIO_ONLY_FORMATS: bestaudio を抽出し FFmpegExtractAudio で変換
    """

    def download(self, url: str, *, output_format: str | None = None) -> str:
        """
        Parameters
        ----------
        url : str
            YouTube 動画の URL
        output_format : str | None
            保存フォーマット（例: "mp4", "webm", "mp3"）。
            None の場合は "mp4" を使用。

        Returns
        -------
        str
            保存されたファイルパス（要求フォーマットで必ず返す）
        """
        # 要求フォーマットを大文字小文字区別なく取得
        fmt = (output_format or "mp4").lower()
        if fmt not in DOWNLOAD_FORMATS:
            raise ValueError(
                f"Unsupported format: {fmt}. Supported: {', '.join(DOWNLOAD_FORMATS)}"
            )

        # 安全なテンプレート：拡張子は yt_dlp が自動決定
        safe_outtmpl = os.path.join(self.download_dir, "%(title)s.%(ext)s")
        ydl_opts: dict[str, object] = {"outtmpl": safe_outtmpl}

        # 映像系フォーマット
        if fmt in VIDEO_FORMATS:
            if fmt == "mp4":
                # H.264 + AAC の MP4 ストリームを直接取得して高速マージ
                ydl_opts.update({
                    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                    "merge_output_format": "mp4",
                })
            else:
                # その他（webm, mkv, flv, 3gp）は変換せず mkv や相当するコンテナで結合
                ydl_opts.update({
                    "format": "bestvideo+bestaudio/best",
                    # merge_output_format を指定しないことで yt_dlp が安全な形式で結合
                })
        else:
            # 音声のみフォーマット
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": fmt,
                        "preferredquality": "0",
                    }
                ],
            })

        # ダウンロード実行
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "video")
            # VIDEOの場合はinfo['ext']を拡張子に、AUDIOの場合は要求fmtを拡張子に
            ext = info.get("ext", fmt) if fmt in VIDEO_FORMATS else fmt
            downloaded_path = os.path.join(self.download_dir, f"{title}.{ext}")

        # デバッグ出力
        print(f"[DEBUG] info['ext'] = {info.get('ext')}, fmt = {fmt}")
        print(f"[DEBUG] downloaded_path exists: {os.path.exists(downloaded_path)}, path: {downloaded_path}")

        # 要求フォーマットと異なれば Converter で変換
        if ext.lower() != fmt:
            converter = Converter(self.config)
            converted_path = converter.convert_to_format(downloaded_path, fmt)
            try:
                os.remove(downloaded_path)
            except FileNotFoundError:
                pass
            downloaded_path = converted_path

        print(f"[INFO] Downloaded: {downloaded_path}")
        return downloaded_path

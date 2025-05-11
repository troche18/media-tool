import os
import subprocess
from media_tool.config import Config
from media_tool.utils import check_ffmpeg_installed, get_ffmpeg_supported_formats

# ffmpeg の存在確認
check_ffmpeg_installed()

# ffmpeg が扱える拡張子一覧
SUPPORTED_FORMATS = get_ffmpeg_supported_formats()

# 音声／映像フォーマット分類
AUDIO_ONLY_FORMATS = {"mp3", "m4a", "aac", "ogg", "wav", "flac", "opus"}
VIDEO_FORMATS = {"mp4", "webm", "mkv", "flv", "3gp"}


class Converter:
    """形式変換ユーティリティ"""

    def __init__(self, config: Config | None = None) -> None:
        self.config: Config = config or Config()
        self.config.load(self.config.CONFIG_PATH)
        os.makedirs(self.config.OUTPUT_DIR, exist_ok=True)

    def convert_to_format(self, input_path: str, output_format: str) -> str:
        """input_path を output_format へ変換し、OUTPUT_DIR に保存してパスを返す"""
        output_format = output_format.lower()

        # ── 妥当性チェック ────────────────────────────────
        if output_format not in SUPPORTED_FORMATS:
            raise ValueError(
                f"convertエラー: ffmpeg でサポートされていないフォーマットです: {output_format}"
            )
        if not os.path.exists(input_path):
            raise FileNotFoundError(
                f"convertエラー: ファイルが存在しません: {input_path}"
            )

        # ── 出力ファイルパス ──────────────────────────────
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(self.config.OUTPUT_DIR, f"{base_name}.{output_format}")

        # ── FFmpeg コマンド構築 ───────────────────────────
        if output_format in AUDIO_ONLY_FORMATS:
            cmd = ["ffmpeg", "-y", "-i", input_path, "-vn", output_path]

        elif output_format == "mp4":
            cmd = [
                "ffmpeg", "-y", "-i", input_path,
                "-c:v", "libx264", "-c:a", "aac",
                "-movflags", "+faststart",
                output_path,
            ]

        elif output_format == "webm":
            # WebM は VP9 + Opus で再エンコード
            cmd = [
                "ffmpeg", "-y", "-i", input_path,
                "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "32",
                "-c:a", "libopus", "-b:a", "128k",
                output_path,
            ]

        else:  # mkv, flv, 3gp など → ストリームコピー
            cmd = ["ffmpeg", "-y", "-i", input_path, "-c", "copy", output_path]

        # ── 実行 ────────────────────────────────────────
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"ffmpeg failed (exit {e.returncode})") from e

        return output_path

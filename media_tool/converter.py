import os
import subprocess
from media_tool.config import Config
from media_tool.utils import check_ffmpeg_installed, get_ffmpeg_supported_formats

# 初期化時にffmpegの存在をチェック
try:
    check_ffmpeg_installed()
except EnvironmentError as e:
    raise

# 初期ロード
SUPPORTED_FORMATS = get_ffmpeg_supported_formats()

class Converter:
    def __init__(self, config: Config):
        self.config = config

    def convert_to_format(self, input_path: str, output_format: str) -> str:
        output_format = output_format.lower()
        if output_format not in SUPPORTED_FORMATS:
            raise ValueError("convertエラー", f"ffmpegでサポートされていないフォーマットです。{output_format}")
        if not os.path.exists(input_path):
            raise ValueError("convertエラー", f"ファイルが存在しません{input_path}")
        input_path_ext = input_path.split(".")[-1]
        if "." not in input_path or input_path_ext not in SUPPORTED_FORMATS:
            raise ValueError("convertエラー", f"ffmpegでサポートされていないフォーマットです。{input_path_ext}")
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}.{output_format}"
        if os.path.exists(output_path):
            os.remove(output_path)

        cmd = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-vn",          # 音声のみ抽出
            output_path,
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if proc.returncode != 0:
            log = proc.stdout.decode("utf-8", errors="ignore")
            raise RuntimeError(f"ffmpeg failed:\n{log}")

        return output_path
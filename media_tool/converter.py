import os
from media_tool.config import Config
from media_tool.utils import check_ffmpeg_installed, get_ffmpeg_supported_formats, FFMPEG_SESSION

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
        check_ffmpeg_installed()

    def convert_to_format(self, input_path: str, output_format: str) -> str:
        output_format = output_format.lower()
        if output_format not in SUPPORTED_FORMATS:
            raise ValueError(...)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(self.config.OUTPUT_DIR, f"{base_name}.{output_format}")

        cmd = ["-i", input_path, output_path]
        try:
            FFMPEG_SESSION.run(cmd)  # ← 使いまわし
            return output_path
        except Exception as e:
            raise
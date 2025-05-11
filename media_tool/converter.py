import os
import subprocess
from media_tool.config import Config
from media_tool.utils import check_ffmpeg_installed, get_ffmpeg_supported_formats

# ffmpeg の存在を確認
check_ffmpeg_installed()

# ffmpeg が扱えるフォーマット一覧
SUPPORTED_FORMATS = get_ffmpeg_supported_formats()


class Converter:
    """音声・動画ファイルを別形式に変換するユーティリティ"""

    def __init__(self, config: Config | None = None) -> None:
        # 共通設定を読み込む
        self.config: Config = config or Config()
        self.config.load(self.config.CONFIG_PATH)
        # 出力ディレクトリを用意
        os.makedirs(self.config.OUTPUT_DIR, exist_ok=True)

    def convert_to_format(self, input_path: str, output_format: str) -> str:
        """input_path を output_format へ変換し、OUTPUT_DIR に保存してパスを返す"""
        output_format = output_format.lower()

        # フォーマット妥当性チェック
        if output_format not in SUPPORTED_FORMATS:
            raise ValueError("convertエラー", f"ffmpeg でサポートされていないフォーマットです: {output_format}")

        if not os.path.exists(input_path):
            raise ValueError("convertエラー", f"ファイルが存在しません: {input_path}")

        input_ext = os.path.splitext(input_path)[1].lstrip(".").lower()
        if input_ext not in SUPPORTED_FORMATS:
            raise ValueError("convertエラー", f"ffmpeg でサポートされていないフォーマットです: {input_ext}")

        # 出力ファイルパス
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(self.config.OUTPUT_DIR, f"{base_name}.{output_format}")

        # 既存ファイルを置き換え
        if os.path.exists(output_path):
            os.remove(output_path)

        # ffmpeg 実行
        cmd = [
            "ffmpeg",
            "-y",           # 既存ファイルを自動上書き
            "-i", input_path,
            "-vn",          # 音声のみ
            output_path,
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if proc.returncode != 0:
            log = proc.stdout.decode("utf-8", errors="ignore")
            raise RuntimeError(f"ffmpeg failed:\n{log}")

        return output_path

import os
import json
from platformdirs import user_downloads_dir, user_documents_dir


class Config:
    def __init__(self):
        self.OUTPUT_DIR = user_documents_dir()
        self.DOWNLOAD_DIR = user_downloads_dir()
        self.DEFAULT_FORMAT = "mp3"
        self.LOG_LEVEL = "INFO"
        self.BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        self.ROOT_DIR = os.path.dirname(self.BASE_DIR)
        self.CONFIG_PATH = os.path.join(self.ROOT_DIR, "config.json")

    def load(self, config_path):
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
            for key in ["OUTPUT_DIR", "DOWNLOAD_DIR", "DEFAULT_FORMAT", "LOG_LEVEL"]:
                if key in config_data:
                    setattr(self, key, config_data[key])

    def validate(self):
        from .utils import get_ffmpeg_supported_formats
        errors = []
        if not os.path.isdir(self.OUTPUT_DIR):
            errors.append("OUTPUT_DIR")
        if not os.path.isdir(self.DOWNLOAD_DIR):
            errors.append("DOWNLOAD_DIR")
        if self.DEFAULT_FORMAT not in get_ffmpeg_supported_formats():
            errors.append("DEFAULT_FORMAT")
        if self.LOG_LEVEL not in {"DEBUG", "INFO", "WARNING", "ERROR"}:
            errors.append("LOG_LEVEL")
        if errors:
            raise ValueError(f"Invalid config values: {', '.join(errors)}")

    def save(self, config_path):
        new_config = {
            "OUTPUT_DIR": self.OUTPUT_DIR,
            "DOWNLOAD_DIR": self.DOWNLOAD_DIR,
            "DEFAULT_FORMAT": self.DEFAULT_FORMAT,
            "LOG_LEVEL": self.LOG_LEVEL
        }
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(new_config, f, indent=2, ensure_ascii=False)
            print(f"設定を保存しました: {config_path}")
        except Exception as e:
            print(f"[エラー] 設定の保存に失敗しました: {e}")
            raise
    
    def get_config_dict(self):
        return {
                "OUTPUT_DIR": self.OUTPUT_DIR,
                "DOWNLOAD_DIR": self.DOWNLOAD_DIR,
                "DEFAULT_FORMAT": self.DEFAULT_FORMAT,
                "LOG_LEVEL": self.LOG_LEVEL,
            }
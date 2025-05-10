import subprocess
import os

def check_ffmpeg_installed():
    try:
        startupinfo = None
        if os.name == 'nt':
            import subprocess
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, startupinfo=startupinfo)
    except Exception as e:
        raise EnvironmentError("ffmpeg が見つかりません") from e

def get_ffmpeg_supported_formats():
    """ffmpeg がサポートする拡張子一覧を取得"""
    try:
        check_ffmpeg_installed()
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-formats"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=True
        )
        lines = result.stdout.splitlines()

        supported = set()
        for line in lines:
            if line.startswith(" D "):
                parts = line.split()
                exts = [e for e in parts if e.startswith(".")]
                for e in exts:
                    ext = e[1:].lower()
                    supported.add(ext)
        if not supported:
            raise ValueError("No formats found from ffmpeg.")
    except Exception as e:
        return {
            "mp3", "wav", "ogg", "flac", "aac",
            "mp4", "avi", "mkv", "mov", "wmv",
            "webm", "m4a", "mpg", "mpeg", "flv"
        }
    return supported

class FFmpegSession:
    def __init__(self):
        self.startupinfo = None
        if os.name == 'nt':
            import subprocess
            self.startupinfo = subprocess.STARTUPINFO()
            self.startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    def run(self, args):
        return subprocess.run(
            ["ffmpeg"] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            startupinfo=self.startupinfo
        )

FFMPEG_SESSION = FFmpegSession()
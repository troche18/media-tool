import argparse
import sys

from media_tool.config import Config
from media_tool.converter import Converter, SUPPORTED_FORMATS as CONVERT_FORMATS
from media_tool.downloaders.youtube import YouTubeDownloader
from media_tool.downloaders.niconico import NicoNicoDownloader
from media_tool.settings_gui import SettingsGUI


def main() -> None:
    # 共通設定をロード
    config = Config()
    config.load(config.CONFIG_PATH)
    try:
        config.validate()
    except ValueError as e:
        print("Error in config:", e)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Media Tool CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # convert
    convert_parser = subparsers.add_parser("convert", help="Convert media file")
    convert_parser.add_argument("input", help="Input file path")
    convert_parser.add_argument(
        "--format",
        default=config.DEFAULT_FORMAT,
        choices=CONVERT_FORMATS,
        help=f"Output format (default: {config.DEFAULT_FORMAT}). Supported: {', '.join(CONVERT_FORMATS)}",
    )
    convert_parser.add_argument(
        "--ext",
        dest="extension",
        help="任意の拡張子を指定（例: aac）※指定すると --format は無視されます",
    )

    # download
    download_parser = subparsers.add_parser("download", help="Download video from URL")
    download_parser.add_argument("url", help="Video URL (YouTube / ニコニコ動画)")
    download_parser.add_argument(
        "--format",
        choices=CONVERT_FORMATS,
        help="Convert to this format after download (省略時はダウンロードのみ)",
    )

    # settings
    subparsers.add_parser("settings", help="Open settings GUI")

    args = parser.parse_args()

    if args.command == "convert":
        converter = Converter(config)
        output_format = args.extension or args.format
        result = converter.convert_to_format(args.input, output_format)
        print(f"Converted to {result}")

    elif args.command == "download":
        # URL で動画サイトを判定し、共通設定を共有
        downloader = (
            YouTubeDownloader(config=config)
            if "youtube" in args.url.lower()
            else NicoNicoDownloader(config=config)
        )
        result = downloader.download(args.url, output_format=args.format)
        print(f"Saved to {result}")

    elif args.command == "settings":
        import tkinter as tk
        root = tk.Tk()
        SettingsGUI(root)  # type: ignore[arg-type]
        root.mainloop()


if __name__ == "__main__":
    main()

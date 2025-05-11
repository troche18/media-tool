import argparse
import sys
from media_tool.converter import Converter, SUPPORTED_FORMATS as CONVERT_FORMATS
from media_tool.downloaders.youtube import YouTubeDownloader
from media_tool.downloaders.niconico import NicoNicoDownloader
from media_tool.config import Config
from media_tool.settings_gui import SettingsGUI

def main():
    config = Config()
    config.load(config.CONFIG_PATH)
    try:
        config.validate()
    except ValueError as e:
        print("Error in config:", e)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Media Tool CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Convert
    convert_parser = subparsers.add_parser("convert", help="Convert media file")
    convert_parser.add_argument("input", help="Input file path")
    convert_parser.add_argument("--format", default="mp3", help=f"Output format (default: mp3). Supported: {', '.join(CONVERT_FORMATS)}")
    convert_parser.add_argument("--ext", dest="extension", help="任意の拡張子を指定（例: aac）※指定すると --format は無視されます")

    # Download
    download_parser = subparsers.add_parser("download", help="Download and (optionally) convert a video")
    download_parser.add_argument("url", help="Video URL (YouTube / ニコニコ動画)")
    download_parser.add_argument(
        "--format",
        default="mp3",
        choices=CONVERT_FORMATS,
        help="Convert to this format after download (default: mp3)",
    )

    args = parser.parse_args()

    if args.command == "convert":
        converter = Converter(config)
        output_format = args.extension or args.format
        result = converter.convert_to_format(args.input, output_format)
        print(f"Converted to {result}")
    
    elif args.command == "download":
        if "nicovideo.jp" in args.url or "nico.ms" in args.url:
            downloader = NicoNicoDownloader()
        else:
            downloader = YouTubeDownloader()
        
        result = downloader.download(args.url, output_format=args.format)
        print(f"Saved to: {result}")
    
    elif args.command == "settings":
        import tkinter as tk
        root = tk.Tk()
        app = SettingsGUI(root)
        root.mainloop()
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
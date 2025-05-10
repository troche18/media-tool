import argparse
import sys
from media_tool.converter import Converter, SUPPORTED_FORMATS as CONVERT_FORMATS
from media_tool.downloaders.youtube import YouTubeDownloader, SUPPORTED_FORMATS as DOWNLOAD_FORMATS
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
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Convert
    convert_parser = subparsers.add_parser("convert", help="Convert media file")
    convert_parser.add_argument("input", help="Input file path")
    convert_parser.add_argument("--format", default="mp3", help=f"Output format (default: mp3). Supported: {', '.join(CONVERT_FORMATS)}")
    convert_parser.add_argument("--ext", dest="extension", help="任意の拡張子を指定（例: aac）※指定すると --format は無視されます")

    # Download
    download_parser = subparsers.add_parser("download", help="Download video from URL")
    download_parser.add_argument("url", help="Video URL")
    download_parser.add_argument("--format", default="mp4", help=f"Download format (default: mp4). Supported: {', '.join(DOWNLOAD_FORMATS)}")

    args = parser.parse_args()

    if args.command == "convert":
        converter = Converter(config)
        output_format = args.extension or args.format
        result = converter.convert_to_format(args.input, output_format)
        print(f"Converted to {result}")

    elif args.command == "download":
        dl = YouTubeDownloader()
        result = dl.download(args.url, format=args.format)
        print(f"Downloaded to {result}")
    
    elif args.command == "settings":
        import tkinter as tk
        root = tk.Tk()
        app = SettingsGUI(root)
        root.mainloop()

if __name__ == "__main__":
    main()
#!/usr/bin/env python
"""
Media-Tool Launcher
...
"""

from __future__ import annotations
import os
import sys
from pathlib import Path

import argparse
from media_tool.config import Config
from media_tool.converter import Converter, SUPPORTED_FORMATS as CONVERT_FORMATS
from media_tool.downloaders.youtube import YouTubeDownloader
from media_tool.downloaders.niconico import NicoNicoDownloader
from media_tool.settings_gui import SettingsGUI

def main() -> None:
    config = Config()
    config.load(config.CONFIG_PATH)
    try:
        config.validate()
    except ValueError as e:
        print("Error in config:", e)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Media Tool CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ■ convert: 複数ファイル対応
    convert_parser = subparsers.add_parser("convert", help="Convert media files")
    convert_parser.add_argument(
        "inputs",
        nargs="+",
        help="Input file paths（複数指定可）"
    )
    convert_parser.add_argument(
        "--format",
        default=config.DEFAULT_FORMAT,
        choices=CONVERT_FORMATS,
        help=f"出力拡張子（ffmpeg 対応）を指定（既定: {config.DEFAULT_FORMAT}）",
    )

    # ■ download: 複数URL & プレイリスト対応
    download_parser = subparsers.add_parser("download", help="Download video(s) from URL(s)")
    download_parser.add_argument(
        "urls",
        nargs="+",
        help="Video URLs（YouTube / ニコニコ動画、複数もしくはプレイリストURL可）"
    )
    download_parser.add_argument(
        "--format",
        choices=CONVERT_FORMATS,
        help="ダウンロード後にこの拡張子へ変換（省略時は変換なし）",
    )

    # ■ settings
    subparsers.add_parser("settings", help="Open settings GUI")

    args = parser.parse_args()

    if args.command == "convert":
        converter = Converter(config)
        for inp in args.inputs:
            try:
                result = converter.convert_to_format(inp, args.format)
                print(f"[INFO] Converted: {result}")
            except Exception as e:
                print(f"[ERROR] Failed to convert {inp}: {e}")

    elif args.command == "download":
        for url in args.urls:
            # URL判断とダウンローダー生成
            downloader = (
                YouTubeDownloader(config=config)
                if "youtube" in url.lower()
                else NicoNicoDownloader(config=config)
            )
            try:
                results = downloader.download(url, output_format=args.format)
                # 戻り値がリストなら複数表示、そうでなければ単一
                if isinstance(results, list):
                    for path in results:
                        print(f"[INFO] Saved to {path}")
                else:
                    print(f"[INFO] Saved to {results}")
            except Exception as e:
                print(f"[ERROR] Failed to download {url}: {e}")

    elif args.command == "settings":
        import tkinter as tk
        root = tk.Tk()
        SettingsGUI(root)  # type: ignore[arg-type]
        root.mainloop()

if __name__ == "__main__":
    main()

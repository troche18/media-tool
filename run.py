#!/usr/bin/env python
"""
Media-Tool Launcher
----------------------------------
clone 直後に run.py をダブルクリック（または `python run.py`）すれば
Pixi が自動で依存を解決し、GUI もしくは CLI が起動します。

オプション:
  --cli       CLI モードで起動
"""

from __future__ import annotations
import os
import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent


# ──────────────────────────────────────────────────────────
# 判定・チェック系
# ──────────────────────────────────────────────────────────
def inside_pixi() -> bool:
    """現在 Pixi 環境内かを判定"""
    return "PIXI_PROJECT_ROOT" in os.environ


def ensure_pixi():
    """Pixi がインストールされているか確認"""
    if shutil.which("pixi"):
        return
    print(
        "[ERROR] Pixi が見つかりません。\n"
        "下記コマンドで Pixi をインストールしてから run.py を再実行してください。\n\n"
        "  Windows (PowerShell):  irm https://pixi.sh/install.ps1 | iex\n"
        "  macOS/Linux (Shell):  curl -fsSL https://pixi.sh/install.sh | sh"
    )
    sys.exit(1)


def ensure_ffmpeg():
    """ffmpeg バイナリの存在を確認（Pixi 依存で自動解決されている想定）"""
    if shutil.which("ffmpeg"):
        return
    print(
        "[ERROR] ffmpeg が見つかりません。\n"
        "pyproject.toml の [tool.pixi.dependencies] に `ffmpeg = \"*\"` を追記し、\n"
        "`pixi lock --update-all` を実行してから再度 run.py を起動してください。"
    )
    sys.exit(1)


# ──────────────────────────────────────────────────────────
# Pixi 外→内 再実行
# ──────────────────────────────────────────────────────────
def reinvoke_via_pixi(extra_args: list[str]):
    """Pixi 環境外なら Pixi 経由でこのスクリプトを再実行"""
    print("Pixi 環境を初期化・起動します… (初回は数分かかる場合があります)")
    cmd = ["pixi", "run", "python", str(ROOT / "run.py"), "--_internal"] + extra_args
    os.execvp(cmd[0], cmd)  # 現プロセスを置き換え


# ──────────────────────────────────────────────────────────
# メイン
# ──────────────────────────────────────────────────────────
def main():
    args = sys.argv[1:]
    internal = False
    if "--_internal" in args:
        args.remove("--_internal")
        internal = True

    # Pixi 外なら Pixi で再実行
    if not inside_pixi() and not internal:
        ensure_pixi()
        reinvoke_via_pixi(args)

    # ここから Pixi 環境内
    ensure_ffmpeg()

    if "--cli" in args:
        args.remove("--cli")
        from cli import main as cli_main
        sys.argv = ["media-tool"] + args
        cli_main()
    else:
        from media_tool.gui import MediaToolGUI
        app = MediaToolGUI()
        app.mainloop()


if __name__ == "__main__":
    main()

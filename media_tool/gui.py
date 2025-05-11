#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Media-Tool GUI

機能:
  • ファイルの一括変換
  • URL/プレイリストの一括ダウンロード
  • 拡張子個別指定 (ffmpeg 対応形式)
  • 設定 GUI の呼び出しと即時反映
"""
from __future__ import annotations

import sys
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from media_tool.config import Config
from media_tool.converter import Converter, SUPPORTED_FORMATS
from media_tool.downloaders.youtube import YouTubeDownloader
from media_tool.downloaders.niconico import NicoNicoDownloader
from media_tool.settings_gui import SettingsGUI

# ----------------------------------------------------------------------
# ユーティリティ
# ----------------------------------------------------------------------
def format_paths_for_dialog(paths: list[str], limit: int = 5) -> str:
    """ダイアログ用にパスを簡略表示する。"""
    if not paths:
        return "(なし)"
    names = [Path(p).name for p in paths]
    if len(names) <= limit:
        return "\n".join(names)
    shown = "\n".join(names[:limit])
    return f"{shown}\n…他 {len(names) - limit} 件"


# ----------------------------------------------------------------------
# メイン GUI
# ----------------------------------------------------------------------
class MediaToolGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Media Tool")
        self.resizable(False, False)

        # 設定読み込み
        self.config = Config()
        self.config.load(self.config.CONFIG_PATH)
        try:
            self.config.validate()
        except ValueError as e:
            messagebox.showerror("設定エラー", str(e))
            sys.exit(1)

        # ウィジェット構築
        self._build_widgets()

    # ------------------------------------------------------------------
    # ウィジェット
    # ------------------------------------------------------------------
    def _build_widgets(self) -> None:
        pad = {"padx": 10, "pady": 4}

        # ==== 変換セクション ===========================================
        convert_frame = ttk.LabelFrame(self, text="変換")
        convert_frame.grid(row=0, column=0, sticky="ew", **pad)

        ttk.Label(convert_frame, text="出力形式").grid(row=0, column=0, **pad)
        self.cv_format_var = tk.StringVar(value=self.config.DEFAULT_FORMAT)
        ttk.OptionMenu(
            convert_frame,
            self.cv_format_var,
            self.cv_format_var.get(),
            *SUPPORTED_FORMATS,
        ).grid(row=0, column=1, **pad)

        ttk.Button(
            convert_frame,
            text="ファイルを選択して変換",
            command=self._on_convert_click,
        ).grid(row=0, column=2, **pad)

        # ==== ダウンロードセクション ===================================
        download_frame = ttk.LabelFrame(self, text="ダウンロード")
        download_frame.grid(row=1, column=0, sticky="ew", **pad)

        ttk.Label(download_frame, text="URL").grid(row=0, column=0, **pad)
        self.url_var = tk.StringVar()
        ttk.Entry(download_frame, textvariable=self.url_var, width=45).grid(
            row=0, column=1, **pad
        )

        ttk.Label(download_frame, text="出力形式").grid(row=1, column=0, **pad)
        self.dl_format_var = tk.StringVar(value=self.config.DEFAULT_FORMAT)
        ttk.OptionMenu(
            download_frame,
            self.dl_format_var,
            self.dl_format_var.get(),
            *SUPPORTED_FORMATS,
        ).grid(row=1, column=1, **pad)

        ttk.Button(
            download_frame, text="ダウンロード", command=self._on_download_click
        ).grid(row=1, column=2, **pad)

        # ==== 設定ボタン ===============================================
        ttk.Button(
            self,
            text="設定を開く",
            command=self._open_settings,
            width=30,
        ).grid(row=2, column=0, padx=10, pady=(6, 10), sticky="ew")

    # ------------------------------------------------------------------
    # イベントハンドラ
    # ------------------------------------------------------------------
    # --- 変換 ---------------------------------------------------------
    def _on_convert_click(self) -> None:
        paths = filedialog.askopenfilenames(
            title="変換するファイルを選択",
            filetypes=[("メディアファイル", "*.*")],
        )
        if not paths:
            return
        threading.Thread(
            target=self._convert_worker,
            args=(list(paths), self.cv_format_var.get()),
            daemon=True,
        ).start()

    def _convert_worker(self, paths: list[str], fmt: str) -> None:
        converter = Converter(self.config)
        success, errors = [], []
        for p in paths:
            try:
                success.append(converter.convert_to_format(p, fmt))
            except Exception as e:
                errors.append(f"{Path(p).name}: {e}")
        self.after(0, lambda: self._show_result("変換", success, errors))

    # --- ダウンロード -------------------------------------------------
    def _on_download_click(self) -> None:
        url_text = self.url_var.get().strip()
        if not url_text:
            messagebox.showwarning("入力エラー", "URL を入力してください。")
            return
        urls = url_text.split()  # スペース区切り可
        threading.Thread(
            target=self._download_worker,
            args=(urls, self.dl_format_var.get()),
            daemon=True,
        ).start()

    def _download_worker(self, urls: list[str], fmt: str) -> None:
        success, errors = [], []
        for url in urls:
            try:
                dl = (
                    YouTubeDownloader(config=self.config)
                    if "youtube" in url.lower()
                    else NicoNicoDownloader(config=self.config)
                )
                res = dl.download(url, output_format=fmt)
                success.extend(res if isinstance(res, list) else [res])
            except Exception as e:
                errors.append(f"{url}: {e}")
        self.after(0, lambda: self._show_result("ダウンロード", success, errors))

    # --- 設定 ---------------------------------------------------------
    def _open_settings(self) -> None:
        win = tk.Toplevel(self)
        win.title("設定")
        SettingsGUI(win, on_update=self._reload_config)
        win.grab_set()  # モーダル化

    def _reload_config(self) -> None:
        """設定ファイルを再読み込みし、GUI へ反映。"""
        try:
            self.config.load(self.config.CONFIG_PATH)
            self.cv_format_var.set(self.config.DEFAULT_FORMAT)
            self.dl_format_var.set(self.config.DEFAULT_FORMAT)
        except Exception as e:
            messagebox.showerror("設定再読込失敗", str(e))

    # ------------------------------------------------------------------
    # 共通ダイアログ
    # ------------------------------------------------------------------
    def _show_result(self, title: str, success: list[str], errors: list[str]) -> None:
        if success:
            messagebox.showinfo(
                f"{title}完了",
                f"{len(success)} 件を処理しました:\n\n"
                f"{format_paths_for_dialog(success)}\n\n"
                "※完全なパスはコンソールログ参照",
            )
        if errors:
            messagebox.showerror(
                f"{title}失敗",
                f"{len(errors)} 件でエラー:\n\n{format_paths_for_dialog(errors)}",
            )


# ----------------------------------------------------------------------
# エントリポイント
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = MediaToolGUI()
    app.mainloop()

import tkinter as tk
from tkinter import filedialog, messagebox
import os
from media_tool.config import Config

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

class SettingsGUI:
    def __init__(self, root, on_save=None):
        self.root = root
        self.on_save = on_save
        self.config = Config()
        self.config.load(CONFIG_PATH)
        try:
            self.config.validate()
        except ValueError:
            pass
        self.create_widgets()

    def create_widgets(self):
        global OUTPUT_DIR, DOWNLOAD_DIR, DEFAULT_FORMAT, LOG_LEVEL
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # 出力ディレクトリ
        tk.Label(frame, text="出力ディレクトリ (OUTPUT_DIR)").pack(anchor=tk.W)
        self.output_dir = tk.StringVar(value=self.config.OUTPUT_DIR)
        tk.Entry(frame, textvariable=self.output_dir, width=60).pack(side=tk.TOP, fill=tk.X)
        tk.Button(frame, text="参照...", command=self.select_output_dir).pack(pady=2)

        # ダウンロードディレクトリ
        tk.Label(frame, text="ダウンロードディレクトリ (DOWNLOAD_DIR)").pack(anchor=tk.W, pady=(10, 0))
        self.download_dir = tk.StringVar(value=self.config.DOWNLOAD_DIR)
        tk.Entry(frame, textvariable=self.download_dir, width=60).pack(side=tk.TOP, fill=tk.X)
        tk.Button(frame, text="参照...", command=self.select_download_dir).pack(pady=2)

        # デフォルト形式
        tk.Label(frame, text="デフォルト形式 (DEFAULT_FORMAT)").pack(anchor=tk.W, pady=(10, 0))
        self.default_format = tk.StringVar(value=self.config.DEFAULT_FORMAT)
        tk.Entry(frame, textvariable=self.default_format, width=60).pack(side=tk.TOP, fill=tk.X)

        # ログレベル
        tk.Label(frame, text="ログレベル (LOG_LEVEL)").pack(anchor=tk.W, pady=(10, 0))
        self.log_level = tk.StringVar(value=self.config.LOG_LEVEL)
        tk.OptionMenu(frame, self.log_level, "DEBUG", "INFO", "WARNING", "ERROR").pack(anchor=tk.W)

        # 保存ボタン
        tk.Button(frame, text="保存", command=self.save_settings, bg="green", fg="white").pack(pady=15)

    def select_output_dir(self):
        path = filedialog.askdirectory(initialdir=self.output_dir.get())
        if path:
            self.output_dir.set(path)

    def select_download_dir(self):
        path = filedialog.askdirectory(initialdir=self.download_dir.get())
        if path:
            self.download_dir.set(path)

    def save_settings(self):
        self.config.OUTPUT_DIR = self.output_dir.get()
        self.config.DOWNLOAD_DIR = self.download_dir.get()
        self.config.DEFAULT_FORMAT = self.default_format.get()
        self.config.LOG_LEVEL = self.log_level.get()
        try:
            self.config.validate()
        except ValueError as e:
            messagebox.showerror("エラー", f"{e}の値が不正です。")
            return
        self.config.save(CONFIG_PATH)
        if self.on_save:
            self.on_save()
        self.root.destroy()
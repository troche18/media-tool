import tkinter as tk
from tkinter import filedialog, messagebox
from media_tool.utils import check_ffmpeg_installed, get_ffmpeg_supported_formats
from media_tool.converter import Converter
from media_tool.downloaders.youtube import YouTubeDownloader, DOWNLOAD_FORMATS
from media_tool.config import Config
from media_tool.settings_gui import SettingsGUI

class MediaToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Tool")
        self.config = Config()
        self.config.load(self.config.CONFIG_PATH)  # config.json から読み込み
        try:
            self.config.validate()
        except ValueError as e:
            print(f"設定値に問題があります: {e}")
        self.convert_formats = get_ffmpeg_supported_formats()
        self.refresh_ui_from_config()

    def refresh_ui_from_config(self):
        # 既存のウィジェット削除
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # ffmpegチェック
        check_ffmpeg_installed()

        # メニューバー
        menubar = tk.Menu(self.root)
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="設定を開く", command=self.open_settings)
        menubar.add_cascade(label="設定", menu=settings_menu)
        self.root.config(menu=menubar)

        # 変換セクション
        self.convert_frame = tk.LabelFrame(self.root, text="Convert File")
        self.convert_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.file_path = tk.StringVar()
        tk.Entry(self.convert_frame, textvariable=self.file_path, width=50).pack(side="left", padx=5)
        tk.Button(self.convert_frame, text="Select File", command=self.select_file).pack(side="left")

        self.convert_format_var = tk.StringVar(value=self.config.DEFAULT_FORMAT)  # ← Config経由
        self.convert_format_menu = tk.OptionMenu(self.convert_frame, self.convert_format_var, *self.convert_formats)
        self.convert_format_menu.pack(side="left")

        self.custom_ext_var = tk.StringVar()
        self.custom_ext_entry = tk.Entry(self.convert_frame, textvariable=self.custom_ext_var, width=10)
        self.custom_ext_entry.pack(side="left", padx=2)
        tk.Label(self.convert_frame, text="拡張子").pack(side="left")

        self.error_label = tk.Label(self.convert_frame, text="", fg="red")
        self.error_label.pack(side="left", padx=5)

        self.convert_btn = tk.Button(self.convert_frame, text="Convert", command=self.convert_file)
        self.convert_btn.pack(side="left")

        # ダウンロードセクション
        self.download_frame = tk.LabelFrame(self.root, text="Download Video (YouTube)")
        self.download_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.url_var = tk.StringVar()
        tk.Entry(self.download_frame, textvariable=self.url_var, width=50).pack(side="left", padx=5)

        self.download_format_var = tk.StringVar(value="mp4")
        self.download_format_menu = tk.OptionMenu(self.download_frame, self.download_format_var, *DOWNLOAD_FORMATS)
        self.download_format_menu['menu'].delete(0, 'end')
        for fmt in DOWNLOAD_FORMATS:
            self.download_format_menu['menu'].add_command(label=fmt, command=tk._setit(self.download_format_var, fmt))
        self.download_format_menu.pack(side="left")

        self.download_btn = tk.Button(self.download_frame, text="Download", command=self.download_video)
        self.download_btn.pack(side="left")

        # イベントバインディング
        self.custom_ext_var.trace_add("write", self.validate_extension)

    def select_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.file_path.set(path)
            self.update_button_states()

    def update_button_states(self):
        input_set = bool(self.file_path.get())
        self.convert_btn.config(state=tk.NORMAL if input_set else tk.DISABLED)

    def validate_extension(self, *args):
        custom_ext = self.custom_ext_var.get().strip().lower()
        selected_format = self.convert_format_var.get()

        # カスタム拡張子があれば優先
        output_format = custom_ext or selected_format
        
        if not custom_ext:
            self.error_label.config(text="")
            return

        if output_format in self.convert_formats:
            self.error_label.config(text="✔ OK")
        else:
            self.error_label.config(text=f"⚠ 無効な形式: {output_format}")

    def convert_file(self):
        converter = Converter(self.config)
        input_path = self.file_path.get()
        custom_ext = self.custom_ext_var.get().strip()
        selected_format = self.convert_format_var.get()
        output_format = custom_ext or selected_format
        
        try:
            output_path = converter.convert_to_format(input_path, output_format)
            messagebox.showinfo("Success", f"Converted to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def download_video(self):
        url = self.url_var.get()
        output_format = self.download_format_var.get()
        print(output_format)
        if not url:
            messagebox.showerror("Error", "Please enter a URL.")
            return
        try:
            result = YouTubeDownloader().download(url, format=output_format)
            messagebox.showinfo("Success", f"Saved at {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_settings(self):
        """settings_gui.py のSettingsGUIを別ウィンドウで開く"""
        settings_root = tk.Toplevel(self.root)
        def on_saved():
            self.refresh_ui_from_config()

        SettingsGUI(settings_root, on_save=on_saved)

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaToolGUI(root)
    root.mainloop()
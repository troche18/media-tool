#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Media-Tool 設定 GUI
(JSON 版・動的フィールド・内部パス除外・横幅拡大・
 パス項目に参照ダイアログ付き)
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Dict, Union

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from media_tool.config import Config

# ────────────────────────────────────────────────────────────────────
# 画面に出さない内部キー
# ────────────────────────────────────────────────────────────────────
EXCLUDE_KEYS = {"BASE_DIR", "ROOT_DIR", "CONFIG_PATH"}

# ────────────────────────────────────────────────────────────────────
# 型エイリアス
# ────────────────────────────────────────────────────────────────────
JSONValue = Union[str, int, float, bool]

# ────────────────────────────────────────────────────────────────────
# ユーティリティ
# ────────────────────────────────────────────────────────────────────
def _parse_value(value: str, target_type: type) -> JSONValue:
    """文字列を target_type に変換（失敗時は str のまま返す）。"""
    try:
        if target_type is bool:
            return value.lower() in {"1", "true", "yes", "on"}
        if target_type is int:
            return int(value)
        if target_type is float:
            return float(value)
        if target_type is Path:
            return str(Path(value).expanduser())
    except Exception:
        pass
    return value

def _to_str(value: Any) -> str:
    return str(value if not isinstance(value, Path) else value.expanduser())

def _is_path_field(key: str, value: Any) -> bool:
    """パス入力欄にするか判定。"""
    if isinstance(value, Path):
        return True
    return key.endswith(("DIR", "_DIR", "PATH", "_PATH"))

# ────────────────────────────────────────────────────────────────────
# 設定 GUI 本体
# ────────────────────────────────────────────────────────────────────
class SettingsGUI(ttk.Frame):
    FIELD_PAD = {"padx": 6, "pady": 4}

    def __init__(self, master: tk.Misc, *, on_update: Callable[[], None] | None = None) -> None:
        super().__init__(master, padding=10)
        self.pack(fill="both", expand=True)

        # ── ウィンドウ設定 ──
        if isinstance(master, (tk.Tk, tk.Toplevel)):
            master.minsize(width=600, height=260)
            master.resizable(True, False)
        self.columnconfigure(1, weight=1)  # Entry 列
        self.columnconfigure(2, weight=0)  # ボタン列

        # ── 設定読込 ──
        self.cfg = Config()
        self.cfg.load(self.cfg.CONFIG_PATH)
        self.on_update = on_update
        self._field_vars: Dict[str, tk.Variable] = {}

        # ── 動的フィールド生成 ──
        row = 0
        for key, value in sorted(self._iter_user_items()):
            ttk.Label(self, text=key).grid(row=row, column=0, sticky="w", **self.FIELD_PAD)

            if isinstance(value, bool):
                var = tk.BooleanVar(value=value)
                ttk.Checkbutton(self, variable=var).grid(
                    row=row, column=1, sticky="w", **self.FIELD_PAD
                )
            else:
                var = tk.StringVar(value=_to_str(value))
                entry = ttk.Entry(self, textvariable=var, width=60)

                if _is_path_field(key, value):
                    entry.grid(row=row, column=1, sticky="ew", **self.FIELD_PAD)
                    ttk.Button(
                        self, text="参照…", width=8,
                        command=self._make_browse_cmd(var, key)
                    ).grid(row=row, column=2, sticky="e", **self.FIELD_PAD)
                else:
                    entry.grid(
                        row=row, column=1, columnspan=2,
                        sticky="ew", **self.FIELD_PAD
                    )

            self._field_vars[key] = var
            row += 1

        # ── 保存ボタン ──
        ttk.Button(self, text="保存して閉じる", command=self._on_save).grid(
            row=row, column=0, columnspan=3, pady=(12, 0)
        )

    # ────────────────────────────────────────────────────────────
    # 内部メソッド
    # ────────────────────────────────────────────────────────────
    def _iter_user_items(self):
        """ユーザーが編集できる項目を列挙。"""
        for attr in dir(self.cfg):
            if not attr.isupper():
                continue
            if attr.startswith("_") or attr in EXCLUDE_KEYS:
                continue
            yield attr, getattr(self.cfg, attr)

    def _make_browse_cmd(self, var: tk.StringVar, key: str) -> Callable[[], None]:
        """参照ダイアログのコールバックを生成。"""
        def _browse() -> None:
            current = var.get() or "."
            title = f"{key} を選択"
            if key.endswith(("DIR", "_DIR")):
                sel = filedialog.askdirectory(initialdir=current, title=title)
            else:
                sel = filedialog.askopenfilename(initialdir=current, title=title)
            if sel:
                var.set(sel)
        return _browse

    # ────────────────────────────────────────────────────────────
    # 保存
    # ────────────────────────────────────────────────────────────
    def _on_save(self) -> None:
        try:
            updated: Dict[str, JSONValue] = {}

            for key, var in self._field_vars.items():
                current = getattr(self.cfg, key)
                raw = var.get()
                new_val: JSONValue = (
                    bool(var.get()) if isinstance(current, bool)
                    else _parse_value(raw, type(current))
                )
                setattr(self.cfg, key, new_val)
                updated[key] = new_val

            self.cfg.validate()

            with open(self.cfg.CONFIG_PATH, "w", encoding="utf-8") as fp:
                json.dump(updated, fp, ensure_ascii=False, indent=2)

            messagebox.showinfo("保存完了", "設定を保存しました。")

            if callable(self.on_update):
                self.on_update()

            self.master.destroy()

        except Exception as e:
            messagebox.showerror("保存失敗", str(e))

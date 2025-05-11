# Media Tool · 音声・動画変換 & ダウンロードツール <!-- omit in toc -->

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Powered by Pixi](https://img.shields.io/badge/Env-Pixi%20🦀-brightgreen)](https://pixi.sh)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)

シンプルかつ高速に **YouTube / ニコニコ動画** からのダウンロードと  
**音声・動画フォーマット変換** を行うクロスプラットフォームツールです。  
GUI（Tkinter）と CLI を搭載し、初心者でもすぐに使い始められます。

- [主な機能](#主な機能)
- [動作環境](#動作環境)
- [インストール](#インストール)
  - [Pixi を使わずに試す場合（簡易）](#pixi-を使わずに試す場合簡易)
- [使い方](#使い方)
  - [GUI](#gui)
  - [CLI](#cli)
- [設定ファイル](#設定ファイル)
- [開発](#開発)
- [License](#license)

---

## 主な機能
- 📥 **ダウンロード**: YouTube / ニコニコ動画（プレイリスト対応）
- 🔄 **形式変換**: mp3・aac・flac・mp4・webm など FFmpeg がサポートする拡張子
- 🖥 **GUI**: Tkinter 製のシンプルな操作画面
- 🖧 **CLI**: `python cli.py URL -f mp3` など 1 行コマンド
- ⚙️ **設定管理**: `config.json` で出力先やデフォルト形式を保存
- 🦀 **Pixi 環境**: 依存パッケージを汚さずインストール

## 動作環境
| 種別          | バージョン / 備考 |
|--------------|------------------|
| Python       | **3.11 以上** |
| OS           | Windows / macOS / Linux |
| 必須バイナリ | [FFmpeg](https://ffmpeg.org/) (PATH が通っていること) |
| Python依存   | `yt-dlp`, `platformdirs` |

> **補足**: `tkinter` は標準ライブラリ、`ffmpeg` は外部実行ファイルです。

## インストール
~~~bash
# Pixi をまだ導入していない場合
curl -fsSL https://pixi.sh/install.sh | bash

# リポジトリを取得
git clone https://github.com/yourname/media-tool.git
cd media-tool

# Pixi で依存を構築
pixi install          # 初回のみ
pixi run python run.py  # GUI 起動
~~~

### Pixi を使わずに試す場合（簡易）
~~~bash
python -m venv .venv && source .venv/bin/activate  # Windows は .venv\Scripts\activate
pip install -r requirement.txt
python run.py
~~~

## 使い方

### GUI
~~~bash
pixi run python run.py
~~~
1. URL を入力  
2. 変換後フォーマットを選択  
3. `Download` をクリック

### CLI
~~~bash
pixi run python cli.py <URL> -f mp3 -o ~/Music
~~~
主なオプション:

| オプション | 意味 | 既定値 |
|-----------|------|-------|
| `-f`, `--format` | 出力フォーマット | `mp3` |
| `-o`, `--output-dir` | 出力ディレクトリ | `~/Downloads` |
| `--keep-temp` | 一時ファイルを削除しない | False |

## 設定ファイル
初回起動時にルート直下へ `config.json` が生成されます。  
GUI で変更するか、直接 JSON を編集してください。

| 項目 | 説明 |
|------|------|
| `OUTPUT_DIR` | 変換後ファイルの保存先 |
| `DOWNLOAD_DIR` | 元動画の保存先 |
| `DEFAULT_FORMAT` | GUI／CLI 既定フォーマット |
| `LOG_LEVEL` | `INFO` / `DEBUG` |

## 開発
~~~bash
# テスト実行
pixi run pytest

# スタンドアロン実行ファイル作成 (Windows例)
pixi run pyinstaller run.py -n media-tool-gui --onefile -w
~~~
- **依存管理**: `pyproject.toml` + Pixi  
- **開発依存**: `pytest`, `pyinstaller` 等は `dev-requirements.txt` へ分離

## License
[MIT](LICENSE)

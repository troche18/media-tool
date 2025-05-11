# Media Tool · 音声・動画変換 & ダウンロードツール <!-- omit in toc -->

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Powered by Pixi](https://img.shields.io/badge/Env-Pixi%20🦀-brightgreen)](https://pixi.sh)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)

シンプルかつ高速に **YouTube / ニコニコ動画** からのダウンロードと  
**音声・動画フォーマット変換** を行うクロスプラットフォームツールです。  

- [主な機能](#主な機能)
- [動作環境](#動作環境)
- [インストール](#インストール)
- [使い方](#使い方)
  - [GUI](#gui)
  - [CLI](#cli)
- [設定ファイル](#設定ファイル)
- [License](#license)

---

## 主な機能
- **ダウンロード**: YouTube / ニコニコ動画（プレイリスト対応）
- **形式変換**: mp3・aac・flac・mp4・webm など FFmpeg がサポートする拡張子
- **GUI**: Tkinter 製のシンプルな操作画面
- **CLI**: `python cli.py URL -f mp3` など 1 行コマンド
- **設定管理**: `config.json` で出力先やデフォルト形式を保存
- **Pixi 環境**: 依存パッケージを汚さずインストール

## 動作環境
| 種別          | バージョン / 備考 |
|--------------|------------------|
| Python       | **3.11 以上** |
| OS           | Windows / macOS / Linux |
| 必須バイナリ | [FFmpeg](https://ffmpeg.org/) (PATH が通っていること) |
| Python依存   | `yt-dlp`, `platformdirs` |

> **補足**: `tkinter` は標準ライブラリ、`ffmpeg` は外部実行ファイルです。

## インストール

本ツールは **Python 3.11 以上** と **Pixi** さえ入っていれば、他に前提ソフトは不要です。  
ローカル環境を汚さず一発でセットアップできます。

~~~bash
# 1) Pixi をインストール（未導入の場合のみ）
curl -fsSL https://pixi.sh/install.sh | bash    # Linux/macOS
# Windows PowerShell:
# iwr -useb https://pixi.sh/install.ps1 | iex

# 2) リポジトリを取得
git clone https://github.com/troche18/media-tool.git
cd media-tool

# 3) 起動
python run.py
~~~

> **備考**  
> - pip / venv 手順は不要です。すべて Pixi が面倒を見ます。  
> - FFmpeg は同梱せず、システム PATH 上の実行ファイルを利用します（必要に応じて追加してください）。

## 使い方

### GUI
~~~bash
# ダブルクリック、または
python run.py                 # Pixi 環境なら `pixi run python run.py`
~~~
1. URL を入力  
2. 変換後フォーマットを選択  
3. **Download** をクリック

### CLI
~~~bash
# GUI と同じランチャーに --cli を付ける
python run.py --cli <URL> -f mp3 -o ~/Music
~~~
主なオプション | 意味 | 既定値
--------------|------|------
`-f`, `--format` | 出力フォーマット | `mp3`
`-o`, `--output-dir` | 出力ディレクトリ | `~/Downloads`
`--keep-temp` | 一時ファイルを削除しない | False

> `cli.py` を直接呼び出すことも可能ですが、依存チェックを自動化する **run.py** を推奨します。

## 設定ファイル
初回起動時にルート直下へ `config.json` が生成されます。  
GUI で変更するか、直接 JSON を編集してください。

| 項目 | 説明 |
|------|------|
| `OUTPUT_DIR` | 変換後ファイルの保存先 |
| `DOWNLOAD_DIR` | 元動画の保存先 |
| `DEFAULT_FORMAT` | GUI／CLI 既定フォーマット |
| `LOG_LEVEL` | `INFO` / `DEBUG` |

## License
[MIT](LICENSE)

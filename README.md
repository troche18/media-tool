# Media Tool - 音声・動画変換 & ダウンロードツール

シンプルなメディア変換・ダウンロードツールです。GUIとCLIの両方に対応し、YouTubeやニコニコ動画からもダウンロード可能です。

## 機能

- 動画 → 音声変換（MP3など）
- YouTube / ニコニコ動画からの動画ダウンロード
- GUIによる操作（Tkinter）
- 設定フォームによるディレクトリ設定
- config.jsonで設定管理
- Rust製環境管理ツール「Pixi」使用

## 依存

- Python 3.11+
- Pixi (https://pixi.sh )
- FFmpeg

## インストール

```bash
# Pixiをインストール
curl -fsSL https://pixi.sh/install.sh | bash

# 依存をインストール
pixi install
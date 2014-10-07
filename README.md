# pyslash

[![Build Status](https://travis-ci.org/7pairs/pyslash.svg?branch=master)](https://travis-ci.org/7pairs/pyslash)
[![Coverage Status](https://coveralls.io/repos/7pairs/pyslash/badge.png?branch=master)](https://coveralls.io/r/7pairs/pyslash?branch=master)

## 概要

[nikkansports.com](http://www.nikkansports.com/)のプロ野球の試合結果を整形するツールです。[ねことくまとへび](http://seven-pairs.hatenablog.jp/)というブログで野球の戦評を書くときに使用しています。Pythonを使ってHTMLをslashし、テキストとして再構築することからpyslashという名前をつけました。それ以上の深い意味はありません。たぶん。

## インストール

同梱の `setup.py` を実行してください。

```
python setup.py install
```

pipを利用している場合は、GitHubから直接インストールすることもできます。

```
pip install git+https://github.com/7pairs/pyslash.git
```

## 実行方法

チーム、試合日（任意）を指定して実行してください。

```
pyslash -t <team> [-d <day>]
```

`<team>` には以下のいずれかを指定してください。オリックス、横浜DeNAの略号に違和感がありますが、これはnikkansports.com内の表記に準拠しているためです。

|略号|チーム|
|---|---|
|l|埼玉西武|
|e|東北楽天|
|m|千葉ロッテ|
|h|福岡ソフトバンク|
|bu|オリックス|
|f|北海道日本ハム|
|g|読売|
|t|阪神|
|c|広島東洋|
|d|中日|
|bs|横浜DeNA|
|s|東京ヤクルト|

`<day>` には以下のいずれかの書式で試合日を指定してください。

* `YYYYMMDD` の8桁。YYYY年MM月DD日として扱われます。
* `MMDD` の4桁。今年のMM月DD日として扱われます。
* `DD` の2桁。今月のDD日として扱われます。

`<day>` を指定しなかった場合、実行日（実行した環境のシステム日付）が入力されたものとして扱われます。

また、スコアテーブルのURLを直接指定して実行することもできます。

```
pyslash -u <url>
```

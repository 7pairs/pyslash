# pyslash

[![Build Status](https://travis-ci.org/7pairs/pyslash.svg?branch=master)](https://travis-ci.org/7pairs/pyslash)
[![Coverage Status](https://img.shields.io/coveralls/7pairs/pyslash.svg)](https://coveralls.io/r/7pairs/pyslash?branch=master)

## 概要

[nikkansports.com](http://www.nikkansports.com/) からプロ野球の試合結果を取得し、プレーンテキストで見やすいように整形するツールです。 [ねことくまとへび](http://seven-pairs.hatenablog.jp/) というブログでライオンズ戦の戦評を書くときに使用しています。Pythonを用いてHTMLをslashし、テキストとして再構築することからpyslashという名前をつけました。それ以上の深い意味はありません。たぶん。

## バージョン

Python3.4での動作を確認しています。また、3.2、3.3でもユニットテストを行っていますので、おそらく両バージョンでも動作するものと思われます。なお、Python2系には対応しておりません。ご了承ください。

## インストール

同梱の `setup.py` を実行してください。

```
python setup.py install
```

pipを導入している方は、GitHubから直接インストールすることもできます。

```
pip install git+https://github.com/7pairs/pyslash.git
```

## 実行方法

チーム、試合日（任意）を指定して実行してください。

```
pyslash -t <team> [-d <day>]
```

`<team>` には以下のいずれかの略号を指定してください。オリックス、横浜DeNAの略号に違和感があるかもしれませんが、これはnikkansports.com内での表記に準拠しているためです。

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

`<day>` を指定しなかった場合、実行した環境のシステム日付が入力されたものとして扱われます。

また、スコアテーブルのURLを直接指定して実行することもできます。

```
pyslash -u <url>
```

# pyslash

[![Build Status](https://travis-ci.org/7pairs/pyslash.svg?branch=master)](https://travis-ci.org/7pairs/pyslash)
[![Coverage Status](https://img.shields.io/coveralls/7pairs/pyslash.svg)](https://coveralls.io/r/7pairs/pyslash?branch=master)

## 概要

"pyslash" は [nikkansports.com](http://www.nikkansports.com/) からプロ野球の試合結果を取得し、プレーンテキストで見やすいように整形するツールです。
[ねことくまとへび](http://seven-pairs.hatenablog.jp/) というブログでライオンズ戦の戦評を書くときに利用しています。
PythonでHTMLをslashし、プレーンテキストとして再構築することから "pyslash" と名付けました。
それ以上の深い意味はありません。
たぶん。

## バージョン

Python3.4での動作を確認しています。また、Python3.2および3.3でもユニットテストを実施しています。

## インストール

同梱の `setup.py` を実行してください。

```console
$ python setup.py install
```

pipを利用して、GitHubから直接インストールすることもできます。

```console
$ pip install git+https://github.com/7pairs/pyslash.git
```

## 実行方法

### チームと試合日を指定する

```console
$ pyslash -t <team> [-d <day>]
```

`<team>` には以下のいずれかの略号を指定してください。
オリックス、横浜DeNAの略号に違和感があるかもしれませんが、nikkansports.com内での表記に準拠するためにこのような形になっています。

|略号|チーム          |
|----|----------------|
|bs  |横浜DeNA        |
|bu  |オリックス      |
|c   |広島東洋        |
|d   |中日            |
|e   |東北楽天        |
|f   |北海道日本ハム  |
|g   |読売            |
|h   |福岡ソフトバンク|
|l   |埼玉西武        |
|m   |千葉ロッテ      |
|s   |東京ヤクルト    |
|t   |阪神            |

`<day>` には以下のいずれかの書式で試合日を指定してください。

|書式      |解釈                              |
|----------|----------------------------------|
|`YYYYMMDD`|YYYY年MM月DD日として処理をします。|
|`MMDD`    |今年のMM月DD日として処理をします。|
|`DD`      |今月のDD日として処理をします。    |

なお、 `<day>` を指定しなかった場合は、nikkansports.comのトップページからリンクされている試合（当日の試合であることが多いでしょう）を対象とします。

### スコアのURLを指定する

```
$ pyslash -u <url>
```

`<url>` にはnikkansports.com内のスコアのページのURLを指定してください。

## ライセンス

pyslashは [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0) にて提供します。

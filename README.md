# pyslash

[![Build Status](https://travis-ci.org/7pairs/pyslash.svg?branch=master)](https://travis-ci.org/7pairs/pyslash)
[![Coverage Status](https://img.shields.io/coveralls/7pairs/pyslash.svg)](https://coveralls.io/r/7pairs/pyslash?branch=master)

## 概要

"pyslash" は [nikkansports.com](http://www.nikkansports.com/) からプロ野球の試合結果を取得し、整形されたプレーンテキストとして出力するツールです。
ブログ『 [ねことくまとへび](http://lions.blue/) 』で戦評を書く際に利用しています。
PythonでHTMLを切り刻み、プレーンテキストとして再構築することから "pyslash" と名付けました。
それ以上の深い意味はありません。
たぶん。

## バージョン

Python3.6での動作を確認しています。
また、Python3.3〜3.5でもユニットテストを実施しています。

## インストール

同梱の `setup.py` を実行してください。

```
$ python setup.py install
```

pipを利用して、GitHubのリポジトリから直接インストールすることもできます。

```
$ pip install git+https://github.com/7pairs/pyslash.git
```

## 実行

### チームと試合日を指定する

```
$ pyslash -t <team> [-d <day>]
```

`<team>` には以下のいずれかの略号を指定してください。
横浜DeNA、オリックスの略号に違和感があるかもしれませんが、nikkansports.com内での表記に準拠するためこのような形になっています。

| 略号 | チーム           |
|------|------------------|
| `bs` | 横浜DeNA         |
| `bu` | オリックス       |
| `c`  | 広島東洋         |
| `d`  | 中日             |
| `e`  | 東北楽天         |
| `f`  | 北海道日本ハム   |
| `g`  | 読売             |
| `h`  | 福岡ソフトバンク |
| `l`  | 埼玉西武         |
| `m`  | 千葉ロッテ       |
| `s`  | 東京ヤクルト     |
| `t`  | 阪神             |

`<day>` には以下のいずれかの書式で試合日を指定してください。

| 書式       | 処理                               |
|------------|------------------------------------|
| `YYYYMMDD` | YYYY年MM月DD日として処理をします。 |
| `MMDD`     | 今年のMM月DD日として処理をします。 |
| `DD`       | 今月のDD日として処理をします。     |

なお、 `-d` オプションを省略した場合は、nikkansports.comのトップページからリンクされている試合を対象として処理します。

### スコアのURLを指定する

```
$ pyslash -u <url>
```

`<url>` にはnikkansports.com内のスコアのページのURLを指定してください。

## ライブラリ

pyslashでは下記のライブラリを利用しています。

- [beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4)
- [click](https://pypi.python.org/pypi/click)
- [enum34](https://pypi.python.org/pypi/enum34)
- [nose](https://pypi.python.org/pypi/nose)
- [mock](https://pypi.python.org/pypi/mock)

## ライセンス

pyslashは [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0) にて提供します。

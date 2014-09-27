# -*- coding: utf-8 -*-

"""
nikkansports.py

Usage:
nikkansports.py -t <team> [-d <day>]
nikkansports.py -u <url>
nikkansports.py -h | --help
nikkansports.py -v | --version

Options:
-d <day>      game day.
-h --help     print this help message and exit.
-t <team>     initials of team.
-u <url>      url of score table.
-v --version  print the version number and exit.
"""

from docopt import docopt

import crawler.baseball


# バージョン番号
VERSION = '1.0.0'


if __name__ == '__main__':
    # 引数を取得する
    args = docopt(__doc__, version=VERSION)

    # スコアテーブルを出力する
    if args.get('-t'):
        day = args.get('-d') or ''
        print(crawler.baseball.get_score_table_by_param(args['-t'], day))
    elif args.get('-u'):
        print(crawler.baseball.get_score_table_by_url(args['-u']))

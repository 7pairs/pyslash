# -*- coding: utf-8 -*-

"""
execute.py

Usage:
execute.py -t <team> [-d <day>]
execute.py -u <url>
execute.py -h | --help
execute.py -v | --version

Options:
-d <day>      game day.
-h --help     print this help message and exit.
-t <team>     initials of team.
-u <url>      url of score table.
-v --version  print the version number and exit.
"""

from docopt import docopt

import nikkansports.baseball


# バージョン番号
VERSION = '1.0.0'


if __name__ == '__main__':
    # 引数を取得する
    args = docopt(__doc__, version=VERSION)

    # スコアテーブルを出力する
    if args.get('-t'):
        day = args.get('-d') or ''
        print(nikkansports.baseball.get_score_table_by_param(args['-t'], day))
    elif args.get('-u'):
        print(nikkansports.baseball.get_score_table(args['-u']))

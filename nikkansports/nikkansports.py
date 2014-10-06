# -*- coding: utf-8 -*-

"""
Tools for parsing 'nikkansports.com'.

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
import datetime

from docopt import docopt

from crawler import baseball


# バージョン番号
__version__ = '1.0.0'


if __name__ == '__main__':
    # 引数を取得する
    args = docopt(__doc__, version=__version__)

    # スコアテーブルを出力する
    if args.get('-t'):
        today = datetime.datetime.today()
        day_str = args.get('-d') or ''
        day_str_len = len(day_str)
        if day_str_len == 8:
            day = datetime.datetime.strptime(day_str, '%Y%m%d')
        elif day_str_len == 4:
            day = datetime.datetime.strptime(day_str, '%m%d')
            day = day.replace(year=today.year)
        elif day_str_len == 2:
            day = datetime.datetime.strptime(day_str, '%d')
            day = day.replace(year=today.year, month=today.month)
        else:
            day = None
        print(baseball.get_score_table(args['-t'], day))
    elif args.get('-u'):
        print(baseball.get_score_table_by_url(args['-u']))

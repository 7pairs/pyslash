# -*- coding: utf-8 -*-

#
# Copyright 2015 Jun-ya HASEBA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Tools for parsing 'nikkansports.com'.

Usage:
pyslash -t <team> [-d <day>]
pyslash -u <url>
pyslash -h | --help
pyslash -v | --version

Options:
-d <day>      game day.
-h --help     print this help message and exit.
-t <team>     initials of team.
-u <url>      url of score table.
-v --version  print the version number and exit.
"""
import datetime
import os
import sys

from docopt import docopt

try:
    # setup.py実行後
    from pyslash import baseball
    from pyslash import __version__
except ImportError:
    # 未インストール状態での動作確認時
    sys.path.append(os.path.split(os.path.dirname(__file__))[0])
    from pyslash import baseball
    from pyslash import __version__


def main():
    """
    テーブルスコアを標準出力に書き出す。
    """
    # 引数を取得する
    args = docopt(__doc__, version=__version__)

    # スコアテーブルを出力する
    if args.get('-t'):
        today = datetime.date.today()
        day_str = args.get('-d') or ''
        day_str_len = len(day_str)
        if day_str_len == 8:
            day = datetime.datetime.strptime(day_str, '%Y%m%d').date()
        elif day_str_len == 4:
            day = datetime.datetime.strptime(day_str, '%m%d').date()
            day = day.replace(year=today.year)
        elif day_str_len == 2:
            day = datetime.datetime.strptime(day_str, '%d').date()
            day = day.replace(year=today.year, month=today.month)
        else:
            day = None
        print(baseball.create_result(args['-t'], day))
    elif args.get('-u'):
        print(baseball.create_result_by_url(args['-u']))


if __name__ == '__main__':
    main()

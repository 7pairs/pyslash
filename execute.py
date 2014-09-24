# -*- coding: utf-8 -*-

import sys

import nikkansports.baseball


if __name__ == '__main__':
    # 引数をチェック
    if len(sys.argv) != 2:
        print('Usage: python %s url' % sys.argv[0])
        quit()

    # スコアテーブルを出力
    score_table = nikkansports.baseball.get_score_table(sys.argv[1])
    print(score_table)

# -*- coding: utf-8 -*-

import datetime

from nose.tools import *

from nikkansports import baseball
from nikkansports.exception import ParseError


def test_get_html_01():
    """
    引数に有効なURLを指定したとき、そのURLのHTMLの内容を文字列として返すことを確認する。
    """
    html = baseball.get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014050203.html')
    actual = ('<title>プロ野球スコア速報 ロッテ対西武 : nikkansports.com</title>' in html)
    assert_equal(True, actual)


def test_get_html_02():
    """
    引数に無効なURLを指定したとき、空文字列を返すことを確認する。
    """
    html = baseball.get_html('エラーアルよー')
    assert_equal('', html)


def test_create_dict_01():
    """
    引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
    """
    with open('./test/test_create_dict.html') as test_file:
        html = test_file.read()
    actual = baseball.create_dict(html)
    assert_equal('日本ハム', actual['bat_first'])
    assert_equal('西武', actual['field_first'])
    assert_equal(4, actual['match'])
    assert_equal(datetime.date(2014, 4, 29), actual['date'])
    assert_equal('西武ドーム', actual['stadium'])
    assert_equal([[0, 0], [0, 0], [0, 1], [0, 0], [0, 2], [0, 0], [1, 0], [0, 1], [0, 'x']], actual['score'])
    assert_equal([1, 4], actual['total_score'])
    assert_equal(['牧田', 2, 1, 0], actual['win'])
    assert_equal(['高橋', 0, 1, 3], actual['save'])
    assert_equal(['メンドーサ', 1, 4, 0], actual['lose'])
    assert_equal([['7回表', '佐藤賢', 3, 'ソロ', '牧田']], actual['homerun'])


@raises(ParseError)
def test_create_dict_02():
    """
    引数に無効なHTML文字列を指定したとき、ParseErrorが発生することを確認する。
    """
    with open('./test/test_create_dict_error.html') as test_file:
        html = test_file.read()
    actual = baseball.create_dict(html)


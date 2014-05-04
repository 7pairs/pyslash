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
    assert_equal([[0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 1, 0, 2, 0, 0, 1, 'x']], actual['score'])
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


def test_get_full_team_name_01():
    """
    引数に'西武'を指定したとき、'埼玉西武'を返すことを確認する。
    """
    actual = baseball.get_full_team_name('西武')
    assert_equal('埼玉西武', actual)


def test_get_full_team_name_02():
    """
    引数に'楽天'を指定したとき、'東北楽天'を返すことを確認する。
    """
    actual = baseball.get_full_team_name('楽天')
    assert_equal('東北楽天', actual)


def test_get_full_team_name_03():
    """
    引数に'ロッテ'を指定したとき、'千葉ロッテ'を返すことを確認する。
    """
    actual = baseball.get_full_team_name('ロッテ')
    assert_equal('千葉ロッテ', actual)


def test_get_full_team_name_04():
    """
    引数に'ソフトバンク'を指定したとき、'福岡ソフトバンク'を返すことを確認する。
    """
    actual = baseball.get_full_team_name('ソフトバンク')
    assert_equal('福岡ソフトバンク', actual)


def test_get_full_team_name_05():
    """
    引数に'オリックス'を指定したとき、'オリックス'を返すことを確認する。
    """
    actual = baseball.get_full_team_name('オリックス')
    assert_equal('オリックス', actual)


def test_get_full_team_name_06():
    """
    引数に'日本ハム'を指定したとき、'北海道日本ハム'を返すことを確認する。
    """
    actual = baseball.get_full_team_name('日本ハム')
    assert_equal('北海道日本ハム', actual)


def test_get_full_team_name_07():
    """
    引数に'巨人'を指定したとき、'読売'を返すことを確認する。
    """
    actual = baseball.get_full_team_name('巨人')
    assert_equal('読売', actual)


def test_get_full_team_name_08():
    """
    引数に'阪神'を指定したとき、'阪神'を返すことを確認する。
    """
    actual = baseball.get_full_team_name('阪神')
    assert_equal('阪神', actual)


def test_get_full_team_name_09():
    """
    引数に'広島'を指定したとき、'広島東洋'を返すことを確認する。
    """
    actual = baseball.get_full_team_name('広島')
    assert_equal('広島東洋', actual)


def test_get_full_team_name_10():
    """
    引数に'中日'を指定したとき、'中日'を返すことを確認する。
    """
    actual = baseball.get_full_team_name('中日')
    assert_equal('中日', actual)


def test_get_full_team_name_11():
    """
    引数に'ＤｅＮＡ'を指定したとき、'横浜ＤｅＮＡ'を返すことを確認する。
    """
    actual = baseball.get_full_team_name('ＤｅＮＡ')
    assert_equal('横浜ＤｅＮＡ', actual)


def test_get_full_team_name_12():
    """
    引数に'ヤクルト'を指定したとき、'東京ヤクルト'を返すことを確認する。
    """
    actual = baseball.get_full_team_name('ヤクルト')
    assert_equal('東京ヤクルト', actual)


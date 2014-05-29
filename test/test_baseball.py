# -*- coding: utf-8 -*-

import datetime
import textwrap

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
    html = baseball.get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014042905.html')
    actual = baseball.create_dict(html)
    assert_equal('日本ハム', actual['bat_first'])
    assert_equal('西武', actual['field_first'])
    assert_equal(4, actual['match'])
    assert_equal(datetime.date(2014, 4, 29), actual['date'])
    assert_equal('西武ドーム', actual['stadium'])
    assert_equal([
        ['0', '0', '0', '0', '0', '0', '1', '0', '0'],
        ['0', '0', '1', '0', '2', '0', '0', '1', 'x'],
    ], actual['score'])
    assert_equal([1, 4], actual['total_score'])
    assert_equal(['牧田', 2, 1, 0], actual['win'])
    assert_equal(['高橋', 0, 1, 3], actual['save'])
    assert_equal(['メンドーサ', 1, 4, 0], actual['lose'])
    assert_equal([['7回表', '佐藤賢', 3, 'ソロ', '牧田']], actual['homerun'])


def test_create_dict_02():
    """
    引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
    （2ラン、3ランの解析時不具合対応 #13）
    """
    html = baseball.get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014050906.html')
    actual = baseball.create_dict(html)
    assert_equal('西武', actual['bat_first'])
    assert_equal('ソフトバンク', actual['field_first'])
    assert_equal(7, actual['match'])
    assert_equal(datetime.date(2014, 5, 9), actual['date'])
    assert_equal('北九州', actual['stadium'])
    assert_equal([
        ['0', '1', '0', '3', '0', '0', '0', '0', '2'],
        ['1', '1', '0', '0', '0', '0', '2', '0', '0'],
    ], actual['score'])
    assert_equal([6, 4], actual['total_score'])
    assert_equal(['ウィリアムス', 1, 0, 0], actual['win'])
    assert_equal(['高橋', 0, 1, 6], actual['save'])
    assert_equal(['千賀', 0, 1, 0], actual['lose'])
    assert_equal([['1回裏', '内川', 8, 'ソロ', '岸'], ['7回裏', '柳田', 5, '２ラン', '岸']], actual['homerun'])


def test_create_dict_03():
    """
    引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
    （サヨナラゲームの解析時不具合対応 #11）
    """
    html = baseball.get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014032804.html')
    actual = baseball.create_dict(html)
    assert_equal('オリックス', actual['bat_first'])
    assert_equal('日本ハム', actual['field_first'])
    assert_equal(1, actual['match'])
    assert_equal(datetime.date(2014, 3, 28), actual['date'])
    assert_equal('札幌ドーム', actual['stadium'])
    assert_equal([
        ['2', '1', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0'],
        ['0', '1', '0', '0', '1', '0', '1', '1', '0', '1', '0', '1x'],
    ], actual['score'])
    assert_equal([5, 6], actual['total_score'])
    assert_equal(['増井', 1, 0, 0], actual['win'])
    assert_equal(['海田', 0, 1, 0], actual['lose'])
    assert_equal([['10回表', 'ペーニャ', 1, 'ソロ', '宮西']], actual['homerun'])


@raises(ParseError)
def test_create_dict_04():
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


def test_get_full_stadium_name_01():
    """
    引数に'西武ドーム'を指定したとき、'西武ドーム'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('西武ドーム')
    assert_equal('西武ドーム', actual)


def test_get_full_stadium_name_02():
    """
    引数に'コボスタ宮城'を指定したとき、'楽天Koboスタジアム宮城'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('コボスタ宮城')
    assert_equal('楽天Koboスタジアム宮城', actual)


def test_get_full_stadium_name_03():
    """
    引数に'ＱＶＣマリン'を指定したとき、'QVCマリンフィールド'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('ＱＶＣマリン')
    assert_equal('QVCマリンフィールド', actual)


def test_get_full_stadium_name_04():
    """
    引数に'ヤフオクドーム'を指定したとき、'福岡 ヤフオク!ドーム'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('ヤフオクドーム')
    assert_equal('福岡 ヤフオク!ドーム', actual)


def test_get_full_stadium_name_05():
    """
    引数に'京セラドーム大阪'を指定したとき、'京セラドーム大阪'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('京セラドーム大阪')
    assert_equal('京セラドーム大阪', actual)


def test_get_full_stadium_name_06():
    """
    引数に'札幌ドーム'を指定したとき、'札幌ドーム'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('札幌ドーム')
    assert_equal('札幌ドーム', actual)


def test_get_full_stadium_name_07():
    """
    引数に'東京ドーム'を指定したとき、'東京ドーム'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('東京ドーム')
    assert_equal('東京ドーム', actual)


def test_get_full_stadium_name_08():
    """
    引数に'甲子園'を指定したとき、'阪神甲子園球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('甲子園')
    assert_equal('阪神甲子園球場', actual)


def test_get_full_stadium_name_09():
    """
    引数に'マツダスタジアム'を指定したとき、'Mazda Zoom-Zoomスタジアム広島'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('マツダスタジアム')
    assert_equal('Mazda Zoom-Zoomスタジアム広島', actual)


def test_get_full_stadium_name_10():
    """
    引数に'ナゴヤドーム'を指定したとき、'ナゴヤドーム'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('ナゴヤドーム')
    assert_equal('ナゴヤドーム', actual)


def test_get_full_stadium_name_11():
    """
    引数に'横浜'を指定したとき、'横浜スタジアム'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('横浜')
    assert_equal('横浜スタジアム', actual)


def test_get_full_stadium_name_12():
    """
    引数に'神宮'を指定したとき、'明治神宮野球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('神宮')
    assert_equal('明治神宮野球場', actual)


def test_create_score_table_01():
    """
    引数に辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
    """
    data = {
        'bat_first': '北海道日本ハム',
        'field_first': '埼玉西武',
        'match': 4,
        'date': datetime.date(2014, 4, 29),
        'stadium': '西武ドーム',
        'score': [
            ['0', '0', '0', '0', '0', '0', '1', '0', '0'],
            ['0', '0', '1', '0', '2', '0', '0', '1', 'x'],
        ],
        'total_score': [1, 4],
        'win': ['牧田', 2, 1, 0],
        'save': ['高橋', 0, 1, 3],
        'lose': ['メンドーサ', 1, 4, 0],
        'homerun': [['7回表', '佐藤賢', 3, 'ソロ', '牧田']],
    }

    expected = textwrap.dedent("""\
        【埼玉西武 vs 北海道日本ハム 第4回戦】
        （2014年4月29日：西武ドーム）
        
        北海道日本ハム  0 0 0  0 0 0  1 0 0  1
        埼玉西武　　　  0 0 1  0 2 0  0 1 x  4
        
        [勝] 牧田　　　 2勝1敗0Ｓ
        [Ｓ] 高橋　　　 0勝1敗3Ｓ
        [敗] メンドーサ 1勝4敗0Ｓ
        
        [本塁打]
          7回表 佐藤賢  3号 ソロ （牧田）
    """)

    actual = baseball.create_score_table(data)
    assert_equal(expected, actual)


def test_create_score_table_02():
    """
    引数に辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
    （本塁打欄の整列不具合対応 #14）
    """
    data = {
        'bat_first': '埼玉西武',
        'field_first': '千葉ロッテ',
        'match': 1,
        'date': datetime.date(2014, 4, 1),
        'stadium': 'QVCマリンフィールド',
        'score': [
            ['0', '0', '2', '0', '0', '1', '0', '1', '2'],
            ['1', '0', '0', '0', '0', '0', '0', '1', '0'],
        ],
        'total_score': [6, 2],
        'win': ['牧田', 1, 0, 0],
        'lose': ['涌井', 0, 1, 0],
        'homerun': [['8回表', 'ランサム', 1, 'ソロ', '吉原'], ['9回表', '浅村', 2, '２ラン', '吉原']],
    }

    expected = textwrap.dedent("""\
        【千葉ロッテ vs 埼玉西武 第1回戦】
        （2014年4月1日：QVCマリンフィールド）
        
        埼玉西武　  0 0 2  0 0 1  0 1 2  6
        千葉ロッテ  1 0 0  0 0 0  0 1 0  2
        
        [勝] 牧田 1勝0敗0Ｓ
        [敗] 涌井 0勝1敗0Ｓ
        
        [本塁打]
          8回表 ランサム  1号 ソロ　 （吉原）
          9回表 浅村　　  2号 ２ラン （吉原）
    """)

    actual = baseball.create_score_table(data)
    assert_equal(expected, actual)


def test_create_score_table_03():
    """
    引数に辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
    （サヨナラゲームの解析時不具合対応 #11）
    """
    data = {
        'bat_first': 'オリックス',
        'field_first': '北海道日本ハム',
        'match': 1,
        'date': datetime.date(2014, 3, 28),
        'stadium': '札幌ドーム',
        'score': [
            ['2', '1', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0'],
            ['0', '1', '0', '0', '1', '0', '1', '1', '0', '1', '0', '1x'],
        ],
        'total_score': [5, 6],
        'win': ['増井', 1, 0, 0],
        'lose': ['海田', 0, 1, 0],
        'homerun': [['10回表', 'ペーニャ', 1, 'ソロ', '宮西']]
    }

    expected = textwrap.dedent("""\
        【北海道日本ハム vs オリックス 第1回戦】
        （2014年3月28日：札幌ドーム）
        
        オリックス　　  2 1 0  0 0 0  0 0 1  1 0 0   5
        北海道日本ハム  0 1 0  0 1 0  1 1 0  1 0 1x  6
        
        [勝] 増井 1勝0敗0Ｓ
        [敗] 海田 0勝1敗0Ｓ
        
        [本塁打]
          10回表 ペーニャ  1号 ソロ （宮西）
    """)

    actual = baseball.create_score_table(data)
    assert_equal(expected, actual)


def test_create_score_table_04():
    """
    引数に辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
    （2桁得点時不具合対応 #15）
    """
    data = {
        'bat_first': '埼玉西武',
        'field_first': '東北楽天',
        'match': 10,
        'date': datetime.date(2014, 5, 18),
        'stadium': '岩手県営野球場',
        'score': [
            ['1', '4', '1', '2', '0', '1', '0', '3', '0'],
            ['1', '0', '0', '0', '0', '0', '1', '0', '0'],
        ],
        'total_score': [12, 2],
        'win': ['十亀', 2, 2, 3],
        'lose': ['塩見', 2, 4, 0],
        'homerun': [
            ['2回表', '浅村', 6, '２ラン', '塩見'],
            ['3回表', '浅村', 7, 'ソロ', '塩見'],
            ['4回表', '山崎', 1, '２ラン', '塩見'],
        ],
    }

    expected = textwrap.dedent("""\
        【東北楽天 vs 埼玉西武 第10回戦】
        （2014年5月18日：岩手県営野球場）
        
        埼玉西武  1 4 1  2 0 1  0 3 0  12
        東北楽天  1 0 0  0 0 0  1 0 0   2
        
        [勝] 十亀 2勝2敗3Ｓ
        [敗] 塩見 2勝4敗0Ｓ
        
        [本塁打]
          2回表 浅村  6号 ２ラン （塩見）
          3回表 浅村  7号 ソロ　 （塩見）
          4回表 山崎  1号 ２ラン （塩見）
    """)

    actual = baseball.create_score_table(data)
    assert_equal(expected, actual)


def test_get_score_table():
    """
    引数に有効なURLを指定したとき、スコアテーブルの文字列を返すことを確認する。
    """
    expected = textwrap.dedent("""\
        【千葉ロッテ vs 埼玉西武 第6回戦】
        （2014年5月2日：QVCマリンフィールド）
        
        埼玉西武　  0 2 0  0 0 0  0 0 0  2
        千葉ロッテ  0 0 0  0 0 0  0 0 0  0
        
        [勝] 岸　 3勝2敗0Ｓ
        [敗] 成瀬 3勝2敗0Ｓ
    """)

    actual = baseball.get_score_table('http://www.nikkansports.com/baseball/professional/score/2014/pl2014050203.html')
    assert_equal(expected, actual)


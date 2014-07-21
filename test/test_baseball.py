# -*- coding: utf-8 -*-

import datetime
import textwrap

from mock import Mock
from mock import patch

from nose.tools import *

from nikkansports import baseball
from nikkansports.exception import InvalidDateError, InvalidTeamError, ParseError, ResultNotFoundError


RETURN_VALUE_FOR_GET_URL = """\
<div class="dataContents">
    <table border="1" summary="プロ野球の対戦表">
        <tr>
            <th colspan="3" class="bg">対戦</th>
            <th>開始</th>
        </tr>
        <tr>
            <td class="line home">
                <a href="http://www.nikkansports.com/baseball/professional/team/fighters/top-fighters.html">日本ハム</a>
            </td>
            <td class="line score">
                <a href="http://www.nikkansports.com">－</a>
            </td>
            <td class="line away">
                <a href="http://www.nikkansports.com/baseball/professional/team/swallows/top-swallows.html">ヤクルト</a>
            </td>
            <td class="num">18:00</td>
        </tr>
        <tr>
            <td class="line home">
                <a href="http://www.nikkansports.com/baseball/professional/team/eagles/top-eagles.html">楽天</a>
            </td>
            <td class="line score">
                <a href="http://www.nikkansports.com/baseball/professional/score/2014/il2014061402.html">0－3</a>
            </td>
            <td class="line away">
                <a href="http://www.nikkansports.com/baseball/professional/team/giants/top-giants.html">巨人</a>
            </td>
            <td class="num">8回裏</td>
        </tr>
        <tr>
            <td class="line home">
                <a href="http://www.nikkansports.com/baseball/professional/team/lions/top-lions.html">西武</a>
            </td>
            <td class="line score">
                <a href="http://www.nikkansports.com/baseball/professional/score/2014/il2014061403.html">3－2</a>
            </td>
            <td class="line away">
                <a href="http://www.nikkansports.com/baseball/professional/team/tigers/top-tigers.html">阪神</a>
            </td>
            <td class="num">終了</td>
        </tr>
        <tr>
            <td class="line home">
                <a href="http://www.nikkansports.com/baseball/professional/team/marines/top-marines.html">ロッテ</a>
            </td>
            <td class="line score">
                <a href="http://www.nikkansports.com/baseball/professional/score/2014/il2014061404.html">6－4</a>
            </td>
            <td class="line away">
                <a href="http://www.nikkansports.com/baseball/professional/team/carp/top-carp.html">広島</a>
            </td>
            <td class="num">8回裏</td>
        </tr>
        <tr>
            <td class="line home">
                <a href="http://www.nikkansports.com/baseball/professional/team/buffaloes/top-buffaloes.html">オリック</a>
            </td>
            <td class="line score">
                <a href="http://www.nikkansports.com/baseball/professional/score/2014/il2014061405.html">7－4</a>
            </td>
            <td class="line away">
                <a href="http://www.nikkansports.com/baseball/professional/team/dragons/top-dragons.html">中日</a>
            </td>
            <td class="num">終了</td>
        </tr>
        <tr>
            <td class="line home">
                <a href="http://www.nikkansports.com/baseball/professional/team/hawks/top-hawks.html">ソフトバ</a>
            </td>
            <td class="line score">
                <a href="http://www.nikkansports.com/baseball/professional/score/2014/il2014061406.html">4－2</a>
            </td>
            <td class="line away">
                <a href="http://www.nikkansports.com/baseball/professional/team/baystars/top-baystars.html">ＤｅＮＡ</a>
            </td>
            <td class="num">8回裏</td>
        </tr>
    </table>
</div>
"""


@patch('nikkansports.baseball.get_html')
def test_get_url_01(get_html):
    """
    引数に'l'を指定したとき、埼玉西武の試合のURLを返すことを確認する。
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    actual = baseball.get_url('l')
    assert_equal('http://www.nikkansports.com/baseball/professional/score/2014/il2014061403.html', actual)


@patch('nikkansports.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_url_02(get_html):
    """
    引数に'e'を指定したとき、ResultNotFoundErrorがraiseされることを確認する。
    (東北楽天が試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    actual = baseball.get_url('e')


@patch('nikkansports.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_url_03(get_html):
    """
    引数に'm'を指定したとき、ResultNotFoundErrorがraiseされることを確認する。
    (千葉ロッテが試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    actual = baseball.get_url('m')


@patch('nikkansports.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_url_04(get_html):
    """
    引数に'h'を指定したとき、ResultNotFoundErrorがraiseされることを確認する。
    (福岡ソフトバンクが試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    actual = baseball.get_url('h')


@patch('nikkansports.baseball.get_html')
def test_get_url_05(get_html):
    """
    引数に'bu'を指定したとき、オリックスの試合のURLを返すことを確認する。
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    actual = baseball.get_url('bu')
    assert_equal('http://www.nikkansports.com/baseball/professional/score/2014/il2014061405.html', actual)


@patch('nikkansports.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_url_06(get_html):
    """
    引数に'f'を指定したとき、ResultNotFoundErrorがraiseされることを確認する。
    (北海道日本ハムが試合開始前のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    actual = baseball.get_url('f')


@patch('nikkansports.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_url_07(get_html):
    """
    引数に'g'を指定したとき、ResultNotFoundErrorがraiseされることを確認する。
    (読売が試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    actual = baseball.get_url('g')


@patch('nikkansports.baseball.get_html')
def test_get_url_08(get_html):
    """
    引数に't'を指定したとき、阪神の試合のURLを返すことを確認する。
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    actual = baseball.get_url('t')
    assert_equal('http://www.nikkansports.com/baseball/professional/score/2014/il2014061403.html', actual)


@patch('nikkansports.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_url_09(get_html):
    """
    引数に'c'を指定したとき、ResultNotFoundErrorがraiseされることを確認する。
    (広島東洋が試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    actual = baseball.get_url('c')


@patch('nikkansports.baseball.get_html')
def test_get_url_10(get_html):
    """
    引数に'd'を指定したとき、中日の試合のURLを返すことを確認する。
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    actual = baseball.get_url('d')
    assert_equal('http://www.nikkansports.com/baseball/professional/score/2014/il2014061405.html', actual)


@patch('nikkansports.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_url_11(get_html):
    """
    引数に'bs'を指定したとき、ResultNotFoundErrorがraiseされることを確認する。
    (横浜ＤｅＮＡが試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    actual = baseball.get_url('bs')


@patch('nikkansports.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_url_12(get_html):
    """
    引数に's'を指定したとき、ResultNotFoundErrorがraiseされることを確認する。
    (東京ヤクルトが試合開始前のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    actual = baseball.get_url('s')


@raises(InvalidTeamError)
def test_get_url_13():
    """
    引数に無効なチーム名を指定したとき、InvalidTeamErrorがraiseされることを確認する。
    """
    actual = baseball.get_url('q')


def test_parse_date_01():
    """
    引数に何も指定しなかったとき、システム日付の年、月を返すことを確認する。
    """
    year, month = baseball.parse_date()
    assert_equal('2014', year)
    assert_equal('07', month)


def test_parse_date_02():
    """
    引数に2桁の文字列を指定したとき、システム日付の年、指定された月を返すことを確認する。
    """
    year, month = baseball.parse_date('08')
    assert_equal('2014', year)
    assert_equal('08', month)


@raises(InvalidDateError)
def test_parse_date_03():
    """
    引数に無効な2桁の文字列を指定したとき、InvalidDateErrorがraiseされることを確認する。
    """
    year, month = baseball.parse_date('13')


@raises(InvalidDateError)
def test_parse_date_04():
    """
    引数に無効な2桁の文字列を指定したとき、InvalidDateErrorがraiseされることを確認する。
    """
    year, month = baseball.parse_date('LL')


def test_parse_date_05():
    """
    引数に4桁の文字列を指定したとき、指定された年、指定された月を返すことを確認する。
    """
    year, month = baseball.parse_date('1306')
    assert_equal('2013', year)
    assert_equal('06', month)


@raises(InvalidDateError)
def test_parse_date_06():
    """
    引数に無効な4桁の文字列を指定したとき、InvalidDateErrorがraiseされることを確認する。
    """
    year, month = baseball.parse_date('1313')


@raises(InvalidDateError)
def test_parse_date_07():
    """
    引数に無効な4桁の文字列を指定したとき、InvalidDateErrorがraiseされることを確認する。
    """
    year, month = baseball.parse_date('Lism')


def test_parse_date_08():
    """
    引数に6桁の文字列を指定したとき、指定された年、指定された月を返すことを確認する。
    """
    year, month = baseball.parse_date('201510')
    assert_equal('2015', year)
    assert_equal('10', month)


@raises(InvalidDateError)
def test_parse_date_09():
    """
    引数に無効な6桁の文字列を指定したとき、InvalidDateErrorがraiseされることを確認する。
    """
    year, month = baseball.parse_date('201313')


@raises(InvalidDateError)
def test_parse_date_10():
    """
    引数に無効な6桁の文字列を指定したとき、InvalidDateErrorがraiseされることを確認する。
    """
    year, month = baseball.parse_date('Python')


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


def test_get_full_team_name_13():
    """
    引数に'ほっともっと神戸'を指定したとき、'ほっともっとフィールド神戸'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('ほっともっと神戸')
    assert_equal('ほっともっとフィールド神戸', actual)


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


def test_create_score_table_05():
    """
    引数に辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
    （延長戦本塁打不具合対応 #23）
    """
    data = {
        'bat_first': '埼玉西武',
        'field_first': '横浜ＤｅＮＡ',
        'match': 3,
        'date': datetime.date(2014, 6, 21),
        'stadium': '横浜スタジアム',
        'score': [
            ['2', '0', '0', '0', '0', '0', '0', '3', '1', '1'],
            ['0', '0', '0', '1', '0', '4', '0', '1', '0', '2x'],
        ],
        'total_score': [7, 8],
        'win': ['林', 1, 0, 0],
        'lose': ['ウィリアムス', 1, 2, 0],
        'homerun': [
            ['1回表', 'メヒア', 6, '２ラン', 'モスコーソ'],
            ['4回裏', 'グリエル', 2, 'ソロ', '岸'],
            ['6回裏', '後藤', 3, 'ソロ', '岸'],
            ['6回裏', '多村', 1, '２ラン', '岸'],
            ['8回表', '木村', 8, '３ラン', 'ソーサ'],
            ['10回表', '脇谷', 1, 'ソロ', '加賀'],
        ],
    }

    expected = textwrap.dedent("""\
        【横浜ＤｅＮＡ vs 埼玉西武 第3回戦】
        （2014年6月21日：横浜スタジアム）
        
        埼玉西武　　  2 0 0  0 0 0  0 3 1  1   7
        横浜ＤｅＮＡ  0 0 0  1 0 4  0 1 0  2x  8
        
        [勝] 林　　　　　 1勝0敗0Ｓ
        [敗] ウィリアムス 1勝2敗0Ｓ
        
        [本塁打]
           1回表 メヒア　  6号 ２ラン （モスコーソ）
           4回裏 グリエル  2号 ソロ　 （岸）
           6回裏 後藤　　  3号 ソロ　 （岸）
           6回裏 多村　　  1号 ２ラン （岸）
           8回表 木村　　  8号 ３ラン （ソーサ）
          10回表 脇谷　　  1号 ソロ　 （加賀）
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


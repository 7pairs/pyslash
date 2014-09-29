# -*- coding: utf-8 -*-

import datetime
import textwrap

from mock import patch

from nose.tools import *

from crawler import baseball
from crawler.exception import InvalidDateError, InvalidTeamError, ParseError, ResultNotFoundError


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


@patch('crawler.baseball.get_html')
def test_get_url_01(get_html):
    """
    引数に'l'を指定したとき、埼玉西武の試合のURLを返すことを確認する。
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    actual = baseball.get_today_game_url('l')
    assert_equal('http://www.nikkansports.com/baseball/professional/score/2014/il2014061403.html', actual)


@patch('crawler.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_url_02(get_html):
    """
    引数に'e'を指定したとき、ResultNotFoundErrorがraiseされることを確認する。
    (東北楽天が試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    baseball.get_today_game_url('e')


@patch('crawler.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_url_03(get_html):
    """
    引数に'm'を指定したとき、ResultNotFoundErrorがraiseされることを確認する。
    (千葉ロッテが試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    baseball.get_today_game_url('m')


@patch('crawler.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_url_04(get_html):
    """
    引数に'h'を指定したとき、ResultNotFoundErrorがraiseされることを確認する。
    (福岡ソフトバンクが試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    baseball.get_today_game_url('h')


@patch('crawler.baseball.get_html')
def test_get_url_05(get_html):
    """
    引数に'bu'を指定したとき、オリックスの試合のURLを返すことを確認する。
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    actual = baseball.get_today_game_url('bu')
    assert_equal('http://www.nikkansports.com/baseball/professional/score/2014/il2014061405.html', actual)


@patch('crawler.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_url_06(get_html):
    """
    引数に'f'を指定したとき、ResultNotFoundErrorがraiseされることを確認する。
    (北海道日本ハムが試合開始前のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    baseball.get_today_game_url('f')


@patch('crawler.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_url_07(get_html):
    """
    引数に'g'を指定したとき、ResultNotFoundErrorがraiseされることを確認する。
    (読売が試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    baseball.get_today_game_url('g')


@patch('crawler.baseball.get_html')
def test_get_url_08(get_html):
    """
    引数に't'を指定したとき、阪神の試合のURLを返すことを確認する。
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    actual = baseball.get_today_game_url('t')
    assert_equal('http://www.nikkansports.com/baseball/professional/score/2014/il2014061403.html', actual)


@patch('crawler.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_url_09(get_html):
    """
    引数に'c'を指定したとき、ResultNotFoundErrorがraiseされることを確認する。
    (広島東洋が試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    baseball.get_today_game_url('c')


@patch('crawler.baseball.get_html')
def test_get_url_10(get_html):
    """
    引数に'd'を指定したとき、中日の試合のURLを返すことを確認する。
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    actual = baseball.get_today_game_url('d')
    assert_equal('http://www.nikkansports.com/baseball/professional/score/2014/il2014061405.html', actual)


@patch('crawler.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_url_11(get_html):
    """
    引数に'bs'を指定したとき、ResultNotFoundErrorがraiseされることを確認する。
    (横浜ＤｅＮＡが試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    baseball.get_today_game_url('bs')


@patch('crawler.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_url_12(get_html):
    """
    引数に's'を指定したとき、ResultNotFoundErrorがraiseされることを確認する。
    (東京ヤクルトが試合開始前のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_URL
    baseball.get_today_game_url('s')


@raises(InvalidTeamError)
def test_get_url_13():
    """
    引数に無効なチーム名を指定したとき、InvalidTeamErrorがraiseされることを確認する。
    """
    baseball.get_today_game_url('q')


def test_get_date_01():
    """
    引数にスコアテーブルのURLを指定したとき、試合日を返すことを確認する。
    """
    actual = baseball.parse_date('http://www.nikkansports.com/baseball/professional/score/2014/pl2014050203.html')
    assert_equal(datetime.date(2014, 5, 2), actual)


@raises(InvalidDateError)
def test_get_date_02():
    """
    引数に無効なURLを指定したとき、InvalidDateErrorがraiseされることを確認する。
    """
    baseball.parse_date('http://www.konami.jp/am/qma/character_s/')


def test_get_calendar_url_01():
    """
    引数に正しいチーム名を指定したとき、カレンダーのURLを返すことを確認する。
    """
    actual = baseball.get_calendar_url('l', datetime.datetime.strptime('20140401', '%Y%m%d'))
    assert_equal('http://www.nikkansports.com/baseball/professional/schedule/2014/l201404.html', actual)


@raises(InvalidTeamError)
def test_get_calender_url_02():
    """
    引数に無効なチーム名を指定したとき、InvalidTeamErrorがraiseされることを確認する。
    """
    baseball.get_calendar_url('q', datetime.datetime.strptime('20140401', '%Y%m%d'))


def test_get_game_url_01():
    """
    引数に有効なチーム名、日付を指定したとき、スコアテーブルのURLを返すことを確認する。
    """
    actual = baseball.get_game_url('l', datetime.date(2014, 5, 2))
    assert_equal('http://www.nikkansports.com/baseball/professional/score/2014/pl2014050203.html', actual)


@raises(InvalidTeamError)
def test_get_game_url_02():
    """
    引数に無効なチーム名を指定したとき、InvalidTeamErrorがraiseされることを確認する。
    """
    baseball.get_calendar_url('q', datetime.date(2014, 5, 2))


def test_get_html_01():
    """
    引数に有効なURLを指定したとき、そのURLのHTMLの内容を文字列として返すことを確認する。
    """
    html = baseball.get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014050203.html')
    actual = ('<title>プロ野球スコア速報 ロッテ対西武 : nikkansports.com</title>' in html)
    assert_equal(True, actual)


@raises(ValueError)
def test_get_html_02():
    """
    引数に無効なURLを指定したとき、ValueErrorが発生することを確認する。
    """
    html = baseball.get_html('エラーアルよー')
    assert_equal('', html)


def test_create_dict_01():
    """
    引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
    """
    html = baseball.get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014042905.html')
    actual = baseball.parse_score_table(html)
    assert_equal('日本ハム', actual['bat_first'])
    assert_equal('西武', actual['field_first'])
    assert_equal(4, actual['match'])
    assert_equal('西武ドーム', actual['stadium'])
    assert_equal([
        ['0', '0', '0', '0', '0', '0', '1', '0', '0'],
        ['0', '0', '1', '0', '2', '0', '0', '1', 'x'],
    ], actual['score'])
    assert_equal([1, 4], actual['total_score'])
    assert_equal(('牧田', 2, 1, 0), actual['win'])
    assert_equal(('高橋', 0, 1, 3), actual['save'])
    assert_equal(('メンドーサ', 1, 4, 0), actual['lose'])
    assert_equal([('7回表', '佐藤賢', 3, 'ソロ', '牧田')], actual['homerun'])


def test_create_dict_02():
    """
    引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
    （2ラン、3ランの解析時不具合対応 #13）
    """
    html = baseball.get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014050906.html')
    actual = baseball.parse_score_table(html)
    assert_equal('西武', actual['bat_first'])
    assert_equal('ソフトバンク', actual['field_first'])
    assert_equal(7, actual['match'])
    assert_equal('北九州', actual['stadium'])
    assert_equal([
        ['0', '1', '0', '3', '0', '0', '0', '0', '2'],
        ['1', '1', '0', '0', '0', '0', '2', '0', '0'],
    ], actual['score'])
    assert_equal([6, 4], actual['total_score'])
    assert_equal(('ウィリアムス', 1, 0, 0), actual['win'])
    assert_equal(('高橋', 0, 1, 6), actual['save'])
    assert_equal(('千賀', 0, 1, 0), actual['lose'])
    assert_equal([('1回裏', '内川', 8, 'ソロ', '岸'), ('7回裏', '柳田', 5, '２ラン', '岸')], actual['homerun'])


def test_create_dict_03():
    """
    引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
    （サヨナラゲームの解析時不具合対応 #11）
    """
    html = baseball.get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014032804.html')
    actual = baseball.parse_score_table(html)
    assert_equal('オリックス', actual['bat_first'])
    assert_equal('日本ハム', actual['field_first'])
    assert_equal(1, actual['match'])
    assert_equal('札幌ドーム', actual['stadium'])
    assert_equal([
        ['2', '1', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0'],
        ['0', '1', '0', '0', '1', '0', '1', '1', '0', '1', '0', '1x'],
    ], actual['score'])
    assert_equal([5, 6], actual['total_score'])
    assert_equal(('増井', 1, 0, 0), actual['win'])
    assert_equal(('海田', 0, 1, 0), actual['lose'])
    assert_equal([('10回表', 'ペーニャ', 1, 'ソロ', '宮西')], actual['homerun'])


def test_create_dict_04():
    """
    引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
    （打者一巡時の本塁打欄不具合対応 #45）
    """
    html = baseball.get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014081605.html')
    actual = baseball.parse_score_table(html)
    assert_equal('日本ハム', actual['bat_first'])
    assert_equal('西武', actual['field_first'])
    assert_equal(15, actual['match'])
    assert_equal('西武ドーム', actual['stadium'])
    assert_equal([
        ['0', '0', '0', '0', '1', '4', '0', '1', '1', '1', '0', '0'],
        ['0', '0', '0', '0', '6', '0', '0', '1', '0', '1', '0', '0'],
    ], actual['score'])
    assert_equal([8, 8], actual['total_score'])
    assert_equal([
        ('5回裏', '中村', 21, '２ラン', '吉川'),
        ('10回表', '陽', 16, 'ソロ', '中郷'),
        ('10回裏', '森', 3, 'ソロ', '増井'),
    ], actual['homerun'])


def test_create_dict_05():
    """
    引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
    （コールド時のスコア不具合対応 #50）
    """
    html = baseball.get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014090802.html')
    actual = baseball.parse_score_table(html)
    assert_equal('西武', actual['bat_first'])
    assert_equal('ロッテ', actual['field_first'])
    assert_equal(21, actual['match'])
    assert_equal('ＱＶＣマリン', actual['stadium'])
    assert_equal([
        ['3', '0', '0', '1', '2', '1', '0x'],
        ['0', '0', '0', '0', '0', '0', ''],
    ], actual['score'])
    assert_equal([7, 0], actual['total_score'])
    assert_equal([
        ('1回表', '中村', 30, 'ソロ', '藤岡'),
    ], actual['homerun'])


@raises(ParseError)
def test_create_dict_06():
    """
    引数に無効なHTML文字列を指定したとき、ParseErrorが発生することを確認する。
    """
    with open('./test/test_create_dict_error.html') as test_file:
        html = test_file.read()
    baseball.parse_score_table(html)


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


def test_get_full_stadium_name_13():
    """
    引数に'ほっともっと神戸'を指定したとき、'ほっともっとフィールド神戸'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('ほっともっと神戸')
    assert_equal('ほっともっとフィールド神戸', actual)


def test_get_full_stadium_name_14():
    """
    引数に'大宮'を指定したとき、'埼玉県営大宮公園野球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('大宮')
    assert_equal('埼玉県営大宮公園野球場', actual)


def test_get_full_stadium_name_15():
    """
    引数に'静岡'を指定したとき、'静岡県草薙総合運動場硬式野球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('静岡')
    assert_equal('静岡県草薙総合運動場硬式野球場', actual)


def test_get_full_stadium_name_16():
    """
    引数に'サンマリン宮崎'を指定したとき、'サンマリンスタジアム宮崎'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('サンマリン宮崎')
    assert_equal('サンマリンスタジアム宮崎', actual)


def test_get_full_stadium_name_17():
    """
    引数に'鹿児島'を指定したとき、'鹿児島県立鴨池野球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('鹿児島')
    assert_equal('鹿児島県立鴨池野球場', actual)


def test_get_full_stadium_name_18():
    """
    引数に'北九州'を指定したとき、'北九州市民球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('北九州')
    assert_equal('北九州市民球場', actual)
    

def test_get_full_stadium_name_19():
    """
    引数に'函館'を指定したとき、'オーシャンスタジアム'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('函館')
    assert_equal('オーシャンスタジアム', actual)


def test_get_full_stadium_name_20():
    """
    引数に'函館'を指定したとき、'オーシャンスタジアム'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('函館')
    assert_equal('オーシャンスタジアム', actual)


def test_get_full_stadium_name_21():
    """
    引数に'いわき'を指定したとき、'いわきグリーンスタジアム'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('いわき')
    assert_equal('いわきグリーンスタジアム', actual)


def test_get_full_stadium_name_22():
    """
    引数に'どらドラパーク米子'を指定したとき、'どらドラパーク米子市民球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('どらドラパーク米子')
    assert_equal('どらドラパーク米子市民球場', actual)


def test_get_full_stadium_name_23():
    """
    引数に'バッティングパレス相石ひらつか'を指定したとき、'バッティングパレス相石スタジアムひらつか'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('バッティングパレス相石ひらつか')
    assert_equal('バッティングパレス相石スタジアムひらつか', actual)


def test_get_full_stadium_name_24():
    """
    引数に'ひたちなか'を指定したとき、'ひたちなか市民球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('ひたちなか')
    assert_equal('ひたちなか市民球場', actual)


def test_get_full_stadium_name_25():
    """
    引数に'秋田'を指定したとき、'こまちスタジアム'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('秋田')
    assert_equal('こまちスタジアム', actual)


def test_get_full_stadium_name_26():
    """
    引数に'盛岡'を指定したとき、'岩手県営野球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('盛岡')
    assert_equal('岩手県営野球場', actual)


def test_get_full_stadium_name_27():
    """
    引数に'三次'を指定したとき、'三次きんさいスタジアム'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('三次')
    assert_equal('三次きんさいスタジアム', actual)


def test_get_full_stadium_name_28():
    """
    引数に'呉'を指定したとき、'呉市二河野球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('呉')
    assert_equal('呉市二河野球場', actual)


def test_get_full_stadium_name_29():
    """
    引数に'郡山'を指定したとき、'郡山総合運動場開成山野球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('郡山')
    assert_equal('郡山総合運動場開成山野球場', actual)


def test_get_full_stadium_name_30():
    """
    引数に'浜松'を指定したとき、'浜松球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('浜松')
    assert_equal('浜松球場', actual)


def test_get_full_stadium_name_31():
    """
    引数に'倉敷'を指定したとき、'マスカットスタジアム'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('倉敷')
    assert_equal('マスカットスタジアム', actual)


def test_get_full_stadium_name_32():
    """
    引数に'金沢'を指定したとき、'石川県立野球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('金沢')
    assert_equal('石川県立野球場', actual)


def test_get_full_stadium_name_33():
    """
    引数に'富山'を指定したとき、'富山市民球場アルペンスタジアム'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('富山')
    assert_equal('富山市民球場アルペンスタジアム', actual)


def test_get_full_stadium_name_34():
    """
    引数に'沖縄セルラー那覇'を指定したとき、'沖縄セルラースタジアム那覇'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('沖縄セルラー那覇')
    assert_equal('沖縄セルラースタジアム那覇', actual)


def test_get_full_stadium_name_35():
    """
    引数に'旭川'を指定したとき、'スタルヒン球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('旭川')
    assert_equal('スタルヒン球場', actual)


def test_get_full_stadium_name_36():
    """
    引数に'荘内銀行・日新製薬スタジアム'を指定したとき、'荘内銀行・日新製薬スタジアムやまがた'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('荘内銀行・日新製薬スタジアム')
    assert_equal('荘内銀行・日新製薬スタジアムやまがた', actual)


def test_get_full_stadium_name_37():
    """
    引数に'帯広'を指定したとき、'帯広の森野球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('帯広')
    assert_equal('帯広の森野球場', actual)


def test_get_full_stadium_name_38():
    """
    引数に'豊橋'を指定したとき、'豊橋市民球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('豊橋')
    assert_equal('豊橋市民球場', actual)


def test_get_full_stadium_name_39():
    """
    引数に'ハードオフ新潟'を指定したとき、'HARD OFF ECOスタジアム新潟'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('ハードオフ新潟')
    assert_equal('HARD OFF ECOスタジアム新潟', actual)


def test_get_full_stadium_name_40():
    """
    引数に'熊本'を指定したとき、'藤崎台県営野球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('熊本')
    assert_equal('藤崎台県営野球場', actual)


def test_get_full_stadium_name_41():
    """
    引数に'岐阜'を指定したとき、'長良川球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('岐阜')
    assert_equal('長良川球場', actual)


def test_get_full_stadium_name_42():
    """
    引数に'松山'を指定したとき、'坊っちゃんスタジアム'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('松山')
    assert_equal('坊っちゃんスタジアム', actual)


def test_get_full_stadium_name_43():
    """
    引数に'長野'を指定したとき、'長野オリンピックスタジアム'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('長野')
    assert_equal('長野オリンピックスタジアム', actual)


def test_get_full_stadium_name_44():
    """
    引数に'上毛敷島'を指定したとき、'上毛新聞敷島球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('上毛敷島')
    assert_equal('上毛新聞敷島球場', actual)


def test_get_full_stadium_name_45():
    """
    引数に'宇都宮'を指定したとき、'宇都宮清原球場'を返すことを確認する。
    """
    actual = baseball.get_full_stadium_name('宇都宮')
    assert_equal('宇都宮清原球場', actual)


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
        'win': ('牧田', 2, 1, 0),
        'save': ('高橋', 0, 1, 3),
        'lose': ('メンドーサ', 1, 4, 0),
        'homerun': [('7回表', '佐藤賢', 3, 'ソロ', '牧田')],
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
        'win': ('牧田', 1, 0, 0),
        'lose': ('涌井', 0, 1, 0),
        'homerun': [('8回表', 'ランサム', 1, 'ソロ', '吉原'), ('9回表', '浅村', 2, '２ラン', '吉原')],
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
        'win': ('増井', 1, 0, 0),
        'lose': ('海田', 0, 1, 0),
        'homerun': [('10回表', 'ペーニャ', 1, 'ソロ', '宮西')]
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
        'win': ('十亀', 2, 2, 3),
        'lose': ('塩見', 2, 4, 0),
        'homerun': [
            ('2回表', '浅村', 6, '２ラン', '塩見'),
            ('3回表', '浅村', 7, 'ソロ', '塩見'),
            ('4回表', '山崎', 1, '２ラン', '塩見'),
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
        'win': ('林', 1, 0, 0),
        'lose': ('ウィリアムス', 1, 2, 0),
        'homerun': [
            ('1回表', 'メヒア', 6, '２ラン', 'モスコーソ'),
            ('4回裏', 'グリエル', 2, 'ソロ', '岸'),
            ('6回裏', '後藤', 3, 'ソロ', '岸'),
            ('6回裏', '多村', 1, '２ラン', '岸'),
            ('8回表', '木村', 8, '３ラン', 'ソーサ'),
            ('10回表', '脇谷', 1, 'ソロ', '加賀'),
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


def test_create_score_table_06():
    """
    引数に辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
    （延長戦時の空行不具合対応 #44）
    """
    data = {
        'bat_first': '北海道日本ハム',
        'field_first': '埼玉西武',
        'match': 15,
        'date': datetime.date(2014, 8, 16),
        'stadium': '西武ドーム',
        'score': [
            ['0', '0', '0', '0', '1', '4', '0', '1', '1', '1', '0', '0'],
            ['0', '0', '0', '0', '6', '0', '0', '1', '0', '1', '0', '0'],
        ],
        'total_score': [8, 8],
        'homerun': [
            ('5回裏', '中村', 21, '２ラン', '吉川'),
            ('10回表', '陽', 16, 'ソロ', '中郷'),
            ('10回裏', '森', 3, 'ソロ', '増井'),
        ],
    }

    expected = textwrap.dedent("""\
        【埼玉西武 vs 北海道日本ハム 第15回戦】
        （2014年8月16日：西武ドーム）
        
        北海道日本ハム  0 0 0  0 1 4  0 1 1  1 0 0  8
        埼玉西武　　　  0 0 0  0 6 0  0 1 0  1 0 0  8
        
        [本塁打]
           5回裏 中村 21号 ２ラン （吉川）
          10回表 陽　 16号 ソロ　 （中郷）
          10回裏 森　  3号 ソロ　 （増井）
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

    actual = baseball.get_score_table_by_url('http://www.nikkansports.com/baseball/professional/score/2014/pl2014050203.html')
    assert_equal(expected, actual)


def test_get_score_table_by_param():
    """
    引数に有効なチーム、日付を指定したとき、スコアテーブルの文字列を返すことを確認する。
    """
    expected = textwrap.dedent("""\
        【千葉ロッテ vs 埼玉西武 第6回戦】
        （2014年5月2日：QVCマリンフィールド）

        埼玉西武　  0 2 0  0 0 0  0 0 0  2
        千葉ロッテ  0 0 0  0 0 0  0 0 0  0

        [勝] 岸　 3勝2敗0Ｓ
        [敗] 成瀬 3勝2敗0Ｓ
    """)

    actual = baseball.get_score_table('l', datetime.datetime.strptime('20140502', '%Y%m%d'))
    assert_equal(expected, actual)

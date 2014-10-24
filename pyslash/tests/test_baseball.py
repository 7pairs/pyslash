# -*- coding: utf-8 -*-

import datetime
import textwrap

from bs4 import BeautifulSoup
from mock import patch
from nose import tools
from nose.tools import raises

from pyslash.crawler import baseball
from pyslash.crawler.exception import InvalidTeamError, ParseError, ResultNotFoundError


RETURN_VALUE_FOR_GET_HTML = """\
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


def test_get_score_table_01():
    """
    get_score_table()：引数に有効なチーム、試合日を指定したとき、スコアテーブルの文字列を返すことを確認する。
    """
    expected = textwrap.dedent("""\
        【千葉ロッテ vs 埼玉西武 第6回戦】
        （2014年5月2日：QVCマリンフィールド）

        埼玉西武　  0 2 0  0 0 0  0 0 0  2
        千葉ロッテ  0 0 0  0 0 0  0 0 0  0

        [勝] 岸　 3勝2敗0Ｓ
        [敗] 成瀬 3勝2敗0Ｓ
    """)
    result = baseball.get_score_table('l', datetime.datetime(2014, 5, 2))
    tools.assert_equal(expected, result)


@patch('pyslash.crawler.baseball.get_today_game_url')
def test_get_score_table_02(get_today_game_url):
    """
    get_score_table()：試合日にNoneを指定したとき、当日の試合のスコアテーブルの文字列を返すことを確認する。
    """
    get_today_game_url.return_value = 'http://www.nikkansports.com/baseball/professional/score/2014/il2014061403.html'
    expected = textwrap.dedent("""\
        【埼玉西武 vs 阪神 第3回戦】
        （2014年6月14日：西武ドーム）

        阪神　　  1 0 0  0 0 1  0 0 0  2
        埼玉西武  0 2 0  0 0 1  0 0 x  3

        [勝] 菊池 3勝6敗0Ｓ
        [Ｓ] 高橋 0勝1敗12Ｓ
        [敗] 能見 5勝5敗0Ｓ

        [本塁打]
          2回裏 木村　　  6号 ２ラン （能見）
          6回表 マートン  8号 ソロ　 （菊池）
    """)
    result = baseball.get_score_table('l', None)
    tools.assert_equal(expected, result)


@raises(InvalidTeamError)
def test_get_score_table_03():
    """
    get_score_table()：引数に無効なチームを指定したとき、InvalidTeamErrorが送出されることを確認する。
    """
    baseball.get_score_table('err', datetime.datetime(2014, 5, 2))


@raises(InvalidTeamError)
def test_get_score_table_04():
    """
    get_score_table()：引数に無効なチームを指定したとき、InvalidTeamErrorが送出されることを確認する。
    """
    baseball.get_score_table('err', None)


def test_get_score_table_by_url_01():
    """
    get_score_table_by_url()：引数に有効なURLを指定したとき、スコアテーブルの文字列を返すことを確認する。
    """
    expected = textwrap.dedent("""\
        【千葉ロッテ vs 埼玉西武 第6回戦】
        （2014年5月2日：QVCマリンフィールド）

        埼玉西武　  0 2 0  0 0 0  0 0 0  2
        千葉ロッテ  0 0 0  0 0 0  0 0 0  0

        [勝] 岸　 3勝2敗0Ｓ
        [敗] 成瀬 3勝2敗0Ｓ
    """)
    result = baseball.get_score_table_by_url(
        'http://www.nikkansports.com/baseball/professional/score/2014/pl2014050203.html'
    )
    tools.assert_equal(expected, result)


def test_get_game_url_01():
    """
    get_game_url()：引数に有効なチーム、試合日を指定したとき、スコアテーブルのURLを返すことを確認する。
    """
    result = baseball.get_game_url('l', datetime.datetime(2014, 5, 2))
    tools.assert_equal('http://www.nikkansports.com/baseball/professional/score/2014/pl2014050203.html', result)


@raises(InvalidTeamError)
def test_get_game_url_02():
    """
    get_game_url()：引数に無効なチームを指定したとき、InvalidTeamErrorが送出されることを確認する。
    """
    baseball.get_calendar_url('err', datetime.datetime(2014, 5, 2))


def test_get_calendar_url_01():
    """
    get_calendar_url()：引数に有効なチーム、試合日を指定したとき、カレンダーのURLを返すことを確認する。
    """
    result = baseball.get_calendar_url('l', datetime.datetime(2014, 4, 1))
    tools.assert_equal('http://www.nikkansports.com/baseball/professional/schedule/2014/l201404.html', result)


@raises(InvalidTeamError)
def test_get_calender_url_02():
    """
    get_calendar_url()：引数に無効なチームを指定したとき、InvalidTeamErrorが送出されることを確認する。
    """
    baseball.get_calendar_url('err', datetime.datetime(2014, 4, 1))


def test_get_html_01():
    """
    get_html()：引数に有効なURLを指定したとき、HTMLの内容を文字列として返すことを確認する。
    """
    html = baseball.get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014050203.html')
    tools.assert_equal(True, '<title>プロ野球スコア速報 ロッテ対西武 : nikkansports.com</title>' in html)


@raises(ValueError)
def test_get_html_02():
    """
    get_html()：引数に無効なURLを指定したとき、ValueErrorが送出されることを確認する。
    """
    baseball.get_html('えいちてぃーてぃーぴーころんすらっしゅすらっしゅ')


@patch('pyslash.crawler.baseball.get_html')
def test_get_today_game_url_01(get_html):
    """
    get_today_game_url()：引数に'l'を指定したとき、埼玉西武の試合のURLを返すことを確認する。
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_HTML
    result = baseball.get_today_game_url('l')
    tools.assert_equal('http://www.nikkansports.com/baseball/professional/score/2014/il2014061403.html', result)


@patch('pyslash.crawler.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_today_game_url_02(get_html):
    """
    get_today_game_url()：引数に'e'を指定したとき、ResultNotFoundErrorが送出されることを確認する。
    (東北楽天が試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_HTML
    baseball.get_today_game_url('e')


@patch('pyslash.crawler.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_today_game_url_03(get_html):
    """
    get_today_game_url()：引数に'm'を指定したとき、ResultNotFoundErrorが送出されることを確認する。
    (千葉ロッテが試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_HTML
    baseball.get_today_game_url('m')


@patch('pyslash.crawler.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_today_game_url_04(get_html):
    """
    get_today_game_url()：引数に'h'を指定したとき、ResultNotFoundErrorが送出されることを確認する。
    (福岡ソフトバンクが試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_HTML
    baseball.get_today_game_url('h')


@patch('pyslash.crawler.baseball.get_html')
def test_get_today_game_url_05(get_html):
    """
    get_today_game_url()：引数に'bu'を指定したとき、オリックスの試合のURLを返すことを確認する。
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_HTML
    result = baseball.get_today_game_url('bu')
    tools.assert_equal('http://www.nikkansports.com/baseball/professional/score/2014/il2014061405.html', result)


@patch('pyslash.crawler.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_today_game_url_06(get_html):
    """
    get_today_game_url()：引数に'f'を指定したとき、ResultNotFoundErrorが送出されることを確認する。
    (北海道日本ハムが試合開始前のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_HTML
    baseball.get_today_game_url('f')


@patch('pyslash.crawler.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_today_game_url_07(get_html):
    """
    get_today_game_url()：引数に'g'を指定したとき、ResultNotFoundErrorが送出されることを確認する。
    (読売が試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_HTML
    baseball.get_today_game_url('g')


@patch('pyslash.crawler.baseball.get_html')
def test_get_today_game_url_08(get_html):
    """
    get_today_game_url()：引数に't'を指定したとき、阪神の試合のURLを返すことを確認する。
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_HTML
    result = baseball.get_today_game_url('t')
    tools.assert_equal('http://www.nikkansports.com/baseball/professional/score/2014/il2014061403.html', result)


@patch('pyslash.crawler.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_today_game_url_09(get_html):
    """
    get_today_game_url()：引数に'c'を指定したとき、ResultNotFoundErrorが送出されることを確認する。
    (広島東洋が試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_HTML
    baseball.get_today_game_url('c')


@patch('pyslash.crawler.baseball.get_html')
def test_get_today_game_url_10(get_html):
    """
    get_today_game_url()：引数に'd'を指定したとき、中日の試合のURLを返すことを確認する。
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_HTML
    result = baseball.get_today_game_url('d')
    tools.assert_equal('http://www.nikkansports.com/baseball/professional/score/2014/il2014061405.html', result)


@patch('pyslash.crawler.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_today_game_url_11(get_html):
    """
    get_today_game_url()：引数に'bs'を指定したとき、ResultNotFoundErrorが送出されることを確認する。
    (横浜ＤｅＮＡが試合中のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_HTML
    baseball.get_today_game_url('bs')


@patch('pyslash.crawler.baseball.get_html')
@raises(ResultNotFoundError)
def test_get_today_game_url_12(get_html):
    """
    get_today_game_url()：引数に's'を指定したとき、ResultNotFoundErrorが送出されることを確認する。
    (東京ヤクルトが試合開始前のため)
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_HTML
    baseball.get_today_game_url('s')


@patch('pyslash.crawler.baseball.get_html')
@raises(InvalidTeamError)
def test_get_today_game_url_13(get_html):
    """
    get_today_game_url()：引数に無効なチームを指定したとき、InvalidTeamErrorが送出されることを確認する。
    """
    get_html.return_value = RETURN_VALUE_FOR_GET_HTML
    baseball.get_today_game_url('err')


def test_parse_score_table_01():
    """
    parse_score_table()：引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
    """
    html = baseball.get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014042905.html')
    result = baseball.parse_score_table(html)
    tools.assert_equal('日本ハム', result['bat_first'])
    tools.assert_equal('西武', result['field_first'])
    tools.assert_equal(4, result['match'])
    tools.assert_equal('西武ドーム', result['stadium'])
    tools.assert_equal([
        ['0', '0', '0', '0', '0', '0', '1', '0', '0'],
        ['0', '0', '1', '0', '2', '0', '0', '1', 'x'],
    ], result['score'])
    tools.assert_equal([1, 4], result['total_score'])
    tools.assert_equal(('牧田', 2, 1, 0), result['win'])
    tools.assert_equal(('高橋', 0, 1, 3), result['save'])
    tools.assert_equal(('メンドーサ', 1, 4, 0), result['lose'])
    tools.assert_equal([('7回表', '佐藤賢', 3, 'ソロ', '牧田')], result['home_run'])


def test_parse_score_table_02():
    """
    parse_score_table()：引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
    （2ラン、3ラン解析時の不具合対応 #13）
    """
    html = baseball.get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014050906.html')
    result = baseball.parse_score_table(html)
    tools.assert_equal('西武', result['bat_first'])
    tools.assert_equal('ソフトバンク', result['field_first'])
    tools.assert_equal(7, result['match'])
    tools.assert_equal('北九州', result['stadium'])
    tools.assert_equal([
        ['0', '1', '0', '3', '0', '0', '0', '0', '2'],
        ['1', '1', '0', '0', '0', '0', '2', '0', '0'],
    ], result['score'])
    tools.assert_equal([6, 4], result['total_score'])
    tools.assert_equal(('ウィリアムス', 1, 0, 0), result['win'])
    tools.assert_equal(('高橋', 0, 1, 6), result['save'])
    tools.assert_equal(('千賀', 0, 1, 0), result['lose'])
    tools.assert_equal([
        ('1回裏', '内川', 8, 'ソロ', '岸'),
        ('7回裏', '柳田', 5, '２ラン', '岸')
    ], result['home_run'])


def test_parse_score_table_03():
    """
    parse_score_table()：引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
    （サヨナラゲーム解析時の不具合対応 #11）
    """
    html = baseball.get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014032804.html')
    result = baseball.parse_score_table(html)
    tools.assert_equal('オリックス', result['bat_first'])
    tools.assert_equal('日本ハム', result['field_first'])
    tools.assert_equal(1, result['match'])
    tools.assert_equal('札幌ドーム', result['stadium'])
    tools.assert_equal([
        ['2', '1', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0'],
        ['0', '1', '0', '0', '1', '0', '1', '1', '0', '1', '0', '1x'],
    ], result['score'])
    tools.assert_equal([5, 6], result['total_score'])
    tools.assert_equal(('増井', 1, 0, 0), result['win'])
    tools.assert_equal(('海田', 0, 1, 0), result['lose'])
    tools.assert_equal([('10回表', 'ペーニャ', 1, 'ソロ', '宮西')], result['home_run'])


def test_parse_score_table_04():
    """
    parse_score_table()：引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
    （打者一巡があった試合の本塁打解析時の不具合対応 #45）
    """
    html = baseball.get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014081605.html')
    result = baseball.parse_score_table(html)
    tools.assert_equal('日本ハム', result['bat_first'])
    tools.assert_equal('西武', result['field_first'])
    tools.assert_equal(15, result['match'])
    tools.assert_equal('西武ドーム', result['stadium'])
    tools.assert_equal([
        ['0', '0', '0', '0', '1', '4', '0', '1', '1', '1', '0', '0'],
        ['0', '0', '0', '0', '6', '0', '0', '1', '0', '1', '0', '0'],
    ], result['score'])
    tools.assert_equal([8, 8], result['total_score'])
    tools.assert_equal([
        ('5回裏', '中村', 21, '２ラン', '吉川'),
        ('10回表', '陽', 16, 'ソロ', '中郷'),
        ('10回裏', '森', 3, 'ソロ', '増井'),
    ], result['home_run'])


def test_parse_score_table_05():
    """
    parse_score_table()：引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
    （コールドゲーム解析時の不具合対応 #50）
    """
    html = baseball.get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014090802.html')
    result = baseball.parse_score_table(html)
    tools.assert_equal('西武', result['bat_first'])
    tools.assert_equal('ロッテ', result['field_first'])
    tools.assert_equal(21, result['match'])
    tools.assert_equal('ＱＶＣマリン', result['stadium'])
    tools.assert_equal([
        ['3', '0', '0', '1', '2', '1', '0x'],
        ['0', '0', '0', '0', '0', '0', ''],
    ], result['score'])
    tools.assert_equal([7, 0], result['total_score'])
    tools.assert_equal([('1回表', '中村', 30, 'ソロ', '藤岡')], result['home_run'])


@raises(ParseError)
def test_parse_score_table_06():
    """
    parse_score_table()：引数に無効なHTML文字列を指定したとき、ParseErrorが送出されることを確認する。
    """
    baseball.parse_score_table('えいちてぃーえむえる')


def test_get_champions_01():
    """
    get_champions()：引数に2014年を指定したとき、2014年の優勝チームを返すことを確認する。
    """
    result = baseball.get_champions(datetime.datetime(2014, 11, 1))
    tools.assert_equal(('ソフトバンク', '巨人'), result)


def test_get_champions_02():
    """
    get_champions()：引数に2013年を指定したとき、2013年の優勝チームを返すことを確認する。
    """
    result = baseball.get_champions(datetime.datetime(2013, 4, 1))
    tools.assert_equal(('楽天', '巨人'), result)


def test_get_champions_of_this_year_01():
    """
    get_champions_of_this_year()：2014年の優勝チームを返すことを確認する。
    """
    result = baseball.get_champions_of_this_year()
    tools.assert_equal(('ソフトバンク', '巨人'), result)


def test_parse_ranking_01():
    """
    parse_ranking()：引数に2014年のパ・リーグ順位表を指定したとき、優勝チームを返すことを確認する。
    """
    soup = BeautifulSoup("""\
        <table border="0" cellpadding="0" cellspacing="0" summary="">
            <tr>
                <th>順位</th>
                <th>チーム</th>
                <th>試合</th>
                <th>勝数</th>
                <th>敗数</th>
                <th>引分</th>
                <th>勝率</th>
                <th>勝差</th>
                <th>得点</th>
                <th>失点</th>
                <th>本塁打</th>
                <th>盗塁</th>
                <th>打率</th>
                <th>防御率</th>
            </tr>
            <tr>
                <td class="rank">１</td>
                <td class="team">ソフトバンク</td>
                <td>144</td>
                <td>78</td>
                <td>60</td>
                <td>6</td>
                <td>.565</td>
                <td>-</td>
                <td>607</td>
                <td>522</td>
                <td>95</td>
                <td>124</td>
                <td>.280</td>
                <td>3.25</td>
            </tr>
            <tr>
                <td class="rank">２</td>
                <td class="team">オリックス</td>
                <td>144</td>
                <td>80</td>
                <td>62</td>
                <td>2</td>
                <td>.563</td>
                <td>-</td>
                <td>584</td>
                <td>468</td>
                <td>110</td>
                <td>126</td>
                <td>.258</td>
                <td>2.89</td>
            </tr>
            <tr>
                <td class="rank">３</td>
                <td class="team">日本ハム</td>
                <td>144</td>
                <td>73</td>
                <td>68</td>
                <td>3</td>
                <td>.518</td>
                <td>6.5</td>
                <td>593</td>
                <td>569</td>
                <td>119</td>
                <td>134</td>
                <td>.251</td>
                <td>3.61</td>
            </tr>
            <tr>
                <td class="rank">４</td>
                <td class="team">ロッテ</td>
                <td>144</td>
                <td>66</td>
                <td>76</td>
                <td>2</td>
                <td>.465</td>
                <td>14</td>
                <td>556</td>
                <td>642</td>
                <td>96</td>
                <td>64</td>
                <td>.251</td>
                <td>4.14</td>
            </tr>
            <tr>
                <td class="rank">５</td>
                <td class="team">西&nbsp;&nbsp;武</td>
                <td>144</td>
                <td>63</td>
                <td>77</td>
                <td>4</td>
                <td>.450</td>
                <td>16</td>
                <td>574</td>
                <td>600</td>
                <td>125</td>
                <td>74</td>
                <td>.248</td>
                <td>3.77</td>
            </tr>
            <tr>
                <td class="rank">６</td>
                <td class="team">楽&nbsp;&nbsp;天</td>
                <td>144</td>
                <td>64</td>
                <td>80</td>
                <td>0</td>
                <td>.444</td>
                <td>17</td>
                <td>549</td>
                <td>604</td>
                <td>78</td>
                <td>64</td>
                <td>.255</td>
                <td>3.97</td>
            </tr>
        </table>
    """)
    result = baseball.parse_ranking(soup)
    tools.assert_equal('ソフトバンク', result)


def test_parse_ranking_02():
    """
    parse_ranking()：引数に2014年のセ・リーグ順位表を指定したとき、優勝チームを返すことを確認する。
    """
    soup = BeautifulSoup("""\
        <table border="0" cellpadding="0" cellspacing="0" summary="">
            <tr>
                <th>順位</th>
                <th>チーム</th>
                <th>試合</th>
                <th>勝数</th>
                <th>敗数</th>
                <th>引分</th>
                <th>勝率</th>
                <th>勝差</th>
                <th>得点</th>
                <th>失点</th>
                <th>本塁打</th>
                <th>盗塁</th>
                <th>打率</th>
                <th>防御率</th>
            </tr>
            <tr>
                <td class="rank">１</td>
                <td class="team">巨&nbsp;&nbsp;人</td>
                <td>144</td>
                <td>82</td>
                <td>61</td>
                <td>1</td>
                <td>.573</td>
                <td>-</td>
                <td>596</td>
                <td>552</td>
                <td>144</td>
                <td>102</td>
                <td>.257</td>
                <td>3.58</td>
            </tr>
            <tr>
                <td class="rank">２</td>
                <td class="team">阪&nbsp;&nbsp;神</td>
                <td>144</td>
                <td>75</td>
                <td>68</td>
                <td>1</td>
                <td>.524</td>
                <td>7</td>
                <td>599</td>
                <td>614</td>
                <td>94</td>
                <td>55</td>
                <td>.264</td>
                <td>3.88</td>
            </tr>
            <tr>
                <td class="rank">３</td>
                <td class="team">広&nbsp;&nbsp;島</td>
                <td>144</td>
                <td>74</td>
                <td>68</td>
                <td>2</td>
                <td>.521</td>
                <td>7.5</td>
                <td>649</td>
                <td>610</td>
                <td>153</td>
                <td>96</td>
                <td>.272</td>
                <td>3.79</td>
            </tr>
            <tr>
                <td class="rank">４</td>
                <td class="team">中&nbsp;&nbsp;日</td>
                <td>144</td>
                <td>67</td>
                <td>73</td>
                <td>4</td>
                <td>.479</td>
                <td>13.5</td>
                <td>570</td>
                <td>590</td>
                <td>87</td>
                <td>75</td>
                <td>.258</td>
                <td>3.69</td>
            </tr>
            <tr>
                <td class="rank">５</td>
                <td class="team">ＤｅＮＡ</td>
                <td>144</td>
                <td>67</td>
                <td>75</td>
                <td>2</td>
                <td>.472</td>
                <td>14.5</td>
                <td>568</td>
                <td>624</td>
                <td>121</td>
                <td>76</td>
                <td>.253</td>
                <td>3.76</td>
            </tr>
            <tr>
                <td class="rank">６</td>
                <td class="team">ヤクルト</td>
                <td>144</td>
                <td>60</td>
                <td>81</td>
                <td>3</td>
                <td>.426</td>
                <td>21</td>
                <td>667</td>
                <td>717</td>
                <td>139</td>
                <td>62</td>
                <td>.279</td>
                <td>4.62</td>
            </tr>
        </table>
    """)
    result = baseball.parse_ranking(soup)
    tools.assert_equal('巨人', result)


def test_get_champions_before_this_year_01():
    """
    get_champions_before_this_year()：引数に2008年を指定したとき、2008年の優勝チームを返すことを確認する。
    """
    result = baseball.get_champions_before_this_year(2008)
    tools.assert_equal(('西武', '巨人'), result)


def test_parse_champion_list_01():
    """
    parse_champion_list()：
    """
    html = """\
        <table border="0" class="nsTable" summary="パ・リーグ 年度別優勝球団 一覧表">
            <tr>
                <th class="year">年</th>
                <th>優勝チーム（監督）</th>
                <th>勝</th>
                <th>敗</th>
                <th>分</th>
                <th>勝率</th>
            </tr>
            <tr>
                <td>2013</td>
                <td>楽天（星野仙一）</td>
                <td>82</td>
                <td>59</td>
                <td>3</td>
                <td>.582</td>
            </tr>
            <tr>
                <td>2012</td>
                <td>日本ハム（栗山 英樹）</td>
                <td>74</td>
                <td>59</td>
                <td>11</td>
                <td>.556</td>
            </tr>
            <tr>
                <td>2011</td>
                <td>ソフトバンク（秋山 幸二）</td>
                <td>88</td>
                <td>46</td>
                <td>10</td>
                <td>.657</td>
            </tr>
            <tr>
                <td>2010</td>
                <td>ソフトバンク（秋山 幸二）</td>
                <td>76</td>
                <td>63</td>
                <td>5</td>
                <td>.547 </td>
            </tr>
            <tr>
                <td>2009</td>
                <td>日本ハム（梨田 昌孝）</td>
                <td>82</td>
                <td>60</td>
                <td>2</td>
                <td>.577 </td>
            </tr>
            <tr>
                <td>2008</td>
                <td>西武（渡辺 久信）</td>
                <td>76</td>
                <td>64</td>
                <td>4</td>
                <td>.543 </td>
            </tr>
            <tr>
                <td>2007</td>
                <td>日本ハム（ヒルマン）</td>
                <td>79</td>
                <td>60</td>
                <td>5</td>
                <td>.568 </td>
            </tr>
            <tr>
                <td>2006</td>
                <td>日本ハム（ヒルマン）</td>
                <td>82</td>
                <td>54</td>
                <td>0</td>
                <td>.603 </td>
            </tr>
            <tr>
                <td>2005</td>
                <td>ロッテ（バレンタイン）</td>
                <td>84</td>
                <td>49</td>
                <td>3</td>
                <td>.632 </td>
            </tr>
            <tr>
                <td>2004</td>
                <td>西武（伊東 勤）</td>
                <td>74</td>
                <td>58</td>
                <td>1</td>
                <td>.561 </td>
            </tr>
        </table>
    """
    result = baseball.parse_champion_list(html, 2008)
    tools.assert_equal('西武', result)


def test_parse_pitcher_01():
    """
    parse_pitcher()：引数に有効なノードを指定したとき、投手成績のタプルを返すことを確認する。
    """
    soup = BeautifulSoup("""\
        <tr>
            <td class="line">Ｓ</td>
            <td class="line left">高橋&nbsp;（左）</td>
            <td class="line">２</td>
            <td class="line">１</td>
            <td class="line">28</td>
            <td class="line">62</td>
            <td class="line">１</td>
            <td class="line">３</td>
            <td class="line">11</td>
            <td class="line">０</td>
            <td class="line">０</td>
            <td class="line">０</td>
            <td class="line">０</td>
            <td class="line">０</td>
            <td class="line">０</td>
            <td class="line">2.04</td>
        </tr>
    """)
    node = soup.find_all('td')
    result = baseball.parse_pitcher(node)
    tools.assert_equal(('高橋', 2, 1, 28), result)


def test_parse_pitcher_02():
    """
    parse_pitcher()：引数に有効なノード(新加入選手)を指定したとき、投手成績のタプルを返すことを確認する。
    """
    soup = BeautifulSoup("""\
        <tr>
            <td>○</td>
            <td class="left">レイノルズ&nbsp;（右=レッズ）</td>
            <td>３</td>
            <td>５</td>
            <td>０</td>
            <td>９</td>
            <td>７&nbsp;1/3</td>
            <td>33</td>
            <td>109</td>
            <td>９</td>
            <td>２</td>
            <td>１</td>
            <td>１</td>
            <td>５</td>
            <td>５</td>
            <td>4.47</td>
        </tr>
    """)
    node = soup.find_all('td')
    result = baseball.parse_pitcher(node)
    tools.assert_equal(('レイノルズ', 3, 5, 0), result)


def test_parse_date_01():
    """
    parse_date()：引数に有効なURLを指定したとき、試合日を返すことを確認する。
    """
    result = baseball.parse_date('http://www.nikkansports.com/baseball/professional/score/2014/pl2014050203.html')
    tools.assert_equal(datetime.datetime(2014, 5, 2), result)


@raises(ParseError)
def test_parse_date_02():
    """
    parse_date()：引数に無効なURLを指定したとき、ParseErrorが送出されることを確認する。
    """
    baseball.parse_date('http://www.konami.jp/am/qma/character_s/')


def test_create_score_table_01():
    """
    create_score_table()：引数に有効な辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
    """
    data = {
        'bat_first': '北海道日本ハム',
        'field_first': '埼玉西武',
        'match': 4,
        'stadium': '西武ドーム',
        'score': [
            ['0', '0', '0', '0', '0', '0', '1', '0', '0'],
            ['0', '0', '1', '0', '2', '0', '0', '1', 'x'],
        ],
        'total_score': [1, 4],
        'win': ('牧田', 2, 1, 0),
        'save': ('高橋', 0, 1, 3),
        'lose': ('メンドーサ', 1, 4, 0),
        'home_run': [('7回表', '佐藤賢', 3, 'ソロ', '牧田')],
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
    result = baseball.create_score_table(data, datetime.datetime(2014, 4, 29))
    tools.assert_equal(expected, result)


def test_create_score_table_02():
    """
    create_score_table()：引数に有効な辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
    （本塁打欄の不具合対応 #14）
    """
    data = {
        'bat_first': '埼玉西武',
        'field_first': '千葉ロッテ',
        'match': 1,
        'stadium': 'QVCマリンフィールド',
        'score': [
            ['0', '0', '2', '0', '0', '1', '0', '1', '2'],
            ['1', '0', '0', '0', '0', '0', '0', '1', '0'],
        ],
        'total_score': [6, 2],
        'win': ('牧田', 1, 0, 0),
        'lose': ('涌井', 0, 1, 0),
        'home_run': [
            ('8回表', 'ランサム', 1, 'ソロ', '吉原'),
            ('9回表', '浅村', 2, '２ラン', '吉原')
        ],
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
    result = baseball.create_score_table(data, datetime.datetime(2014, 4, 1))
    tools.assert_equal(expected, result)


def test_create_score_table_03():
    """
    create_score_table()：引数に有効な辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
    （サヨナラゲーム解析時の不具合対応 #11）
    """
    data = {
        'bat_first': 'オリックス',
        'field_first': '北海道日本ハム',
        'match': 1,
        'stadium': '札幌ドーム',
        'score': [
            ['2', '1', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0'],
            ['0', '1', '0', '0', '1', '0', '1', '1', '0', '1', '0', '1x'],
        ],
        'total_score': [5, 6],
        'win': ('増井', 1, 0, 0),
        'lose': ('海田', 0, 1, 0),
        'home_run': [('10回表', 'ペーニャ', 1, 'ソロ', '宮西')]
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
    result = baseball.create_score_table(data, datetime.datetime(2014, 3, 28))
    tools.assert_equal(expected, result)


def test_create_score_table_04():
    """
    create_score_table()：引数に有効な辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
    （2桁得点試合解析時の不具合対応 #15）
    """
    data = {
        'bat_first': '埼玉西武',
        'field_first': '東北楽天',
        'match': 10,
        'stadium': '岩手県営野球場',
        'score': [
            ['1', '4', '1', '2', '0', '1', '0', '3', '0'],
            ['1', '0', '0', '0', '0', '0', '1', '0', '0'],
        ],
        'total_score': [12, 2],
        'win': ('十亀', 2, 2, 3),
        'lose': ('塩見', 2, 4, 0),
        'home_run': [
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
    result = baseball.create_score_table(data, datetime.datetime(2014, 5, 18))
    tools.assert_equal(expected, result)


def test_create_score_table_05():
    """
    create_score_table()：引数に有効な辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
    （延長戦の本塁打解析時の不具合対応 #23）
    """
    data = {
        'bat_first': '埼玉西武',
        'field_first': '横浜ＤｅＮＡ',
        'match': 3,
        'stadium': '横浜スタジアム',
        'score': [
            ['2', '0', '0', '0', '0', '0', '0', '3', '1', '1'],
            ['0', '0', '0', '1', '0', '4', '0', '1', '0', '2x'],
        ],
        'total_score': [7, 8],
        'win': ('林', 1, 0, 0),
        'lose': ('ウィリアムス', 1, 2, 0),
        'home_run': [
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
    result = baseball.create_score_table(data, datetime.datetime(2014, 6, 21))
    tools.assert_equal(expected, result)


def test_create_score_table_06():
    """
    create_score_table()：引数に有効な辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
    （延長戦の空行出力時の不具合対応 #44）
    """
    data = {
        'bat_first': '北海道日本ハム',
        'field_first': '埼玉西武',
        'match': 15,
        'stadium': '西武ドーム',
        'score': [
            ['0', '0', '0', '0', '1', '4', '0', '1', '1', '1', '0', '0'],
            ['0', '0', '0', '0', '6', '0', '0', '1', '0', '1', '0', '0'],
        ],
        'total_score': [8, 8],
        'home_run': [
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
    result = baseball.create_score_table(data, datetime.datetime(2014, 8, 16))
    tools.assert_equal(expected, result)


def test_get_long_team_name_01():
    """
    get_long_team_name()：引数に'西武'を指定したとき、'埼玉西武'を返すことを確認する。
    """
    result = baseball.get_long_team_name('西武')
    tools.assert_equal('埼玉西武', result)


def test_get_long_team_name_02():
    """
    get_long_team_name()：引数に'楽天'を指定したとき、'東北楽天'を返すことを確認する。
    """
    result = baseball.get_long_team_name('楽天')
    tools.assert_equal('東北楽天', result)


def test_get_long_team_name_03():
    """
    get_long_team_name()：引数に'ロッテ'を指定したとき、'千葉ロッテ'を返すことを確認する。
    """
    result = baseball.get_long_team_name('ロッテ')
    tools.assert_equal('千葉ロッテ', result)


def test_get_long_team_name_04():
    """
    get_long_team_name()：引数に'ソフトバンク'を指定したとき、'福岡ソフトバンク'を返すことを確認する。
    """
    result = baseball.get_long_team_name('ソフトバンク')
    tools.assert_equal('福岡ソフトバンク', result)


def test_get_long_team_name_05():
    """
    get_long_team_name()：引数に'オリックス'を指定したとき、'オリックス'を返すことを確認する。
    """
    result = baseball.get_long_team_name('オリックス')
    tools.assert_equal('オリックス', result)


def test_get_long_team_name_06():
    """
    get_long_team_name()：引数に'日本ハム'を指定したとき、'北海道日本ハム'を返すことを確認する。
    """
    result = baseball.get_long_team_name('日本ハム')
    tools.assert_equal('北海道日本ハム', result)


def test_get_long_team_name_07():
    """
    get_long_team_name()：引数に'巨人'を指定したとき、'読売'を返すことを確認する。
    """
    result = baseball.get_long_team_name('巨人')
    tools.assert_equal('読売', result)


def test_get_long_team_name_08():
    """
    get_long_team_name()：引数に'阪神'を指定したとき、'阪神'を返すことを確認する。
    """
    result = baseball.get_long_team_name('阪神')
    tools.assert_equal('阪神', result)


def test_get_long_team_name_09():
    """
    get_long_team_name()：引数に'広島'を指定したとき、'広島東洋'を返すことを確認する。
    """
    result = baseball.get_long_team_name('広島')
    tools.assert_equal('広島東洋', result)


def test_get_long_team_name_10():
    """
    get_long_team_name()：引数に'中日'を指定したとき、'中日'を返すことを確認する。
    """
    result = baseball.get_long_team_name('中日')
    tools.assert_equal('中日', result)


def test_get_long_team_name_11():
    """
    get_long_team_name()：引数に'ＤｅＮＡ'を指定したとき、'横浜ＤｅＮＡ'を返すことを確認する。
    """
    result = baseball.get_long_team_name('ＤｅＮＡ')
    tools.assert_equal('横浜ＤｅＮＡ', result)


def test_get_long_team_name_12():
    """
    get_long_team_name()：引数に'ヤクルト'を指定したとき、'東京ヤクルト'を返すことを確認する。
    """
    result = baseball.get_long_team_name('ヤクルト')
    tools.assert_equal('東京ヤクルト', result)


def test_get_long_stadium_name_01():
    """
    get_long_stadium_name()：引数に'西武ドーム'を指定したとき、'西武ドーム'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('西武ドーム')
    tools.assert_equal('西武ドーム', result)


def test_get_long_stadium_name_02():
    """
    get_long_stadium_name()：引数に'コボスタ宮城'を指定したとき、'楽天Koboスタジアム宮城'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('コボスタ宮城')
    tools.assert_equal('楽天Koboスタジアム宮城', result)


def test_get_long_stadium_name_03():
    """
    get_long_stadium_name()：引数に'ＱＶＣマリン'を指定したとき、'QVCマリンフィールド'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('ＱＶＣマリン')
    tools.assert_equal('QVCマリンフィールド', result)


def test_get_long_stadium_name_04():
    """
    get_long_stadium_name()：引数に'ヤフオクドーム'を指定したとき、'福岡 ヤフオク!ドーム'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('ヤフオクドーム')
    tools.assert_equal('福岡 ヤフオク!ドーム', result)


def test_get_long_stadium_name_05():
    """
    get_long_stadium_name()：引数に'京セラドーム大阪'を指定したとき、'京セラドーム大阪'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('京セラドーム大阪')
    tools.assert_equal('京セラドーム大阪', result)


def test_get_long_stadium_name_06():
    """
    get_long_stadium_name()：引数に'札幌ドーム'を指定したとき、'札幌ドーム'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('札幌ドーム')
    tools.assert_equal('札幌ドーム', result)


def test_get_long_stadium_name_07():
    """
    get_long_stadium_name()：引数に'東京ドーム'を指定したとき、'東京ドーム'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('東京ドーム')
    tools.assert_equal('東京ドーム', result)


def test_get_long_stadium_name_08():
    """
    get_long_stadium_name()：引数に'甲子園'を指定したとき、'阪神甲子園球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('甲子園')
    tools.assert_equal('阪神甲子園球場', result)


def test_get_long_stadium_name_09():
    """
    get_long_stadium_name()：引数に'マツダスタジアム'を指定したとき、'Mazda Zoom-Zoomスタジアム広島'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('マツダスタジアム')
    tools.assert_equal('Mazda Zoom-Zoomスタジアム広島', result)


def test_get_long_stadium_name_10():
    """
    get_long_stadium_name()：引数に'ナゴヤドーム'を指定したとき、'ナゴヤドーム'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('ナゴヤドーム')
    tools.assert_equal('ナゴヤドーム', result)


def test_get_long_stadium_name_11():
    """
    get_long_stadium_name()：引数に'横浜'を指定したとき、'横浜スタジアム'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('横浜')
    tools.assert_equal('横浜スタジアム', result)


def test_get_long_stadium_name_12():
    """
    get_long_stadium_name()：引数に'神宮'を指定したとき、'明治神宮野球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('神宮')
    tools.assert_equal('明治神宮野球場', result)


def test_get_long_stadium_name_13():
    """
    get_long_stadium_name()：引数に'ほっともっと神戸'を指定したとき、'ほっともっとフィールド神戸'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('ほっともっと神戸')
    tools.assert_equal('ほっともっとフィールド神戸', result)


def test_get_long_stadium_name_14():
    """
    get_long_stadium_name()：引数に'大宮'を指定したとき、'埼玉県営大宮公園野球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('大宮')
    tools.assert_equal('埼玉県営大宮公園野球場', result)


def test_get_long_stadium_name_15():
    """
    get_long_stadium_name()：引数に'静岡'を指定したとき、'静岡県草薙総合運動場硬式野球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('静岡')
    tools.assert_equal('静岡県草薙総合運動場硬式野球場', result)


def test_get_long_stadium_name_16():
    """
    get_long_stadium_name()：引数に'サンマリン宮崎'を指定したとき、'サンマリンスタジアム宮崎'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('サンマリン宮崎')
    tools.assert_equal('サンマリンスタジアム宮崎', result)


def test_get_long_stadium_name_17():
    """
    get_long_stadium_name()：引数に'鹿児島'を指定したとき、'鹿児島県立鴨池野球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('鹿児島')
    tools.assert_equal('鹿児島県立鴨池野球場', result)


def test_get_long_stadium_name_18():
    """
    get_long_stadium_name()：引数に'北九州'を指定したとき、'北九州市民球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('北九州')
    tools.assert_equal('北九州市民球場', result)
    

def test_get_long_stadium_name_19():
    """
    get_long_stadium_name()：引数に'函館'を指定したとき、'オーシャンスタジアム'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('函館')
    tools.assert_equal('オーシャンスタジアム', result)


def test_get_long_stadium_name_20():
    """
    get_long_stadium_name()：引数に'いわき'を指定したとき、'いわきグリーンスタジアム'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('いわき')
    tools.assert_equal('いわきグリーンスタジアム', result)


def test_get_long_stadium_name_21():
    """
    get_long_stadium_name()：引数に'どらドラパーク米子'を指定したとき、'どらドラパーク米子市民球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('どらドラパーク米子')
    tools.assert_equal('どらドラパーク米子市民球場', result)


def test_get_long_stadium_name_22():
    """
    get_long_stadium_name()：引数に'バッティングパレス相石ひらつか'を指定したとき、'バッティングパレス相石スタジアムひらつか'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('バッティングパレス相石ひらつか')
    tools.assert_equal('バッティングパレス相石スタジアムひらつか', result)


def test_get_long_stadium_name_23():
    """
    get_long_stadium_name()：引数に'ひたちなか'を指定したとき、'ひたちなか市民球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('ひたちなか')
    tools.assert_equal('ひたちなか市民球場', result)


def test_get_long_stadium_name_24():
    """
    get_long_stadium_name()：引数に'秋田'を指定したとき、'こまちスタジアム'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('秋田')
    tools.assert_equal('こまちスタジアム', result)


def test_get_long_stadium_name_25():
    """
    get_long_stadium_name()：引数に'盛岡'を指定したとき、'岩手県営野球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('盛岡')
    tools.assert_equal('岩手県営野球場', result)


def test_get_long_stadium_name_26():
    """
    get_long_stadium_name()：引数に'三次'を指定したとき、'三次きんさいスタジアム'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('三次')
    tools.assert_equal('三次きんさいスタジアム', result)


def test_get_long_stadium_name_27():
    """
    get_long_stadium_name()：引数に'呉'を指定したとき、'呉市二河野球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('呉')
    tools.assert_equal('呉市二河野球場', result)


def test_get_long_stadium_name_28():
    """
    get_long_stadium_name()：引数に'郡山'を指定したとき、'郡山総合運動場開成山野球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('郡山')
    tools.assert_equal('郡山総合運動場開成山野球場', result)


def test_get_long_stadium_name_29():
    """
    get_long_stadium_name()：引数に'浜松'を指定したとき、'浜松球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('浜松')
    tools.assert_equal('浜松球場', result)


def test_get_long_stadium_name_30():
    """
    get_long_stadium_name()：引数に'倉敷'を指定したとき、'マスカットスタジアム'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('倉敷')
    tools.assert_equal('マスカットスタジアム', result)


def test_get_long_stadium_name_31():
    """
    get_long_stadium_name()：引数に'金沢'を指定したとき、'石川県立野球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('金沢')
    tools.assert_equal('石川県立野球場', result)


def test_get_long_stadium_name_32():
    """
    get_long_stadium_name()：引数に'富山'を指定したとき、'富山市民球場アルペンスタジアム'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('富山')
    tools.assert_equal('富山市民球場アルペンスタジアム', result)


def test_get_long_stadium_name_33():
    """
    get_long_stadium_name()：引数に'沖縄セルラー那覇'を指定したとき、'沖縄セルラースタジアム那覇'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('沖縄セルラー那覇')
    tools.assert_equal('沖縄セルラースタジアム那覇', result)


def test_get_long_stadium_name_34():
    """
    get_long_stadium_name()：引数に'旭川'を指定したとき、'スタルヒン球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('旭川')
    tools.assert_equal('スタルヒン球場', result)


def test_get_long_stadium_name_35():
    """
    get_long_stadium_name()：引数に'荘内銀行・日新製薬スタジアム'を指定したとき、'荘内銀行・日新製薬スタジアムやまがた'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('荘内銀行・日新製薬スタジアム')
    tools.assert_equal('荘内銀行・日新製薬スタジアムやまがた', result)


def test_get_long_stadium_name_36():
    """
    get_long_stadium_name()：引数に'帯広'を指定したとき、'帯広の森野球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('帯広')
    tools.assert_equal('帯広の森野球場', result)


def test_get_long_stadium_name_37():
    """
    get_long_stadium_name()：引数に'豊橋'を指定したとき、'豊橋市民球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('豊橋')
    tools.assert_equal('豊橋市民球場', result)


def test_get_long_stadium_name_38():
    """
    get_long_stadium_name()：引数に'ハードオフ新潟'を指定したとき、'HARD OFF ECOスタジアム新潟'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('ハードオフ新潟')
    tools.assert_equal('HARD OFF ECOスタジアム新潟', result)


def test_get_long_stadium_name_39():
    """
    get_long_stadium_name()：引数に'熊本'を指定したとき、'藤崎台県営野球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('熊本')
    tools.assert_equal('藤崎台県営野球場', result)


def test_get_long_stadium_name_40():
    """
    get_long_stadium_name()：引数に'岐阜'を指定したとき、'長良川球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('岐阜')
    tools.assert_equal('長良川球場', result)


def test_get_long_stadium_name_41():
    """
    get_long_stadium_name()：引数に'松山'を指定したとき、'坊っちゃんスタジアム'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('松山')
    tools.assert_equal('坊っちゃんスタジアム', result)


def test_get_long_stadium_name_42():
    """
    get_long_stadium_name()：引数に'長野'を指定したとき、'長野オリンピックスタジアム'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('長野')
    tools.assert_equal('長野オリンピックスタジアム', result)


def test_get_long_stadium_name_43():
    """
    get_long_stadium_name()：引数に'上毛敷島'を指定したとき、'上毛新聞敷島球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('上毛敷島')
    tools.assert_equal('上毛新聞敷島球場', result)


def test_get_long_stadium_name_44():
    """
    get_long_stadium_name()：引数に'宇都宮'を指定したとき、'宇都宮清原球場'を返すことを確認する。
    """
    result = baseball.get_long_stadium_name('宇都宮')
    tools.assert_equal('宇都宮清原球場', result)


def test_create_score_line_01():
    """
    create_score_line()：引数に有効な配列を指定したとき、スコア行を返すことを確認する。
    """
    result = baseball.create_score_line(['0', '0', '0', '0', '0', '0', '1', '0', '0'])
    tools.assert_equal('0 0 0  0 0 0  1 0 0', result)


def test_create_score_line_02():
    """
    create_score_line()：引数に有効な配列(9回裏なし)を指定したとき、スコア行を返すことを確認する。
    """
    result = baseball.create_score_line(['0', '0', '1', '0', '2', '0', '0', '1', 'x'])
    tools.assert_equal('0 0 1  0 2 0  0 1 x', result)


def test_create_score_line_03():
    """
    create_score_line()：引数に有効な配列(サヨナラ)を指定したとき、スコア行を返すことを確認する。
    """
    result = baseball.create_score_line(['0', '1', '0', '1', '1', '0', '1', '0', '1x'])
    tools.assert_equal('0 1 0  1 1 0  1 0 1x', result)


def test_create_score_line_04():
    """
    create_score_line()：引数に有効な配列(延長戦)を指定したとき、スコア行を返すことを確認する。
    """
    result = baseball.create_score_line(['2', '1', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0'])
    tools.assert_equal('2 1 0  0 0 0  0 0 1  1 0 0', result)


def test_create_score_line_05():
    """
    create_score_line()：引数に有効な配列(コールド)を指定したとき、スコア行を返すことを確認する。
    """
    result = baseball.create_score_line(['3', '0', '0', '1', '2', '1', '0x'])
    tools.assert_equal('3 0 0  1 2 1  0x', result)


def test_create_pitcher_line_01():
    """
    create_pitcher_line()：有効な引数を指定したとき、投手成績行を返すことを確認する。
    """
    result = baseball.create_pitcher_line('Ｓ', '高橋', (2, 1, 28))
    tools.assert_equal('[Ｓ] 高橋 2勝1敗28Ｓ\n', result)


def test_search_or_error_01():
    """
    search_or_error()：マッチする条件を引数として指定したとき、マッチングオブジェクトを返すことを確認する。
    """
    result = baseball.search_or_error(r'(\D+)(\d+)', 'マッチ123')
    tools.assert_equal(result.group(0), 'マッチ123')
    tools.assert_equal(result.group(1), 'マッチ')
    tools.assert_equal(result.group(2), '123')


@raises(ParseError)
def test_search_or_error_02():
    """
    search_or_error()：マッチしない条件を引数として指定したとき、ParseErrorが送出されることを確認する。
    """
    baseball.search_or_error(r'(\d+)(\D+)', 'アンマッチ123')


def test_find_or_error_01():
    """
    find_or_error()：検索にヒットする条件を引数として指定したとき、ヒットしたノードを返すことを確認する。
    """
    soup = BeautifulSoup('<div><p><span>テスト</span></p></div>')
    result = baseball.find_or_error(soup, 'span')
    tools.assert_equal(result.string, 'テスト')


@raises(ParseError)
def test_find_or_error_02():
    """
    find_or_error()：検索にしない条件を引数として指定したとき、ParseErrorが送出されることを確認する。
    """
    soup = BeautifulSoup('<div><p><span>テスト</span></p></div>')
    baseball.find_or_error(soup, 'a')


def test_add_space_01():
    """
    add_space()：引数に文字列長の異なる配列を指定したとき、最大長の要素以外の末尾にスペースが付与されていることを確認する。
    """
    result = baseball.add_space('yui', 'mio', 'ritsu', 'tsumugi', 'azusa')
    tools.assert_equal(('yui    ', 'mio    ', 'ritsu  ', 'tsumugi', 'azusa  '), result)


def test_add_space_02():
    """
    add_space()：引数に文字列長の等しい配列を指定したとき、スペースが付与されないことを確認する。
    """
    result = baseball.add_space('Python', 'Erlang', 'Groovy', 'Pascal')
    tools.assert_equal(('Python', 'Erlang', 'Groovy', 'Pascal'), result)


def test_add_em_space_01():
    """
    add_em_space()：引数に文字列長の異なる配列を指定したとき、最大長の要素以外の末尾にスペースが付与されていることを確認する。
    """
    result = baseball.add_em_space(
        '埼玉西武',
        '東北楽天',
        '千葉ロッテ',
        '福岡ソフトバンク',
        'オリックス',
        '北海道日本ハム'
    )
    tools.assert_equal((
        '埼玉西武　　　　',
        '東北楽天　　　　',
        '千葉ロッテ　　　',
        '福岡ソフトバンク',
        'オリックス　　　',
        '北海道日本ハム　',
    ), result)


def test_add_em_space_02():
    """
    add_em_space()：引数に文字列長の等しい配列を指定したとき、スペースが付与されないことを確認する。
    """
    result = baseball.add_em_space('トレンティーノ', 'パグリアルーロ', 'シアンフロッコ')
    tools.assert_equal(('トレンティーノ', 'パグリアルーロ', 'シアンフロッコ'), result)


def test_space_padding_01():
    """
    space_padding()：引数に文字列長の異なる配列を指定したとき、最大長の要素以外の先頭にスペースが付与されていることを確認する。
    """
    result = baseball.space_padding('yui', 'mio', 'ritsu', 'tsumugi', 'azusa')
    tools.assert_equal(('    yui', '    mio', '  ritsu', 'tsumugi', '  azusa'), result)


def test_space_padding_02():
    """
    space_padding()：引数に文字列長の等しい配列を指定したとき、スペースが付与されないことを確認する。
    """
    result = baseball.space_padding('Python', 'Erlang', 'Groovy', 'Pascal')
    tools.assert_equal(('Python', 'Erlang', 'Groovy', 'Pascal'), result)

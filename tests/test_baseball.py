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

import datetime
import textwrap
from unittest import TestCase

from bs4 import BeautifulSoup
from mock import patch

from pyslash import baseball
from pyslash.baseball import GameType, PyslashError


class BaseballTest(TestCase):

    def test_get_score_table_01(self):
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
        result = baseball.create_result('l', datetime.datetime(2014, 5, 2))
        self.assertEqual(expected, result)

    @patch('pyslash.baseball._get_today_table_score_url')
    def test_get_score_table_02(self, get_today_table_score_url):
        """
        get_score_table()：試合日にNoneを指定したとき、当日の試合のスコアテーブルの文字列を返すことを確認する。
        """
        get_today_table_score_url.return_value = 'http://www.nikkansports.com/baseball/professional/score/2014/il2014061403.html'
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
        result = baseball.create_result('l', None)
        self.assertEqual(expected, result)

    def test_get_score_table_03(self):
        """
        get_score_table()：引数に無効なチームを指定したとき、InvalidTeamErrorが送出されることを確認する。
        """
        with self.assertRaises(PyslashError):
            baseball.create_result('err', datetime.datetime(2014, 5, 2))

    def test_get_score_table_04(self):
        """
        get_score_table()：引数に無効なチームを指定したとき、InvalidTeamErrorが送出されることを確認する。
        """
        with self.assertRaises(PyslashError):
            baseball.create_result('err', None)

    def test_get_score_table_by_url_01(self):
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
        result = baseball.create_result_by_url(
            'http://www.nikkansports.com/baseball/professional/score/2014/pl2014050203.html'
        )
        self.assertEqual(expected, result)

    def test_get_game_url_01(self):
        """
        get_game_url()：引数に有効なチーム、試合日を指定したとき、スコアテーブルのURLを返すことを確認する。
        """
        result = baseball._get_table_score_url('l', datetime.datetime(2014, 5, 2))
        self.assertEqual('http://www.nikkansports.com/baseball/professional/score/2014/pl2014050203.html', result)

    def test_get_game_url_02(self):
        """
        get_game_url()：引数に無効なチームを指定したとき、InvalidTeamErrorが送出されることを確認する。
        """
        with self.assertRaises(PyslashError):
            baseball._get_calendar_url('err', datetime.datetime(2014, 5, 2))

    def test_get_calendar_url_01(self):
        """
        get_calendar_url()：引数に有効なチーム、試合日を指定したとき、カレンダーのURLを返すことを確認する。
        """
        result = baseball._get_calendar_url('l', datetime.datetime(2014, 4, 1))
        self.assertEqual('http://www.nikkansports.com/baseball/professional/schedule/2014/l201404.html', result)

    def test_get_calender_url_02(self):
        """
        get_calendar_url()：引数に無効なチームを指定したとき、InvalidTeamErrorが送出されることを確認する。
        """
        with self.assertRaises(PyslashError):
            baseball._get_calendar_url('err', datetime.datetime(2014, 4, 1))

    def test_get_html_01(self):
        """
        get_html()：引数に有効なURLを指定したとき、HTMLの内容を文字列として返すことを確認する。
        """
        html = baseball._get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014050203.html')
        self.assertEqual(True, '<title>プロ野球スコア速報 ロッテ対西武 : nikkansports.com</title>' in html)

    def test_get_html_02(self):
        """
        get_html()：引数に無効なURLを指定したとき、ValueErrorが送出されることを確認する。
        """
        with self.assertRaises(ValueError):
            baseball._get_html('えいちてぃーてぃーぴーころんすらっしゅすらっしゅ')

    def test_get_today_game_url_01(self):
        """
        get_today_game_url()：引数に'l'を指定したとき、埼玉西武の試合のURLを返すことを確認する。
        """
        today_result_url_org = baseball.TODAY_URL
        baseball.TODAY_URL = '/baseball/professional/score/2015/pf-score-20150416.html'

        result = baseball._get_today_table_score_url('l')
        self.assertEqual('http://www.nikkansports.com/baseball/professional/score/2015/pl2015041603.html', result)

        baseball.TODAY_URL = today_result_url_org

    def test_get_today_game_url_02(self):
        """
        get_today_game_url()：引数に'm'を指定したとき、ResultNotFoundErrorが送出されることを確認する。
        (千葉ロッテが試合中のため)
        """
        today_result_url_org = baseball.TODAY_URL
        baseball.TODAY_URL = '/baseball/professional/score/2015/pf-score-20150416.html'

        with self.assertRaises(PyslashError):
            baseball._get_today_table_score_url('m')

        baseball.TODAY_URL = today_result_url_org

    def test_get_today_game_url_03(self):
        """
        get_today_game_url()：引数に無効なチームを指定したとき、InvalidTeamErrorが送出されることを確認する。
        """
        with self.assertRaises(PyslashError):
            baseball._get_today_table_score_url('err')

    def test_parse_score_table_01(self):
        """
        parse_score_table()：引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
        """
        html = baseball._get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014042905.html')
        result = baseball._parse_table_score(html)
        self.assertEqual('日本ハム', result['bat_first'])
        self.assertEqual('西武', result['field_first'])
        self.assertEqual(GameType.pennant_race, result['game_type'])
        self.assertEqual(4, result['match'])
        self.assertEqual('西武ドーム', result['stadium'])
        self.assertEqual([
            ['0', '0', '0', '0', '0', '0', '1', '0', '0'],
            ['0', '0', '1', '0', '2', '0', '0', '1', 'x'],
        ], result['score'])
        self.assertEqual([1, 4], result['total_score'])
        self.assertEqual(('牧田', 2, 1, 0), result['win'])
        self.assertEqual(('高橋', 0, 1, 3), result['save'])
        self.assertEqual(('メンドーサ', 1, 4, 0), result['lose'])
        self.assertEqual([('7回表', '佐藤賢', 3, 'ソロ', '牧田')], result['home_run'])

    def test_parse_score_table_02(self):
        """
        parse_score_table()：引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
        （2ラン、3ラン解析時の不具合対応 #13）
        """
        html = baseball._get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014050906.html')
        result = baseball._parse_table_score(html)
        self.assertEqual('西武', result['bat_first'])
        self.assertEqual('ソフトバンク', result['field_first'])
        self.assertEqual(GameType.pennant_race, result['game_type'])
        self.assertEqual(7, result['match'])
        self.assertEqual('北九州', result['stadium'])
        self.assertEqual([
            ['0', '1', '0', '3', '0', '0', '0', '0', '2'],
            ['1', '1', '0', '0', '0', '0', '2', '0', '0'],
        ], result['score'])
        self.assertEqual([6, 4], result['total_score'])
        self.assertEqual(('ウィリアムス', 1, 0, 0), result['win'])
        self.assertEqual(('高橋', 0, 1, 6), result['save'])
        self.assertEqual(('千賀', 0, 1, 0), result['lose'])
        self.assertEqual([
            ('1回裏', '内川', 8, 'ソロ', '岸'),
            ('7回裏', '柳田', 5, '２ラン', '岸')
        ], result['home_run'])

    def test_parse_score_table_03(self):
        """
        parse_score_table()：引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
        （サヨナラゲーム解析時の不具合対応 #11）
        """
        html = baseball._get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014032804.html')
        result = baseball._parse_table_score(html)
        self.assertEqual('オリックス', result['bat_first'])
        self.assertEqual('日本ハム', result['field_first'])
        self.assertEqual(GameType.pennant_race, result['game_type'])
        self.assertEqual(1, result['match'])
        self.assertEqual('札幌ドーム', result['stadium'])
        self.assertEqual([
            ['2', '1', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0'],
            ['0', '1', '0', '0', '1', '0', '1', '1', '0', '1', '0', '1x'],
        ], result['score'])
        self.assertEqual([5, 6], result['total_score'])
        self.assertEqual(('増井', 1, 0, 0), result['win'])
        self.assertEqual(('海田', 0, 1, 0), result['lose'])
        self.assertEqual([('10回表', 'ペーニャ', 1, 'ソロ', '宮西')], result['home_run'])

    def test_parse_score_table_04(self):
        """
        parse_score_table()：引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
        （打者一巡があった試合の本塁打解析時の不具合対応 #45）
        """
        html = baseball._get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014081605.html')
        result = baseball._parse_table_score(html)
        self.assertEqual('日本ハム', result['bat_first'])
        self.assertEqual('西武', result['field_first'])
        self.assertEqual(GameType.pennant_race, result['game_type'])
        self.assertEqual(15, result['match'])
        self.assertEqual('西武ドーム', result['stadium'])
        self.assertEqual([
            ['0', '0', '0', '0', '1', '4', '0', '1', '1', '1', '0', '0'],
            ['0', '0', '0', '0', '6', '0', '0', '1', '0', '1', '0', '0'],
        ], result['score'])
        self.assertEqual([8, 8], result['total_score'])
        self.assertEqual([
            ('5回裏', '中村', 21, '２ラン', '吉川'),
            ('10回表', '陽', 16, 'ソロ', '中郷'),
            ('10回裏', '森', 3, 'ソロ', '増井'),
        ], result['home_run'])

    def test_parse_score_table_05(self):
        """
        parse_score_table()：引数に有効なHTML文字列を指定したとき、その内容を辞書として返すことを確認する。
        （コールドゲーム解析時の不具合対応 #50）
        """
        html = baseball._get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014090802.html')
        result = baseball._parse_table_score(html)
        self.assertEqual('西武', result['bat_first'])
        self.assertEqual('ロッテ', result['field_first'])
        self.assertEqual(GameType.pennant_race, result['game_type'])
        self.assertEqual(21, result['match'])
        self.assertEqual('ＱＶＣマリン', result['stadium'])
        self.assertEqual([
            ['3', '0', '0', '1', '2', '1', '0x'],
            ['0', '0', '0', '0', '0', '0', ''],
        ], result['score'])
        self.assertEqual([7, 0], result['total_score'])
        self.assertEqual(('岸', 11, 4, 0), result['win'])
        self.assertEqual(('藤岡', 6, 10, 0), result['lose'])
        self.assertEqual([('1回表', '中村', 30, 'ソロ', '藤岡')], result['home_run'])

    def test_parse_score_table_06(self):
        """
        parse_score_table()：引数に有効なHTML文字列(CSファーストステージ)を指定したとき、その内容を辞書として返すことを確認する。
        """
        html = baseball._get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014101201.html')
        result = baseball._parse_table_score(html)
        self.assertEqual('日本ハム', result['bat_first'])
        self.assertEqual('オリックス', result['field_first'])
        self.assertEqual(GameType.first_stage, result['game_type'])
        self.assertEqual(2, result['match'])
        self.assertEqual('京セラドーム大阪', result['stadium'])
        self.assertEqual([
            ['2', '0', '0', '0', '0', '0', '1', '1', '0'],
            ['0', '0', '0', '0', '0', '1', '2', '3', 'x'],
        ], result['score'])
        self.assertEqual([4, 6], result['total_score'])
        self.assertEqual(('馬原', 1, 0, 0), result['win'])
        self.assertEqual(('平野佳', 0, 0, 1), result['save'])
        self.assertEqual(('谷元', 0, 1, 0), result['lose'])
        self.assertEqual([
            ('7回表', 'ミランダ', 1, 'ソロ', '佐藤達'),
            ('8回裏', 'Ｔ－岡田', 1, '３ラン', '谷元'),
        ], result['home_run'])

    def test_parse_score_table_07(self):
        """
        parse_score_table()：引数に有効なHTML文字列(CSファイナルステージ)を指定したとき、その内容を辞書として返すことを確認する。
        """
        html = baseball._get_html('http://www.nikkansports.com/baseball/professional/score/2014/pl2014101902.html')
        result = baseball._parse_table_score(html)
        self.assertEqual('日本ハム', result['bat_first'])
        self.assertEqual('ソフトバンク', result['field_first'])
        self.assertEqual(GameType.final_stage, result['game_type'])
        self.assertEqual(5, result['match'])
        self.assertEqual('ヤフオクドーム', result['stadium'])
        self.assertEqual([
            ['0', '0', '0', '0', '0', '0', '3', '1', '0', '0', '2'],
            ['0', '4', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ], result['score'])
        self.assertEqual([6, 4], result['total_score'])
        self.assertEqual(('鍵谷', 2, 0, 0), result['win'])
        self.assertEqual(('増井', 0, 0, 1), result['save'])
        self.assertEqual(('サファテ', 0, 1, 1), result['lose'])
        self.assertEqual([('8回表', '中田', 4, 'ソロ', '五十嵐')], result['home_run'])

    def test_parse_score_table_08(self):
        """
        parse_score_table()：引数に有効なHTML文字列(日本シリーズ)を指定したとき、その内容を辞書として返すことを確認する。
        """
        html = baseball._get_html('http://www.nikkansports.com/baseball/professional/score/2014/ns2014102901.html')
        result = baseball._parse_table_score(html)
        self.assertEqual('阪神', result['bat_first'])
        self.assertEqual('ソフトバンク', result['field_first'])
        self.assertEqual(GameType.nippon_series, result['game_type'])
        self.assertEqual(4, result['match'])
        self.assertEqual('ヤフオクドーム', result['stadium'])
        self.assertEqual([
            ['0', '0', '2', '0', '0', '0', '0', '0', '0', '0'],
            ['2', '0', '0', '0', '0', '0', '0', '0', '0', '3x'],
        ], result['score'])
        self.assertEqual([2, 5], result['total_score'])
        self.assertEqual(('サファテ', 1, 0, 1), result['win'])
        self.assertEqual(('安藤', 0, 1, 0), result['lose'])
        self.assertEqual([('10回裏', '中村', 1, '３ラン', '呉')], result['home_run'])

    def test_parse_score_table_09(self):
        """
        parse_score_table()：引数に有効なHTML文字列(オープン戦)を指定したとき、その内容を辞書として返すことを確認する。
        （オープン戦対応 #81）
        """
        html = baseball._get_html('http://www.nikkansports.com/baseball/professional/score/2015/pg2015030803.html')
        result = baseball._parse_table_score(html)
        self.assertEqual('西武', result['bat_first'])
        self.assertEqual('オリックス', result['field_first'])
        self.assertEqual(GameType.pre_season_game, result['game_type'])
        self.assertEqual(1, result['match'])
        self.assertEqual('わかさ京都', result['stadium'])
        self.assertEqual([
            ['2', '4', '0', '0', '5', '0', '0', '3', '0'],
            ['0', '0', '0', '0', '0', '0', '1', '0', '1'],
        ], result['score'])
        self.assertEqual([14, 2], result['total_score'])
        self.assertEqual(('岸', 1, 0, 0), result['win'])
        self.assertEqual(('東明', 0, 1, 0), result['lose'])
        self.assertEqual([
            ('1回表', '中村', 1, '２ラン', '東明'),
            ('7回裏', 'Ｔ－岡田', 1, 'ソロ', 'バスケス'),
        ], result['home_run'])

    def test_parse_score_table_10(self):
        """
        parse_score_table()：引数に無効なHTML文字列を指定したとき、ParseErrorが送出されることを確認する。
        """
        with self.assertRaises(PyslashError):
            baseball._parse_table_score('えいちてぃーえむえる')

    def test_get_champions_01(self):
        """
        get_champions()：引数に2014年を指定したとき、2014年の優勝チームを返すことを確認する。
        """
        result = baseball._get_champions(2014)
        self.assertEqual(('ソフトバンク', '巨人'), result)

    def test_get_champions_02(self):
        """
        get_champions()：引数に2013年を指定したとき、2013年の優勝チームを返すことを確認する。
        """
        result = baseball._get_champions(2013)
        self.assertEqual(('楽天', '巨人'), result)

    # def test_get_champions_of_this_year_01():
    #     """
    #     get_champions_of_this_year()：2014年の優勝チームを返すことを確認する。
    #     """
    #     result = baseball.get_champions_of_this_year()
    #     tools.assert_equal(('ソフトバンク', '巨人'), result)

    def test_parse_ranking_01(self):
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
        """, 'html.parser')
        result = baseball._get_top(soup)
        self.assertEqual('ソフトバンク', result)

    def test_parse_ranking_02(self):
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
        """, 'html.parser')
        result = baseball._get_top(soup)
        self.assertEqual('巨人', result)

    def test_get_champions_before_this_year_01(self):
        """
        get_champions_before_this_year()：引数に2008年を指定したとき、2008年の優勝チームを返すことを確認する。
        """
        result = baseball._get_champions_before_this_year(2008)
        self.assertEqual(('西武', '巨人'), result)

    def test_parse_champion_list_01(self):
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
        result = baseball._get_champion(html, 2008)
        self.assertEqual('西武', result)

    def test_parse_pitcher_01(self):
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
        """, 'html.parser')
        node = soup.find_all('td')
        result = baseball._parse_pitcher(node)
        self.assertEqual(('高橋', 2, 1, 28), result)

    def test_parse_pitcher_02(self):
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
        """, 'html.parser')
        node = soup.find_all('td')
        result = baseball._parse_pitcher(node)
        self.assertEqual(('レイノルズ', 3, 5, 0), result)

    def test_parse_date_01(self):
        """
        parse_date()：引数に有効なURLを指定したとき、試合日を返すことを確認する。
        """
        result = baseball._parse_day('http://www.nikkansports.com/baseball/professional/score/2014/pl2014050203.html')
        self.assertEqual(datetime.date(2014, 5, 2), result)

    def test_parse_date_02(self):
        """
        parse_date()：引数に無効なURLを指定したとき、ParseErrorが送出されることを確認する。
        """
        with self.assertRaises(PyslashError):
            baseball._parse_day('http://www.konami.jp/am/qma/character_s/')

    def test_create_score_table_01(self):
        """
        create_score_table()：引数に有効な辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
        """
        data = {
            'bat_first': '北海道日本ハム',
            'field_first': '埼玉西武',
            'game_type': GameType.pennant_race,
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
        result = baseball._format_result(data, datetime.datetime(2014, 4, 29))
        self.assertEqual(expected, result)

    def test_create_score_table_02(self):
        """
        create_score_table()：引数に有効な辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
        （本塁打欄の不具合対応 #14）
        """
        data = {
            'bat_first': '埼玉西武',
            'field_first': '千葉ロッテ',
            'game_type': GameType.pennant_race,
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
        result = baseball._format_result(data, datetime.datetime(2014, 4, 1))
        self.assertEqual(expected, result)

    def test_create_score_table_03(self):
        """
        create_score_table()：引数に有効な辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
        （サヨナラゲーム解析時の不具合対応 #11）
        """
        data = {
            'bat_first': 'オリックス',
            'field_first': '北海道日本ハム',
            'game_type': GameType.pennant_race,
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
        result = baseball._format_result(data, datetime.datetime(2014, 3, 28))
        self.assertEqual(expected, result)

    def test_create_score_table_04(self):
        """
        create_score_table()：引数に有効な辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
        （2桁得点試合解析時の不具合対応 #15）
        """
        data = {
            'bat_first': '埼玉西武',
            'field_first': '東北楽天',
            'game_type': GameType.pennant_race,
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
        result = baseball._format_result(data, datetime.datetime(2014, 5, 18))
        self.assertEqual(expected, result)

    def test_create_score_table_05(self):
        """
        create_score_table()：引数に有効な辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
        （延長戦の本塁打解析時の不具合対応 #23）
        """
        data = {
            'bat_first': '埼玉西武',
            'field_first': '横浜ＤｅＮＡ',
            'game_type': GameType.pennant_race,
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
        result = baseball._format_result(data, datetime.datetime(2014, 6, 21))
        self.assertEqual(expected, result)

    def test_create_score_table_06(self):
        """
        create_score_table()：引数に有効な辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
        （延長戦の空行出力時の不具合対応 #44）
        """
        data = {
            'bat_first': '北海道日本ハム',
            'field_first': '埼玉西武',
            'game_type': GameType.pennant_race,
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
        result = baseball._format_result(data, datetime.datetime(2014, 8, 16))
        self.assertEqual(expected, result)

    def test_create_score_table_07(self):
        """
        create_score_table()：引数に有効な辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
        （クライマックスシリーズ見出し対応 #58）
        """
        data = {
            'bat_first': '埼玉西武',
            'field_first': '北海道日本ハム',
            'game_type': GameType.first_stage,
            'match': 2,
            'stadium': '札幌ドーム',
            'score': [
                ['0', '0', '0', '0', '1', '0', '0', '1', '6'],
                ['0', '0', '0', '1', '0', '0', '0', '0', '0'],
            ],
            'total_score': [8, 1],
            'win': ('西口', 1, 0, 0),
            'lose': ('石井', 0, 1, 0),
            'home_run': [
                ('4回裏', 'ホフパワー', 1, 'ソロ', '西口'),
                ('9回表', '中村', 1, '３ラン', '宮西'),
            ],
        }
        expected = textwrap.dedent("""\
            【北海道日本ハム vs 埼玉西武 CSファーストステージ第2戦】
            （2011年10月30日：札幌ドーム）

            埼玉西武　　　  0 0 0  0 1 0  0 1 6  8
            北海道日本ハム  0 0 0  1 0 0  0 0 0  1

            [勝] 西口 1勝0敗0Ｓ
            [敗] 石井 0勝1敗0Ｓ

            [本塁打]
              4回裏 ホフパワー  1号 ソロ　 （西口）
              9回表 中村　　　  1号 ３ラン （宮西）
        """)
        result = baseball._format_result(data, datetime.datetime(2011, 10, 30))
        self.assertEqual(expected, result)

    def test_create_score_table_08(self):
        """
        create_score_table()：引数に有効な辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
        （クライマックスシリーズ見出し対応 #58）
        """
        data = {
            'bat_first': '千葉ロッテ',
            'field_first': '東北楽天',
            'game_type': GameType.final_stage,
            'match': 4,
            'stadium': '日本製紙クリネックススタジアム宮城',
            'score': [
                ['0', '0', '0', '4', '0', '0', '1', '0', '0'],
                ['1', '2', '0', '2', '0', '0', '1', '2', 'x'],
            ],
            'total_score': [5, 8],
            'win': ('斎藤', 1, 0, 0),
            'save': ('田中', 1, 0, 1),
            'lose': ('ロサ', 0, 1, 0),
            'home_run': [
                ('4回表', 'Ｇ．Ｇ．佐藤', 1, '３ラン', '辛島'),
                ('4回裏', 'ジョーンズ', 2, '２ラン', '西野'),
                ('7回裏', 'マギー', 1, 'ソロ', 'ロサ'),
            ],
        }
        expected = textwrap.dedent("""\
            【東北楽天 vs 千葉ロッテ CSファイナルステージ第4戦】
            （2013年10月21日：日本製紙クリネックススタジアム宮城）

            千葉ロッテ  0 0 0  4 0 0  1 0 0  5
            東北楽天　  1 2 0  2 0 0  1 2 x  8

            [勝] 斎藤 1勝0敗0Ｓ
            [Ｓ] 田中 1勝0敗1Ｓ
            [敗] ロサ 0勝1敗0Ｓ

            [本塁打]
              4回表 Ｇ．Ｇ．佐藤  1号 ３ラン （辛島）
              4回裏 ジョーンズ　  2号 ２ラン （西野）
              7回裏 マギー　　　  1号 ソロ　 （ロサ）
        """)
        result = baseball._format_result(data, datetime.datetime(2013, 10, 21))
        self.assertEqual(expected, result)

    def test_create_score_table_09(self):
        """
        create_score_table()：引数に有効な辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
        （クライマックスシリーズ／日本シリーズ対応 #62）
        """
        data = {
            'bat_first': '埼玉西武',
            'field_first': '読売',
            'game_type': GameType.nippon_series,
            'match': 7,
            'stadium': '東京ドーム',
            'score': [
                ['0', '0', '0', '0', '1', '0', '0', '2', '0'],
                ['1', '1', '0', '0', '0', '0', '0', '0', '0'],
            ],
            'total_score': [3, 2],
            'win': ('星野', 1, 0, 0),
            'save': ('グラマン', 0, 0, 2),
            'lose': ('越智', 1, 1, 0),
            'home_run': [
                ('2回裏', '坂本', 1, 'ソロ', '西口'),
                ('5回表', 'ボカチカ', 1, 'ソロ', '内海'),
            ],
        }
        expected = textwrap.dedent("""\
            【読売 vs 埼玉西武 日本シリーズ第7戦】
            （2008年11月9日：東京ドーム）

            埼玉西武  0 0 0  0 1 0  0 2 0  3
            読売　　  1 1 0  0 0 0  0 0 0  2

            [勝] 星野　　 1勝0敗0Ｓ
            [Ｓ] グラマン 0勝0敗2Ｓ
            [敗] 越智　　 1勝1敗0Ｓ

            [本塁打]
              2回裏 坂本　　  1号 ソロ （西口）
              5回表 ボカチカ  1号 ソロ （内海）
        """)
        result = baseball._format_result(data, datetime.datetime(2008, 11, 9))
        self.assertEqual(expected, result)

    def test_create_score_table_10(self):
        """
        create_score_table()：引数に有効な辞書を指定したとき、スコアテーブルの文字列を返すことを確認する。
        （オープン戦対応 #81）
        """
        data = {
            'bat_first': '埼玉西武',
            'field_first': 'オリックス',
            'game_type': GameType.pre_season_game,
            'match': 1,
            'stadium': 'わかさスタジアム京都',
            'score': [
                ['2', '4', '0', '0', '5', '0', '0', '3', '0'],
                ['0', '0', '0', '0', '0', '0', '1', '0', '1'],
            ],
            'total_score': [14, 2],
            'win': ('岸', 1, 0, 0),
            'lose': ('東明', 0, 1, 0),
            'home_run': [
                ('1回表', '中村', 1, '２ラン', '東明'),
                ('7回裏', 'Ｔ－岡田', 1, 'ソロ', 'バスケス'),
            ],
        }
        expected = textwrap.dedent("""\
            【オリックス vs 埼玉西武 オープン戦】
            （2015年3月8日：わかさスタジアム京都）

            埼玉西武　  2 4 0  0 5 0  0 3 0  14
            オリックス  0 0 0  0 0 0  1 0 1   2

            [勝] 岸　 1勝0敗0Ｓ
            [敗] 東明 0勝1敗0Ｓ

            [本塁打]
              1回表 中村　　  1号 ２ラン （東明）
              7回裏 Ｔ－岡田  1号 ソロ　 （バスケス）
        """)
        result = baseball._format_result(data, datetime.datetime(2015, 3, 8))
        self.assertEqual(expected, result)

    def test_get_long_team_name_01(self):
        """
        get_long_team_name()：引数に'西武'を指定したとき、'埼玉西武'を返すことを確認する。
        """
        result = baseball._get_long_team_name('西武')
        self.assertEqual('埼玉西武', result)

    def test_get_long_team_name_02(self):
        """
        get_long_team_name()：引数に'楽天'を指定したとき、'東北楽天'を返すことを確認する。
        """
        result = baseball._get_long_team_name('楽天')
        self.assertEqual('東北楽天', result)

    def test_get_long_team_name_03(self):
        """
        get_long_team_name()：引数に'ロッテ'を指定したとき、'千葉ロッテ'を返すことを確認する。
        """
        result = baseball._get_long_team_name('ロッテ')
        self.assertEqual('千葉ロッテ', result)

    def test_get_long_team_name_04(self):
        """
        get_long_team_name()：引数に'ソフトバンク'を指定したとき、'福岡ソフトバンク'を返すことを確認する。
        """
        result = baseball._get_long_team_name('ソフトバンク')
        self.assertEqual('福岡ソフトバンク', result)

    def test_get_long_team_name_05(self):
        """
        get_long_team_name()：引数に'オリックス'を指定したとき、'オリックス'を返すことを確認する。
        """
        result = baseball._get_long_team_name('オリックス')
        self.assertEqual('オリックス', result)

    def test_get_long_team_name_06(self):
        """
        get_long_team_name()：引数に'日本ハム'を指定したとき、'北海道日本ハム'を返すことを確認する。
        """
        result = baseball._get_long_team_name('日本ハム')
        self.assertEqual('北海道日本ハム', result)

    def test_get_long_team_name_07(self):
        """
        get_long_team_name()：引数に'巨人'を指定したとき、'読売'を返すことを確認する。
        """
        result = baseball._get_long_team_name('巨人')
        self.assertEqual('読売', result)

    def test_get_long_team_name_08(self):
        """
        get_long_team_name()：引数に'阪神'を指定したとき、'阪神'を返すことを確認する。
        """
        result = baseball._get_long_team_name('阪神')
        self.assertEqual('阪神', result)

    def test_get_long_team_name_09(self):
        """
        get_long_team_name()：引数に'広島'を指定したとき、'広島東洋'を返すことを確認する。
        """
        result = baseball._get_long_team_name('広島')
        self.assertEqual('広島東洋', result)

    def test_get_long_team_name_10(self):
        """
        get_long_team_name()：引数に'中日'を指定したとき、'中日'を返すことを確認する。
        """
        result = baseball._get_long_team_name('中日')
        self.assertEqual('中日', result)

    def test_get_long_team_name_11(self):
        """
        get_long_team_name()：引数に'ＤｅＮＡ'を指定したとき、'横浜ＤｅＮＡ'を返すことを確認する。
        """
        result = baseball._get_long_team_name('ＤｅＮＡ')
        self.assertEqual('横浜ＤｅＮＡ', result)

    def test_get_long_team_name_12(self):
        """
        get_long_team_name()：引数に'ヤクルト'を指定したとき、'東京ヤクルト'を返すことを確認する。
        """
        result = baseball._get_long_team_name('ヤクルト')
        self.assertEqual('東京ヤクルト', result)

    def test_get_long_stadium_name_01(self):
        """
        get_long_stadium_name()：引数に'西武ドーム'を指定したとき、'西武ドーム'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('西武ドーム')
        self.assertEqual('西武ドーム', result)

    def test_get_long_stadium_name_02(self):
        """
        get_long_stadium_name()：引数に'コボスタ宮城'を指定したとき、'楽天Koboスタジアム宮城'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('コボスタ宮城')
        self.assertEqual('楽天Koboスタジアム宮城', result)

    def test_get_long_stadium_name_03(self):
        """
        get_long_stadium_name()：引数に'ＱＶＣマリン'を指定したとき、'QVCマリンフィールド'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('ＱＶＣマリン')
        self.assertEqual('QVCマリンフィールド', result)

    def test_get_long_stadium_name_04(self):
        """
        get_long_stadium_name()：引数に'ヤフオクドーム'を指定したとき、'福岡 ヤフオク!ドーム'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('ヤフオクドーム')
        self.assertEqual('福岡 ヤフオク!ドーム', result)

    def test_get_long_stadium_name_05(self):
        """
        get_long_stadium_name()：引数に'京セラドーム大阪'を指定したとき、'京セラドーム大阪'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('京セラドーム大阪')
        self.assertEqual('京セラドーム大阪', result)

    def test_get_long_stadium_name_06(self):
        """
        get_long_stadium_name()：引数に'札幌ドーム'を指定したとき、'札幌ドーム'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('札幌ドーム')
        self.assertEqual('札幌ドーム', result)

    def test_get_long_stadium_name_07(self):
        """
        get_long_stadium_name()：引数に'東京ドーム'を指定したとき、'東京ドーム'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('東京ドーム')
        self.assertEqual('東京ドーム', result)

    def test_get_long_stadium_name_08(self):
        """
        get_long_stadium_name()：引数に'甲子園'を指定したとき、'阪神甲子園球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('甲子園')
        self.assertEqual('阪神甲子園球場', result)

    def test_get_long_stadium_name_09(self):
        """
        get_long_stadium_name()：引数に'マツダスタジアム'を指定したとき、'Mazda Zoom-Zoomスタジアム広島'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('マツダスタジアム')
        self.assertEqual('Mazda Zoom-Zoomスタジアム広島', result)

    def test_get_long_stadium_name_10(self):
        """
        get_long_stadium_name()：引数に'ナゴヤドーム'を指定したとき、'ナゴヤドーム'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('ナゴヤドーム')
        self.assertEqual('ナゴヤドーム', result)

    def test_get_long_stadium_name_11(self):
        """
        get_long_stadium_name()：引数に'横浜'を指定したとき、'横浜スタジアム'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('横浜')
        self.assertEqual('横浜スタジアム', result)

    def test_get_long_stadium_name_12(self):
        """
        get_long_stadium_name()：引数に'神宮'を指定したとき、'明治神宮野球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('神宮')
        self.assertEqual('明治神宮野球場', result)

    def test_get_long_stadium_name_13(self):
        """
        get_long_stadium_name()：引数に'ほっともっと神戸'を指定したとき、'ほっともっとフィールド神戸'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('ほっともっと神戸')
        self.assertEqual('ほっともっとフィールド神戸', result)

    def test_get_long_stadium_name_14(self):
        """
        get_long_stadium_name()：引数に'大宮'を指定したとき、'埼玉県営大宮公園野球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('大宮')
        self.assertEqual('埼玉県営大宮公園野球場', result)

    def test_get_long_stadium_name_15(self):
        """
        get_long_stadium_name()：引数に'静岡'を指定したとき、'静岡県草薙総合運動場硬式野球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('静岡')
        self.assertEqual('静岡県草薙総合運動場硬式野球場', result)

    def test_get_long_stadium_name_16(self):
        """
        get_long_stadium_name()：引数に'サンマリン宮崎'を指定したとき、'サンマリンスタジアム宮崎'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('サンマリン宮崎')
        self.assertEqual('サンマリンスタジアム宮崎', result)

    def test_get_long_stadium_name_17(self):
        """
        get_long_stadium_name()：引数に'鹿児島'を指定したとき、'鹿児島県立鴨池野球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('鹿児島')
        self.assertEqual('鹿児島県立鴨池野球場', result)

    def test_get_long_stadium_name_18(self):
        """
        get_long_stadium_name()：引数に'北九州'を指定したとき、'北九州市民球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('北九州')
        self.assertEqual('北九州市民球場', result)

    def test_get_long_stadium_name_19(self):
        """
        get_long_stadium_name()：引数に'函館'を指定したとき、'オーシャンスタジアム'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('函館')
        self.assertEqual('オーシャンスタジアム', result)

    def test_get_long_stadium_name_20(self):
        """
        get_long_stadium_name()：引数に'いわき'を指定したとき、'いわきグリーンスタジアム'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('いわき')
        self.assertEqual('いわきグリーンスタジアム', result)

    def test_get_long_stadium_name_21(self):
        """
        get_long_stadium_name()：引数に'どらドラパーク米子'を指定したとき、'どらドラパーク米子市民球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('どらドラパーク米子')
        self.assertEqual('どらドラパーク米子市民球場', result)

    def test_get_long_stadium_name_22(self):
        """
        get_long_stadium_name()：引数に'バッティングパレス相石ひらつか'を指定したとき、'バッティングパレス相石スタジアムひらつか'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('バッティングパレス相石ひらつか')
        self.assertEqual('バッティングパレス相石スタジアムひらつか', result)

    def test_get_long_stadium_name_23(self):
        """
        get_long_stadium_name()：引数に'ひたちなか'を指定したとき、'ひたちなか市民球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('ひたちなか')
        self.assertEqual('ひたちなか市民球場', result)

    def test_get_long_stadium_name_24(self):
        """
        get_long_stadium_name()：引数に'秋田'を指定したとき、'こまちスタジアム'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('秋田')
        self.assertEqual('こまちスタジアム', result)

    def test_get_long_stadium_name_25(self):
        """
        get_long_stadium_name()：引数に'盛岡'を指定したとき、'岩手県営野球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('盛岡')
        self.assertEqual('岩手県営野球場', result)

    def test_get_long_stadium_name_26(self):
        """
        get_long_stadium_name()：引数に'三次'を指定したとき、'三次きんさいスタジアム'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('三次')
        self.assertEqual('三次きんさいスタジアム', result)

    def test_get_long_stadium_name_27(self):
        """
        get_long_stadium_name()：引数に'呉'を指定したとき、'呉市二河野球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('呉')
        self.assertEqual('呉市二河野球場', result)

    def test_get_long_stadium_name_28(self):
        """
        get_long_stadium_name()：引数に'郡山'を指定したとき、'郡山総合運動場開成山野球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('郡山')
        self.assertEqual('郡山総合運動場開成山野球場', result)

    def test_get_long_stadium_name_29(self):
        """
        get_long_stadium_name()：引数に'浜松'を指定したとき、'浜松球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('浜松')
        self.assertEqual('浜松球場', result)

    def test_get_long_stadium_name_30(self):
        """
        get_long_stadium_name()：引数に'倉敷'を指定したとき、'マスカットスタジアム'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('倉敷')
        self.assertEqual('マスカットスタジアム', result)

    def test_get_long_stadium_name_31(self):
        """
        get_long_stadium_name()：引数に'金沢'を指定したとき、'石川県立野球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('金沢')
        self.assertEqual('石川県立野球場', result)

    def test_get_long_stadium_name_32(self):
        """
        get_long_stadium_name()：引数に'富山'を指定したとき、'富山市民球場アルペンスタジアム'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('富山')
        self.assertEqual('富山市民球場アルペンスタジアム', result)

    def test_get_long_stadium_name_33(self):
        """
        get_long_stadium_name()：引数に'沖縄セルラー那覇'を指定したとき、'沖縄セルラースタジアム那覇'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('沖縄セルラー那覇')
        self.assertEqual('沖縄セルラースタジアム那覇', result)

    def test_get_long_stadium_name_34(self):
        """
        get_long_stadium_name()：引数に'旭川'を指定したとき、'スタルヒン球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('旭川')
        self.assertEqual('スタルヒン球場', result)

    def test_get_long_stadium_name_35(self):
        """
        get_long_stadium_name()：引数に'荘内銀行・日新製薬スタジアム'を指定したとき、'荘内銀行・日新製薬スタジアムやまがた'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('荘内銀行・日新製薬スタジアム')
        self.assertEqual('荘内銀行・日新製薬スタジアムやまがた', result)

    def test_get_long_stadium_name_36(self):
        """
        get_long_stadium_name()：引数に'帯広'を指定したとき、'帯広の森野球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('帯広')
        self.assertEqual('帯広の森野球場', result)

    def test_get_long_stadium_name_37(self):
        """
        get_long_stadium_name()：引数に'豊橋'を指定したとき、'豊橋市民球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('豊橋')
        self.assertEqual('豊橋市民球場', result)

    def test_get_long_stadium_name_38(self):
        """
        get_long_stadium_name()：引数に'ハードオフ新潟'を指定したとき、'HARD OFF ECOスタジアム新潟'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('ハードオフ新潟')
        self.assertEqual('HARD OFF ECOスタジアム新潟', result)

    def test_get_long_stadium_name_39(self):
        """
        get_long_stadium_name()：引数に'熊本'を指定したとき、'藤崎台県営野球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('熊本')
        self.assertEqual('藤崎台県営野球場', result)

    def test_get_long_stadium_name_40(self):
        """
        get_long_stadium_name()：引数に'岐阜'を指定したとき、'長良川球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('岐阜')
        self.assertEqual('長良川球場', result)

    def test_get_long_stadium_name_41(self):
        """
        get_long_stadium_name()：引数に'松山'を指定したとき、'坊っちゃんスタジアム'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('松山')
        self.assertEqual('坊っちゃんスタジアム', result)

    def test_get_long_stadium_name_42(self):
        """
        get_long_stadium_name()：引数に'長野'を指定したとき、'長野オリンピックスタジアム'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('長野')
        self.assertEqual('長野オリンピックスタジアム', result)

    def test_get_long_stadium_name_43(self):
        """
        get_long_stadium_name()：引数に'上毛敷島'を指定したとき、'上毛新聞敷島球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('上毛敷島')
        self.assertEqual('上毛新聞敷島球場', result)

    def test_get_long_stadium_name_44(self):
        """
        get_long_stadium_name()：引数に'宇都宮'を指定したとき、'宇都宮清原球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('宇都宮')
        self.assertEqual('宇都宮清原球場', result)

    def test_get_long_stadium_name_45(self):
        """
        get_long_stadium_name()：引数に'尾道'を指定したとき、'しまなみ球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('尾道')
        self.assertEqual('しまなみ球場', result)

    def test_get_long_stadium_name_46(self):
        """
        get_long_stadium_name()：引数に'わかさ京都'を指定したとき、'わかさスタジアム京都'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('わかさ京都')
        self.assertEqual('わかさスタジアム京都', result)

    def test_get_long_stadium_name_47(self):
        """
        get_long_stadium_name()：引数に'福島'を指定したとき、'福島県営あづま球場'を返すことを確認する。
        """
        result = baseball._get_long_stadium_name('福島')
        self.assertEqual('福島県営あづま球場', result)

    def test_create_score_line_01(self):
        """
        create_score_line()：引数に有効な配列を指定したとき、スコア行を返すことを確認する。
        """
        result = baseball._format_score(['0', '0', '0', '0', '0', '0', '1', '0', '0'])
        self.assertEqual('0 0 0  0 0 0  1 0 0', result)

    def test_create_score_line_02(self):
        """
        create_score_line()：引数に有効な配列(9回裏なし)を指定したとき、スコア行を返すことを確認する。
        """
        result = baseball._format_score(['0', '0', '1', '0', '2', '0', '0', '1', 'x'])
        self.assertEqual('0 0 1  0 2 0  0 1 x', result)

    def test_create_score_line_03(self):
        """
        create_score_line()：引数に有効な配列(サヨナラ)を指定したとき、スコア行を返すことを確認する。
        """
        result = baseball._format_score(['0', '1', '0', '1', '1', '0', '1', '0', '1x'])
        self.assertEqual('0 1 0  1 1 0  1 0 1x', result)

    def test_create_score_line_04(self):
        """
        create_score_line()：引数に有効な配列(延長戦)を指定したとき、スコア行を返すことを確認する。
        """
        result = baseball._format_score(['2', '1', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0'])
        self.assertEqual('2 1 0  0 0 0  0 0 1  1 0 0', result)

    def test_create_score_line_05(self):
        """
        create_score_line()：引数に有効な配列(コールド)を指定したとき、スコア行を返すことを確認する。
        """
        result = baseball._format_score(['3', '0', '0', '1', '2', '1', '0x'])
        self.assertEqual('3 0 0  1 2 1  0x', result)

    def test_create_pitcher_line_01(self):
        """
        create_pitcher_line()：有効な引数を指定したとき、投手成績行を返すことを確認する。
        """
        result = baseball._format_pitcher('Ｓ', '高橋', (2, 1, 28))
        self.assertEqual('[Ｓ] 高橋 2勝1敗28Ｓ\n', result)

    def test_search_or_error_01(self):
        """
        search_or_error()：マッチする条件を引数として指定したとき、マッチングオブジェクトを返すことを確認する。
        """
        result = baseball._search_or_error(r'(\D+)(\d+)', 'マッチ123')
        self.assertEqual(result.group(0), 'マッチ123')
        self.assertEqual(result.group(1), 'マッチ')
        self.assertEqual(result.group(2), '123')

    def test_search_or_error_02(self):
        """
        search_or_error()：マッチしない条件を引数として指定したとき、ParseErrorが送出されることを確認する。
        """
        with self.assertRaises(PyslashError):
            baseball._search_or_error(r'(\d+)(\D+)', 'アンマッチ123')

    def test_find_or_error_01(self):
        """
        find_or_error()：検索にヒットする条件を引数として指定したとき、ヒットしたノードを返すことを確認する。
        """
        soup = BeautifulSoup('<div><p><span>テスト</span></p></div>', 'html.parser')
        result = baseball._find_or_error(soup, 'span')
        self.assertEqual(result.string, 'テスト')

    def test_find_or_error_02(self):
        """
        find_or_error()：検索にしない条件を引数として指定したとき、ParseErrorが送出されることを確認する。
        """
        soup = BeautifulSoup('<div><p><span>テスト</span></p></div>', 'html.parser')
        with self.assertRaises(PyslashError):
            baseball._find_or_error(soup, 'a')

    def test_add_space_01(self):
        """
        add_space()：引数に文字列長の異なる配列を指定したとき、最大長の要素以外の末尾にスペースが付与されていることを確認する。
        """
        result = baseball._add_space('yui', 'mio', 'ritsu', 'tsumugi', 'azusa')
        self.assertEqual(('yui    ', 'mio    ', 'ritsu  ', 'tsumugi', 'azusa  '), result)

    def test_add_space_02(self):
        """
        add_space()：引数に文字列長の等しい配列を指定したとき、スペースが付与されないことを確認する。
        """
        result = baseball._add_space('Python', 'Erlang', 'Groovy', 'Pascal')
        self.assertEqual(('Python', 'Erlang', 'Groovy', 'Pascal'), result)

    def test_add_em_space_01(self):
        """
        add_em_space()：引数に文字列長の異なる配列を指定したとき、最大長の要素以外の末尾にスペースが付与されていることを確認する。
        """
        result = baseball._add_em_space(
            '埼玉西武',
            '東北楽天',
            '千葉ロッテ',
            '福岡ソフトバンク',
            'オリックス',
            '北海道日本ハム'
        )
        self.assertEqual((
            '埼玉西武　　　　',
            '東北楽天　　　　',
            '千葉ロッテ　　　',
            '福岡ソフトバンク',
            'オリックス　　　',
            '北海道日本ハム　',
        ), result)

    def test_add_em_space_02(self):
        """
        add_em_space()：引数に文字列長の等しい配列を指定したとき、スペースが付与されないことを確認する。
        """
        result = baseball._add_em_space('トレンティーノ', 'パグリアルーロ', 'シアンフロッコ')
        self.assertEqual(('トレンティーノ', 'パグリアルーロ', 'シアンフロッコ'), result)

    def test_space_padding_01(self):
        """
        space_padding()：引数に文字列長の異なる配列を指定したとき、最大長の要素以外の先頭にスペースが付与されていることを確認する。
        """
        result = baseball._space_padding('yui', 'mio', 'ritsu', 'tsumugi', 'azusa')
        self.assertEqual(('    yui', '    mio', '  ritsu', 'tsumugi', '  azusa'), result)

    def test_space_padding_02(self):
        """
        space_padding()：引数に文字列長の等しい配列を指定したとき、スペースが付与されないことを確認する。
        """
        result = baseball._space_padding('Python', 'Erlang', 'Groovy', 'Pascal')
        self.assertEqual(('Python', 'Erlang', 'Groovy', 'Pascal'), result)

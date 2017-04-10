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

from collections import defaultdict
import datetime
import re
import urllib.request

from bs4 import BeautifulSoup
from enum import Enum


class PyslashError(Exception):
    """
    当ライブラリで想定していない入出力があったことを示す例外。
    """


class GameType(Enum):
    """
    試合の種類を表す列挙型。
    """
    pre_season_game = 0
    """オープン戦"""

    pennant_race = 1
    """ペナントレース"""

    first_stage = 2
    """クライマックスシリーズファーストステージ"""

    final_stage = 3
    """クライマックスシリーズファイナルステージ"""

    nippon_series = 4
    """日本シリーズ"""


# nikkansports.comのURL
NIKKANSPORTS_URL = 'http://www.nikkansports.com'

# 本日の試合結果のURL
TODAY_URL = '/baseball/professional/score/'

# 順位表のURL
STANDINGS_URL = '/baseball/professional/data/standings/'

# パ・リーグ優勝チームのURL
VICTORY_P_URL = '/baseball/professional/data/pfdata/victory/pf-victory_pl.html'

# セ・リーグ優勝チームのURL
VICTORY_C_URL = '/baseball/professional/data/pfdata/victory/pf-victory_cl.html'

# テーブルスコアのURLテンプレート
TABLE_SCORE_URL_TEMPLATE = r'/baseball/professional/score/%04d/\D+%04d%02d%02d\d+\.html'

# 試合日程のURLテンプレート
CALENDAR_URL_TEMPLATE = '/baseball/professional/schedule/%04d/%s%04d%02d.html'

# テーブルスコアの正規表現パターン
TABLE_SCORE_URL_PATTERN = r'/baseball/professional/score/\d{4}/\D+(\d{4})(\d{2})(\d{2})\d+\.html'

# チーム名変換テーブル
TEAM_NAMES = {
    'bs': 'ＤｅＮＡ',
    'bu': 'オリックス',
    'c': '広島',
    'd': '中日',
    'e': '楽天',
    'f': '日本ハム',
    'g': '巨人',
    'h': 'ソフトバンク',
    'l': '西武',
    'm': 'ロッテ',
    's': 'ヤクルト',
    't': '阪神',
}

# チーム正式名称変換テーブル
LONG_TEAM_NAMES = {
    'ＤｅＮＡ': '横浜ＤｅＮＡ',
    '広島': '広島東洋',
    '楽天': '東北楽天',
    '日本ハム': '北海道日本ハム',
    '巨人': '読売',
    'ソフトバンク': '福岡ソフトバンク',
    '西武': '埼玉西武',
    'ロッテ': '千葉ロッテ',
    'ヤクルト': '東京ヤクルト',
}

# 球場正式名称変換テーブル
LONG_STADIUM_NAMES = {
    '横浜': '横浜スタジアム',
    'マツダスタジアム': 'Mazda Zoom-Zoomスタジアム広島',
    'コボスタ宮城': '楽天Koboスタジアム宮城',
    'ヤフオクドーム': '福岡 ヤフオク!ドーム',
    'ＱＶＣマリン': 'QVCマリンフィールド',
    '神宮': '明治神宮野球場',
    '甲子園': '阪神甲子園球場',
    'ほっともっと神戸': 'ほっともっとフィールド神戸',
    '大宮': '埼玉県営大宮公園野球場',
    '静岡': '静岡県草薙総合運動場硬式野球場',
    'サンマリン宮崎': 'サンマリンスタジアム宮崎',
    '鹿児島': '鹿児島県立鴨池野球場',
    '北九州': '北九州市民球場',
    '函館': 'オーシャンスタジアム',
    'いわき': 'いわきグリーンスタジアム',
    'どらドラパーク米子': 'どらドラパーク米子市民球場',
    'バッティングパレス相石ひらつか': 'バッティングパレス相石スタジアムひらつか',
    'ひたちなか': 'ひたちなか市民球場',
    '秋田': 'こまちスタジアム',
    '盛岡': '岩手県営野球場',
    '三次': '三次きんさいスタジアム',
    '呉': '呉市二河野球場',
    '郡山': '郡山総合運動場開成山野球場',
    '浜松': '浜松球場',
    '倉敷': 'マスカットスタジアム',
    '金沢': '石川県立野球場',
    '富山': '富山市民球場アルペンスタジアム',
    '沖縄セルラー那覇': '沖縄セルラースタジアム那覇',
    '旭川': 'スタルヒン球場',
    '荘内銀行・日新製薬スタジアム': '荘内銀行・日新製薬スタジアムやまがた',
    '帯広': '帯広の森野球場',
    '豊橋': '豊橋市民球場',
    'ハードオフ新潟': 'HARD OFF ECOスタジアム新潟',
    '熊本': '藤崎台県営野球場',
    '岐阜': '長良川球場',
    '松山': '坊っちゃんスタジアム',
    '長野': '長野オリンピックスタジアム',
    '上毛敷島': '上毛新聞敷島球場',
    '宇都宮': '宇都宮清原球場',
    '尾道': 'しまなみ球場',
    'わかさ京都': 'わかさスタジアム京都',
    '福島': '福島県営あづま球場',
}


def create_result(team, day):
    """
    指定されたチーム、日付の試合結果を文字列として取得する。

    :param team: チーム略称
    :type team: str
    :param day: 試合日
    :type day: datetime.date
    :return: 試合結果
    :rtype: str
    """
    # テーブルスコアのURLを取得する
    url = _get_table_score_url(team, day) if day else _get_today_table_score_url(team)

    # 試合結果を返す
    return create_result_by_url(url)


def create_result_by_url(url):
    """
    指定されたURLのテーブルスコアを解析し、試合結果を文字列として取得する。

    :param url: URL
    :type url: str
    :return: 試合結果
    :rtype: str
    """
    # 試合結果を構築する
    html = _get_html(url)
    score_data = _parse_table_score(html)
    day = _parse_day(url)
    return _format_result(score_data, day)


def _get_table_score_url(team, day):
    """
    指定されたチーム、日付のテーブルスコアのURLを取得する。

    :param team: チーム略称
    :type team: str
    :param day: 試合日
    :type day: datetime.date
    :return: URL
    :rtype: str
    """
    # 当該チームの試合日程のHTMLを取得する
    url = _get_calendar_url(team, day)
    html = _get_html(url)

    # テーブルスコアのURLを取得する
    pattern = TABLE_SCORE_URL_TEMPLATE % (day.year, day.year, day.month, day.day)
    m = _search_or_error(pattern, html)
    return NIKKANSPORTS_URL + m.group(0)


def _get_calendar_url(team, day):
    """
    指定されたチーム、年月の試合日程のURLを取得する。

    :param team: チーム略称
    :type team: str
    :param day: 日付(年月のフィールドのみ参照)
    :type day: datetime.date
    :return: URL
    :rtype: str
    """
    # チーム名をチェックする
    if team not in TEAM_NAMES:
        raise PyslashError('Invalid team name: ' + team)

    # 試合日程のURLを取得する
    return NIKKANSPORTS_URL + CALENDAR_URL_TEMPLATE % (day.year, team, day.year, day.month)


def _get_html(url):
    """
    指定されたURLのHTMLを文字列として取得する。

    :param url: URL
    :type url: str
    :return: HTML
    :rtype: str
    """
    # 指定されたURLのHTMLを取得する
    with urllib.request.urlopen(url) as response:
        encoding = response.headers.get_content_charset() or 'utf-8'
        return response.read().decode(encoding, 'ignore')


def _get_today_table_score_url(team):
    """
    指定されたチームの今日の試合のテーブルスコアのURLを取得する。

    :param team: チーム略称
    :type team: str
    :return: URL
    :rtype: str
    """
    # チーム名を取得する
    try:
        team_name = TEAM_NAMES[team]
    except KeyError:
        raise PyslashError('Invalid team name: ' + team)

    # 全カードのテーブルスコアのURLを取得する
    html = _get_html(NIKKANSPORTS_URL + TODAY_URL)
    soup = BeautifulSoup(html, 'html.parser')
    score_tables = soup.find_all('table', {'class': 'scoreTable'})

    # 当該チームのスコアを探索する
    for i, table in enumerate(score_tables):
        team_in_tables = table.find_all('td', {'class': 'team'})
        for team_in_table in team_in_tables:
            if re.sub(r'\s', '', team_in_table.string) == team_name:
                target_paragraph = soup.find_all('p', {'class': 'nScore'})[i]
                url = _find_or_error(target_paragraph, 'a').get('href')
                return NIKKANSPORTS_URL + url

    # 結果が見つからない場合は例外とする
    raise PyslashError('Result not found.')


def _parse_table_score(html):
    """
    指定されたテーブルスコアの文字列を解析し、スコア情報を格納した辞書に変換する。

    :param html: テーブルスコア
    :type html: str
    :return: スコア情報
    :rtype: dict
    """
    # 戻り値用の辞書
    score_data = {}

    # BeautifulSoupオブジェクトを構築する
    soup = BeautifulSoup(html, 'html.parser')

    # 先攻チーム／後攻チーム
    card_title = _find_or_error(soup, 'h4', {'id': 'cardTitle'})
    m = _search_or_error(r'([^\s]+)\s対\s([^\s]+)', card_title.string)
    score_data['bat_first'] = m.group(2)
    score_data['field_first'] = m.group(1)

    # 試合日
    up_date = _find_or_error(soup, 'p', {'id': 'upDate'})
    m = _search_or_error(r'(\d+)年(\d+)月(\d+)日', up_date.span.string)
    day = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    # 球場／試合種別
    data = _find_or_error(soup, 'p', {'class': 'data'})
    m = _search_or_error(r'◇([^◇]+)◇開始\d+時\d+分◇([^◇]+)◇観衆\d+人', data.string)
    score_data['stadium'] = m.group(2)
    if m.group(1) == '日本シリーズ':
        score_data['game_type'] = GameType.nippon_series
    elif m.group(1) == 'クライマックスシリーズ':
        if score_data['field_first'] in _get_champions(day.year):
            score_data['game_type'] = GameType.final_stage
        else:
            score_data['game_type'] = GameType.first_stage
    elif m.group(1) == 'オープン戦':
        score_data['game_type'] = GameType.pre_season_game
    else:
        score_data['game_type'] = GameType.pennant_race

    # 回戦
    time = _find_or_error(soup, 'p', {'id': 'time'})
    m = _search_or_error(r'(\d+)勝(\d+)敗(\d+)分け', time.string)
    score_data['match'] = int(m.group(1)) + int(m.group(2)) + int(m.group(3))
    if score_data['game_type'] == GameType.final_stage:
        # アドバンテージの1勝ぶんを差し引く
        score_data['match'] -= 1

    # スコア
    score_data['score'] = []
    score_data['total_score'] = []
    score_table = _find_or_error(soup, 'table', {'class': 'scoreTable'})
    rows = score_table.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        score_data['score'].append([x.string.strip().lower() for x in cols[1:-1]])
        score_data['total_score'].append(int(cols[-1].string))
    for i, (top, bottom) in enumerate(zip(score_data['score'][0], score_data['score'][1])):
        # コールドゲームの最終回以降の余分な空白を除去する
        if top == '' and bottom == '':
            score_data['score'][0] = score_data['score'][0][:i]
            score_data['score'][1] = score_data['score'][1][:i]
            break

    # 勝利投手／セーブ投手／敗戦投手
    pitcher = _find_or_error(soup, 'table', {'class': 'pitcher'})
    rows = pitcher.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        status = cols[0].string
        if status == '○':
            score_data['win'] = _parse_pitcher(cols)
        elif status == 'Ｓ':
            score_data['save'] = _parse_pitcher(cols)
        elif status == '●':
            score_data['lose'] = _parse_pitcher(cols)

    # 本塁打
    score_data['home_run'] = []
    footnotes = soup.find_all('dl', {'class': 'data'})
    for footnote in footnotes:
        if footnote.dt.string == '◇本塁打':
            # 打撃成績から本塁打の出たイニングを収集する
            home_run_innings = defaultdict(list)
            tables = soup.find_all('table', {'class', 'batter'})
            for i, table in enumerate(tables):
                rows = table.find_all('tr')

                # イニングの見出しを収集する
                inning_numbers = []
                cols = rows[0].find_all('th')
#                for col in cols[8:]:
                for col in cols[9:]:
                    inning = col.string.strip()
                    if inning:
                        inning_numbers.append(int(inning))
                    else:
                        # 打者2巡目は見出しが空欄になっているため
                        inning_numbers.append(inning_numbers[-1])

                # 本塁打を収集する
                for row in rows[1:]:
                    cols = row.find_all('td')
#                    for j, col in enumerate(cols[8:]):
                    for j, col in enumerate(cols[9:]):
                        m = re.search(r'.本', col.string)
                        if m:
#                            m = _search_or_error(r'([^（]+)（[^）]+）', cols[1].string)
#                            home_run_innings[m.group(1)].append(str(inning_numbers[j]) + '回' + ['表', '裏'][i])
                            home_run_innings[cols[1].string].append(str(inning_numbers[j]) + '回' + ['表', '裏'][i])

            # 末尾の本塁打欄を解析する
            lines = footnote.find_all('dd')
            for line in lines:
                m = _search_or_error(r'([^\d]+)(\d+)号（(ソロ|２ラン|３ラン|満塁)\d+m=([^）]+)）', line.string)
                score_data['home_run'].append((
                    home_run_innings[m.group(1)].pop(0),
                    m.group(1),
                    int(m.group(2)),
                    m.group(3),
                    m.group(4)
                ))

            # 本塁打欄は1つしかないはず
            break

    # 構築した辞書を返す
    return score_data


def _get_champions(year):
    """
    指定された年度の両リーグの優勝チームを取得する。

    :param year: 年度
    :type year: int
    :return: パの優勝チーム、セの優勝チーム
    :rtype: tuple
    """
    # 今年かそれ以外かで処理を振り分ける
    if year == datetime.date.today().year:
        return _get_champions_of_this_year()
    else:
        return _get_champions_before_this_year(year)


def _get_champions_of_this_year():
    """
    今年の両リーグの優勝チームを取得する。

    :return: パの優勝チーム、セの優勝チーム
    :rtype: tuple
    """
    # 順位表のHTMLを取得する
    html = _get_html(NIKKANSPORTS_URL + STANDINGS_URL)

    # BeautifulSoupオブジェクトを構築する
    soup = BeautifulSoup(html, 'html.parser')

    # 両リーグの優勝チームを取得する
    tables = soup.find_all('table')
    return _get_top(tables[1]), _get_top(tables[0])


def _get_top(node):
    """
    指定された順位表を解析し、首位のチームを取得する。

    :param node: 順位表のノード
    :type node: bs4.element.Tag
    :return: 首位のチーム
    :rtype: str
    """
    # 順位表を行ごとに解析する
    rows = node.find_all('tr')
    for row in rows:
        # 首位の行を探索する
        rank = row.find('td', {'class': 'rank'})
        if rank and rank.string == '１':
            # 首位のチーム名を返す
            champion = row.find('td', {'class': 'team'})
            return re.sub('\s', '', champion.string)


def _get_champions_before_this_year(year):
    """
    指定された年度の両リーグの優勝チームを取得する。

    :param year: 年度
    :type year: int
    :return: パの優勝チーム、セの優勝チーム
    :rtype: tuple
    """
    # 歴代優勝チームのHTMLを取得する
    p_html = _get_html(NIKKANSPORTS_URL + VICTORY_P_URL)
    c_html = _get_html(NIKKANSPORTS_URL + VICTORY_C_URL)

    # 両リーグの優勝チームを取得する
    return _get_champion(p_html, year), _get_champion(c_html, year)


def _get_champion(html, year):
    """
    歴代優勝チームのHTMLを探索し、指定された年度の優勝チームを取得する。

    :param html: HTML
    :type html: str
    :param year: 年度
    :type year: int
    :return: 優勝チーム
    :rtype: str
    """
    # BeautifulSoupオブジェクトを構築する
    soup = BeautifulSoup(html, 'html.parser')

    # 歴代優勝チームのtable要素を取得する
    table = _find_or_error(soup, 'table', {'class': 'nsTable'})
    rows = table.find_all('tr')

    # 指定された年度の優勝チームを探索する
    for row in rows:
        cols = row.find_all('td')
        if cols and int(cols[0].string) == year:
            m = _search_or_error(r'([^（]+)（[^）]+）', cols[1].string)
            return m.group(1)


def _parse_pitcher(node):
    """
    投手成績のノードを解析し、タプルに変換する。

    :param node: 投手成績のノード
    :type node: bs4.element.Tag
    :return: 投手名、勝利数、敗北数、セーブ数
    :rtype: tuple
    """
    return node[1].string, int(node[3].string), int(node[4].string), int(node[5].string)

    # 投手名を切り出す
    m = _search_or_error(r'([^\s]+)\s（[^）]+）', node[1].string)

    # タプルに変換する
    return m.group(1), int(node[2].string), int(node[3].string), int(node[4].string)


def _parse_day(url):
    """
    指定されたURLから試合日を抽出する。

    :param url: URL
    :type url: str
    :return 試合日
    :rtype datetime.date
    """
    # URLから試合日を抽出する
    m = _search_or_error(TABLE_SCORE_URL_PATTERN, url)
    return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))


def _format_result(score_data, day):
    """
    スコア情報をもとに試合結果を構築する。

    :param score_data: スコア情報
    :type score_data: dict
    :param day: 試合日
    :type day: datetime.date
    :return: 試合結果
    :rtype: str
    """
    # ヘッダ欄を構築する
    field_first = _get_long_team_name(score_data['field_first'])
    bat_first = _get_long_team_name(score_data['bat_first'])
    if score_data['game_type'] == GameType.nippon_series:
        match = '日本シリーズ第%d戦' % score_data['match']
    elif score_data['game_type'] == GameType.final_stage:
        match = 'CSファイナルステージ第%d戦' % score_data['match']
    elif score_data['game_type'] == GameType.first_stage:
        match = 'CSファーストステージ第%d戦' % score_data['match']
    elif score_data['game_type'] == GameType.pre_season_game:
        match = 'オープン戦'
    else:
        match = '第%d回戦' % score_data['match']
    result = '【%s vs %s %s】\n' % (field_first, bat_first, match)
    result += '（%d年%d月%d日／%s）\n' % (
        day.year,
        day.month,
        day.day,
        _get_long_stadium_name(score_data['stadium'])
    )
    result += '\n'

    # スコア欄を構築する
    bat_first, field_first = _add_em_space(bat_first, field_first)
    top_score, bottom_score = _add_space(
        _format_score(score_data['score'][0]),
        _format_score(score_data['score'][1])
    )
    top_total_score, bottom_total_score = _space_padding(
        str(score_data['total_score'][0]),
        str(score_data['total_score'][1])
    )
    result += '%s  %s  %s\n' % (bat_first, top_score, top_total_score)
    result += '%s  %s  %s\n' % (field_first, bottom_score, bottom_total_score)

    # 投手成績欄を構築する
    win = score_data.get('win')
    save = score_data.get('save')
    lose = score_data.get('lose')
    win_player, save_player, lose_player = _add_em_space(
        win[0] if win else '',
        save[0] if save else '',
        lose[0] if lose else ''
    )
    pitcher = (
        _format_pitcher('勝', win_player, win[1:] if win else None) +
        _format_pitcher('Ｓ', save_player, save[1:] if save else None) +
        _format_pitcher('敗', lose_player, lose[1:] if lose else None)
    )
    if pitcher:
        result += '\n' + pitcher

    # 本塁打欄を構築する
    home_run = score_data.get('home_run')
    if home_run:
        result += '\n'
        result += '[本塁打]\n'

        # 各項目の最大長を取得する
        max_inning_len = 0
        max_player_len = 0
        max_type_len = 0
        for line in home_run:
            max_inning_len = max(max_inning_len, len(line[0]))
            max_player_len = max(max_player_len, len(line[1]))
            max_type_len = max(max_type_len, len(line[3]))

        # 桁揃えのスペースを付与しながら本塁打欄を構築する
        for line in home_run:
            result += '  %s %s %2d号 %s （%s）\n' % (
                ' ' * (max_inning_len - len(line[0])) + line[0],
                line[1] + '　' * (max_player_len - len(line[1])),
                line[2],
                line[3] + '　' * (max_type_len - len(line[3])),
                line[4]
            )

    # 構築したスコアを返す
    return result


def _get_long_team_name(team_name):
    """
    指定されたチーム名を正式名称に変換する。

    :param team_name: チーム名
    :type team_name: str
    :return: 正式名称
    :rtype: str
    """
    # 変換テーブルを探索する
    return LONG_TEAM_NAMES.get(team_name, team_name)


def _get_long_stadium_name(stadium_name):
    """
    指定された球場名を正式名称に変換する。

    :param stadium_name: 球場名
    :type stadium_name: str
    :return: 正式名称
    :rtype: str
    """
    # 変換テーブルを探索する
    return LONG_STADIUM_NAMES.get(stadium_name, stadium_name)


def _format_score(scores):
    """
    スコア行(先攻のみ、もしくは後攻のみ)を構築する。

    :param scores: 各イニングのスコア
    :type scores: list
    :return: スコア行
    :rtype: str
    """
    # 各イニングのスコアを連結する
    line = ''
    for i, score in enumerate(scores):
        if i != 0:
            # 3イニングごとに広めに区切る
            if i % 3 == 0:
                line += '  '
            else:
                line += ' '
        line += score

    # 構築したスコア行を返す
    return line


def _format_pitcher(caption, name, result):
    """
    投手成績を構築する。

    :param caption: 見出し
    :type caption: str
    :param name: 投手名
    :type name: str
    :param result: 成績
    :type result: tuple
    :return: 投手成績
    :rtype: str
    """
    # 投手成績を構築する
    return '[{0}] {1} {2}勝{3}敗{4}Ｓ\n'.format(caption, name, *result) if result else ''


def _search_or_error(pattern, string):
    """
    re.search() を実行し、その結果を返す。
    ただし、結果がNoneだった場合はPyslashErrorを送出する。

    :param pattern: 正規表現パターン
    :type pattern: str
    :param string: 走査対象文字列
    :type string: str
    :return: マッチング結果
    :rtype: re.__Match
    """
    # re.search() の結果を返す
    m = re.search(pattern, string)
    if m:
        return m
    else:
        raise PyslashError('Pattern not found: %s %s' % (pattern, string))


def _find_or_error(bs, *args):
    """
    bs4.BeautifulSoup.find() を実行し、その結果を返す。
    ただし、結果がNoneだった場合はPyslashErrorを送出する。

    :param bs: findメソッドを実行するBeautifulSoupオブジェクト
    :type bs: BeautifulSoup
    :param args: findメソッドに渡す引数群
    :type args: list
    :return: 探索結果
    :rtype: bs4.element.Tag
    """
    # bs4.BeautifulSoup.find() の結果を返す
    result = bs.find(*args)
    if result:
        return result
    else:
        raise PyslashError()


def _add_space(*args):
    """
    指定された文字列のうち、最大長に満たなかった文字列の末尾に半角スペースを付与する。

    :param args: 対象の文字列群
    :type args: tuple
    :return: 編集後の文字列群
    :rtype: tuple
    """
    # スペースを付与する
    max_len = max(map(len, args))
    ret_val = map(lambda x: x.ljust(max_len), args)

    # 編集結果を返す
    return tuple(ret_val)


def _add_em_space(*args):
    """
    指定された文字列のうち、最大長に満たなかった文字列の末尾に全角スペースを付与する。

    :param args: 対象の文字列群
    :type args: tuple
    :return: 編集後の文字列群
    :rtype: tuple
    """
    # スペースを付与する
    max_len = max(map(len, args))
    ret_val = map(lambda x: x.ljust(max_len, '　'), args)

    # 編集結果を返す
    return tuple(ret_val)


def _space_padding(*args):
    """
    指定された文字列のうち、最大長に満たなかった文字列の先頭に半角スペースを付与する。

    :param args: 対象の文字列群
    :type args: tuple
    :return: 編集後の文字列群
    :rtype: tuple
    """
    # スペースを付与する
    max_len = max(map(len, args))
    ret_val = map(lambda x: x.rjust(max_len), args)

    # 編集結果を返す
    return tuple(ret_val)

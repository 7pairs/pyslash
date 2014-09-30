# -*- coding: utf-8 -*-

from collections import defaultdict
import datetime
import re
import urllib.request

from bs4 import BeautifulSoup

from .exception import InvalidTeamError, ParseError, ResultNotFoundError


# チーム短縮名変換テーブル
SHORT_TEAM_NAMES = {
    'l': '西武',
    'e': '楽天',
    'm': 'ロッテ',
    'h': 'ソフトバ',
    'bu': 'オリック',
    'f': '日本ハム',
    'g': '巨人',
    't': '阪神',
    'c': '広島',
    'd': '中日',
    'bs': 'ＤｅＮＡ',
    's': 'ヤクルト',
}


def get_score_table(team, day):
    """
    指定されたチーム、試合日のスコアテーブルを文字列として返す。

    :param team: チーム略称
    :type team: str
    :param day: 試合日
    :type day: datetime.datetime
    :return: スコアテーブル
    :rtype: str
    """
    # スコアテーブルのURLを取得する
    url = get_game_url(team, day) if day else get_today_game_url(team)

    # スコアテーブルを返す
    return get_score_table_by_url(url)


def get_score_table_by_url(url):
    """
    指定されたURLのスコアテーブルを文字列として返す。

    :param url: URL
    :type url: str
    :return: スコアテーブル
    :rtype: str
    """
    # スコアテーブルを構築する
    html = get_html(url)
    score_data = parse_score_table(html)
    ret_val = create_score_table(score_data, parse_date(url))

    # スコアテーブルを返す
    return ret_val


def get_game_url(team, day):
    """
    指定されたチーム、試合日のスコアテーブルのURLを返す。

    :param team: チーム略称
    :type team: str
    :param day: 試合日
    :type day: datetime.datetime
    :return: スコアテーブルのURL
    :rtype: str
    """
    # カレンダーのHTMLを取得する
    url = get_calendar_url(team, day)
    html = get_html(url)

    # スコアテーブルのURLを取得する
    pattern = r'/baseball/professional/score/%04d/\D+%04d%02d%02d\d+\.html' % (
        day.year,
        day.year,
        day.month,
        day.day
    )
    m = search_or_error(pattern, html)

    # 取得したURLを返す
    return 'http://www.nikkansports.com' + m.group(0)


def get_calendar_url(team, day):
    """
    指定されたチーム、日付のカレンダーのURLを返す。

    :param team: チーム略称
    :type team: str
    :param day: 日付
    :type day: datetime.datetime
    :return: カレンダーのURL
    :rtype: str
    """
    # チーム名をチェックする
    if team not in SHORT_TEAM_NAMES:
        raise InvalidTeamError()

    # URLを構築する
    url = 'http://www.nikkansports.com/baseball/professional/schedule/%04d/%s%04d%02d.html' % (
        day.year,
        team,
        day.year,
        day.month
    )

    # 構築したURLを返す
    return url


def get_html(url):
    """
    指定されたURLのHTMLを文字列として返す。

    :param url: URL
    :type url: str
    :return: HTML
    :rtype: str
    """
    # 指定されたURLのHTMLを返す
    with urllib.request.urlopen(url) as response:
        encoding = response.headers.get_content_charset() or 'utf-8'
        return response.read().decode(encoding)


def get_today_game_url(team):
    """
    指定されたチームの今日の試合スコアテーブルのURLを返す。

    :param team: チーム略称
    :type team: str
    :return: スコアテーブルのURL
    :rtype: str
    """
    # チームの短縮名を取得する
    try:
        short_name = SHORT_TEAM_NAMES[team]
    except KeyError:
        raise InvalidTeamError()

    # 全カードのスコアテーブルのURLを取得する
    html = get_html('http://www.nikkansports.com/')
    soup = BeautifulSoup(html)
    table = find_or_error(soup, 'table', {'summary': 'プロ野球の対戦表'})
    cards = table.find_all('tr')

    # 当該チームのスコアを探索する
    for card in cards:
        links = card.find_all('a')
        for link in links:
            m = re.search(short_name, link.string)
            if m:
                # 試合中/中止の場合はエラーとする
                inning = card.find('td', {'class': 'num'})
                if inning.string != '終了':
                    raise ResultNotFoundError()

                # スコアテーブルのURLを返す
                score = card.find('td', {'class': 'score'})
                return score.a.get('href')


def parse_score_table(html):
    """
    指定されたHTML文字列を解析し、スコアに関連する情報を格納した辞書を返す。

    :param html: HTML文字列
    :type html: str
    :return: スコア情報
    :rtype: dict
    """
    # 戻り値用の辞書
    ret_val = {}

    # BeautifulSoupオブジェクトを構築する
    soup = BeautifulSoup(html)

    # 先攻チーム/後攻チーム
    card = find_or_error(soup, 'h4', {'id': 'cardTitle'})
    m = search_or_error(r'([^\s]+)\s対\s([^\s]+)', card.string)
    ret_val['bat_first'] = m.group(2)
    ret_val['field_first'] = m.group(1)

    # 回戦
    match = find_or_error(soup, 'p', {'id': 'time'})
    m = search_or_error(r'(\d+)勝(\d+)敗(\d+)分け', match.string)
    ret_val['match'] = int(m.group(1)) + int(m.group(2)) + int(m.group(3))

    # 球場
    stadium = find_or_error(soup, 'p', {'class': 'data'})
    m = search_or_error(r'◇開始\d+時\d+分◇([^◇]+)◇観衆\d+人', stadium.string)
    ret_val['stadium'] = m.group(1)

    # スコア
    ret_val['score'] = []
    ret_val['total_score'] = []
    score = find_or_error(soup, 'table', {'class': 'scoreTable'})
    rows = score.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        ret_val['score'].append([x.string.strip().lower() for x in cols[1:-1]])
        ret_val['total_score'].append(int(cols[-1].string))
    for i, (top, bottom) in enumerate(zip(ret_val['score'][0], ret_val['score'][1])):
        # コールドゲームの場合に最終回以降の無駄な空白を除去する
        if top == '' and bottom == '':
            ret_val['score'][0] = ret_val['score'][0][:i]
            ret_val['score'][1] = ret_val['score'][1][:i]

    # 勝利投手/セーブ投手/敗戦投手
    pitcher = find_or_error(soup, 'table', {'class': 'pitcher'})
    rows = pitcher.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        status = cols[0].string
        if status == '○':
            ret_val['win'] = parse_pitcher(cols)
        elif status == 'Ｓ':
            ret_val['save'] = parse_pitcher(cols)
        elif status == '●':
            ret_val['lose'] = parse_pitcher(cols)

    # 本塁打
    ret_val['home_run'] = []
    footnotes = soup.find_all('dl', {'class': 'data'})
    for footnote in footnotes:
        if footnote.dt.string == '◇本塁打':
            # 打撃成績から本塁打の出たイニングを収集する
            home_run_innings = defaultdict(list)
            tables = soup.find_all('table', {'class', 'batter'})
            for i, table in enumerate(tables):
                rows = table.find_all('tr')

                # イニングを収集する
                inning_numbers = []
                cols = rows[0].find_all('th')
                for col in cols[8:]:
                    inning = col.string.strip()
                    if inning:
                        inning_numbers.append(int(inning))
                    else:
                        # 打者2巡目は見出しが空欄になっているため……
                        inning_numbers.append(inning_numbers[-1])

                # 本塁打を収集する
                for row in rows[1:]:
                    cols = row.find_all('td')
                    for j, col in enumerate(cols[8:]):
                        m = re.search(r'.本', col.string)
                        if m:
                            m = search_or_error(r'([^（]+)（[^）]+）', cols[1].string)
                            home_run_innings[m.group(1)].append(str(inning_numbers[j]) + '回' + ['表', '裏'][i])

            # 末尾の本塁打欄を解析する
            lines = footnote.find_all('dd')
            for line in lines:
                m = search_or_error(r'([^\d]+)(\d+)号（(ソロ|２ラン|３ラン|満塁)\d+m=([^）]+)）', line.string)
                ret_val['home_run'].append((
                    home_run_innings[m.group(1)].pop(0),
                    m.group(1),
                    int(m.group(2)),
                    m.group(3),
                    m.group(4)
                ))

            # 本塁打欄は1つしかないはず
            break

    # 構築した辞書を返す
    return ret_val


def parse_pitcher(node):
    """
    投手成績を解析し、勝利数、敗北数、セーブ数を返す。

    :param node: 投手成績のHTMLノード
    :type node: bs4.element.ResultSet
    :return: 解析結果
    :rtype: tuple
    """
    # 投手の名前を切り出す
    m = search_or_error(r'([^\s]+)\s（[^）]+）', node[1].string)

    # 解析結果を返す
    return m.group(1), int(node[2].string), int(node[3].string), int(node[4].string)


def parse_date(url):
    """
    指定されたURLを解析し、試合日を返す。

    :param url: URL
    :type url: str
    :return 試合日
    :rtype datetime.datetime
    """
    # URLから試合日を抽出する
    pattern = r'http://www\.nikkansports\.com/baseball/professional/score/\d{4}/\D+(\d{4})(\d{2})(\d{2})\d+\.html'
    m = search_or_error(pattern, url)

    # 抽出した日付を返す
    return datetime.datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))


def create_score_table(score_data, day):
    """
    スコア情報の格納された辞書をもとにスコアテーブルを構築する。

    :param score_data: スコア情報
    :type score_data: dict
    :return: スコアテーブル
    :rtype: str
    """
    # ヘッダ欄を構築する
    field_first = get_full_team_name(score_data['field_first'])
    bat_first = get_full_team_name(score_data['bat_first'])
    ret_val = '【%s vs %s 第%d回戦】\n' % (field_first, bat_first, score_data['match'])
    ret_val += '（%d年%d月%d日：%s）\n' % (
        day.year,
        day.month,
        day.day,
        get_full_stadium_name(score_data['stadium'])
    )
    ret_val += '\n'

    # スコア欄を構築する
    bat_first, field_first = add_zenkaku_space(bat_first, field_first)
    top_score, bottom_score = add_space(
        create_score_line(score_data['score'][0]),
        create_score_line(score_data['score'][1])
    )
    top_total_score, bottom_total_score = space_padding(
        str(score_data['total_score'][0]),
        str(score_data['total_score'][1])
    )
    ret_val += '%s  %s  %s\n' % (bat_first, top_score, top_total_score)
    ret_val += '%s  %s  %s\n' % (field_first, bottom_score, bottom_total_score)

    # 投手成績欄を構築する
    win = score_data.get('win')
    save = score_data.get('save')
    lose = score_data.get('lose')
    win_player, save_player, lose_player = add_zenkaku_space(
        win[0] if win else '',
        save[0] if save else '',
        lose[0] if lose else ''
    )
    pitcher = (
        create_pitcher_line('勝', win_player, win[1:] if win else None) +
        create_pitcher_line('Ｓ', save_player, save[1:] if save else None) +
        create_pitcher_line('敗', lose_player, lose[1:] if lose else None)
    )
    if pitcher:
        ret_val += '\n' + pitcher

    # 本塁打欄を構築する
    home_run = score_data.get('home_run')
    if home_run:
        ret_val += '\n'
        ret_val += '[本塁打]\n'

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
            ret_val += '  %s %s %2d号 %s （%s）\n' % (
                ' ' * (max_inning_len - len(line[0])) + line[0],
                line[1] + '　' * (max_player_len - len(line[1])),
                line[2],
                line[3] + '　' * (max_type_len - len(line[3])),
                line[4]
            )

    # 構築したスコアを返す
    return ret_val


def create_pitcher_line(caption, name, result):
    """
    投手成績(1行)を構築する。

    :param caption: 見出し
    :type caption: str
    :param name: 投手名
    :type name: str
    :param result: 成績
    :type result: tuple
    :return: 投手成績
    :rtype: str
    """
    # 投手成績を編集して返す
    return '[{0}] {1} {2}勝{3}敗{4}Ｓ\n'.format(caption, name, *result) if result else ''


# チーム名変換テーブル
FULL_TEAM_NAME = {
    '西武': '埼玉西武',
    '楽天': '東北楽天',
    'ロッテ': '千葉ロッテ',
    'ソフトバンク': '福岡ソフトバンク',
    '日本ハム': '北海道日本ハム',
    '巨人': '読売',
    '広島': '広島東洋',
    'ＤｅＮＡ': '横浜ＤｅＮＡ',
    'ヤクルト': '東京ヤクルト',        
}


def get_full_team_name(team_name):
    """
    指定されたチーム名を正式名称に変換する。

    @param team_name: チーム名
    @type team_name: str
    @return: 変換後のチーム名
    @rtype: str
    """
    # 変換テーブルを探索
    return FULL_TEAM_NAME.get(team_name, team_name)


# 球場名変換テーブル
FULL_STADIUM_NAME = {
    'コボスタ宮城': '楽天Koboスタジアム宮城',
    'ＱＶＣマリン': 'QVCマリンフィールド',
    'ヤフオクドーム': '福岡 ヤフオク!ドーム',
    '甲子園': '阪神甲子園球場',
    'マツダスタジアム': 'Mazda Zoom-Zoomスタジアム広島',
    '横浜': '横浜スタジアム',
    '神宮': '明治神宮野球場',
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
}


def get_full_stadium_name(stadium_name):
    """
    指定された球場名を正式名称に変換する。

    @param stadium_name: 球場名
    @type stadium_name: str
    @return: 変換後の球場名
    @rtype: str
    """
    # 変換テーブルを探索
    return FULL_STADIUM_NAME.get(stadium_name, stadium_name)


def find_or_error(bs, *args):
    """
    BeautifulSoupのfindメソッドを呼び出し、その結果を返す。
    findの結果がNoneだった場合はParseErrorを送出する。

    @param bs: findメソッドを呼び出すオブジェクト
    @type bs: bs4.BeautifulSoup
    @param args: findメソッドに渡す引数
    @type args: list
    @return: findの結果
    @rtype: bs4.element.Tag
    """
    # findメソッドを呼び出して結果を返す
    result = bs.find(*args)
    if result:
        return result
    else:
        raise ParseError()


def search_or_error(pattern, string):
    """
    re.search関数を呼び出し、その結果を返す。
    searchの結果がNoneだった場合はParseErrorを送出する。

    @param pattern: 正規表現
    @type pattern: str
    @param string: 走査対象
    @type string: str
    @return: マッチング結果
    @rtype: re.MatchObject
    """
    # searchメソッドを実行して結果を返す
    m = re.search(pattern, string)
    if m:
        return m
    else:
        raise ParseError()


def create_score_line(score):
    """
    スコア行(先攻のみ、もしくは後攻のみ)を構築する。

    @param score: 各イニングのスコア
    @type score: list
    @return: スコア行
    @rtype: str
    """
    # イニングスコアを連結
    retval = ''
    for i, run in enumerate(score):
        if i != 0:
            # 3イニングごとに広めに区切る
            if i % 3 == 0:
                retval += '  '
            else:
                retval += ' '
        retval += run

    # 構築したスコア行を返す
    return retval


def add_space(*args):
    """
    指定された文字列のうち、最大長に満たなかった文字列の末尾に半角スペースを付与する。

    @param args: 対象文字列
    @type args: list
    @return: 編集後の文字列
    @rtype: tuple
    """
    # スペースを付与
    max_len = max(map(len, args))
    retval = map(lambda x: x + ' ' * (max_len - len(x)), args)

    # 編集結果を返す
    return tuple(retval)


def add_zenkaku_space(*args):
    """
    指定された文字列のうち、最大長に満たなかった文字列の末尾に全角スペースを付与する。

    @param args: 対象文字列
    @type args: list
    @return: 編集後の文字列
    @rtype: tuple
    """
    # スペースを付与
    max_len = max(map(len, args))
    retval = map(lambda x: x + '　' * (max_len - len(x)), args)

    # 編集結果を返す
    return tuple(retval)


def space_padding(*args):
    """
    指定された文字列のうち、最大長に満たなかった文字列の先頭に半角スペースを付与する。

    @param args: 対象文字列
    @type args: list
    @return: 編集後の文字列
    @rtype: tuple
    """
    # スペースを付与
    max_len = max(map(len, args))
    retval = map(lambda x: ' ' * (max_len - len(x)) + x, args)

    # 編集結果を返す
    return tuple(retval)

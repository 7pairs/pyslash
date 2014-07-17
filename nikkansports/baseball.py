# -*- coding: utf-8 -*-

from collections import defaultdict
import datetime
import re
import sys
import urllib.request

from bs4 import BeautifulSoup

try:
    from nikkansports.exception import InvalidTeamError, ParseError, ResultNotFoundError
except ImportError:
    from exception import InvalidTeamError, ParseError, ResultNotFoundError


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


def parse_date(target=''):
    """
    指定された文字列を年と月に分割して返す。

    @param target: 年月
    @type target: str
    @return: 年、月
    @rtype: tupple
    """
    # システム日付を取得
    today = datetime.datetime.today()

    # 年と月を分割
    if len(target) == 6:
        return (target[:4], target[4:])
    elif len(target) == 4:
        return ('20' + target[:2], target[2:])
    elif len(target) == 2:
        return (str(today.year), target)
    elif len(target) == 0:
        return (str(today.year), '%02d' % today.month)


def get_url(team):
    """
    指定されたチームの試合結果のURLを文字列として返す。

    @param team: チーム名
    @type team: str
    @return: URL
    @rtype: str
    """
    # チーム短縮名を取得
    try:
        short_name = SHORT_TEAM_NAMES[team]
    except KeyError:
        raise InvalidTeamError()

    # 試合結果のURLを取得
    html = get_html('http://www.nikkansports.com/')
    soup = BeautifulSoup(html)
    table = find_or_error(soup, 'table', {'summary': 'プロ野球の対戦表'})
    cards = table.find_all('tr')
    for card in cards:
        links = card.find_all('a')
        for link in links:
            m = re.search(short_name, link.string)
            if m:
                num = card.find('td', {'class': 'num'})
                if num.string != '終了':
                    raise ResultNotFoundError()
                score = card.find('td', {'class': 'score'})
                return score.a.get('href')
    

def get_score_table(url):
    """
    指定されたURLからスコアテーブルを取得して文字列として返す。

    @param url: URL
    @type url: str
    @return: スコアテーブル
    @rtype: str
    """
    # スコアテーブルを構築
    html = get_html(url)
    data = create_dict(html)
    retval = create_score_table(data)

    # 構築したスコアテーブルを返す
    return retval


def get_html(url):
    """
    指定されたURLからHTMLを取得して文字列として返す。

    @param url: URL
    @type url: str
    @return: HTML文字列
    @rtype: str
    """
    # 指定されたURLを開く
    html = ''
    try:
        with urllib.request.urlopen(url) as response:
            encoding = response.headers.get_content_charset()
            if not encoding:
                encoding = 'utf-8'
            html = response.read().decode(encoding)
    except Exception as e:
        pass

    # HTMLを文字列として返す
    return html


def create_dict(html):
    """
    指定されたHTML文字列を解析し、スコアに関連する情報を格納した辞書を返す。

    @param html: HTML文字列
    @type html: str
    @retrun: スコア情報
    @rtype: dict
    """
    # 戻り値用辞書
    retval = {}

    # 引数をもとにBeautifulSoupオブジェクトを構築
    soup = BeautifulSoup(html)

    # 先攻チーム/後攻チーム
    card = find_or_error(soup, 'h4', {'id': 'cardTitle'})
    m = search_or_error(r'([^\s]+)\s対\s([^\s]+)', card.string)
    retval['bat_first'] = m.group(2)
    retval['field_first'] = m.group(1)

    # 回戦
    match = find_or_error(soup, 'p', {'id': 'time'})
    m = search_or_error(r'(\d+)勝(\d+)敗(\d+)分け', match.string)
    retval['match'] = int(m.group(1)) + int(m.group(2)) + int(m.group(3))

    # 試合日
    date = find_or_error(soup, 'p', {'id': 'upDate'})
    m = search_or_error(r'(\d+)年(\d+)月(\d+)日', date.span.string)
    retval['date'] = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    # 球場
    stadium = find_or_error(soup, 'p', {'class': 'data'})
    m = search_or_error(r'◇開始\d+時\d+分◇([^◇]+)◇観衆\d+人', stadium.string)
    retval['stadium'] = m.group(1)

    # スコア
    retval['score'] = []
    retval['total_score'] = []
    score = find_or_error(soup, 'table', {'class': 'scoreTable'})
    rows = score.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        retval['score'].append([x.string.lower() for x in cols[1:-1]])
        retval['total_score'].append(int(cols[-1].string))

    # 勝利投手/セーブ投手/敗戦投手
    pitcher = soup.find('table', {'class': 'pitcher'})
    if pitcher:
        rows = pitcher.find_all('tr')
        for row in rows[1:]:
            cols = row.find_all('td')
            status = cols[0].string
            if status == '○':
                retval['win'] = parse_pitcher(cols)
            elif status == 'Ｓ':
                retval['save'] = parse_pitcher(cols)
            elif status == '●':
                retval['lose'] = parse_pitcher(cols)

    # 本塁打
    retval['homerun'] = []
    footnotes = soup.find_all('dl', {'class': 'data'})
    if footnotes:
        for footnote in footnotes:
            if footnote.dt.string == '◇本塁打':
                # テーブルスコアから本塁打の出たイニングを収集
                innings = defaultdict(list)
                tables = soup.find_all('table', {'class', 'batter'})
                for i, table in enumerate(tables):
                    rows = table.find_all('tr')
                    for row in rows[1:]:
                        cols = row.find_all('td')
                        for j, col in enumerate(cols[8:]):
                            m = re.search(r'.本', col.string)
                            if m:
                                m = search_or_error(r'([^（]+)（[^）]+）', cols[1].string)
                                innings[m.group(1)].append(str(j + 1) + '回' + ['表', '裏'][i])

                # 末尾の本塁打欄を解析
                lines = footnote.find_all('dd')
                for line in lines:
                    m = search_or_error(r'([^\d]+)(\d+)号（(ソロ|２ラン|３ラン|満塁)\d+m=([^）]+)）', line.string)
                    retval['homerun'].append([
                        innings[m.group(1)].pop(0),
                        m.group(1),
                        int(m.group(2)),
                        m.group(3),
                        m.group(4)
                    ])

                # 本塁打欄は1つしかないはず
                break

    # 構築した辞書を返す
    return retval


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
}


def get_full_stadium_name(stadium_name):
    """
    指定された球場名を正式名称に変換する。

    @param team_name: 球場名
    @type team_name: str
    @return: 変換後の球場名
    @rtype: str
    """
    # 変換テーブルを探索
    return FULL_STADIUM_NAME.get(stadium_name, stadium_name)


def create_score_table(data):
    """
    スコア情報の格納された辞書をもとにスコアテーブルを構築する。

    @param data: スコア情報
    @type data: dict
    @return: スコアテーブル
    @rtype: str
    """
    # ヘッダ
    field_first = get_full_team_name(data['field_first'])
    bat_first = get_full_team_name(data['bat_first'])
    retval = '【%s vs %s 第%d回戦】\n' % (field_first, bat_first, data['match'])
    retval += '（%d年%d月%d日：%s）\n' % (
        data['date'].year,
        data['date'].month,
        data['date'].day,
        get_full_stadium_name(data['stadium'])
    )
    retval += '\n'

    # スコア
    bat_first, field_first = add_zenkaku_space(bat_first, field_first)
    top_score, bottom_score = add_space(create_score_line(data['score'][0]), create_score_line(data['score'][1]))
    top_total_score, bottom_total_score = space_padding(str(data['total_score'][0]), str(data['total_score'][1]))

    retval += '%s  %s  %s\n' % (bat_first, top_score, top_total_score)
    retval += '%s  %s  %s\n' % (field_first, bottom_score, bottom_total_score)
    retval += '\n'

    # 投手成績
    win_pitcher, save_pitcher, lose_pitcher = add_zenkaku_space(
        data.get('win', [''])[0],
        data.get('save', [''])[0],
        data.get('lose', [''])[0]
    )

    if 'win' in data:
        retval += '[勝] %s %d勝%d敗%dＳ\n' % tuple([win_pitcher] + data['win'][1:])
    if 'save' in data:
        retval += '[Ｓ] %s %d勝%d敗%dＳ\n' % tuple([save_pitcher] + data['save'][1:])
    if 'lose' in data:
        retval += '[敗] %s %d勝%d敗%dＳ\n' % tuple([lose_pitcher] + data['lose'][1:])

    # 本塁打
    if data.get('homerun'):
        retval += '\n'
        retval += '[本塁打]\n'

        inning_max_len = 0
        player_max_len = 0
        type_max_len = 0
        for line in data['homerun']:
            inning_max_len = max(inning_max_len, len(line[0]))
            player_max_len = max(player_max_len, len(line[1]))
            type_max_len = max(type_max_len, len(line[3]))

        for line in data['homerun']:
            line[0] = ' ' * (inning_max_len - len(line[0])) + line[0]
            line[1] += '　' * (player_max_len - len(line[1]))
            line[3] += '　' * (type_max_len - len(line[3]))
            retval += '  %s %s %2d号 %s （%s）\n' % tuple(line)

    # 構築したスコアを返す
    return retval

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


def parse_pitcher(cols):
    """
    投手成績を解析する。

    @param cols: 投手成績のHTMLノード
    @type cols: bs4.element.ResultSet
    @return: 解析結果
    @rtype: list
    """
    # 投手の名前を切り出す
    m = re.search(r'([^\s]+)\s（[^）]+）', cols[1].string)
    if not m:
        raise ParseError()

    # 解析結果を返す
    return [m.group(1), int(cols[2].string), int(cols[3].string), int(cols[4].string)]


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


if __name__ == '__main__':
    # 引数をチェック
    if len(sys.argv) != 2:
        print('Usage: python %s url' % sys.argv[0])
        quit()

    # スコアテーブルを出力
    score_table = get_score_table(sys.argv[1])
    print(score_table)


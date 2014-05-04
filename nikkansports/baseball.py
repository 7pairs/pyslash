# -*- coding: utf-8 -*-

from collections import defaultdict
import datetime
import re
import urllib.request

from bs4 import BeautifulSoup

from nikkansports.exception import ParseError


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
    m = re.search(r'([^\s]+)\s対\s([^\s]+)', card.string)
    if not m:
        raise ParseError()
    retval['bat_first'] = m.group(2)
    retval['field_first'] = m.group(1)

    # 回戦
    match = find_or_error(soup, 'p', {'id': 'time'})
    m = re.search(r'(\d+)勝(\d+)敗(\d+)分け', match.string)
    if not m:
        raise ParseError()
    retval['match'] = int(m.group(1)) + int(m.group(2)) + int(m.group(3))

    # 試合日
    date = find_or_error(soup, 'p', {'id': 'upDate'})
    m = re.search(r'(\d+)年(\d+)月(\d+)日', date.span.string)
    if not m:
        raise ParseError()
    retval['date'] = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    # 球場
    stadium = find_or_error(soup, 'p', {'class': 'data'})
    m = re.search(r'◇開始\d+時\d+分◇([^◇]+)◇観衆\d+人', stadium.string)
    if not m:
        raise ParseError()
    retval['stadium'] = m.group(1)

    # スコア
    retval['score'] = []
    retval['total_score'] = []
    score = find_or_error(soup, 'table', {'class': 'scoreTable'})
    rows = score.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        retval['score'].append([int(x.string) if x.string.isdigit() else 'x' for x in cols[1:-1]])
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
                                m = re.search(r'([^（]+)（[^）]+）', cols[1].string)
                                innings[m.group(1)].append(str(j + 1) + '回' + ['表', '裏'][i])

                # 末尾の本塁打欄を解析
                lines = footnote.find_all('dd')
                for line in lines:
                    m = re.search(r'([^\d]+)(\d+)号（([^\d]+)\d+m=([^）]+)）', line.string)
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


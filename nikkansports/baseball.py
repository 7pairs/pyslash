# -*- coding: utf-8 -*-

import urllib.request

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


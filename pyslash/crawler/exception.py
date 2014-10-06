# -*- coding: utf-8 -*-


class InvalidTeamError(Exception):
    """
    指定されたチーム名が不正であることを示す例外。
    """


class ResultNotFoundError(Exception):
    """
    指定された条件の試合が見つからないことを示す例外。
    """


class ParseError(Exception):
    """
    文字列の解析に失敗したことを示す例外。
    """

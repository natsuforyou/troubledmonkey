#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .const import Const


class TroubleLog:
    __url: str
    __normal_response: str
    __change_type: int
    __changed_response: str
    # __is_crash: bool = False
    # __exception: Exception = None

    def __init__(self, url: str, normal_response: str, change_type: int, changed_response: str):
        self.__url = url
        self.__normal_response = normal_response
        self.__change_type = change_type
        self.__changed_response = changed_response

    # def crash(self, is_crash: bool, exception: Exception):
    #     self.__is_crash = is_crash
    #     self.__exception = exception

    def commit(self):
        __cursor = Const.conn.cursor()
        sql = 'INSERT INTO [troubled_log] ([REQUEST_URL], [RESPONSE], [CHANGE_TYPE], [CHANGED_RESPONSE]) ' \
              'VALUE (?, ?, ?, ?, ?)'
        __cursor.execute(sql, (self.__url, self.__normal_response, self.__change_type, self.__changed_response))

        __cursor.close()
        Const.conn.commit()

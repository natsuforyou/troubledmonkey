#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api, Resource, reqparse
from ui.platfrom import Platform
from ui.ios import IOS
from ui.android import Android
import mysql.connector
from troubled.tamper import Tamper


class Message:
    @staticmethod
    def success(data=None):
        return {'code': 0, 'msg': '成功', 'data': data}

    @staticmethod
    def fail():
        return {'code': 1, 'msg': '失败', 'data': None}


app = Flask(__name__)
api = Api(app)

conn = mysql.connector.connect(host='127.0.0.1', user='tm', password='monkey', database='monkey')

tamper = Tamper()


# 启动case
@app.route('/start', methods=['GET'])
def start_ui(case_id: str, platform: str) -> None:
    platform = get_instance_of_platform(platform)
    platform.start()


def get_instance_of_platform(platform: str) -> Platform:
    if platform.upper() == 'IOS':
        return IOS()
    if platform.upper() == 'ANDROID':
        return Android()


# 获取某个case某次执行的进度
@app.route('/schedule', methods=['GET'])
def schedule(log_id: str):
    pass


# 篡改结果
@app.route('/tamper', methods=['POST'])
def tamper(url: str, content: str) -> str:
    return tamper.troubled(url, content)


@api.resource('/case')
class Case(Resource):
    # 新增case
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('schema', type=str)
        parser.add_argument('keywords', type=str)
        parser.add_argument('comments', type=str)
        args = parser.parse_args()

        _cursor = conn.cursor()
        _cursor.execute('INSERT INTO url_case (`NAME`,`SCHEMA`, `KEYWORDS`, `COMMENTS`) VALUES (?, ?, ?, ?)', args)
        return Message.success()


@api.resource('/cases')
class Cases(Resource):
    # 获取cases
    def get(self):
        _cursor = conn.cursor()
        values = _cursor.execute('SELECT * FROM url_case')
        return Message.success(values)


@api.resource('/task')
class Task(Resource):
    # 新增task
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('team', type=str)
        parser.add_argument('platform', type=str)
        parser.add_argument('comments', type=str)
        args = parser.parse_args()
        _cursor = conn.cursor()
        _cursor.execute('INSERT INTO test_task (`NAME`,`TEAM`, `PLATFORM`, `COMMENTS`) VALUES (?, ?, ?, ?)', args)
        return Message.success()


@api.resource('/tasks')
class Tasks(Resource):
    # 获取case
    def get(self):
        _cursor = conn.cursor()
        values = _cursor.execute('SELECT * FROM test_task')
        return Message.success(values)


# @api.resource('/logs')
# class Log(Resource):
#     # 获取日志
#     @app.route('/logs', methods=['GET'])
#     def logs(self):
#         _cursor = conn.cursor()
#         values = _cursor.execute('SELECT * FROM troubled_log')
#         _cursor.close()
#         return values
#
#     # 获取某个日志
#     @app.route('/log/<log_id>', methods=['GET'])
#     def log(log_id: str):
#         _cursor = conn.cursor()
#         values = _cursor.execute('SELECT * FROM troubled_log WHERE LOG_ID = ?', log_id)
#         _cursor.close()
#         return values


if __name__ == '__main__':
    app.run('0.0.0.0', threaded=True, debug=True)

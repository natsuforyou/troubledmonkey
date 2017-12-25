#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from ui.platfrom import Platform
from ui.ios import IOS
from ui.android import Android
import mysql.connector
from troubled.tamper import Tamper
import json

app = Flask(__name__)
api = Api(app)
requestParser = reqparse.RequestParser()

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
def tamper(url: str, content: str):
    return tamper.troubled(url, content)


@api.resource('/schemas')
class Schemas(Resource):
    # 新增url schema
    def post(self) -> None:
        parser = reqparse.RequestParser()
        parser.add_argument('schema', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('url', type=str)
        args = parser.parse_args()

        _cursor = conn.cursor()
        _cursor.execute('INSERT INTO url_schema (SCHEMA, NAME, URL) VALUES (?, ?, ?)', args)
        _cursor.close()
        pass

    # 获取url schema
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int)
        parser.add_argument('pageSize', type=int)
        args = parser.parse_args()
        _cursor = conn.cursor()
        values = _cursor.execute('SELECT * FROM url_schema')
        _cursor.close()
        return values


@api.resource('/cases')
class Cases(Resource):
    # 新增case
    def post(self) -> None:
        args = request.values
        _cursor = conn.cursor()
        _cursor.execute('INSERT INTO test_case VALUES (?, ?, ?)', ())
        _cursor.close()
        pass

    # 获取case
    def get(self):
        args = request.values
        _cursor = conn.cursor()
        values = _cursor.execute('SELECT * FROM test_case')
        _cursor.close()
        return values


@api.resource('/logs')
class Log(Resource):
    # 获取日志
    @app.route('/logs', methods=['GET'])
    def logs(self):
        _cursor = conn.cursor()
        values = _cursor.execute('SELECT * FROM troubled_log')
        _cursor.close()
        return values

    # 获取某个日志
    @app.route('/log/<log_id>', methods=['GET'])
    def log(log_id: str):
        _cursor = conn.cursor()
        values = _cursor.execute('SELECT * FROM troubled_log WHERE LOG_ID = ?', log_id)
        _cursor.close()
        return values


if __name__ == '__main__':
    app.run('0.0.0.0', threaded=True, debug=True)

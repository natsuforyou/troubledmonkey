from flask import jsonify, json
from models import Case, Task, TroubledLog, TroubledLogDetail


class Response:
    @staticmethod
    def success(data=None):
        return jsonify({'code': 0, 'msg': '成功', 'data': data})

    @staticmethod
    def fail(data=None):
        return jsonify({'code': 1, 'msg': '失败', 'data': data})


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Case):
            return obj.__str__()
        if isinstance(obj, Task):
            return obj.__str__()
        if isinstance(obj, TroubledLog):
            return obj.__str__()
        if isinstance(obj, TroubledLogDetail):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)

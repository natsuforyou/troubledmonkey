#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import sys

from base import ChangeType


class Monkey(object):
    def support(self, change_type: int) -> bool: pass

    def make_trouble(self, body, name, value) -> None: pass


class ChangeToNegativeMonkey(Monkey):
    def support(self, change_type: int) -> bool:
        return change_type == ChangeType.CHANGE_TO_NEGATIVE

    def make_trouble(self, body, name, value) -> None:
        body[name] = -sys.maxsize


class ChangeToBigMonkey(Monkey):
    def support(self, change_type: int) -> bool:
        return change_type == ChangeType.CHANGE_TO_BIG

    def make_trouble(self, body, name, value) -> None:
        body[name] = sys.maxsize


class ChangeToNumberMonkey(Monkey):
    def support(self, change_type: int) -> bool:
        return change_type == ChangeType.CHANGE_TO_NUMBER

    def make_trouble(self, body, name, value) -> None:
        body[name] = random.randint(0, sys.maxsize)


class ChangeToStringMonkey(Monkey):
    def support(self, change_type: int) -> bool:
        return change_type == ChangeType.CHANGE_TO_STRING

    def make_trouble(self, body, name, value) -> None:
        body[name] = str(value)


class ChangeToNoneMonkey(Monkey):
    def support(self, change_type: int) -> bool:
        return change_type == ChangeType.CHANGE_TO_NULL

    def make_trouble(self, body, name, value) -> None:
        body[name] = None


class ChangeToDelMonkey(Monkey):
    def support(self, change_type: int) -> bool:
        return change_type == ChangeType.CHANGE_TO_DEL

    def make_trouble(self, body, name, value) -> None:
        body.pop(name)


class ChangeToAddMonkey(Monkey):
    def support(self, change_type: int) -> bool:
        return change_type == ChangeType.CHANGE_TO_ADD

    def make_trouble(self, body, name, value) -> None:
        body.pop(name)
        body['crashString'] = 1


class Monkeys(Monkey):
    # 篡改器的数组
    monkeys = []
    monkeyCache = {}
    trouble_count = 0

    def __init__(self, *args: Monkey):
        self.monkeys = args

    @staticmethod
    def default_instance():
        return Monkeys(ChangeToNegativeMonkey(),
                       ChangeToBigMonkey(),
                       ChangeToNumberMonkey(),
                       ChangeToStringMonkey(),
                       ChangeToNoneMonkey(),
                       ChangeToDelMonkey(),
                       ChangeToAddMonkey())

    def support(self, change_type: int) -> bool:
        if len(self.monkeys) > 0:
            return True

    def make_trouble(self, body, name, value) -> None:
        monkey = self.find_suitable_monkey(self.trouble_count % len(self.monkeys))
        self.trouble_count += 1
        if monkey is None:
            raise RuntimeError('')
        return monkey.make_trouble(body, name, value)

    def find_suitable_monkey(self, change_type) -> Monkey:
        result = self.monkeyCache.get(change_type)
        if result is None:
            for monkey in self.monkeys:
                if monkey.support(change_type):
                    result = monkey
                    self.monkeyCache[change_type] = monkey
                    break
        return result

    def troubled(self, url, content) -> dict:
        json_object = json.loads(content)

        trouble_count = self.do_troubled(url, '', json_object)
        changed_response = json.dumps(json_object)

        return {'trouble_count': trouble_count, 'changed_response': changed_response}

    def do_troubled(self, url, name, element, _trouble_count=None):
        if _trouble_count is None:
            _trouble_count = self.trouble_count
        if isinstance(element, list):
            return self.do_troubled(url, name + '[0]', element[0], _trouble_count)
        elif isinstance(element, dict):
            for key, value in element.items():
                if isinstance(value, list) | isinstance(value, dict):
                    return self.do_troubled(url, name + '[' + key + ']', value, _trouble_count)
                else:
                    if _trouble_count < len(self.monkeys):
                        self.make_trouble(element, key, value)
                        return _trouble_count
                    else:
                        _trouble_count -= len(self.monkeys)

    def count(self, element, trouble_count: int = 0) -> int:
        if isinstance(element, list):
            return self.count(element[0], trouble_count)
        elif isinstance(element, dict):
            for key, value in element.items():
                if isinstance(value, list) | isinstance(value, dict):
                    return self.count(value, trouble_count)
                else:
                    trouble_count += len(self.monkeys)
        return trouble_count


# 全局变量
monkeys = Monkeys.default_instance()

if __name__ == '__main__':
    _content = {
        'returnCode': 200,
        'returnMsg': '操作成功',
        'data': {
            'count': 3,
            'list': [
                {'name': '钱嘉鑫', 'age': 24, 'a': 2},
                {'name': '钱嘉鑫', 'age': 24, 'b': 2},
                {'name': '钱嘉鑫', 'age': 24}
            ]
        }
    }

    o = json.dumps(_content)
    _body = json.loads(o)
    a = monkeys.count(_body)
    print(a)

    # for x in range(0, 100):

    # monkeys.do_troubled('', '', body)

    # print(body)

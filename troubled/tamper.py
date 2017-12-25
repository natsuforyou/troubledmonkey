#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from TMonkey.troubled.monkey import MonkeyComposite
from TMonkey.troubled.changetype import ChangeType
from TMonkey.troubled.troubledlog import TroubleLog
import json


class Tamper:
    __monkey = MonkeyComposite()
    __troubled_count = {}

    def select_change_type(self, url, name):
        troubled_log_by_url = self.__troubled_count.get(url)
        if troubled_log_by_url is None:
            troubled_log_by_url = {name: 1}
            self.__troubled_count[url] = troubled_log_by_url
            return 1
        else:
            changed_type = troubled_log_by_url.get(name)
            if changed_type is None:
                troubled_log_by_url[name] = 1
                return 1
            else:
                change_type = changed_type + 1
                if change_type > ChangeType.MAX_SIZE:
                    return -1
                else:
                    troubled_log_by_url[name] = change_type
                    return change_type

    def troubled(self, url, content: bytes) -> bytes:
        body = json.loads(content, encoding='utf-8')
        normal_response = json.dumps(body)
        selected_change_type = self.do_troubled(url, '', body)
        changed_response = json.dumps(body)
        TroubleLog(url, normal_response, selected_change_type, changed_response).commit()
        return changed_response.encode('utf-8')

    def do_troubled(self, url, name, element) -> int:
        if isinstance(element, list):
            return self.do_troubled(url, name + '_array', element[0])
        elif isinstance(element, dict):
            for key, value in element.items():
                if isinstance(value, list) | isinstance(value, dict):
                    return self.do_troubled(url, name + '_' + key, value)
                else:
                    selected_change_type = self.select_change_type(url, name + '_' + key)
                    if selected_change_type > 0:
                        self.__monkey.tramp(element, key, value, selected_change_type)
                        return selected_change_type

    def get_trouble_log_list(self):
        return self.__troubled_count


if __name__ == '__main__':
    a = Tamper()

    content = {
        'returnCode': 200,
        'returnMsg': '操作成功',
        'data': {
            'count': 3,
            'list': [
                {'name': '钱嘉鑫', 'age': 24},
                {'name': '钱嘉鑫', 'age': 24},
                {'name': '钱嘉鑫', 'age': 24}
            ]
        }
    }

    str = json.dumps(content)

    for x in range(0, 100):
        body = json.loads(str)
        a.do_troubled('nihao', 'response', body)
        print(body)
        print(a.get_trouble_log_list())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from TMonkey.troubled import changetype
import sys
import random
import json


class Monkey(object):
    def support(self, change_type: int) -> bool: pass

    def tramp(self, body, name, value, change_type): pass

    def do_tramper(self, body, name, value) -> None: pass


class ChangeToNegativeMonkey(Monkey):
    def support(self, change_type: int) -> bool:
        return change_type == changetype.ChangeType.CHANGE_TO_NEGATIVE

    def do_tramper(self, body, name, value) -> None:
        body[name] = -sys.maxsize


class ChangeToBigMonkey(Monkey):
    def support(self, change_type: int) -> bool:
        return change_type == changetype.ChangeType.CHANGE_TO_BIG

    def do_tramper(self, body, name, value) -> None:
        body[name] = sys.maxsize


class ChangeToNumberMonkey(Monkey):
    def support(self, change_type: int) -> bool:
        return change_type == changetype.ChangeType.CHANGE_TO_NUMBER

    def do_tramper(self, body, name, value) -> None:
        body[name] = random.randint(0, sys.maxsize)


class ChangeToStringMonkey(Monkey):
    def support(self, change_type: int) -> bool:
        return change_type == changetype.ChangeType.CHANGE_TO_STRING

    def do_tramper(self, body, name, value) -> None:
        body[name] = str(value)


class ChangeToNoneMonkey(Monkey):
    def support(self, change_type: int) -> bool:
        return change_type == changetype.ChangeType.CHANGE_TO_NULL

    def do_tramper(self, body, name, value) -> None:
        body[name] = None


class ChangeToDelMonkey(Monkey):
    def support(self, change_type: int) -> bool:
        return change_type == changetype.ChangeType.CHANGE_TO_DEL

    def do_tramper(self, body, name, value) -> None:
        body.pop(name)


class ChangeToAddMonkey(Monkey):
    def support(self, change_type: int) -> bool:
        return change_type == changetype.ChangeType.CHANGE_TO_ADD

    def do_tramper(self, body, name, value) -> None:
        body.pop(name)
        body['crashString'] = 1


class MonkeyComposite(Monkey):
    tamper_list = [
                    # ChangeToNegativeMonkey(),
                   # ChangeToBigMonkey(),
                   # ChangeToNumberMonkey(),
                   # ChangeToStringMonkey(),
                   # ChangeToNoneMonkey(),
                   # ChangeToDelMonkey(),
                   ChangeToAddMonkey()]

    def support(self, change_type: int) -> bool:
        if len(self.tamper_list) > 0:
            return True

    def tramp(self, body, name, value, change_type) -> None:
        for tamper in self.tamper_list:
            if tamper.support(change_type):
                tamper.do_tramper(body, name, value)

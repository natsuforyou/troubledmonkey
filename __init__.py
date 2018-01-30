db_url = 'mysql+pymysql://tm:monkey@127.0.0.1:3306/monkey?charset=utf8'


class ChangeType(object):
    CHANGE_TO_NEGATIVE = 0
    CHANGE_TO_BIG = 1
    CHANGE_TO_NUMBER = 2
    CHANGE_TO_STRING = 3
    CHANGE_TO_NULL = 4
    CHANGE_TO_DEL = 5
    CHANGE_TO_ADD = 6


class TroubledLogState:
    PROCESSING = 'PROCESSING'
    DONE = 'DONE'


class TroubledLogDetailState:
    UI_START = 'UI_START'
    MONKEY_DONE = 'MONKEY_DONE'
    DONE = 'DONE'


class OSType:
    IOS = 'IOS'
    ANDROID = 'ANDROID'

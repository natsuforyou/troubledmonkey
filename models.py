# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import db_url

Base = declarative_base()
metadata = Base.metadata

db = create_engine(db_url)
session = sessionmaker(bind=db)()


class Case(Base):
    __tablename__ = 'case'

    ID = Column(Integer, primary_key=True)
    NAME = Column(String(20))
    SCHEMA = Column(String(100))
    KEYWORDS = Column(String(100))
    RESPONSE = Column(String(500))
    TOTAL_COUNT = Column(Integer)
    COMMENTS = Column(String(50))

    def __init__(self, **kwargs):
        self.NAME = kwargs.get('name')
        self.SCHEMA = kwargs.get('schema')
        self.KEYWORDS = kwargs.get('keywords')
        self.RESPONSE = kwargs.get('response')
        self.TOTAL_COUNT = kwargs.get('total_count')
        self.COMMENTS = kwargs.get('comments')

    def __str__(self):
        return {'id': self.ID,
                'name': self.NAME,
                'schema': self.SCHEMA,
                'keywords': self.KEYWORDS,
                'total_count': self.TOTAL_COUNT,
                'comments': self.COMMENTS}


class Task(Base):
    __tablename__ = 'task'

    ID = Column(Integer, primary_key=True)
    NAME = Column(String(20))
    TEAM = Column(String(10))
    PLATFORM = Column(String(20))
    CASES = Column(String(100), nullable=False)
    COMMENTS = Column(String(50))

    def __init__(self, obj):
        self.NAME = obj.get('name')
        self.SCHEMA = obj.get('team')
        self.KEYWORDS = obj.get('platform')
        self.CASES = obj.get('cases')
        self.COMMENTS = obj.get('comments')

    def __str__(self):
        return {'id': self.ID,
                'name': self.NAME,
                'team': self.TEAM,
                'platform': self.PLATFORM,
                'cases': self.CASES,
                'comments': self.COMMENTS}


class TroubledLog(Base):
    __tablename__ = 'troubled_log'

    ID = Column(Integer, primary_key=True)
    TASK_ID = Column(Integer)
    TASK_NAME = Column(String(20))
    STATE = Column(String(10))
    CREATE_TIME = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    LOG_SIZE = Column(Integer)
    OFFSET = Column(Integer)

    def __init__(self, **kwargs):
        self.TASK_ID = kwargs.get('task_id')
        self.TASK_NAME = kwargs.get('task_name')
        self.STATE = kwargs.get('state')
        self.LOG_SIZE = kwargs.get('log_size')
        self.OFFSET = kwargs.get('offset')

    def __str__(self):
        return {'id': self.ID,
                'taskId': self.TASK_ID,
                'taskName': self.TASK_NAME,
                'state': self.STATE,
                'createTime': self.CREATE_TIME,
                'logSize': self.LOG_SIZE,
                'offset': self.OFFSET}


class TroubledLogDetail(Base):
    __tablename__ = 'troubled_log_detail'

    ID = Column(Integer, primary_key=True)
    LOG_ID = Column(Integer)
    CASE_ID = Column(Integer)
    CASE_NAME = Column(String(20))
    TROUBLED_STRATEGY = Column(String(20))
    TROUBLED_RESPONSE = Column(String)
    STATE = Column(String)
    IS_CRASH = Column(String(5))
    CRASH_LOG = Column(String(500))
    SCREEN_SHOT = Column(String)
    CREATE_TIME = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    def __init__(self, **kwargs):
        self.LOG_ID = kwargs.get('log_id')
        self.CASE_ID = kwargs.get('case_id')
        self.CASE_NAME = kwargs.get('case_name')
        self.TROUBLED_STRATEGY = kwargs.get('troubled_strategy')
        self.TROUBLED_RESPONSE = kwargs.get('troubled_response')
        self.STATE = kwargs.get('state')
        self.IS_CRASH = kwargs.get('is_crash')
        self.CRASH_LOG = kwargs.get('crash_log')
        self.SCREEN_SHOT = kwargs.get('screen_shot')

    def __str__(self):
        return {'id': self.ID,
                'logId': self.LOG_ID,
                'caseId': self.CASE_ID,
                'caseName': self.CASE_NAME,
                'troubledStrategy': self.TROUBLED_STRATEGY,
                'troubledResponse': self.TROUBLED_RESPONSE,
                'isCrash': self.IS_CRASH,
                'crashLog': self.CRASH_LOG,
                'screenShot': self.SCREEN_SHOT,
                'createTime': self.CREATE_TIME}

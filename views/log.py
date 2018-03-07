from flask import Blueprint

from models import TroubledLog, TroubledLogDetail, session_maker
from views.wrapper import Response

log = Blueprint('log', __name__)


# 列出所有日志
@log.route(rule='/logs', methods=['GET'])
def get_logs():
    session = session_maker()
    values = session.query(TroubledLog).all()
    return Response.success(values)


# 获取某一个日志
@log.route(rule='/logs/<int:log_id>', methods=['GET'])
def get_log(log_id: str):
    session = session_maker()
    values = session.query(TroubledLogDetail).filter(TroubledLogDetail.LOG_ID == log_id).all()
    return Response.success(values)

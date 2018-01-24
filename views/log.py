from flask import Blueprint

from models import TroubledLog, TroubledLogDetail, session
from views.wrapper import Response

log = Blueprint('log', __name__)


# 列出所有日志
@log.route(rule='/logs', methods=['GET'])
def get_logs():
    values = session.query(TroubledLog).all()
    return Response.success(values)


# 获取某一个日志
@log.route(rule='/logs/<int:log_id>', methods=['GET'])
def get_log(log_id: str):
    values = session.query(TroubledLogDetail).filter(TroubledLogDetail.ID == log_id)
    return Response.success(values)

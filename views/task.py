from flask import Blueprint
from flask_restful import reqparse

from models import Case, Task, TroubledLog, session_maker
from ui import OS
from views.wrapper import Response
from base import TroubledLogState

task = Blueprint('task', __name__)


# 获取所有task
@task.route(rule='/tasks', methods=['GET'])
def get_tasks():
    session = session_maker()
    values = session.query(Task).all()
    return Response.success(values)


# 新增一个task
@task.route(rule='/tasks', methods=['PUT'])
def add_task():
    session = session_maker()
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('team', type=str)
    parser.add_argument('platform', type=str)
    parser.add_argument('cases', type=str)
    parser.add_argument('comments', type=str)
    args = parser.parse_args()
    session.add(Task(args))
    session.commit()
    return Response.success()


# 启动case
@task.route('/tasks/<task_id>', methods=['PUT'])
def start_task(task_id: str):
    session = session_maker()
    _processing_logs = session.query(TroubledLog).filter(TroubledLog.TASK_ID == task_id).filter(
        TroubledLog.STATE == TroubledLogState.PROCESSING).all()

    if len(_processing_logs) != 0:
        raise RuntimeError('当前有任务正在执行中')

    _task = session.query(Task).filter(Task.ID == task_id).one_or_none()
    if _task is None:
        raise RuntimeError('无法执行该条任务，因为该任务不存在！')
    session.add(
        TroubledLog(task_id=task_id, task_name=_task.NAME, state=TroubledLogState.PROCESSING, log_size=1000, offset=0))
    session.commit()

    _troubled_log = session.query(TroubledLog).filter(TroubledLog.TASK_ID == task_id).filter(
        TroubledLog.STATE == TroubledLogState.PROCESSING).one_or_none()

    _case_id = _task.CASES
    _cases = session.query(Case).filter(Case.ID.in_(_case_id.split(','))).all()

    os = OS.instance(_task.PLATFORM)
    os.start(_troubled_log, *_cases)

    session.query(TroubledLog).filter(TroubledLog.TASK_ID == task_id).filter(
        TroubledLog.STATE == TroubledLogState.PROCESSING).update({TroubledLog.STATE: TroubledLogState.DONE})
    session.commit()
    return Response.success()

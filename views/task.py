from flask import Blueprint
from flask_restful import reqparse

from models import Task, TroubledLog, session
from ui.android import Android
from ui.ios import IOS
from ui.platfrom import Platform
from views.wrapper import Response

task = Blueprint('task', __name__)


# 获取所有task
@task.route(rule='/tasks', methods=['GET'])
def get_tasks():
    values = session.query(Task).all()
    return Response.success(values)


# 新增一个task
@task.route(rule='/tasks', methods=['PUT'])
def add_task():
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
def start_ui(task_id: str) -> None:
    task = session.query(Task).filter(Task.ID == task_id).one_or_none()
    if task is None:
        raise RuntimeError('无法执行该条任务，因为该任务不存在！')
    platform = get_instance_of_platform(task.PLATFORM)
    session.add(TroubledLog(task_id=task_id, task_name=task.NAME, status='PROCESSING', log_size=1000, offset=0))
    session.commit()
    platform.start()


def get_instance_of_platform(platform: str) -> Platform:
    if platform.upper() == 'IOS':
        return IOS()
    if platform.upper() == 'ANDROID':
        return Android()

from flask import Blueprint
from flask_restful import reqparse

from models import Case, session
from views.wrapper import Response

case = Blueprint('case', __name__)


# 列出所有case
@case.route(rule='/cases', methods=['GET'])
def get_cases():
    values = session.query(Case).all()
    return Response.success(values)


# 新增一个case
@case.route(rule='/cases', methods=['PUT'])
def add_case():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('schema', type=str)
    parser.add_argument('keywords', type=str)
    parser.add_argument('comments', type=str)
    args = parser.parse_args()
    session.add(Case(args))
    session.commit()
    return Response.success()

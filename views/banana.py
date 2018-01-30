from flask import Blueprint
from flask_restful import reqparse
import json

from models import Case, TroubledLog, TroubledLogDetail, session
from monkeys import monkeys
from .. import TroubledLogState, TroubledLogDetailState

banana = Blueprint('banana', __name__)


# 篡改结果
@banana.route('/bananas', methods=['POST'])
def banana() -> str:
    parser = reqparse.RequestParser()
    parser.add_argument('url', type=str)
    parser.add_argument('param', type=str)
    parser.add_argument('body', type=str)
    args = parser.parse_args()

    url: str = args.get('url')
    param: str = args.get('param')
    body: str = args.get('body')

    _troubled_log = session.query(TroubledLog).filter(
        TroubledLog.STATE == TroubledLogState.PROCESSING).one_or_none()

    _troubled_log_detail: TroubledLogDetail = session.query(TroubledLogDetail).filter(
        TroubledLogDetail.ID == _troubled_log.TASK_ID).filter(
        TroubledLog.STATE == TroubledLogDetailState.UI_START).one_or_none()

    if _troubled_log_detail is not None:

        _case_id = _troubled_log_detail.CASE_ID
        _case = session.query(Case).filter(Case.ID == _case_id).one_or_none()

        _keywords = _case.KEYWORDS

        if url.__contains__(_keywords) | param.__contains__(_keywords):
            _troubled_result = monkeys.troubled(args.get('url'), args.get('body'))
            _changed_response = json.dumps(_troubled_result.get('changed_response'))
            _troubled_log_detail.TROUBLED_STRATEGY = _troubled_result.get('trouble_count')
            _troubled_log_detail.TROUBLED_RESPONSE = _changed_response
            _troubled_log_detail.STATE = TroubledLogDetailState.MONKEY_DONE
            session.update(_troubled_log_detail)
            session.commit()
            return _changed_response

        else:
            return body
    else:
        return body

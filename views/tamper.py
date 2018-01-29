from flask import Blueprint

from troubled.monkeys import MonkeyZoo

from models import Case, session

tamper = Blueprint('tamper', __name__)
monkey_zoo = MonkeyZoo()


# 篡改结果
@tamper.route('/tamper', methods=['POST'])
def tamper(log_id, case_id: str, url: str, content: str) -> str:
    case = session.query(Case).filter(Case.ID == case_id).one_or_none
    return monkey_zoo.troubled(log_id, case, url, content)

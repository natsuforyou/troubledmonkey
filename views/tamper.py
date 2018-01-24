from flask import Blueprint

from troubled.tamper import Tamper

tampers = Blueprint('tampers', __name__)
tamper = Tamper()


# 篡改结果
@tampers.route('/tamper', methods=['POST'])
def tamper(url: str, content: str) -> str:
    return tamper.troubled(url, content)

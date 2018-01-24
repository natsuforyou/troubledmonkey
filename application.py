#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask

from views.case import case
from views.log import log
from views.tamper import tampers
from views.task import task
from views.wrapper import Response, CustomEncoder

app = Flask(__name__)
app.register_blueprint(case)
app.register_blueprint(task)
app.register_blueprint(log)
app.register_blueprint(tampers)
app.json_encoder = CustomEncoder


@app.errorhandler(Exception)
def handle_exception(error):
    print(error)
    return Response.fail(str(error))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)

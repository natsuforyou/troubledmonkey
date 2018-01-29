from mitmproxy import http
import re
import requests

keywords: str


def response(flow: http.HTTPFlow) -> None:
    url = flow.request.pretty_url
    content = flow.request.content.decode()

    if url.__contains__(keywords) | content.__contains__(keywords):
        flow.response.content = do(url, flow.response.content.decode()).encode()


        # if url.startswith('https://piao.o2o.cmbchina.com/yummy-portal/JSONServer/execute.do'):
        #     if re.match('.*PRD0020.*', url) is not None:
        #         flow.response.content = do(url, flow.response.content.decode()).encode()
        #
        #     elif re.match('.*SI_PRD0026.*', flow.request.content.decode("utf-8")) is not None:
        #         flow.response.content = do(url, flow.response.content.decode()).encode()
        #
        #     elif url.startswith('https://movie.o2o.cmbchina.com/MovieApi/cinema/allcinema'):
        #         flow.response.content = do(url, flow.response.content.decode()).encode()


def do(url: str, content: str) -> str:
    res = requests.post(url='localhost:8080/tamper', data={'log_id': '', 'case_id': '', 'url': url, 'content': content})
    data = res.text
    return data

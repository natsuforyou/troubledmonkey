from mitmproxy import http
import requests


def response(flow: http.HTTPFlow) -> None:
    url = flow.request.pretty_url
    param = flow.request.content.decode()
    body = flow.response.content.decode()
    res = requests.post(url='localhost:8080/bananas', data={'url': url, 'param': param, 'body': body})
    flow.response.content = res.text.encode()

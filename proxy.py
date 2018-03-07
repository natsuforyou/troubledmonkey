from mitmproxy import http
import requests


def response(flow: http.HTTPFlow) -> None:
    url = flow.request.pretty_url
    content_type = flow.response.headers.get('Content-Type')
    print(content_type)
    if (content_type is not None) and content_type.__contains__('application/json'):
        param = flow.request.content.decode()
        body = flow.response.content.decode()
        res = requests.post(url='http://localhost:8081/bananas', data={'url': url, 'param': param, 'body': body})
        flow.response.content = res.text.encode()

import requests.models
# from test_demo.middleware.handler import Handler
import json
# logger = Handler.logger


class Response(object):

    def __init__(self, url, method):
        self.url = url
        self.method = method

    def get_response(self, **kwargs):
        res = requests.request(self.method, self.url, **kwargs)
        try:
            return res.json()
        except json.decoder.JSONDecodeError:
            print('返回数据不是json格式')


if __name__ == '__main__':
    url1 = 'http://apis.juhe.cn/mobile/get'
    data = {
        "phone": "18190992526",
        "key": "0aff0a88da3f5742ce42e88ccf3d2ae4"
    }
    res1 = Response(url1, 'post').get_response(data=data)
    print(res1)
    print(type(res1))

    url2 = 'https://www.baidu.com'
    res2 = Response(url2, 'get').get_response()
    print(res2)

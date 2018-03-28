# @Time    : 2018/3/23 15:24
# @Author  : Niyoufa
import urllib.parse
import tornado.gen
import tornado.httpclient

def get_client(use_proxy=False):
    if use_proxy == True:
        tornado.httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
    client = tornado.httpclient.AsyncHTTPClient()
    return client

@tornado.gen.coroutine
def get(url, params=None, **kwargs):
    if params and isinstance(params, dict):
        url += "?"
        url += urllib.parse.urlencode(params)

    http_client = get_client()
    response = yield http_client.fetch(url, **kwargs)
    return response

async def async_get(url, params=None, **kwargs):
    if params and isinstance(params, dict):
        url += "?"
        url += urllib.parse.urlencode(params)

    http_client = get_client()
    response = await http_client.fetch(url, **kwargs)
    return response

@tornado.gen.coroutine
def gets(urls, **kwargs):
    http_client = get_client()
    responses = yield [http_client.fetch(url, **kwargs) for url in urls]
    return responses
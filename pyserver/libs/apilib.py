# @Time    : 2018/3/23 15:24
# @Author  : Niyoufa
import urllib.parse
import tornado.gen
import tornado.httpclient
from pyserver.libs.singletonlib import Singleton


class AsyncCallAPI(Singleton):
    def get_client(self, **kwargs):
        use_proxy = kwargs.get("use_proxy")
        if use_proxy == True:
            tornado.httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
        client = tornado.httpclient.AsyncHTTPClient()
        return client

    @tornado.gen.coroutine
    def request(self, method, url, callback, **kwargs):
        def handle_response(response):
            if callback and callable(callback):
                callback(response)

        request = tornado.httpclient.HTTPRequest(url, method, **kwargs)
        response = yield self.get_client(**kwargs).fetch(request, **kwargs)
        return response

    @tornado.gen.coroutine
    def get(self, url, params=None, callback=None, **kwargs):
        """
        Sends a GET request.
        :param url: 
        :param params: 
        :param callback: 
        :param kwargs: 
        :return: 
        """
        if params and isinstance(params, dict):
            url += "?"
            url += urllib.parse.urlencode(params)

        if "error_callback" in kwargs:
            error_callback = kwargs.get("error_callback")
            del kwargs["error_callback"]
        else:
            error_callback = None

        try:
            response = yield self.request("GET", url, callback, **kwargs)
            return response
        except tornado.httpclient.HTTPError as err:
            # utils.error_print("url:{url}, err:{err}".format(url=url, err=err))
            if error_callback and callable(error_callback):
                error_callback("get", url, callback, err=err, **kwargs)
# @Time    : 2018/3/20 16:01
# @Author  : Niyoufa
import asyncio
import tornado.web
import tornado.gen
import tornado.httpclient
from torserver.libs.mysqllib import test


class MainHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS + ('PROPFIND',)

    def initialize(self, **kwargs):
        print("initialize", kwargs)
        print(self.settings)
        print(self.current_user, self.xsrf_token)

    @tornado.gen.coroutine
    def prepare(self):
        super(MainHandler, self).prepare()
        self.path_args = [1,2]
        self.path_kwargs = {"a":1}
        print(self.path_args, self.path_kwargs)
        self.param1 = self.get_argument("param1", None)

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch, "https://www.baidu.com")
        print(response)
        data = yield test()
        print(data)
        self.write("hello")

    def on_finish(self):
        # 也会阻塞
        super(MainHandler, self).on_finish()

handlers = [
    (r"/api/main", MainHandler, dict(version="v0.0.0_0")),
]
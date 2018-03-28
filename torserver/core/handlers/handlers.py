# @Time    : 2018/3/23 16:34
# @Author  : Niyoufa
import tornado.web
import tornado.gen


class BaseHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS + ()

    def initialize(self, **kwargs):
        pass

    @tornado.gen.coroutine
    def prepare(self):
        pass

    def on_finish(self):
        pass
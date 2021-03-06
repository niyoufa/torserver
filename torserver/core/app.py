# @Time    : 2018/3/12 15:33
# @Author  : Niyoufa
import tornado.web
import tornado.concurrent
import tornado.httpserver
import tornado.ioloop
from tornado.options import options

from torserver.libs.constlib import const
from torserver.libs.optionslib import parse_options
from torserver.core.module import Module


class Application(tornado.web.Application):

    def __init__(self, module:Module):

        settings = dict(
            debug = const.DEBUG,
            autoreload = const.AUTORELOAD,
            cookie_secret = const.COOKIE_SECRET,
            xsrf_cookies = const.XSRF_COOKIES,
        )

        static_path = module.get_static_absolute_path()
        if static_path:
            settings.update(dict(static_path=static_path))

        template_path = module.get_template_absolute_path()
        if template_path:
            settings.update(dict(template_path=template_path))

        redis_config = module.get_redis_config()
        if redis_config:
            settings.update(dict(pycket={
                'engine': 'redis',
                'storage': {
                    'host': redis_config["host"],
                    'port': redis_config["port"],
                    'db_sessions': redis_config["db_sessions"],
                    'db_notifications': redis_config["db_notifications"],
                    'max_connections': redis_config["max_connections"],
                },
                'cookies': {
                    'expires_days': 7,
                    # 'expires':None, #秒
                },
            }))
        super(Application, self).__init__(module.handlers, **settings)
        self.executor = tornado.concurrent.futures.ThreadPoolExecutor()

def run():
    if not const.SETTINGS_MODULE:
        raise const.ConstSettingNotExistError("can't find settings.py file")

    parse_options()
    module = Module()
    app = Application(module)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(module.port)
    http_server.start(options.num_processes)
    tornado.ioloop.IOLoop.current().add_callback(lambda: print("server start, port: {port}!".format(port=module.port)))
    tornado.ioloop.IOLoop.current().start()
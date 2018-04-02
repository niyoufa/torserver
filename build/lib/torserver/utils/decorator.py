# @Time    : 2018/3/31 下午4:12
# @Author  : Niyoufa
import time
import traceback
import functools

from tornado.concurrent import Future
from tornado import gen
from tornado.options import options
from tornado.web import asynchronous
from tornado.ioloop import IOLoop

from torserver.core.exceptions import HandlerError

def handler_except(func):
    """请求响应异常处理装饰器"""

    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except HandlerError as err:
            self.set_status(err.status_code)
            self.finish({"code":err.status_code, "msg":err.reason})
        except:
            self.set_status(500)
            self.finish({"code":500, "msg":"{msg}".format(msg=traceback.format_exc())})
    return wrapper

def future_except(func):
    """协程-请求响应异常处理装饰器"""

    @gen.coroutine
    def wrapper(self, *args, **kwargs):
        try:
            self._auto_finish = False
            future = func(self, *args, **kwargs)
            if isinstance(future, Future):
                yield future
        except HandlerError as err:
            self.set_status(err.status_code)
            self.finish({"code":err.status_code, "msg":err.reason})
        except:
            self.set_status(500)
            self.finish({"code": 500, "msg": "{error}".format(
                error=traceback.format_exc()
            )})
    return wrapper

def threadpoll_executor(func):

    @asynchronous
    @functools.wraps(func)
    def _wrapper(self, *args, **kwargs):
        """
        下面的callback必须在主线程执行
        self.write(),self.finish()等都不是线程安全的
        直接在handler中return，该结果即future.result(), 后续将被self.write(result)
        不要在子线程中执行self.write(),因为这并非线程安全的方法
        通过ioloop.IOLoop.instance().add_callback的方式，将其交给主线程执行
        ioloop提供的add_callback是线程安全的
        """

        def callback(future):
            try:
                self.finish(future.result())
            except HandlerError as err:
                self.set_status(err.status_code)
                self.finish({"code": err.status_code, "msg": err.reason})
            except:
                self.set_status(500)
                self.finish({"code": 500, "msg": "{error}".format(
                    error=traceback.format_exc()
                )})

        _future = self.application.executor.submit(
            functools.partial(func, self, *args, **kwargs)
        )
        IOLoop.current().add_future(_future, callback)
    return _wrapper

def time_consume(func):
    """函数耗时计算"""

    def wrapper(*args,**kwargs):
        start_time = time.time()
        result = func(*args,**kwargs)
        time_useage = time.time() - start_time
        if options.func_time_monitor:
            print("{func_name}:{time_useage}ms".format(
                func_name = func.__name__,
                time_useage  = int(time_useage*1000)
            ))
        return result
    return wrapper
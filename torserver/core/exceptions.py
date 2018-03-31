# @Time    : 2018/3/12 17:48
# @Author  : Niyoufa
from tornado.web import HTTPError


class HandlerError(HTTPError):
    """请求响应处理异常类, 继承该异常类的异常会被全局捕捉，详见utils/decorator.py"""


class MissingArgumentError(HandlerError):
    """缺失请求参数错误"""

    def __init__(self, arg_name):
        super(MissingArgumentError, self).__init__(
            400, '缺失请求参数 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '缺失请求参数 %s' % arg_name
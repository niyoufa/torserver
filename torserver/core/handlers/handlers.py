# @Time    : 2018/3/23 16:34
# @Author  : Niyoufa
from http import HTTPStatus
from tornado import escape
from tornado.web import RequestHandler
from tornado import gen

from torserver.utils import http_status
responses = {v: v.phrase for v in HTTPStatus.__members__.values()}
responses.update({v: v.phrase for v in http_status.HTTPStatus.__members__.values()})

from torserver.core.exceptions import MissingArgumentError


class BaseHandler(RequestHandler):
    """请求和响应处理基类"""

    SUPPORTED_METHODS = RequestHandler.SUPPORTED_METHODS + ()

    def initialize(self, **kwargs):
        """作为URL规范的第三个参数会作为关键词参数传给该方法"""
        pass

    @gen.coroutine
    def prepare(self):
        """在请求方法 get、post等执行前调用，进行通用的初始化，支持协程"""
        pass

    def on_finish(self):
        """请求方法结束发送响应给客户端后调用，和prepare对应，进行清理，日志处理"""
        pass

    def on_connection_close(self):
        """客户端关闭连接后调用，清理和长连接相关的资源"""
        pass

    def set_default_headers(self):
        """在请求开始时设置请求头部"""

    def _get_argument(self, name, default, source, strip=True):
        """获取参数"""
        args = self._get_arguments(name, source, strip=strip)
        if not args:
            if default is self._ARG_DEFAULT:
                raise MissingArgumentError(name)
            return default
        return args[-1]

    def set_status(self, status_code, reason=None):
        self._status_code = status_code
        if reason is not None:
            self._reason = escape.native_str(reason)
        else:
            try:
                self._reason = responses[status_code]
            except KeyError:
                raise ValueError("未知状态码 %d", status_code)

    def files(self):
        files = []
        if self.request.files:
            request_files = self.request.files.get("file")
            for file in request_files:
                content_type = file.get("content_type")
                filename = file.get("filename")
                body = file.get("body").decode()
                files.append(dict(
                    filename=filename,
                    content_type=content_type,
                    body=body,
                ))
        return files
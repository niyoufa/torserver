# @Time    : 2018/3/20 14:07
# @Author  : Niyoufa
import os
import sys
import traceback
from tornado.options import options
from torserver.libs.constlib import const
from torserver.utils.print import error_print


class ModuleNotExistsError(Exception):
    """
    模块不存在错误
    """


class ModuleConfigError(Exception):
    """
    模块配置错误
    """


class Module(object):
    """
    模块
    """

    def __init__(self, module_name):
        self.module_name = module_name or "default"

        if self.module_name not in const.MODULES:
            raise ModuleNotExistsError("module not exists：{module_name}".format(module_name=module_name))

        self.module_config = const.MODULES[self.module_name]
        if not isinstance(self.module_config, dict) or "":
            raise ModuleConfigError("module config error format：{module_config}".format(module_config=self.module_config))

        self.handlers = []
        self.handlers.extend(self.load_third_module())
        self.handlers.extend(self.load_module())
        self.print_handlers()

        self.port = options.port or self.module_config.get("port")
        if not isinstance(self.port, int):
            raise TypeError("port must be int")

    def get_static_absolute_path(self):
        static_path = self.module_config.get("static_path") or options.static_path
        if static_path and not static_path.endswith("/"):
            static_path += "/"
        return os.path.join(const.BASE_DIR, static_path + "static")

    def get_template_absolute_path(self):
        template_path = self.module_config.get("template_path") or options.template_path
        if template_path and not template_path.endswith("/"):
            template_path += "/"
        return os.path.join(const.BASE_DIR, template_path + "templates")

    def get_redis_config(self):
        DATABASES = const.DATABASES
        redis_configs = {}
        for k, v in DATABASES.items():
            if v.get("type") == "redis":
                redis_configs.update({k:v})
        return redis_configs.get(options.redis)

    def print_handlers(self):
        for handler in self.handlers:
            print(handler[0])

    def load_module(self):
        module_path = self.module_config.get("module_path")
        if not type(module_path) == list:
            module_path = [module_path]
        handlers = []
        print("load module...")
        print("[{module_name}]".format(module_name=self.module_name))
        for path in module_path:
            print("'{path}'".format(path=path))
            sub_module_hanlders = []
            try:
                __import__(path)
                module = sys.modules[path]
                module_hanlders = getattr(module, "handlers", None)
                if isinstance(module_hanlders, list):
                    sub_module_hanlders.extend(module_hanlders)
            except:
                info = traceback.format_exc()
                error_print("{path} load error, {info}".format(path=path, info=info))
            else:
                handlers.extend(sub_module_hanlders)
        return handlers

    def load_third_module(self):
        # TODO 加载第三方模块
        handlers = []
        return handlers
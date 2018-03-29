# @Time    : 2018/3/12 16:41
# @Author  : Niyoufa
import os
import importlib
ENVIRONMENT_VARIABLE = "SETTINGS_MODULE"


class _const(object):
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    class ConstSettingNotExistError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("can't change const %s" % name)
        if not name.isupper():
            raise self.ConstCaseError(
                'const name "%s" is not all uppercase' %
                name)
        self.__dict__[name] = value

    def __getattr__(self, item):
        if item not in self.__dict__:
            return None
        else:
            return super(_const, self).__getattribute__(item)


const = _const()
try:
    settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
    if settings_module:
        settings = importlib.import_module(settings_module)
        for setting in dir(settings):
            if setting.isupper():
                setting_value = getattr(settings, setting)
                setattr(const, setting, setting_value)
except BaseException:
    raise const.ConstSettingNotExistError("can't find settings.py file")

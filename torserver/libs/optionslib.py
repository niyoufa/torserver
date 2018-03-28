# @Time    : 2018/3/20 14:20
# @Author  : Niyoufa
import os
import importlib
ENVIRONMENT_VARIABLE = "OPTIONS_MODULE"
from tornado.options import parse_command_line

def parse_options():
    options_module_name = os.environ.get(ENVIRONMENT_VARIABLE)
    importlib.import_module(options_module_name)
    parse_command_line()

def get_options_module():
    options_module_name = os.environ.get(ENVIRONMENT_VARIABLE)
    options_module = importlib.import_module(options_module_name)
    return options_module

# @Time    : 2018/3/12 16:42
# @Author  : Niyoufa


import os

# 服务器调试模式, 值为False时不自动重启服务器
DEBUG = False

# 是否自检重启
AUTORELOAD = True

# cookie_secret
COOKIE_SECRET = "2379874hsdhf0234990sdhsaiuofyasop977djdj"

# xsrf_cookies
XSRF_COOKIES = True

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 模块配置，可以在配置文件中配置，也可以在ModuleModel存储模块信息
MODULES = {
    "default": {
        "module_path": ["test_port.handlers"],
        "name": "",
        "description": "",
        "port": 8069,
        "static_path": "",
        "template_path": "",
        "command_path": "",
    },
}

# 允许访问的HOST配置
ALLOWED_HOSTS = []

# 第三方模块
INSTALLED_MODULES = []

# 账号配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'labourlaw',
        'USER':'labor',
        'PASSWORD':'!labor@2017#',
        'HOST':'180.96.11.78',
        'PORT':'3309',
    },
    'redis': {
        'host': 'localhost',
        'port': '6379',
        'db_sessions': 10,
        'db_notifications':11,
        'max_connections':2**31,
        'type': 'redis',
    },
    'es_test': {
        'name' : 'test',
        "timeout" : 60,
        "http_auth" : [
            "aegis",
            "shield"
        ],
        "hosts" : [
            "192.168.11.99:9200"
        ],
        'type': 'elasticsearch',
    },
    'es_backup': {
        "name" : "backup",
        "timeout" : 60,
        "http_auth" : [
            "aegisuser",
            "aegisshield"
        ],
        "hosts" : [
            "hotbkes.aegis-info.com:9255",
            "hotbkes2.aegis-info.com:9255"
        ],
        'type': 'elasticsearch',
    },
    'es_product': {
        "name" : "product",
        "timeout" : 60,
        "http_auth" : [
            "python",
            "XK3cFTp0Noci"
        ],
        "hosts" : [
            "web.aegis-info.com:9200",
            "web2.aegis-info.com:9200"
        ],
        'type': 'elasticsearch',
    },
    'mongodb_test': {
        "host": "192.168.11.99",
        "port": 9933,
        "replicaset": "gtSet",
        'type': 'mongodb',
    },
    'mongodb_product': {
        "host": "180.96.11.71",
        "port": 10040,
        "type": "mongodb",
    }
}



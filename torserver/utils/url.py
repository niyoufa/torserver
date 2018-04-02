# @Time    : 2018/4/2 11:13
# @Author  : Niyoufa
import re

def validate(url):
    regex = "^(https?)://.+$"
    if not re.match(regex, url):
        raise Exception("url format error： {url}".format(url=url))
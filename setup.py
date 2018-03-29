# @Time    : 2018/3/27 15:49
# @Author  : Niyoufa
from setuptools import find_packages, setup

setup(
    name='torserver',
    version='2.0',
    author="niyoufa",
    author_email="niyoufa@aegis-data.cn",
    packages=find_packages(),
    license = "BSD",
    scripts = ["torserver/bin/torserver-admin.py"],
    url="http://www.niyoufa.com",
    description="A web application framework base on tornado and other async libraries."
)
# @Time    : 2018/3/27 15:49
# @Author  : Niyoufa
from setuptools import find_packages, setup

setup(
    name = 'torserver',
    version = '2.0',
    author = "niyoufa",
    author_email = "niyoufa@aegis-data.cn",
    packages = find_packages(),
    include_package_data = True,
    data_files = [
        ("torserver/conf/project_template/project_name", ["torserver/conf/project_template/project_name/__init__.py-tpl"]),
        ("torserver/conf/project_template/project_name", ["torserver/conf/project_template/project_name/options.py-tpl"]),
        ("torserver/conf/project_template/project_name", ["torserver/conf/project_template/project_name/run.py-tpl"]),
        ("torserver/conf/project_template/project_name", ["torserver/conf/project_template/project_name/settings.py-tpl"]),
    ],
    license = "BSD",
    scripts = ["torserver/bin/torserver-admin.py"],
    url="http://www.niyoufa.com",
    description="A web application framework base on tornado and other async libraries."
)
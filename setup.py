# @Time    : 2018/3/27 15:49
# @Author  : Niyoufa
import os
from setuptools import find_packages, setup

def traverse_tree(path, file_handle=None):
    if not os.path.abspath(path):
        raise Exception("path is not exists")

    for root, dirs, files in os.walk(path):
        if callable(file_handle):
            for file in files:
                file_handle(root, file)

def get_template_files():
    data_files = []
    def file_handle(root, file):
        data_files.append((root, [os.path.join(root, file)]))

    traverse_tree("torserver/conf", file_handle=file_handle)
    import pdb
    pdb.set_trace()
    return data_files

setup(
    name = 'torserver',
    version = '2.0',
    author = "niyoufa",
    author_email = "niyoufa@aegis-data.cn",
    packages = find_packages(),
    include_package_data = True,
    data_files = get_template_files(),
    license = "BSD",
    scripts = ["torserver/bin/torserver-admin.py"],
    url="http://www.niyoufa.com",
    description="A web application framework base on tornado and other async libraries."
)
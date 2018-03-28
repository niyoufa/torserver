# @Time    : 2018/3/29 上午12:28
# @Author  : Niyoufa
import os

def traverse_tree(path, file_handle=None, dir_handle=None):
    if not os.path.abspath(path):
        raise Exception("path is not exists")
    for root, dirs, files in os.walk(path):
        if callable(file_handle):
            for file in files:
                file_handle(root, file)
        if callable(dir_handle):
            for dir in dirs:
                traverse_tree(os.path.join(root, dir), file_handle, dir_handle)

if __name__ == "__main__":
    traverse_tree(".", file_handle=lambda x:print(x))
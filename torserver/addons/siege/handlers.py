# @Time    : 2018/4/2 10:55
# @Author  : Niyoufa
import os
import uuid
import json
import pandas
from collections import OrderedDict

from torserver.libs.constlib import const
from torserver.core.handlers import handlers
from torserver.core.exceptions import MissingArgumentError
from torserver.utils import decorator
from torserver.utils import url

SIEGE = {
    "Trans Rate": "每秒事务处理量",
    "Throughput": "吞吐率",
    "Elap Time": "测试用时",
    "Failed": "失败传输次数",
    "Date & Time": "日期",
    "OKAY": "OKAY",
    "Data Trans": "测试传输数据量",
    "Concurrent": "并发用户数",
    "Trans": "访问次数",
    "Resp Time": "平均响应时间"
}


class SiegeHandler(handlers.BaseHandler):

    def prepare(self):
        self.concurrent = int(self.get_argument("concurrent", 15))
        self.reps = self.get_argument("reps", 1)
        self.file = self.get_argument("file", None)
        self.url = self.get_argument("url", None)

    @decorator.threadpoll_executor
    def get(self, *args, **kwargs):
        result = self.init_response_data()
        self.options = ""
        self.options += " -c {concurrent}".format(concurrent = self.concurrent)
        self.options += " -r {reps}".format(reps = self.reps)

        siege_path = os.path.join(const.BASE_DIR, "siege")
        if not os.path.isdir(siege_path):
            os.makedirs(siege_path)

        siege_id = str(uuid.uuid4())
        log_file = os.path.join(siege_path, "{siege_id}.siege".format(siege_id=siege_id))
        self.options += " --log={log_file}".format(
            log_file = log_file,
        )

        if self.file:
            with open(self.file, "r") as f:
                for line in f.readlines():
                    url.validate(line.strip())
            self.options += " -f {file}".format(file = self.file)
            os.system("siege {options}".format(
                options = self.options,
            ))
        elif self.url:
            url.validate(self.url)
            os.system("siege {options} {URL}".format(
                options = self.options,
                URL = self.url
            ))
        else:
            raise MissingArgumentError("参数url, file 至少一个不为空")

        data = json.loads(pandas.read_csv(log_file).to_json())
        for k, v in data.items():
            result.setdefault("data", OrderedDict()).update({SIEGE[k.strip()]:v["0"]})

        return result


handlers = [
    (r"/siege", SiegeHandler),
]



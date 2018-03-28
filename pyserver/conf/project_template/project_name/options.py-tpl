# @Time    : 2018/3/12 16:44
# @Author  : Niyoufa

from tornado.options import define


define("module_name", default="", help="API模块名称")
define("port", type=int, help="指定启动端口")
define("num_processes", default=1, help="tornado进程数")
define("redis", default="redis", help="指定使用的redis")
define("es", default="product", help="指定使用的es集群")
define("mongodb", default="product", help="指定使用的mongodb集群， test:测试；product:生产")
define("cache", default=False, type=bool, help="是否加载缓存")
define("func_time_monitor", default=True, type=bool, help="接口性能监控")
define("api_log", default=False, type=bool, help="接口日志")
define("static_path", default="", type=str, help="静态文件路径")
define("template_path", default="", type=str, help="模板文件路径")


def add_options_arguments(parser):
    parser.add_argument(
        '--module_name',
        help='模块名称',
    )
# @Time    : 2018/3/25 下午9:35
# @Author  : Niyoufa

from torserver.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    创建项目
    """

    def handle(self, *args, **options):
        print(args, options)
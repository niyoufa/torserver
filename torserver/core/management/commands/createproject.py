# @Time    : 2018/3/25 下午9:35
# @Author  : Niyoufa
import os
import shutil
from importlib import import_module
from torserver.core import template
from torserver.core.management.base import BaseCommand
from torserver.core.management.base import CommandError
from torserver.utils import dir
from torserver.utils.print import green_print


class Command(BaseCommand):
    """
    创建项目
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "projectname",
            help = ("项目名称"),
            type = lambda x:self.check_projectname(x)
        )
        parser.add_argument(
            "--projectpath",
            help = ("项目路径, 默认为当前路径"),
            default = self.get_default_projectpath(),
            type = lambda x:self.check_projectpath(x)
        )

    def check_projectname(self, projectname):
        if not projectname:
            raise CommandError("you must provide a projectname")
        elif not projectname.isidentifier():
            raise CommandError("'{projectname}' is not a valid project identifier".format(
                projectname = projectname
            ))
        else:
            try:
                import_module(projectname)
            except:
                pass
            else:
                raise CommandError("'{projectname}' conflicts with the name of an existing Python".format(
                    projectname = projectname
                ))

        return projectname

    def get_default_projectpath(self):
        return os.path.abspath(".")

    def check_projectpath(self, projectpath):
        if not os.path.isabs(projectpath):
            raise CommandError("projectpath:{projectpath} is not exists".format(
                projectpath=projectpath
            ))
        return projectpath

    def handle(self, *args, **options):
        self.projectname = options["projectname"]
        self.projectpath = os.path.join(options["projectpath"], self.projectname)

        def file_handle(root, file):
            if file.endswith("-tpl"):
                old_file = os.path.join(root, file)
                new_file = os.path.join(self.projectpath, file[:-4])
                shutil.copyfile(old_file, new_file)

        try:
            os.makedirs(self.projectpath)
            dir.traverse_tree(template.get_project_template_path(), file_handle=file_handle)
        except FileExistsError:
            raise CommandError("project has exists")

        green_print("project {project_name} create success: {projectpath}".format(
            project_name = self.projectname,
            projectpath = self.projectpath
        ))



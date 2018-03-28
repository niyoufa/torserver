# @Time    : 2018/3/12 15:31
# @Author  : Niyoufa
import os
import sys
import importlib
import traceback
import pyserver
from pyserver.libs.constlib import const
from pyserver.core.management.base import BaseCommand
from pyserver.core.management.base import CommandError
from pyserver.core.management.base import CommandParser
from pyserver.core.management.base import handle_default_options
from pyserver import utils

def get_commands():
    commands = [
        ["help", "命令帮助信息"],
        ["shell", "python解释执行命令行工具"],
    ]
    commands.append(get_core_commands())

    modules = const.MODULES
    for module_name in modules:
        module = modules[module_name]
        name = module.get("name") or ""
        command_path = module.get("command_path")
        if command_path:
            try:
                command_file_path = os.path.join(const.BASE_DIR,
                     "/".join(command_path.split(".") + ["/management/commands"] ))
                names = [f.split(".py")[0] for f in os.listdir(command_file_path) if not f.startswith("__")]
                sub_commands = []
                for name in names:
                    try:
                        modulename = "{command_path}.management.commands.{name}".format(
                            command_path=command_path,
                            name=name
                        )
                        import_module = importlib.import_module(modulename)
                        command_obj = import_module.Command()
                        if command_obj.__doc__:
                            doc = command_obj.__doc__.strip()
                        else:
                            doc = ""
                        sub_commands.append(
                            [
                                name,
                                doc,
                                command_obj
                            ]
                        )
                    except:
                        print(traceback.format_exc())

                commands.append([module_name, name, sub_commands])
            except:
                print(traceback.format_exc())
        else:
            utils.warning_print("module '{module_name}' command_path is  {command_path}, "
                  "please set module command_path in settings MODULES".format(
                      module_name=module_name, command_path=command_path))

    command_dict = {}
    for command in commands:
        if isinstance(command[1], list):
            for sub_command in command[1]:
                command_dict[command[0] + "." + sub_command[0]] = sub_command
        else:
            command_dict[command[0]] = command

    return commands, command_dict

def get_core_commands():
    names = [f.split(".py")[0] for f in os.listdir("/".join([__path__[0], "commands"]))
             if not f.startswith("__")]
    sub_commands = []
    for name in names:
        try:
            modulename = "{command_path}.management.commands.{name}".format(
                command_path="pyserver.core",
                name=name
            )
            import_module = importlib.import_module(modulename)
            command_obj = import_module.Command()
            if command_obj.__doc__:
                doc = command_obj.__doc__.strip()
            else:
                doc = ""
            sub_commands.append(
                [
                    name,
                    doc,
                    command_obj
                ]
            )
        except:
            print(traceback.format_exc())
    return ["core", "系统命令", sub_commands]

def load_command_class(app_name, name):
    module = importlib.import_module('%s.management.commands.%s' % (app_name, name))
    return module.Command()


class ManagementUtility(object):

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.commands, self.command_dict = get_commands()

    def main_help_text(self):
        commands_info = ""
        for command in self.commands:
            print(command)
            if len(command) == 3 and isinstance(command[2], list):
                commands_info += "\n" + command[0] + ":"
                for sub_command in command[2]:
                    commands_info += "\n" + "    " + command[0] + "." + sub_command[0] + " " + sub_command[1]
            else:
                commands_info += "\n" + command[0] + "    " + command[1]
        usage = [
            "输入 python run.py help <命令名称>' 获取命令的帮助信息",
            "可用的命令:%s" % (commands_info),
        ]

        return '\n'.join(usage)

    def execute(self):
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = "help"

        if subcommand == "startserver":
            sys.argv = self.argv[1:]
            from pyserver.core.app import run
            run()
        else:
            parser = CommandParser(None, usage="%(prog)s subcommand [options] [args]", add_help=False)
            parser.add_argument('--pythonpath')
            parser.add_argument('args', nargs='*')

            options, args = parser.parse_known_args(self.argv[2:])
            handle_default_options(options)

            if subcommand == 'help':
                    print(self.main_help_text())
            elif self.argv[1:] in (['--help'], ['-h']):
                print(self.main_help_text() + '\n')
            elif self.argv[2:] in (['--help'], ['-h']):
                kclass = self.fetch_command(subcommand)
                kclass.print_help(self.prog_name, subcommand)
            elif subcommand == 'version' or self.argv[1:] == ['--version']:
                print("{version}".format(version=pyserver.__version__) + '\n')
            elif subcommand == 'shell':
                self._ipython()
            else:
                kclass = self.fetch_command(subcommand)
                if kclass:
                    kclass.run_from_argv(self.argv)

    def _ipython(self):
        """Start IPython >= 1.0"""
        from IPython import start_ipython
        start_ipython(argv=[])

    def fetch_command(self, subcommand):
        if subcommand in self.command_dict:
            app_name = self.command_dict[subcommand][2]
            if isinstance(app_name, BaseCommand):
                klass = app_name
            else:
                klass = load_command_class(app_name, subcommand)
            return klass
        else:
            print("'{command}'命令不存在".format(command=subcommand))

    def load_command_class(self, app_name, name):
        module = importlib.import_module('%s.management.commands.%s' % (app_name, name))
        return module.Command()


def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    utility = ManagementUtility(argv)
    utility.execute()
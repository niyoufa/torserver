# @Time    : 2018/3/12 15:31
# @Author  : Niyoufa
import os
import sys
import importlib
import traceback
import torserver
from torserver.libs.constlib import const
from torserver.core.management.base import BaseCommand
from torserver.core.management.base import CommandError
from torserver.core.management.base import CommandParser
from torserver.core.management.base import handle_default_options
from torserver.utils.print import warning_print

def get_commands():
    commands = [
        ["shell", "命令行工具"],
        ["startserver", "启动server"],
        ["", ""],
    ]
    commands.append(get_core_commands())

    modules = const.MODULES or {}
    for module_name in modules:
        module = modules[module_name]
        name = module.get("name") or ""
        command_path = module.get("command_path")
        if command_path != None:
            if command_path:
                try:
                    command_file_path = os.path.join(const.BASE_DIR or "",
                         "/".join(command_path.split(".") + ["/management/commands"] ))
                    names = [f.split(".py")[0] for f in os.listdir(command_file_path) if not f.startswith("__")]
                    sub_commands = []
                    for name in names:
                        try:
                            command_obj = load_command_class(command_path, name)
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
            warning_print("module '{module_name}' command_path is  {command_path}, "
                  "please set module command_path in settings MODULES".format(
                      module_name=module_name, command_path=command_path))

    command_dict = {}
    for command in commands:
        if len(command) == 3 and isinstance(command[2], list):
            for sub_command in command[2]:
                command_dict["{module_name}_{command_name}".format(module_name=command[0],
                                                                   command_name=sub_command[0])] = sub_command[2]
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
                command_path="torserver.core",
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

def load_command_class(module_path, name):
    module = importlib.import_module('%s.management.commands.%s' % (module_path, name))
    return module.Command()


class ManagementUtility(object):

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.commands, self.command_dict = get_commands()

    def main_help_text(self):
        commands_info = ""
        commands_info += "\n"
        for command in self.commands:
            if len(command) == 3 and isinstance(command[2], list):
                for sub_command in command[2]:
                    commands_info += "\n{module_name}_{command_name} {command_info}".format(
                        module_name = command[0],
                        command_name = sub_command[0],
                        command_info = sub_command[1],
                    )
                commands_info += "\n"
            elif len(command) == 2:
                commands_info += "\n" + command[0] + " " + command[1]
            else:
                raise CommandError("command error")
        usage = [
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
            from torserver.core.app import run
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
                print("{version}".format(version=torserver.__version__) + '\n')
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
            command_obj = self.command_dict[subcommand]
            if not isinstance(command_obj, BaseCommand):
                raise CommandError("命令类型错误：{}")
            return command_obj
        else:
            raise CommandError("'{command}'命令不存在".format(command=subcommand))


def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    utility = ManagementUtility(argv)
    utility.execute()
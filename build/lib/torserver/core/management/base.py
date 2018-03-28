# @Time    : 2018/3/25 下午1:14
# @Author  : Niyoufa
import os
import sys
from argparse import ArgumentParser
import torserver


class CommandError(Exception):
    pass


class BaseCommand(object):
    help = ""

    def handle(self, *args, **options):
        raise NotImplementedError('subclasses of BaseCommand must provide a handle() method')

    def create_parser(self, prog_name, subcommand):
        """
        Create and return the ``ArgumentParser`` which will be used to
        parse the arguments to this command.
        """
        parser = CommandParser(
            self, prog="%s %s" % (os.path.basename(prog_name), subcommand),
            description=self.help or None,
        )
        parser.add_argument(
            '--pythonpath',
            help='A directory to add to the Python path',
        )
        self.add_arguments(parser)
        return parser

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        try:
            import sys
            sys.argv = sys.argv[2:]
            from torserver.libs.optionslib import parse_options, get_options_module
            options_module = get_options_module()
            options_module.add_options_arguments(parser)
            parse_options()
        except:
            pass

    def print_help(self, prog_name, subcommand):
        """
        Print the help message for this command, derived from
        ``self.usage()``.
        """
        parser = self.create_parser(prog_name, subcommand)
        parser.print_help()

    def run_from_argv(self, argv):
        """
        Set up any environment changes requested (e.g., Python path
        and settings), then run this command. If the
        command raises a ``CommandError``, intercept it and print it sensibly
        to stderr. If the ``--traceback`` option is present or the raised
        ``Exception`` is not ``CommandError``, raise it.
        """
        self._called_from_command_line = True
        parser = self.create_parser(argv[0], argv[1])
        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        args = cmd_options.pop('args', ())
        self.execute(*args, **cmd_options)

    def execute(self, *args, **options):
        """
        Execute this command
        """
        self.handle(*args, **options)


class CommandParser(ArgumentParser):
    def __init__(self, cmd, **kwargs):
        self.cmd = cmd
        super(CommandParser, self).__init__(**kwargs)

    def parse_args(self, args=None, namespace=None):
        if (hasattr(self.cmd, 'missing_args_message') and
                not (args or any(not arg.startswith('-') for arg in args))):
            self.error(self.cmd.missing_args_message)
        return super(CommandParser, self).parse_args(args, namespace)

    def error(self, message):
        if self.cmd._called_from_command_line:
            super(CommandParser, self).error(message)
        else:
            raise CommandError("Error: %s" % message)

def handle_default_options(options):
    """
    Include any default options that all commands should accept here
    so that ManagementUtility can handle them before searching for
    user commands.
    """
    if options.pythonpath:
        sys.path.insert(0, options.pythonpath)




import argparse

from App.Core.Abstract import AbstractCommand
from App.Subprocesses import LpstatSubprocess
from App.helpers import logger, config, cache


class PrintersCommand(AbstractCommand):
    def _parameters(self):
        subparser = self._argument_parser.add_subparsers(title='subjects')

        list_parser = subparser.add_parser('list', help='Create list of printers')
        list_parser.add_argument('-l', '--local', help='Use command locale', action="store_true")
        list_parser.set_defaults(func=self._exec_get_list)

    def _exec_get_list(self, args: argparse.Namespace):
        local = args.local or False

        #: TODO: Get list by network
        printers = LpstatSubprocess(logger(), config(), cache()).get_printers_list() if local else []

        for printer in printers:
            self._output.header("Printers:")

            self._output.line(f"{printer['display_name']}:", indent=2)
            self._output.line(f"Name: {printer['name']}:", indent=4)
            self._output.line(f"{printer['']}:", indent=2)
            self._output.line(f"{printer['display_name']}:", indent=2)
            self._output.line(f"{printer['display_name']}:", indent=2)


    def _execute(self, args: argparse.Namespace):
        pass

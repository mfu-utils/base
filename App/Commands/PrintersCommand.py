import argparse

from App.Core.Abstract import AbstractCommand
from App.Subprocesses import LpstatSubprocess
from App.helpers import logger, config, cache


class PrintersCommand(AbstractCommand):
    signature = "printers"
    help = "Printers management"

    def _parameters(self):
        subparser = self._argument_parser.add_subparsers(title='subjects')

        list_parser = subparser.add_parser('list', help='Create list of printers')
        list_parser.add_argument('-l', '--local', help='Use command locale', action="store_true")
        list_parser.set_defaults(func=self._exec_get_list)

    def _exec_get_list(self, args: argparse.Namespace):
        local = args.local or False

        #: TODO: Get list by network
        printers = LpstatSubprocess(logger(), config(), cache()).get_printers_list() if local else []

        self._output.endl()
        self._output.header("Printers:")

        if not len(printers):
            self._output.line("None")

        for printer in printers:
            self._output.header(f"- {printer['display_name']}:")
            self._output.line(f"Index: {' ' * 4}{printer['index']}", indent=2)
            self._output.line(f"Name: {' ' * 5}{printer['name']}", indent=2)
            self._output.line(f"Device: {' ' * 3}{printer['device']}", indent=2)
            self._output.line(f"Connected: {printer['connected']}", indent=2)
            self._output.endl()

    def _execute(self, args: argparse.Namespace):
        pass

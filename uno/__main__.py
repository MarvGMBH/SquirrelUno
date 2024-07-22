"""
Entry point for the uno package to run from Console
"""

import argparse
from __init__ import main

class CLI:
    """
    Command Line Interface for the Uno package.
    """
    def __init__(self):
        """
        Initialize the CLI with argument parsers.
        """
        self.parser = argparse.ArgumentParser(description='Uno command line interface')
        self.subparsers = self.parser.add_subparsers(dest='command', help='Commands')
        self.parser.add_argument('--debug', action='store_true', help='Enable debugging mode')
        self._setup_version_info()

    def _setup_version_info(self):
        """
        Set up the subcommand for displaying version information.
        """
        parser_a = self.subparsers.add_parser('info', help='shows version and other information')
        parser_a.add_argument('--hide_info', action='store_true', help='shows only version text')
        parser_a.set_defaults(func=self.version_info)

    def parse_args(self):
        """
        Parse the command line arguments.

        :return: Parsed arguments
        """
        return self.parser.parse_args()

    def run(self):
        """
        Execute the appropriate function based on the parsed arguments.
        """
        args = self.parse_args()
        if args.command:
            args.func(args)
        else:
            self.handle_no_command(args)

    def handle_no_command(self, args):
        """
        Handle the case where no command is provided.

        :param args: Parsed arguments
        """
        if args.debug:
            print('Debug Mode active')
        main(args.debug)

    def version_info(self, args):
        """
        Display version information.

        :param args: Parsed arguments
        """
        print('v00.00.01')
        if not args.hide_info:
            print('A fun little Uno implementation by Dominik Krenn')

if __name__ == '__main__':
    cli = CLI()
    cli.run()

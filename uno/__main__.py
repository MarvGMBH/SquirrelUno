import argparse
from __init__ import main

class CLI:
    """
    Command Line Interface for Uno game.
    """
    def __init__(self):
        """
        Initializes the CLI with argument parsing.
        """
        self.parser = argparse.ArgumentParser(description='Uno command line interface')
        self.subparsers = self.parser.add_subparsers(dest='command', help='Commands')
        self.parser.add_argument('--debug', action='store_true', help='Enable debugging mode')
        self._setup_version_info()

    def _setup_version_info(self):
        """
        Sets up the version info command.
        """
        parser_info = self.subparsers.add_parser('info', help='Shows version and other information')
        parser_info.add_argument('--hide_info', action='store_true', help='Shows only version text')
        parser_info.set_defaults(func=self.version_info)

    def parse_args(self):
        """
        Parses the command-line arguments.
        """
        return self.parser.parse_args()

    def run(self):
        """
        Runs the CLI and handles the parsed arguments.
        """
        args = self.parse_args()
        if args.command:
            if hasattr(args, 'func'):
                args.func(args)
            else:
                self.parser.print_help()
        else:
            self.handle_no_command(args)

    def handle_no_command(self, args):
        """
        Handles the case when no command is provided.
        """
        if args.debug:
            print('Debug Mode active')
        main(args.debug)

    def version_info(self, args):
        """
        Displays version information.
        """
        print('v00.00.01')
        if not args.hide_info:
            print('A fun little Uno implementation by Dominik Krenn')

if __name__ == '__main__':
    cli = CLI()
    cli.run()

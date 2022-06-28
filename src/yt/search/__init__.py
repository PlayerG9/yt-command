#!/usr/bin/python3
r"""
search for videos

only lists videos between 1min and 6min.
if you need longer or shorter videos, then use the --longer or --shorter arguments
"""
import youtubesearchpython


COMMAND_NAME = "search"


def initialise(helper: 'argparse.ArgumentParser', commands: dict):  # noqa
    import argparse

    parser: argparse.ArgumentParser = helper.add_parser(
        COMMAND_NAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help=__doc__.split('\n', 1)[0],  # short help in main-help
        description=__doc__  # long help in command-help
    )

    parser.add_argument('query')

    parser.add_argument('-l', '--longer', help="removes upper timelimit of filter")
    parser.add_argument('-s', '--shorter', help="removes lower timelimit of filter")

    commands[COMMAND_NAME] = execute


def execute(arguments):
    Searcher(query=arguments.query).execute()


class Searcher:
    def __init__(self, query: str):
        self.query = query

    def execute(self):
        pass

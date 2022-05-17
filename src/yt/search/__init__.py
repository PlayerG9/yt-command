#!/usr/bin/python3
r"""
search for videos
"""
import youtubesearchpython


def initialise(helper: 'argparse.ArgumentParser'):  # noqa
    import argparse

    parser: argparse.ArgumentParser = helper.add_parser(
        "search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help=__doc__.split('\n', 1)[0],  # short help in main-help
        description=__doc__  # long help in command-help
    )

    parser.add_argument('query')


def execute(arguments):
    Searcher(query=arguments.query).execute()


class Searcher:
    def __init__(self, query: str):
        self.query = query

    def execute(self):
        pass

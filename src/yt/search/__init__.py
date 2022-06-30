#!/usr/bin/python3
r"""
search for videos

yt search "Last one standing"

only lists videos between 1min and 6min.
if you need longer or shorter videos, then use the --longer or --shorter arguments
"""
import traceback

import youtubesearchpython
import logging
import shutil


COMMAND_NAME = "search"


def initialise(helper: 'argparse.ArgumentParser', commands: dict):  # noqa
    import argparse

    short, description = __doc__.strip().split('\n', 1)

    parser: argparse.ArgumentParser = helper.add_parser(
        COMMAND_NAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help=short,  # short help in main-help
        description=description  # long help in command-help
    )

    parser.add_argument('query')

    # parser.add_argument('-l', '--longer', help="removes upper timelimit of filter")
    # parser.add_argument('-s', '--shorter', help="removes lower timelimit of filter")

    parser.add_argument('-c', '--channel', help="specifies a channel-name")
    parser.add_argument('-L', '--limit', help="limit of results", default=6)

    commands[COMMAND_NAME] = execute


def execute(arguments):
    Searcher(args=arguments).execute()


class Searcher:
    search: youtubesearchpython.CustomSearch

    def __init__(self, args):
        self.query = self.createQuery(args)
        self.config = args

    def execute(self) -> None:
        self.createSearcher()
        self.printSearchResults()

    @staticmethod
    def createQuery(args) -> str:
        if args.channel:
            return f"{args.channel} {args.query}"
        else:
            return f"{args.query}"

    def createSearcher(self) -> None:
        from youtubesearchpython import CustomSearch, SearchMode, VideoDurationFilter, VideoSortOrder
        self.search = CustomSearch(
            query=self.query,
            searchPreferences=SearchMode.videos + VideoDurationFilter.short + VideoSortOrder.relevance,
            limit=self.config.limit,
            timeout=30
        )
        logging.debug(f"URL: {self.search.url}")

    def printSearchResults(self) -> None:
        result = self.search.result()
        terminal_width = shutil.get_terminal_size()[0]

        for video in result['result']:
            video: dict
            try:
                title: str = video['title']
                link: str = video['link']
                channel_name: str = video['channel']['name']
                duration: str = video['duration']
                view_count: str = video['viewCount']['short']  # alternative option is 'text'
            except KeyError as error:
                logging.warning("failed to evaluate one result element")
                logging.warning(f"({error.__class__.__name__}: {error})")
                if self.config.debug:
                    traceback.print_exception(None, error, error.__traceback__)
                continue
            else:
                print(f" {title} ".center(terminal_width, "="))
                print(f"Link:     {link}")
                print(f"Channel:  {channel_name}")
                print(f"Duration: {duration}")
                print(f"Views:    {view_count}")
                print()  # for a better separation

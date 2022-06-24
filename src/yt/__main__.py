#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import argparse
import logging
import sys

import __init__ as yt

WELCOME_TEXT = r"""
        _                                                      _ 
  _   _| |_       ___ ___  _ __ ___  _ __ ___   __ _ _ __   __| |
 | | | | __|____ / __/ _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` |
 | |_| | ||_____| (_| (_) | | | | | | | | | | | (_| | | | | (_| |
  \__, |\__|     \___\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|
  |___/                                                          
"""


def configure_logging(arguments):

    if arguments.verbose:
        level = logging.DEBUG
    elif arguments.quiet:
        level = logging.WARNING
    else:
        level = logging.DEBUG if __debug__ else logging.INFO

    logging.basicConfig(
        datefmt="%H:%M:%S",
        style='{',
        format="{asctime}|{message}",
        level=level,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=True
    )

    parser.add_argument('-V', '--version', version=yt.__version__, action="version")
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help="produce more output")
    parser.add_argument('-q', '--quiet', action='store_true', required=False, help="produce less output")

    helper = parser.add_subparsers(  # create helper for new sup-commands
        title="command",
        dest="command",
        help='available commands'
    )

    import download
    download.initialise(helper=helper)
    import search
    search.initialise(helper=helper)

    arguments = parser.parse_args()
    configure_logging(arguments)
    command = arguments.command

    if not command:
        print(WELCOME_TEXT)
        parser.print_usage()
        sys.exit(0)

    logging.debug(f"execute command: {command!r}")
    if command == 'download':
        download.execute(arguments)
    elif command == 'search':
        search.execute(arguments)
    else:
        raise ValueError(f"Missing or Invalid command: {command!r}")


if __name__ == '__main__':
    main()

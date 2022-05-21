#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import argparse
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


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=True
    )

    parser.add_argument('--version', version=yt.__version__, action="version")

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
    command = arguments.command

    if command:
        print(WELCOME_TEXT)
    else:
        parser.print_usage()
        sys.exit(0)

    if command == 'download':
        download.execute(arguments)
    elif command == 'search':
        search.execute(arguments)
    else:
        raise ValueError(f"Missing or Invalid command: {command}")


if __name__ == '__main__':
    main()

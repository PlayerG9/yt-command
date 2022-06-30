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


def configure_logging(arguments) -> None:

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


def main() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=True)
    parser.usage = WELCOME_TEXT

    parser.add_argument(
        '-V', '--version',
        version=yt.__version__,
        action="version")
    # parser.add_argument(
    #     '-v', '--verbose',
    #     action='store_true',
    #     required=False,
    #     help="produce more output")
    # parser.add_argument(
    #     '-q', '--quiet',
    #     action='store_true',
    #     required=False,
    #     help="produce less output")
    parser.add_argument(
        '-D', '--debug',
        action='store_true',
        required=False,
        default=__debug__,
        help="print more on errors")

    # create helper for new sup-commands
    helper = parser.add_subparsers(
        title="command",
        dest="command",
        help='available commands')

    command_index = dict()

    import download
    download.initialise(helper=helper, commands=command_index)
    import search
    search.initialise(helper=helper, commands=command_index)
    import open as cmd_open  # don't override the default open()
    cmd_open.initialise(helper=helper, commands=command_index)

    arguments = parser.parse_args()
    configure_logging(arguments)
    command_name = arguments.command

    if not command_name:
        print(WELCOME_TEXT)
        parser.print_usage()
        sys.exit(0)

    logging.debug(f"execute command: {command_name!r}")
    command = command_index.get(command_name)
    if command:
        command(arguments)
    else:
        raise ValueError(f"Missing or Invalid command: {command_name!r}")


if __name__ == '__main__':
    main()

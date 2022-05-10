#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import argparse
import __init__ as yt


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

    arguments = parser.parse_args()
    command = arguments.command

    if command == 'download':
        download.execute(arguments)
    elif command == 'search':
        pass
    else:
        raise ValueError(f"Missing or Invalid command: {command}")


if __name__ == '__main__':
    main()

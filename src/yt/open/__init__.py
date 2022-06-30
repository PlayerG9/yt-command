#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
starts your default browser with youtube
start your default browser and opens a new tab with youtube.com
"""
import webbrowser


COMMAND_NAME = "open"
URL_TO_OPEN = 'https://www.youtube.com/'


def initialise(helper: 'argparse.ArgumentParser', commands: dict) -> None:  # noqa
    import argparse

    short, description = __doc__.strip().split('\n', 1)

    parser: argparse.ArgumentParser = helper.add_parser(
        COMMAND_NAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help=short,  # short help in main-help
        description=description  # long help in command-help
    )

    parser.add_argument('-w', '--window')

    commands[COMMAND_NAME] = execute


def execute(arguments) -> None:
    if arguments.window:
        webbrowser.open_new_tab(URL_TO_OPEN)
    else:
        webbrowser.open_new(URL_TO_OPEN)

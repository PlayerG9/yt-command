#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
starts your default browser with youtube
"""
import webbrowser


COMMAND_NAME = "open"
URL_TO_OPEN = 'https://www.youtube.com/'


def initialise(helper: 'argparse.ArgumentParser', commands: dict):  # noqa
    import argparse

    parser: argparse.ArgumentParser = helper.add_parser(
        COMMAND_NAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help=__doc__.split('\n', 1)[0],  # short help in main-help
        description=__doc__  # long help in command-help
    )

    parser.add_argument('-w', '--window')

    commands[COMMAND_NAME] = execute


def execute(arguments):
    if arguments.window:
        webbrowser.open_new_tab(URL_TO_OPEN)
    else:
        webbrowser.open_new(URL_TO_OPEN)

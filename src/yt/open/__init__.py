#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
starts your default browser with youtube
"""
import webbrowser


def initialise(helper: 'argparse.ArgumentParser'):  # noqa
    import argparse

    parser: argparse.ArgumentParser = helper.add_parser(
        "open",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help=__doc__.split('\n', 1)[0],  # short help in main-help
        description=__doc__  # long help in command-help
    )


def execute(_):
    webbrowser.open('https://www.youtube.com/', autoraise=True)

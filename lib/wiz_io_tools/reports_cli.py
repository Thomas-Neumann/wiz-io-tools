#!/usr/bin/env
#
# command line interface for wiz_io_tools.reports
#

import argparse
import logging
import sys

from colorama import Fore, Back, Style
from typing import Optional, Dict

# configure_logger(lh, loglevel) and ColoredFormatter are based on
# https://gist.github.com/joshbode/58fac7ababc700f51e2a9ecdebe563ad

class ColoredFormatter(logging.Formatter):
    """
    colored log formatter
    """

    def __init__(self, *args, colors: Optional[Dict[str, str]]=None, **kwargs) -> None:
        """
        initialize the formatter with specified format strings
        """
        super().__init__(*args, **kwargs)
        self.colors = colors if colors else {}


    def format(self, record) -> str:
        """
        Format the specified record as text.
        """
        record.color = self.colors.get(record.levelname, '')
        record.reset = Style.RESET_ALL
        return super().format(record)


def configure_logger(lh, loglevel):
    formatter = ColoredFormatter(
        '{color}{levelname:.1s}: {message}{reset}',
        style='{',
        colors={
            'DEBUG': Fore.CYAN,
            'INFO': Fore.GREEN,
            'WARNING': Fore.YELLOW,
            'ERROR': Fore.RED,
            'CRITICAL': Fore.RED + Back.WHITE + Style.BRIGHT,
        }
    )
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    lh.handlers[:] = []
    lh.addHandler(sh)
    lh.setLevel(loglevel)
    return lh


def parse_argv(versionstring):
    parser = argparse.ArgumentParser(description='filter wiz.io vulnerability reports', allow_abbrev=False)
    parser.add_argument('--version', action='version', version=f"%(prog)s v{versionstring}")
    parser.add_argument('report_file', type=str, nargs='+', help='one or more wiz.io report files in csv format')
    args = parser.parse_args()

    config = {
        "reports": args.report_file,
    }
    return config

import sys

from config import setup_logging

setup_logging()

from apps.gui_app import gui_main
from apps.cli_app import cli_main

import logging

log = logging.getLogger(__name__)


def main():
    args = sys.argv[1:]
    if args:
        cli_main(args)
    else:
        gui_main()


if __name__ == '__main__':
    main()

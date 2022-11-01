import textwrap
from pathlib import Path

from config import setup_logging

setup_logging()
import logging
import argparse

from calc import calculate_unit_price
from inputs import csv_input
from inputs import user_input
from outputs import to_word

log = logging.getLogger(__name__)


def main():
    log.info(' program start '.center(80, '-'))

    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            "Label Maker - program pro výrobu cenovek s přepočtem na objemové/hmotnostní jednotky."
            "Lze importovat data z csv nebo od uživatele"
        )
    )
    parser.add_argument(
        "data-input",
        choices=["file", "user"],
        default="file",
        const="file",
        nargs="?",

    )
    parser.add_argument(
        "path-file",
        type=Path,
        default="input/sample_data.csv",
        nargs="?",
        const="input/sample_data.csv",
        help="Specifikace cesty k souboru s importovatelnými daty, výchozí: %(default)s)"

    )
    args = parser.parse_args()

    data = []
    data_input = args.data_input

    if data_input == "file":
        file_path = args.path_file
        data = csv_input(file_path)

    elif data_input == "user":
        data = user_input()

    else:
        log.warning(f"Neznámá možnost vstupu: {data_input}")
        exit()

    calculated_data = calculate_unit_price(data)
    to_word(calculated_data, 'templates/labels_template.docx')
    log.info(' program end '.center(80, '-'))


if __name__ == '__main__':
    main()

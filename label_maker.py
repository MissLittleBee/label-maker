from config import setup_logging

setup_logging()
import logging

from calc import calculate_unit_price
from inputs import csv_input
from inputs import user_input
from outputs import to_word

log = logging.getLogger(__name__)


def main():
    log.info(' program start '.center(80, '-'))
    # TODO: vyměnit za argument od argparse

    data = []
    data_input = "file"

    if data_input == "file":
        file_path = "input/sample_data.csv"
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

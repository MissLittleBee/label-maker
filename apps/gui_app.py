import logging

import PySimpleGUI as sg

from calc import calculate_unit_price
from inputs import VALID_FORMS
from outputs import to_word

log = logging.getLogger(__name__)


class GUIApp:

    def __init__(self):
        self.in_files = []
        self.user_labels = []
        self.event_to_action = {
            "-ADD-": self.add_user_label,
            "-CREATE-": self.generate_labels,

        }

    def __enter__(self):
        self.window = self.create_window()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.window.close()

    def __eat_events__(self):
        """Eats falsely fired events
        NOTE: https://github.com/PySimpleGUI/PySimpleGUI/issues/4268
        """
        while True:
            event, values = self.window.read(timeout=0)
            if event == '__TIMEOUT__':
                break
        return

    def run(self):
        while True:
            event, values = self.window.read()
            log.debug((event, values))

            if event == sg.WIN_CLOSED:
                break

            # do actions
            try:
                self.event_to_action[event](values)
                self.__eat_events__()
            except KeyError:
                log.exception('unknown event')

    def create_window(self):

        def _user_tab():
            layout_user_input = [
                [sg.Text("Jméno produktu:")], [sg.InputText(key="name")],
                [sg.Text("Léková forma:")], [sg.Combo(key="form", values=sorted(VALID_FORMS.keys()))],
                [sg.Text("Množství jednotek v balení ")], [sg.InputText(key="quantity")],
                [sg.Text("Cena produktu:")], [sg.InputText(key="price")],
                [sg.Button("Další položka", key="-ADD-"), sg.Button("Vymazat", key="-CLEAR-")]
            ]
            return layout_user_input

        def _layout_csv_input():
            layout_csv_input = [
                [sg.Text("Vybrat soubor .CSV"), sg.Input(key="-IN-CSV"), sg.FileBrowse(file_types=("*.csv*"))],
                [],
            ]
            return layout_csv_input

        sg.theme('Black')

        layout = [
            [sg.Text('Vítejte v programu LabelMaker. Vyberte prosím vstupní data pro tvorbu cenovek:')],
            [sg.TabGroup(
                [[
                sg.Tab("Ručně", _user_tab()),
                sg.Tab("soubor .csv", _layout_csv_input())
            ]]
            )],
            [sg.Button(button_text= "Vytvořit cenovky",key= "-CREATE-")],
        ]

        # Create the Window
        return sg.Window('LabelMaker pro lékárnu', layout)

    def add_user_label(self, values):

        item = {
            "name": values["name"],
            "form": values["form"],
            "quantity": int(values["quantity"]),
            "total_price": int(values["price"]),
        }
        item["unit"] = VALID_FORMS.get(item["form"], "")
        self.user_labels.append(item)

    def generate_labels(self, values):

        calculated_data = calculate_unit_price(self.user_labels)
        to_word(calculated_data, 'templates/labels_template.docx')

def gui_main():
    log.info("Mód GUI")

    with GUIApp() as gui:
        gui.run()

    return 0

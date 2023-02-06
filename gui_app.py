import logging

import PySimpleGUI as sg

from inputs import VALID_FORMS

log = logging.getLogger(__name__)


class GUIApp:

    def __init__(self):
        self.in_files = []
        self.user_labels = []
        self.event_to_action = {
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

            if event == sg., "Exit":
                break

            # do actions
            try:
                self.event_to_action[event](values)
                self.__eat_events__()
            except KeyError:
                log.exception('unknown event')

    def create_window(self):
        sg.theme('Black')
        layout = [
                [sg.Text('Vítejte v programu LabelMaker. Vyberte prosím vstupní data pro tvorbu cenovek:')],
                [sg.Tab('Zadání hodnot uživatelem', [[#připravený layout]]), sg.Tab('Import z CSV', [[#připravený layout]]),
                [sg.Exit()]
                ]


        #layout pro zadání uživatelem --> rozbalí se po zakliknutí buttonu nebo záložky "Zadání hodnot uživatelem"§
        # Jak převedu input do slovníku k tvorbě cenovek? key -IN-
        layout_user_input = [
                [sg.Text("Jméno produktu:")],[sg.InputText()],
                #našeptávání formy podle zadaného prvního písmena: "e" --> všechny lékové formy od "e"
                #[sg.Text("Léková forma:")], [sg.Combo(VALID_FORMS.keys())], #nefunguje - proč nebere keys ze slovníku jako nabídku možností v combo?
                [sg.Text("Množství jednotek v balení ")],[sg.InputText()],
                [sg.Text("Cena produktu:")], [sg.InputText()],
                [sg.Button("Uložit hodnoty a pokračovat"),sg.Button("Uložit a vytvořit cenovky")],

                [sg.Output(size=(50,10))] #pole pro vypsání zadaných hodnot uživatelem
                ]
        #layout pro input z .csv
        layout_csv_input = [
                [sg.Text("Vybrat soubor .CSV") sg.Input(key= "-IN-CSV"), sg.FileBrowse(file_types=("*.csv*")],
                [],
        ]



"""sg.Window("název", layout)
    event, values = window.read()
    window.close()"
    
    *označení cedulek, které potřebují edistovat kvůli překlepu, případně rovnouo možnst editovat""

        # Create the Window
        return sg.Window('LabelMaker pro lékárnu', layout)


def gui_main():
    log.info("Mód GUI")

    with GUIApp() as gui:
        gui.run()

    return 0

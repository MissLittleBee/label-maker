import logging

import PySimpleGUI as sg

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

            if event == sg.WIN_CLOSED:  # always,  always give a way out!
                break

            # do actions
            try:
                self.event_to_action[event](values)
                self.__eat_events__()
            except KeyError:
                log.exception('unknown event')

    def create_window(self):
        layout = [[sg.Text('Some text on Row 1')],
                  [sg.Text('Enter something on Row 2'), sg.InputText()],
                  [sg.Button('Ok'), sg.Button('Cancel')]]

        # Create the Window
        return sg.Window('Window Title', layout)


def gui_main():
    log.info("Mód GUI")

    with GUIApp() as gui:
        gui.run()

    return 0

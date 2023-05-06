from views.MainView import MainView
from PyQt6.QtWidgets import QMainWindow


class Core(MainView):
    def __init__(self, window: QMainWindow, language: str = 'en_us'):
        self.LANGUAGE = language

        super().__init__(window)

from controllers import MainController
from PyQt6.QtWidgets import QMainWindow
from views import MainView


class Core:
    def __init__(self, window: QMainWindow, language: str = 'en_us'):
        self.window = window
        self.language = language

        self.controller = MainController(self)
        self.view = MainView(self)

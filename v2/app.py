import os
import sys

from PyQt6.QtCore import QMetaObject
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow

from core import Core


class MainWindow(QMainWindow):
    def __init__(self, app: QApplication, language: str = 'en_US', theme: str = 'dark', * args, **kwargs):
        super().__init__()

        self.app = app
        self.theme = theme
        self.language = language
        dir = os.path.realpath(os.path.dirname(__file__))
        self.iconPath = os.path.join(dir, 'res', 'drawable', 'ICON_FA.svg')
        self.themePath = os.path.join(
            dir, 'res', 'styles', self.theme + '.css')

        self.configure()
        self.loadCore()

    def loadCore(self):
        self.core = Core(window=self, language=self.language)

        self.setCentralWidget(self.core)
        QMetaObject.connectSlotsByName(self)

    def configure(self):
        self.showMaximized()
        self.setWindowTitle("Features Analyzer")
        self.app.setWindowIcon(QIcon(self.iconPath))

        QMetaObject.connectSlotsByName(self)

        with open(self.themePath, "r") as css:
            self.setStyleSheet(css.read())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(app)

    window.show()

    sys.exit(app.exec())

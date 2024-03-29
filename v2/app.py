import os
import sys

from core import Core
from PyQt6.QtCore import QMetaObject
from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow


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

        self.setCentralWidget(self.core.view)

    def configure(self):
        self.setWindowTitle("Features Analyzer")
        self.app.setWindowIcon(QIcon(self.iconPath))

        # with open(self.themePath, "r") as css:
        #     self.setStyleSheet(css.read())

        self.setGeometry(QGuiApplication.primaryScreen().availableGeometry())
        self.showMaximized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(app)

    sys.exit(app.exec())

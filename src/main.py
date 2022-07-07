import sys

sys.path.append("../")

from lib.util.path import bar
from Core import Core

from subprocess import Popen

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QMetaObject
from PyQt5 import QtGui


class FeaturesAnalyzer(QWidget):
    def __init__(self, darkTheme: bool = True, language: str = 'en_us'):
        """  """
        super(QWidget, self).__init__()
        super().__init__()


        print("""
        ______          _                         _                _
        |  ______  __ _| |_ _   _ _ __ ___ ___   / \   _ __   __ _| |_   _ _______ _ __
        | |_ / _ \/ _` | __| | | | '__/ _ / __| / _ \ | '_ \ / _` | | | | |_  / _ | '__|
        |  _|  __| (_| | |_| |_| | | |  __\__ \/ ___ \| | | | (_| | | |_| |/ |  __| |
        |_|  \___|\__,_|\__|\__,_|_|  \___|___/_/   \_|_| |_|\__,_|_|\__, /___\___|_|
                                                                    |___/
        """)

        self.setTheme(darkTheme)
        self.preLoader()

    def preLoader(self):
        """  """
        self.__smartEnergyLogo = Popen(['python3', 'PreLoader.py', '--se', 'time=1000'])
        self.__smartEnergyLogo.wait()
        self.__featuresAnalyzer = Popen(['python3', 'PreLoader.py', '--fa', 'time=750'])
        self.loadCore()
        self.__featuresAnalyzer.terminate()

    def loadCore(self):
        """  """
        self.core = Core(self, language)
        QMetaObject.connectSlotsByName(self)
        self.showMaximized()
        self.setWindowTitle("Features Analyzer")

    def setTheme(self, darkTheme: bool):
        """  """
        STYLESHEETS = bar.join(['res', 'styles'])

        if darkTheme:
            STYLESHEETS = bar.join([STYLESHEETS, 'dark.css'])
        else:
            STYLESHEETS = bar.join([STYLESHEETS, 'light.css'])

        with open(STYLESHEETS, "r") as css:
            self.setStyleSheet(css.read())


if __name__ == "__main__":
    ICON_SE = bar.join(["res", "drawable", "ICON_SE.svg"])
    ICON_FA = bar.join(["res", "drawable", "ICON_FA.svg"])

    if '--light' in sys.argv:
        darkTheme = False
    else:
        darkTheme = True

    if '--ptBr' in sys.argv:
        language = 'pt_br'
    else:
        language = 'en_us'

    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(ICON_FA))
    featuresAnalyzer = FeaturesAnalyzer(darkTheme, language)
    sys.exit(app.exec_())

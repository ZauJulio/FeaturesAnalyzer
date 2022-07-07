import sys

sys.path.append("../")

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtSvg, QtGui

from lib.util.path import bar


class PreLoader(QtSvg.QSvgWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)

    def showSmartEnergyLogo(self):
        """  """
        self.setWindowTitle("Smart Energy")
        self.load(bar.join(["res", "drawable", "SE_LOGO.svg"]))
        # Centralize loader in the screen
        self.move(QApplication.desktop().screen(
        ).rect().center() - self.rect().center())
        self.show()

    def showFeaturesAnalyzerLogo(self):
        """  """
        self.setWindowTitle("Smart Energy: Features Analyzer")
        self.load(bar.join(["res", "drawable", "FA_LOGO.svg"]))
        self.move(QApplication.desktop().screen(
        ).rect().center() - self.rect().center())
        self.show()


app = QApplication(sys.argv)

window = PreLoader()

if '--se' in sys.argv:
    app.setWindowIcon(QtGui.QIcon(
        bar.join(["res", "drawable", "ICON_SE.svg"])))
    window.showSmartEnergyLogo()

elif '--fa' in sys.argv:
    app.setWindowIcon(QtGui.QIcon(
        bar.join(["res", "drawable", "ICON_FA.svg"])))
    window.showFeaturesAnalyzerLogo()

else:
    sys.exit()

for arg in sys.argv:
    if 'time=' in arg:
        QTimer.singleShot(int(arg[5:]), app.quit)
        break

sys.exit(app.exec_())

from matplotlib.backends.backend_qt import NavigationToolbar2QT
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QGridLayout, QScrollArea, QWidget
from matplotlib.figure import Figure

from widgets import MPLCanvas, SideMenu


class MainView(QWidget):
    def __init__(self, window: QMainWindow) -> None:
        super().__init__()

        self.setObjectName("MainViewParent")
        self.buildWidgets(window)
        self.buildLayout()

    def buildWidgets(self, window: QMainWindow):
        self.fig = Figure(figsize=(5, 4), dpi=100)

        self.mplCanvas = MPLCanvas(fig=self.fig)
        self.navigationBar = NavigationToolbar2QT(self.mplCanvas, self)
        self.sideMenu = SideMenu(self)

    def buildLayout(self):
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setObjectName("scrollAreaMain")
        scrollArea.setContentsMargins(9, 9, 9, 9)
        scrollArea.setMaximumSize(QSize(440, 16777215))
        scrollArea.setWidget(SideMenu(self))

        layout = QGridLayout()
        layout.setObjectName("layout")
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(scrollArea, 0, 0, 2, 1)
        layout.addWidget(self.mplCanvas, 0, 1)
        layout.addWidget(self.navigationBar, 1, 1)

        self.setLayout(layout)

from widgets import MPLCanvas, SideMenu
from PyQt6.QtWidgets import QGridLayout, QScrollArea, QWidget
from PyQt6.QtCore import QSize
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt import NavigationToolbar2QT


class MainView(QWidget):
    def __init__(self, core) -> None:
        self.core = core

        super().__init__(self.core.window)

        self.buildWidgets()
        self.buildLayout()

    def buildWidgets(self):
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
        scrollArea.setWidget(self.sideMenu)

        layout = QGridLayout()
        layout.setObjectName("layout")
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(scrollArea,         0, 0, 2, 1)
        layout.addWidget(self.mplCanvas,     0, 1, 1, 1)
        layout.addWidget(self.navigationBar, 1, 1, 1, 1)

        self.setLayout(layout)

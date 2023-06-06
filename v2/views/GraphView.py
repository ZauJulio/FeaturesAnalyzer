from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from widgets import MPLCanvas


class GraphView(QWidget):
    def __init__(self, core) -> None:
        self.core = core

        super().__init__(self.core.window)

        self.buildWidgets()
        self.buildLayout()

    def buildWidgets(self):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.mplCanvas = MPLCanvas(fig=self.fig)
        self.navigationBar = NavigationToolbar2QT(self.mplCanvas, self)

    def buildLayout(self):
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(self.mplCanvas)
        self.layout().addWidget(self.navigationBar)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().setStretch(0, 100)  # type: ignore

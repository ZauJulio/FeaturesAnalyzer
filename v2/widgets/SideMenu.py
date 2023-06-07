from interfaces import AbstractLayout
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDockWidget, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget

from .DataMenu import DataMenu


class SideMenu(AbstractLayout):
    def buildComponents(self):
        self.dataMenu = DataMenu(self)

    def buildLayout(self):
        self.dock = QDockWidget("Control", self)

        self.dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFloatable)

        self.dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        self.container = QWidget(self)
        self.container.setLayout(QVBoxLayout(self.container))
        self.container.layout().addWidget(self.dataMenu)
        self.dock.setWidget(self.container)
        self.core.window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

        self.setLayout(QVBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.dock)
        self.layout().addItem(QSpacerItem(
            7, 7,
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        ))

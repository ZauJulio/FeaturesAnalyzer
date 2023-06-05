from interfaces import AbstractLayout
from PyQt6.QtWidgets import QSizePolicy, QSpacerItem, QVBoxLayout

from .DataMenu import DataMenu


class SideMenu(AbstractLayout):
    def buildComponents(self):
        self.dataMenu = DataMenu(self)

    def buildLayout(self):
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(self.dataMenu)
        self.layout().addItem(QSpacerItem(
            7, 7,
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        ))

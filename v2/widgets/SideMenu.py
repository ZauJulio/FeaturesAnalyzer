from PyQt6.QtWidgets import QVBoxLayout, QWidget

from .DataSideMenuItem import DataSideMenuItem


class SideMenu(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName("sideMenuLayout")
        self.setLayout(QVBoxLayout())

        self.layout().addWidget(DataSideMenuItem(self))

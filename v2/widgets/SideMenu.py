from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout


class SideMenu(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName("sideMenuLayout")
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel("Hello World"))

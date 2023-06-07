from PyQt6.QtWidgets import QWidget


class AbstractSideMenuItem(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.buildComponents()
        self.buildLayout()

    def buildComponents(self):
        raise NotImplementedError()

    def buildLayout(self):
        raise NotImplementedError()

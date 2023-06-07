from contextlib import suppress
from typing import Callable, Optional

from interfaces.Widget import AbstractWidget
from PyQt6.QtWidgets import QLineEdit, QWidget


class LineEdit(QLineEdit, AbstractWidget):
    def __init__(self,
                 parent: Optional[QWidget] = None,
                 text: str = "",
                 onChange: Callable[[str], None] = lambda x: None,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.setText(text)
        self.editingFinished.connect(lambda: onChange(self.getValue()))

    def getValue(self) -> str:
        return self.text()

    def setValue(self, text: str) -> None:
        self.setText(text)

    def onError(self) -> None:
        self.setStyleSheet("border: 1px solid red;")
        self.textEdited.connect(lambda: self.setStyleSheet(
            "border: 1px solid transparent;"))

    def setOnChange(self, callback: Callable[[str], None]) -> None:
        with suppress(TypeError):
            self.editingFinished.disconnect()

        self.editingFinished.connect(lambda: callback(self.getValue()))

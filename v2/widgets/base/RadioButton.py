from contextlib import suppress
from typing import Callable, Optional

from interfaces.Widget import AbstractWidget
from PyQt6.QtWidgets import QRadioButton, QWidget


class RadioButton(QRadioButton, AbstractWidget):
    def __init__(self,
                 parent: Optional[QWidget] = None,
                 text: str = "",
                 checked: bool = False,
                 checkable: bool = True,
                 onChange: Callable[[bool], None] = lambda x: None,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.setCheckable(checkable)
        self.setChecked(checked)
        self.setText(text)
        self.toggled.connect(lambda: onChange(self.getValue()))

    def getValue(self) -> bool:
        return self.isChecked()

    def setValue(self, checked: bool) -> None:
        self.setChecked(checked)

    def setOnChange(self, callback: Callable[[bool], None]) -> None:
        with suppress(TypeError):
            self.toggled.disconnect()

        self.toggled.connect(lambda: callback(self.getValue()))

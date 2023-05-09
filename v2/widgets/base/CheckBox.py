from contextlib import suppress
from typing import Callable, Optional

from interfaces.Widget import AbstractWidget
from PyQt6.QtWidgets import QCheckBox, QWidget


class CheckBox(QCheckBox, AbstractWidget):
    def __init__(self,
                 parent: Optional[QWidget] = None,
                 checked: bool = False,
                 checkable: bool = True,
                 onChange: Callable[[bool], None] = lambda x: None,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.setCheckable(checkable)
        self.setChecked(checked)
        self.stateChanged.connect(lambda: onChange(self.getValue()))

    def getValue(self) -> bool:
        return self.isChecked()

    def setValue(self, checked: bool) -> None:
        self.setChecked(checked)

    def setOnChange(self, callback: Callable[[bool], None]) -> None:
        with suppress(TypeError):
            self.stateChanged.disconnect()

        self.stateChanged.connect(lambda: callback(self.getValue()))

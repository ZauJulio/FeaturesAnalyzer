from typing import Any, Callable, Optional

from interfaces.Widget import AbstractWidget
from PyQt6.QtWidgets import QLabel, QWidget


class Label(QLabel, AbstractWidget):
    def __init__(self,
                 parent: Optional[QWidget] = None,
                 value: Optional[str] = None,
                 buddy: Optional[QWidget] = None,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.setBuddy(buddy) if buddy else None
        self.setValue(value) if value else None

    def getValue(self) -> str:
        return self.text()

    def setValue(self, value: str) -> None:
        self.setText(value)

    def setOnChange(self, callback: Callable[[str], None]) -> None:
        return None

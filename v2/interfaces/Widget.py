from typing import Any, Callable, Optional

from PyQt6.QtWidgets import QWidget


class AbstractWidget(QWidget):
    def __init__(self,
                 parent: Optional[QWidget] = None,
                 onChange: Callable[[Any], None] = lambda x: None,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.setOnChange(onChange)

    def getValue(self) -> Any:
        raise NotImplementedError()

    def onError(self) -> None:
        pass

    def setValue(self, value: Any) -> None:
        raise NotImplementedError()

    def setOnChange(self, callback: Callable[[Any], None]) -> None:
        raise NotImplementedError()

from typing import Any


class AbstractController:
    def __init__(self, core):
        self.core = core

    def reload(self) -> None:
        raise NotImplementedError()

    def preLoad(self) -> None:
        pass
        # raise NotImplementedError()

    def getOutput(self) -> Any:
        pass
        # raise NotImplementedError()

    def getParams(self) -> Any:  # dict[str, Any]:
        pass
        # raise NotImplementedError()

    def reset(self) -> None:
        pass
        # raise NotImplementedError()

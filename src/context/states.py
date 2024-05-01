from lib.state_manager import State


class ImportSettingsState(State):
    """Import settings state."""

    selected_file: str
    selected_url: str
    data_id: str

    def __init__(self) -> None:
        super().__init__(
            {
                "selected_file": "",
                "selected_url": "",
                "data_id": "",
            },
        )

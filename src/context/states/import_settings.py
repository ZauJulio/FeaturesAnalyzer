from lib.state_manager import FAState

TAB_1_KEY = "pairplot"


class ImportSettingsState(FAState):
    """Import settings state."""

    selected_file: str
    selected_url: str
    data_id: str

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from app import FeaturesAnalyzer

    def __init__(
        self,
        selected_file: str = "",
        selected_url: str = "",
        data_id: str = "",
    ) -> None:
        super().__init__(
            {
                "selected_file": selected_file,
                "selected_url": selected_url,
                "data_id": data_id,
            },
        )

    @staticmethod
    def handle_001_load_data(app: "FeaturesAnalyzer") -> None:
        """Update the data store with the selected file or URL."""
        import pandas as pd

        state = app.store.state.ImportSettings

        if state.data_id and (state.selected_file or state.selected_url):
            df: pd.DataFrame | None = None
            source = state.selected_file or state.selected_url

            match source.split(".")[-1]:
                case "csv":
                    df = pd.read_csv(source)
                case "json":
                    df = pd.read_json(source)
                case "xlsx":
                    df = pd.read_excel(source)
                case _:
                    pass

            if df is not None:
                app.store.state.data[state.data_id] = df

    @staticmethod
    def handle_002_on_data_update(app: "FeaturesAnalyzer") -> None:
        """Update the graph."""
        import seaborn as sns

        state = app.store.state.ImportSettings
        data = app.store.state.data[state.data_id]

        try:
            tab = app.window.graph.get_tab(TAB_1_KEY)
        except KeyError:
            tab = app.window.graph.add_tab(key=TAB_1_KEY, title="Pairplot")

        tab.seaborn_plot(sns.pairplot, data=data, hue="species", size=3)

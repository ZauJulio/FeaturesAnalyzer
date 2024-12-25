from sklearn.cluster import KMeans

from lib.state_manager import FAState

TAB_2_KEY = "kmeans"


class KMeansSolverState(FAState):
    """Import settings state."""

    max_iter: int
    n_clusters: int

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from app import FeaturesAnalyzer

    def __init__(self, max_iter: int = 100, n_clusters: int = 1) -> None:
        super().__init__({"max_iter": max_iter, "n_clusters": n_clusters})

    @staticmethod
    def handle_001_on_params_update(app: "FeaturesAnalyzer") -> None:
        """Generate the model."""
        import_state = app.store.state.ImportSettings
        model_state = app.store.state.KMeansSolver

        if not import_state.data_id:
            return

        data = app.store.state.data[import_state.data_id]
        x = data.iloc[:, [0, 1, 2, 3]].values

        kmeans = KMeans(
            n_clusters=model_state.n_clusters,
            init="k-means++",
            max_iter=model_state.max_iter,
            n_init=10,
            random_state=0,
        )

        y_kmeans = kmeans.fit_predict(x)

        try:
            tab = app.window.graph.get_tab(TAB_2_KEY)
        except KeyError:
            tab = app.window.graph.add_tab(key=TAB_2_KEY, title="KMeans")

        # Remove axes
        tab.figure.clear()

        ax = tab.figure.add_subplot(111, projection="3d")

        ax.scatter(
            x[y_kmeans == 0, 0],
            x[y_kmeans == 0, 1],
            s=100,
            c="purple",
            label="Iris Setosa",
        )

        ax.scatter(
            x[y_kmeans == 1, 0],
            x[y_kmeans == 1, 1],
            s=100,
            c="orange",
            label="Iris Versicolour",
        )
        ax.scatter(
            x[y_kmeans == 2, 0],  # noqa: PLR2004
            x[y_kmeans == 2, 1],  # noqa: PLR2004
            s=100,
            c="green",
            label="Iris Virginica",
        )

        # Plotting the centroids of the clusters
        ax.scatter(
            kmeans.cluster_centers_[:, 0],
            kmeans.cluster_centers_[:, 1],
            s=100,
            c="red",
            label="Centroids",
        )

        tab.canvas.draw()

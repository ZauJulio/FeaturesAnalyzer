from lib.state_manager import FAState
from models import KMeans

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
        x = data.iloc[:, [0, 1, 2]].values

        kmeans = KMeans(
            x=x,
            params=KMeans.schema(
                n_clusters=model_state.n_clusters,
                max_iter=model_state.max_iter,
                init="k-means++",
                random_state=0,
                n_init=10,
            ),
        )

        kmeans.fit(x)

        y_kmeans = kmeans.predict(x)

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
            x[y_kmeans == 0, 2],
            c="purple",
            label="Cluster 1",
        )

        ax.scatter(
            x[y_kmeans == 1, 0],
            x[y_kmeans == 1, 1],
            x[y_kmeans == 1, 2],
            c="orange",
            label="Cluster 2",
        )

        ax.scatter(
            x[y_kmeans == 2, 0],  # noqa: PLR2004
            x[y_kmeans == 2, 1],  # noqa: PLR2004
            x[y_kmeans == 2, 2],  # noqa: PLR2004
            c="green",
            label="Cluster 3",
        )

        # Plotting the centroids of the clusters
        ax.scatter(
            kmeans.method.cluster_centers_[:, 0],
            kmeans.method.cluster_centers_[:, 1],
            kmeans.method.cluster_centers_[:, 2],
            c="red",
            marker="X",
            label="Centroids",
        )

        ax.set_title("KMeans Clustering")
        ax.set_xlabel(data.columns[0])
        ax.set_ylabel(data.columns[1])
        ax.set_zlabel(data.columns[2])  # type: ignore[union-attr]
        ax.legend()

        tab.canvas.draw()

        # Focus on the tab
        app.window.graph.select_tab(TAB_2_KEY)

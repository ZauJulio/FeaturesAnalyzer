from typing import TYPE_CHECKING, Literal

import matplotlib.pyplot as plt
import numpy as np

from lib.state_manager import FAState
from models import MLP
from models.pre_processors import LabelEncoder

TAB_3_KEY = "mlp"


class MLPSolverState(FAState):
    """MLP Solver state."""

    hidden_layer_sizes: tuple[int, ...]
    activation: Literal["identity", "logistic", "tanh", "relu"]
    solver: Literal["lbfgs", "sgd", "adam"]
    max_iter: int

    if TYPE_CHECKING:
        from app import FeaturesAnalyzer

    def __init__(
        self,
        hidden_layer_sizes: tuple[int, ...] = (100,),
        activation: str = "relu",
        solver: str = "adam",
        max_iter: int = 200,
    ) -> None:
        super().__init__({
            "hidden_layer_sizes": hidden_layer_sizes,
            "activation": activation,
            "solver": solver,
            "max_iter": max_iter,
        })

    @staticmethod
    def handle_001_on_params_update(app: "FeaturesAnalyzer") -> None:
        """Generate the model."""
        import_state = app.store.state.ImportSettings
        model_state = app.store.state.MLPSolver

        if not import_state.data_id:
            return

        data = app.store.state.data[import_state.data_id]

        x: np.ndarray = np.asarray(data.iloc[:, :-1].values, dtype=np.float64)

        pre_processor = LabelEncoder()
        labels = pre_processor.run(data.iloc[:, -1].values)

        mlp = MLP()

        mlp.add_pre_processor(pre_processor)

        mlp.run(
            x=x,
            params=MLP.schema(
                hidden_layer_sizes=model_state.hidden_layer_sizes,
                activation=model_state.activation,
                solver=model_state.solver,
                max_iter=model_state.max_iter,
                random_state=42,
            ),
        )

        mlp.fit(x, labels)

        y_pred = mlp.predict(x)

        try:
            tab = app.window.graph.get_tab(TAB_3_KEY)
        except KeyError:
            tab = app.window.graph.add_tab(key=TAB_3_KEY, title="MLP Predictions")

        tab.figure.clear()
        ax = tab.figure.add_subplot(111)

        unique_labels = np.unique(labels)
        colors = plt.cm.get_cmap("tab10", len(unique_labels))

        for i, label in enumerate(unique_labels):
            label_indices = labels == label
            label_name = pre_processor.method.inverse_transform([label])[0]
            ax.scatter(
                np.where(label_indices)[0],
                labels[label_indices],
                color=colors(i),
                marker="o",
                facecolors=colors(i, alpha=0.3),
                label=f"Real {label_name}",
                alpha=0.3,
            )

        for i, label in enumerate(unique_labels):
            label_indices = labels == label
            label_name = pre_processor.method.inverse_transform([label])[0]
            ax.scatter(
                np.where(label_indices)[0],
                y_pred[label_indices],
                color=colors(i),
                marker="+",
                facecolors=colors(i, alpha=0.3),
                label=f"Predicted Label {label_name}",
                alpha=0.7,
            )

        ax.set_title("MLP Predictions vs True Labels")
        ax.set_xlabel("Sample Index")
        ax.set_ylabel("Class Label")
        ax.legend()

        tab.canvas.draw()

        # Focus on the tab
        app.window.graph.select_tab(TAB_3_KEY)

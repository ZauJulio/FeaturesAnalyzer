from typing import Literal

import numpy as np
from sklearn.base import check_is_fitted
from sklearn.exceptions import NotFittedError
from sklearn.neural_network import MLPClassifier

from lib.model_manager import FAModel
from lib.orm.schemas import PydanticBaseModel


class MLPParams(PydanticBaseModel):
    """Parameters for the MLPClassifier model."""

    hidden_layer_sizes: tuple[int, ...] = (100,)
    activation: Literal["identity", "logistic", "tanh", "relu"] = "relu"
    solver: Literal["lbfgs", "sgd", "adam"] = "adam"
    alpha: float = 0.0001
    batch_size: int | str = "auto"
    learning_rate: Literal["constant", "invscaling", "adaptive"] = "constant"
    max_iter: int = 200
    random_state: int | None = None


class MLP(FAModel[MLPClassifier, MLPParams]):
    """MLPClassifier model manager."""

    schema = MLPParams

    def run(self, x: np.ndarray, params: MLPParams | None) -> None:
        """Initialize the model."""
        self.store(x, params)

        if not self.loaded():
            self.method = MLPClassifier(
                hidden_layer_sizes=self.params.hidden_layer_sizes,
                activation=self.params.activation,
                solver=self.params.solver,
                alpha=self.params.alpha,
                batch_size=self.params.batch_size,
                learning_rate=self.params.learning_rate,
                max_iter=self.params.max_iter,
                random_state=self.params.random_state,
            )

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        """Fit the model."""
        try:
            check_is_fitted(self.method)
        except NotFittedError:
            self.method.fit(x, y)
            self.save()

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Predict the labels."""
        return self.method.predict(x)

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        """Predict the probabilities."""
        return self.method.predict_proba(x)

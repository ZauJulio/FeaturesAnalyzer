from typing import Literal

import numpy as np
from sklearn.base import check_is_fitted
from sklearn.cluster import KMeans as SklearnKMeans
from sklearn.exceptions import NotFittedError

from lib.model_manager import FAModelManager
from lib.orm.schemas import PydanticBaseModel


class KMeansParams(PydanticBaseModel):
    """Parameters for the KMeans model."""

    n_clusters: int
    max_iter: int = 300
    n_init: int = 10
    init: Literal["k-means++", "random"] = "k-means++"
    random_state: int = 0


class KMeans(FAModelManager[SklearnKMeans, KMeansParams]):
    """KMeans model manager."""

    schema = KMeansParams

    def __init__(self, x: np.ndarray, params: KMeansParams | None) -> None:
        """Initialize the model."""
        self.store(x, params)

        if not self.loaded():
            self.method = SklearnKMeans(
                n_clusters=self.params.n_clusters,
                max_iter=self.params.max_iter,
                init=self.params.init,
                random_state=self.params.random_state,
            )

    def fit(self, x: np.ndarray) -> None:
        """Fit the model."""
        try:
            check_is_fitted(self.method)
        except NotFittedError:
            self.method.fit(x)
            self.save()

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Predict the clusters."""
        return self.method.predict(x)

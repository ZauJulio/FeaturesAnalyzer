from typing import Literal

import pandas as pd
from sklearn.preprocessing import Normalizer as SklearnNormalizer

from lib.model_manager import FAPreProcessor
from lib.orm.schemas import PydanticBaseModel


class NormalizeParams(PydanticBaseModel):
    """Parameters for the normalize preprocessor."""

    norm: Literal["l1", "l2", "max"] = "l2"


class Normalizer(FAPreProcessor[NormalizeParams]):
    """A preprocessor to normalize data."""

    schema = NormalizeParams

    def run(
        self,
        data: pd.DataFrame,
        params: NormalizeParams | None = NormalizeParams(norm="l2"),  # noqa: B008
    ) -> pd.DataFrame:
        """Normalize data using sklearn."""
        self.store(data, params)

        normalizer = SklearnNormalizer(norm=self.params.norm)
        normalizer.fit(data)

        normalized_data = normalizer.transform(data)

        # Convert the result back to a DataFrame for consistency
        return pd.DataFrame(normalized_data, columns=data.columns, index=data.index)

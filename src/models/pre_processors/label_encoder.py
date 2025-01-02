from typing import Any

from sklearn.preprocessing import LabelEncoder as SklearnLabelEncoder

from lib.model_manager import FAPreProcessor
from lib.orm.schemas import PydanticBaseModel


class LabelEncoderParams(PydanticBaseModel):
    """Parameters for the LabelEncoder preprocessor."""

    columns: list = []


class LabelEncoder(FAPreProcessor[LabelEncoderParams]):
    """A preprocessor to encode labels in specific columns."""

    schema = LabelEncoderParams

    def run(
        self,
        data: Any,
        params: LabelEncoderParams = LabelEncoderParams(columns=[]),  # noqa: B008
    ) -> Any:
        """Encode labels using sklearn."""
        self.store(data, params)

        self.method = SklearnLabelEncoder()

        return self.method.fit_transform(data)

from typing import Any
from venv import logger

from joblib import hash as hashlib


def hsh(data: Any) -> str:
    """Hash the given data."""
    hash_ = hashlib(data)
    if hash_ is None:
        msg = f"Could not hash data: {data}"

        logger.error(msg)
        raise ValueError(msg)

    return hash_

import pickle  # noqa: S403
from pathlib import Path
from typing import Any


def write(obj: Any, path: str | Path) -> None:
    """
    Serialize an object and write it to a file.

    Parameters
    ----------
    obj : T
        The object to serialize.
    path : str
        The file path to write the object to.

    """
    # Create path if it doesn't exist
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    with Path(path).open("wb") as file:
        pickle.dump(obj, file)


def load(path: str | Path) -> Any:
    """
    Load and deserialize an object from a pickle file.

    Parameters
    ----------
    path : str
        The file path to read the object from

    Returns
    -------
        The deserialized object.

    """
    with Path(path).open("rb") as file:
        return pickle.load(file)  # noqa: S301

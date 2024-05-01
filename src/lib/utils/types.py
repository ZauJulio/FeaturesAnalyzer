from collections.abc import Callable
from typing import Any


def nn(value: Any | None):  # noqa: ANN201, ANN401
    """Assert that a value is not None."""
    if value is None:
        msg = "Value cannot be None"
        raise ValueError(msg)

    return value


def property_meta(
    base: type,
    ignore_state: bool = False,  # noqa: FBT001, FBT002
) -> Callable:
    """Check if a class has all the properties from a base class."""

    def decorator(cls: type) -> object:
        """Check if a class has all the properties from a base class."""
        missing_props = []

        for prop in base.__annotations__:
            prop_access = prop.split("__")
            is_private = len(prop_access) > 1
            has_prop = prop in cls.__annotations__

            if ignore_state and prop == "state":
                continue

            if not is_private and not has_prop:
                missing_props.append(prop)

        if missing_props:
            verbose = {}

            for prop in missing_props:
                verbose[prop] = base.__annotations__[prop]

            msg = f"Missing properties in {cls.__name__}: {verbose}"
            raise ValueError(msg)
        return cls

    return decorator

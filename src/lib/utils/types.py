from typing import Any, TypeVar


def nn(value: Any | None):  # noqa: ANN201
    """
    Assert that a value is not None.

    Parameters
    ----------
    value: Any | None
        The value to be checked.

    Raises
    ------
    ValueError
        If the value is None.

    Returns
    -------
    Any
        The value if it is not None.

    """
    if value is None:
        msg = "Value cannot be None"
        raise ValueError(msg)

    return value


T = TypeVar("T", bound=type)


class MetaCheckGenerator:
    """Generator for creating metaclass-based decorators."""

    def __init__(self, base_class: type, ignore_state: bool = False) -> None:
        """
        Initialize the generator with a base class and optional parameters.

        Parameters
        ----------
        base_class: type
            The base class to be checked against.
        ignore_state: bool
            Whether to ignore the 'state' property during checks.

        """
        self.base_class = base_class
        self.ignore_state = ignore_state

    def __call__(self, cls: T) -> T:
        """
        Apply the generated decorator to the given class.

        Parameters
        ----------
        cls: T
            The class to be checked against the base class.

        Raises
        ------
        ValueError
            If the class does not have all the properties from the base class.

        """
        missing_props = []

        for prop in self.base_class.__annotations__:
            # Check if the property is private or has a property
            prop_access = prop.split("__")
            is_private = len(prop_access) > 1

            # Check if the property is in the class annotations
            has_prop = prop in cls.__annotations__

            # Ignore state property
            if self.ignore_state and prop == "state":
                continue

            if not is_private and not has_prop:
                missing_props.append(prop)

        if missing_props:
            verbose = {
                prop: self.base_class.__annotations__[prop] for prop in missing_props
            }
            msg = f"Missing properties in {cls.__name__}: {verbose}"
            raise ValueError(msg)

        return cls

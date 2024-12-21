"""Interfaces."""

from .state import StateGeneric  # noqa: I001
from .widget import GenericWidget
from .controller import GenericController, FAController, FAMetaCheckController
from .module import GenericModule, FAModule, FAMetaCheckModule
from .application import FAApplication, FAMetaCheckApplication

__all__ = [
    "FAApplication",
    "FAController",
    "FAMetaCheckApplication",
    "FAMetaCheckController",
    "FAMetaCheckModule",
    "FAModule",
    "GenericController",
    "GenericModule",
    "GenericWidget",
    "StateGeneric",
]

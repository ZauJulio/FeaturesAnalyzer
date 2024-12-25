from interfaces import FAMetaCheckModule, FAModule

from . import KMeansSolverController, KMeansSolverState


@FAMetaCheckModule
class KMeansSolverModule(FAModule[KMeansSolverController, KMeansSolverState]):
    """KMeans Solver module."""

    name: str = "KMeansSolver"
    controller: KMeansSolverController

    def __init__(self, state: KMeansSolverState) -> None:
        super().__init__(controller=KMeansSolverController(state))

        self.subscribe()

    def subscribe(self) -> None:
        """Load the module subscribers."""
        # On track changes, update the module
        # show button to commit changes
        self.state.on_change(
            "on_untrack",
            lambda *_: self.controller.widget.on_module_change(),
        )

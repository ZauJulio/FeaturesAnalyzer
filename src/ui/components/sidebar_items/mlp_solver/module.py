from interfaces import FAMetaCheckModule, FAModule

from . import MLPSolverController, MLPSolverState


@FAMetaCheckModule
class MLPSolverModule(FAModule[MLPSolverController, MLPSolverState]):
    """KMeans Solver module."""

    name: str = "MLPSolver"
    controller: MLPSolverController

    def __init__(self, state: MLPSolverState) -> None:
        super().__init__(controller=MLPSolverController(state))

        self.subscribe()

    def subscribe(self) -> None:
        """Load the module subscribers."""
        # On track changes, update the module
        # show button to commit changes
        self.state.on_change(
            "on_untrack",
            lambda *_: self.controller.widget.on_module_change(),
        )

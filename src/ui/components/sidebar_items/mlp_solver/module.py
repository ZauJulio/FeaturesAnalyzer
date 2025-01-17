from typing import TYPE_CHECKING

from interfaces import FAMetaCheckModule, FAModule

from . import MLPSolverController, MLPSolverState

if TYPE_CHECKING:
    from app import FeaturesAnalyzer


@FAMetaCheckModule
class MLPSolverModule(FAModule[MLPSolverController, MLPSolverState]):
    """KMeans Solver module."""

    name: str = "MLPSolver"
    app: "FeaturesAnalyzer"
    controller: MLPSolverController

    def __init__(self, app: "FeaturesAnalyzer", state: MLPSolverState) -> None:
        super().__init__(app=app, controller=MLPSolverController(state))

    def subscribe(self) -> None:
        """Load the module subscribers."""
        # On track changes, update the module
        # show button to commit changes
        self.controller.widget.handle_status(state=self.state)

        with self.state as state:
            state.on_change(
                "on_commit",
                lambda *_: state.handle_001_on_params_update(self.app),
            )

            state.on_change("on_commit", lambda *_: self.app.store.dump())

            state.on_change(
                "on_untrack",
                lambda *_: self.controller.widget.on_module_change(),
            )

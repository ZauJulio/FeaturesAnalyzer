from typing import TYPE_CHECKING

from interfaces import FAMetaCheckModule, FAModule

from . import KMeansSolverController, KMeansSolverState

if TYPE_CHECKING:
    from app import FeaturesAnalyzer


@FAMetaCheckModule
class KMeansSolverModule(FAModule[KMeansSolverController, KMeansSolverState]):
    """KMeans Solver module."""

    name: str = "KMeansSolver"
    app: "FeaturesAnalyzer"
    controller: KMeansSolverController

    def __init__(self, app: "FeaturesAnalyzer", state: KMeansSolverState) -> None:
        super().__init__(app=app, controller=KMeansSolverController(state))

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

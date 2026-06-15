"""
cydgui.core.view
================

Convenience base class for declarative screen creation.

A View is a specialized Screen that automatically calls
build() during initialization.

Responsibilities
----------------
- Provide declarative screen construction.
- Keep a reference to the application.
- Expose a simple navigation API.
- Remain lightweight and MicroPython-friendly.

Example
-------

class MainView(View):

    def build(self):

        self.add(
            Label(
                text="Hello"
            )
        )

    def on_settings(self, button):

        self.navigate("settings")
"""

from cydgui.core.screen import Screen


class View(Screen):
    """Declarative screen base class."""

    def __init__(
        self,
        app=None,
        name: str|None = None,
        parameters: dict | None = None
    ) -> None:
        """
        Initialize view.

        Args:
            app:
                Optional application instance.
            name:
                Optional screen name.
            parameters:
                Optional dictionary of parameters.
        """

        self.app = app
        self.parameters = parameters

        super().__init__(
            name=name or self.__class__.__name__
        )

        self.build()

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate(self, route: str, parameters: dict | None = None) -> None:

        if self.app is None:
            return

        # IMPORTANT: allow cleanup hook
        if hasattr(self, "destroy"):
            try:
                self.destroy()
            except:
                pass

        if parameters is None:
            parameters = {}

        self.app.navigate(route, parameters=parameters)
    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def build(self) -> None:
        """
        Build widget hierarchy.

        Override in subclasses.
        """
        pass

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}')"
        )
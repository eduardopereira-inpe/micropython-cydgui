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
        name: str = None
    ) -> None:
        """
        Initialize view.

        Args:
            app:
                Optional application instance.
            name:
                Optional screen name.
        """

        self.app = app

        super().__init__(
            name=name or self.__class__.__name__
        )

        self.build()

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate(
        self,
        route: str
    ) -> None:
        """
        Navigate to another registered route.

        Args:
            route:
                Route name.
        """

        if self.app is None:
            return

        self.app.navigate(route)

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
"""
cydgui.core.screen
==================

A Screen represents a complete application view and acts as the
root container of a widget hierarchy.
"""

from cydgui.core.container import Container


class Screen(Container):
    """Root container representing a full application screen."""

    def __init__(
        self,
        name: str = "",
        background: int = 0x0000
    ) -> None:

        super().__init__(
            x=0,
            y=0,
            width=0,
            height=0
        )

        self.name = name
        self.background = background

        self._dirty = True
        self._needs_clear = False

    # ------------------------------------------------------------------
    # Dirty state
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Dirty state (Substitua os métodos dirty e validate atuais)
    # ------------------------------------------------------------------

    @property
    def dirty(self) -> bool:
        """Return screen invalidation state."""
        return self._dirty or len(self._dirty_children) > 0

    def invalidate(self) -> None:
        """Mark screen as requiring redraw."""
        self._dirty = True

    def validate(self) -> None:
        """Mark screen as rendered."""
        self._dirty = False
        self._dirty_children.clear()

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        """
        Draw the complete screen.

        The screen is responsible for clearing the display
        before drawing the widget tree.
        """

        if not self.visible:
            return
        
        if self._needs_clear:

            renderer.clear(self.background)

            self._needs_clear = False

        super().draw(renderer)

        self.validate()

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def dispatch_touch(self, event) -> bool:
        """
        Dispatch touch event through widget tree.
        """

        return self.on_touch(event)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def on_enter(self) -> None:
        """Called when screen becomes active."""
        self.invalidate()
        self._needs_clear = True

    def on_leave(self) -> None:
        """Called before screen is removed."""
        pass

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"Screen("
            f"name='{self.name}', "
            f"children={len(self.children)})"
        )
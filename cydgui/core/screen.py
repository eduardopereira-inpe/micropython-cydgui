
"""
cydgui.core.screen
==================

A Screen represents a complete application view and acts as the
root container of a widget hierarchy.

Responsibilities
----------------
- Host top-level widgets.
- Act as the root of the widget tree.
- Manage screen lifecycle callbacks.
- Track invalidation state.
- Forward rendering to child widgets.
- Forward touch events to the widget tree.

Notes
-----
- A Screen does not know anything about the display hardware.
- A Screen does not interact directly with the renderer.
- Navigation decides which Screen is currently active.
"""

from cydgui.core.container import Container


class Screen(Container):
    """Root container representing a full application screen.

    Args:
        name: Optional screen identifier.
    """

    def __init__(self, name: str = "") -> None:
        super().__init__(
            x=0,
            y=0,
            width=0,
            height=0
        )

        self.name = name
        self._dirty = True

    @property
    def dirty(self) -> bool:
        """Return the current invalidation state."""
        return self._dirty

    # ------------------------------------------------------------------
    # Invalidation
    # ------------------------------------------------------------------

    def invalidate(self) -> None:
        """Mark the screen as requiring redraw."""
        self._dirty = True

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        """Draw the widget tree.

        Args:
            renderer: Active renderer instance.
        """

        if not self.visible:
            return

        super().draw(renderer)

        self._dirty = False

    # ------------------------------------------------------------------
    # Input events
    # ------------------------------------------------------------------

    def dispatch_touch(self, event) -> bool:
        """Dispatch a touch event through the widget tree.

        Args:
            event: TouchEvent instance.

        Returns:
            True if the event was handled.
        """

        return self.on_touch(event)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def on_enter(self) -> None:
        """Called when the screen becomes active."""

        self.invalidate()

    def on_leave(self) -> None:
        """Called before the screen is deactivated."""
        pass

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a debug representation."""

        return (
            f"Screen("
            f"name='{self.name}', "
            f"children={len(self.children)})"
        )
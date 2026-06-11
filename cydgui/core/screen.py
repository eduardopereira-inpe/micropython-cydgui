"""
cydgui.core.screen
==================

A ``Screen`` is a full-display view that acts as the root container for all
widgets shown at a given time.

Responsibilities
----------------
- Own the root widget tree for one logical "page" of the UI.
- Receive lifecycle callbacks from the navigation system (``on_enter``,
  ``on_leave``).
- Forward draw calls to its root container.
- Forward input events to the widget tree via the EventDispatcher.

Notes
-----
- Only one Screen is active at a time.
- The :class:`~cydgui.core.navigation.Navigation` stack decides which screen
  is current.
- Screens do *not* access the display directly.
"""

from cydgui.core.container import Container


class Screen:
    """A full-screen view that hosts the widget tree.

    Parameters
    ----------
    name:
        An optional human-readable identifier (useful for debugging).
    """

    def __init__(self, name: str = "") -> None:
        # TODO: store name
        # TODO: create root Container instance
        # TODO: store dirty flag
        pass

    # ------------------------------------------------------------------
    # Widget tree management
    # ------------------------------------------------------------------

    def add(self, widget) -> None:
        """Add *widget* to the root container.

        TODO: delegate to self._root.add(widget)
        TODO: call widget.on_attach(self._root)
        """
        pass

    def remove(self, widget) -> None:
        """Remove *widget* from the root container.

        TODO: delegate to self._root.remove(widget)
        TODO: call widget.on_detach()
        """
        pass

    # ------------------------------------------------------------------
    # Dirty tracking
    # ------------------------------------------------------------------

    def invalidate(self) -> None:
        """Mark the entire screen as needing a redraw.

        TODO: propagate to root container
        """
        pass

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        """Draw all visible, dirty widgets via *renderer*.

        TODO: delegate to self._root.draw(renderer)
        """
        pass

    # ------------------------------------------------------------------
    # Input events
    # ------------------------------------------------------------------

    def dispatch_touch(self, event) -> bool:
        """Forward a touch event into the widget tree.

        TODO: delegate to self._root.on_touch(event)
        """
        return False

    # ------------------------------------------------------------------
    # Lifecycle callbacks (called by Navigation)
    # ------------------------------------------------------------------

    def on_enter(self) -> None:
        """Called when this screen becomes the active screen.

        TODO: mark screen as dirty so it is fully redrawn on entry
        TODO: override in subclasses for custom entry logic
        """
        pass

    def on_leave(self) -> None:
        """Called just before this screen is replaced or popped.

        TODO: override in subclasses for custom leave / cleanup logic
        """
        pass

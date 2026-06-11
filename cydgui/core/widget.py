"""
cydgui.core.widget
==================

Base class for every visual element in the cydgui framework.

Design contract
---------------
- A ``Widget`` knows its own geometry (x, y, width, height).
- A ``Widget`` *never* holds a reference to the renderer or the display
  driver; it only calls ``invalidate()`` to request a redraw.
- Drawing is the exclusive responsibility of the
  :class:`~cydgui.render.renderer.Renderer`.
- Every widget exposes ``draw(renderer)`` so the renderer can call back into
  the widget to obtain draw commands.
- Input events reach the widget via the
  :class:`~cydgui.core.events.EventDispatcher`.

Lifecycle
---------
1. Widget is instantiated and added to a Container or Screen.
2. When visible state changes, ``invalidate()`` is called.
3. The App/Renderer pipeline eventually calls ``draw(renderer)``.
"""

from cydgui.utils.geometry import Rect


class Widget:
    """Abstract base widget.

    Parameters
    ----------
    x, y:
        Top-left corner of the widget in screen coordinates.
    width, height:
        Dimensions in pixels.
    visible:
        Initial visibility state.
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0,
        visible: bool = True,
    ) -> None:
        # TODO: store geometry as a Rect
        # TODO: store visible flag
        # TODO: store dirty flag (True initially so first draw happens)
        # TODO: store parent reference (None until added to a container)
        pass

    # ------------------------------------------------------------------
    # Geometry
    # ------------------------------------------------------------------

    @property
    def rect(self) -> Rect:
        """Return the bounding rectangle of this widget.

        TODO: return self._rect
        """
        pass

    # ------------------------------------------------------------------
    # Visibility & dirty tracking
    # ------------------------------------------------------------------

    def invalidate(self) -> None:
        """Mark this widget as needing a redraw.

        TODO: set self._dirty = True
        TODO: propagate invalidation up to parent if available
        """
        pass

    def is_dirty(self) -> bool:
        """Return True if this widget needs to be redrawn.

        TODO: return self._dirty
        """
        pass

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        """Draw this widget using *renderer*.

        This method is called by the rendering pipeline; subclasses must
        override it.

        TODO: implement in subclasses
        TODO: clear self._dirty after drawing
        """
        pass

    # ------------------------------------------------------------------
    # Input events
    # ------------------------------------------------------------------

    def on_touch(self, event) -> bool:
        """Handle a touch event.  Return True if the event was consumed.

        TODO: implement in subclasses that are interactive
        """
        return False

    def on_touch_release(self, event) -> bool:
        """Handle a touch-release event.  Return True if consumed.

        TODO: implement in subclasses
        """
        return False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def on_attach(self, parent) -> None:
        """Called when this widget is added to a parent container.

        TODO: store parent reference
        """
        pass

    def on_detach(self) -> None:
        """Called when this widget is removed from its parent.

        TODO: clear parent reference
        """
        pass

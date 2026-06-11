"""
cydgui.widgets.canvas
=====================

Free-draw surface widget.

A ``Canvas`` provides a blank rectangular area that the application can draw
on freely by registering a ``draw_callback``.  This is useful for custom
charts, gauges, or any widget whose appearance cannot be expressed with the
standard primitives.

Design notes
------------
- The ``draw_callback`` signature is ``callback(canvas, renderer) -> None``.
- The canvas itself is completely passive; it just calls the registered
  callback inside its ``draw()`` method.
- Calling ``invalidate()`` on the canvas causes the callback to be invoked on
  the next render pass.
"""

from cydgui.core.widget import Widget


class Canvas(Widget):
    """A widget that exposes a raw drawing surface to application code.

    Parameters
    ----------
    x, y:
        Top-left corner.
    width, height:
        Canvas dimensions in pixels.
    draw_callback:
        ``callback(canvas, renderer) -> None`` invoked every time the canvas
        needs to be redrawn.
    bg:
        Background fill colour applied before the callback.  Use ``None`` for
        transparent (no fill).
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0,
        draw_callback=None,
        bg: int = None,
    ) -> None:
        super().__init__(x=x, y=y, width=width, height=height)
        # TODO: store draw_callback and bg
        pass

    # ------------------------------------------------------------------
    # Callback management
    # ------------------------------------------------------------------

    def set_draw_callback(self, callback) -> None:
        """Set or replace the draw callback.

        TODO: store callback, call invalidate()
        """
        pass

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        """Fill background (if any) and invoke the draw callback.

        TODO: if self._bg is not None, call renderer.fill_rect(...)
        TODO: if self._draw_callback is set, call it with (self, renderer)
        TODO: clear self._dirty
        """
        pass

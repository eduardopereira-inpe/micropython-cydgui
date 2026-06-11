"""
cydgui.widgets.label
====================

Static or dynamic text display widget.

A ``Label`` renders a string of text at a fixed position.  It uses the active
theme's foreground colour and default font unless overridden.

Design notes
------------
- The label does *not* wrap text automatically.  Use multiple labels or a
  future ``TextArea`` widget for multi-line content.
- Call ``set_text(value)`` to change the displayed string; this automatically
  calls ``invalidate()`` so the renderer redraws only this widget.
- Background is transparent by default (``bg=None``).
"""

from cydgui.core.widget import Widget


class Label(Widget):
    """Displays a single line of text.

    Parameters
    ----------
    x, y:
        Top-left corner of the label.
    text:
        Initial text string.
    color:
        Text colour (RGB565).  When *None* the theme foreground is used.
    bg:
        Background fill colour (RGB565).  When *None* the background is
        transparent.
    font:
        Font reference or driver font object.  When *None* the theme default
        font is used.
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        text: str = "",
        color: int = None,
        bg: int = None,
        font=None,
    ) -> None:
        super().__init__(x=x, y=y)
        # TODO: store text, color, bg, font
        pass

    # ------------------------------------------------------------------
    # Text management
    # ------------------------------------------------------------------

    def set_text(self, value: str) -> None:
        """Update the displayed text and request a redraw.

        TODO: update self._text
        TODO: call self.invalidate()
        """
        pass

    def get_text(self) -> str:
        """Return the current text string.

        TODO: return self._text
        """
        return ""

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        """Render the label text via *renderer*.

        TODO: resolve color from self._color or renderer.theme.foreground
        TODO: call renderer.draw_text(self._rect.x, self._rect.y,
                                      self._text, color, self._font, self._bg)
        TODO: clear self._dirty
        """
        pass

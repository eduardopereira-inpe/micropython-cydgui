"""
cydgui.widgets.image
====================

Bitmap / raw image display widget.

An ``Image`` widget renders a raw pixel buffer or a 1-bit monochrome bitmap at
a given position.  It is intentionally minimal; more complex image formats can
be handled by subclasses or helper utilities.

Supported source formats (planned)
-----------------------------------
- Raw RGB565 buffer (``bytes`` or ``bytearray``).
- 1-bit monochrome bitmap (e.g. XBM format).
- A file path string (future: stream from flash / SD card).

Design notes
------------
- The image does not scale or decode on its own; the renderer handles that.
- Width and height must be provided at construction time (no auto-detect).
- Changing the source via ``set_source()`` triggers ``invalidate()``.
"""

from cydgui.core.widget import Widget


class Image(Widget):
    """Displays a bitmap image.

    Parameters
    ----------
    x, y:
        Top-left corner.
    width, height:
        Image dimensions in pixels.
    source:
        Raw pixel buffer, bitmap bytes, or a file path string.
    transparent_color:
        Optional colour value treated as transparent (chroma key).
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0,
        source=None,
        transparent_color: int = None,
    ) -> None:
        super().__init__(x=x, y=y, width=width, height=height)
        # TODO: store source and transparent_color
        pass

    # ------------------------------------------------------------------
    # Source management
    # ------------------------------------------------------------------

    def set_source(self, source) -> None:
        """Update the image source and request a redraw.

        TODO: store source, call invalidate()
        """
        pass

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        """Blit the image to the display via *renderer*.

        TODO: call renderer.draw_bitmap(x, y, source, width, height)
        TODO: handle transparent_color if set
        TODO: clear self._dirty
        """
        pass

"""
cydgui.render.renderer
======================

Abstract renderer interface.

All display-specific renderers must subclass :class:`Renderer` and implement
every method.  Widgets receive the renderer as a parameter to their
``draw(renderer)`` call and must only use the methods declared here, keeping
widget code display-agnostic.

Coordinate system
-----------------
- Origin (0, 0) is the top-left corner of the display.
- x increases to the right, y increases downward.
- All coordinates are in integer pixels.

Colour format
-------------
- Colours are 16-bit RGB565 integers by default (matches ILI9341 native
  format).  Concrete renderers may accept other formats as long as they
  document their convention.

Notes
-----
- MicroPython does not support ``abc.ABCMeta``; the "abstract" nature of this
  class is enforced by convention: every method raises ``NotImplementedError``.
"""

from cydgui.core.theme import Theme
from cydgui.utils.geometry import Rect


class Renderer:
    """Abstract renderer — defines the drawing API available to widgets.

    Parameters
    ----------
    width, height:
        Display resolution in pixels.
    theme:
        The active :class:`~cydgui.core.theme.Theme`; widgets may query the
        renderer for theme values rather than holding a theme reference
        themselves.
    """

    def __init__(self, width: int, height: int, theme: Theme = None) -> None:
        # TODO: store width, height, theme
        pass

    # ------------------------------------------------------------------
    # Display control
    # ------------------------------------------------------------------

    def clear(self, color: int = 0x0000) -> None:
        """Fill the entire display with *color*.

        TODO: implement in subclass
        """
        raise NotImplementedError

    def flush(self) -> None:
        """Push the frame buffer to the physical display (if double-buffered).

        TODO: implement in subclass
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Primitive drawing
    # ------------------------------------------------------------------

    def draw_pixel(self, x: int, y: int, color: int) -> None:
        """Draw a single pixel.

        TODO: implement in subclass
        """
        raise NotImplementedError

    def draw_line(self, x0: int, y0: int, x1: int, y1: int, color: int) -> None:
        """Draw a line from (x0, y0) to (x1, y1).

        TODO: implement in subclass
        """
        raise NotImplementedError

    def draw_rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        """Draw a hollow rectangle.

        TODO: implement in subclass
        """
        raise NotImplementedError

    def fill_rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        """Draw a filled rectangle.

        TODO: implement in subclass
        """
        raise NotImplementedError

    def draw_circle(self, x: int, y: int, r: int, color: int) -> None:
        """Draw a hollow circle centred at (x, y) with radius *r*.

        TODO: implement in subclass
        """
        raise NotImplementedError

    def fill_circle(self, x: int, y: int, r: int, color: int) -> None:
        """Draw a filled circle.

        TODO: implement in subclass
        """
        raise NotImplementedError

    def draw_round_rect(
        self, x: int, y: int, w: int, h: int, r: int, color: int
    ) -> None:
        """Draw a hollow rectangle with rounded corners of radius *r*.

        TODO: implement in subclass
        """
        raise NotImplementedError

    def fill_round_rect(
        self, x: int, y: int, w: int, h: int, r: int, color: int
    ) -> None:
        """Draw a filled rectangle with rounded corners.

        TODO: implement in subclass
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Text
    # ------------------------------------------------------------------

    def draw_text(
        self,
        x: int,
        y: int,
        text: str,
        color: int,
        font=None,
        bg: int = None,
    ) -> None:
        """Render *text* starting at (x, y).

        Parameters
        ----------
        font:
            A :class:`~cydgui.core.theme.FontRef` or a driver-specific font
            object.  When None the renderer uses its default font.
        bg:
            Optional background colour for the text bounding box.

        TODO: implement in subclass
        """
        raise NotImplementedError

    def text_size(self, text: str, font=None) -> tuple:
        """Return the (width, height) in pixels of *text* rendered with *font*.

        TODO: implement in subclass
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Image / bitmap
    # ------------------------------------------------------------------

    def draw_bitmap(
        self,
        x: int,
        y: int,
        bitmap,
        w: int,
        h: int,
        color: int = None,
        bg: int = None,
    ) -> None:
        """Draw a 1-bit or raw bitmap at (x, y).

        TODO: implement in subclass
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Clipping
    # ------------------------------------------------------------------

    def set_clip(self, rect: Rect) -> None:
        """Restrict all drawing to *rect*.

        TODO: implement in subclass if supported by the hardware
        """
        raise NotImplementedError

    def clear_clip(self) -> None:
        """Remove any active clipping rectangle.

        TODO: implement in subclass
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Theme access
    # ------------------------------------------------------------------

    @property
    def theme(self) -> Theme:
        """Return the active theme.

        TODO: return self._theme
        """
        pass

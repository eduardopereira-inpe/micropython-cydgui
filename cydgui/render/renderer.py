"""
cydgui.render.renderer
======================

Abstract renderer interface.

All display-specific renderers must subclass Renderer and implement
the drawing methods defined here.

Widgets must only use this API, keeping them independent from
the underlying display driver.
"""

from cydgui.utils.geometry import Rect


class Renderer:
    """Abstract renderer.

    Args:
        width: Display width in pixels.
        height: Display height in pixels.
        theme: Optional theme object.
    """

    def __init__(
        self,
        width: int,
        height: int,
        theme=None
    ) -> None:

        self._width = width
        self._height = height

        self._theme = theme

        self._clip_rect = None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def width(self) -> int:
        """Display width."""
        return self._width

    @property
    def height(self) -> int:
        """Display height."""
        return self._height

    @property
    def theme(self):
        """Current theme object."""
        return self._theme

    @property
    def clip_rect(self):
        """Current clipping rectangle."""
        return self._clip_rect

    # ------------------------------------------------------------------
    # Display control
    # ------------------------------------------------------------------

    def clear(self, color: int = 0x0000) -> None:
        """Clear entire display."""
        raise NotImplementedError

    def flush(self) -> None:
        """Flush pending drawing operations."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Primitive drawing
    # ------------------------------------------------------------------

    def draw_pixel(
        self,
        x: int,
        y: int,
        color: int
    ) -> None:
        """Draw a single pixel."""
        raise NotImplementedError

    def draw_line(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        color: int
    ) -> None:
        """Draw a line."""
        raise NotImplementedError

    def draw_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        color: int
    ) -> None:
        """Draw rectangle outline."""
        raise NotImplementedError

    def fill_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        color: int
    ) -> None:
        """Draw filled rectangle."""
        raise NotImplementedError

    def draw_circle(
        self,
        x: int,
        y: int,
        radius: int,
        color: int
    ) -> None:
        """Draw circle outline."""
        raise NotImplementedError

    def fill_circle(
        self,
        x: int,
        y: int,
        radius: int,
        color: int
    ) -> None:
        """Draw filled circle."""
        raise NotImplementedError

    def draw_round_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        radius: int,
        color: int
    ) -> None:
        """Draw rounded rectangle outline."""
        raise NotImplementedError

    def fill_round_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        radius: int,
        color: int
    ) -> None:
        """Draw filled rounded rectangle."""
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
        bg: int = None
    ) -> None:
        """Draw text."""
        raise NotImplementedError

    def text_size(
        self,
        text: str,
        font=None
    ) -> tuple:
        """Return text size."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Images
    # ------------------------------------------------------------------

    def draw_bitmap(
        self,
        x: int,
        y: int,
        bitmap,
        w: int,
        h: int,
        color: int = None,
        bg: int = None
    ) -> None:
        """Draw bitmap."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Clipping
    # ------------------------------------------------------------------

    def set_clip(
        self,
        rect: Rect
    ) -> None:
        """Set clipping rectangle."""

        self._clip_rect = rect

    def clear_clip(self) -> None:
        """Remove clipping rectangle."""

        self._clip_rect = None

    def in_clip(
        self,
        x: int,
        y: int
    ) -> bool:
        """Check whether a point is inside the clipping region."""

        if self._clip_rect is None:
            return True

        return self._clip_rect.contains(
            x,
            y
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def invalidate(self) -> None:
        """Optional hook for buffered renderers."""
        pass

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"width={self.width}, "
            f"height={self.height})"
        )
"""
cydgui.widgets.image
====================

Image widget.

Displays a bitmap or sprite using the active renderer.

Design goals
------------
- Renderer agnostic.
- Lightweight for MicroPython.
- No image decoding.
- Accepts already-loaded bitmap objects.
"""

from cydgui.core.widget import Widget


class Image(Widget):
    """Image widget."""

    LEFT = 0
    CENTER = 1
    RIGHT = 2

    TOP = 0
    MIDDLE = 1
    BOTTOM = 2

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 32,
        height: int = 32,
        bitmap=None,
        bitmap_width: int = 0,
        bitmap_height: int = 0,
        align: int = LEFT,
        valign: int = TOP,
    ) -> None:
        """
        Initialize image widget.

        Args:
            x: Left position.
            y: Top position.
            width: Widget width.
            height: Widget height.
            bitmap: Bitmap object.
            bitmap_width: Bitmap width.
            bitmap_height: Bitmap height.
            align: Horizontal alignment.
            valign: Vertical alignment.
        """

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height
        )

        self._bitmap = bitmap

        self._bitmap_width = bitmap_width
        self._bitmap_height = bitmap_height

        self._align = align
        self._valign = valign

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def bitmap(self):
        """Return current bitmap."""

        return self._bitmap

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def set_bitmap(
        self,
        bitmap,
        width: int,
        height: int
    ) -> None:
        """
        Replace image bitmap.

        Args:
            bitmap: New bitmap.
            width: Bitmap width.
            height: Bitmap height.
        """

        self._bitmap = bitmap

        self._bitmap_width = width
        self._bitmap_height = height

        self.invalidate()

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(
        self,
        renderer
    ) -> None:
        """Draw image."""

        if not self.visible:
            return

        if self._bitmap is None:
            self.validate()
            return

        x = self.absolute_x
        y = self.absolute_y

        #
        # Horizontal alignment
        #

        if self._align == self.CENTER:

            x += (
                self.width -
                self._bitmap_width
            ) // 2

        elif self._align == self.RIGHT:

            x += (
                self.width -
                self._bitmap_width
            )

        #
        # Vertical alignment
        #

        if self._valign == self.MIDDLE:

            y += (
                self.height -
                self._bitmap_height
            ) // 2

        elif self._valign == self.BOTTOM:

            y += (
                self.height -
                self._bitmap_height
            )

        renderer.draw_bitmap(
            x=x,
            y=y,
            bitmap=self._bitmap,
            w=self._bitmap_width,
            h=self._bitmap_height
        )

        self.validate()

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def on_touch(
        self,
        event
    ) -> bool:
        """
        Images do not consume touch events.
        """

        return False

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"Image("
            f"x={self.x}, "
            f"y={self.y}, "
            f"width={self.width}, "
            f"height={self.height})"
        )
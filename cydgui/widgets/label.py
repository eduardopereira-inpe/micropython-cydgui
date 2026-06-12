"""
cydgui.widgets.label
====================

Text display widget.
"""

from cydgui.core.widget import Widget


class Label(Widget):
    """Static text widget."""

    LEFT = 0
    CENTER = 1
    RIGHT = 2

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 20,
        text: str = "",
        color: int = 0xFFFF,
        font=None,
        align: int = LEFT,
    ) -> None:

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height
        )

        self._text = text
        self._color = color
        self._font = font

        self._align = align

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def text(self) -> str:
        """Return label text."""
        return self._text

    @property
    def color(self) -> int:
        """Return text color."""
        return self._color

    @property
    def font(self):
        """Return font."""
        return self._font

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def set_text(
        self,
        value: str
    ) -> None:
        """Update label text."""

        if self._text == value:
            return

        self._text = value

        self.invalidate()

    def set_color(
        self,
        value: int
    ) -> None:
        """Update text color."""

        if self._color == value:
            return

        self._color = value

        self.invalidate()

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(
        self,
        renderer
    ) -> None:
        """Draw label."""

        if not self.visible:
            return

        text_w, text_h = renderer.text_size(
            self._text,
            self._font
        )

        x = self.absolute_x

        if self._align == self.CENTER:

            x += (
                self.width - text_w
            ) // 2

        elif self._align == self.RIGHT:

            x += (
                self.width - text_w
            )

        y = self.absolute_y + (
            (self.height - text_h) // 2
        )

        renderer.draw_text(
            x=x,
            y=y,
            text=self._text,
            color=self._color,
            font=self._font
        )

        self.validate()

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def on_touch(self, event) -> bool:
        """Labels do not consume touch events."""
        return False

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"Label("
            f"text='{self._text}', "
            f"x={self.x}, "
            f"y={self.y})"
        )
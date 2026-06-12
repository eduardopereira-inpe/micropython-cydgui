"""
cydgui.widgets.button
=====================

Clickable button widget.

A Button is an interactive widget that fires a callback when tapped.

The widget is renderer-independent and relies only on the
Renderer API.
"""

from cydgui.core.widget import Widget
from cydgui.core.touch_event import TouchEvent


class Button(Widget):
    """Clickable button widget."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 80,
        height: int = 30,
        text: str = "",
        on_press=None,
        color: int = 0xFFFF,
        bg: int = 0x001F,
        radius: int = 4,
        disabled: bool = False
    ) -> None:
        """Initialize button."""

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height
        )

        self._text = text
        self._on_press = on_press

        self._color = color
        self._bg = bg

        self._radius = radius

        self._disabled = disabled
        self._pressed = False

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def text(self) -> str:
        """Button text."""

        return self._text

    @property
    def disabled(self) -> bool:
        """Disabled state."""

        return self._disabled

    @property
    def pressed(self) -> bool:
        """Pressed state."""

        return self._pressed

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def set_text(
        self,
        value: str
    ) -> None:
        """Update button text."""

        if self._text == value:
            return

        self._text = value
        self.invalidate()

    def set_disabled(
        self,
        value: bool
    ) -> None:
        """Enable or disable button."""

        if self._disabled == value:
            return

        self._disabled = value
        self.invalidate()

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(
        self,
        renderer
    ) -> None:
        """Draw button."""

        if not self.visible:
            return

        bg = self._bg

        if self._disabled:
            bg = 0x8410

        elif self._pressed:
            bg = self._bg >> 1

        renderer.fill_round_rect(
            self.x,
            self.y,
            self.width,
            self.height,
            self._radius,
            bg
        )

        if self._text:

            text_w, text_h = renderer.text_size(
                self._text
            )

            text_x = (
                self.x +
                ((self.width - text_w) // 2)
            )

            text_y = (
                self.y +
                ((self.height - text_h) // 2)
            )

            renderer.draw_text(
                text_x,
                text_y,
                self._text,
                self._color
            )

        self._dirty = False

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def on_touch(
        self,
        event
    ) -> bool:
        """Handle touch event."""

        if self._disabled:
            return False

        inside = self.contains(
            event.x,
            event.y
        )

        if event.is_down:

            if not inside:
                return False

            self._pressed = True
            self.invalidate()

            return True

        if event.is_up:

            if not self._pressed:
                return False

            self._pressed = False
            self.invalidate()

            if (
                inside and
                callable(self._on_press)
            ):
                self._on_press(self)

            return True

        return self._pressed

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"Button("
            f"text='{self._text}', "
            f"x={self.x}, "
            f"y={self.y}, "
            f"width={self.width}, "
            f"height={self.height})"
        )
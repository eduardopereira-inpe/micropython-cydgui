"""
cydgui.widgets.checkbox
=======================

Checkbox widget.

A Checkbox represents a boolean value that can be toggled by the user.

Features
--------
- Checked / unchecked state
- Optional text label
- Optional callback
- Touch interaction
- Renderer agnostic
"""

from cydgui.core.widget import Widget


class Checkbox(Widget):
    """Checkbox widget."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        size: int = 20,
        text: str = "",
        checked: bool = False,
        color: int = 0xFFFF,
        bg: int = 0x0000,
        check_color: int = 0x07E0,
        font=None,
        on_change=None,
    ) -> None:
        """
        Initialize checkbox.

        Args:
            x: Left position.
            y: Top position.
            size: Checkbox square size.
            text: Optional label.
            checked: Initial state.
            color: Border and text color.
            bg: Background color.
            check_color: Check mark color.
            font: Optional font.
            on_change: Callback(checkbox, checked).
        """

        width = size

        if text:
            width += size + 4 + (len(text) * 8)

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=size
        )

        self._size = size

        self._text = text

        self._checked = checked

        self._color = color
        self._bg = bg

        self._check_color = check_color

        self._font = font

        self._on_change = on_change

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def checked(self) -> bool:
        """Return current state."""
        return self._checked

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def set_checked(
        self,
        value: bool
    ) -> None:
        """
        Set checkbox state.

        Args:
            value: New state.
        """

        value = bool(value)

        if self._checked == value:
            return

        self._checked = value

        self.invalidate()

        if callable(self._on_change):
            self._on_change(
                self,
                self._checked
            )

    def toggle(self) -> None:
        """Toggle checkbox state."""

        self.set_checked(
            not self._checked
        )

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(
        self,
        renderer
    ) -> None:
        """Draw checkbox."""

        if not self.visible:
            return

        x = self.absolute_x
        y = self.absolute_y

        #
        # Checkbox square
        #

        renderer.fill_rect(
            x,
            y,
            self._size,
            self._size,
            self._bg
        )

        renderer.draw_rect(
            x,
            y,
            self._size,
            self._size,
            self._color
        )

        #
        # Check mark
        #

        if self._checked:

            renderer.draw_line(
                x + 4,
                y + self._size // 2,
                x + self._size // 2,
                y + self._size - 4,
                self._check_color
            )

            renderer.draw_line(
                x + self._size // 2,
                y + self._size - 4,
                x + self._size - 4,
                y + 4,
                self._check_color
            )

        #
        # Label
        #

        if self._text:

            text_x = x + self._size + 4

            text_h = renderer.text_size(
                self._text,
                self._font
            )[1]

            text_y = (
                y +
                (self._size - text_h) // 2
            )

            renderer.draw_text(
                text_x,
                text_y,
                self._text,
                self._color,
                self._font
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
        Handle touch event.

        Returns:
            True if consumed.
        """

        if not self.enabled:
            return False

        if not event.is_down:
            return False

        if not self.contains(
            event.x,
            event.y
        ):
            return False

        self.toggle()

        return True

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"Checkbox("
            f"checked={self._checked}, "
            f"text='{self._text}')"
        )
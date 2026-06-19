"""
cydgui.widgets.textbox
======================

Single-line editable text widget.
"""

from cydgui.core.widget import Widget


class TextBox(Widget):
    """Single-line editable text box."""

    __slots__ = (
        "_text",
        "_color",
        "_bg",
        "_border_color",
        "_radius",
        "_font",
        "_max_length",
        "_password",
        "_focused",
        "_cursor_position",
    )

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 120,
        height: int = 30,
        text: str = "",
        color: int = 0xFFFF,
        bg: int = 0x0000,
        border_color: int = 0xFFFF,
        radius: int = 2,
        max_length: int = 64,
        password: bool = False,
        font=None,
    ) -> None:

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height
        )

        self._text = text
        self._color = color
        self._bg = bg

        self._border_color = border_color
        self._radius = radius

        self._font = font

        self._max_length = max_length
        self._password = password

        self._focused = False
        self._cursor_position = len(text)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def text(self) -> str:
        """Return current text."""
        return self._text

    @property
    def focused(self) -> bool:
        """Return focus state."""
        return self._focused

    # ------------------------------------------------------------------
    # Text operations
    # ------------------------------------------------------------------

    def set_text(
        self,
        value: str
    ) -> None:
        """Replace textbox contents."""

        value = str(value)

        if len(value) > self._max_length:
            value = value[:self._max_length]

        self._text = value
        self._cursor_position = len(value)

        self.invalidate()

    def clear(self) -> None:
        """Clear textbox."""

        self._text = ""
        self._cursor_position = 0

        self.invalidate()

    def insert(
        self,
        value: str
    ) -> None:
        """Insert text at cursor position."""

        if not value:
            return

        if len(self._text) >= self._max_length:
            return

        left = self._text[:self._cursor_position]
        right = self._text[self._cursor_position:]

        self._text = left + value + right

        if len(self._text) > self._max_length:
            self._text = self._text[:self._max_length]

        self._cursor_position = len(self._text)

        self.invalidate()

    def backspace(self) -> None:
        """Remove previous character."""

        if not self._text:
            return

        if self._cursor_position <= 0:
            return

        left = self._text[:self._cursor_position - 1]
        right = self._text[self._cursor_position:]

        self._text = left + right

        self._cursor_position -= 1

        self.invalidate()

    # ------------------------------------------------------------------
    # Focus
    # ------------------------------------------------------------------

    def focus(self) -> None:
        """Give focus to textbox."""

        if not self._focused:
            self._focused = True
            self.invalidate()

    def blur(self) -> None:
        """Remove focus."""

        if self._focused:
            self._focused = False
            self.invalidate()

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(
        self,
        renderer
    ) -> None:

        if not self.visible:
            return

        x = self.absolute_x
        y = self.absolute_y

        renderer.fill_round_rect(
            x,
            y,
            self.width,
            self.height,
            self._radius,
            self._bg
        )

        renderer.draw_round_rect(
            x,
            y,
            self.width,
            self.height,
            self._radius,
            self._border_color
        )

        display_text = self._text

        if self._password:
            display_text = "*" * len(display_text)

        text_w, text_h = renderer.text_size(
            display_text,
            self._font
        )

        text_x = x + 4

        text_y = (
            y +
            ((self.height - text_h) // 2)
        )
        
        try:
            renderer.draw_text(
                text_x,
                text_y,
                display_text,
                self._color,
                self._font
            )
        except:
            pass

        #
        # Cursor
        #

        if self._focused:

            cursor_x = text_x + text_w + 1

            renderer.draw_line(
                cursor_x,
                y + 4,
                cursor_x,
                y + self.height - 5,
                self._color
            )

        self.validate()

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def on_touch(
        self,
        event
    ) -> bool:

        if not self.enabled:
            return False

        if not event.is_down:
            return False

        if self.contains(
            event.x,
            event.y
        ):

            self.focus()

            return True

        self.blur()

        return False

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"TextBox("
            f"text='{self._text}', "
            f"x={self.x}, "
            f"y={self.y}, "
            f"width={self.width}, "
            f"height={self.height})"
        )
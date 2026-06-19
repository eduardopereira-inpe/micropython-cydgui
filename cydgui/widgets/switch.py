"""
cydgui.widgets.switch
=====================

Switch widget.

A Switch represents a boolean value using a sliding thumb.

Features
--------
- ON/OFF state
- Touch interaction
- Optional callback
- Renderer agnostic
"""

from cydgui.core.widget import Widget


class Switch(Widget):
    """ON/OFF switch widget."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 50,
        height: int = 24,
        checked: bool = False,
        on_color: int = 0x07E0,
        off_color: int = 0x8410,
        thumb_color: int = 0xFFFF,
        border_color: int = 0xFFFF,
        on_change=None,
    ) -> None:
        """
        Initialize switch.

        Args:
            x: Left position.
            y: Top position.
            width: Switch width.
            height: Switch height.
            checked: Initial state.
            on_color: Background when enabled.
            off_color: Background when disabled.
            thumb_color: Thumb color.
            border_color: Border color.
            on_change: Callback(widget, checked).
        """

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height
        )

        self._checked = checked

        self._on_color = on_color
        self._off_color = off_color

        self._thumb_color = thumb_color
        self._border_color = border_color

        self._on_change = on_change

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def checked(self) -> bool:
        """Return switch state."""
        return self._checked

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def set_checked(
        self,
        value: bool
    ) -> None:
        """
        Set switch state.

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
        """Toggle switch state."""

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
        """Draw switch."""

        if not self.visible:
            return

        x = self.absolute_x
        y = self.absolute_y

        radius = self.height // 2

        #
        # Background
        #

        bg_color = (
            self._on_color
            if self._checked
            else self._off_color
        )

        renderer.fill_round_rect(
            x,
            y,
            self.width,
            self.height,
            radius,
            bg_color
        )

        renderer.draw_round_rect(
            x,
            y,
            self.width,
            self.height,
            radius,
            self._border_color
        )

        #
        # Thumb
        #

        thumb_radius = radius - 2

        if self._checked:

            thumb_x = (
                x +
                self.width -
                radius
            )

        else:

            thumb_x = (
                x +
                radius
            )

        thumb_y = y + radius

        renderer.fill_circle(
            thumb_x,
            thumb_y,
            thumb_radius,
            self._thumb_color
        )

        renderer.draw_circle(
            thumb_x,
            thumb_y,
            thumb_radius,
            self._border_color
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
            f"Switch("
            f"checked={self._checked}, "
            f"x={self.x}, "
            f"y={self.y})"
        )

    def destroy(self) -> None:
        self._on_change = None
        super().destroy()
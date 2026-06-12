"""
cydgui.widgets.progressbar
==========================

A simple progress bar widget for the CYD GUI framework.

The ProgressBar visually represents a numeric value within a range,
rendered as a filled horizontal bar.

Design principles:
- Inherits from Widget base class
- No global state
- Renderer-agnostic drawing
- Supports synchronous and async updates
"""

from cydgui.core.widget import Widget
import uasyncio as asyncio

class ProgressBar(Widget):
    """A horizontal progress bar widget."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 12,
        min_value: int = 0,
        max_value: int = 100,
        value: int = 0,
        bar_color: int = 0x07E0,        # green (RGB565 default)
        bg_color: int = 0x0000,         # black
        border_color: int = 0xFFFF,     # white
        show_border: bool = True,
    ) -> None:
        """
        Initialize the progress bar widget.

        Args:
            x: X position relative to parent.
            y: Y position relative to parent.
            width: Total width of the progress bar.
            height: Height of the progress bar.
            min_value: Minimum value of the range.
            max_value: Maximum value of the range.
            value: Initial progress value.
            bar_color: Color of the filled portion (RGB565).
            bg_color: Background color (RGB565).
            border_color: Border color (RGB565).
            show_border: Whether to render a border around the bar.
        """
        super().__init__(x=x, y=y, width=width, height=height)

        self._min = min_value
        self._max = max_value
        self._value = value

        self._bar_color = bar_color
        self._bg_color = bg_color
        self._border_color = border_color
        self._show_border = show_border

    # ------------------------------------------------------------
    # Value handling
    # ------------------------------------------------------------

    @property
    def value(self) -> int:
        """Return current progress value."""
        return self._value

    def set_value(self, value: int) -> None:
        """
        Set progress value and mark widget for redraw.

        Args:
            value: New progress value.
        """
        self._value = self._clamp(value)
        self.invalidate()

    def increment(self, step: int = 1) -> None:
        """
        Increment progress value.

        Args:
            step: Amount to increase.
        """
        self.set_value(self._value + step)

    def _clamp(self, value: int) -> int:
        """Clamp value inside allowed range."""
        if value < self._min:
            return self._min
        if value > self._max:
            return self._max
        return value

    def _ratio(self) -> float:
        """Return normalized progress ratio (0.0 - 1.0)."""
        if self._max == self._min:
            return 0.0
        return (self._value - self._min) / (self._max - self._min)

    # ------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------

    def draw(self, renderer) -> None:
        """
        Draw the progress bar using the provided renderer.

        Args:
            renderer: Renderer instance responsible for drawing primitives.
        """
        if not self.visible:
            return

        x = self.absolute_x
        y = self.absolute_y
        w = self.width
        h = self.height

        # Background
        renderer.fill_rect(x, y, w, h, self._bg_color)

        # Filled bar
        fill_w = int(w * self._ratio())
        if fill_w > 0:
            renderer.fill_rect(x, y, fill_w, h, self._bar_color)

        # Border
        if self._show_border:
            renderer.draw_rect(x, y, w, h, self._border_color)

        self.validate()

    # ------------------------------------------------------------
    # Async helpers (optional convenience)
    # ------------------------------------------------------------

    async def animate_to(self, target: int, step: int = 1, delay_ms: int = 10) -> None:
        """
        Smoothly animate progress toward a target value.

        Args:
            target: Final value to reach.
            step: Increment step per iteration.
            delay_ms: Delay between steps in milliseconds.
        """


        if target > self._value:
            while self._value < target:
                self.increment(step)
                await asyncio.sleep_ms(delay_ms)
        else:
            while self._value > target:
                self.increment(-step)
                await asyncio.sleep_ms(delay_ms)
"""
cydgui.widgets.gauge
=====================

Circular gauge widget for displaying analog values.

Designed for IoT dashboards on low-power devices like CYD (240x320).

Features:
- Min/max range mapping
- Arc-based rendering
- Needle indicator
- Optional label and value display
- Lightweight approximation (no floating point required if avoided)

Notes:
- Renderer must implement basic primitives:
  - draw_line
  - draw_text
"""

import math
from cydgui.core.widget import Widget


class Gauge(Widget):
    """
    Circular gauge widget.

    Displays a value in a semi-circular dial format.
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        radius: int = 60,
        min_value: int = 0,
        max_value: int = 100,
        value: int = 0,
        start_angle: int = 135,
        end_angle: int = 405,
        color: int = 0xFFFF,
        needle_color: int = 0xF800,
        bg_color: int = 0x0000,
        show_value: bool = True,
        label: str = "",
    ) -> None:
        """
        Initialize gauge widget.

        Args:
            x: Position X (center)
            y: Position Y (center)
            radius: Radius of gauge
            min_value: Minimum value
            max_value: Maximum value
            value: Initial value
            start_angle: Start angle (degrees)
            end_angle: End angle (degrees)
            color: Arc color
            needle_color: Needle color
            bg_color: Background color
            show_value: Show numeric value
            label: Optional label text
        """

        super().__init__(x=x, y=y, width=radius * 2, height=radius * 2)

        self._radius = radius

        self._min = min_value
        self._max = max_value
        self._value = value

        self._start_angle = start_angle
        self._end_angle = end_angle

        self._color = color
        self._needle_color = needle_color
        self._bg_color = bg_color

        self._show_value = show_value
        self._label = label

    # ------------------------------------------------------------
    # Value handling
    # ------------------------------------------------------------

    def set_value(self, value: int) -> None:
        """Update gauge value."""
        if value == self._value:
            return

        self._value = value
        self.invalidate()

    def value(self) -> int:
        return self._value

    # ------------------------------------------------------------
    # Math helpers
    # ------------------------------------------------------------

    def _clamp(self, v, vmin, vmax):
        if v < vmin:
            return vmin
        if v > vmax:
            return vmax
        return v

    def _map_value_to_angle(self) -> float:
        """Map value to angle range."""

        v = self._clamp(self._value, self._min, self._max)

        ratio = (v - self._min) / (self._max - self._min)

        return self._start_angle + ratio * (self._end_angle - self._start_angle)

    def _deg_to_rad(self, deg: float) -> float:
        return deg * 3.141592653 / 180.0

    # ------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------

    def draw(self, renderer) -> None:
        """
        Draw gauge widget.
        """

        if not self.visible:
            return

        cx = self.x + self._radius
        cy = self.y + self._radius

        # background circle (optional simplified)
        renderer.fill_circle(cx, cy, self._radius, self._bg_color)

        # draw arc (segmented approximation)
        steps = 30

        prev_x = None
        prev_y = None

        for i in range(steps + 1):

            angle = self._start_angle + (
                (self._end_angle - self._start_angle) * i / steps
            )

            rad = self._deg_to_rad(angle)

            x = cx + int(self._radius * 0.85 * math.cos(rad))
            y = cy + int(self._radius * 0.85 * math.sin(rad))

            if prev_x is not None:
                renderer.draw_line(prev_x, prev_y, x, y, self._color)

            prev_x = x
            prev_y = y

        # needle
        needle_angle = self._map_value_to_angle()
        rad = self._deg_to_rad(needle_angle)

        nx = cx + int(self._radius * 0.75 * math.cos(rad))
        ny = cy + int(self._radius * 0.75 * math.sin(rad))

        renderer.draw_line(cx, cy, nx, ny, self._needle_color)

        # center dot
        renderer.fill_circle(cx, cy, 3, self._needle_color)

        # label
        if self._label:
            renderer.draw_text(
                self.x,
                self.y + self._radius * 2 - 20,
                self._label,
                self._color,
            )

        # value
        if self._show_value:
            renderer.draw_text(
                cx - 10,
                cy - 10,
                str(self._value),
                self._color,
            )

        self.validate()

    # ------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Gauge("
            f"value={self._value}, "
            f"min={self._min}, "
            f"max={self._max}, "
            f"radius={self._radius})"
        )
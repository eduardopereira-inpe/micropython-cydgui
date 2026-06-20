"""
cydgui.render.ili9341_renderer
==============================

ILI9341 renderer implementation.

This renderer adapts the rdagger/micropython-ili9341 driver to the
generic cydgui Renderer API.
"""

from cydgui.render.renderer import Renderer
import math


_DEFAULT_WIDTH = 240
_DEFAULT_HEIGHT = 320


class ILI9341Renderer(Renderer):
    """ILI9341 renderer implementation."""

    __slots__ = ("_driver",)

    def __init__(
        self,
        driver,
        width=_DEFAULT_WIDTH,
        height=_DEFAULT_HEIGHT,
        theme=None
    ) -> None:

        super().__init__(
            width=width,
            height=height,
            theme=theme
        )

        self._driver = driver

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _inside_display(
        self,
        x: int,
        y: int
    ) -> bool:

        return (
            0 <= x < self.width and
            0 <= y < self.height
        )

    def _inside_clip(
        self,
        x: int,
        y: int
    ) -> bool:

        if self.clip_rect is None:
            return True

        return self.clip_rect.contains(
            x,
            y
        )

    def _can_draw(
        self,
        x: int,
        y: int
    ) -> bool:

        return (
            self._inside_display(x, y) and
            self._inside_clip(x, y)
        )
    
    @property
    def driver(self):
        return self._driver

    # ------------------------------------------------------------------
    # Display control
    # ------------------------------------------------------------------

    def block(self, x0, y0, x1, y1, data):
        self._driver.block(
            x0,
            y0,
            x1,
            y1,
            data
        )

    def clear(
        self,
        color: int = 0x0000
    ) -> None:

        self._driver.clear(color)

    def flush(self) -> None:
        """
        No-op.

        The referenced ILI9341 driver writes directly
        to the display.
        """
        pass

    # ------------------------------------------------------------------
    # Primitive drawing
    # ------------------------------------------------------------------

    def draw_pixel(
        self,
        x: int,
        y: int,
        color: int
    ) -> None:

        if not self._can_draw(x, y):
            return

        self._driver.draw_pixel(
            x,
            y,
            color
        )

    def draw_line(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        color: int
    ) -> None:

        self._driver.draw_line(
            x0,
            y0,
            x1,
            y1,
            color
        )

    def draw_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        color: int
    ) -> None:

        self._driver.draw_rectangle(
            x,
            y,
            w,
            h,
            color
        )

    def fill_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        color: int
    ) -> None:
        
        if w <= 0 or h <= 0:
            return

        self._driver.fill_vrect(
            x,
            y,
            w,
            h,
            color
        )

    def draw_circle(
        self,
        x: int,
        y: int,
        radius: int,
        color: int
    ) -> None:

        self._driver.draw_circle(
            x,
            y,
            radius,
            color
        )

    def fill_circle(
        self,
        x: int,
        y: int,
        radius: int,
        color: int
    ) -> None:

        self._driver.fill_circle(
            x,
            y,
            radius,
            color
        )

    def draw_round_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        radius: int,
        color: int
    ) -> None:

        self.draw_line(
            x + radius,
            y,
            x + w - radius,
            y,
            color
        )

        self.draw_line(
            x + radius,
            y + h,
            x + w - radius,
            y + h,
            color
        )

        self.draw_line(
            x,
            y + radius,
            x,
            y + h - radius,
            color
        )

        self.draw_line(
            x + w,
            y + radius,
            x + w,
            y + h - radius,
            color
        )

    def fill_round_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        radius: int,
        color: int
    ) -> None:

        self.fill_rect(
            x + radius,
            y,
            w - (radius * 2),
            h,
            color
        )

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
        bg=None
    ) -> None:

        if font is None:

            self._driver.draw_text8x8(
                x,
                y,
                text,
                color,
                bg or 0
            )

            return

        self._driver.draw_text(
            x,
            y,
            text,
            font,
            color,
            bg or 0
        )

    def text_size(
        self,
        text: str,
        font=None
    ) -> tuple:

        if font is None:
            return (
                len(text) * 8,
                8
            )

        width = 0
        height = 0

        for char in text:

            _, w, h = font.get_letter(
                char,
                0xFFFF,
                0x0000
            )

            width += w + 1

            if h > height:
                height = h

        return (
            width,
            height
        )

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
        color=None,
        bg=None
    ) -> None:

        self._driver.draw_sprite(
            bitmap,
            x,
            y,
            w,
            h
        )

    # ------------------------------------------------------------------
    # Clipping
    # ------------------------------------------------------------------

    def set_clip(
        self,
        rect
    ) -> None:

        super().set_clip(rect)

    def clear_clip(self) -> None:

        super().clear_clip()

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Ellipse
    # ------------------------------------------------------------------

    def fill_ellipse(
        self,
        x: int,
        y: int,
        rx: int,
        ry: int,
        color: int
    ) -> None:

        if rx <= 0 or ry <= 0:
            return

        rx2 = rx * rx
        ry2 = ry * ry

        for yy in range(-ry, ry + 1):

            y2 = yy * yy

            try:

                span = int(
                    rx *
                    ((1.0 - (y2 / ry2)) ** 0.5)
                )

            except Exception:

                continue

            self.draw_line(
                x - span,
                y + yy,
                x + span,
                y + yy,
                color
            )


    def draw_ellipse(
        self,
        x: int,
        y: int,
        rx: int,
        ry: int,
        color: int
    ) -> None:

        if rx <= 0 or ry <= 0:
            return

        prev_x = x + rx
        prev_y = y

        for deg in range(1, 361):

            rad = math.radians(deg)

            px = x + int(rx * math.cos(rad))
            py = y + int(ry * math.sin(rad))

            self.draw_line(
                prev_x,
                prev_y,
                px,
                py,
                color
            )

            prev_x = px
            prev_y = py


    # ------------------------------------------------------------------
    # Diamond
    # ------------------------------------------------------------------

    def fill_diamond(
        self,
        x: int,
        y: int,
        radius: int,
        color: int
    ) -> None:

        if radius <= 0:
            return

        for i in range(radius + 1):

            w = radius - i

            self.draw_line(
                x - w,
                y - i,
                x + w,
                y - i,
                color
            )

            if i > 0:

                self.draw_line(
                    x - w,
                    y + i,
                    x + w,
                    y + i,
                    color
                )


    def draw_diamond(
        self,
        cx: int,
        cy: int,
        radius: int,
        color: int
    ) -> None:

        if radius <= 0:
            return

        self.draw_line(
            cx,
            cy - radius,
            cx + radius,
            cy,
            color
        )

        self.draw_line(
            cx + radius,
            cy,
            cx,
            cy + radius,
            color
        )

        self.draw_line(
            cx,
            cy + radius,
            cx - radius,
            cy,
            color
        )

        self.draw_line(
            cx - radius,
            cy,
            cx,
            cy - radius,
            color
        )
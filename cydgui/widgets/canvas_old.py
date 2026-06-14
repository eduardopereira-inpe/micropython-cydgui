"""
cydgui.widgets.canvas
=====================

Generic drawing canvas widget.

Features
--------
- Optional background and border.
- Drawing primitives storage.
- Renderer-agnostic.
- Optional touch handling.
- Supports dynamic drawing updates.
- Suitable as foundation for charts, gauges and custom graphics.

Design goals
------------
- No direct hardware access.
- No global state.
- Compatible with Container/View hierarchy.
- Minimal memory usage for MicroPython.
"""

from cydgui.core.widget import Widget


class Canvas(Widget):
    """Generic drawing canvas."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 100,
        bg: int = 0x0000,
        border_color: int = None,
        touchable: bool = False,
        on_touch=None,
    ) -> None:
        """
        Initialize canvas.

        Args:
            x: Local X coordinate.
            y: Local Y coordinate.
            width: Canvas width.
            height: Canvas height.
            bg: Background color.
            border_color: Optional border color.
            touchable: Enable touch interaction.
            on_touch: Touch callback.
        """

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height
        )

        self._bg = bg
        self._border_color = border_color

        self._touchable = touchable
        self._touch_callback = on_touch

        #
        # Drawing command list
        #
        self._commands = []

    # ------------------------------------------------------------------
    # Drawing API
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Remove all drawing commands."""

        self._commands.clear()

        self.invalidate()

    def draw_pixel(
        self,
        x: int,
        y: int,
        color: int
    ) -> None:
        """Add pixel command."""

        self._commands.append(
            ("pixel", x, y, color)
        )

        self.invalidate()

    def draw_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: int
    ) -> None:
        """Add line command."""

        self._commands.append(
            ("line", x1, y1, x2, y2, color)
        )

        self.invalidate()

    def draw_rect(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: int,
        filled: bool = False
    ) -> None:
        """Add rectangle command."""

        self._commands.append(
            (
                "rect",
                x,
                y,
                width,
                height,
                color,
                filled
            )
        )

        self.invalidate()

    def draw_circle(
        self,
        x: int,
        y: int,
        radius: int,
        color: int,
        filled: bool = False
    ) -> None:
        """Add circle command."""

        self._commands.append(
            (
                "circle",
                x,
                y,
                radius,
                color,
                filled
            )
        )

        self.invalidate()

    def draw_text(
        self,
        x: int,
        y: int,
        text: str,
        color: int = 0xFFFF
    ) -> None:
        """Add text command."""

        self._commands.append(
            (
                "text",
                x,
                y,
                text,
                color
            )
        )

        self.invalidate()

    def draw_arc(
            self,
            cx: int,
            cy: int,
            radius: int,
            start_angle: int,
            end_angle: int,
            color: int,
            step: int = 6
        ) -> None:
            """
            Draw an arc using line segments.

            Args:
                cx: Center X.
                cy: Center Y.
                radius: Arc radius.
                start_angle: Start angle in degrees.
                end_angle: End angle in degrees.
                color: Line color.
                step: Angle increment.
            """

            try:
                from math import sin, cos, radians
            except ImportError:
                return

            previous = None

            angle = start_angle

            while angle <= end_angle:

                x = int(
                    cx +
                    cos(radians(angle)) * radius
                )

                y = int(
                    cy +
                    sin(radians(angle)) * radius
                )

                if previous is not None:

                    self.draw_line(
                        previous[0],
                        previous[1],
                        x,
                        y,
                        color
                    )

                previous = (x, y)

                angle += step

            self.invalidate()

    # ------------------------------------------------------------------
    # Touch
    # ------------------------------------------------------------------

    @property
    def touchable(self) -> bool:
        """Return touch state."""

        return self._touchable

    def set_touchable(
        self,
        value: bool
    ) -> None:
        """Enable or disable touch."""

        self._touchable = value

    def on_touch(
        self,
        event
    ) -> bool:
        """
        Handle touch events.

        Returns:
            True when consumed.
        """

        if not self._touchable:
            return False

        if not self.contains(
            event.x,
            event.y
        ):
            return False

        if callable(
            self._touch_callback
        ):
            self._touch_callback(event)

        return True

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def draw(
        self,
        renderer
    ) -> None:
        """Render canvas."""

        if not self.visible:
            return

        ax = self.absolute_x
        ay = self.absolute_y

        #
        # Background
        #

        renderer.fill_rect(
            ax,
            ay,
            self.width,
            self.height,
            self._bg
        )

        #
        # Border
        #

        if self._border_color is not None:

            renderer.draw_rect(
                ax,
                ay,
                self.width,
                self.height,
                self._border_color
            )

        #
        # Commands
        #

        for cmd in self._commands:

            op = cmd[0]

            # ------------------------------
            # Pixel
            # ------------------------------

            if op == "pixel":

                _, x, y, color = cmd

                renderer.draw_pixel(
                    ax + x,
                    ay + y,
                    color
                )

            # ------------------------------
            # Line
            # ------------------------------

            elif op == "line":

                (
                    _,
                    x1,
                    y1,
                    x2,
                    y2,
                    color
                ) = cmd

                renderer.draw_line(
                    ax + x1,
                    ay + y1,
                    ax + x2,
                    ay + y2,
                    color
                )

            # ------------------------------
            # Rectangle
            # ------------------------------

            elif op == "rect":

                (
                    _,
                    x,
                    y,
                    w,
                    h,
                    color,
                    filled
                ) = cmd

                if filled:

                    renderer.fill_rect(
                        ax + x,
                        ay + y,
                        w,
                        h,
                        color
                    )

                else:

                    renderer.draw_rect(
                        ax + x,
                        ay + y,
                        w,
                        h,
                        color
                    )

            # ------------------------------
            # Circle
            # ------------------------------

            elif op == "circle":

                (
                    _,
                    x,
                    y,
                    radius,
                    color,
                    filled
                ) = cmd

                if filled:

                    renderer.fill_circle(
                        ax + x,
                        ay + y,
                        radius,
                        color
                    )

                else:

                    renderer.draw_circle(
                        ax + x,
                        ay + y,
                        radius,
                        color
                    )

            # ------------------------------
            # Text
            # ------------------------------

            elif op == "text":

                (
                    _,
                    x,
                    y,
                    text,
                    color
                ) = cmd

                renderer.draw_text(
                    ax + x,
                    ay + y,
                    text,
                    color
                )

        self.validate()

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"Canvas("
            f"x={self.x}, "
            f"y={self.y}, "
            f"width={self.width}, "
            f"height={self.height}, "
            f"commands={len(self._commands)})"
        )
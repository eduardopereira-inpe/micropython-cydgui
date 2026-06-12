"""
cydgui.widgets.canvas
=====================

Drawing canvas widget.
"""

from cydgui.core.widget import Widget


class Canvas(Widget):
    """Interactive drawing canvas."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 100,
        color: int = 0xFFFF,
        bg: int = None,
        border_color: int = 0xFFFF,
        border_width: int = 1,
    ) -> None:

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height
        )

        self._color = color

        self._bg = bg

        self._border_color = border_color
        self._border_width = border_width

        self._drawing = False

        self._last_x = 0
        self._last_y = 0

        self._segments = []

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Clear canvas contents."""

        self._segments.clear()

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

        #
        # Background
        #

        if self._bg is not None:

            renderer.fill_rect(
                x,
                y,
                self.width,
                self.height,
                self._bg
            )

        #
        # Border
        #

        if (
            self._border_width > 0 and
            self._border_color is not None
        ):

            for i in range(
                self._border_width
            ):

                renderer.draw_rect(
                    x + i,
                    y + i,
                    self.width - (i * 2),
                    self.height - (i * 2),
                    self._border_color
                )

        #
        # Draw stored segments
        #

        for segment in self._segments:

            x0, y0, x1, y1, color = segment

            renderer.draw_line(
                x0,
                y0,
                x1,
                y1,
                color
            )

        self.validate()

    # ------------------------------------------------------------------
    # Touch
    # ------------------------------------------------------------------

    def on_touch(
        self,
        event
    ) -> bool:

        inside = self.contains(
            event.x,
            event.y
        )

        #
        # Touch down
        #

        if event.is_down:

            if not inside:
                return False

            self._drawing = True

            self._last_x = event.x
            self._last_y = event.y

            return True

        #
        # Touch move
        #

        if event.is_move:

            if not self._drawing:
                return False

            self._segments.append(
                (
                    self._last_x,
                    self._last_y,
                    event.x,
                    event.y,
                    self._color
                )
            )

            self._last_x = event.x
            self._last_y = event.y

            self.invalidate()

            return True

        #
        # Touch up
        #

        if event.is_up:

            if not self._drawing:
                return False

            self._drawing = False

            return True

        return False

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
            f"segments={len(self._segments)})"
        )
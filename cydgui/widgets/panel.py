"""
cydgui.widgets.panel
====================

Container widget with optional background and border.
"""

from cydgui.core.container import Container


class Panel(Container):
    """Visual container widget."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 100,
        bg: int = None,
        border_color: int = None,
        border_width: int = 0,
        radius: int = 0,
    ) -> None:

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height
        )

        self._bg = bg

        self._border_color = border_color
        self._border_width = border_width

        self._radius = radius

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def background(self):
        """Return background color."""
        return self._bg

    @property
    def border_color(self):
        """Return border color."""
        return self._border_color

    @property
    def border_width(self):
        """Return border width."""
        return self._border_width

    @property
    def radius(self):
        """Return corner radius."""
        return self._radius

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def set_background(
        self,
        color: int
    ) -> None:
        """Update background color."""

        if self._bg == color:
            return

        self._bg = color

        self.invalidate()

    def set_border_color(
        self,
        color: int
    ) -> None:
        """Update border color."""

        if self._border_color == color:
            return

        self._border_color = color

        self.invalidate()

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(
        self,
        renderer
    ) -> None:
        """Draw panel and children."""

        if not self.visible:
            return

        x = self.absolute_x
        y = self.absolute_y

        #
        # Background
        #

        if self._bg is not None:

            if self._radius > 0:

                renderer.fill_round_rect(
                    x,
                    y,
                    self.width,
                    self.height,
                    self._radius,
                    self._bg
                )

            else:

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

                if self._radius > 0:

                    renderer.draw_round_rect(
                        x + i,
                        y + i,
                        self.width - (i * 2),
                        self.height - (i * 2),
                        self._radius,
                        self._border_color
                    )

                else:

                    renderer.draw_rect(
                        x + i,
                        y + i,
                        self.width - (i * 2),
                        self.height - (i * 2),
                        self._border_color
                    )

        #
        # Draw children
        #

        for child in self.children:

            child.draw(renderer)

        self.validate()

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def on_touch(
        self,
        event
    ) -> bool:
        """
        Delegate touch handling to Container.
        """

        return super().on_touch(event)

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"Panel("
            f"x={self.x}, "
            f"y={self.y}, "
            f"width={self.width}, "
            f"height={self.height}, "
            f"children={len(self.children)})"
        )
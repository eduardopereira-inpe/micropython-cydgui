"""
cydgui.layouts.column
=====================

Vertical layout container.

Automatically arranges child widgets from top to bottom.
"""

from cydgui.core.container import Container


class Column(Container):
    """Vertical layout container."""

    LEFT = 0
    CENTER = 1
    RIGHT = 2
    STRETCH = 3

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 100,
        spacing: int = 0,
        alignment: int = CENTER,
    ) -> None:

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height
        )

        self._spacing = spacing
        self._alignment = alignment

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _layout_children(self) -> None:
        """Position child widgets."""

        current_y = 0

        for child in self.children:

            new_x = child.x
            new_y = current_y

            if self._alignment == self.LEFT:

                new_x = 0

            elif self._alignment == self.CENTER:

                new_x = (
                    self.width -
                    child.width
                ) // 2

            elif self._alignment == self.RIGHT:

                new_x = (
                    self.width -
                    child.width
                )

            elif self._alignment == self.STRETCH:

                new_x = 0

                if child.width != self.width:
                    child.rect.width = self.width

            #
            # Update only if changed
            #

            if (
                child.rect.x != new_x or
                child.rect.y != new_y
            ):
                child.rect.x = new_x
                child.rect.y = new_y

                child.invalidate()

            current_y += (
                child.height +
                self._spacing
            )

        self.invalidate()

    # ------------------------------------------------------------------
    # Children
    # ------------------------------------------------------------------

    def add(self, widget):

        super().add(widget)

        self._layout_children()

        return widget

    def remove(self, widget):

        super().remove(widget)

        self._layout_children()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def relayout(self) -> None:

        self._layout_children()

    @property
    def spacing(self) -> int:
        return self._spacing

    def set_spacing(
        self,
        value: int
    ) -> None:

        if self._spacing == value:
            return

        self._spacing = value

        self.relayout()

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"Column("
            f"children={len(self.children)}, "
            f"spacing={self._spacing})"
        )
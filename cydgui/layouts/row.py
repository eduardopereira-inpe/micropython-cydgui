"""
cydgui.layouts.row
==================

Horizontal layout container.

Automatically arranges child widgets from left to right.
"""

from cydgui.core.container import Container


class Row(Container):
    """Horizontal layout container."""

    __slots__ = (
        "_spacing",
        "_alignment",
    )

    TOP = 0
    CENTER = 1
    BOTTOM = 2
    STRETCH = 3

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 30,
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

        current_x = 0

        for child in self.iter_children():

            new_x = current_x
            new_y = child.y

            if self._alignment == self.TOP:

                new_y = 0

            elif self._alignment == self.CENTER:

                new_y = (
                    self.height -
                    child.height
                ) // 2

            elif self._alignment == self.BOTTOM:

                new_y = (
                    self.height -
                    child.height
                )

            elif self._alignment == self.STRETCH:

                new_y = 0

                if child.height != self.height:
                    child.rect.height = self.height

            #
            # Update only when needed
            #

            if (
                child.rect.x != new_x or
                child.rect.y != new_y
            ):
                child.rect.x = new_x
                child.rect.y = new_y

                child.invalidate()

            current_x += (
                child.width +
                self._spacing
            )

        self.invalidate()

    # ------------------------------------------------------------------
    # Children
    # ------------------------------------------------------------------

    def add(
        self,
        widget
    ):
        """Add child widget."""

        super().add(widget)

        self._layout_children()

        return widget

    def remove(
        self,
        widget
    ) -> None:
        """Remove child widget."""

        super().remove(widget)

        self._layout_children()

    # ------------------------------------------------------------------
    # Layout control
    # ------------------------------------------------------------------

    def relayout(self) -> None:
        """Force layout update."""

        self._layout_children()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

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
            f"Row("
            f"children={len(self.children)}, "
            f"spacing={self._spacing})"
        )
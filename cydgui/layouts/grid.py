"""
cydgui.layouts.grid
===================

Grid layout container.

Automatically arranges child widgets into rows and columns.
"""

from cydgui.core.container import Container


class Grid(Container):
    """Grid layout container."""

    __slots__ = (
        "_rows",
        "_columns",
        "_spacing",
    )

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 100,
        rows: int = 1,
        columns: int = 1,
        spacing: int = 0,
    ) -> None:
        """
        Initialize grid.

        Args:
            x: Left position.
            y: Top position.
            width: Grid width.
            height: Grid height.
            rows: Number of rows.
            columns: Number of columns.
            spacing: Cell spacing.
        """

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height
        )

        self._rows = max(1, rows)
        self._columns = max(1, columns)
        self._spacing = spacing

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _layout_children(self) -> None:
        """Position child widgets."""

        if not self._children:
            return

        cell_width = (
            self.width -
            ((self._columns - 1) * self._spacing)
        ) // self._columns

        cell_height = (
            self.height -
            ((self._rows - 1) * self._spacing)
        ) // self._rows

        for index, child in enumerate(self._children):

            row = index // self._columns
            column = index % self._columns

            if row >= self._rows:
                break

            child.rect.x = (
                column *
                (cell_width + self._spacing)
            )

            child.rect.y = (
                row *
                (cell_height + self._spacing)
            )

            #
            # Stretch child to cell
            #

            child.rect.width = cell_width
            child.rect.height = cell_height

    # ------------------------------------------------------------------
    # Children management
    # ------------------------------------------------------------------

    def add(
        self,
        widget
    ) -> None:
        """Add child widget."""

        super().add(widget)

        self._layout_children()

        self.invalidate()

    def remove(
        self,
        widget
    ) -> None:
        """Remove child widget."""

        super().remove(widget)

        self._layout_children()

        self.invalidate()

    # ------------------------------------------------------------------
    # Layout control
    # ------------------------------------------------------------------

    def relayout(self) -> None:
        """Force layout recalculation."""

        self._layout_children()

        self.invalidate()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def columns(self) -> int:
        return self._columns

    @property
    def spacing(self) -> int:
        return self._spacing

    def set_rows(
        self,
        value: int
    ) -> None:
        """Update row count."""

        self._rows = max(1, value)

        self.relayout()

    def set_columns(
        self,
        value: int
    ) -> None:
        """Update column count."""

        self._columns = max(1, value)

        self.relayout()

    def set_spacing(
        self,
        value: int
    ) -> None:
        """Update spacing."""

        self._spacing = max(0, value)

        self.relayout()

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"Grid("
            f"rows={self._rows}, "
            f"columns={self._columns}, "
            f"children={len(self.children)})"
        )
"""
cydgui.layouts.grid
===================

Grid layout manager.

``Grid`` is a :class:`~cydgui.core.container.Container` that positions its
children in a fixed-column grid.  Children are placed left-to-right,
top-to-bottom, wrapping to a new row when the column count is reached.

Parameters controlled by ``Grid``
-----------------------------------
- ``columns``  — number of columns in the grid (required).
- ``spacing_x`` — horizontal gap between cells in pixels.
- ``spacing_y`` — vertical gap between rows in pixels.
- ``padding``   — inner margin applied to all four sides of the grid.
- ``cell_width`` — fixed cell width.  Set to 0 to let the grid compute it
  from the container width and column count.
- ``cell_height`` — fixed cell height.  Set to 0 to use the tallest child.

Notes
-----
- Call ``layout()`` after adding/removing children to recalculate positions.
- ``layout()`` is also called automatically by ``add()`` and ``remove()``.
"""

from cydgui.core.container import Container


class Grid(Container):
    """Arranges children in a fixed-column grid.

    Parameters
    ----------
    x, y:
        Top-left position of the grid.
    width:
        Total available width.
    columns:
        Number of columns.
    spacing_x, spacing_y:
        Horizontal and vertical gap between cells.
    padding:
        Inner margin on all four sides.
    cell_width, cell_height:
        Fixed cell dimensions.  Use 0 to let the grid auto-compute them.
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        columns: int = 1,
        spacing_x: int = 0,
        spacing_y: int = 0,
        padding: int = 0,
        cell_width: int = 0,
        cell_height: int = 0,
    ) -> None:
        super().__init__(x=x, y=y, width=width)
        # TODO: store columns, spacing_x, spacing_y, padding, cell_width,
        #       cell_height
        pass

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def layout(self) -> None:
        """Recalculate child positions on the grid.

        TODO: compute cell_width from container width if not specified
        TODO: iterate over children; compute (col, row) index and pixel position
        TODO: update self._rect.height to fit all rows + padding
        TODO: call self.invalidate()
        """
        pass

    # ------------------------------------------------------------------
    # Overrides
    # ------------------------------------------------------------------

    def add(self, widget) -> None:
        """Add *widget* and re-run layout.

        TODO: call super().add(widget)
        TODO: call self.layout()
        """
        pass

    def remove(self, widget) -> None:
        """Remove *widget* and re-run layout.

        TODO: call super().remove(widget)
        TODO: call self.layout()
        """
        pass

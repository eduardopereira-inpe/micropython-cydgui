"""
cydgui.layouts.column
=====================

Vertical layout manager.

``Column`` is a :class:`~cydgui.core.container.Container` that stacks its
children one below the other along the y-axis.  Children keep their own
widths; the column width expands to accommodate the widest child.

Parameters controlled by ``Column``
-------------------------------------
- ``spacing``  — pixels between consecutive children.
- ``padding``  — inner margin applied to all four sides.
- ``align``    — horizontal alignment of narrower children (``"left"``,
  ``"center"``, ``"right"``).

Notes
-----
- Call ``layout()`` after adding/removing children to recalculate positions.
- ``layout()`` is also called automatically by ``add()`` and ``remove()``.
"""

from cydgui.core.container import Container


class Column(Container):
    """Stacks children vertically with optional spacing and padding.

    Parameters
    ----------
    x, y:
        Top-left position of the column.
    height:
        Total available height.  Set to 0 to size the column to fit children.
    spacing:
        Gap in pixels between consecutive children.
    padding:
        Inner margin (applied equally to all four sides).
    align:
        Horizontal alignment: ``"left"``, ``"center"``, or ``"right"``.
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        height: int = 0,
        spacing: int = 0,
        padding: int = 0,
        align: str = "left",
    ) -> None:
        super().__init__(x=x, y=y, height=height)
        # TODO: store spacing, padding, align
        pass

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def layout(self) -> None:
        """Recalculate child positions.

        TODO: iterate over children and compute y offsets considering spacing
        TODO: apply horizontal alignment based on self._align
        TODO: update self._rect.width to fit widest child + 2 * padding
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

"""
cydgui.layouts.row
==================

Horizontal layout manager.

``Row`` is a :class:`~cydgui.core.container.Container` that positions its
children side-by-side along the x-axis.  Children keep their own heights;
the row height expands to accommodate the tallest child.

Parameters controlled by ``Row``
----------------------------------
- ``spacing``  — pixels between consecutive children.
- ``padding``  — inner margin applied to all four sides.
- ``align``    — vertical alignment of shorter children (``"top"``,
  ``"center"``, ``"bottom"``).

Notes
-----
- Call ``layout()`` after adding/removing children to recalculate positions.
- ``layout()`` is also called automatically by ``add()`` and ``remove()``.
"""

from cydgui.core.container import Container


class Row(Container):
    """Arranges children horizontally with optional spacing and padding.

    Parameters
    ----------
    x, y:
        Top-left position of the row.
    width:
        Total available width.  Set to 0 to size the row to fit its children.
    spacing:
        Gap in pixels between consecutive children.
    padding:
        Inner margin (applied equally to all four sides).
    align:
        Vertical alignment: ``"top"``, ``"center"``, or ``"bottom"``.
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        spacing: int = 0,
        padding: int = 0,
        align: str = "top",
    ) -> None:
        super().__init__(x=x, y=y, width=width)
        # TODO: store spacing, padding, align
        pass

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def layout(self) -> None:
        """Recalculate child positions.

        TODO: iterate over children and compute x offsets considering spacing
        TODO: apply vertical alignment based on self._align
        TODO: update self._rect.height to fit tallest child + 2 * padding
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

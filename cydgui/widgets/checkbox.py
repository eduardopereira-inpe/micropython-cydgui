"""
cydgui.widgets.checkbox
=======================

Boolean toggle widget with a check-mark indicator.

A ``CheckBox`` displays a small square box with an optional check mark and an
optional text label to its right.  Tapping the widget toggles its state and
fires the ``on_change`` callback.

Design notes
------------
- State is a simple boolean: ``True`` = checked, ``False`` = unchecked.
- The check-mark is drawn by the renderer (e.g., a diagonal cross or a
  tick-shaped polyline).
- ``on_change`` signature: ``on_change(checkbox, checked: bool) -> None``.
"""

from cydgui.core.widget import Widget


class CheckBox(Widget):
    """A toggleable check-box with an optional label.

    Parameters
    ----------
    x, y:
        Top-left corner.
    text:
        Label text displayed to the right of the box.
    checked:
        Initial checked state.
    on_change:
        Callable ``on_change(checkbox, checked) -> None``.
    box_size:
        Side length of the check box in pixels.
    color:
        Check-mark and border colour (RGB565).  Defaults to theme foreground.
    bg:
        Box fill colour when unchecked (RGB565).  Defaults to theme background.
    check_color:
        Box fill colour when checked (RGB565).  Defaults to theme primary.
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        text: str = "",
        checked: bool = False,
        on_change=None,
        box_size: int = 18,
        color: int = None,
        bg: int = None,
        check_color: int = None,
    ) -> None:
        super().__init__(x=x, y=y)
        # TODO: store text, checked, on_change, box_size, color, bg,
        #       check_color
        # TODO: compute widget width from box_size + text width
        pass

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def set_checked(self, value: bool) -> None:
        """Update checked state and request a redraw.

        TODO: store value, call invalidate()
        """
        pass

    def is_checked(self) -> bool:
        """Return current checked state.

        TODO: return self._checked
        """
        return False

    def toggle(self) -> None:
        """Toggle checked state.

        TODO: call set_checked(not self._checked)
        TODO: fire on_change callback
        """
        pass

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        """Render the checkbox via *renderer*.

        TODO: draw box rectangle (filled with check_color if checked, bg otherwise)
        TODO: draw check mark if checked
        TODO: draw label text to the right
        TODO: clear self._dirty
        """
        pass

    # ------------------------------------------------------------------
    # Input events
    # ------------------------------------------------------------------

    def on_touch(self, event) -> bool:
        """Toggle state on tap.

        TODO: check if tap is within widget bounds
        TODO: call toggle()
        TODO: return True
        """
        return False

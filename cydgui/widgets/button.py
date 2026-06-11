"""
cydgui.widgets.button
=====================

Clickable button widget.

A ``Button`` is an interactive widget that fires a callback when tapped.  It
consists of a filled rounded rectangle (the background) and an optional text
label drawn on top.

Design notes
------------
- The callback is a plain callable: ``on_press(button) -> None``.
- Visual state (normal, pressed, disabled) determines which theme colours are
  used when drawing.
- The button calls ``invalidate()`` on state changes so only the affected area
  is redrawn.
- Touch detection is performed by checking whether the touch coordinates fall
  within ``self.rect``.
"""

from cydgui.core.widget import Widget


class Button(Widget):
    """Tappable button with a label.

    Parameters
    ----------
    x, y:
        Top-left corner of the button.
    width, height:
        Dimensions in pixels.
    text:
        Button label text.
    on_press:
        Callable invoked when the button is tapped: ``on_press(button)``.
    color:
        Text colour (RGB565).  Defaults to theme foreground.
    bg:
        Button background colour (RGB565).  Defaults to theme primary.
    radius:
        Corner radius for the rounded rectangle.
    disabled:
        When True the button ignores touch events.
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 80,
        height: int = 30,
        text: str = "",
        on_press=None,
        color: int = None,
        bg: int = None,
        radius: int = 4,
        disabled: bool = False,
    ) -> None:
        super().__init__(x=x, y=y, width=width, height=height)
        # TODO: store text, on_press, color, bg, radius, disabled
        # TODO: initialise _pressed = False
        pass

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def set_text(self, value: str) -> None:
        """Update label text and invalidate.

        TODO: store value, call invalidate()
        """
        pass

    def set_disabled(self, value: bool) -> None:
        """Enable or disable the button.

        TODO: store value, call invalidate()
        """
        pass

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        """Draw the button background and label via *renderer*.

        TODO: choose colours based on _pressed / disabled state
        TODO: call renderer.fill_round_rect(...)
        TODO: call renderer.draw_text(...) for the label (centred)
        TODO: clear self._dirty
        """
        pass

    # ------------------------------------------------------------------
    # Input events
    # ------------------------------------------------------------------

    def on_touch(self, event) -> bool:
        """Begin press animation and record touch.

        TODO: return False if disabled
        TODO: check event coordinates against self.rect
        TODO: set _pressed = True, call invalidate()
        TODO: return True to consume the event
        """
        return False

    def on_touch_release(self, event) -> bool:
        """Complete the press: fire callback and clear pressed state.

        TODO: set _pressed = False, call invalidate()
        TODO: call self._on_press(self) if callable
        TODO: return True
        """
        return False

"""
cydgui.widgets.switch
=====================

Toggle switch widget (on / off).

A ``Switch`` renders a pill-shaped track with a circular thumb that slides
between two positions to indicate on/off state.  It is functionally equivalent
to :class:`~cydgui.widgets.checkbox.CheckBox` but provides a distinct visual
style more common in modern HMI and mobile UIs.

Design notes
------------
- State is a boolean: ``True`` = on, ``False`` = off.
- The thumb position interpolates between left and right ends of the track.
- ``on_change`` signature: ``on_change(switch, state: bool) -> None``.
- Animation (sliding thumb) is planned for a future release; current skeleton
  snaps immediately.
"""

from cydgui.core.widget import Widget


class Switch(Widget):
    """A sliding on/off toggle control.

    Parameters
    ----------
    x, y:
        Top-left corner.
    state:
        Initial on/off state.
    on_change:
        Callable ``on_change(switch, state) -> None``.
    width, height:
        Overall dimensions of the switch.  The thumb radius is derived from
        the height.
    track_on_color:
        Track fill colour when the switch is ON (RGB565).  Defaults to theme
        primary.
    track_off_color:
        Track fill colour when the switch is OFF (RGB565).  Defaults to theme
        border.
    thumb_color:
        Thumb (knob) fill colour (RGB565).  Defaults to white.
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        state: bool = False,
        on_change=None,
        width: int = 44,
        height: int = 22,
        track_on_color: int = None,
        track_off_color: int = None,
        thumb_color: int = None,
    ) -> None:
        super().__init__(x=x, y=y, width=width, height=height)
        # TODO: store state, on_change, track_on_color, track_off_color,
        #       thumb_color
        pass

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def set_state(self, value: bool) -> None:
        """Update on/off state and request a redraw.

        TODO: store value, call invalidate()
        """
        pass

    def is_on(self) -> bool:
        """Return current state.

        TODO: return self._state
        """
        return False

    def toggle(self) -> None:
        """Toggle current state.

        TODO: call set_state(not self._state)
        TODO: fire on_change callback
        """
        pass

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        """Render the switch track and thumb via *renderer*.

        TODO: draw pill-shaped track using fill_round_rect
        TODO: compute thumb x position based on state
        TODO: draw thumb circle using fill_circle
        TODO: clear self._dirty
        """
        pass

    # ------------------------------------------------------------------
    # Input events
    # ------------------------------------------------------------------

    def on_touch(self, event) -> bool:
        """Toggle state on tap.

        TODO: check tap coordinates against self.rect
        TODO: call toggle()
        TODO: return True
        """
        return False

"""
cydgui.core.events
==================

Simple event dispatcher for touch input.

This module converts raw touch state into high-level TouchEvent
objects and forwards them to the active screen.
"""

from cydgui.core.touch_event import TouchEvent


class EventDispatcher:
    """Converts raw touch input into TouchEvent stream."""

    __slots__ = (
        "_touch",
        "_pressed",
        "_last_x",
        "_last_y",
        "_event",
    )

    def __init__(self, touch_device=None) -> None:
        """
        Args:
            touch_device: Hardware touch driver (XPT2046 or compatible).
        """

        self._touch = touch_device

        self._pressed = False
        self._last_x = 0
        self._last_y = 0
        self._event = TouchEvent(0, 0, TouchEvent.UP)

    # ------------------------------------------------------------------
    # Input polling
    # ------------------------------------------------------------------

    def poll(self):
        """
        Poll touch hardware and return a TouchEvent or None.

        Returns:
            TouchEvent or None
        """

        if self._touch is None:
            return None

        result = self._touch.get_touch()

        if result is not None:

            x, y = result

            self._last_x = x
            self._last_y = y

            if not self._pressed:

                self._pressed = True

                return self._event.set(
                    x,
                    y,
                    TouchEvent.DOWN
                )

            return self._event.set(
                x,
                y,
                TouchEvent.MOVE
            )

        if self._pressed:

            self._pressed = False

            return self._event.set(
                self._last_x,
                self._last_y,
                TouchEvent.UP
            )

        return None

    # ------------------------------------------------------------------
    # Reset state
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Reset internal state."""

        self._pressed = False
        self._last_x = 0
        self._last_y = 0

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"EventDispatcher("
            f"pressed={self._pressed}, "
            f"last_x={self._last_x}, "
            f"last_y={self._last_y})"
        )
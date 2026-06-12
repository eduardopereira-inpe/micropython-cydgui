"""
cydgui.core.touch_event
=======================

Touch event definitions used by the cydgui input system.

Design notes
------------
- Lightweight implementation for MicroPython.
- Represents a normalized touch event.
- Supports press, move and release events.
- Future widgets can implement gestures on top of this model.
"""


class TouchEvent:
    """Represents a touch interaction.

    Attributes:
        x: Touch X coordinate.
        y: Touch Y coordinate.
        event_type: Event type constant.
    """

    DOWN = 1
    MOVE = 2
    UP = 3

    def __init__(
        self,
        x: int,
        y: int,
        event_type: int
    ) -> None:
        """Initialize a touch event.

        Args:
            x: Touch X coordinate.
            y: Touch Y coordinate.
            event_type: One of DOWN, MOVE or UP.
        """

        self.x = x
        self.y = y
        self.event_type = event_type

    @property
    def is_down(self) -> bool:
        """Return True when this is a touch down event."""
        return self.event_type == self.DOWN

    @property
    def is_move(self) -> bool:
        """Return True when this is a touch move event."""
        return self.event_type == self.MOVE

    @property
    def is_up(self) -> bool:
        """Return True when this is a touch release event."""
        return self.event_type == self.UP

    def __repr__(self) -> str:
        """Return a debug representation."""

        names = {
            self.DOWN: "DOWN",
            self.MOVE: "MOVE",
            self.UP: "UP"
        }

        return (
            "TouchEvent("
            f"x={self.x}, "
            f"y={self.y}, "
            f"type={names.get(self.event_type, 'UNKNOWN')}"
            ")"
        )

    def __eq__(self, other) -> bool:
        """Compare two touch events."""

        if not isinstance(other, TouchEvent):
            return False

        return (
            self.x == other.x and
            self.y == other.y and
            self.event_type == other.event_type
        )
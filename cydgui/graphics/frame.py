"""
cydgui.graphics.frame
=====================

Sprite frame definition.

A Frame represents a single image inside a SpriteSheet.

The class is intentionally lightweight and immutable after creation.
Besides the frame index, it optionally stores metadata that can be used
by future versions of the framework, such as custom frame duration,
anchor point, collision box, or user-defined data.

The renderer only needs the frame index. All remaining fields are
optional and ignored unless explicitly used by higher-level systems.

Example:
    frame = Frame(5)

    frame.index
    # 5

    frame = Frame(
        index=3,
        duration=120,
        anchor_x=16,
        anchor_y=28
    )
"""


class Frame:
    """Represents a single frame of a sprite animation.

    Args:
        index: Frame index inside the sprite sheet.
        duration: Optional frame duration in milliseconds.
            When None, the animation FPS controls timing.
        anchor_x: Optional horizontal anchor.
        anchor_y: Optional vertical anchor.
        data: Optional user metadata.
    """

    __slots__ = (
        "_index",
        "_duration",
        "_anchor_x",
        "_anchor_y",
        "_data",
    )

    def __init__(
        self,
        index,
        duration=None,
        anchor_x=0,
        anchor_y=0,
        data=None,
    ):
        """Initialize a frame."""

        self._index = int(index)
        self._duration = duration
        self._anchor_x = int(anchor_x)
        self._anchor_y = int(anchor_y)
        self._data = data

    @property
    def index(self):
        """Return the sprite sheet frame index."""
        return self._index

    @property
    def duration(self):
        """Return the custom frame duration.

        Returns:
            int | None: Duration in milliseconds or None.
        """
        return self._duration

    @property
    def anchor_x(self):
        """Return the horizontal anchor."""
        return self._anchor_x

    @property
    def anchor_y(self):
        """Return the vertical anchor."""
        return self._anchor_y

    @property
    def data(self):
        """Return optional user metadata."""
        return self._data

    def has_custom_duration(self):
        """Return whether this frame overrides animation timing.

        Returns:
            bool: True when a custom duration is defined.
        """
        return self._duration is not None

    def __repr__(self):
        """Return a developer-friendly representation."""
        return (
            "Frame(index={}, duration={}, anchor=({}, {}))".format(
                self._index,
                self._duration,
                self._anchor_x,
                self._anchor_y,
            )
        )
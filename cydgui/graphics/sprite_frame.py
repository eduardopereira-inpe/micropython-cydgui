"""
cydgui.graphics.sprite_frame
============================

Loaded sprite frame.

A SpriteFrame represents decoded image data loaded from a SpriteSheet.

It stores the RGB565 buffer together with its dimensions.

This object is immutable after creation and is intended to be shared
between sprites when frame caching is enabled.
"""


class SpriteFrame:
    """Represents a loaded sprite frame."""

    __slots__ = (
        "_index",
        "_buffer",
        "_width",
        "_height",
    )

    def __init__(self, index, buffer, width, height):
        """Initialize a loaded frame.

        Args:
            index: Frame index.
            buffer: RGB565 byte buffer.
            width: Frame width.
            height: Frame height.
        """

        self._index = index
        self._buffer = buffer
        self._width = width
        self._height = height

    @property
    def index(self):
        """Return frame index."""
        return self._index

    @property
    def buffer(self):
        """Return RGB565 buffer."""
        return self._buffer

    @property
    def width(self):
        """Return frame width."""
        return self._width

    @property
    def height(self):
        """Return frame height."""
        return self._height

    @property
    def size(self):
        """Return (width, height)."""
        return (
            self._width,
            self._height,
        )

    def __len__(self):
        """Return buffer size in bytes."""
        return len(self._buffer)

    def __repr__(self):
        """Return developer representation."""
        return (
            "SpriteFrame(index={}, {}x{})".format(
                self._index,
                self._width,
                self._height,
            )
        )
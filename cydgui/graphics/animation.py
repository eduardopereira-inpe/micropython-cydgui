"""
cydgui.graphics.animation
=========================

Animation definition.

An Animation is an immutable description of a sequence of frames
and how they should be played.

It contains no rendering logic and no knowledge of SpriteSheet.

Responsibilities:
    - Store frame indices or Frame objects.
    - Define playback speed (fps).
    - Define playback mode (loop, once, ping-pong, etc).
"""

from cydgui.graphics.animation_mode import AnimationMode


class Animation:
    """Animation definition."""

    __slots__ = (
        "_name",
        "_frames",
        "_fps",
        "_mode",
    )

    def __init__(
        self,
        name,
        frames,
        fps=8,
        mode=AnimationMode.LOOP,
    ):
        """Initialize animation.

        Args:
            name (str): Animation identifier.
            frames (iterable): Sequence of frame indices.
            fps (int): Frames per second.
            mode (AnimationMode): Playback mode.
        """

        self._name = name
        self._fps = max(1, int(fps))
        self._mode = mode

        # Store only integer indices (lightweight for MicroPython)
        self._frames = [int(f) for f in frames]

    #################################################################
    # Properties
    #################################################################

    @property
    def name(self):
        """Return animation name."""
        return self._name

    @property
    def fps(self):
        """Return frames per second."""
        return self._fps

    @property
    def mode(self):
        """Return playback mode."""
        return self._mode

    #################################################################
    # Frame access
    #################################################################

    def frame(self, index):
        """Return frame index at position.

        Args:
            index (int): Position in animation sequence.

        Returns:
            int: SpriteSheet frame index.
        """
        return self._frames[index]

    def __len__(self):
        """Return number of frames."""
        return len(self._frames)

    #################################################################
    # Helpers
    #################################################################

    @classmethod
    def range(
        cls,
        name,
        first,
        last,
        fps=8,
        mode=AnimationMode.LOOP,
    ):
        """Create animation from a range of indices."""

        return cls(
            name=name,
            frames=range(first, last + 1),
            fps=fps,
            mode=mode,
        )

    @classmethod
    def row(
        cls,
        sheet,
        name,
        row,
        start=0,
        count=None,
        fps=8,
        mode=AnimationMode.LOOP,
    ):
        """Create animation from a SpriteSheet row.

        Args:
            sheet: SpriteSheet instance.
            name: Animation name.
            row: Row index in sprite sheet.
            start: Starting column.
            count: Number of frames (None = full row).
            fps: Playback speed.
            mode: Playback mode.

        Returns:
            Animation
        """

        frames = sheet.row(
            row=row,
            start=start,
            count=count,
        )

        return cls(
            name=name,
            frames=frames,
            fps=fps,
            mode=mode,
        )
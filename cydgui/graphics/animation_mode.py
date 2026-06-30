"""
cydgui.graphics.animation_mode
==============================

Animation playback mode definitions.

This module provides lightweight integer constants describing how an
animation should advance. The values are intentionally simple to minimize
memory usage and execution cost on MicroPython targets.

The animator is responsible for interpreting these modes.

Example:
    from cydgui.graphics.animation_mode import AnimationMode

    mode = AnimationMode.LOOP
"""


class AnimationMode:
    """Animation playback modes.

    Attributes:
        HOLD: Display the current frame indefinitely.
        LOOP: Restart from the first frame after the last frame.
        ONCE: Play once and stop on the last frame.
        PING_PONG: Play forward then backward repeatedly.
        RANDOM: Randomly select the next frame.
        TRIGGER: Wait for an external trigger before advancing.
    """

    HOLD = 0
    LOOP = 1
    ONCE = 2
    PING_PONG = 3
    RANDOM = 4
    TRIGGER = 5

    @classmethod
    def is_valid(cls, mode):
        """Return whether the given mode is valid.

        Args:
            mode: Animation mode value.

        Returns:
            bool: True if the mode is supported.
        """
        return 0 <= mode <= 5

    @classmethod
    def name(cls, mode):
        """Return the symbolic name of a mode.

        Args:
            mode: Animation mode value.

        Returns:
            str: Mode name. Returns "UNKNOWN" for invalid values.
        """
        if mode == cls.HOLD:
            return "HOLD"

        if mode == cls.LOOP:
            return "LOOP"

        if mode == cls.ONCE:
            return "ONCE"

        if mode == cls.PING_PONG:
            return "PING_PONG"

        if mode == cls.RANDOM:
            return "RANDOM"

        if mode == cls.TRIGGER:
            return "TRIGGER"

        return "UNKNOWN"
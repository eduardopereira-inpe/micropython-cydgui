"""
cydgui.graphics.animator
========================

Animation playback controller.

The Animator is responsible only for:
    - Advancing animation frames over time.
    - Respecting AnimationMode rules.
    - Exposing the current logical frame.

It does NOT:
    - Render anything
    - Know about SpriteSheet
    - Know about SpriteAtlas
    - Perform any I/O

Time is driven externally via ticks_ms().
"""

from time import ticks_diff

from cydgui.graphics.animation_mode import AnimationMode


class Animator:
    """Controls animation playback."""

    __slots__ = (
        "_animation",
        "_frame",
        "_last_time",
        "_direction",
        "_playing",
        "_finished",
    )

    def __init__(self, animation=None):
        """Initialize Animator.

        Args:
            animation (Animation | None): Optional initial animation.
        """

        self._animation = None

        self._frame = 0

        self._last_time = None

        self._direction = 1

        self._playing = False

        self._finished = False

        if animation is not None:
            self.play(animation)

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def animation(self):
        """Current animation."""
        return self._animation

    @property
    def frame_index(self):
        """Current frame index."""
        return self._frame

    @property
    def frame(self):
        """Return current Frame object from animation."""

        if self._animation is None:
            return None

        return self._animation.frame(self._frame)

    @property
    def playing(self):
        """Whether animation is playing."""
        return self._playing

    @property
    def finished(self):
        """Whether animation finished (only ONCE mode)."""
        return self._finished

    @property
    def is_last_frame(self):
        """True if current frame is last frame."""
        if self._animation is None:
            return False

        return self._frame == (len(self._animation) - 1)

    # ---------------------------------------------------------
    # Playback control
    # ---------------------------------------------------------

    def play(self, animation):
        """Start playing an animation.

        Args:
            animation (Animation): Animation to play.
        """

        self._animation = animation
        self.restart()

    def restart(self):
        """Restart current animation."""

        if self._animation is None:
            return

        self._frame = 0
        self._direction = 1
        self._last_time = None
        self._playing = True
        self._finished = False

    def stop(self):
        """Stop animation playback."""
        self._playing = False

    # ---------------------------------------------------------
    # Update loop
    # ---------------------------------------------------------

    def update(self, now):
        """Advance animation based on time.

        Args:
            now (int): ticks_ms() current time.
        """

        if not self._playing or self._animation is None:
            return

        if self._last_time is None:
            self._last_time = now
            return

        current_frame = self.frame

        # frame-based duration override
        if hasattr(current_frame, "duration") and hasattr(current_frame, "has_custom_duration"):
            if current_frame.has_custom_duration():
                interval = current_frame.duration
            else:
                interval = 1000 // self._animation.fps
        else:
            interval = 1000 // self._animation.fps

        if ticks_diff(now, self._last_time) < interval:
            return

        self._last_time = now
        self._advance()

    # ---------------------------------------------------------
    # Internal logic
    # ---------------------------------------------------------

    def _advance(self):
        """Advance frame based on animation mode."""

        mode = self._animation.mode

        if mode == AnimationMode.HOLD:
            return

        if mode == AnimationMode.LOOP:
            self._advance_loop()
            return

        if mode == AnimationMode.ONCE:
            self._advance_once()
            return

        if mode == AnimationMode.PING_PONG:
            self._advance_ping_pong()
            return

        # Future modes
        if mode == AnimationMode.RANDOM:
            return

        if mode == AnimationMode.TRIGGER:
            return

    # ---------------------------------------------------------
    # Mode implementations
    # ---------------------------------------------------------

    def _advance_loop(self):
        self._frame += 1

        if self._frame >= len(self._animation):
            self._frame = 0

    def _advance_once(self):
        if self._frame < (len(self._animation) - 1):
            self._frame += 1
            return

        self._finished = True
        self._playing = False

    def _advance_ping_pong(self):
        self._frame += self._direction

        if self._frame >= len(self._animation):
            self._frame = len(self._animation) - 2
            self._direction = -1
            return

        if self._frame < 0:
            self._frame = 1
            self._direction = 1
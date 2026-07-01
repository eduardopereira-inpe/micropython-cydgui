"""
cydgui.graphics.sprite
======================

Sprite model.

A Sprite combines:
    - SpriteSheet (pixel data)
    - SpriteAtlas (animation definitions)
    - Animator (time control)

Responsibilities:
    - Hold position and visual state.
    - Resolve animation from atlas.
    - Update animation over time.
    - Provide current SpriteFrame for rendering.

The Sprite performs no rendering.
"""

from cydgui.graphics.animator import Animator


class Sprite:
    """Animated sprite."""

    __slots__ = (
        "_sheet",
        "_atlas",
        "_animator",
        "_frame",
        "_x",
        "_y",
        "_vx",
        "_vy",
        "_dx",
        "_dy",
        "_enabled",
        "_opaque",
        "_flip_x",
        "_flip_y",
    )

    def __init__(
        self,
        sheet,
        atlas,
        x=0,
        y=0,
        opaque=True,
    ):
        """Initialize sprite.

        Args:
            sheet: SpriteSheet instance.
            atlas: SpriteAtlas instance.
            x: Initial X position.
            y: Initial Y position.
            opaque: Whether sprite fully covers its bounds.
        """

        self._sheet = sheet
        self._atlas = atlas

        self._animator = Animator()

        self._frame = None

        self._x = int(x)
        self._y = int(y)

        self._enabled = True
        self._opaque = bool(opaque)

        self._flip_x = False
        self._flip_y = False
        self._vx = 0.0
        self._vy = 0.0

        # Movement resolution (pixels)
        self._dx = 1.0
        self._dy = 1.0

    # ---------------------------------------------------------
    # Position
    # ---------------------------------------------------------

    @property
    def x(self):
        return int(self._x)

    @x.setter
    def x(self, value):
        self._x = int(value)

    @property
    def y(self):
        return int(self._y)

    @y.setter
    def y(self, value):
        self._y = int(value)

    @property
    def position(self):
        return (self._x, self._y)
    
    @property
    def vx(self):
        return self._vx


    @property
    def vy(self):
        return self._vy
    
    def set_velocity(self, vx=0.0, vy=0.0):
        """Set sprite velocity."""

        self._vx = float(vx)
        self._vy = float(vy)
        
    def stop_motion(self):
        """Stop sprite movement."""

        self._vx = 0.0
        self._vy = 0.0
        
    def reverse_x(self):
        self._vx = -self._vx
        
    def reverse_y(self):
        self._vy = -self._vy

    def move_to(self, x, y):
        self._x = int(x)
        self._y = int(y)

    def move_by(self, dx, dy):
        self._x += int(dx)
        self._y += int(dy)

    # ---------------------------------------------------------
    # Frame
    # ---------------------------------------------------------

    @property
    def frame(self):
        """Return current SpriteFrame."""
        return self._frame

    # ---------------------------------------------------------
    # State
    # ---------------------------------------------------------

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = bool(value)

    @property
    def opaque(self):
        return self._opaque

    @opaque.setter
    def opaque(self, value):
        self._opaque = bool(value)

    # ---------------------------------------------------------
    # Flip
    # ---------------------------------------------------------

    @property
    def flip_x(self):
        """Return horizontal flip state."""
        return self._flip_x


    @property
    def flip_y(self):
        """Return vertical flip state."""
        return self._flip_y


    def set_flip(
        self,
        horizontal=False,
        vertical=False,
    ):
        """Set sprite mirroring.

        Args:
            horizontal: Mirror horizontally.
            vertical: Mirror vertically.
        """

        horizontal = bool(horizontal)
        vertical = bool(vertical)

        if (
            horizontal == self._flip_x and
            vertical == self._flip_y
        ):
            return

        self._flip_x = horizontal
        self._flip_y = vertical

        self._update_frame()


    def reset_flip(self):
        """Restore original orientation."""

        self.set_flip(False, False)
    # ---------------------------------------------------------
    # Animation control
    # ---------------------------------------------------------

    def play(self, name):
        """Play animation by name."""

        animation = self._atlas.animation(name)

        if animation is None:
            raise ValueError(
                "Unknown animation '{}'".format(name)
            )

        self._animator.play(animation)

        self._update_frame()

    def stop(self):
        """Stop animation."""
        self._animator.stop()

    def restart(self):
        """Restart animation."""
        self._animator.restart()
        self._update_frame()

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------

    def update(self, now):
        """Update animation state.

        Args:
            now: ticks_ms()
        """

        self._animator.update(now)
        self._update_frame()

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    def _update_frame(self):
        """Resolve current SpriteFrame."""
        
        
        self._x += self._vx * self._dx
        self._y += self._vy * self._dx

        animation = self._animator.animation

        if animation is None:
            self._frame = None
            return

        frame = self._animator.frame

        if frame is None:
            self._frame = None
            return

        self._frame = self._sheet.get_frame(
            frame,
            flip_x=self._flip_x,
            flip_y=self._flip_y,
        )

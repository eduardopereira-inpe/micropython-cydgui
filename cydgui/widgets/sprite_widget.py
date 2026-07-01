"""
cydgui.widgets.sprite_widget
============================

Sprite widget.

A SpriteWidget integrates a graphics.Sprite into the CYDGUI
widget system.

Responsibilities
----------------
- Hold a Sprite instance.
- Delegate position to the Sprite.
- Update sprite animation.
- Render the current frame.

The widget contains no animation logic and does not manipulate
Sprite internals.
"""

from time import ticks_ms

from cydgui.core.widget import Widget


class SpriteWidget(Widget):
    """Widget that displays a Sprite."""

    __slots__ = (
        "_sprite",
    )

    def __init__(
        self,
        sprite,
        x=None,
        y=None,
        width=None,
        height=None,
        **kwargs
    ):
        """Initialize the widget.

        Args:
            sprite:
                Sprite instance.

            x:
                Optional initial X position.

            y:
                Optional initial Y position.

            width:
                Optional widget width.

            height:
                Optional widget height.
        """

        self._sprite = sprite

        if x is not None:
            sprite.x = x

        if y is not None:
            sprite.y = y

        if width is None:
            width = sprite.frame.width if sprite.frame else sprite.sheet.frame_width

        if height is None:
            height = sprite.frame.height if sprite.frame else sprite.sheet.frame_height

        super().__init__(
            x=sprite.x,
            y=sprite.y,
            width=width,
            height=height,
            **kwargs
        )

    #################################################################
    # Sprite
    #################################################################

    @property
    def sprite(self):
        """Return the wrapped sprite."""
        return self._sprite

    #################################################################
    # Position (delegated to Sprite)
    #################################################################

    @property
    def x(self):
        """Return sprite X position."""
        return self._sprite.x

    @x.setter
    def x(self, value):
        self._sprite.x = int(value)

    @property
    def y(self):
        """Return sprite Y position."""
        return self._sprite.y

    @y.setter
    def y(self, value):
        self._sprite.y = int(value)

    @property
    def position(self):
        """Return sprite position."""
        return self._sprite.position

    def move_to(self, x, y):
        """Move the sprite."""
        self._sprite.move_to(x, y)

    def move_by(self, dx, dy):
        """Move the sprite by an offset."""
        self._sprite.move_by(dx, dy)

    #################################################################
    # Animation shortcuts
    #################################################################

    def play(self, name):
        """Play an animation."""
        self._sprite.play(name)

    def stop(self):
        """Stop animation."""
        self._sprite.stop()

    def restart(self):
        """Restart animation."""
        self._sprite.restart()

    #################################################################
    # Flip shortcuts
    #################################################################

    def set_flip(
        self,
        horizontal=False,
        vertical=False,
    ):
        """Mirror the sprite."""
        self._sprite.set_flip(
            horizontal=horizontal,
            vertical=vertical,
        )

    #################################################################
    # Widget lifecycle
    #################################################################

    def update(self):
        """Update sprite animation."""

        if not self.visible:
            return

        if not self.enabled:
            return

        self._sprite.update(
            ticks_ms()
        )

    #################################################################
    # Rendering
    #################################################################

    def draw(self, renderer):
        """Render the current frame."""

        if not self.visible:
            return

        frame = self._sprite.frame

        if frame is None:
            return

        renderer.draw_sprite(
            frame.buffer,
            self._sprite.x,
            self._sprite.y,
            frame.width,
            frame.height,
        )
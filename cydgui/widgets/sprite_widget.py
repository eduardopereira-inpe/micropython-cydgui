"""
cydgui.widgets.sprite_widget
============================

Sprite widget.

A SpriteWidget integrates a graphics.Sprite into the CYDGUI
widget system.

Responsibilities
----------------
- Hold a Sprite instance.
- Render the current sprite frame.
- Update sprite animation.
- Execute an optional behavior callback.

The widget contains no animation logic. Behaviors can be
attached dynamically using ``set_behavior()``.
"""

from time import ticks_ms

from cydgui.core.widget import Widget
import uasyncio as asyncio


class SpriteWidget(Widget):
    """Widget that displays a Sprite."""

    __slots__ = (
        "_sprite",
        "_camera_x",
        "_camera_y",
        "_behavior",
        "state",
        "touch",
    )

    def __init__(
        self,
        sprite,
        x=0,
        y=0,
        width=None,
        height=None,
        camera_x=0,
        camera_y=0,
        behavior=None,
        touch=None,
        **kwargs
    ):
        """Initialize the widget.

        Args:
            sprite:
                Sprite instance.

            x:
                Viewport X.

            y:
                Viewport Y.

            width:
                Viewport width.

            height:
                Viewport height.

            camera_x:
                Camera X position.

            camera_y:
                Camera Y position.

            behavior:
                Optional behavior callback.

            touch:
                Optional touch device passed to the behavior.
        """

        self._sprite = sprite

        self._camera_x = int(camera_x)
        self._camera_y = int(camera_y)

        self._behavior = behavior

        #
        # Public runtime state used by behaviors.
        #

        self.state = {}

        #
        # Optional touch device.
        #

        self.touch = touch

        if width is None:
            width = (
                sprite.frame.width
                if sprite.frame
                else sprite.sheet.frame_width
            )

        if height is None:
            height = (
                sprite.frame.height
                if sprite.frame
                else sprite.sheet.frame_height
            )

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            **kwargs
        )

    #################################################################
    # Sprite
    #################################################################

    @property
    def sprite(self):
        """Return sprite."""
        return self._sprite

    #################################################################
    # Camera
    #################################################################

    @property
    def camera_x(self):
        """Return camera X."""
        return self._camera_x

    @camera_x.setter
    def camera_x(self, value):
        self._camera_x = int(value)

    @property
    def camera_y(self):
        """Return camera Y."""
        return self._camera_y

    @camera_y.setter
    def camera_y(self, value):
        self._camera_y = int(value)

    @property
    def camera(self):
        """Return camera position."""
        return (
            self._camera_x,
            self._camera_y,
        )

    def set_camera(self, x, y):
        """Set camera position."""

        self._camera_x = int(x)
        self._camera_y = int(y)

    def move_camera(self, dx, dy):
        """Move camera."""

        self._camera_x += int(dx)
        self._camera_y += int(dy)

    #################################################################
    # Behavior
    #################################################################

    @property
    def behavior(self):
        """Return current behavior."""
        return self._behavior

    def set_behavior(self, callback):
        """Attach a behavior callback.

        Args:
            callback:
                Callable receiving this widget.
        """

        self._behavior = callback

    #################################################################
    # Animation shortcuts
    #################################################################

    def play(self, name):
        """Play animation."""
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
        """Mirror sprite."""

        self._sprite.set_flip(
            horizontal=horizontal,
            vertical=vertical,
        )

    #################################################################
    # Update
    #################################################################

    def update(self):
        """Update sprite."""

        if not self.visible:
            return

        if not self.enabled:
            return

        self._sprite.update(
            ticks_ms()
        )

        if self._behavior is not None:
            self._behavior(self)
            
            
    async def start(self):

        while True:

            self.update()

            await asyncio.sleep_ms(16)

    #################################################################
    # Draw
    #################################################################

    def draw(self, renderer):
        """Render sprite inside the viewport."""

        if not self.visible:
            return

        frame = self._sprite.frame

        if frame is None:
            return

        screen_x = (
            self.x +
            self._sprite.x -
            self._camera_x
        )

        screen_y = (
            self.y +
            self._sprite.y -
            self._camera_y
        )

        #
        # Quick rejection.
        #

        if (
            screen_x + frame.width <= self.x or
            screen_y + frame.height <= self.y or
            screen_x >= self.x + self.width or
            screen_y >= self.y + self.height
        ):
            return

        renderer.driver.draw_sprite(
            frame.buffer,
            screen_x,
            screen_y,
            frame.width,
            frame.height,
        )
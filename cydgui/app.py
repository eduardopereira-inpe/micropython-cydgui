"""
cydgui.app
==========

Core application object.

The App is responsible for:

- Holding the active screen.
- Polling the touch driver.
- Generating TouchEvent instances.
- Rendering dirty screens.
- Running the async event loop.

This implementation is intentionally lightweight and suitable
for MicroPython devices such as the Cheap Yellow Display (CYD).
"""

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


from cydgui.core.touch_event import TouchEvent


class App:
    """Main application object."""

    def __init__(
        self,
        renderer,
        screen,
        touch=None,
        frame_delay_ms: int = 16
    ) -> None:
        """
        Initialize application.

        Args:
            renderer: Renderer instance.
            touch: Optional touch driver.
            frame_delay_ms: Frame delay in milliseconds.
        """

        self._renderer = renderer
        self._touch = touch

        

        self._frame_delay_ms = frame_delay_ms

        self._screen = None

        self._running = False

        self._pressed = False

        self._last_x = 0
        self._last_y = 0
        
        self.set_screen(screen=screen)

    # ------------------------------------------------------------------
    # Screen management
    # ------------------------------------------------------------------

    @property
    def screen(self):
        """Return active screen."""

        return self._screen

    def set_screen(
        self,
        screen
    ) -> None:
        """
        Set active screen.

        Args:
            screen: Screen instance.
        """

        if self._screen is screen:
            return

        if self._screen:
            self._screen.on_leave()

        self._screen = screen

        if self._screen:
            self._screen.on_enter()

    # ------------------------------------------------------------------
    # Touch processing
    # ------------------------------------------------------------------

    def _poll_touch(self):
        """
        Poll touch driver and generate TouchEvent.

        Returns:
            TouchEvent or None.
        """

        if self._touch is None:
            return None

        touch = self._touch.get_touch()

        if touch is not None:

            x, y = touch

            self._last_x = x
            self._last_y = y

            if not self._pressed:

                self._pressed = True

                return TouchEvent(
                    x=x,
                    y=y,
                    event_type=TouchEvent.DOWN
                )

            return TouchEvent(
                x=x,
                y=y,
                event_type=TouchEvent.MOVE
            )

        if self._pressed:

            self._pressed = False

            return TouchEvent(
                x=self._last_x,
                y=self._last_y,
                event_type=TouchEvent.UP
            )

        return None

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _render(self) -> None:
        """Render active screen."""

        if self._screen is None:
            return

        if not self._screen.dirty:
            return

        self._screen.draw(
            self._renderer
        )

        self._renderer.flush()

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    async def _run_async(self) -> None:
        """Async application loop."""

        self._running = True

        while self._running:

            event = self._poll_touch()

            if (
                event is not None and
                self._screen is not None
            ):
                self._screen.dispatch_touch(
                    event
                )

            self._render()

            try:
                await asyncio.sleep_ms(
                    self._frame_delay_ms
                )
            except AttributeError:
                await asyncio.sleep(
                    self._frame_delay_ms / 1000
                )

    # ------------------------------------------------------------------
    # Control
    # ------------------------------------------------------------------

    def stop(self) -> None:
        """Stop application loop."""

        self._running = False

    def run(self) -> None:
        """Run application."""

        asyncio.run(
            self._run_async()
        )

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"App("
            f"screen={self._screen}, "
            f"running={self._running})"
        )
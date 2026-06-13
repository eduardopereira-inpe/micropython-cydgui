"""
cydgui.app
==========

Core application object.

Responsibilities
----------------
- Hold renderer and touch driver references.
- Manage screen navigation.
- Poll touch events.
- Generate TouchEvent objects.
- Render dirty screens.
- Run the async application loop.

Designed for MicroPython and the Cheap Yellow Display.
"""

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


from cydgui.core.touch_event import TouchEvent
from cydgui.core.navigation import Navigation


class App:
    """Main application object."""

    def __init__(
        self,
        renderer,
        touch=None,
        screen=None,
        frame_delay_ms: int = 16
    ) -> None:
        """
        Initialize application.

        Args:
            renderer: Renderer instance.
            touch: Optional touch driver.
            screen: Optional initial screen.
            frame_delay_ms: Main loop delay.
        """

        self._renderer = renderer
        self._touch = touch

        self._frame_delay_ms = frame_delay_ms

        self._navigation = Navigation()

        self._running = False

        self._pressed = False

        self._last_x = 0
        self._last_y = 0
        
        self._routes = {}

        if screen is not None:
            self.set_screen(screen)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    @property
    def screen(self):
        """Return current active screen."""

        return self._navigation.current

    def set_screen(
        self,
        screen
    ) -> None:
        """
        Replace current screen.

        Args:
            screen: Screen instance.
        """

        self._navigation.clear()

        if screen is not None:

            screen.app = self

            self._navigation.push(screen)

    def push(
        self,
        screen
    ) -> None:
        """
        Push a screen onto the navigation stack.

        Args:
            screen: Screen instance.
        """

        if screen is None:
            return

        screen.app = self

        self._navigation.push(screen)

    def pop(self):
        """
        Pop current screen.

        Returns:
            Removed screen.
        """

        return self._navigation.pop()

    @property
    def navigation(self):
        """Return navigation manager."""

        return self._navigation

    # ------------------------------------------------------------------
    # Touch processing
    # ------------------------------------------------------------------

    def _poll_touch(self):
        """
        Poll touch driver.

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

        screen = self.screen

        if screen is None:
            return

        if not screen.dirty:
            return

        screen.draw(
            self._renderer
        )

        self._renderer.flush()

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    async def _run_async(self) -> None:
        """Application async loop."""

        self._running = True

        while self._running:

            event = self._poll_touch()

            screen = self.screen

            if (
                event is not None and
                screen is not None
            ):
                screen.dispatch_touch(event)

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
        """Stop application."""

        self._running = False

    def run(self) -> None:
        """Start application."""

        asyncio.run(
            self._run_async()
        )
        
    def route(
        self,
        name,
        view_class
    ):
        self._routes[name] = view_class
        
    def navigate(
        self,
        name, 
        parameters: dict | None = None
    ):

        view_class = self._routes[name]

        self.set_screen(
            view_class(self, parameters=parameters)
        )

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"App("
            f"screen={self.screen}, "
            f"running={self._running})"
        )
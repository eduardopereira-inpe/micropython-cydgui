"""
cydgui.app
==========

Core application object (hardened version for ESP32 MicroPython).

Improvements:
-------------
- Safer asyncio task lifecycle management
- Reduced task leakage on navigation
- Better screen transition cleanup
- Yield after cancel to allow uasyncio release
- More deterministic memory behavior
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
        frame_delay_ms: int = 5
    ) -> None:

        self._renderer = renderer
        self._touch = touch
        self._frame_delay_ms = frame_delay_ms

        self._navigation = Navigation()

        self._running = False
        self._pressed = False

        self._last_x = 0
        self._last_y = 0

        self._routes = {}

        # managed async tasks
        self._tasks = set()

        if screen is not None:
            self.set_screen(screen)

    # ---------------------------------------------------------
    # Task management
    # ---------------------------------------------------------

    def create_task(self, coro):
        """Register a managed asyncio task."""

        task = asyncio.create_task(coro)
        self._tasks.add(task)
        return task

    def _cleanup_tasks(self):
        """Remove finished tasks safely."""

        # evita mutação durante iteração indireta
        alive = set()

        for t in self._tasks:
            if t.done():
                continue
            alive.add(t)

        self._tasks = alive

    def _cancel_all_tasks(self):
        """Cancel all running tasks safely."""

        if not self._tasks:
            return

        tasks = list(self._tasks)
        self._tasks.clear()

        for task in tasks:
            try:
                task.cancel()
            except:
                pass

        # IMPORTANT: yield to uasyncio so cancellation propagates
        try:
            asyncio.sleep_ms(0)
        except:
            pass

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    @property
    def screen(self):
        return self._navigation.current

    def set_screen(self, screen) -> None:
        """Replace current screen safely."""

        # IMPORTANT: ensure previous screen is released if needed
        if self._navigation.current:
            old = self._navigation.current
            try:
                if hasattr(old, "destroy"):
                    old.destroy()
            except:
                pass

        self._navigation.clear()

        if screen is not None:
            screen.app = self
            self._navigation.push(screen)

    def navigate(
        self,
        name,
        parameters: dict | None = None
    ):
        """
        Navigate between views safely.
        Prevents task leakage between screens.
        """

        self._cancel_all_tasks()

        view_class = self._routes[name]

        self.set_screen(
            view_class(self, parameters=parameters)
        )

    def push(self, screen) -> None:

        if screen is None:
            return

        screen.app = self
        self._navigation.push(screen)

    def pop(self):

        return self._navigation.pop()

    @property
    def navigation(self):
        return self._navigation

    # ------------------------------------------------------------------
    # Touch processing
    # ------------------------------------------------------------------

    def _poll_touch(self):

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

        screen = self.screen

        if screen is None:
            return

        if not screen.dirty:
            return

        screen.draw(self._renderer)
        self._renderer.flush()

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    async def _run_async(self) -> None:

        self._running = True

        while self._running:

            event = self._poll_touch()
            screen = self.screen

            if event is not None and screen is not None:
                screen.dispatch_touch(event)

            self._render()

            # cleanup finished tasks
            self._cleanup_tasks()

            await asyncio.sleep_ms(self._frame_delay_ms)

    # ------------------------------------------------------------------
    # Control
    # ------------------------------------------------------------------

    def stop(self) -> None:
        self._running = False

    def run(self) -> None:
        asyncio.run(self._run_async())

    def route(self, name, view_class):
        self._routes[name] = view_class

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"App("
            f"screen={self.screen}, "
            f"running={self._running})"
        )
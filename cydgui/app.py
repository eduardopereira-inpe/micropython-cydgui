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

import gc


from cydgui.core.events import EventDispatcher
from cydgui.core.navigation import Navigation


class App:
    """Main application object."""

    __slots__ = (
        "_renderer",
        "_touch",
        "_dispatcher",
        "_frame_delay_ms",
        "_navigation",
        "_running",
        "_routes",
        "_tasks",
        "_task_cleanup_counter",
    )

    def __init__(
        self,
        renderer,
        touch=None,
        screen=None,
        frame_delay_ms: int = 5
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
        self._dispatcher = EventDispatcher(touch)
        self._frame_delay_ms = frame_delay_ms

        self._navigation = Navigation()

        self._running = False

        self._routes = {}

        # NEW: managed async tasks
        self._tasks = set()
        self._task_cleanup_counter = 0

        if screen is not None:
            self.set_screen(screen)

    # ---------------------------------------------------------
    # Task management
    # ---------------------------------------------------------

    def create_task(self, coro):
        """Register a managed asyncio task.

        Args:
            coro: Coroutine to run.
        """
        task = asyncio.create_task(coro)
        self._tasks.add(task)
        return task

    def _cleanup_tasks(self):
        """Remove finished tasks."""
        if not self._tasks:
            return

        for task in tuple(self._tasks):
            if task.done():
                self._tasks.discard(task)

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

        self._navigation.clear(destroy=True)

        gc.collect()

        if screen is not None:

            screen.app = self

            self._navigation.push(screen)

            gc.collect()

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

        return self._dispatcher.poll()

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

            if event is not None and screen is not None:
                screen.dispatch_touch(event)

            self._render()

            # Reduce per-frame allocations by cleaning tasks periodically.
            self._task_cleanup_counter += 1
            if self._task_cleanup_counter >= 32:
                self._task_cleanup_counter = 0
                self._cleanup_tasks()

            await asyncio.sleep_ms(self._frame_delay_ms)
    # ------------------------------------------------------------------
    # Control
    # ------------------------------------------------------------------

    def stop(self) -> None:
        """Stop application."""

        self._running = False
        self._cleanup_tasks()

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

        self._navigation.clear(destroy=True)

        gc.collect()

        screen = view_class(self, parameters=parameters)

        screen.app = self

        self._navigation.push(screen)

        gc.collect()

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"App("
            f"screen={self.screen}, "
            f"running={self._running})"
        )
    
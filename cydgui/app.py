"""
cydgui.app
==========

Core application object.  ``App`` is the single entry point for every
cydgui-based program.  It owns the renderer, the theme, the event dispatcher,
and the navigation stack.

Responsibilities
----------------
- Bootstrap the framework.
- Hold references to all top-level collaborators.
- Drive the main ``uasyncio`` event loop.
- Delegate screen transitions to :class:`~cydgui.core.navigation.Navigation`.
- Delegate input events to :class:`~cydgui.core.events.EventDispatcher`.

Design notes
------------
- No global state: every dependency is injected via the constructor.
- Compatible with MicroPython's ``uasyncio`` (``import uasyncio as asyncio``).
- Widgets *never* receive a reference to the renderer directly; they call
  ``invalidate()`` and the App/Renderer pipeline does the actual drawing.
"""

# MicroPython ships ``uasyncio``; CPython ships ``asyncio``.
# The try/except lets the module be imported on both platforms.
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio  # type: ignore

from cydgui.core.events import EventDispatcher
from cydgui.core.navigation import Navigation
from cydgui.core.theme import Theme
from cydgui.render.renderer import Renderer


class App:
    """Root application object.

    Parameters
    ----------
    renderer:
        A concrete :class:`~cydgui.render.renderer.Renderer` implementation.
    theme:
        The active :class:`~cydgui.core.theme.Theme`.  When *None* a default
        theme is created automatically.
    """

    def __init__(self, renderer: Renderer, theme: Theme = None) -> None:
        # TODO: store renderer and theme references
        # TODO: create EventDispatcher instance
        # TODO: create Navigation instance
        # TODO: initialise dirty / redraw flag
        pass

    # ------------------------------------------------------------------
    # Screen management (delegated to Navigation)
    # ------------------------------------------------------------------

    def push(self, screen) -> None:
        """Push *screen* onto the navigation stack and make it active.

        TODO: delegate to self._navigation.push(screen)
        TODO: mark display as dirty
        """
        pass

    def pop(self) -> None:
        """Pop the current screen from the navigation stack.

        TODO: delegate to self._navigation.pop()
        TODO: mark display as dirty
        """
        pass

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    async def _run_async(self) -> None:
        """Async main loop.

        TODO: poll touch / input driver via EventDispatcher
        TODO: call renderer when display is dirty
        TODO: yield control with ``await asyncio.sleep_ms(0)`` between frames
        """
        pass

    def run(self) -> None:
        """Start the application.  Blocks until the application exits.

        TODO: call asyncio.run(self._run_async())
        """
        pass

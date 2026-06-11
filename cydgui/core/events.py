"""
cydgui.core.events
==================

Event types and the ``EventDispatcher`` used to route input events through the
widget tree.

Event model
-----------
- Events are plain objects (no subclassing of ``Exception``).
- The dispatcher polls the input driver (touch, keyboard, …) and produces
  ``Event`` instances.
- Events are passed to the active screen's ``dispatch_touch`` method.
- Listeners can also be registered directly on the dispatcher for global
  shortcuts or custom event types.

Adding a new event type
-----------------------
1. Add a constant to :data:`EventType`.
2. Create a corresponding ``Event`` subclass if extra fields are needed.
3. Emit it from the input driver adapter.

Notes
-----
- Compatible with MicroPython: no use of ``dataclasses``, ``enum.Enum``, or
  other CPython-only stdlib.
"""


# ---------------------------------------------------------------------------
# Event type constants
# ---------------------------------------------------------------------------

class EventType:
    """Namespace for event type identifiers.

    TODO: add more event types as needed (e.g. SWIPE, KEY_PRESS, …)
    """

    TOUCH_DOWN = "touch_down"
    TOUCH_MOVE = "touch_move"
    TOUCH_UP = "touch_up"
    CUSTOM = "custom"


# ---------------------------------------------------------------------------
# Event objects
# ---------------------------------------------------------------------------

class Event:
    """Generic event object.

    Parameters
    ----------
    event_type:
        One of the :class:`EventType` constants.
    """

    def __init__(self, event_type: str) -> None:
        # TODO: store event_type
        # TODO: store timestamp (utime.ticks_ms())
        pass


class TouchEvent(Event):
    """Touch / pointer event carrying screen coordinates.

    Parameters
    ----------
    event_type:
        Should be one of ``TOUCH_DOWN``, ``TOUCH_MOVE``, or ``TOUCH_UP``.
    x, y:
        Touch coordinates in screen pixels.
    """

    def __init__(self, event_type: str, x: int, y: int) -> None:
        super().__init__(event_type)
        # TODO: store x and y coordinates
        pass


# ---------------------------------------------------------------------------
# EventDispatcher
# ---------------------------------------------------------------------------

class EventDispatcher:
    """Routes events from input drivers to the active screen.

    Usage
    -----
    ::

        dispatcher = EventDispatcher()
        dispatcher.add_listener(EventType.TOUCH_DOWN, my_handler)
        dispatcher.dispatch(TouchEvent(EventType.TOUCH_DOWN, x=100, y=200))

    Design notes
    ------------
    - Listeners are plain callables: ``handler(event) -> None``.
    - No global listener registry; the instance owns its own listeners.
    - The active screen is injected by the App after each navigation change.
    """

    def __init__(self) -> None:
        # TODO: initialise listener dict: {event_type: [callables]}
        # TODO: store reference to active screen (None initially)
        pass

    # ------------------------------------------------------------------
    # Listener management
    # ------------------------------------------------------------------

    def add_listener(self, event_type: str, handler) -> None:
        """Register *handler* to be called when *event_type* events occur.

        TODO: append handler to self._listeners[event_type]
        """
        pass

    def remove_listener(self, event_type: str, handler) -> None:
        """Unregister *handler* for *event_type*.

        TODO: remove handler from self._listeners[event_type]
        """
        pass

    # ------------------------------------------------------------------
    # Dispatch
    # ------------------------------------------------------------------

    def dispatch(self, event: Event) -> None:
        """Deliver *event* to registered listeners and the active screen.

        TODO: call each listener registered for event.event_type
        TODO: if active screen is set, call screen.dispatch_touch(event)
        """
        pass

    # ------------------------------------------------------------------
    # Active screen
    # ------------------------------------------------------------------

    def set_active_screen(self, screen) -> None:
        """Update the screen that receives touch events.

        TODO: store screen reference
        """
        pass

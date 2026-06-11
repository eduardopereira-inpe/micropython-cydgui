"""
cydgui.core.navigation
======================

Screen navigation stack for the cydgui framework.

The ``Navigation`` class manages a stack of :class:`~cydgui.core.screen.Screen`
objects, allowing the application to:

- ``push(screen)`` — display a new screen on top of the current one.
- ``pop()``         — return to the previous screen.
- ``replace(screen)`` — swap the top screen without growing the stack.

The navigation object notifies screens of lifecycle events (``on_enter``,
``on_leave``) and informs the :class:`~cydgui.core.events.EventDispatcher` of
the active screen after each transition.

Design notes
------------
- The stack never becomes empty; ``pop()`` on a single-item stack is a no-op.
- Navigation does not reference the renderer directly; it leaves display
  invalidation to the App.
"""


class Navigation:
    """Manages a stack of screens and drives screen lifecycle callbacks.

    Parameters
    ----------
    dispatcher:
        The application's :class:`~cydgui.core.events.EventDispatcher`; it is
        updated after every screen transition so touch events are routed to the
        correct screen.
    """

    def __init__(self, dispatcher) -> None:
        # TODO: store dispatcher reference
        # TODO: initialise stack list: self._stack = []
        pass

    # ------------------------------------------------------------------
    # Stack operations
    # ------------------------------------------------------------------

    def push(self, screen) -> None:
        """Push *screen* onto the stack.

        The previous screen receives ``on_leave()``.
        The new screen receives ``on_enter()``.
        The dispatcher's active screen is updated.

        TODO: call current().on_leave() if stack is not empty
        TODO: append screen to self._stack
        TODO: call screen.on_enter()
        TODO: update dispatcher active screen
        """
        pass

    def pop(self) -> None:
        """Pop the top screen from the stack.

        Does nothing if only one screen remains.

        TODO: guard against empty / single-item stack
        TODO: call current().on_leave()
        TODO: pop from self._stack
        TODO: call current().on_enter() (the newly exposed screen)
        TODO: update dispatcher active screen
        """
        pass

    def replace(self, screen) -> None:
        """Replace the current top screen with *screen*.

        TODO: call current().on_leave()
        TODO: replace top of stack with screen
        TODO: call screen.on_enter()
        TODO: update dispatcher active screen
        """
        pass

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------

    def current(self):
        """Return the currently active screen, or None if the stack is empty.

        TODO: return self._stack[-1] if self._stack else None
        """
        return None

    @property
    def depth(self) -> int:
        """Return the number of screens currently in the stack.

        TODO: return len(self._stack)
        """
        return 0

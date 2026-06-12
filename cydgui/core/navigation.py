"""
cydgui.core.navigation
======================

Screen navigation manager.

Responsible for managing the screen stack and handling
screen transitions.

Design goals
------------
- Lightweight.
- No renderer dependency.
- No touch dependency.
- Compatible with MicroPython.
"""

from cydgui.core.screen import Screen


class Navigation:
    """Screen navigation stack."""

    def __init__(self) -> None:
        """Initialize navigation."""

        self._stack = []

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def current(self):
        """
        Return active screen.

        Returns:
            Screen or None.
        """

        if not self._stack:
            return None

        return self._stack[-1]

    @property
    def size(self) -> int:
        """Return stack size."""

        return len(self._stack)

    @property
    def empty(self) -> bool:
        """Return True when stack is empty."""

        return len(self._stack) == 0

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def push(
        self,
        screen: Screen
    ) -> None:
        """
        Push screen onto stack.

        Args:
            screen: Screen instance.
        """

        if screen is None:
            return

        current = self.current

        if current:
            current.on_leave()

        self._stack.append(screen)

        screen.on_enter()

    def pop(self):
        """
        Pop current screen.

        Returns:
            Removed screen or None.
        """

        if not self._stack:
            return None

        current = self._stack.pop()

        current.on_leave()

        if self.current:
            self.current.on_enter()

        return current

    def replace(
        self,
        screen: Screen
    ) -> None:
        """
        Replace current screen.

        Args:
            screen: New screen.
        """

        self.pop()

        self.push(screen)

    def clear(self) -> None:
        """Remove all screens."""

        while self._stack:
            screen = self._stack.pop()

            try:
                screen.on_leave()
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def contains(
        self,
        screen: Screen
    ) -> bool:
        """
        Check if screen exists in stack.

        Args:
            screen: Screen instance.

        Returns:
            bool
        """

        return screen in self._stack

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        current = self.current

        if current is None:
            return "Navigation(empty)"

        return (
            f"Navigation("
            f"screens={len(self._stack)}, "
            f"current='{current.name}')"
        )
"""
cydgui.core.screen
==================

Root screen implementation.

Responsibilities
----------------
- Own the root widget tree.
- Perform full screen clear only when necessary.
- Support partial redraw through dirty children.
- Dispatch touch events.

Designed for MicroPython and CYD.
"""

from cydgui.core.container import Container


class Screen(Container):
    """Root screen with partial redraw support."""

    __slots__ = (
        "name",
        "background",
        "_needs_full_clear",
    )

    def __init__(
        self,
        name: str = "",
        background: int = 0x0000
    ) -> None:
        """
        Initialize screen.

        Args:
            name:
                Screen name.
            background:
                Screen background color.
        """
        super().__init__(
            x=0,
            y=0,
            width=240,
            height=320
        )

        self.name = name
        self.background = background

        #
        # Full clear required only:
        # - first render
        # - screen navigation
        #
        self._needs_full_clear = True

    # ------------------------------------------------------------------
    # Dirty state
    # ------------------------------------------------------------------

    @property
    def dirty(self) -> bool:
        """
        Return dirty state.

        Returns:
            True when screen or any child requires redraw.
        """
        return (
            self._dirty or
            len(self._dirty_children) > 0
        )

    def invalidate(self) -> None:
        """
        Invalidate entire screen.

        Used when:
        - entering screen
        - structural changes
        - full refresh required
        """
        self._dirty = True
        self._needs_full_clear = True

    def child_invalidated(self, child) -> None:
        """
        Track dirty child.

        IMPORTANT:
        Do not invalidate entire screen.
        Only register child for partial redraw.
        """
        self._dirty_children[id(child)] = child

    def validate(self) -> None:
        """
        Mark screen as clean.
        """
        self._dirty = False
        self._dirty_children.clear()

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        """
        Draw screen.

        Full redraw:
            - first render
            - navigation
            - explicit invalidate()

        Partial redraw:
            - dirty widgets only
        """
        if not self.visible:
            return

        #
        # Full screen clear only when needed.
        #
        if self._needs_full_clear:

            renderer.clear(self.background)

            self._needs_full_clear = False

            #
            # Force complete widget tree redraw.
            #
            self._dirty = True

        super().draw(renderer)

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def dispatch_touch(self, event) -> bool:
        """
        Dispatch touch event through widget tree.

        Args:
            event:
                Touch event.

        Returns:
            True if handled.
        """
        return self.on_touch(event)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def on_enter(self) -> None:
        """
        Called when screen becomes active.
        """
        self.invalidate()

    def on_leave(self) -> None:
        """
        Called before screen is removed.
        """
        pass

    def destroy(self) -> None:
        """Release the full screen tree."""

        self._needs_full_clear = True
        super().destroy()

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"Screen("
            f"name='{self.name}', "
            f"children={len(self.children)})"
        )
"""
cydgui.core.screen
==================
"""

from cydgui.core.container import Container


class Screen(Container):
    """Root screen without global clear invalidation."""

    def __init__(self, name: str = "", background: int = 0x0000) -> None:
        super().__init__(x=0, y=0, width=240, height=320)

        self.name = name
        self.background = background

        self._needs_full_clear = True

    # ------------------------------------------------------------------
    # Dirty state
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Dirty state (Substitua os métodos dirty e validate atuais)
    # ------------------------------------------------------------------

    @property
    def dirty(self) -> bool:
        """Return screen invalidation state."""
        return self._dirty or len(self._dirty_children) > 0

    def invalidate(self) -> None:
        self._dirty = True
        self._needs_full_clear = True

    def child_invalidated(self, child) -> None:
        self._dirty = True

    def validate(self) -> None:
        """Mark screen as rendered."""
        self._dirty = False
        self._dirty_children.clear()

    # -------------------------
    # Drawing FIXED
    # -------------------------

    def draw(self, renderer) -> None:
        if not self.visible:
            return

        if self._needs_full_clear:
            renderer.clear(self.background)
            self._needs_full_clear = False

        super().draw(renderer)
        self.validate()

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def dispatch_touch(self, event) -> bool:
        """
        Dispatch touch event through widget tree.
        """

        return self.on_touch(event)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def on_enter(self) -> None:
        """Called when screen becomes active."""
        self.invalidate()
        self._needs_clear = True

    def on_leave(self) -> None:
        """Called before screen is removed."""
        pass

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"Screen("
            f"name='{self.name}', "
            f"children={len(self.children)})"
        )
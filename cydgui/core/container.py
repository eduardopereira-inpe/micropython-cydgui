"""
cydgui.core.container
=====================

Container widget.

Stores child widgets, dispatches events and draws the widget tree.
"""

from cydgui.core.widget import Widget


class Container(Widget):
    """Base container widget."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0,
        visible: bool = True,
        enabled: bool = True,
    ) -> None:

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            visible=visible,
            enabled=enabled,
        )

        self._children = []
        self._dirty_children = set()

    def mark_child_dirty(self, widget):
        self._dirty_children.add(widget)

        if self._parent:
            self._parent.mark_child_dirty(self)

    # ------------------------------------------------------------------
    # Child management
    # ------------------------------------------------------------------

    def add(self, widget):
        """Add child widget."""

        if widget not in self._children:

            self._children.append(widget)

            widget.on_attach(self)

            self.invalidate()

        return widget

    def remove(self, widget) -> None:
        """Remove child widget."""

        if widget in self._children:

            self._children.remove(widget)

            widget.on_detach()

            self.invalidate()

    def clear(self) -> None:
        """Remove all children."""

        for child in self._children:
            child.on_detach()

        self._children.clear()

        self.invalidate()

    @property
    def children(self):
        """Return children."""

        return tuple(self._children)

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        """Draw container and only dirty or necessary visible children."""
        if not self.visible:
            return

        for child in self._children:
            if not child.visible:
                continue

            if not child.dirty:
                continue

            # Só desenha se o filho estiver marcado como dirty 
            # OU se o próprio container pai foi totalmente invalidado
            if child.dirty or self.dirty:
                if hasattr(child, 'renderer'):
                    child.set_renderer(renderer)
                
                child.draw(renderer)

        self.validate()

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def on_touch(self, event) -> bool:
        """Dispatch touch event."""

        if not self.enabled:
            return False

        for child in reversed(self._children):

            if not child.visible:
                continue

            if not child.contains(
                event.x,
                event.y
            ):
                continue

            if child.on_touch(event):
                return True

        return False

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"Container("
            f"children={len(self._children)})"
        )
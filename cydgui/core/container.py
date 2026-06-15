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

    def mark_child_dirty(self, widget):
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

        children = self._children
        self._children = []

        for child in children:
            child.on_detach()

        self.invalidate()

    @property
    def children(self):
        """Return children."""

        if self._children_tuple is None or len(self._children_tuple) != len(self._children):
            self._children_tuple = tuple(self._children)

        return self._children_tuple

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

            set_renderer = getattr(child, "set_renderer", None)
            if set_renderer is not None:
                set_renderer(renderer)

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
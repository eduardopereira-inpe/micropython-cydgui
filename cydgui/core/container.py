"""
cydgui.core.container
=====================
"""

from cydgui.core.widget import Widget


class Container(Widget):
    """Widget that stores children and manages partial redraw."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._children = []
        self._dirty_children = set()

    # -------------------------
    # Dirty propagation FIX
    # -------------------------

    def child_invalidated(self, child: Widget) -> None:
        """
        Receives dirty notification from children.

        IMPORTANT:
        We DO NOT clear screen here anymore.
        We only mark subtree dirty.
        """
        self._dirty = True
        self._dirty_children.add(child)

        if self._parent:
            self._parent.child_invalidated(self)

    # -------------------------
    # Children
    # -------------------------

    def add(self, widget: Widget):
        if widget not in self._children:
            self._children.append(widget)
            widget.on_attach(self)
            self.invalidate()
        return widget

    def remove(self, widget: Widget) -> None:
        if widget in self._children:
            self._children.remove(widget)
            widget.on_detach()
            self.invalidate()

    @property
    def children(self):
        return tuple(self._children)

    # -------------------------
    # Drawing (FIXED: NO FULL WIPE LOGIC HERE)
    # -------------------------

    def draw(self, renderer) -> None:
        if not self.visible:
            return

        for child in self._children:
            if not child.visible:
                continue

            if child.dirty:
                child.draw(renderer)

        self.validate()
        self._dirty_children.clear()

    # -------------------------
    # Touch
    # -------------------------

    def on_touch(self, event) -> bool:
        if not self.enabled:
            return False

        for child in reversed(self._children):
            if child.visible and child.contains(event.x, event.y):
                if child.on_touch(event):
                    return True

        return False
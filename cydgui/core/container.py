"""
cydgui.core.container
=====================
"""

from cydgui.core.widget import Widget


class Container(Widget):
    """Widget that stores children and manages partial redraw."""

    __slots__ = (
        "_children",
        "_dirty_children",
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._children = []
        self._dirty_children = {}

    def mark_child_dirty(self, widget):
        self._dirty_children[id(widget)] = widget

        if self._parent:
            self._parent.child_invalidated(self)

    # Backward-compatible alias used by Widget.invalidate()
    def child_invalidated(self, child):
        self.mark_child_dirty(child)

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

    def clear(self, destroy_children: bool = False) -> None:
        """Remove all children."""

        for child in list(self._children):
            try:
                if destroy_children and hasattr(child, "destroy"):
                    child.destroy()
                else:
                    child.on_detach()
            except Exception:
                pass

        self._children.clear()
        self._dirty_children.clear()

        self.invalidate()

    @property
    def children(self):
        return tuple(self._children)

    def iter_children(self):
        """Return direct children iterator without allocating a tuple."""
        return self._children

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Propriedades de Estado (Adicionar antes do draw)
    # ------------------------------------------------------------------

    @property
    def dirty(self) -> bool:
        return self._dirty or len(self._dirty_children) > 0

    def validate(self) -> None:
        super().validate()
        self._dirty_children.clear()

    def destroy(self) -> None:
        self.clear(destroy_children=True)
        super().destroy()

    # ------------------------------------------------------------------
    # Drawing (Substitua o método draw atual)
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        if not self.visible:
            return

        #
        # Container redraw
        #
        if self._dirty:

            super().draw(renderer)

            for child in self._children:

                if not child.visible:
                    continue

                if hasattr(child, "renderer"):
                    child.set_renderer(renderer)

                child.draw(renderer)

        #
        # Partial redraw
        #
        else:

            for child in self._dirty_children.values():

                if not child.visible:
                    continue

                if hasattr(child, "renderer"):
                    child.set_renderer(renderer)

                child.draw(renderer)

        self.validate()

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
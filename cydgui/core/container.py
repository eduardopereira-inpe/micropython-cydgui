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
        self._dirty_children = {}

    def mark_child_dirty(self, widget):
        self._dirty_children[id(widget)] = widget

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

    # ------------------------------------------------------------------
    # Drawing (Substitua o método draw atual)
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        if not self.visible:
            return

        for child in self._children:
            if not child.visible:
                continue

            # ATENÇÃO AQUI: Usamos a variável interna self._dirty em vez 
            # da property self.dirty. Isso garante que só os componentes
            # que realmente mudaram sejam desenhados, economizando CPU.
            if child.dirty or self._dirty:
                if hasattr(child, 'renderer'):
                    child.set_renderer(renderer)
                
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
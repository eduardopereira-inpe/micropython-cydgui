"""
cydgui.core.container
=====================

A Container is a widget capable of owning child widgets.

Responsibilities
----------------
- Store child widgets.
- Draw child widgets.
- Dispatch input events to child widgets.
- Propagate invalidation requests.

Design notes
------------
- Container performs no automatic layout.
- Child coordinates are relative to the container.
- Children are drawn in insertion order.
- Events are dispatched in reverse order (top-most widget first).
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

    # ------------------------------------------------------------------
    # Child management
    # ------------------------------------------------------------------

    def add(self, widget: Widget) -> Widget:
        """
        Add a child widget.

        Returns
        -------
        Widget
            The added widget.
        """

        if widget not in self._children:

            self._children.append(widget)

            widget.on_attach(self)

            self.invalidate()

        return widget

    def remove(self, widget: Widget) -> None:
        """Remove a child widget."""

        if widget in self._children:

            self._children.remove(widget)

            widget.on_detach()

            self.invalidate()

    def clear(self) -> None:
        """Remove all child widgets."""

        for child in self._children:
            child.on_detach()

        self._children.clear()

        self.invalidate()

    @property
    def children(self):
        """Return child widgets as a read-only tuple."""

        return tuple(self._children)

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        """Draw visible child widgets."""

        if not self.visible:
            return

        for child in self._children:

            if not child.visible:
                continue

            if child.dirty:
                child.draw(renderer)

        self.validate()

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def on_touch(self, event) -> bool:
        """
        Dispatch touch event.

        Children are checked in reverse order so the most recently
        added widget receives the event first.
        """

        if not self.enabled:
            return False

        x = event.x
        y = event.y

        for child in reversed(self._children):

            if not child.visible:
                continue

            if not child.contains(x, y):
                continue

            if child.on_touch(event):
                return True

        return False

    def on_touch_release(self, event) -> bool:
        """Dispatch touch release."""

        if not self.enabled:
            return False

        for child in reversed(self._children):

            if not child.visible:
                continue

            if child.on_touch_release(event):
                return True

        return False
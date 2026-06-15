"""
cydgui.core.widget
==================

Base class for every visual element in the cydgui framework.
"""

from cydgui.utils.geometry import Rect


class Widget:
    """Base widget for all visual components."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0,
        visible: bool = True,
        enabled: bool = True,
    ) -> None:

        self._rect = Rect(x=x, y=y, width=width, height=height)

        self._visible = visible
        self._enabled = enabled

        self._dirty = True
        self._parent = None

    # -------------------------
    # Geometry
    # -------------------------

    @property
    def rect(self) -> Rect:
        return self._rect

    @property
    def x(self) -> int:
        return self._rect.x

    @property
    def y(self) -> int:
        return self._rect.y

    @property
    def width(self) -> int:
        return self._rect.width

    @property
    def height(self) -> int:
        return self._rect.height

    def move_to(self, x: int, y: int) -> None:
        if self._rect.x == x and self._rect.y == y:
            return

        self._rect.x = x
        self._rect.y = y
        self.invalidate()
        
    def contains(
        self,
        x: int,
        y: int
    ) -> bool:
        """
        Return True if a screen coordinate lies inside
        this widget.
        """

        ax = self.absolute_x
        ay = self.absolute_y

        return (
            ax <= x < (ax + self.width)
            and
            ay <= y < (ay + self.height)
        )

    def resize(self, width: int, height: int) -> None:
        if self._rect.width == width and self._rect.height == height:
            return

        self._rect.width = width
        self._rect.height = height
        self.invalidate()

    # -------------------------
    # Absolute coordinates
    # -------------------------

    @property
    def absolute_x(self) -> int:
        return self._parent.absolute_x + self.x if self._parent else self.x

    @property
    def absolute_y(self) -> int:
        return self._parent.absolute_y + self.y if self._parent else self.y

    @property
    def absolute_rect(self) -> Rect:
        return Rect(
            x=self.absolute_x,
            y=self.absolute_y,
            width=self.width,
            height=self.height,
        )

    # -------------------------
    # State
    # -------------------------

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        if self._visible == value:
            return
        self._visible = value
        self.invalidate()

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        if self._enabled == value:
            return
        self._enabled = value
        self.invalidate()

    # -------------------------
    # Dirty system (FIXED)
    # -------------------------

    @property
    def dirty(self) -> bool:
        return self._dirty

    def invalidate(self) -> None:
        """
        Mark widget as dirty and propagate upward WITHOUT forcing full-screen reset.
        """
        self._dirty = True

        # propagate only signal, NOT screen clearing behavior
        if self._parent:
            self._parent.child_invalidated(self)

    def validate(self) -> None:
        self._dirty = False

    # -------------------------
    # Drawing
    # -------------------------

    def draw(self, renderer) -> None:
        self.validate()

    # -------------------------
    # Input
    # -------------------------

    def on_touch(self, event) -> bool:
        return False

    # -------------------------
    # Parent
    # -------------------------

    @property
    def parent(self):
        return self._parent

    def on_attach(self, parent) -> None:
        self._parent = parent

    def on_detach(self) -> None:
        self._parent = None

    # -------------------------
    # Debug
    # -------------------------

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, w={self.width}, h={self.height})"
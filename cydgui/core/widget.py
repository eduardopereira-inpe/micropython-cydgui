"""
cydgui.core.widget
==================

Base class for every visual element in the cydgui framework.

Design contract
---------------
- A Widget knows its own geometry.
- A Widget never talks directly to the display driver.
- A Widget never talks directly to the touch driver.
- Rendering is delegated to a Renderer instance.
- Widgets can request redraws through invalidate().
- Widgets can belong to a parent Container.
- Coordinates are relative to the parent widget.

Lifecycle
---------
1. Widget is instantiated.
2. Widget is attached to a parent Container.
3. Widget requests redraws via invalidate().
4. App rendering pipeline calls draw(renderer).
5. Touch events are dispatched through on_touch().
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

        self._rect = Rect(
            x=x,
            y=y,
            width=width,
            height=height
        )

        self._visible = visible
        self._enabled = enabled

        self._dirty = True

        self._parent = None

    # ------------------------------------------------------------------
    # Geometry
    # ------------------------------------------------------------------

    @property
    def rect(self) -> Rect:
        """Return widget bounds."""
        return self._rect

    @property
    def x(self) -> int:
        """Return local X coordinate."""
        return self._rect.x

    @property
    def y(self) -> int:
        """Return local Y coordinate."""
        return self._rect.y

    @property
    def width(self) -> int:
        """Return widget width."""
        return self._rect.width

    @property
    def height(self) -> int:
        """Return widget height."""
        return self._rect.height

    @property
    def absolute_x(self) -> int:
        """Return absolute screen X coordinate."""

        if self._parent:
            return self._parent.absolute_x + self.x

        return self.x

    @property
    def absolute_y(self) -> int:
        """Return absolute screen Y coordinate."""

        if self._parent:
            return self._parent.absolute_y + self.y

        return self.y

    def contains(
        self,
        x: int,
        y: int
    ) -> bool:
        """Return True if a point lies inside the widget."""

        ax = self.absolute_x
        ay = self.absolute_y

        return (
            ax <= x < (ax + self.width) and
            ay <= y < (ay + self.height)
        )

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    @property
    def visible(self) -> bool:
        """Return widget visibility."""
        return self._visible

    @visible.setter
    def visible(
        self,
        value: bool
    ) -> None:

        if self._visible != value:
            self._visible = value
            self.invalidate()

    @property
    def enabled(self) -> bool:
        """Return enabled state."""
        return self._enabled

    @enabled.setter
    def enabled(
        self,
        value: bool
    ) -> None:

        if self._enabled != value:
            self._enabled = value
            self.invalidate()

    # ------------------------------------------------------------------
    # Dirty tracking
    # ------------------------------------------------------------------

    @property
    def dirty(self) -> bool:
        """Return dirty state."""
        return self._dirty

    def invalidate(self) -> None:
        """Mark widget as requiring redraw."""

        self._dirty = True

        if self._parent:
            self._parent.invalidate()

    def validate(self) -> None:
        """Mark widget as rendered."""

        self._dirty = False

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        """
        Draw widget contents.

        Subclasses should override this method.
        """

        self.validate()

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def on_touch(self, event) -> bool:
        """
        Handle a touch event.

        The event may represent:
        - TouchEvent.DOWN
        - TouchEvent.MOVE
        - TouchEvent.UP

        Args:
            event: TouchEvent instance.

        Returns:
            True if the event was consumed.
        """

        return False

    # ------------------------------------------------------------------
    # Parent management
    # ------------------------------------------------------------------

    @property
    def parent(self):
        """Return parent widget."""
        return self._parent

    def on_attach(
        self,
        parent
    ) -> None:
        """Attach widget to a parent container."""

        self._parent = parent

    def on_detach(self) -> None:
        """Detach widget from its parent."""

        self._parent = None

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"x={self.x}, "
            f"y={self.y}, "
            f"width={self.width}, "
            f"height={self.height})"
        )
"""
cydgui.utils.geometry
=====================

Lightweight geometric primitives used throughout the cydgui framework.

Classes
-------
Point       An (x, y) integer coordinate pair.
Size        A (width, height) integer dimension pair.
Rect        An axis-aligned rectangle defined by (x, y, width, height).

Design notes
------------
- All values are plain Python integers (no floats) to keep memory usage low on
  MicroPython.
- These classes are intentionally minimal; they provide only the helpers that
  the framework itself uses internally.
- No external dependencies.
"""


class Point:
    """An integer (x, y) coordinate pair.

    Parameters
    ----------
    x, y:
        Horizontal and vertical coordinates.
    """

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other) -> bool:

        if not isinstance(other, Point):
            return False

        return (
            self.x == other.x and
            self.y == other.y
        )


class Size:
    """An integer (width, height) dimension pair.

    Parameters
    ----------
    width, height:
        Horizontal and vertical extents.
    """

    def __init__(
        self,
        width: int = 0,
        height: int = 0
    ) -> None:

        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return f"Size({self.width}, {self.height})"

    def __eq__(self, other) -> bool:

        if not isinstance(other, Size):
            return False

        return (
            self.width == other.width and
            self.height == other.height
        )


class Rect:
    """An axis-aligned rectangle.

    Parameters
    ----------
    x, y:
        Top-left corner coordinates.
    width, height:
        Rectangle dimensions in pixels.
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0
    ) -> None:

        self._x = x
        self._y = y
        self._width = width
        self._height = height

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def right(self) -> int:
        """Return x + width (exclusive right edge)."""
        return self._x + self._width

    @property
    def bottom(self) -> int:
        """Return y + height (exclusive bottom edge)."""
        return self._y + self._height

    @property
    def cx(self) -> int:
        """Return the horizontal centre x-coordinate."""
        return self._x + (self._width // 2)

    @property
    def cy(self) -> int:
        """Return the vertical centre y-coordinate."""
        return self._y + (self._height // 2)
    
    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = value

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._height = value

    # ------------------------------------------------------------------
    # Geometric operations
    # ------------------------------------------------------------------

    def contains(self, x: int, y: int) -> bool:
        """Return True if the point (x, y) is inside this rectangle."""

        return (
            self.x <= x < self.right and
            self.y <= y < self.bottom
        )

    def intersects(self, other: "Rect") -> bool:
        """Return True if this rectangle overlaps with *other*."""

        return not (
            self.right <= other.x or
            other.right <= self.x or
            self.bottom <= other.y or
            other.bottom <= self.y
        )

    def union(self, other: "Rect") -> "Rect":
        """Return the smallest Rect that contains both self and *other*."""

        left = min(self.x, other.x)
        top = min(self.y, other.y)

        right = max(self.right, other.right)
        bottom = max(self.bottom, other.bottom)

        return Rect(
            x=left,
            y=top,
            width=right - left,
            height=bottom - top
        )

    def move_to(self, x: int, y: int) -> None:
        """Move rectangle to an absolute position."""

        self._x = x
        self._y = y

    def resize(self, width: int, height: int) -> None:
        """Resize rectangle."""

        self._width = width
        self._height = height

    def copy(self) -> "Rect":
        """Return a copy of this rectangle."""

        return Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def __repr__(self) -> str:

        return (
            f"Rect("
            f"{self.x}, "
            f"{self.y}, "
            f"{self.width}, "
            f"{self.height})"
        )

    def __eq__(self, other) -> bool:

        if not isinstance(other, Rect):
            return False

        return (
            self.x == other.x and
            self.y == other.y and
            self.width == other.width and
            self.height == other.height
        )
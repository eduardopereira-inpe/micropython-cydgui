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
        # TODO: store x, y
        pass

    def __repr__(self) -> str:
        # TODO: return f"Point({self.x}, {self.y})"
        return "Point()"

    def __eq__(self, other) -> bool:
        # TODO: compare x and y
        return False


class Size:
    """An integer (width, height) dimension pair.

    Parameters
    ----------
    width, height:
        Horizontal and vertical extents.
    """

    def __init__(self, width: int = 0, height: int = 0) -> None:
        # TODO: store width, height
        pass

    def __repr__(self) -> str:
        # TODO: return f"Size({self.width}, {self.height})"
        return "Size()"


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
        self, x: int = 0, y: int = 0, width: int = 0, height: int = 0
    ) -> None:
        # TODO: store x, y, width, height
        pass

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def x(self) -> int:
        """TODO: return self._x"""
        return 0

    @property
    def y(self) -> int:
        """TODO: return self._y"""
        return 0

    @property
    def width(self) -> int:
        """TODO: return self._width"""
        return 0

    @property
    def height(self) -> int:
        """TODO: return self._height"""
        return 0

    @property
    def right(self) -> int:
        """Return x + width (exclusive right edge).

        TODO: return self._x + self._width
        """
        return 0

    @property
    def bottom(self) -> int:
        """Return y + height (exclusive bottom edge).

        TODO: return self._y + self._height
        """
        return 0

    @property
    def cx(self) -> int:
        """Return the horizontal centre x-coordinate.

        TODO: return self._x + self._width // 2
        """
        return 0

    @property
    def cy(self) -> int:
        """Return the vertical centre y-coordinate.

        TODO: return self._y + self._height // 2
        """
        return 0

    # ------------------------------------------------------------------
    # Geometric operations
    # ------------------------------------------------------------------

    def contains(self, x: int, y: int) -> bool:
        """Return True if the point (x, y) is inside this rectangle.

        TODO: return x >= self.x and x < self.right
                  and y >= self.y and y < self.bottom
        """
        return False

    def intersects(self, other: "Rect") -> bool:
        """Return True if this rectangle overlaps with *other*.

        TODO: implement axis-aligned intersection test
        """
        return False

    def union(self, other: "Rect") -> "Rect":
        """Return the smallest Rect that contains both self and *other*.

        TODO: compute min/max of corners and return new Rect
        """
        return Rect()

    def __repr__(self) -> str:
        # TODO: return f"Rect({self.x}, {self.y}, {self.width}, {self.height})"
        return "Rect()"

    def __eq__(self, other) -> bool:
        # TODO: compare all four components
        return False

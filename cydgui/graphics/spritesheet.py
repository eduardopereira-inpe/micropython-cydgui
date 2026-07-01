"""
cydgui.graphics.spritesheet
===========================

Sprite sheet resource.

A SpriteSheet is responsible only for:
    - Loading RGB565 sprite data from storage.
    - Providing SpriteFrame objects.
    - Managing a lightweight frame cache.
    - Exposing sheet geometry helpers.

It does NOT manage animations or state.
"""

from cydgui.graphics.sprite_frame import SpriteFrame


class SpriteSheet:
    """Sprite sheet resource."""

    __slots__ = (
        "_path",
        "_frame_width",
        "_frame_height",
        "_sheet_width",
        "_sheet_height",
        "_columns",
        "_rows",
        "_frame_size",
        "_cache",
        "_cache_order",
        "_cache_size",
        "_file",
        "_closed",
    )

    def __init__(
        self,
        path,
        frame_width,
        frame_height,
        sheet_width,
        sheet_height,
        cache_size=8,
    ):
        """Initialize the sprite sheet.

        Args:
            path: Path to RGB565 binary file.
            frame_width: Frame width in pixels.
            frame_height: Frame height in pixels.
            sheet_width: Total sheet width in pixels.
            sheet_height: Total sheet height in pixels.
            cache_size: Number of frames to cache.
        """

        self._path = path

        self._frame_width = int(frame_width)
        self._frame_height = int(frame_height)

        self._sheet_width = int(sheet_width)
        self._sheet_height = int(sheet_height)

        self._columns = self._sheet_width // self._frame_width
        self._rows = self._sheet_height // self._frame_height

        self._frame_size = self._frame_width * self._frame_height * 2

        self._cache = {}
        self._cache_order = []
        self._cache_size = cache_size

        self._file = open(path, "rb")
        self._closed = False

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def frame_width(self):
        return self._frame_width

    @property
    def frame_height(self):
        return self._frame_height

    @property
    def columns(self):
        return self._columns

    @property
    def rows(self):
        return self._rows

    @property
    def frame_count(self):
        return self._columns * self._rows

    # ---------------------------------------------------------
    # Geometry helper (NEW CORE API)
    # ---------------------------------------------------------

    def row(self, row, start=0, count=None):
        """Return a range of frame indices from a row.

        Args:
            row: Row index.
            start: Starting column.
            count: Number of frames.

        Returns:
            range: Frame indices.
        """

        if count is None:
            count = self._columns - start

        first = row * self._columns + start

        return range(first, first + count)

    # ---------------------------------------------------------
    # Frame access
    # ---------------------------------------------------------

    def get_frame(
        self,
        index,
        flip_x=False,
        flip_y=False,
    ):
        """Return a SpriteFrame."""

        key = (
            index,
            flip_x,
            flip_y,
        )

        if self._cache_size != 0:

            frame = self._cache.get(key)

            if frame is not None:
                return frame

        frame = self._load_frame(index)

        if flip_x or flip_y:
            frame = self._transform(
                frame,
                flip_x,
                flip_y,
            )

        self._add_cache(key, frame)

        return frame

    # ---------------------------------------------------------
    # Cache
    # ---------------------------------------------------------

    def clear_cache(self):
        """Clear frame cache."""

        self._cache.clear()
        self._cache_order.clear()

    def _add_cache(self, key, frame):
        """Insert frame into cache."""

        if self._cache_size == 0:
            return

        if key in self._cache:
            return

        while len(self._cache_order) >= self._cache_size:

            old = self._cache_order.pop(0)

            del self._cache[old]

        self._cache[key] = frame
        self._cache_order.append(key)

    # ---------------------------------------------------------
    # Frame loading
    # ---------------------------------------------------------

    def _load_frame(self, index):
        """Load a single frame from file."""

        if not 0 <= index < self.frame_count:
            raise IndexError("Frame index out of range.")

        column = index % self._columns
        row = index // self._columns

        x = column * self._frame_width
        y = row * self._frame_height

        buffer = bytearray(self._frame_size)

        position = 0

        for line in range(self._frame_height):

            offset = (
                ((y + line) * self._sheet_width + x) * 2
            )

            self._file.seek(offset)

            size = self._frame_width * 2

            buffer[position:position + size] = self._file.read(size)

            position += size

        return SpriteFrame(
            index=index,
            buffer=buffer,
            width=self._frame_width,
            height=self._frame_height,
        )
    #################################################################
    # Image transforms
    #################################################################

    def _transform(
        self,
        frame,
        flip_x=False,
        flip_y=False,
    ):
        """Return a transformed SpriteFrame.

        Args:
            frame: Source SpriteFrame.
            flip_x: Mirror horizontally.
            flip_y: Mirror vertically.

        Returns:
            SpriteFrame: Transformed frame.
        """

        if not (flip_x or flip_y):
            return frame

        return SpriteFrame(
            index=frame.index,
            buffer=self._flip(
                frame.buffer,
                flip_x=flip_x,
                flip_y=flip_y,
            ),
            width=frame.width,
            height=frame.height,
        )


    def _flip(
        self,
        source,
        flip_x=False,
        flip_y=False,
    ):
        """Flip an RGB565 image.

        This method performs horizontal, vertical or combined flips
        using a single implementation.

        Args:
            source: Source RGB565 buffer.
            flip_x: Mirror horizontally.
            flip_y: Mirror vertically.

        Returns:
            bytearray: Flipped image buffer.
        """

        w = self._frame_width
        h = self._frame_height

        stride = w * 2

        dst = bytearray(len(source))

        for y in range(h):

            src_row = y * stride

            if flip_y:
                dst_row = (h - 1 - y) * stride
            else:
                dst_row = src_row

            for x in range(w):

                src = src_row + x * 2

                if flip_x:
                    dst_col = (w - 1 - x) * 2
                else:
                    dst_col = x * 2

                dst_index = dst_row + dst_col

                dst[dst_index] = source[src]
                dst[dst_index + 1] = source[src + 1]

        return dst


    def _flip_x(self, source):
        """Mirror image horizontally."""

        return self._flip(
            source,
            flip_x=True,
        )


    def _flip_y(self, source):
        """Mirror image vertically."""

        return self._flip(
            source,
            flip_y=True,
        )


    def _flip_xy(self, source):
        """Mirror image horizontally and vertically."""

        return self._flip(
            source,
            flip_x=True,
            flip_y=True,
        )

    # ---------------------------------------------------------
    # Resource management
    # ---------------------------------------------------------

    def close(self):
        """Release resources."""

        if self._closed:
            return

        self.clear_cache()
        self._file.close()
        self._closed = True

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass
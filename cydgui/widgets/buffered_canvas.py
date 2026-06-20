import uasyncio as asyncio
from cydgui.core.widget import Widget


class BufferedCanvas(Widget):
    """
    Canvas RGB565 com framebuffer local.

    Todo desenho ocorre em RAM e ao final é enviado
    para o display através de uma única chamada:

        renderer.block(...)

    Formato:
        RGB565 Big Endian
        2 bytes por pixel
    """

    __slots__ = (
        "_bg",
        "_border_color",
        "_touchable",
        "_touch_callback",
        "interval_ms",
        "_running",
        "_renderer",
        "_buffer",
        "_view",
        "_color_cache",
    )

    # ---------------------------------------------------------
    # INIT
    # ---------------------------------------------------------

    def __init__(
        self,
        x=0,
        y=0,
        width=100,
        height=100,
        bg=0x0000,
        border_color=None,
        interval_ms=0,
        touchable=False,
        on_touch=None,
    ):

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height
        )

        self._bg = bg
        self._border_color = border_color

        self._touchable = touchable
        self._touch_callback = on_touch

        self.interval_ms = interval_ms
        self._running = False

        self._renderer = None

        size = width * height * 2

        self._buffer = bytearray(size)
        self._view = memoryview(self._buffer)

        self._color_cache = {}

        self.clear(bg)

    # ---------------------------------------------------------
    # COLOR CACHE
    # ---------------------------------------------------------

    def _color_bytes(self, color):

        cache = self._color_cache

        value = cache.get(color)

        if value is None:

            value = bytes((
                (color >> 8) & 0xFF,
                color & 0xFF
            ))

            cache[color] = value

        return value

    # ---------------------------------------------------------
    # RENDERER
    # ---------------------------------------------------------

    @property
    def renderer(self):
        return self._renderer

    def set_renderer(self, renderer):
        self._renderer = renderer

    # ---------------------------------------------------------
    # CLEAR
    # ---------------------------------------------------------

    def clear(self, color=None):

        if color is None:
            color = self._bg

        pixel = self._color_bytes(color)

        row = pixel * self.width

        buf = self._buffer

        row_len = len(row)

        buf[0:row_len] = row

        copied = row_len
        total = len(buf)

        while copied < total:

            chunk = min(copied, total - copied)

            buf[copied:copied + chunk] = buf[0:chunk]

            copied += chunk

    # ---------------------------------------------------------
    # PIXEL
    # ---------------------------------------------------------

    def pixel(self, x, y, color):

        if (
            x < 0
            or y < 0
            or x >= self.width
            or y >= self.height
        ):
            return

        idx = ((y * self.width) + x) * 2

        self._view[idx] = (color >> 8) & 0xFF
        self._view[idx + 1] = color & 0xFF

    # ---------------------------------------------------------
    # HLINE
    # ---------------------------------------------------------

    def hline(self, x, y, w, color):

        if y < 0 or y >= self.height:
            return

        if x < 0:
            w += x
            x = 0

        if x + w > self.width:
            w = self.width - x

        if w <= 0:
            return

        pixel = self._color_bytes(color)

        row = pixel * w

        offset = ((y * self.width) + x) * 2

        self._view[offset:offset + (w * 2)] = row

    # ---------------------------------------------------------
    # VLINE
    # ---------------------------------------------------------

    def vline(self, x, y, h, color):

        if x < 0 or x >= self.width:
            return

        if y < 0:
            h += y
            y = 0

        if y + h > self.height:
            h = self.height - y

        if h <= 0:
            return

        hi = (color >> 8) & 0xFF
        lo = color & 0xFF

        idx = ((y * self.width) + x) * 2

        stride = self.width * 2

        mv = self._view

        for _ in range(h):

            mv[idx] = hi
            mv[idx + 1] = lo

            idx += stride

    # ---------------------------------------------------------
    # LINE
    # ---------------------------------------------------------

    def line(self, x0, y0, x1, y1, color):

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1

        err = dx - dy

        while True:

            self.pixel(x0, y0, color)

            if x0 == x1 and y0 == y1:
                break

            e2 = err << 1

            if e2 > -dy:
                err -= dy
                x0 += sx

            if e2 < dx:
                err += dx
                y0 += sy

    # ---------------------------------------------------------
    # RECT
    # ---------------------------------------------------------

    def rect(self, x, y, w, h, color):

        if w <= 0 or h <= 0:
            return

        self.hline(x, y, w, color)
        self.hline(x, y + h - 1, w, color)

        self.vline(x, y, h, color)
        self.vline(x + w - 1, y, h, color)

    # ---------------------------------------------------------
    # FILL RECT
    # ---------------------------------------------------------

    def fill_rect(self, x, y, w, h, color):

        if (
            w <= 0
            or h <= 0
            or x >= self.width
            or y >= self.height
        ):
            return

        if x < 0:
            w += x
            x = 0

        if y < 0:
            h += y
            y = 0

        if x + w > self.width:
            w = self.width - x

        if y + h > self.height:
            h = self.height - y

        if w <= 0 or h <= 0:
            return

        pixel = self._color_bytes(color)

        row = pixel * w

        stride = self.width * 2
        row_bytes = w * 2

        mv = self._view

        offset = ((y * self.width) + x) * 2

        for _ in range(h):

            mv[offset:offset + row_bytes] = row

            offset += stride

    # ---------------------------------------------------------
    # CIRCLE
    # ---------------------------------------------------------

    def circle(self, cx, cy, r, color):

        x = r
        y = 0

        err = 1 - r

        while x >= y:

            self.pixel(cx + x, cy + y, color)
            self.pixel(cx + y, cy + x, color)

            self.pixel(cx - y, cy + x, color)
            self.pixel(cx - x, cy + y, color)

            self.pixel(cx - x, cy - y, color)
            self.pixel(cx - y, cy - x, color)

            self.pixel(cx + y, cy - x, color)
            self.pixel(cx + x, cy - y, color)

            y += 1

            if err < 0:
                err += (y << 1) + 1
            else:
                x -= 1
                err += ((y - x) << 1) + 1

    # ---------------------------------------------------------
    # BLIT RGB565
    # ---------------------------------------------------------

    def blit(self, x, y, width, height, data):

        if (
            x < 0
            or y < 0
            or x + width > self.width
            or y + height > self.height
        ):
            return

        row_bytes = width * 2

        dst_stride = self.width * 2

        mv = self._view

        for row in range(height):

            src = row * row_bytes

            dst = (
                ((y + row) * self.width + x)
                * 2
            )

            mv[dst:dst + row_bytes] = data[src:src + row_bytes]

    # ---------------------------------------------------------
    # FLUSH
    # ---------------------------------------------------------

    def flush(self):

        if not self._renderer:
            return

        self._renderer.block(
            self.absolute_x,
            self.absolute_y,
            self.absolute_x + self.width - 1,
            self.absolute_y + self.height - 1,
            self._buffer
        )

    # ---------------------------------------------------------
    # DRAW
    # ---------------------------------------------------------

    def draw(self, renderer):

        if not self.visible:
            return

        self._renderer = renderer

        self.clear(self._bg)

        if self._border_color is not None:

            self.rect(
                0,
                0,
                self.width,
                self.height,
                self._border_color
            )

        self.on_draw()

        self.flush()

        self.validate()

    # ---------------------------------------------------------
    # OVERRIDE
    # ---------------------------------------------------------

    def on_draw(self):
        pass

    # ---------------------------------------------------------
    # ASYNC LOOP
    # ---------------------------------------------------------

    async def start(self):

        if self._running:
            return

        self._running = True

        while self._running:

            await self.update_async()

            self.invalidate()

            await asyncio.sleep_ms(self.interval_ms)

    def stop(self):
        self._running = False

    async def update_async(self):
        pass

    # ---------------------------------------------------------
    # DESTROY
    # ---------------------------------------------------------

    def destroy(self):

        self._running = False

        self._touch_callback = None
        self._renderer = None

        self._buffer = None
        self._view = None

        self._color_cache.clear()

        super().destroy()
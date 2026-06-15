import uasyncio as asyncio
from math import sin, cos, radians
from cydgui.core.async_widget import AsyncWidget


class AsyncCanvas(AsyncWidget):
    """
    Canvas híbrido:
    - mantém compatibilidade com Canvas (draw_callback)
    - adiciona loop async opcional
    - não quebra Container pipeline
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 100,
        bg: int = 0x0000,
        border_color: int | None = None,
        touchable: bool = False,
        on_touch=None,
        on_draw=None,
        interval_ms: int = 0,
    ) -> None:

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            interval_ms=interval_ms
        )

        self._bg = bg
        self._border_color = border_color

        self._touchable = touchable
        self._touch_callback = on_touch

        # compat com Canvas original
        self._draw_callback = on_draw

        self._renderer = None

    # ---------------------------------------------------------
    # Renderer binding
    # ---------------------------------------------------------

    @property
    def renderer(self):
        return self._renderer

    def set_renderer(self, renderer) -> None:
        self._renderer = renderer

    # ---------------------------------------------------------
    # Touch (igual Canvas estável)
    # ---------------------------------------------------------

    def on_touch(self, event) -> bool:
        if not self._touchable:
            return False

        if not self.contains(event.x, event.y):
            return False

        if callable(self._touch_callback):
            self._touch_callback(event)

        return True

    # ---------------------------------------------------------
    # DRAW PRINCIPAL (UNIFICAÇÃO COM CANVAS ESTÁVEL)
    # ---------------------------------------------------------

    def draw(self, renderer) -> None:
        if not self.visible:
            return

        self._renderer = renderer

        ax = self.absolute_x
        ay = self.absolute_y

        # fundo
        renderer.fill_rect(ax, ay, self.width, self.height, self._bg)

        # borda
        if self._border_color is not None:
            renderer.draw_rect(ax, ay, self.width, self.height, self._border_color)

        # callback de desenho (MESMA API DO Canvas)
        if callable(self._draw_callback):
            self._draw_callback(self)

        self.validate()

    # ---------------------------------------------------------
    # Async hook (NOVO - opcional)
    # ---------------------------------------------------------

    async def update_async(self):
        """
        Override opcional.
        Usado para animações (não substitui draw).
        """
        pass

    # ---------------------------------------------------------
    # Primitivas de desenho (iguais Canvas)
    # ---------------------------------------------------------

    def draw_pixel(self, x, y, color):
        if self._renderer:
            self._renderer.draw_pixel(
                self.absolute_x + x,
                self.absolute_y + y,
                color
            )

    def draw_line(self, x1, y1, x2, y2, color):
        if self._renderer:
            self._renderer.draw_line(
                self.absolute_x + x1,
                self.absolute_y + y1,
                self.absolute_x + x2,
                self.absolute_y + y2,
                color
            )

    def draw_rect(self, x, y, w, h, color, filled=False):
        if not self._renderer:
            return

        ax = self.absolute_x + x
        ay = self.absolute_y + y

        if filled:
            self._renderer.fill_rect(ax, ay, w, h, color)
        else:
            self._renderer.draw_rect(ax, ay, w, h, color)

    def draw_circle(self, x, y, r, color, filled=False):
        if not self._renderer:
            return

        ax = self.absolute_x + x
        ay = self.absolute_y + y

        if filled:
            self._renderer.fill_circle(ax, ay, r, color)
        else:
            self._renderer.draw_circle(ax, ay, r, color)

    def draw_text(self, x, y, text, color=0xFFFF):
        if self._renderer:
            self._renderer.draw_text(
                self.absolute_x + x,
                self.absolute_y + y,
                text,
                color
            )

    def draw_arc(self, cx, cy, radius, start_angle, end_angle, color, step=6):
        if not self._renderer:
            return

        prev = None
        angle = start_angle

        while angle <= end_angle:
            x = int(cx + cos(radians(angle)) * radius)
            y = int(cy + sin(radians(angle)) * radius)

            if prev is not None:
                self.draw_line(prev[0], prev[1], x, y, color)

            prev = (x, y)
            angle += step

    # ---------------------------------------------------------
    # Compat cleanup
    # ---------------------------------------------------------

    def clear(self):
        self._draw_callback = None
        self.invalidate()
import uasyncio as asyncio
from cydgui.core.widget import Widget


class AsyncCanvas(Widget):
    """
    Canvas híbrido:
    - compatível com Canvas (draw(renderer))
    - adiciona loop async opcional
    - mantém pipeline do Container intacto
    """

    __slots__ = (
        "_bg",
        "_border_color",
        "_touchable",
        "_touch_callback",
        "interval_ms",
        "_running",
        "_renderer",
        "_draw_callback",
    )

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 100,
        bg: int = 0x0000,
        border_color: int | None = None,
        interval_ms: int = 0,
        touchable: bool = False,
        on_touch=None,
        on_draw=None
    ) -> None:

        super().__init__(x=x, y=y, width=width, height=height)

        self._bg = bg
        self._border_color = border_color

        self._touchable = touchable
        self._touch_callback = on_touch

        self.interval_ms = interval_ms
        self._running = False

        self._renderer = None
        
        self._draw_callback = on_draw

    # ---------------------------------------------------------
    # Renderer
    # ---------------------------------------------------------

    @property
    def renderer(self):
        return self._renderer

    def set_renderer(self, renderer) -> None:
        self._renderer = renderer

    # ---------------------------------------------------------
    # DRAW (OBRIGATÓRIO - igual Canvas)
    # ---------------------------------------------------------

    def draw(self, renderer) -> None:
        if not self.visible:
            return

        self._renderer = renderer

        ax = self.absolute_x
        ay = self.absolute_y

        renderer.fill_rect(ax, ay, self.width, self.height, self._bg)

        if self._border_color is not None:
            renderer.draw_rect(ax, ay, self.width, self.height, self._border_color)

        self.on_draw()

        self.validate()

    # ---------------------------------------------------------
    # Hook de desenho (substitui on_draw callback)
    # ---------------------------------------------------------

    def on_draw(self):
        """Override em subclasses."""
        pass

    # ---------------------------------------------------------
    # Async loop
    # ---------------------------------------------------------

    async def start(self):
        self._running = True
        while self._running:
            await self.update_async()
            self.invalidate()
            await asyncio.sleep_ms(self.interval_ms)

    def stop(self):
        self._running = False

    async def update_async(self):
        """Override opcional"""
        pass

    # ---------------------------------------------------------
    # Primitivas
    # ---------------------------------------------------------

    def draw_line(self, x1, y1, x2, y2, color):
        if self._renderer:
            self._renderer.draw_line(
                self.absolute_x + x1,
                self.absolute_y + y1,
                self.absolute_x + x2,
                self.absolute_y + y2,
                color
            )

    def draw_text(self, x, y, text, color=0xFFFF):
        if self._renderer:
            self._renderer.draw_text(
                self.absolute_x + x,
                self.absolute_y + y,
                text,
                color
            )

    def destroy(self) -> None:
        self._running = False
        self._touch_callback = None
        self._draw_callback = None
        self._renderer = None
        super().destroy()
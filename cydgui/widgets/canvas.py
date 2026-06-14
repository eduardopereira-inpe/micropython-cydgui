from math import sin, cos, radians
from cydgui.core.widget import Widget

class Canvas(Widget):
    """
    Canvas otimizado em Modo Imediato.
    Compatível com a árvore de renderização e ciclo de vida do Container.
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 100,
        bg: int = 0x0000,
        border_color: int|None = None,
        touchable: bool = False,
        on_touch=None,
        on_draw=None,
    ) -> None:
        super().__init__(x=x, y=y, width=width, height=height)
        self._bg = bg
        self._border_color = border_color
        
        # Infraestrutura de Toque
        self._touchable = touchable
        self._touch_callback = on_touch
        
        # Infraestrutura de Desenho (Callback imediato)
        self._draw_callback = on_draw
        self._renderer = None

    # ------------------------------------------------------------------
    # Gerenciamento do Renderer (Injetado pelo Container)
    # ------------------------------------------------------------------

    @property
    def renderer(self):
        """Expõe a propriedade para o hasattr(child, 'renderer') do Container."""
        return self._renderer

    def set_renderer(self, renderer) -> None:
        """Define o renderizador físico ativo."""
        self._renderer = renderer

    # ------------------------------------------------------------------
    # Sistema de Toque
    # ------------------------------------------------------------------

    @property
    def touchable(self) -> bool:
        return self._touchable

    def set_touchable(self, value: bool) -> None:
        self._touchable = value

    def on_touch(self, event) -> bool:
        if not self._touchable:
            return False

        if not self.contains(event.x, event.y):
            return False

        if callable(self._touch_callback):
            self._touch_callback(event)

        return True

    # ------------------------------------------------------------------
    # Renderização Única (Immediate Mode)
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        """Método principal chamado pelo Container para desenhar o Widget."""
        if not self.visible:
            return

        # Garante o sincronismo do renderer local
        self._renderer = renderer
        
        ax = self.absolute_x
        ay = self.absolute_y

        # 1. Desenha o Fundo do Canvas
        renderer.fill_rect(ax, ay, self.width, self.height, self._bg)

        # 2. Desenha a Borda (se configurada)
        if self._border_color is not None:
            renderer.draw_rect(ax, ay, self.width, self.height, self._border_color)

        # 3. Executa o desenho estático do usuário (Modo Imediato)
        if callable(self._draw_callback):
            self._draw_callback(self)

        self.validate()

    # ------------------------------------------------------------------
    # API de Desenho (Protegida contra chamadas prematuras)
    # ------------------------------------------------------------------

    def draw_pixel(self, x: int, y: int, color: int) -> None:
        if self._renderer is None: return
        self._renderer.draw_pixel(self.absolute_x + x, self.absolute_y + y, color)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
        if self._renderer is None: return
        self._renderer.draw_line(
            self.absolute_x + x1, self.absolute_y + y1,
            self.absolute_x + x2, self.absolute_y + y2, color
        )

    def draw_rect(self, x: int, y: int, w: int, h: int, color: int, filled: bool = False) -> None:
        if self._renderer is None: return
        ax, ay = self.absolute_x + x, self.absolute_y + y
        if filled:
            self._renderer.fill_rect(ax, ay, w, h, color)
        else:
            self._renderer.draw_rect(ax, ay, w, h, color)

    def draw_circle(self, x: int, y: int, r: int, color: int, filled: bool = False) -> None:
        if self._renderer is None: return
        ax, ay = self.absolute_x + x, self.absolute_y + y
        if filled:
            self._renderer.fill_circle(ax, ay, r, color)
        else:
            self._renderer.draw_circle(ax, ay, r, color)

    def draw_text(self, x: int, y: int, text: str, color: int = 0xFFFF) -> None:
        if self._renderer is None: return
        self._renderer.draw_text(self.absolute_x + x, self.absolute_y + y, text, color)

    def draw_arc(self, cx: int, cy: int, radius: int, start_angle: int, end_angle: int, color: int, step: int = 6) -> None:
        if self._renderer is None: return
        previous = None
        angle = start_angle
        while angle <= end_angle:
            x = int(cx + cos(radians(angle)) * radius)
            y = int(cy + sin(radians(angle)) * radius)
            if previous is not None:
                self.draw_line(previous[0], previous[1], x, y, color)
            previous = (x, y)
            angle += step

    def clear(self) -> None:
        """Desvincula o desenho e força a limpeza na próxima renderização."""
        self._draw_callback = None
        self.invalidate()

    def __repr__(self) -> str:
        return f"Canvas(x={self.x}, y={self.y}, width={self.width}, height={self.height})"
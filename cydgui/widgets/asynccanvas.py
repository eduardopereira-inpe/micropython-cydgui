import uasyncio as asyncio
from math import sin, cos, radians
from cydgui.core.widget import Widget

class AsyncCanvas(Widget):
    """Canvas otimizado para animações e modo imediato usando uasyncio."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 100,
        bg: int = 0x0000,
        border_color: int = None,
        touchable: bool = False,
        on_touch=None,
    ) -> None:
        super().__init__(x=x, y=y, width=width, height=height)
        
        self._bg = bg
        self._border_color = border_color
        self._touchable = touchable
        self._touch_callback = on_touch
        
        # Referência do renderer guardada na inicialização ou no primeiro ciclo
        self._renderer = None
        
        # Callback para o usuário programar a lógica da animação externa
        self._animation_loop = None
        self._anim_task = None

    def set_renderer(self, renderer) -> None:
        """Define o renderizador físico (necessário para modo imediato)."""
        self._renderer = renderer

    # ------------------------------------------------------------------
    # API de Desenho Direto (Modo Imediato)
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Limpa o canvas instantaneamente com a cor de fundo."""
        if self._renderer:
            self._renderer.fill_rect(
                self.absolute_x, self.absolute_y, 
                self.width, self.height, self._bg
            )

    def draw_pixel(self, x: int, y: int, color: int) -> None:
        if self._renderer:
            self._renderer.draw_pixel(self.absolute_x + x, self.absolute_y + y, color)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
        if self._renderer:
            self._renderer.draw_line(
                self.absolute_x + x1, self.absolute_y + y1,
                self.absolute_x + x2, self.absolute_y + y2, color
            )

    def draw_rect(self, x: int, y: int, w: int, h: int, color: int, filled: bool = False) -> None:
        if self._renderer:
            ax, ay = self.absolute_x + x, self.absolute_y + y
            if filled:
                self._renderer.fill_rect(ax, ay, w, h, color)
            else:
                self._renderer.draw_rect(ax, ay, w, h, color)

    def draw_circle(self, x: int, y: int, r: int, color: int, filled: bool = False) -> None:
        if self._renderer:
            ax, ay = self.absolute_x + x, self.absolute_y + y
            if filled:
                self._renderer.fill_circle(ax, ay, r, color)
            else:
                self._renderer.draw_circle(ax, ay, r, color)

    def draw_text(self, x: int, y: int, text: str, color: int = 0xFFFF) -> None:
        if self._renderer:
            self._renderer.draw_text(self.absolute_x + x, self.absolute_y + y, text, color)

    def draw_arc(self, cx: int, cy: int, radius: int, start_angle: int, end_angle: int, color: int, step: int = 6) -> None:
        """Desenho de arco otimizado (calcula e plota direto)."""
        previous = None
        angle = start_angle
        while angle <= end_angle:
            x = int(cx + cos(radians(angle)) * radius)
            y = int(cy + sin(radians(angle)) * radius)
            if previous is not None:
                self.draw_line(previous[0], previous[1], x, y, color)
            previous = (x, y)
            angle += step

    # ------------------------------------------------------------------
    # Infraestrutura Async para Animações
    # ------------------------------------------------------------------

    def start_animation(self, loop_coroutine, fps: int = 30) -> None:
        """Inicia um loop de animação assíncrono."""
        self.stop_animation()
        self._animation_loop = loop_coroutine
        self._anim_task = asyncio.create_task(self._run_animation(fps))

    def stop_animation(self) -> None:
        """Para a animação atual."""
        if self._anim_task:
            self._anim_task.cancel()
            self._anim_task = None

    async def _run_animation(self, fps: int) -> None:
        """Gerenciador interno do frame-rate da animação."""
        delay = int(1000 / fps)
        try:
            while True:
                if self._animation_loop:
                    # Executa a lógica e desenhos do usuário para este frame
                    await self._animation_loop(self)
                
                # Cede o controle para outras tarefas e dita o FPS
                await asyncio.sleep_ms(delay)
        except asyncio.CancelledError:
            pass

    # ------------------------------------------------------------------
    # Sistema de UI Convencional (Fallback Estático)
    # ------------------------------------------------------------------

    def draw(self, renderer) -> None:
        """Mantido para compatibilidade com a árvore de renderização do cydgui."""
        if not self._renderer:
            self._renderer = renderer
            
        if not self.visible:
            return
            
        # Desenha fundo e bordas básicos se não estiver rodando animação ativa
        if not self._anim_task:
            renderer.fill_rect(self.absolute_x, self.absolute_y, self.width, self.height, self._bg)
            if self._border_color is not None:
                renderer.draw_rect(self.absolute_x, self.absolute_y, self.width, self.height, self._border_color)
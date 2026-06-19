import time
from cydgui.core.async_widget import AsyncWidget
from cydgui.utils.colors import Colors

class ClockWidget(AsyncWidget):
    """Live clock widget updated asynchronously."""

    __slots__ = (
        "_text",
        "_color",
        "_bg_color",
        "_font",
        "_align",
    )

    LEFT = 0
    CENTER = 1
    RIGHT = 2

    # REMOVIDAS as variáveis estáticas (x, y, width, height) que quebravam o Rect do Widget

    def __init__(self, x, y, width=80, height=20, 
                 color=Colors.WHITE,
                 bg_color=0x0000,  
                 font=None,
                 align: int = LEFT):

        
        self._text = "00:00:00"
        self._color = color
        self._bg_color = bg_color 
        self._font = font
        self._align = align
        
        super().__init__(
            interval_ms=1000,
            x=x, y=y, width=width, height=height
        )

        

    async def update_async(self):
        """Atualiza apenas o texto periodicamente."""
        t = time.localtime()
        self._text = "{:02d}:{:02d}:{:02d}".format(t[3], t[4], t[5])

    # O método start() foi removido pois a classe pai AsyncWidget agora gerencia isso perfeitamente!

    def draw(self, renderer) -> None:
        """Draw label."""
        if not self.visible:
            return
        
        # 1. Limpa APENAS a área deste widget usando a cor de fundo definida
        renderer.fill_rect(
            self.absolute_x, 
            self.absolute_y, 
            self.width, 
            self.height, 
            self._bg_color
        )

        # 2. Calcula as dimensões do texto para o alinhamento
        text_w, text_h = renderer.text_size(
            self._text,
            self._font
        )

        draw_x = self.absolute_x

        if self._align == self.CENTER:
            draw_x += (self.width - text_w) // 2
        elif self._align == self.RIGHT:
            draw_x += (self.width - text_w)

        draw_y = self.absolute_y + ((self.height - text_h) // 2)

        # 3. Desenha o texto atualizado por cima da área limpa
        renderer.draw_text(
            x=draw_x,
            y=draw_y,
            text=self._text,
            color=self._color,
            font=self._font
        )

        self.validate()
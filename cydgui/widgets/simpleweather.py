import uasyncio as asyncio
import time
from cydgui.core.async_widget import AsyncWidget
from cydgui.utils.colors import Colors
from cydgui.utils.tools import get_weather_by_coords


class WeatherWidget(AsyncWidget):
    """
    Widget de clima em tempo real atualizado assincronamente.
    Exibe a cidade, temperatura e descrição das condições.
    """

    LEFT = 0
    CENTER = 1
    RIGHT = 2

    def __init__(self, x, y, lat, lon, api_key,
                 width=120, height=80, 
                 color=Colors.WHITE,
                 bg_color=0x0000,  
                 font_title=None,
                 font_temp=None,
                 font_desc=None,
                 align: int = CENTER,
                 interval_minutes=15): # Atualiza a cada 15 minutos por padrão

        # Repassa a geometria para o AsyncWidget. 
        # Convertendo minutos para milissegundos para o loop async.
        super().__init__(
            interval_ms=interval_minutes * 60 * 1000,
            x=x, y=y, width=width, height=height
        )

        self.lat = lat
        self.lon = lon
        self.api_key = api_key

        # Estado inicial visual
        self._local = "Carregando..."
        self._temp = "--"
        self._desc = ""
        
        # Estilização
        self._color = color
        self._bg_color = bg_color 
        self._font_title = font_title
        self._font_temp = font_temp
        self._font_desc = font_desc
        self._align = align

    async def update_async(self):
        """
        Busca os dados de clima e atualiza o estado do widget.
        Nota: urequests é síncrono, então a interface pode ter um micro-congelamento
        durante o download HTTP. Como é a cada 15 min, o impacto é mínimo.
        """
        self._log("Atualizando dados do clima...")
        
        # Usamos a função que criamos anteriormente
        clima = get_weather_by_coords(self.lat, self.lon, self.api_key)
        
        if clima and clima["sucesso"]:
            self._local = clima["local"]
            self._temp = f"{clima['temp']:.1f}°C"
            self._desc = clima["descricao"]
        else:
            self._local = "Erro API"
            self._temp = "--"
            self._desc = "Verifique a rede"

    def _get_aligned_x(self, renderer, text, font):
        """Função auxiliar para calcular a posição X baseada no alinhamento"""
        text_w, _ = renderer.text_size(text, font)
        draw_x = self.absolute_x

        if self._align == self.CENTER:
            draw_x += (self.width - text_w) // 2
        elif self._align == self.RIGHT:
            draw_x += (self.width - text_w)
            
        return draw_x

    def draw(self, renderer) -> None:
        """Desenha a interface do widget"""
        if not self.visible:
            return
        
        # 1. Fundo do Widget (Background)
        renderer.fill_rect(
            self.absolute_x, 
            self.absolute_y, 
            self.width, 
            self.height, 
            self._bg_color
        )

        # Divisão da altura para os 3 elementos (Cidade, Temperatura, Descrição)
        padding_y = 5
        current_y = self.absolute_y + padding_y

        # 2. Desenha o Nome da Cidade (Topo)
        x_local = self._get_aligned_x(renderer, self._local, self._font_title)
        renderer.draw_text(
            x=x_local,
            y=current_y,
            text=self._local,
            color=self._color,
            font=self._font_title
        )
        
        _, h_title = renderer.text_size(self._local, self._font_title)
        current_y += h_title + padding_y

        # 3. Desenha a Temperatura (Centro - Em destaque)
        x_temp = self._get_aligned_x(renderer, self._temp, self._font_temp)
        renderer.draw_text(
            x=x_temp,
            y=current_y,
            text=self._temp,
            color=self._color,
            font=self._font_temp
        )
        
        _, h_temp = renderer.text_size(self._temp, self._font_temp)
        current_y += h_temp + padding_y

        # 4. Desenha a Descrição (Rodapé)
        x_desc = self._get_aligned_x(renderer, self._desc, self._font_desc)
        renderer.draw_text(
            x=x_desc,
            y=current_y,
            text=self._desc,
            color=self._color,  # Você pode passar uma cor secundária aqui se quiser
            font=self._font_desc
        )

        self.validate()
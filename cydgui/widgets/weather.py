import gc
import uasyncio as asyncio
from cydgui.widgets.async_canvas import AsyncCanvas  
from cydgui.utils.colors import Colors
from cydgui.utils.tools import get_weather_by_coords, remove_acentos
from math import sin, cos, radians

class WeatherWidget(AsyncCanvas):
    """
    Widget de clima inspirado em painéis modernos, usando layout de grid em modo imediato.
    """
    def __init__(self, x, y, width, height, lat, lon, api_key, bg_color=Colors.NAVY, interval_minutes=15, **kwargs):
        super().__init__(
            x=x, y=y, width=width, height=height, 
            interval_ms=interval_minutes * 60 * 1000, 
            bg=bg_color, 
            **kwargs
        )
        self.lat = lat
        self.lon = lon
        self.api_key = api_key
        
        # Estado inicial expandido para o grid
        self._local = "Carregando"
        self._temp = "--"
        self._feels_like = "--"
        self._desc = ""
        self._humidity = "--"
        self._wind = "--"
        self._pressure = "--"
        self._visibility = "--"
        self._weather_id = 0
        
    async def update_async(self):
        """Busca e atualiza todos os dados do clima"""
        gc.collect()
        clima = get_weather_by_coords(self.lat, self.lon, self.api_key)
        gc.collect()
        
        if clima and clima.get("sucesso"):
            self._local = remove_acentos(clima["local"])
            print(remove_acentos(clima["descricao"]))
            
            # Formatação sem decimais para ficar com visual mais "limpo" igual a imagem
            self._temp = f"{clima.get('temp', 0):.0f}C"
            self._feels_like = f"Sens: {clima.get('sensacao', 0):.0f}C"
            
            # Dados do Grid
            self._humidity = f"{clima.get('umidade', 0)}%"
            self._wind = f"{clima.get('vento', 0)}m/s"
            self._pressure = f"{clima.get('pressao', 0)}hPa"
            self._visibility = f"{clima.get('visibilidade', 0):.0f}km"
            
            self._weather_id = clima.get("id", 803)
        else:
            self._local = "Erro API"
            self._desc = "Verifique a rede"
            self._weather_id = 0
            
        del clima
        gc.collect()
        

    # ---------------------------------------------------------
    # DESENHO DOS ÍCONES (Mantidos da versão anterior)
    # ---------------------------------------------------------
    def _draw_sun(self, cx, cy, radius, color):
        if not self.renderer: return
        self.renderer.fill_circle(cx, cy, radius, color)
        ray_length = radius + 6
        for angle in range(0, 360, 45):
            x1 = int(cx + cos(radians(angle)) * (radius + 2))
            y1 = int(cy + sin(radians(angle)) * (radius + 2))
            x2 = int(cx + cos(radians(angle)) * ray_length)
            y2 = int(cy + sin(radians(angle)) * ray_length)
            self.renderer.draw_line(x1, y1, x2, y2, color)

    def _draw_cloud(self, cx, cy, color):
        if not self.renderer: return
        self.renderer.fill_circle(cx, cy, 12, color)          
        self.renderer.fill_circle(cx - 12, cy + 4, 8, color)  
        self.renderer.fill_circle(cx + 12, cy + 4, 8, color)  
        self.renderer.fill_rect(cx - 12, cy + 4, 24, 8, color) 

    def _draw_rain(self, cx, cy, color_cloud, color_rain):
        if not self.renderer: return
        self._draw_cloud(cx, cy - 5, color_cloud)
        for i in range(-10, 15, 8):
            self.renderer.draw_line(cx + i, cy + 10, cx + i - 3, cy + 18, color_rain)

    # ---------------------------------------------------------
    # NOVO: DESENHO DOS CARDS DO GRID
    # ---------------------------------------------------------
    def _draw_card(self, ax, ay, x, y, w, h, title, value):
        if not self.renderer: return
        # Cor de fundo do card (Um tom diferente para dar contraste)
        # O MicroPython aceita códigos de cor RGB565 direto. Ex: 0x2124 (Cinza escuro)
        CARD_BG = 0x2965 # Cinza/Azul leve
        
        # Preenche o retângulo do card
        self.renderer.fill_rect(ax + x, ay + y, w, h, CARD_BG)
        # Borda muito sutil
        self.renderer.draw_rect(ax + x, ay + y, w, h, Colors.DARK_GRAY)
        
        # Título (menor/cinza) - Centralizado "no olho" baseado em 8px por letra
        self.renderer.draw_text(ax + x + 5, ay + y + 5, title, Colors.LIGHT_GRAY)
        # Valor (branco/destaque)
        self.renderer.draw_text(ax + x + 5, ay + y + 20, value, Colors.WHITE)

    # ---------------------------------------------------------
    # RENDERIZAÇÃO DO LAYOUT PRINCIPAL
    # ---------------------------------------------------------
    def on_draw(self):
        ax = self.absolute_x
        ay = self.absolute_y
        
        if not self.renderer: return

        # === 1. PARTE SUPERIOR (Destaque Principal) ===
        
        # Temperatura (Grande, lado esquerdo)
        self.renderer.draw_text(ax + 10, ay + 15, self._temp, Colors.WHITE)
        
        # Ícone (Centro-Esquerda)
        icon_cx = ax + 85
        icon_cy = ay + 20
        if self._weather_id == 800:
            self._draw_sun(icon_cx, icon_cy, 10, Colors.YELLOW)
        elif 801 <= self._weather_id <= 804:
            self._draw_cloud(icon_cx, icon_cy, Colors.WHITE)
        elif 200 <= self._weather_id < 600:
            self._draw_rain(icon_cx, icon_cy, Colors.WHITE, Colors.CYAN)
        else:
            self._draw_cloud(icon_cx, icon_cy, Colors.DARK_GRAY)

        # Descrição e Sensação (Lado Direito)
        self.renderer.draw_text(ax + 115, ay + 10, self._desc, Colors.WHITE)
        self.renderer.draw_text(ax + 115, ay + 25, self._feels_like, Colors.LIGHT_GRAY)

        # Linha separadora discreta
        self.renderer.draw_line(ax + 10, ay + 50, ax + self.width - 10, ay + 50, Colors.DARK_GRAY)

        # === 2. PARTE INFERIOR (Grid de Cards) ===
        
        # Geometria do Grid: 2 Colunas x 2 Linhas
        pad = 10
        card_w = (self.width - (pad * 3)) // 2  # Divide o espaço em 2 colunas
        card_h = 35                             # Altura do card
        
        col1_x = pad
        col2_x = pad + card_w + pad
        
        row1_y = 60
        row2_y = 60 + card_h + pad

        # Desenha os 4 Cards de dados
        self._draw_card(ax, ay, col1_x, row1_y, card_w, card_h, "Vento", self._wind)
        self._draw_card(ax, ay, col2_x, row1_y, card_w, card_h, "Umid.", self._humidity)
        
        self._draw_card(ax, ay, col1_x, row2_y, card_w, card_h, "Pressao", self._pressure)
        self._draw_card(ax, ay, col2_x, row2_y, card_w, card_h, "Visib.", self._visibility)
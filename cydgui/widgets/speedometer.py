import math
from .async_canvas import AsyncCanvas
from cydgui.utils.colors import Colors


class SpeedometerWidget(AsyncCanvas):
    """
    Widget de velocímetro radial (meio círculo).
    Visual aprimorado com ponteiro espesso, zonas de cor e eixo central.
    """

    def __init__(self, min_val=0, max_val=100, interval_ms=50, **kwargs):
        super().__init__(interval_ms=interval_ms, **kwargs)

        self.min_val = min_val
        self.max_val = max_val
        self.value = min_val
        
        # Variáveis exclusivas para a simulação de movimento
        self._step = 2

    # ---------------------------------------------------------
    # UPDATE (async state)
    # ---------------------------------------------------------

    async def update_async(self):
        # Simulação: faz o ponteiro ir e voltar
        self.value += self._step
        if self.value >= self.max_val or self.value <= self.min_val:
            self._step *= -1

    # ---------------------------------------------------------
    # DRAW (Estética Aprimorada)
    # ---------------------------------------------------------

    def on_draw(self):
        w = self.width
        h = self.height
        
        # Centro deslocado para cima para deixar margem inferior para o texto
        cx = w // 2
        cy = h - 20 
        r = min(w // 2, h) - 15 
        
        # Definição de Cores
        COR_TEXTO = Colors.WHITE if hasattr(Colors, 'WHITE') else 0xFFFF
        COR_PONTEIRO = Colors.RED if hasattr(Colors, 'RED') else 0xF800
        COR_BASE = Colors.DARK_GRAY if hasattr(Colors, 'DARK_GRAY') else 0x4208
        COR_BOM = Colors.GREEN if hasattr(Colors, 'GREEN') else 0x07E0
        COR_ALERTA = Colors.YELLOW if hasattr(Colors, 'YELLOW') else 0xFFE0
        COR_PERIGO = Colors.RED if hasattr(Colors, 'RED') else 0xF800

        # -----------------------------------------------------
        # 1. LINHA DE BASE INFERIOR (Visual de sustentação)
        # -----------------------------------------------------
        self.draw_line(cx - r - 5, cy, cx + r + 5, cy, COR_BASE)

        # -----------------------------------------------------
        # 2. ESCALA COM ZONAS DE COR E TICKS PRIMÁRIOS/SECUNDÁRIOS
        # -----------------------------------------------------
        passos_escala = 20  # Aumentei para 20 traços para melhor resolução visual
        for i in range(passos_escala + 1):
            ratio = i / passos_escala
            angle = math.pi - (ratio * math.pi)
            
            # Zonas de cor (0-60% Verde, 60-80% Amarelo, 80-100% Vermelho)
            if ratio < 0.6:
                cor_tick = COR_BOM
            elif ratio < 0.8:
                cor_tick = COR_ALERTA
            else:
                cor_tick = COR_PERIGO

            # Intercalando traços maiores e menores
            is_major = (i % 2 == 0)
            t_len = 12 if is_major else 6
            
            tick_r_in = r - t_len
            tick_r_out = r
            
            x1 = cx + int(tick_r_in * math.cos(angle))
            y1 = cy - int(tick_r_in * math.sin(angle))
            x2 = cx + int(tick_r_out * math.cos(angle))
            y2 = cy - int(tick_r_out * math.sin(angle))
            
            self.draw_line(x1, y1, x2, y2, cor_tick)

        # -----------------------------------------------------
        # 3. PONTEIRO ESPESSO (Formato em Triângulo)
        # -----------------------------------------------------
        val_seguro = max(self.min_val, min(self.max_val, self.value))
        val_ratio = (val_seguro - self.min_val) / (self.max_val - self.min_val)
        angle_ponteiro = math.pi - (val_ratio * math.pi)
        
        # Ponta do ponteiro (recuada levemente em relação à escala)
        r_ponteiro = r - 15
        px = cx + int(r_ponteiro * math.cos(angle_ponteiro))
        py = cy - int(r_ponteiro * math.sin(angle_ponteiro))
        
        # Calculando a base ortogonal do triângulo do ponteiro
        base_w = 4 # Espessura para cada lado a partir do centro (total 8px)
        bx1 = cx - int(base_w * math.sin(angle_ponteiro))
        by1 = cy - int(base_w * math.cos(angle_ponteiro))
        bx2 = cx + int(base_w * math.sin(angle_ponteiro))
        by2 = cy + int(base_w * math.cos(angle_ponteiro))

        # Renderizando o "triângulo preenchido" com linhas sequenciais
        linhas_preenchimento = base_w * 2
        for i in range(linhas_preenchimento + 1):
            f = i / linhas_preenchimento
            # Interpolando os pontos na base
            inter_x = bx1 + (bx2 - bx1) * f
            inter_y = by1 + (by2 - by1) * f
            self.draw_line(int(inter_x), int(inter_y), px, py, COR_PONTEIRO)

        # -----------------------------------------------------
        # 4. EIXO CENTRAL (HUB MECÂNICO)
        # -----------------------------------------------------
        # Usamos o _renderer diretamente para acessar o fill_rect
        if self._renderer:
            hub_size = 8
            # Quadrado preenchido base
            self._renderer.fill_rect(
                self.absolute_x + cx - (hub_size // 2), 
                self.absolute_y + cy - (hub_size // 2), 
                hub_size, hub_size, 
                COR_BASE
            )
            # Borda ao redor do quadrado
            self._renderer.draw_rect(
                self.absolute_x + cx - (hub_size // 2), 
                self.absolute_y + cy - (hub_size // 2), 
                hub_size, hub_size, 
                COR_TEXTO
            )

        # -----------------------------------------------------
        # 5. TEXTO DIGITAL ABAIXO DO CENTRO
        # -----------------------------------------------------
        texto = "{:.0f}".format(self.value)
        # Compensação baseada em ~8px por char para tentar centralizar a string
        offset_x = (len(texto) * 8) // 2
        
        # Colocamos o texto abaixo da base de sustentação
        self.draw_text(cx - offset_x, cy + 8, texto, COR_TEXTO)
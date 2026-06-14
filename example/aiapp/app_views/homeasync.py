import uasyncio as asyncio
import gc
from cydgui.core.view import View
from cydgui.widgets.label import Label
from cydgui.widgets.button import Button

# Importamos o seu novo componente otimizado
from cydgui.widgets.async_canvas import AsyncCanvas

# ---------------------------------------------------------
# Cores Globais (Padrão RGB565)
# ---------------------------------------------------------
CYAN       = 0x07FF  
YELLOW     = 0xFFE0  
MAGENTA    = 0xF81F  
WHITE      = 0xFFFF  
GRAY       = 0x4208  
DARK_GRAY  = 0x2104  

async def animacao_logo(logo):
    """
    Corotina que gerencia a animação contínua do logo.
    Roda em segundo plano sem travar os botões ou o touch da View.
    """
    # Inicializa variáveis de estado da animação anexadas à própria função
    if not hasattr(animacao_logo, "passo"):
        animacao_logo.passo = 0
        animacao_logo.onda_raio = 6

    # 1. ATUALIZAÇÃO DA LÓGICA
    animacao_logo.passo += 1
    
    # Faz o raio do Wi-Fi expandir entre 6 e 14 pixels
    animacao_logo.onda_raio += 1
    if animacao_logo.onda_raio > 14:
        animacao_logo.onda_raio = 6

    # Alterna a altura dos pacotes baseada no passo atual (efeito ping-pong)
    y_pacote_esq = 60 - (animacao_logo.passo % 25)
    y_pacote_dir = 30 + (animacao_logo.passo % 25)

    # 2. RENDERIZAÇÃO IMEDIATA (Sem acumular comandos na RAM)
    logo.clear()

    # --- Elementos Estáticos (Grid de Fundo) ---
    for x in range(10, 130, 20):
        for y in range(10, 90, 20):
            logo.draw_pixel(x, y, DARK_GRAY)

    # --- Base Física: Placa CYD ---
    logo.draw_line(65, 50, 35, 65, YELLOW)
    logo.draw_line(35, 65, 65, 80, YELLOW)
    logo.draw_line(65, 80, 95, 65, YELLOW)
    logo.draw_line(95, 65, 65, 50, YELLOW)
    logo.draw_line(35, 65, 35, 73, GRAY)
    logo.draw_line(65, 80, 65, 88, GRAY)
    logo.draw_line(95, 65, 95, 73, GRAY)
    logo.draw_line(35, 73, 65, 88, GRAY)
    logo.draw_line(65, 88, 95, 73, GRAY)
    
    # Chip ESP32
    logo.draw_line(65, 60, 55, 65, YELLOW)
    logo.draw_line(55, 65, 65, 70, YELLOW)
    logo.draw_line(65, 70, 75, 65, YELLOW)
    logo.draw_line(75, 65, 65, 60, YELLOW)

    # Pilares de Comunicação
    logo.draw_line(35, 30, 35, 65, GRAY)
    logo.draw_line(95, 30, 95, 65, GRAY)

    # --- Elementos Dinâmicos/Animados ---
    # Pacotes de dados movendo-se verticalmente nos pilares
    logo.draw_rect(33, y_pacote_esq, 4, 4, WHITE, True)
    logo.draw_rect(93, y_pacote_dir, 4, 4, WHITE, True)

    # --- Tela Flutuante: A GUI ---
    logo.draw_line(65, 15, 35, 30, CYAN)
    logo.draw_line(35, 30, 65, 45, CYAN)
    logo.draw_line(65, 45, 95, 30, CYAN)
    logo.draw_line(95, 30, 65, 15, CYAN)

    # Wireframe interno
    logo.draw_line(65, 20, 45, 30, WHITE)
    logo.draw_line(45, 30, 65, 40, WHITE)
    logo.draw_line(65, 40, 85, 30, WHITE)
    logo.draw_line(85, 30, 65, 20, WHITE)

    # Gráfico de barras (Pode receber um leve balanço se quiser mais animação)
    logo.draw_line(55, 35, 55, 25, MAGENTA)
    logo.draw_line(65, 40, 65, 20, CYAN)
    logo.draw_line(75, 35, 75, 28, YELLOW)

    # Nódulos IoT
    logo.draw_circle(65, 15, 2, WHITE, True)
    logo.draw_circle(35, 30, 2, WHITE, True)
    logo.draw_circle(65, 45, 2, WHITE, True)
    logo.draw_circle(95, 30, 2, WHITE, True)

    # Ondas Wi-Fi Irradiando dinamicamente
    logo.draw_arc(65, 15, animacao_logo.onda_raio, 210, 330, CYAN)
    if animacao_logo.onda_raio > 10:
        logo.draw_arc(65, 15, animacao_logo.onda_raio - 4, 210, 330, CYAN)

    # Tipografia estática
    logo.draw_text(4, 4, "CYD", YELLOW)
    logo.draw_text(104, 4, "GUI", CYAN)


class HomeView(View):
    """Application home screen."""

    def __init__(self, app, parameters=None):
        super().__init__(app, "home", parameters)
        self.logo = None

    # ---------------------------------------------------------
    # Build
    # ---------------------------------------------------------

    def build(self):
        if self.parameters is None:
            self.parameters = {}

        ssid = self.parameters.get("ssid", "-")
        ip = self.parameters.get("ip", "-")
        connected = (ip is not None and ip != "-")
        status = "Connected" if connected else "Disconnected"

        # Buttons e Labels estáticos normais da View
        self.add(Button(x=10, y=10, width=80, height=30, text="WiFi", on_press=self.on_settings))
        self.add(Label(x=0, y=15, width=240, height=20, text="CYDGUI", align=Label.CENTER))
        self.add(Label(x=0, y=38, width=240, height=20, text="Embedded UI Framework", align=Label.CENTER))

        # -----------------------------------------------------
        # Instanciando o novo AsyncCanvas
        # -----------------------------------------------------
        self.logo = AsyncCanvas(
            x=55,
            y=65,
            width=130,
            height=90,
            bg=0x0000,
            touchable=False
        )
        
        # Passa o renderer principal do framework para o modo imediato operar
        # Nota: Ajuste 'self.app.renderer' conforme o nome correto do renderer no cydgui
        if hasattr(self.app, 'renderer'):
            self.logo.set_renderer(self.app.renderer)

        self.add(self.logo)

        # Inicia o loop de animação assíncrona a 20 frames por segundo
        self.logo.start_animation(animacao_logo, fps=20)

        # -----------------------------------------------------
        # Informações adicionais na tela
        # -----------------------------------------------------
        self.add(Label(x=20, y=165, width=200, height=20, text="Status: {}".format(status), align=Label.LEFT))
        self.add(Label(x=20, y=190, width=200, height=20, text="SSID: {}".format(ssid), align=Label.LEFT))
        self.add(Label(x=20, y=215, width=200, height=20, text="IP: {}".format(ip), align=Label.LEFT))
        self.add(Button(x=60, y=260, width=120, height=40, text="Settings", on_press=self.on_settings))

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    def on_settings(self, button):
        # MUITO IMPORTANTE: Para a animação antes de sair da View 
        # para evitar memory leaks ou tarefas órfãs no asyncio
        if self.logo:
            self.logo.stop_animation()

        self.clear()
        gc.collect()
        self.navigate("wifi_scan")
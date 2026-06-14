import gc
from cydgui.core.view import View
from cydgui.widgets.label import Label
from cydgui.widgets.button import Button
from cydgui.widgets.canvas import Canvas

def create_logo(logo: Canvas):
    """
    Atua como o callback de renderização do Canvas.
    Esta função será chamada automaticamente pelo framework toda vez que 
    o componente precisar ser redesenhado na tela, já com o renderer ativo.
    """
    # ---------------------------------------------------------
    # Paleta de Cores (Padrão RGB565)
    # ---------------------------------------------------------
    CYAN       = 0x07FF  # Representa a tela/interface (GUI)
    YELLOW     = 0xFFE0  # Representa a placa (Cheap Yellow Display)
    MAGENTA    = 0xF81F  # Detalhe visual de dados
    WHITE      = 0xFFFF  # Elementos de destaque e nós
    GRAY       = 0x4208  # Estruturas e sombras (Cinza médio)
    DARK_GRAY  = 0x2104  # Fundo sutil (Cinza bem escuro)

    # ---------------------------------------------------------
    # 1. Fundo Tecnológico (Utilizando draw_pixel)
    # ---------------------------------------------------------
    for x in range(10, 130, 20):
        for y in range(10, 90, 20):
            logo.draw_pixel(x, y, DARK_GRAY)

    # ---------------------------------------------------------
    # 2. Base Física: Placa CYD (Utilizando draw_line)
    # ---------------------------------------------------------
    # Face superior da placa
    logo.draw_line(65, 50, 35, 65, YELLOW) # Topo -> Esquerda
    logo.draw_line(35, 65, 65, 80, YELLOW) # Esquerda -> Baixo
    logo.draw_line(65, 80, 95, 65, YELLOW) # Baixo -> Direita
    logo.draw_line(95, 65, 65, 50, YELLOW) # Direita -> Topo

    # Espessura da placa (Efeito 3D extrudado para baixo)
    logo.draw_line(35, 65, 35, 73, GRAY)
    logo.draw_line(65, 80, 65, 88, GRAY)
    logo.draw_line(95, 65, 95, 73, GRAY)
    # Bordas inferiores
    logo.draw_line(35, 73, 65, 88, GRAY)
    logo.draw_line(65, 88, 95, 73, GRAY)

    # Detalhe interno da placa: Chip ESP32 centralizado
    logo.draw_line(65, 60, 55, 65, YELLOW)
    logo.draw_line(55, 65, 65, 70, YELLOW)
    logo.draw_line(65, 70, 75, 65, YELLOW)
    logo.draw_line(75, 65, 65, 60, YELLOW)

    # ---------------------------------------------------------
    # 3. Comunicação IoT: Conexões verticais (Utilizando draw_rect)
    # ---------------------------------------------------------
    logo.draw_line(35, 30, 35, 65, GRAY) # Pilar Esquerdo
    logo.draw_line(95, 30, 95, 65, GRAY) # Pilar Direito

    # Pacotes de dados brancos (Retângulos preenchidos)
    logo.draw_rect(33, 45, 4, 4, WHITE, True) # Pacote subindo na esq.
    logo.draw_rect(93, 50, 4, 4, WHITE, True) # Pacote descendo na dir.

    # ---------------------------------------------------------
    # 4. Tela Flutuante: A GUI (Utilizando draw_line)
    # ---------------------------------------------------------
    logo.draw_line(65, 15, 35, 30, CYAN)
    logo.draw_line(35, 30, 65, 45, CYAN)
    logo.draw_line(65, 45, 95, 30, CYAN)
    logo.draw_line(95, 30, 65, 15, CYAN)

    # Wireframe interno (Painel de conteúdo da GUI)
    logo.draw_line(65, 20, 45, 30, WHITE)
    logo.draw_line(45, 30, 65, 40, WHITE)
    logo.draw_line(65, 40, 85, 30, WHITE)
    logo.draw_line(85, 30, 65, 20, WHITE)

    # Gráfico de barras na GUI
    logo.draw_line(55, 35, 55, 25, MAGENTA) # Barra Esquerda
    logo.draw_line(65, 40, 65, 20, CYAN)    # Barra Central Maior
    logo.draw_line(75, 35, 75, 28, YELLOW)  # Barra Direita Menor

    # ---------------------------------------------------------
    # 5. Nódulos IoT (Utilizando draw_circle)
    # ---------------------------------------------------------
    logo.draw_circle(65, 15, 2, WHITE, True) # Nó Topo
    logo.draw_circle(35, 30, 2, WHITE, True) # Nó Esquerdo
    logo.draw_circle(65, 45, 2, WHITE, True) # Nó Base da tela
    logo.draw_circle(95, 30, 2, WHITE, True) # Nó Direito

    # ---------------------------------------------------------
    # 6. Emissão de Sinal Wi-Fi (Utilizando draw_arc)
    # ---------------------------------------------------------
    logo.draw_arc(65, 15, 6, 210, 330, CYAN)
    logo.draw_arc(65, 15, 10, 210, 330, CYAN)
    logo.draw_arc(65, 15, 14, 210, 330, CYAN)

    # ---------------------------------------------------------
    # 7. Tipografia e Branding (Utilizando draw_text)
    # ---------------------------------------------------------
    logo.draw_text(4, 4, "CYD", YELLOW)
    logo.draw_text(104, 4, "GUI", CYAN)


class HomeView(View):
    """Application home screen."""

    def __init__(self, app, parameters=None):
        super().__init__(app, "home", parameters)

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

        # -----------------------------------------------------
        # WiFi Button
        # -----------------------------------------------------
        self.add(
            Button(
                x=10,
                y=10,
                width=80,
                height=30,
                text="WiFi",
                on_press=self.on_settings
            )
        )

        # -----------------------------------------------------
        # Framework Title
        # -----------------------------------------------------
        self.add(Label(x=0, y=15, width=240, height=20, text="CYDGUI", align=Label.CENTER))
        self.add(Label(x=0, y=38, width=240, height=20, text="Embedded UI Framework", align=Label.CENTER))

        # -----------------------------------------------------
        # Logo Canvas (Configurado com o Callback)
        # -----------------------------------------------------
        logo = Canvas(
            x=55,
            y=65,
            width=130,
            height=90,
            bg=0x0000,
            touchable=False,
            on_draw=create_logo  # <--- Injeta a função de desenho aqui!
        )

        self.add(logo)  # O Container vai gerenciar e disparar o desenho no tempo correto

        # -----------------------------------------------------
        # Connection Information
        # -----------------------------------------------------
        self.add(Label(x=20, y=165, width=200, height=20, text="Status: {}".format(status), align=Label.LEFT))
        self.add(Label(x=20, y=190, width=200, height=20, text="SSID: {}".format(ssid), align=Label.LEFT))
        self.add(Label(x=20, y=215, width=200, height=20, text="IP: {}".format(ip), align=Label.LEFT))

        # -----------------------------------------------------
        # Main Action
        # -----------------------------------------------------
        self.add(
            Button(
                x=60,
                y=260,
                width=120,
                height=40,
                text="Settings",
                on_press=self.on_settings
            )
        )

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    def on_settings(self, button):
        self.clear()
        gc.collect()
        self.navigate("wifi_scan")

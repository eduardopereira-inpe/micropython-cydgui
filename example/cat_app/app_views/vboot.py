import gc
from cydgui.core.view import View
from cydgui.widgets.label import Label
from cydgui.widgets.canvas import Canvas
from cydgui.utils.colors import Colors

from connectivity.wifi import connect_to_wifi, WLAN
from udotenv.dotenv import load_dotenv

from .home import create_logo

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio



class BootView(View):

    __slots__ = (
        "logo",
        "status_label",
        "_startup_task",
    )

    def __init__(self, app, parameters=None):
        super().__init__(app, "boot", parameters)

    def build(self):

        # Título
        self.add(
            Label(
                x=0,
                y=20,
                width=240,
                height=30,
                text="CYDGUI",
                color=Colors.CYAN,
                align=Label.CENTER
            )
        )

        # Subtítulo
        self.add(
            Label(
                x=0,
                y=45,
                width=240,
                height=20,
                text="Embedded IoT Framework",
                color=Colors.WHITE,
                align=Label.CENTER
            )
        )

        # Logo central
        self.logo = Canvas(
            x=55,
            y=75,
            width=130,
            height=90,
            bg=Colors.BLACK,
            touchable=False,
            on_draw=create_logo
        )

        self.add(self.logo)

        # Status
        self.status_label = Label(
            x=0,
            y=180,
            width=240,
            height=20,
            text="Inicializando sistema...",
            color=Colors.YELLOW,
            align=Label.CENTER
        )

        self.add(self.status_label)

        # Barra de progresso (simples)
        self.add(
            Label(
                x=20,
                y=220,
                width=200,
                height=20,
                text="[###############-----]",
                color=Colors.CYAN,
                align=Label.CENTER
            )
        )

        # Versão
        self.add(
            Label(
                x=0,
                y=280,
                width=240,
                height=20,
                text="Firmware v1.0.0",
                color=Colors.GRAY,
                align=Label.CENTER
            )
        )

        # Navega automaticamente após 2 segundos
        self._startup_task = self.app.create_task(self.startup())

    async def startup(self):
        
        self.status_label.text = " "

        await asyncio.sleep_ms(100)

        self.status_label.text = "Conectando Wi-Fi..."
        
        await asyncio.sleep_ms(100)
        
        config = load_dotenv("env.txt")

        SSID = config.get("WIFI_SSID")
        PASSWORD = config.get("WIFI_PASS")
        API_OPENWEATHER = config.get("API_OPENWEATHER")
        
        try:

            connect_to_wifi(ssid=SSID, password=PASSWORD, verbose=True)
            gc.collect()

#             ip, mascara, gateway, dns_antigo = WLAN.ifconfig()
# 
#             # Forçamos a placa a usar o mesmo IP/Gateway, mas com o DNS público do Google (8.8.8.8)
#             WLAN.ifconfig((ip, mascara, gateway, '8.8.8.8'))            
        except Excepition as e:
            print(f"[VBOOT] Error: {e}")
            self.navigate("matrixrain")
            
        
        self.status_label.text = " "

        await asyncio.sleep_ms(1000)

        self.status_label.text = "Carregando modulos..."

        await asyncio.sleep_ms(1000)

        self.navigate("cat")


    def destroy(self):

        if hasattr(self, "_startup_task") and self._startup_task:
            try:
                self._startup_task.cancel()
            except Exception:
                pass
            self._startup_task = None

        super().destroy()

#         self.navigate("home")
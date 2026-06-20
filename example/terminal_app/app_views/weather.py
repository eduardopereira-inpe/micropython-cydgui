import gc
import uasyncio as asyncio
from machine import Pin

from cydgui.core.view import View
from cydgui.widgets.button import Button
from cydgui.widgets.label import Label
from cydgui.widgets.clock_widget import ClockWidget
from cydgui.widgets.weather import WeatherWidget
from cydgui.widgets.crypto import CryptoWidget
from cydgui.utils.constants import Constants
from cydgui.utils.colors import Colors

from cydgui.utils.tools import get_lat_lon_from_my_ip

class WeatherView(View):
    """
    Dashboard interativo para exibição do clima em tempo real.
    Gerencia o ciclo de vida dos widgets assíncronos (Relógio e Clima)
    para evitar memory leaks ao fechar a tela.
    """

    __slots__ = (
        "api_key",
        "clock",
        "_clock_task",
        "crypto",
        "_crypto_task",
        "weather",
        "info",
        "_startup_task",
        "_weather_task",
    )

    def __init__(self, app, parameters=None):
        super().__init__(app, "weather_dashboard", parameters)

    # ---------------------------------------------------------
    # BUILD (Agora super rápido, sem bloqueios de rede!)
    # ---------------------------------------------------------

    def build(self):

        self.parameters = self.parameters or {}
        self.api_key = self.parameters.get("api_key", "SUA_CHAVE_AQUI")

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        self.add(Button(
            x=5,
            y=10,
            width=25,
            height=20,
            text="<",
            on_press=self.on_back
        ))

        self.add(Label(
            x=35,
            y=10,
            width=110,
            height=20,
            text="Tempo",
            align=Label.CENTER
        ))

        self.clock = ClockWidget(
            x=150,
            y=10,
            width=85,
            height=20
        )

        self._clock_task = self.app.create_task(self.clock.start())
        self.add(self.clock)

        # -----------------------------------------------------
        # CRYPTO (MARKET STRIP)
        # -----------------------------------------------------

        crypto_width = 150
        crypto_height = 28

        self.crypto = CryptoWidget(
            x=(Constants.DISPLAY_WIDTH - crypto_width) // 2,
            y=38,
            width=crypto_width,
            height=crypto_height,
            interval_minutes=5,
            bg_color=0x1022  # leve destaque visual
        )

        self._crypto_task = self.app.create_task(self.crypto.start())
        self.add(self.crypto)

        # -----------------------------------------------------
        # WEATHER
        # -----------------------------------------------------

        w_width = 240
        w_height = 150
        w_x = int((Constants.DISPLAY_WIDTH - w_width) / 2)

        self.weather = WeatherWidget(
            x=w_x,
            y=72,  # desce para acomodar crypto strip
            width=w_width,
            height=w_height,
            lat=-23.2237,
            lon=-45.9009,
            api_key=self.api_key,
            bg_color=Colors.NAVY,
            interval_minutes=15
        )

        self.add(self.weather)

        # -----------------------------------------------------
        # FOOTER
        # -----------------------------------------------------

        self.info = Label(
            x=0,
            y=220,
            width=Constants.DISPLAY_WIDTH,
            height=20,
            text="Iniciando...",
            align=Label.CENTER
        )

        self.add(self.info)

        # -----------------------------------------------------
        # STARTUP ASYNC
        # -----------------------------------------------------

        self._startup_task = self.app.create_task(self._startup_routine())
        self._backligh_task = self.app.create_task(self._backlight_run())

    # ---------------------------------------------------------
    # STARTUP ASSÍNCRONO (Busca IP e Inicia o Clima)
    # ---------------------------------------------------------
    
    
    async def _backlight_run(self):
        
        print("Starting Backlight")
        
        is_on = True
        btn = Pin(1, Pin.IN, Pin.PULL_UP)
        backlight = Pin(0, Pin.OUT)
        while True:
            
            if btn.value() == 0:
                if is_on is True:
                    is_on = False
                    backlight.value(0)
                    print("Light off")
                else:
                    is_on = True
                    backlight.value(1)
                    print("Light on")
                
            await asyncio.sleep_ms(500)
            

    async def _startup_routine(self):
        # 1. Dá um fôlego de 100ms para o MicroPython desenhar a interface inteira na tela
        await asyncio.sleep_ms(100)

        # 2. Se as coordenadas não vieram por parâmetro, buscamos pelo IP
        if 'lat' not in self.parameters:
            self.info.text = "Buscando loc. por IP..."
            self.info.invalidate()
            await asyncio.sleep_ms(50) # Atualiza a UI para mostrar a mensagem
            
            try:
                # Mesmo sendo síncrono, a tela já está desenhada, então o usuário vê o aviso
                lat_lon = get_lat_lon_from_my_ip()
                if lat_lon.get('Error') is None:
                    self.weather.lat = lat_lon["Latitude"]
                    self.weather.lon = lat_lon["Longitude"]
            except Exception as e:
                print("Erro ao buscar IP:", e)
        else:
            # Usa o que veio do menu principal
            self.weather.lat = self.parameters.get("lat")
            self.weather.lon = self.parameters.get("lon")

        # Restaura a mensagem do rodapé
        self.info.text = "Atua. via OpenWeatherMap"

        # 3. Agora sim, damos o start() no widget com as coordenadas corretas!
        self._weather_task = self.app.create_task(self.weather.start())

    # ---------------------------------------------------------
    # CLEANUP
    # ---------------------------------------------------------

    def destroy(self):
        # Cancelar a rotina de startup caso o usuário saia muito rápido da tela
        if hasattr(self, "_startup_task") and self._startup_task:
            try:
                self._startup_task.cancel()
            except Exception:
                pass
            self._startup_task = None

        if hasattr(self, "_weather_task") and self._weather_task:
            try:
                self._weather_task.cancel()
            except Exception:
                pass
            self._weather_task = None

        if hasattr(self, "_crypto_task") and self._crypto_task:
            try:
                self._crypto_task.cancel()
            except Exception:
                pass
            self._crypto_task = None

        if hasattr(self, "_clock_task") and self._clock_task:
            try:
                self._clock_task.cancel()
            except Exception:
                pass
            self._clock_task = None

        try:
            self.crypto.stop()
        except Exception:
            pass

        try:
            self.weather.stop()
        except Exception:
            pass

        try:
            self.clock.stop()
        except Exception:
            pass

        super().destroy()

        gc.collect()

    # ---------------------------------------------------------
    # NAV
    # ---------------------------------------------------------

    def on_back(self, button):
        app = self.app

        try:
            self.crypto.stop()
        except Exception:
            pass

        try:
            self.weather.stop()
        except Exception:
            pass

        try:
            self.clock.stop()
        except Exception:
            pass

        if app is not None:
            app.navigate("home")



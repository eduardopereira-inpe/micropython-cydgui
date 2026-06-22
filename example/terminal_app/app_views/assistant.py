import gc

from cydgui.core.view import View
from cydgui.widgets.button import Button
from cydgui.widgets.label import Label
from cydgui.widgets.clock_widget import ClockWidget
from cydgui.widgets.crypto import CryptoWidget
from cydgui.widgets.eye import EyeWidget
from cydgui.widgets.weather import WeatherWidget

from cydgui.utils.tools import get_lat_lon_from_my_ip
from cydgui.utils.constants import Constants
from cydgui.utils.colors import Colors

from cydgui.bl_state import BlState

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


class AssistantView(View):

    __slots__ = (
        "clock",
        "_clock_task",
        "crypto",
        "_crypto_task",
        "eyes",
        "_eyes_task",
        "weather",
        "_weather_task",
        "_startup_task",
        "info",
        "bl_state",
        "_bl_task",
    )

    def __init__(self, app, parameters=None):
        super().__init__(app, "assistant", parameters)

    def build(self):

        self.parameters = self.parameters or {}

        # --------------------------------------------------
        # BACKLIGHT
        # --------------------------------------------------

        self.bl_state = BlState(
            pin_num=Constants.BL_PIN,
            pin_btn=Constants.BL_BTN_PIN
        )

        self._bl_task = self.app.create_task(
            self.bl_state.monitor()
        )

        # --------------------------------------------------
        # HEADER
        # --------------------------------------------------

        self.add(Button(
            x=5,
            y=5,
            width=25,
            height=20,
            text="<",
            on_press=self.on_back
        ))

        self.add(Label(
            x=35,
            y=5,
            width=105,
            height=20,
            text="Assistant",
            align=Label.CENTER
        ))

        self.clock = ClockWidget(
            x=150,
            y=5,
            width=85,
            height=20
        )

        self.add(self.clock)

        self._clock_task = self.app.create_task(
            self.clock.start()
        )

        # --------------------------------------------------
        # CRYPTO
        # --------------------------------------------------

        crypto_width = 150
        crypto_height = 28

        self.crypto = CryptoWidget(
            x=(Constants.DISPLAY_WIDTH - crypto_width) // 2,
            y=32,
            width=crypto_width,
            height=crypto_height,
            interval_minutes=5,
            bg_color=0x1022
        )

        self.add(self.crypto)

        gc.collect()

        self._crypto_task = self.app.create_task(
            self.crypto.start()
        )

        # --------------------------------------------------
        # EYES
        # --------------------------------------------------

        eyes_width = 90
        eyes_height = 50

        self.eyes = EyeWidget(
            x=(Constants.DISPLAY_WIDTH - eyes_width) // 2,
            y=68,
            width=eyes_width,
            height=eyes_height,
            iris_size=16
        )

        self.add(self.eyes)

        self._eyes_task = self.app.create_task(
            self.eyes.update()
        )

        # --------------------------------------------------
        # WEATHER
        # --------------------------------------------------

        weather_width = 230
        weather_height = 150

        self.weather = WeatherWidget(
            x=(Constants.DISPLAY_WIDTH - weather_width) // 2,
            y=125,
            width=weather_width,
            height=weather_height,
            lat=0,
            lon=0,
            api_key=self.parameters.get("api_key"),
            bg_color=Colors.NAVY,
            interval_minutes=15
        )

        self.add(self.weather)

        # --------------------------------------------------
        # FOOTER
        # --------------------------------------------------

        self.info = Label(
            x=0,
            y=295,
            width=Constants.DISPLAY_WIDTH,
            height=20,
            text="Inicializando...",
            align=Label.CENTER
        )

        self.add(self.info)

        # --------------------------------------------------
        # STARTUP
        # --------------------------------------------------

        self._startup_task = self.app.create_task(
            self._startup_routine()
        )

    async def _startup_routine(self):

        await asyncio.sleep_ms(100)

        try:

            if (
                self.parameters.get("lat") is not None
                and self.parameters.get("lon") is not None
            ):

                self.weather.lat = self.parameters.get("lat")
                self.weather.lon = self.parameters.get("lon")

            else:

                self.info.text = "Buscando localizacao..."
                self.info.invalidate()

                await asyncio.sleep_ms(50)

                lat_lon = get_lat_lon_from_my_ip()

                if lat_lon and lat_lon.get("Error") is None:

                    self.weather.lat = lat_lon["Latitude"]
                    self.weather.lon = lat_lon["Longitude"]

        except Exception as e:
            print("Erro localizacao:", e)

        self.info.text = "Atualizado via OpenWeather"
        self.info.invalidate()

        self._weather_task = self.app.create_task(
            self.weather.start()
        )

    def destroy(self):

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

        if hasattr(self, "_eyes_task") and self._eyes_task:
            try:
                self._eyes_task.cancel()
            except Exception:
                pass
            self._eyes_task = None

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

        if hasattr(self, "_bl_task") and self._bl_task:
            try:
                self._bl_task.cancel()
            except Exception:
                pass
            self._bl_task = None

        try:
            self.crypto.stop()
        except Exception:
            pass

        try:
            self.clock.stop()
        except Exception:
            pass

        super().destroy()

        gc.collect()

    def on_back(self, button):

        self.app.navigate("home")
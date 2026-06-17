import micropython
micropython.alloc_emergency_exception_buf(100)

import gc


# Configura o coletor para ser altamente agressivo
gc.threshold(gc.mem_free() // 4)


from connectivity.wifi import connect_to_wifi, WLAN

from cydgui.render.ili9341_renderer import ILI9341Renderer
from cydgui.app import App

from cydgui.driver.tft_touch import TFTTouch
from app_views.home import HomeView
from app_views.terminal import TerminalView
from app_views.memory_graph import MemoryGraphView
from app_views.speeddometer import SpeedometerView
from app_views.weather import WeatherView
from app_views.vboot import BootView
from udotenv.dotenv import load_dotenv

import urequests
import ujson

import uasyncio as asyncio
from cydgui.utils.tools import get_lat_lon_from_my_ip


# ============================================================
# Hardware
# ============================================================

tft_touch = TFTTouch(
    disp_sck=12,
    disp_mosi=11,
    disp_miso=13,
    
    # Pinos de Controle Individuais
    disp_cs=10,
    disp_dc=5,
    disp_rst=4,
    disp_bl=21,
    touch_cs=41,
    touch_int=3, # GPIO 36 não existe no S3 DevKit, mudado para 3
)


display = tft_touch.display
touch = tft_touch.touch

renderer = ILI9341Renderer(display)


# ============================================================
# Application
# ============================================================

gc.collect()
app = App(
    renderer=renderer,
    touch=touch
)

app.route("boot", BootView)
app.route("home", HomeView)
app.route("terminal", TerminalView)
app.route("memory_graph", MemoryGraphView)
app.route("speedometer", SpeedometerView)
app.route("weather_dashboard", WeatherView)


app.navigate("boot")
    
app.run()
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

from udotenv.dotenv import load_dotenv

import urequests
import ujson

import uasyncio as asyncio
from cydgui.utils.tools import get_lat_lon_from_my_ip

config = load_dotenv("env.txt")

API_KEY = config.get("API_KEY")
SSID = config.get("WIFI_SSID")
PASSWORD = config.get("WIFI_PASS")
API_OPENWEATHER = config.get("API_OPENWEATHER")

connect_to_wifi(ssid=SSID, password=PASSWORD, verbose=True)


ip, mascara, gateway, dns_antigo = WLAN.ifconfig()

# Forçamos a placa a usar o mesmo IP/Gateway, mas com o DNS público do Google (8.8.8.8)
WLAN.ifconfig((ip, mascara, gateway, '8.8.8.8'))


if WLAN.isconnected():

    ip = WLAN.ifconfig()[0]
else:
    ip = '-'


gc.collect()

# ============================================================
# Hardware
# ============================================================

tft_touch = TFTTouch()
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

app.route("home", HomeView)
app.route("terminal", TerminalView)
app.route("memory_graph", MemoryGraphView)
app.route("speedometer", SpeedometerView)
app.route("weather_dashboard", WeatherView)
app.navigate("home", parameters={"ssid": SSID, "ip": ip })

gc.collect()
lat_lon = get_lat_lon_from_my_ip()
print(lat_lon)
del lat_lon
gc.collect()

    
app.run()
from connectivity.wifi import WLAN

from cydgui.driver import CYD
from cydgui.render.ili9341_renderer import ILI9341Renderer

from cydgui.app import App

from app_views.home import HomeView
from app_views.wifisettings import WiFiSettingsView
from app_views.wifiscan import WiFiScanView

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
# 
# from connectivity import connect_to_wifi
#    
# connect_to_wifi("RedeGamer", "Vick0508")


# ============================================================
# Hardware
# ============================================================

cyd = CYD()

display = cyd.display
touch = cyd.touch

renderer = ILI9341Renderer(display)


# ============================================================
# Application
# ============================================================

app = App(
    renderer=renderer,
    touch=touch
)

app.route("home", HomeView)
app.route("settings", WiFiSettingsView)
app.route("wifi_scan", WiFiScanView)
app.navigate("home")


app.run()
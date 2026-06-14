import gc
from connectivity.wifi import WLAN

from cydgui.render.ili9341_renderer import ILI9341Renderer
from cydgui.app import App

from app_views.home import HomeView
from app_views.wifisettings import WiFiSettingsView
from app_views.wifiscan import WiFiScanView

# 
from cydgui.driver.tft_touch import TFTTouch



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
app.route("wifi_settings", WiFiSettingsView)
app.route("wifi_scan", WiFiScanView)
app.navigate("home")
gc.collect()

app.run()
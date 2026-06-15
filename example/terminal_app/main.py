import gc
from connectivity.wifi import connect_to_wifi, WLAN

from cydgui.render.ili9341_renderer import ILI9341Renderer
from cydgui.app import App

from cydgui.driver.tft_touch import TFTTouch
from app_views.home import HomeView
from app_views.terminal import TerminalView

from udotenv.dotenv import load_dotenv


config = load_dotenv("env.txt")

API_KEY = config.get("API_KEY")
SSID = config.get("WIFI_SSID")
PASSWORD = config.get("WIFI_PASS")

connect_to_wifi(ssid=SSID, password=PASSWORD, verbose=True)

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

app.navigate("home", parameters={"ssid": SSID, "ip": ip })

gc.collect()

app.run()
import gc
from connectivity.wifi import connect_to_wifi, WLAN

from cydgui.render.ili9341_renderer import ILI9341Renderer
from cydgui.app import App

from cydgui.driver.tft_touch import TFTTouch
from app_views.home import HomeView
from app_views.terminal import TerminalView

from udotenv.dotenv import load_dotenv

gc.collect()
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

tft_touch = TFTTouch(

    disp_sck=6,
    disp_mosi=7,
    disp_miso=5,

    # Display control
    disp_cs=4,
    disp_dc=3,
    disp_rst=2,
    disp_bl=0,
# 
#     # Touch SPI
#     touch_sck=25,
#     touch_mosi=32,
#     touch_miso=39,
# 
#     # Touch control
#     touch_cs=33,
#     touch_int=36,

    # Features
    has_touch=False,

    # Display config
    rotation=0
  

#     disp_sck=12,
#     disp_mosi=11,
#     disp_miso=13,
#     
#     # Pinos de Controle Individuais
#     disp_cs=10,
#     disp_dc=5,
#     disp_rst=4,
#     disp_bl=21,
#     touch_cs=41,
#     touch_int=3, # GPIO 36 não existe no S3 DevKit, mudado para 3
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

app.route("home", HomeView)
app.route("terminal", TerminalView)

app.navigate("home", parameters={"ssid": SSID, "ip": ip })

gc.collect()

app.run()

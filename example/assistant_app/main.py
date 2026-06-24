
# WLAN é um Singleton, criado para economizar memória e evitar heap,
# Fragmentação de memória.

from connectivity.wifi import WLAN


from cydgui.render.ili9341_renderer import ILI9341Renderer
from cydgui.driver.tft_touch import TFTTouch
from cydgui.app import App

from views.assistant import AssistantView
from views.vboot import BootView
 
# Configuração de Hardware 

# Configuração para TFT 2.8 no
# Esp32 -super Mini

tft_touch = TFTTouch(
    disp_sck=6,
    disp_mosi=7,
    disp_miso=5,
    disp_cs=4,
    disp_dc=3,
    disp_rst=2,
    disp_bl=0,
    has_touch=False,
    rotation=0
)



display = tft_touch.display
touch = tft_touch.touch

renderer = ILI9341Renderer(display)


# Instanciando a aplicação
 
gc.collect()

app = App(
    renderer=renderer,
    touch=touch
    )

# Definimos as Rotas

app.route("assistant", AssistantView)
app.route("vboot", BootView)


# Navegamos entre Views.
app.navigate("vboot")

# Executando App
app.run()
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 

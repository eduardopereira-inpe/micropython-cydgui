import micropython
micropython.alloc_emergency_exception_buf(100)

import gc

import uasyncio as asyncio

# Configura o coletor para ser altamente agressivo
gc.threshold(gc.mem_free() // 4)


from cydgui.render.ili9341_renderer import ILI9341Renderer
from cydgui.app import App

from cydgui.driver.tft_touch import TFTTouch
from app_views.home import HomeView
from app_views.terminal import TerminalView
from app_views.memory_graph import MemoryGraphView
from app_views.speeddometer import SpeedometerView
from app_views.weather import WeatherView
from app_views.vboot import BootView


# ============================================================
# Hardware
# ============================================================

# ==============================================================================
# TABELA DE CONEXÕES: ESP32-S3 DEV KIT + TELA TFT 2.8" (COM TOUCH INTEGRADO)
# ==============================================================================
#
# +-------------------+-------------------------+--------------------+---------------------------------------------------------------+
# | Pino da Tela TFT  | Função do Pino          | ESP32-S3 DevKit    | Observações / Alternativas                                    |
# +-------------------+-------------------------+--------------------+---------------------------------------------------------------+
# | VCC               | Alimentação Digital     | 3V3 / 5V           | Verifique se sua tela possui regulador interno para 5V.       |
# | GND               | Terra / Negativo        | GND                | Conecte a qualquer pino GND da placa.                         |
# | CS (Display)      | Chip Select da Tela     | GPIO 10            | Pino de controle do Display (Padrão FSPI SS).                 |
# | RESET / RST       | Reinício da Tela        | GPIO 14            | Pode ser alterado para qualquer pino digital livre.          |
# | DC / RS           | Data / Command          | GPIO 13            | Define se o dado enviado é comando ou imagem.                 |
# | SDI / MOSI        | Linha de Dados SPI      | GPIO 11            | Pino nativo de Hardware SPI (MOSI / FSPI D).                  |
# | SCK / SCL         | Clock do SPI            | GPIO 12            | Pino nativo de Hardware SPI (SCK / FSPI CLK).                 |
# | LED / BL          | Luz de Fundo(Backlight) | GPIO 21            | Permite controle de brilho via código/PWM (ou ligue no 3V3).  |
# | SDO / MISO        | Retorno de Dados SPI    | GPIO 13            | Nota: No S3, DC e MISO compartilham se for SPI de 3 fios.     |
# |                   |                         |                    | Se usar Touch/SD separado, use o GPIO 9 para MISO (FSPI Q).   |
# | T_CLK             | Clock do Touch          | GPIO 12            | Compartilha o mesmo pino GPIO 12 (Barramento SPI).            |
# | T_CS              | Chip Select do Touch    | GPIO 1             | Pino de controle dedicado para ativar a leitura do toque.     |
# | T_DIN             | Entrada de Dados Touch  | GPIO 11            | Compartilha o mesmo pino GPIO 11 (Barramento SPI).            |
# | T_DO              | Saída de Dados Touch    | GPIO 9             | Conecta ao pino MISO de Hardware (FSPI Q) para ler o toque.   |
# | T_IRQ             | Interrupção do Touch    | GPIO 2             | Opcional: Útil para acordar o ESP32 com um toque na tela.     |
# +-------------------+-------------------------+--------------------+---------------------------------------------------------------+
#
# CONFIGURAÇÃO DE HARDWARE SPI NATIVA DO ESP32-S3 (FSPI):
# sck=12, mosi=11, miso=9, cs=10
# ==============================================================================


# ==============================================================================
# TABELA DE CONEXÕES: ESP32-C3 SUPER MINI + TELA TFT 2.8" (COM TOUCH INTEGRADO)
# ==============================================================================
#
# +-------------------+-------------------------+--------------------+---------------------------------------------------------------+
# | Pino da Tela TFT  | Função do Pino          | ESP32-C3 SuperMini | Observações / Alternativas                                    |
# +-------------------+-------------------------+--------------------+---------------------------------------------------------------+
# | VCC               | Alimentação Digital     | 3V3                | Alimenta o circuito lógico da tela.                           |
# | GND               | Terra / Negativo        | GND                | Conecte ao pino GND da placa.                                 |
# | CS (Display)      | Chip Select da Tela     | GPIO 4             | Ativa/desativa a comunicação com a tela.                      |
# | RESET / RST       | Reinício da Tela        | GPIO 2             | Pode ser ligado ao pino EN/RST do ESP32 para economizar pino. |
# | DC / RS           | Data / Command          | GPIO 3             | Define se o dado enviado é comando ou imagem.                 |
# | SDI / MOSI        | Linha de Dados SPI      | GPIO 7             | Pino obrigatório de Hardware SPI (MOSI).                      |
# | SCK / SCL         | Clock do SPI            | GPIO 6             | Pino obrigatório de Hardware SPI (SCK).                       |
# | LED / BL          | Luz de Fundo(Backlight) | GPIO 0 3V3 (Recomendado)  | Ligado direto para brilho máximo (economiza pino).            |
# | SDO / MISO        | Retorno de Dados SPI    | GPIO 5             | Pino obrigatório de Hardware SPI (MISO) para Touch/SD.        |
# | T_CLK             | Clock do Touch          | GPIO 6             | Compartilha o mesmo pino GPIO 6 (Barramento SPI).             |
# | T_CS              | Chip Select do Touch    | GPIO 1             | Ativa a leitura do toque.                                     |
# | T_DIN             | Entrada de Dados Touch  | GPIO 7             | Compartilha o mesmo pino GPIO 7 (Barramento SPI).             |
# | T_DO              | Saída de Dados Touch    | GPIO 5             | Compartilha o mesmo pino GPIO 5 (Barramento SPI).             |
# | T_IRQ             | Interrupção do Touch    | Desconectado       | Não é obrigatório (economiza um pino precioso).               |
# +-------------------+-------------------------+--------------------+---------------------------------------------------------------+
#
# DICA PARA O CÓDIGO (MicroPython):
# Ao inicializar o barramento SPI no ESP32-C3 Mini, utilize:
# spi = SPI(1, baudrate=40000000, sck=Pin(6), mosi=Pin(7), miso=Pin(5))
# ==============================================================================

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

app.route("boot", BootView)
app.route("home", HomeView)
app.route("terminal", TerminalView)
app.route("memory_graph", MemoryGraphView)
app.route("speedometer", SpeedometerView)
app.route("weather_dashboard", WeatherView)


app.navigate("boot")


app.run()

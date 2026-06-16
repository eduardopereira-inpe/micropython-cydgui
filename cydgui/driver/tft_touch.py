from cydgui.driver.ili9341 import Display
from cydgui.driver.xpt2046 import Touch
from machine import Pin, SPI
import uasyncio as asyncio
from cydgui.utils.constants import Constants

class TFTTouch:
    def __init__(self,
                 # Barramento SPI Compartilhado (Padrão para ESP32-S3)
                 disp_sck=12,
                 disp_mosi=11,
                 disp_miso=13,
                 # Pinos de Controle Individuais
                 disp_cs=10,
                 disp_dc=5,
                 disp_rst=4,
                 disp_bl=21,
                 touch_cs=9,
                 touch_int=3, # GPIO 36 não existe no S3 DevKit, mudado para 3
                 ):
        
        # 1. Criação do barramento SPI único e compartilhado por Hardware (SPI 1)
        # O ESP32-S3 gerencia as velocidades diferentes automaticamente por dispositivo
        self._shared_spi = SPI(
            1,
            baudrate=20000000, # 20MHz para escrita fluida no vídeo
            sck=Pin(disp_sck),
            mosi=Pin(disp_mosi),
            miso=Pin(disp_miso)
        )

        # 2. Inicialização do Display (ILI9341) usando o SPI compartilhado
        self._display = Display(
            self._shared_spi,
            cs=Pin(disp_cs, Pin.OUT),
            dc=Pin(disp_dc, Pin.OUT),
            rst=Pin(disp_rst, Pin.OUT),
            width=Constants.DISPLAY_WIDTH,
            height=Constants.DISPLAY_HEIGHT,
            rotation=Constants.DISPLAY_ROTATION
        )

        # Backlight
        tft_bl = Pin(disp_bl, Pin.OUT)
        tft_bl.value(1) # Liga a luz de fundo

        # Inicializa variável necessária para o método double_tap não quebrar no primeiro clique
        self.last_tap = (-1, -1)

        self._touch_event = asyncio.Event()
        self._touch_queue = []
        self.display_width = Constants.DISPLAY_WIDTH
        self.display_height = Constants.DISPLAY_HEIGHT

        # 3. Inicialização do Touch (XPT2046) usando o MESMO SPI compartilhado
        # Nota: O driver interno do XPT2046 reduz temporariamente o baudrate para ~2.5MHz durante a leitura
        self._touch = Touch(
            self._shared_spi,
            cs=Pin(touch_cs, Pin.OUT),
            width=Constants.DISPLAY_WIDTH,
            height=Constants.DISPLAY_HEIGHT,
            int_pin=Pin(touch_int),
            int_handler=self._touch_handler,
            invert_x=Constants.TOUCH_INVERT_X,
            invert_y=Constants.TOUCH_INVERT_Y,
        )

    def __call__(self, x, y):
        self.last_tap = (x, y)

    @property
    def touch(self):
        return self._touch
    
    @property
    def display(self):
        return self._display

    ######################################################
    #   Touchscreen Press Event
    ######################################################
    def _touch_handler(self, x, y):
        """
        Callback chamado pelo driver Touch.
        """
        x = (self.display_width - 1) - x

        self._x = x
        self._y = y

        self._touch_queue.append((x, y))

        try:
            self._touch_event.set()
        except:
            pass

    def touches(self):
        if self._touch_queue:
            return self._touch_queue.pop(0)
        return None

    async def wait_touch(self):
        """
        Aguarda proximo toque.
        """
        while not self._touch_queue:
            self._touch_event.clear()
            await self._touch_event.wait()

        return self._touch_queue.pop(0)

    async def touch_stream(self):
        while True:
            yield await self.wait_touch()

    def double_tap(self, x, y, error_margin = 10):
        '''
        Returns whether or not a double tap was detected.

        Return:
            True: Double-tap detected.
            False: Single tap detected.
        '''
        # Double tap to exit
        if self.last_tap[0] - error_margin <= x and self.last_tap[0] + error_margin >= x:
            if self.last_tap[1] - error_margin <= y and self.last_tap[1] + error_margin >= y:
                self.last_tap = (-1,-1)
                return True
        self.last_tap = (x,y)
        return False

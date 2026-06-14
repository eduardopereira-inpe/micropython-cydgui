from cydgui.driver.ili9341 import Display
from cydgui.driver.xpt2046 import Touch
from machine import Pin, SPI

import uasyncio as asyncio

from cydgui.utils.constants import Constants


class TFTTouch:
    def __init__(self, 
                 display_width=Constants.DISPLAY_WIDTH, 
                 display_height=Constants.DISPLAY_HEIGHT
                 ):
        # SPI for display
        self._hspi = SPI(
            1,
            baudrate=40000000,
            sck=Pin(14),
            mosi=Pin(13),
            miso=Pin(12)
        )

        self._display = Display(
            self._hspi, 
            cs=Pin(15, Pin.OUT),
            dc=Pin(2, Pin.OUT),
            rst=Pin(27, Pin.OUT),
            width=Constants.DISPLAY_WIDTH, 
            height=Constants.DISPLAY_HEIGHT,
            rotation=Constants.DISPLAY_ROTATION
        )

        # Backlight
        tft_bl = Pin(21, Pin.OUT)
        tft_bl.value(1) #Turn on backlight

        # Touch
        self._sspi = SPI(
            2,
            baudrate=1000000,
            sck=Pin(25),
            mosi=Pin(32),
            miso=Pin(39)
        )

        self._touch_event = asyncio.Event()
        self._touch_queue = []
        self.display_width = display_width
        self.display_height = display_height

        self._touch = Touch(
            self._sspi,
            cs=Pin(33, Pin.OUT),
            width=Constants.DISPLAY_WIDTH,
            height=Constants.DISPLAY_HEIGHT,
            int_pin=Pin(36), 
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



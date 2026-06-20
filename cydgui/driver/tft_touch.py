import gc
from cydgui.driver.ili9341 import Display
from cydgui.driver.xpt2046 import Touch
from machine import Pin, SPI

import uasyncio as asyncio

from cydgui.utils.constants import Constants


class TFTTouch:
    def __init__(
        self,

        # Display SPI
        disp_sck=14,
        disp_mosi=13,
        disp_miso=12,

        # Display control
        disp_cs=15,
        disp_dc=2,
        disp_rst=27,
        disp_bl=21,

        # Touch SPI
        touch_sck=25,
        touch_mosi=32,
        touch_miso=39,

        # Touch control
        touch_cs=33,
        touch_int=36,

        # Features
        has_touch=True,

        # Display config
        display_width=Constants.DISPLAY_WIDTH,
        display_height=Constants.DISPLAY_HEIGHT,
        rotation=Constants.DISPLAY_ROTATION
    ):

        self.display_width = display_width
        self.display_height = display_height

        # SPI do display
        self._hspi = SPI(
            1,
            baudrate=40000000,
            sck=Pin(disp_sck),
            mosi=Pin(disp_mosi),
            miso=Pin(disp_miso)
        )

        self._display = Display(
            self._hspi,
            cs=Pin(disp_cs, Pin.OUT),
            dc=Pin(disp_dc, Pin.OUT),
            rst=Pin(disp_rst, Pin.OUT),
            width=display_width,
            height=display_height,
            rotation=rotation
        )

        # Backlight
        self._backlight = Pin(disp_bl, Pin.OUT)
        self._backlight.value(1)

        # Touch opcional
        self._touch = None
        self._touch_event = None
        self._touch_queue = []

        if has_touch:
            gc.collect()
            
            self._sspi = SPI(
                2,
                baudrate=1000000,
                sck=Pin(touch_sck),
                mosi=Pin(touch_mosi),
                miso=Pin(touch_miso)
            )

            self._touch_event = asyncio.Event()

            self._touch = Touch(
                self._sspi,
                cs=Pin(touch_cs, Pin.OUT),
                width=display_width,
                height=display_height,
                int_pin=Pin(touch_int),
                int_handler=self._touch_handler,
                invert_x=Constants.TOUCH_INVERT_X,
                invert_y=Constants.TOUCH_INVERT_Y,
            )

        self.last_tap = (-1, -1)

    def __call__(self, x, y):
        self.last_tap = (x, y)

    @property
    def touch(self):
        return self._touch

    @property
    def display(self):
        return self._display

    @property
    def has_touch(self):
        return self._touch is not None

    ######################################################
    # Touchscreen Press Event
    ######################################################
    def _touch_handler(self, x, y):
        x = (self.display_width - 1) - x

        self._x = x
        self._y = y

        self._touch_queue.append((x, y))

        try:
            self._touch_event.set()
        except Exception:
            pass

    def touches(self):
        if not self.has_touch:
            return None

        if self._touch_queue:
            return self._touch_queue.pop(0)

        return None

    async def wait_touch(self):
        if not self.has_touch:
            raise RuntimeError("Touchscreen desabilitado")

        while not self._touch_queue:
            self._touch_event.clear()
            await self._touch_event.wait()

        return self._touch_queue.pop(0)

    async def touch_stream(self):
        if not self.has_touch:
            raise RuntimeError("Touchscreen desabilitado")

        while True:
            yield await self.wait_touch()

    def double_tap(self, x, y, error_margin=10):
        if self.last_tap[0] - error_margin <= x <= self.last_tap[0] + error_margin:
            if self.last_tap[1] - error_margin <= y <= self.last_tap[1] + error_margin:
                self.last_tap = (-1, -1)
                return True

        self.last_tap = (x, y)
        return False

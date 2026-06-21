from machine import Pin
import uasyncio as asyncio

class BlState:
    __slots__ = ("pin", "pin_btn", "state", "verbose")
    def __init__(self, pin_num, pin_btn, verbose=True):
        self.pin = Pin(pin_num, Pin.OUT)
        self.pin_btn = Pin(pin_btn, Pin.IN, Pin.PULL_UP)
        self.state = False
        self.verbose = verbose

    def _log(self, message):
        if self.verbose:
            print(message)

    def toggle(self):
        if self.pin_btn.value() == 0:
            self._log("Button pressed, toggling backlight state.")
            self.state = not self.state
            self.pin.value(self.state)
        
    async def monitor(self):
        while True:
            self.toggle()
            await asyncio.sleep_ms(100)
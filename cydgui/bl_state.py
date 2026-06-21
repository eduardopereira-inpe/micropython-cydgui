from machine import Pin
import uasyncio as asyncio
import time
class BlState:
    __slots__ = (
        "pin", 
        "pin_btn", 
        "state", 
        "verbose", 
        "dtime_minutes",
        "_last_toggle_time"
        )
    def __init__(self, pin_num, pin_btn, verbose=True, dtime_minutes=5):
        self.pin = Pin(pin_num, Pin.OUT)
        self.pin_btn = Pin(pin_btn, Pin.IN, Pin.PULL_UP)
        self.state = False
        self._last_toggle_time = 0
        self.verbose = verbose
        self.dtime_minutes = dtime_minutes

    def _log(self, message):
        if self.verbose:
            print(message)

    def toggle(self):
        if self.pin_btn.value() == 0:
            self._log("Button pressed, toggling backlight state.")
            self.state = not self.state
            self.pin.value(self.state)
            self._last_toggle_time = time.ticks_ms()

        if self.state and time.ticks_diff(time.ticks_ms(), self._last_toggle_time) > self.dtime_minutes * 60 * 1000:
            self._log("Auto-toggling backlight off after timeout.")
            self.state = False
            self.pin.value(self.state)
            self._last_toggle_time = time.ticks_ms()
            
    async def monitor(self):
        while True:
            self.toggle()
            await asyncio.sleep_ms(100)
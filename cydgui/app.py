import utime
import uasyncio as asyncio


class App:
    """
    Frame-driven UI engine (ESP32 friendly).
    Single scheduler = predictable performance.
    """

    def __init__(self, renderer, touch=None, frame_delay_ms: int = 5):
        self._renderer = renderer
        self._touch = touch
        self._frame_delay_ms = frame_delay_ms

        self._running = False

        self._routes = {}
        self._screen = None

        self._widgets = set()

        self._last_tick = utime.ticks_ms()

    # ---------------------------------------------------------
    # Widget registration
    # ---------------------------------------------------------

    def register_widget(self, widget):
        self._widgets.add(widget)

    def unregister_widget(self, widget):
        self._widgets.discard(widget)

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    def route(self, name, view_class):
        self._routes[name] = view_class

    def navigate(self, name, parameters=None):
        self._widgets.clear()

        view_class = self._routes[name]
        self._screen = view_class(self, parameters=parameters)

    # ---------------------------------------------------------
    # MAIN LOOP
    # ---------------------------------------------------------

    async def _run_async(self):

        self._running = True

        while self._running:

            now = utime.ticks_ms()
            dt = utime.ticks_diff(now, self._last_tick)
            self._last_tick = now

            event = self._poll_touch()
            if event and self._screen:
                self._screen.dispatch_touch(event)

            for w in self._widgets:
                try:
                    w.tick(now, dt)
                except:
                    pass

            if self._screen and self._screen.dirty:
                self._screen.draw(self._renderer)
                self._renderer.flush()

            await asyncio.sleep_ms(self._frame_delay_ms)

    def run(self):
        asyncio.run(self._run_async())

    def _poll_touch(self):
        if not self._touch:
            return None

        t = self._touch.get_touch()
        if t:
            from cydgui.core.touch_event import TouchEvent
            x, y = t
            return TouchEvent(x=x, y=y, event_type=TouchEvent.DOWN)
        return None
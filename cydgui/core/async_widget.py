import uasyncio as asyncio
from cydgui.core.widget import Widget

class AsyncWidget(Widget):
    """
    Base widget for real-time async updates.
    Designed for clocks, sensors, network status, etc.
    """

    # Aceita kwargs para repassar x, y, width, height para o Widget
    def __init__(self, interval_ms=1000, verbose=False, **kwargs):
        super().__init__(**kwargs)
        self.interval_ms = interval_ms
        self._running = False
        self._task = None
        self.verbose = verbose

    def _log(self, msg):
        if self.verbose:
            print("[AsyncWidget]", msg)

    async def start(self):
        """Start async loop gracefully directly in the current task."""
        if self._running:
            return

        self._running = True
        await self._loop()

    async def stop(self):
        """Stop async loop."""
        self._running = False
        self._task = None

    async def _loop(self):
        """Internal loop."""
        while self._running:
            try:
                await self.update_async()
            except Exception as e:
                self._log("error: {}".format(e))

            self.invalidate()
            await asyncio.sleep_ms(self.interval_ms)

    async def update_async(self):
        """Override this method. Called periodically in async loop."""
        pass
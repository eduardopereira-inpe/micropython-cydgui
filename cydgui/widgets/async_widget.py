# cydgui/widgets/async_widget.py

import uasyncio as asyncio
import gc

from cydgui.core.widget import Widget


class AsyncWidget(Widget):
    """
    Base widget for real-time async updates.

    Designed for clocks, sensors, network status, etc.
    """

    def __init__(self, interval_ms=1000):
        super().__init__()
        self.interval_ms = interval_ms
        self._running = False
        self._task = None

    async def start(self):
        """Start async loop."""
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._loop())

    async def stop(self):
        """Stop async loop."""
        self._running = False

    async def _loop(self):
        """Internal loop."""
        while self._running:
            await self.update_async()
            self.invalidate()
            await asyncio.sleep_ms(self.interval_ms)

    async def update_async(self):
        """
        Override this method.

        Called periodically in async loop.
        """
        pass
import gc
from .async_canvas import AsyncCanvas
from cydgui.utils.colors import Colors


class MemoryGraphWidget(AsyncCanvas):
    """
    Gráfico de memória livre (tempo real).
    """

    def __init__(self, max_samples=60, interval_ms=1000, **kwargs):
        super().__init__(interval_ms=interval_ms, **kwargs)

        self.max_samples = max_samples
        self.samples = []

    # ---------------------------------------------------------
    # UPDATE (async state)
    # ---------------------------------------------------------

    async def update_async(self):
        free = gc.mem_free()

        self.samples.append(free)

        if len(self.samples) > self.max_samples:
            self.samples.pop(0)

    # ---------------------------------------------------------
    # DRAW (OBRIGATÓRIO no pipeline)
    # ---------------------------------------------------------

    def on_draw(self):

        if not self.samples:
            return

        w = self.width
        h = self.height

        max_val = max(self.samples)
        min_val = min(self.samples)

        rng = max(max_val - min_val, 1)

        n = len(self.samples)
        step_x = w / max(n - 1, 1)

        prev_x = None
        prev_y = None

        for i, value in enumerate(self.samples):

            x = int(i * step_x)

            norm = (value - min_val) / rng
            y = int(h - 1 - norm * (h - 1))

            if prev_x is not None:
                self.draw_line(prev_x, prev_y, x, y, Colors.CYAN)

            prev_x, prev_y = x, y

        self.draw_text(
            2,
            2,
            "Mem.: {:.2f} kB".format(self.samples[-1] / 1024),
            Colors.WHITE
        )
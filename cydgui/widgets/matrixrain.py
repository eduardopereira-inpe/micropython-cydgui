from random import randint
from cydgui.core.widget import Widget
from cydgui.driver.ili9341 import color565

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

class MatrixRainWidget(Widget):
    CELL = 8

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        self.BLACK = 0
        self.WHITE = color565(255, 255, 255)

        self.GREEN1 = color565(0, 255, 0)
        self.GREEN2 = color565(0, 180, 0)
        self.GREEN3 = color565(0, 100, 0)

        self.cols = self.width // self.CELL
        self.rows = self.height // self.CELL

        self.drops = [
            {
                "y": randint(-self.rows, 0),
                "speed": randint(1, 2)
            }
            for _ in range(self.cols)
        ]
        
        self._display = None

    def random_char(self):
        return chr(randint(33, 126))

    def draw(self, renderer):
        """
        renderer deve expor: renderer.display (ILI9341 Display)
        """

        self._display = renderer.driver
        self.validate()
        
    async def update(self):
        if self._display is None:
            return
        
        while True:

            for col in range(self.cols):

                d = self.drops[col]

                # pequena aleatoriedade de atualização (efeito mais "orgânico")
                if randint(0, 2):
                    continue

                x = self.x + col * self.CELL
                y = d["y"]

                # cabeça branca
                if 0 <= y < self.rows:
                    self._display.draw_text8x8(
                        x,
                        self.y + y * self.CELL,
                        self.random_char(),
                        self.WHITE,
                        self.BLACK
                    )

                # trilha verde
                colors = (self.GREEN1, self.GREEN2, self.GREEN3)

                for i in range(1, 4):
                    ty = y - i
                    if 0 <= ty < self.rows:
                        self._display.draw_text8x8(
                            x,
                            self.y + ty * self.CELL,
                            self.random_char(),
                            colors[i - 1],
                            self.BLACK
                        )

                # limpeza de cauda (evita acúmulo visual)
                erase = y - 8
                if 0 <= erase < self.rows:
                    self._display.fill_rectangle(
                        x,
                        self.y + erase * self.CELL,
                        self.CELL,
                        self.CELL,
                        self.BLACK
                    )

                # atualização do estado
                d["y"] += d["speed"]

                if d["y"] > self.rows + 10:
                    d["y"] = randint(-self.rows, 0)
                    d["speed"] = randint(1, 3)
                    
                await asyncio.sleep_ms(30)


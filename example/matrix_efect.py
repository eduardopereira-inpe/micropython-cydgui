from random import randint
from time import sleep_ms

from cydgui.driver.ili9341 import Display
from cydgui.driver.ili9341 import color565
from cydgui.driver.tft_touch import TFTTouch


class MatrixRain:

    CELL = 8

    def __init__(self, display):

        self.display = display

        self.BLACK = 0
        self.WHITE = color565(255, 255, 255)

        self.GREEN1 = color565(0, 255, 0)
        self.GREEN2 = color565(0, 180, 0)
        self.GREEN3 = color565(0, 100, 0)

        self.cols = display.width // self.CELL

        self.drops = []

        for _ in range(self.cols):
            self.drops.append({
                "y": randint(-30, 0),
                "speed": randint(1, 2)
            })

    def random_char(self):
        return chr(randint(33, 126))

    def update(self):

        rows = self.display.height // self.CELL

        for col in range(self.cols):

            d = self.drops[col]

            if randint(0, 2):
                continue

            x = col * self.CELL
            y = d["y"]

            # cabeça branca
            if 0 <= y < rows:
                self.display.draw_text8x8(
                    x,
                    y * self.CELL,
                    self.random_char(),
                    self.WHITE,
                    self.BLACK
                )

            # trilha
            colors = (
                self.GREEN1,
                self.GREEN2,
                self.GREEN3
            )

            for tail in range(1, 4):

                ty = y - tail

                if 0 <= ty < rows:

                    self.display.draw_text8x8(
                        x,
                        ty * self.CELL,
                        self.random_char(),
                        colors[tail - 1],
                        self.BLACK
                    )

            # apagar rastro distante
            erase = y - 8

            if 0 <= erase < rows:

                self.display.fill_rectangle(
                    x,
                    erase * self.CELL,
                    self.CELL,
                    self.CELL,
                    self.BLACK
                )

            d["y"] += d["speed"]

            if d["y"] > rows + 10:
                d["y"] = randint(-30, 0)
                d["speed"] = randint(1, 3)


# --------------------------
# Uso
# --------------------------

tft_touch = TFTTouch()

display = tft_touch.display

display.clear()

matrix = MatrixRain(display)

while True:
    matrix.update()
    sleep_ms(30)
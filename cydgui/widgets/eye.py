from random import randint

from cydgui.core.widget import Widget
from cydgui.driver.ili9341 import color565

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


class EyeWidget(Widget):

    SPRITE_SIZE = 32

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        self.WHITE = color565(255, 255, 255)
        self.BLACK = color565(0, 0, 0)

        self._display = None
        self._initialized = False

        self.sprite = None

        self._calculate_layout()

    def _calculate_layout(self):

        center_x = self.x + self.width // 2

        self.eye_y = self.y + self.height // 2

        spacing = self.width // 4

        self.left_eye_x = center_x - spacing
        self.right_eye_x = center_x + spacing

        self.eye_rx = max(20, self.width // 6)
        self.eye_ry = max(15, self.height // 4)

        self.max_move_x = max(
            4,
            self.eye_rx // 3
        )

        self.max_move_y = max(
            3,
            self.eye_ry // 3
        )

        self.left_x = self.left_eye_x
        self.left_y = self.eye_y

        self.right_x = self.right_eye_x
        self.right_y = self.eye_y

        self.target_dx = 0
        self.target_dy = 0

    def draw(self, renderer):

        self._display = renderer.driver

        if not self._initialized:

            self._draw_eyes()

            self.sprite = self._display.load_sprite(
                "cydgui/assets/brown_eye.rgb565",
                self.SPRITE_SIZE,
                self.SPRITE_SIZE
            )

            self._draw_sprite(
                self.left_x,
                self.left_y
            )

            self._draw_sprite(
                self.right_x,
                self.right_y
            )

            self._initialized = True

        self.validate()

    def _draw_eyes(self):

        d = self._display

        d.fill_ellipse(
            self.left_eye_x,
            self.eye_y,
            self.eye_rx,
            self.eye_ry,
            self.WHITE
        )

        d.fill_ellipse(
            self.right_eye_x,
            self.eye_y,
            self.eye_rx,
            self.eye_ry,
            self.WHITE
        )

        d.draw_ellipse(
            self.left_eye_x,
            self.eye_y,
            self.eye_rx,
            self.eye_ry,
            self.BLACK
        )

        d.draw_ellipse(
            self.right_eye_x,
            self.eye_y,
            self.eye_rx,
            self.eye_ry,
            self.BLACK
        )

    def _erase_sprite(self, x, y):

        half = self.SPRITE_SIZE // 2

        self._display.fill_rectangle(
            x - half,
            y - half,
            self.SPRITE_SIZE,
            self.SPRITE_SIZE,
            self.WHITE
        )

    def _draw_sprite(self, x, y):

        half = self.SPRITE_SIZE // 2

        self._display.draw_sprite(
            self.sprite,
            x - half,
            y - half,
            self.SPRITE_SIZE,
            self.SPRITE_SIZE
        )

    def _new_target(self):

        self.target_dx = randint(
            -self.max_move_x,
            self.max_move_x
        )

        self.target_dy = randint(
            -self.max_move_y,
            self.max_move_y
        )

    async def update(self):

        if self._display is None:
            return

        self._new_target()

        while True:

            target_left_x = (
                self.left_eye_x +
                self.target_dx
            )

            target_left_y = (
                self.eye_y +
                self.target_dy
            )

            target_right_x = (
                self.right_eye_x +
                self.target_dx
            )

            target_right_y = (
                self.eye_y +
                self.target_dy
            )

            self._erase_sprite(
                self.left_x,
                self.left_y
            )

            self._erase_sprite(
                self.right_x,
                self.right_y
            )

            if self.left_x < target_left_x:
                self.left_x += 1
            elif self.left_x > target_left_x:
                self.left_x -= 1

            if self.left_y < target_left_y:
                self.left_y += 1
            elif self.left_y > target_left_y:
                self.left_y -= 1

            if self.right_x < target_right_x:
                self.right_x += 1
            elif self.right_x > target_right_x:
                self.right_x -= 1

            if self.right_y < target_right_y:
                self.right_y += 1
            elif self.right_y > target_right_y:
                self.right_y -= 1

            self._draw_sprite(
                self.left_x,
                self.left_y
            )

            self._draw_sprite(
                self.right_x,
                self.right_y
            )

            if (
                self.left_x == target_left_x and
                self.left_y == target_left_y
            ):
                self._new_target()

            await asyncio.sleep_ms(40)
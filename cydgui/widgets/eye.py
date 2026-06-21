from random import randint

from cydgui.core.widget import Widget
from cydgui.driver.ili9341 import color565

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


class EyeWidget(Widget):

    VALID_IRIS_SIZES = (16, 22, 32)

    def __init__(
        self,
        x,
        y,
        width,
        height,
        iris_size=32
    ):
        super().__init__(x, y, width, height)

        if iris_size not in self.VALID_IRIS_SIZES:
            raise ValueError(
                "iris_size deve ser 16, 22 ou 32"
            )

        self.iris_size = iris_size

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

        self.eye_rx = max(
            20,
            self.width // 6
        )

        self.eye_ry = max(
            15,
            self.height // 4
        )

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

    def draw(self, renderer):

        self._display = renderer.driver

        if not self._initialized:

            self._draw_eyes()

            sprite_name = (
                f"cydgui/assets/"
                f"brown_eye_{self.iris_size}_{self.iris_size}.rgb565"
            )

            self.sprite = self._display.load_sprite(
                sprite_name,
                self.iris_size,
                self.iris_size
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

        half = self.iris_size // 2

        self._display.fill_rectangle(
            x - half,
            y - half,
            self.iris_size,
            self.iris_size,
            self.WHITE
        )

    def _draw_sprite(self, x, y):

        half = self.iris_size // 2

        self._display.draw_sprite(
            self.sprite,
            x - half,
            y - half,
            self.iris_size,
            self.iris_size
        )

    def _set_position(
        self,
        left_x,
        left_y,
        right_x,
        right_y
    ):

        self._erase_sprite(
            self.left_x,
            self.left_y
        )

        self._erase_sprite(
            self.right_x,
            self.right_y
        )

        self.left_x = left_x
        self.left_y = left_y

        self.right_x = right_x
        self.right_y = right_y

        self._draw_sprite(
            self.left_x,
            self.left_y
        )

        self._draw_sprite(
            self.right_x,
            self.right_y
        )

    async def animation(
        self,
        from_pos,
        to_pos,
        delay_ms=40
    ):
        """
        Anima de uma posição para outra.

        from_pos = (dx, dy)
        to_pos   = (dx, dy)
        """

        from_dx, from_dy = from_pos
        to_dx, to_dy = to_pos

        current_dx = from_dx
        current_dy = from_dy

        while True:

            if current_dx < to_dx:
                current_dx += 1
            elif current_dx > to_dx:
                current_dx -= 1

            if current_dy < to_dy:
                current_dy += 1
            elif current_dy > to_dy:
                current_dy -= 1

            self._set_position(
                self.left_eye_x + current_dx,
                self.eye_y + current_dy,
                self.right_eye_x + current_dx,
                self.eye_y + current_dy
            )

            if (
                current_dx == to_dx and
                current_dy == to_dy
            ):
                break

            await asyncio.sleep_ms(
                delay_ms
            )

    def current_offset(self):

        return (
            self.left_x - self.left_eye_x,
            self.left_y - self.eye_y
        )

    async def move_to(
        self,
        dx,
        dy,
        delay_ms=40
    ):
        """
        Move para um deslocamento relativo.
        """

        dx = max(
            -self.max_move_x,
            min(self.max_move_x, dx)
        )

        dy = max(
            -self.max_move_y,
            min(self.max_move_y, dy)
        )

        await self.animation(
            self.current_offset(),
            (dx, dy),
            delay_ms
        )

    async def center(
        self,
        delay_ms=40
    ):
        await self.move_to(
            0,
            0,
            delay_ms
        )

    async def auto_moving(
        self,
        delay_ms=40,
        pause_ms=1000
    ):
        """
        Movimento automático aleatório.
        """

        while True:

            dx = randint(
                -self.max_move_x,
                self.max_move_x
            )

            dy = randint(
                -self.max_move_y,
                self.max_move_y
            )

            await self.move_to(
                dx,
                dy,
                delay_ms
            )

            await asyncio.sleep_ms(
                pause_ms
            )

    async def update(self):

        await self.auto_moving()
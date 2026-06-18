import uasyncio as asyncio
import urandom

from .async_canvas import AsyncCanvas


class EyeWidget(AsyncCanvas):

    PUPIL_ROUND = "round"
    PUPIL_DIAMOND = "diamond"

    def __init__(
        self,
        iris_color=0x07E0,
        pupil_shape="round",
        blink_interval=(3000, 7000),
        sclera_color=0xFFFF,
        pupil_color=0x0000,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.iris_color = iris_color
        self.pupil_shape = pupil_shape

        self.sclera_color = sclera_color
        self.pupil_color = pupil_color

        self.blink_interval = blink_interval

        self.eye_x = 0.0
        self.eye_y = 0.0

        self.max_offset = 0.35

        self._blink = 0.0
        self._next_blink = self._random_blink()

    # --------------------------------------------------
    # Movimento
    # --------------------------------------------------

    def look_at(self, dx: float, dy: float):
        """
        -1.0 .. +1.0
        """

        if dx < -1:
            dx = -1
        if dx > 1:
            dx = 1

        if dy < -1:
            dy = -1
        if dy > 1:
            dy = 1

        self.eye_x = dx
        self.eye_y = dy

        self.invalidate()

    # --------------------------------------------------
    # Piscar
    # --------------------------------------------------

    def _random_blink(self):
        a, b = self.blink_interval
        return urandom.randint(a, b)

    async def _do_blink(self):

        steps = 6

        for i in range(steps):
            self._blink = (i + 1) / steps
            self.invalidate()
            await asyncio.sleep_ms(20)

        for i in range(steps):
            self._blink = 1.0 - ((i + 1) / steps)
            self.invalidate()
            await asyncio.sleep_ms(20)

        self._blink = 0

    # --------------------------------------------------
    # Async
    # --------------------------------------------------

    async def update_async(self):

        self._next_blink -= self.interval_ms

        if self._next_blink <= 0:
            await self._do_blink()
            self._next_blink = self._random_blink()

    # --------------------------------------------------
    # Draw
    # --------------------------------------------------

    def on_draw(self):

        r = self.renderer

        cx = self.width // 2
        cy = self.height // 2

        # -----------------------------------------
        # fechamento da pálpebra
        # -----------------------------------------

        eye_h = int(self.height * (1.0 - self._blink))

        if eye_h <= 2:
            return

        # -----------------------------------------
        # globo ocular
        # -----------------------------------------

        r.fill_ellipse(
            self.absolute_x + cx,
            self.absolute_y + cy,
            self.width // 2,
            eye_h // 2,
            self.sclera_color
        )

        # -----------------------------------------
        # deslocamento da íris
        # -----------------------------------------

        ox = int(
            self.eye_x *
            (self.width * self.max_offset / 2)
        )

        oy = int(
            self.eye_y *
            (eye_h * self.max_offset / 2)
        )

        iris_r = min(self.width, eye_h) // 4

        iris_x = self.absolute_x + cx + ox
        iris_y = self.absolute_y + cy + oy

        # -----------------------------------------
        # íris
        # -----------------------------------------

        r.fill_circle(
            iris_x,
            iris_y,
            iris_r,
            self.iris_color
        )

        # -----------------------------------------
        # pupila
        # -----------------------------------------

        pupil_r = iris_r // 2

        if self.pupil_shape == self.PUPIL_ROUND:

            r.fill_circle(
                iris_x,
                iris_y,
                pupil_r,
                self.pupil_color
            )

        else:

            r.fill_diamond(
                iris_x,
                iris_y,
                pupil_r,
                self.pupil_color
            )




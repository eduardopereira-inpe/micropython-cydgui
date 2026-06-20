import math
from .buffered_canvas import BufferedCanvas
from cydgui.utils.colors import Colors


class SpeedometerWidget(BufferedCanvas):
    """
    Speedometer otimizado para framebuffer RGB565.

    Estratégia:
    - background (estático) pré-renderizado uma vez
    - frame: copia background + ponteiro + texto
    """

    __slots__ = (
        "min_val",
        "max_val",
        "value",
        "_step",
        "_background",
        "_bg_ready",
    )

    # ---------------------------------------------------------
    # INIT
    # ---------------------------------------------------------

    def __init__(self, min_val=0, max_val=100, interval_ms=50, **kwargs):

        super().__init__(interval_ms=interval_ms, **kwargs)

        self.min_val = min_val
        self.max_val = max_val
        self.value = min_val

        self._step = 2

        self._background = bytearray(self.width * self.height * 2)
        self._bg_ready = False

    # ---------------------------------------------------------
    # ASYNC UPDATE
    # ---------------------------------------------------------

    async def update_async(self):

        self.value += self._step

        if self.value >= self.max_val or self.value <= self.min_val:
            self._step *= -1

    # ---------------------------------------------------------
    # BUILD BACKGROUND (EXECUTADO 1x)
    # ---------------------------------------------------------

    def _build_background(self):

        # copia base do canvas
        self._buffer[:] = bytes(self._buffer)

        cx = self.width // 2
        cy = self.height - 20
        r = min(self.width // 2, self.height) - 15

        COR_BASE = Colors.DARK_GRAY if hasattr(Colors, 'DARK_GRAY') else 0x4208
        COR_BOM = Colors.GREEN if hasattr(Colors, 'GREEN') else 0x07E0
        COR_ALERTA = Colors.YELLOW if hasattr(Colors, 'YELLOW') else 0xFFE0
        COR_PERIGO = Colors.RED if hasattr(Colors, 'RED') else 0xF800

        # base horizontal
        self.hline(cx - r - 5, cy, (r * 2) + 10, COR_BASE)

        # ticks
        steps = 20

        for i in range(steps + 1):

            ratio = i / steps
            angle = math.pi - (ratio * math.pi)

            if ratio < 0.6:
                color = COR_BOM
            elif ratio < 0.8:
                color = COR_ALERTA
            else:
                color = COR_PERIGO

            is_major = (i % 2 == 0)
            length = 12 if is_major else 6

            r_in = r - length
            r_out = r

            x1 = cx + int(r_in * math.cos(angle))
            y1 = cy - int(r_in * math.sin(angle))

            x2 = cx + int(r_out * math.cos(angle))
            y2 = cy - int(r_out * math.sin(angle))

            self.line(x1, y1, x2, y2, color)

        # hub base
        hub = 8

        self.fill_rect(
            cx - hub // 2,
            cy - hub // 2,
            hub,
            hub,
            COR_BASE
        )

        self.rect(
            cx - hub // 2,
            cy - hub // 2,
            hub,
            hub,
            0xFFFF
        )

        self._bg_ready = True

    # ---------------------------------------------------------
    # DRAW FRAME
    # ---------------------------------------------------------

    def draw(self, renderer):

        if not self.visible:
            return

        self._renderer = renderer

        # primeira vez constrói background
        if not self._bg_ready:
            self._build_background()

        # copia background para frame atual
        self._buffer[:] = self._background

        cx = self.width // 2
        cy = self.height - 20
        r = min(self.width // 2, self.height) - 15

        val = max(self.min_val, min(self.max_val, self.value))
        ratio = (val - self.min_val) / (self.max_val - self.min_val)

        angle = math.pi - (ratio * math.pi)

        # ponteiro
        r_ptr = r - 15

        px = cx + int(r_ptr * math.cos(angle))
        py = cy - int(r_ptr * math.sin(angle))

        base_w = 4

        bx1 = cx - int(base_w * math.sin(angle))
        by1 = cy - int(base_w * math.cos(angle))

        bx2 = cx + int(base_w * math.sin(angle))
        by2 = cy + int(base_w * math.cos(angle))

        COR_PONTEIRO = Colors.RED if hasattr(Colors, 'RED') else 0xF800
        COR_TEXTO = Colors.WHITE if hasattr(Colors, 'WHITE') else 0xFFFF

        # ponteiro preenchido
        steps = base_w * 2

        for i in range(steps + 1):

            f = i / steps

            x = int(bx1 + (bx2 - bx1) * f)
            y = int(by1 + (by2 - by1) * f)

            self.line(x, y, px, py, COR_PONTEIRO)

        # hub dinâmico
        hub = 6

        self.fill_rect(
            cx - hub // 2,
            cy - hub // 2,
            hub,
            hub,
            COR_PONTEIRO
        )

        self.rect(
            cx - hub // 2,
            cy - hub // 2,
            hub,
            hub,
            COR_TEXTO
        )

        # texto
        text = str(int(val))
        offset = (len(text) * 4)

        self.draw_text(
            cx - offset,
            cy + 10,
            text,
            COR_TEXTO
        )

        # flush único
        self.flush()

        self.validate()
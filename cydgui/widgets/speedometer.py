import math

from .async_canvas import AsyncCanvas
from cydgui.utils.colors import Colors


class SpeedometerWidget(AsyncCanvas):

    __slots__ = (
        "min_val",
        "max_val",
        "value",
    )

    def __init__(
        self,
        min_val=0,
        max_val=100,
        value=0,
        interval_ms=1000,
        **kwargs
    ):
        super().__init__(interval_ms=interval_ms, **kwargs)

        self.min_val = min_val
        self.max_val = max_val
        self.value = value

    # ---------------------------------------------------------
    # API
    # ---------------------------------------------------------

    def set_value(self, value):

        value = max(
            self.min_val,
            min(self.max_val, value)
        )

        if value != self.value:
            self.value = value
            self.invalidate()

    # ---------------------------------------------------------
    # DRAW
    # ---------------------------------------------------------

    def on_draw(self):

        w = self.width
        h = self.height

        cx = w // 2
        cy = h - 20

        r = min(w // 2, h) - 15

        COR_TEXTO = getattr(
            Colors,
            "WHITE",
            0xFFFF
        )

        COR_PONTEIRO = getattr(
            Colors,
            "RED",
            0xF800
        )

        COR_BASE = getattr(
            Colors,
            "DARK_GRAY",
            0x4208
        )

        COR_BOM = getattr(
            Colors,
            "GREEN",
            0x07E0
        )

        COR_ALERTA = getattr(
            Colors,
            "YELLOW",
            0xFFE0
        )

        COR_PERIGO = getattr(
            Colors,
            "RED",
            0xF800
        )

        # -----------------------------------------------------
        # LINHA BASE
        # -----------------------------------------------------

        self.draw_line(
            cx - r - 5,
            cy,
            cx + r + 5,
            cy,
            COR_BASE
        )

        # -----------------------------------------------------
        # ESCALA
        # -----------------------------------------------------

        passos = 20

        for i in range(passos + 1):

            ratio = i / passos

            angle = math.pi - (ratio * math.pi)

            if ratio < 0.60:
                cor = COR_BOM
            elif ratio < 0.80:
                cor = COR_ALERTA
            else:
                cor = COR_PERIGO

            major = (i % 2 == 0)

            tick = 12 if major else 6

            x1 = cx + int((r - tick) * math.cos(angle))
            y1 = cy - int((r - tick) * math.sin(angle))

            x2 = cx + int(r * math.cos(angle))
            y2 = cy - int(r * math.sin(angle))

            self.draw_line(
                x1,
                y1,
                x2,
                y2,
                cor
            )

        # -----------------------------------------------------
        # MARCADORES
        # -----------------------------------------------------

        self.draw_text(
            8,
            cy - 10,
            str(self.min_val),
            COR_TEXTO
        )

        meio = (self.min_val + self.max_val) // 2

        meio_txt = str(meio)

        self.draw_text(
            cx - (len(meio_txt) * 4),
            5,
            meio_txt,
            COR_TEXTO
        )

        max_txt = str(self.max_val)

        self.draw_text(
            w - (len(max_txt) * 8) - 8,
            cy - 10,
            max_txt,
            COR_TEXTO
        )

        # -----------------------------------------------------
        # PONTEIRO
        # -----------------------------------------------------

        span = self.max_val - self.min_val

        if span <= 0:
            span = 1

        ratio = (
            self.value - self.min_val
        ) / span

        angle = math.pi - (ratio * math.pi)

        needle_r = r - 15

        px = cx + int(
            needle_r * math.cos(angle)
        )

        py = cy - int(
            needle_r * math.sin(angle)
        )

        base_w = 4

        bx1 = cx - int(
            base_w * math.sin(angle)
        )

        by1 = cy - int(
            base_w * math.cos(angle)
        )

        bx2 = cx + int(
            base_w * math.sin(angle)
        )

        by2 = cy + int(
            base_w * math.cos(angle)
        )

        for i in range(base_w * 2 + 1):

            f = i / (base_w * 2)

            x = bx1 + (bx2 - bx1) * f
            y = by1 + (by2 - by1) * f

            self.draw_line(
                int(x),
                int(y),
                px,
                py,
                COR_PONTEIRO
            )

        # -----------------------------------------------------
        # HUB
        # -----------------------------------------------------

        if self._renderer:

            hub = 8

            x = self.absolute_x + cx - hub // 2
            y = self.absolute_y + cy - hub // 2

            self._renderer.fill_rect(
                x,
                y,
                hub,
                hub,
                COR_BASE
            )

            self._renderer.draw_rect(
                x,
                y,
                hub,
                hub,
                COR_TEXTO
            )

        # -----------------------------------------------------
        # VALOR
        # -----------------------------------------------------

        txt = str(int(self.value))

        self.draw_text(
            cx - (len(txt) * 4),
            cy + 8,
            txt,
            COR_TEXTO
        )
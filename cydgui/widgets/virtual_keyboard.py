"""
cydgui.widgets.virtual_keyboard
================================

Stable on-screen keyboard for CYD GUI framework.

Fixes:
------
- Shortened control labels (^, <-, SPC, OK) to fit small screens (240x320)
- Implemented Numeric/Symbol layout toggle (123 / ABC)
- No layout rebuild inside draw() unless state changes
- Uses local coordinates correctly
- Safe hit-test
"""

from cydgui.core.widget import Widget
from cydgui.core.touch_event import TouchEvent


class VirtualKeyboard(Widget):
    """On-screen virtual keyboard."""

    # Layout Alfabético
    ROWS_ALPHA = [
        list("QWERTYUIOP"),
        list("ASDFGHJKL"),
        ["^"] + list("ZXCVBNM") + ["<-"],
        ["123", "SPC", "OK"]
    ]

    # Layout Numérico e Símbolos
    ROWS_NUM = [
        list("1234567890"),
        list("@#$_&-+()="),
        list("!?:;\"',.") + ["<-"],
        ["ABC", "SPC", "OK"]
    ]

    KEY_H = 28
    SPACING = 2

    def __init__(
        self,
        x=0,
        y=0,
        width=240,
        height=120,
        on_key=None,
        bg=0x0000,
        key_bg=0x2104,
        key_color=0xFFFF,
        accent=0x07E0,
        radius=3,
    ):
        super().__init__(x=x, y=y, width=width, height=height)

        self._on_key = on_key

        self._bg = bg
        self._key_bg = key_bg
        self._key_color = key_color
        self._accent = accent
        self._radius = radius

        self._shift = False
        self._numeric = False
        self.ROWS = self.ROWS_ALPHA  # Layout ativo

        # cached layout (LOCAL coordinates only)
        self._keys = []
        self._layout_dirty = True

    # ------------------------------------------------------------
    # Layout (ONLY when needed)
    # ------------------------------------------------------------

    def _build_layout(self):

        self._keys = []

        y = 0  # LOCAL coordinate

        for row in self.ROWS:

            n = len(row)
            key_w = (self.width // n) - self.SPACING

            x = 0  # LOCAL coordinate

            for key in row:

                self._keys.append((
                    x,
                    y,
                    key_w,
                    self.KEY_H,
                    key
                ))

                x += key_w + self.SPACING

            y += self.KEY_H + self.SPACING

        self._layout_dirty = False

    # ------------------------------------------------------------
    # Label logic
    # ------------------------------------------------------------

    def _label(self, key):
        # Retorna o símbolo de controle puro
        if key in ("^", "<-", "SPC", "OK", "123", "ABC"):
            return key

        # Aplica Shift nas letras
        return key.upper() if self._shift else key.lower()

    def _emit(self, key):
        # Trata teclas de mudança de estado interno primeiro (funciona mesmo sem on_key)
        if key == "^":
            self._shift = not self._shift
            self.invalidate()
            return
            
        if key == "123":
            self._numeric = True
            self.ROWS = self.ROWS_NUM
            self._layout_dirty = True
            self.invalidate()
            return
            
        if key == "ABC":
            self._numeric = False
            self.ROWS = self.ROWS_ALPHA
            self._layout_dirty = True
            self.invalidate()
            return

        # Se não houver callback para o input de texto, interrompe aqui
        if self._on_key is None:
            return

        if key == "SPC":
            self._on_key(" ")
            return

        if key == "<-":
            self._on_key("BACKSPACE")
            return

        if key == "OK":
            self._on_key("\n")
            return

        self._on_key(self._label(key))

    # ------------------------------------------------------------
    # Hit test (LOCAL coordinates)
    # ------------------------------------------------------------

    def _hit_test(self, x, y):

        lx = x - self.absolute_x
        ly = y - self.absolute_y

        for kx, ky, kw, kh, key in self._keys:

            if kx <= lx < kx + kw and ky <= ly < ky + kh:
                return key

        return None

    # ------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------

    def draw(self, renderer):

        if not self.visible:
            return

        if self._layout_dirty:
            self._build_layout()

        # background
        renderer.fill_rect(
            self.absolute_x,
            self.absolute_y,
            self.width,
            self.height,
            self._bg
        )

        for kx, ky, kw, kh, key in self._keys:

            label = self._label(key)

            ax = self.absolute_x + kx
            ay = self.absolute_y + ky

            # CLAMP safety (prevents ILI9341 crash)
            if ax < 0 or ay < 0:
                continue

            # Destaca botões especiais com a cor de accent
            bg = self._accent if key in ("^", "<-", "OK", "123", "ABC") else self._key_bg

            renderer.fill_round_rect(
                ax,
                ay,
                kw,
                kh,
                self._radius,
                bg
            )

            tw, th = renderer.text_size(label)

            tx = ax + (kw - tw) // 2
            ty = ay + (kh - th) // 2

            renderer.draw_text(tx, ty, label, self._key_color)

        self.validate()

    # ------------------------------------------------------------
    # Input
    # ------------------------------------------------------------

    def on_touch(self, event):

        if not self.enabled:
            return False

        if not self._keys:
            self._build_layout()

        key = self._hit_test(event.x, event.y)

        if key is None:
            return False

        if event.is_down:
            self._emit(key)
            return True

        return False

    # ------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------

    def __repr__(self):

        return f"VirtualKeyboard(x={self.x}, y={self.y}, shift={self._shift}, numeric={self._numeric})"
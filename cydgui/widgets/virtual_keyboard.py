"""
cydgui.widgets.virtual_keyboard
================================

Modern on-screen keyboard for CYD GUI framework.

Features:
---------
- Alphabetic and numeric layouts
- Variable key widths
- Floating keyboard style
- Soft shadow effect
- Shift active highlight
- Rounded buttons
- Efficient cached layout
"""

from cydgui.core.widget import Widget
from cydgui.core.touch_event import TouchEvent


class VirtualKeyboard(Widget):
    """Modern on-screen virtual keyboard."""

    __slots__ = (
        "_on_key",
        "_bg",
        "_key_bg",
        "_key_color",
        "_accent",
        "_border_color",
        "_shadow_color",
        "_shift_active",
        "_radius",
        "_shift",
        "_numeric",
        "ROWS",
        "_keys",
        "_layout_dirty",
    )

    ROWS_ALPHA = [
        list("QWERTYUIOP"),
        list("ASDFGHJKL"),
        ["^"] + list("ZXCVBNM") + ["<-"],
        ["123", "SPC", "OK"]
    ]

    ROWS_NUM = [
        list("1234567890"),
        list("@#$_&-+()="),
        list("!?:;\"',.") + ["<-"],
        ["ABC", "SPC", "OK"]
    ]

    KEY_H = 28
    SPACING = 2
    PADDING = 4

    def __init__(
        self,
        x=0,
        y=0,
        width=240,
        height=120,
        on_key=None,
        bg=0x0841,
        key_bg=0x3186,
        key_color=0xFFFF,
        accent=0x04DF,
        border_color=0xC618,
        shadow_color=0x0000,
        shift_active=0xFD20,
        radius=4,
    ):
        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height
        )

        self._on_key = on_key

        self._bg = bg
        self._key_bg = key_bg
        self._key_color = key_color
        self._accent = accent

        self._border_color = border_color
        self._shadow_color = shadow_color
        self._shift_active = shift_active

        self._radius = radius

        self._shift = False
        self._numeric = False

        self.ROWS = self.ROWS_ALPHA

        self._keys = []
        self._layout_dirty = True

    # ---------------------------------------------------------
    # Layout
    # ---------------------------------------------------------

    def _key_units(self, key):
        """Return relative width units."""

        if key == "SPC":
            return 4.0

        if key in ("123", "ABC"):
            return 1.8

        if key == "OK":
            return 1.8

        if key == "<-":
            return 1.8

        if key == "^":
            return 1.5

        return 1.0

    def _build_layout(self):
        """Build keyboard layout."""

        self._keys = []

        y = self.PADDING

        for row in self.ROWS:

            units = sum(
                self._key_units(key)
                for key in row
            )

            available_w = (
                self.width
                - (self.PADDING * 2)
                - ((len(row) - 1) * self.SPACING)
            )

            px_per_unit = available_w / units

            x = self.PADDING

            for index, key in enumerate(row):

                if index == len(row) - 1:

                    kw = (
                        self.width
                        - self.PADDING
                        - x
                    )

                else:

                    kw = int(
                        px_per_unit *
                        self._key_units(key)
                    )

                self._keys.append(
                    (
                        x,
                        y,
                        kw,
                        self.KEY_H,
                        key
                    )
                )

                x += kw + self.SPACING

            y += self.KEY_H + self.SPACING

        self._layout_dirty = False

    # ---------------------------------------------------------
    # Labels
    # ---------------------------------------------------------

    def _label(self, key):

        if key in (
            "^",
            "<-",
            "SPC",
            "OK",
            "123",
            "ABC"
        ):
            return key

        return (
            key.upper()
            if self._shift
            else key.lower()
        )

    # ---------------------------------------------------------
    # Emit
    # ---------------------------------------------------------

    def _emit(self, key):

        if key == "^":

            self._shift = not self._shift

            self.invalidate()

            return

        if key == "123":

            self._numeric = True

            self.ROWS = self.ROWS_NUM

            self._layout_dirty = True

            self.invalidate()

            if self.parent:
                self.parent.invalidate()

            return

        if key == "ABC":

            self._numeric = False

            self.ROWS = self.ROWS_ALPHA

            self._layout_dirty = True

            self.invalidate()

            if self.parent:
                self.parent.invalidate()

            return
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

        self._on_key(
            self._label(key)
        )

    # ---------------------------------------------------------
    # Hit Test
    # ---------------------------------------------------------

    def _hit_test(self, x, y):

        lx = x - self.absolute_x
        ly = y - self.absolute_y

        for kx, ky, kw, kh, key in self._keys:

            if (
                kx <= lx < kx + kw and
                ky <= ly < ky + kh
            ):
                return key

        return None

    # ---------------------------------------------------------
    # Colors
    # ---------------------------------------------------------

    def _key_background(self, key):

        if key == "^" and self._shift:
            return self._shift_active

        if key in (
            "^",
            "<-",
            "OK",
            "123",
            "ABC"
        ):
            return self._accent

        return self._key_bg

    # ---------------------------------------------------------
    # Draw
    # ---------------------------------------------------------

    def draw(self, renderer):

        if not self.visible:
            return
        renderer.fill_rect(
            self.absolute_x, 
            self.absolute_y, 
            self.width, 
            self.height, 
            self._bg
        )

        if self._layout_dirty:
            self._build_layout()

        #
        # IMPORTANT:
        # Fully clear keyboard area before redraw.
        #

        renderer.fill_rect(
            self.absolute_x,
            self.absolute_y,
            self.width,
            self.height,
            self._bg
        )

        #
        # Optional outer frame
        #

        renderer.draw_round_rect(
            self.absolute_x,
            self.absolute_y,
            self.width,
            self.height,
            self._radius + 2,
            self._border_color
        )

        for kx, ky, kw, kh, key in self._keys:

            ax = self.absolute_x + kx
            ay = self.absolute_y + ky

            bg = self._key_background(key)

            #
            # Shadow
            #

            renderer.fill_round_rect(
                ax + 1,
                ay + 1,
                kw,
                kh,
                self._radius,
                self._shadow_color
            )

            #
            # Main button
            #

            renderer.fill_round_rect(
                ax,
                ay,
                kw,
                kh,
                self._radius,
                bg
            )

            #
            # Border
            #

            renderer.draw_round_rect(
                ax,
                ay,
                kw,
                kh,
                self._radius,
                self._border_color
            )

            label = self._label(key)

            tw, th = renderer.text_size(label)

            tx = ax + ((kw - tw) // 2)
            ty = ay + ((kh - th) // 2)

            renderer.draw_text(
                tx,
                ty,
                label,
                self._key_color
            )

        self.validate()

    # ---------------------------------------------------------
    # Touch
    # ---------------------------------------------------------

    def on_touch(self, event):

        if not self.enabled:
            return False

        if not self._keys:
            self._build_layout()

        key = self._hit_test(
            event.x,
            event.y
        )

        if key is None:
            return False

        if event.is_down:

            self._emit(key)

            return True

        return False

    # ---------------------------------------------------------
    # Debug
    # ---------------------------------------------------------

    def __repr__(self):

        return (
            f"VirtualKeyboard("
            f"x={self.x}, "
            f"y={self.y}, "
            f"shift={self._shift}, "
            f"numeric={self._numeric})"
        )

    def destroy(self) -> None:
        self._on_key = None
        self._keys = []
        super().destroy()
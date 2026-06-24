"""
cydgui.widgets.slider
=====================

Horizontal slider widget.
"""

from cydgui.core.widget import Widget
from cydgui.utils.colors import Colors


class Slider(Widget):

    __slots__ = (
        "_min",
        "_max",
        "_value",
        "_thumb_width",
        "_track_color",
        "_fill_color",
        "_thumb_color",
        "_dragging",
        "_on_change",
        "_bg_color"
    )

    def __init__(
        self,
        x=0,
        y=0,
        width=120,
        height=20,
        min_value=0,
        max_value=100,
        value=0,
        thumb_width=16,
        track_color=Colors.DARK_GRAY,
        fill_color=Colors.BLUE,
        thumb_color=Colors.WHITE,
        on_change=None,
    ):
        super().__init__(x, y, width, height)

        self._min = min_value
        self._max = max_value
        self._value = value

        self._thumb_width = thumb_width

        self._track_color = track_color
        self._fill_color = fill_color
        self._thumb_color = thumb_color
        self._bg_color = Colors.BLACK

        self._dragging = False

        self._on_change = on_change

    # --------------------------------------------------
    # Value
    # --------------------------------------------------

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):

        if v < self._min:
            v = self._min

        if v > self._max:
            v = self._max

        if v == self._value:
            return

        self._value = v

        if self._on_change:
            self._on_change(v)

        self.invalidate()

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _value_to_position(self):

        span = self._max - self._min

        if span <= 0:
            return 0

        ratio = (self._value - self._min) / span

        return int(
            ratio * (self.width - self._thumb_width)
        )

    def _position_to_value(self, pos):

        usable = self.width - self._thumb_width

        if usable <= 0:
            return self._min

        if pos < 0:
            pos = 0

        if pos > usable:
            pos = usable

        ratio = pos / usable

        return int(
            self._min +
            ratio * (self._max - self._min)
        )

    def _update_from_touch(self, screen_x):

        local_x = screen_x - self.absolute_x

        pos = local_x - (self._thumb_width // 2)

        self.value = self._position_to_value(pos)

    # --------------------------------------------------
    # Drawing
    # --------------------------------------------------

    def draw(self, renderer):

        ax = self.absolute_x
        ay = self.absolute_y

        # --------------------------------------------------
        # 1. LIMPA A ÁREA DO WIDGET (ESSENCIAL)
        # --------------------------------------------------
        renderer.fill_rect(
            ax,
            ay,
            self.width,
            self.height,
            self._bg_color  # ou Colors.BLACK / Colors.DARKGREY
        )

        # --------------------------------------------------
        # 2. CONFIGURAÇÕES VISUAIS
        # --------------------------------------------------
        track_h = max(4, self.height // 4)
        track_y = ay + (self.height - track_h) // 2

        thumb_x = ax + self._value_to_position()

        # limites úteis (evita overflow visual)
        usable_width = self.width - self._thumb_width

        # --------------------------------------------------
        # 3. TRACK (TRILHA BASE)
        # --------------------------------------------------
        renderer.fill_rect(
            ax,
            track_y,
            self.width,
            track_h,
            self._track_color
        )

        # --------------------------------------------------
        # 4. FILL (PROGRESSO)
        # --------------------------------------------------
        fill_width = thumb_x - ax + (self._thumb_width // 2)

        if fill_width < 0:
            fill_width = 0
        elif fill_width > self.width:
            fill_width = self.width

        renderer.fill_rect(
            ax,
            track_y,
            fill_width,
            track_h,
            self._fill_color
        )

        # --------------------------------------------------
        # 5. THUMB (BOTÃO)
        # --------------------------------------------------
        renderer.fill_rect(
            thumb_x,
            ay,
            self._thumb_width,
            self.height,
            self._thumb_color
        )

        # opcional: borda leve do thumb (melhora leitura visual)
        # renderer.rect(thumb_x, ay, self._thumb_width, self.height, Colors.WHITE)

        # --------------------------------------------------
        # 6. FINALIZA
        # --------------------------------------------------
        self.validate()

    # --------------------------------------------------
    # Touch
    # --------------------------------------------------

    def on_touch(self, event):

        if not self.enabled:
            return False

        tx = event.x
        ty = event.y

        # Touch down
        if event.is_down:

            if self.contains(tx, ty):
                self._dragging = True
                self._update_from_touch(tx)
                return True

        # Touch move
        elif event.is_move:

            if self._dragging:
                self._update_from_touch(tx)
                return True

        # Touch up
        elif event.is_up:

            if self._dragging:
                self._dragging = False
                return True

        return False

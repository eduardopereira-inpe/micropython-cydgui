"""
cydgui.widgets.listview
=======================

Lightweight selectable list widget optimized for resistive touch displays.

Features
--------
- Single selection
- Click selection
- No drag scrolling
- External scroll buttons
- Text truncation
- Low memory usage
"""

from cydgui.core.widget import Widget


class ListView(Widget):
    """Selectable text list."""

    def __init__(
        self,
        x=0,
        y=0,
        width=120,
        height=120,
        items=None,
        row_height=24,
        bg_color=0x0000,
        text_color=0xFFFF,
        selected_color=0x07E0,
        border_color=0xFFFF,
        show_border=True,
        on_select=None,
    ):
        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height
        )

        self._items = list(items or [])

        self._row_height = max(
            12,
            row_height
        )

        self._bg_color = bg_color
        self._text_color = text_color
        self._selected_color = selected_color
        self._border_color = border_color

        self._show_border = show_border

        self._selected_index = -1

        self._first_visible = 0

        self._on_select = on_select

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def items(self):
        return self._items

    @property
    def selected_index(self):
        return self._selected_index

    @property
    def selected_item(self):

        if (
            self._selected_index < 0 or
            self._selected_index >= len(self._items)
        ):
            return None

        return self._items[
            self._selected_index
        ]

    @property
    def visible_rows(self):
        return max(
            1,
            self.height // self._row_height
        )

    # ---------------------------------------------------------
    # Data
    # ---------------------------------------------------------

    def set_items(self, items):

        self._items = list(items)

        self._selected_index = -1
        self._first_visible = 0

        self.invalidate()

    def clear(self):

        self._items = []

        self._selected_index = -1
        self._first_visible = 0

        self.invalidate()

    def add_item(self, item):

        self._items.append(
            str(item)
        )

        self.invalidate()

    # ---------------------------------------------------------
    # Scroll
    # ---------------------------------------------------------

    def scroll_up(self):

        if self._first_visible > 0:

            self._first_visible -= 1

            self.invalidate()

    def scroll_down(self):

        max_first = max(
            0,
            len(self._items) -
            self.visible_rows
        )

        if self._first_visible < max_first:

            self._first_visible += 1

            self.invalidate()

    # ---------------------------------------------------------
    # Selection
    # ---------------------------------------------------------

    def select(self, index):

        if not (
            0 <= index <
            len(self._items)
        ):
            return

        self._selected_index = index

        if self._on_select:

            try:

                self._on_select(
                    index,
                    self._items[index]
                )

            except Exception as exc:

                print(exc)

        self.invalidate()

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _truncate_text(self, text):

        max_chars = max(
            4,
            (self.width - 16) // 8
        )

        if len(text) <= max_chars:
            return text

        return (
            text[:max_chars - 3] +
            "..."
        )

    def _row_from_y(self, screen_y):

        local_y = (
            screen_y -
            self.absolute_y
        )

        row = (
            local_y //
            self._row_height
        )

        index = (
            self._first_visible +
            row
        )

        if (
            0 <= index <
            len(self._items)
        ):
            return index

        return None

    # ---------------------------------------------------------
    # Drawing
    # ---------------------------------------------------------

    def draw(self, renderer):

        if not self.visible:
            return

        x = self.absolute_x
        y = self.absolute_y

        renderer.fill_rect(
            x,
            y,
            self.width,
            self.height,
            self._bg_color
        )

        for row in range(
            self.visible_rows
        ):

            index = (
                self._first_visible +
                row
            )

            if index >= len(self._items):
                break

            row_y = (
                y +
                row *
                self._row_height
            )

            text = self._items[index]

            color = self._text_color

            if index == self._selected_index:

                text = "> " + text

                color = self._selected_color

            text = self._truncate_text(
                text
            )

            renderer.draw_text(
                x + 4,
                row_y + 4,
                text,
                color
            )

        if self._show_border:

            renderer.draw_rect(
                x,
                y,
                self.width,
                self.height,
                self._border_color
            )

        self.validate()

    # ---------------------------------------------------------
    # Touch
    # ---------------------------------------------------------

    def on_touch(self, event):

        if not self.enabled:
            return False

        if not self.contains(
            event.x,
            event.y
        ):
            return False

        if getattr(
            event,
            "type",
            None
        ) != "up":
            return True

        index = self._row_from_y(
            event.y
        )

        if index is not None:

            self.select(index)

        return True
    
    def ensure_visible(self):

        if self._selected_index < self._first_visible:

            self._first_visible = (
                self._selected_index
            )

        elif self._selected_index >= (
            self._first_visible +
            self.visible_rows
        ):

            self._first_visible = (
                self._selected_index -
                self.visible_rows + 1
            )

        self.invalidate()
    
    def move_up(self):

        if self._selected_index > 0:

            self.select(
                self._selected_index - 1
            )

            self.ensure_visible()


    def move_down(self):

        if self._selected_index < (
            len(self._items) - 1
        ):

            self.select(
                self._selected_index + 1
            )

            self.ensure_visible()
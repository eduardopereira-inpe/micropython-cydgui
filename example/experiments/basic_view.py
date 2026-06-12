from cydgui.driver import CYD
from cydgui.render.ili9341_renderer import ILI9341Renderer

from cydgui.app import App
from cydgui.core.view import View

from cydgui.widgets.label import Label
from cydgui.widgets.button import Button
from cydgui.widgets.textbox import TextBox
from cydgui.widgets.checkbox import Checkbox
from cydgui.widgets.switch import Switch
from cydgui.widgets.progressbar import ProgressBar

from cydgui.layouts.column import Column
from cydgui.layouts.row import Row

import uasyncio as asyncio


# ============================================================
# Demo View
# ============================================================

class DemoView(View):

    def build(self):

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        self.add(
            Label(
                x=0,
                y=10,
                width=240,
                height=20,
                text="Layout Test",
                align=Label.CENTER
            )
        )

        # ----------------------------------------------------
        # TextBox
        # ----------------------------------------------------

        self.textbox = TextBox(
            x=20,
            y=40,
            width=200,
            height=30
        )

        self.textbox.set_text("Ready")

        self.add(self.textbox)

        # ----------------------------------------------------
        # Column
        # ----------------------------------------------------

        self.controls = Column(
            x=20,
            y=90,
            width=200,
            height=80,
            spacing=10
        )

        self.add(self.controls)

        # ----------------------------------------------------
        # Checkbox
        # ----------------------------------------------------

        self.checkbox = Checkbox(
            text="Enable Feature",
            checked=False,
            on_change=self.on_checkbox
        )

        self.controls.add(
            self.checkbox
        )

        # ----------------------------------------------------
        # Switch
        # ----------------------------------------------------

        self.switch = Switch(
            checked=False,
            on_change=self.on_switch
        )

        self.controls.add(
            self.switch
        )

        # ----------------------------------------------------
        # Progress
        # ----------------------------------------------------

        self.progress = ProgressBar(
            x=20,
            y=200,
            width=200,
            height=15,
            value=0
        )

        self.add(
            self.progress
        )

        # ----------------------------------------------------
        # Row
        # ----------------------------------------------------

        self.buttons = Row(
            x=10,
            y=150,
            width=220,
            height=40,
            spacing=10
        )

        self.add(
            self.buttons
        )

        self.buttons.add(
            Button(
                width=100,
                height=40,
                text="Start",
                on_press=self.on_start
            )
        )

        self.buttons.add(
            Button(
                width=100,
                height=40,
                text="Reset",
                on_press=self.on_reset
            )
        )

    # ========================================================
    # Events
    # ========================================================

    def on_checkbox(self, widget, checked):

        self.textbox.set_text(
            "Checkbox ON"
            if checked
            else "Checkbox OFF"
        )

    def on_switch(self, widget, checked):

        self.textbox.set_text(
            "Switch ON"
            if checked
            else "Switch OFF"
        )

    async def animate_progress(self):

        self.textbox.set_text(
            "Running..."
        )

        await self.progress.animate_to(
            100,
            step=2,
            delay_ms=20
        )

        await asyncio.sleep(1)

        await self.progress.animate_to(
            0,
            step=2,
            delay_ms=20
        )

        self.textbox.set_text(
            "Finished"
        )

    def on_start(self, button):

        asyncio.create_task(
            self.animate_progress()
        )

    def on_reset(self, button):

        self.textbox.set_text(
            "Ready"
        )

        self.progress.set_value(
            0
        )

        self.checkbox.set_checked(
            False
        )

        self.switch.set_checked(
            False
        )


# ============================================================
# Hardware
# ============================================================

cyd = CYD()

renderer = ILI9341Renderer(
    cyd.display
)


# ============================================================
# App
# ============================================================

app = App(
    renderer=renderer,
    touch=cyd.touch
)

app.set_screen(
    DemoView()
)

app.run()
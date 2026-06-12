from cydgui.driver import CYD
from cydgui.render.ili9341_renderer import ILI9341Renderer

from cydgui.app import App

from cydgui.core.view import View

from cydgui.widgets.label import Label
from cydgui.widgets.button import Button
from cydgui.widgets.canvas import Canvas
from cydgui.widgets.textbox import TextBox
from cydgui.widgets.checkbox import Checkbox
from cydgui.widgets.switch import Switch
from cydgui.widgets.progressbar import ProgressBar

from cydgui.layouts.column import Column
from cydgui.layouts.row import Row

import uasyncio as asyncio


# ============================================================
# Main View
# ============================================================

class MainView(View):

    def build(self):

        self.add(
            Label(
                x=0,
                y=5,
                width=240,
                height=20,
                text="Main View",
                align=Label.CENTER
            )
        )

        self.textbox = TextBox(
            x=20,
            y=40,
            width=200,
            height=30
        )

        self.textbox.set_text("Ready")

        self.add(self.textbox)

        self.progress = ProgressBar(
            x=10,
            y=300,
            width=220,
            height=12,
            value=0
        )

        self.add(self.progress)

        self.controls = Column(
            x=20,
            y=90,
            width=200,
            height=80,
            spacing=8
        )

        self.add(self.controls)

        self.checkbox = Checkbox(
            text="Enable feature",
            on_change=self.on_checkbox
        )

        self.controls.add(self.checkbox)

        self.switch = Switch(
            checked=False,
            on_change=self.on_switch
        )

        self.controls.add(self.switch)

        self.buttons = Row(
            x=10,
            y=220,
            width=220,
            height=40,
            spacing=10
        )

        self.add(self.buttons)

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
                text="Settings",
                on_press=self.on_settings
            )
        )

    # --------------------------------------------------------
    # Events
    # --------------------------------------------------------

    def on_checkbox(self, widget, checked):

        self.textbox.set_text(
            "Checkbox ON" if checked else "Checkbox OFF"
        )

    def on_switch(self, widget, checked):

        self.textbox.set_text(
            "Switch ON" if checked else "Switch OFF"
        )

    async def animate_progress(self):

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

    def on_start(self, button):

        self.textbox.set_text(
            "Running..."
        )

        asyncio.create_task(
            self.animate_progress()
        )

    def on_settings(self, button):

        self.app.push(
            SettingsView()
        )


# ============================================================
# Settings View
# ============================================================

class SettingsView(View):

    def build(self):

        self.add(
            Canvas(
                x=0,
                y=0,
                width=240,
                height=320,
                bg=0x001F
            )
        )

        self.add(
            Label(
                x=0,
                y=20,
                width=240,
                height=20,
                text="Settings",
                align=Label.CENTER
            )
        )

        self.add(
            Button(
                x=60,
                y=260,
                width=120,
                height=40,
                text="Back",
                on_press=self.on_back
            )
        )

    def on_back(self, button):

        self.app.pop()


# ============================================================
# Hardware
# ============================================================

cyd = CYD()

renderer = ILI9341Renderer(
    cyd.display
)


# ============================================================
# Application
# ============================================================

app = App(
    renderer=renderer,
    touch=cyd.touch
)

app.set_screen(
    MainView()
)

app.run()
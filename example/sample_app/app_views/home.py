from cydgui.widgets.label import Label
from cydgui.widgets.button import Button
from cydgui.widgets.gauge import Gauge
from cydgui.core.view import View


try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

    
# ============================================================
# Home View
# ============================================================

class HomeView(View):

    def __init__(self, app):
        self.app = app
        super().__init__("home")

    def build(self):

        self.add(
            Label(
                x=0,
                y=40,
                width=240,
                height=20,
                text="HOME SCREEN",
                align=Label.CENTER
            )
        )

        self.gauge = Gauge(
            x=60,
            y=80,
            radius=50,
            min_value=0,
            max_value=100,
            value=50
        )

        self.add(self.gauge)

        self.add(
            Button(
                x=60,
                y=180,
                width=120,
                height=40,
                text="Gauge + Async",
                on_press=self.on_gauge_async
            )
        )

        self.add(
            Button(
                x=60,
                y=240,
                width=120,
                height=40,
                text="Settings",
                on_press=self.on_settings
            )
        )

    def on_settings(self, button):
        self.navigate("settings")

    def on_gauge_async(self, button):

        if self.gauge is not None:

            task = asyncio.create_task(self.gauge.set_value_async(75))
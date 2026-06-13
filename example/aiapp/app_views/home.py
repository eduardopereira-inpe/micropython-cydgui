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
            Button(
                x=10,
                y=10,
                width=80,
                height=30,
                text="WiFi",
                on_press=self.on_settings
            )
        )

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




    def on_settings(self, button):
        self.clear()
        self.navigate("settings")

    def on_gauge_async(self, button):
        pass
from cydgui.widgets.label import Label
from cydgui.widgets.button import Button
from cydgui.widgets.gauge import Gauge
from cydgui.core.view import View


try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

import network

    
# ============================================================
# WiFi Selection View
# ============================================================

class WiFiSelectionView(View):

    def __init__(self, app):
        self.app = app
        super().__init__("wifi_selection")
        self.networks = []


    def build(self):

        self.add(
            Label(
                x=0,
                y=40,
                width=240,
                height=20,
                text="WiFi Selection",
                align=Label.CENTER
            )
        )

        sta_if = network.WLAN(network.STA_IF)

        sta_if.active(True)
        self.networks = sta_if.scan()

        for i, net in enumerate(self.networks):
            ssid = net[0].decode('utf-8')
            self.add(
                Button(
                    x=20,
                    y=80 + i * 40,
                    width=200,
                    height=30,
                    text=ssid,
                    on_press=self.on_select_wifi
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

    def on_select_wifi(self, button):
        pass

    def on_settings(self, button):
        self.navigate("settings")

    def on_gauge_async(self, button):
        pass
from connectivity.wifi import WLAN

from cydgui.core.view import View

from cydgui.widgets.label import Label
from cydgui.widgets.button import Button
from cydgui.widgets.listview import ListView

from cydgui.utils.constants import Constants

import gc
class WiFiScanView(View):
    """WiFi network selection screen."""

    def __init__(self, app):

        self.app = app

        self._ssid_map = {}

        super().__init__("wifi_scan")

    # ---------------------------------------------------------
    # Build
    # ---------------------------------------------------------

    def build(self):

        self.add(
            Button(
                x=10,
                y=10,
                width=80,
                height=30,
                text="Home",
                on_press=self.on_home
            )
        )

        self.add(
            Label(
                x=0,
                y=45,
                width=Constants.DISPLAY_WIDTH,
                height=20,
                text="Select WiFi Network",
                align=Label.CENTER
            )
        )

        # -----------------------------------------------------
        # WiFi List
        # -----------------------------------------------------

        self.networks = ListView(
            x=10,
            y=75,
            width=180,
            height=180,
            items=[],
            on_select=self.on_network_selected
        )

        self.add(self.networks)

        # -----------------------------------------------------
        # Scroll Up
        # -----------------------------------------------------

        self.add(
            Button(
                x=200,
                y=75,
                width=30,
                height=40,
                text="^",
                on_press=self.on_scroll_up
            )
        )

        # -----------------------------------------------------
        # Scroll Down
        # -----------------------------------------------------

        self.add(
            Button(
                x=200,
                y=125,
                width=30,
                height=40,
                text="v",
                on_press=self.on_scroll_down
            )
        )

        # -----------------------------------------------------
        # Refresh Scan
        # -----------------------------------------------------

        self.add(
            Button(
                x=60,
                y=270,
                width=120,
                height=40,
                text="Refresh",
                on_press=self.on_refresh
            )
        )

        self.scan_networks()

    # ---------------------------------------------------------
    # WiFi Scan
    # ---------------------------------------------------------

    def scan_networks(self):

        try:

            WLAN.active(True)

            networks = WLAN.scan()

            items = []
            self._ssid_map = {}

            for network in networks:

                ssid = network[0]
                rssi = network[3]

                if isinstance(ssid, bytes):
                    ssid = ssid.decode()

                if not ssid:
                    continue

                display_name = (
                    "{} ({})".format(
                        ssid,
                        rssi
                    )
                )

                if display_name in self._ssid_map:
                    continue

                self._ssid_map[
                    display_name
                ] = ssid

                items.append(
                    display_name
                )

            items.sort()

            self.networks.set_items(
                items
            )

        except Exception as exc:

            print(
                "WiFi scan error:",
                exc
            )

    # ---------------------------------------------------------
    # List Navigation
    # ---------------------------------------------------------

    def on_scroll_up(
        self,
        button
    ):
        self.networks.scroll_up()

    def on_scroll_down(
        self,
        button
    ):
        self.networks.scroll_down()

    # ---------------------------------------------------------
    # Refresh
    # ---------------------------------------------------------

    def on_refresh(
        self,
        button
    ):
        self.scan_networks()

    # ---------------------------------------------------------
    # Selection
    # ---------------------------------------------------------

    def on_network_selected(
        self,
        index,
        item
    ):

        ssid = self._ssid_map.get(
            item,
            item
        )

        print(
            "Selected:",
            ssid
        )

        # Future:
        #
        # self.app.selected_ssid = ssid
        # self.navigate("wifi_settings")

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    def on_home(
        self,
        button
    ):
        self.clear()

        gc.collect()
        self.navigate("home")
from connectivity.wifi import WLAN

from cydgui.core.view import View

from cydgui.widgets.label import Label
from cydgui.widgets.button import Button
from cydgui.widgets.listview import ListView

from cydgui.utils.constants import Constants


class WiFiScanView(View):
    """WiFi network selection screen."""

    def __init__(self, app, parameters):

        self.app = app

        self._ssid_map = {}

        super().__init__(app, "wifi_scan", parameters)

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
            on_select=None
        )

        self.add(self.networks)

        # -----------------------------------------------------
        # Up
        # -----------------------------------------------------

        self.add(
            Button(
                x=200,
                y=75,
                width=30,
                height=40,
                text="^",
                on_press=self.on_up
            )
        )

        # -----------------------------------------------------
        # Down
        # -----------------------------------------------------

        self.add(
            Button(
                x=200,
                y=125,
                width=30,
                height=40,
                text="v",
                on_press=self.on_down
            )
        )

        # -----------------------------------------------------
        # Select
        # -----------------------------------------------------

        self.add(
            Button(
                x=60,
                y=270,
                width=120,
                height=40,
                text="Select",
                on_press=self.on_select
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

            if items:
                self.networks.select(0)

        except Exception as exc:

            print(
                "WiFi scan error:",
                exc
            )

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    def on_up(
        self,
        button
    ):
        self.networks.move_up()

    def on_down(
        self,
        button
    ):
        self.networks.move_down()

    # ---------------------------------------------------------
    # Confirm Selection
    # ---------------------------------------------------------

    def on_select(
        self,
        button
    ):

        item = self.networks.selected_item

        if item is None:
            return

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
        self.navigate("wifi_settings", parameters={"ssid": ssid})

    # ---------------------------------------------------------
    # Home
    # ---------------------------------------------------------

    def on_home(
        self,
        button
    ):
        self.navigate("home") 
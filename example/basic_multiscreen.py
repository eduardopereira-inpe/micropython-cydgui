from cydgui.driver import CYD
from cydgui.render.ili9341_renderer import ILI9341Renderer

from cydgui.app import App
from cydgui.core.view import View

from cydgui.widgets.label import Label
from cydgui.widgets.button import Button
from cydgui.widgets.gauge import Gauge


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

        self.add(
            Gauge(
                x=60,
                y=80,
                radius=50,
                min_value=0,
                max_value=100,
                value=50
            )
        )

        self.add(
            Button(
                x=60,
                y=180,
                width=120,
                height=40,
                text="Settings",
                on_press=self.on_settings
            )
        )

    def on_settings(self, button):
        self.navigate("settings")


# ============================================================
# Settings View
# ============================================================

class SettingsView(View):

    def __init__(self, app):
        self.app = app
        super().__init__("settings")

    def build(self):

        self.add(
            Label(
                x=0,
                y=40,
                width=240,
                height=20,
                text="SETTINGS SCREEN",
                align=Label.CENTER
            )
        )

        self.add(
            Button(
                x=60,
                y=140,
                width=120,
                height=40,
                text="Home",
                on_press=self.on_home
            )
        )

    def on_home(self, button):

        self.navigate("home")


# ============================================================
# Hardware
# ============================================================

cyd = CYD()

display = cyd.display
touch = cyd.touch

renderer = ILI9341Renderer(display)


# ============================================================
# Application
# ============================================================

app = App(
    renderer=renderer,
    touch=touch
)

app.route("home", HomeView)
app.route("settings", SettingsView)

app.navigate("home")

app.run()
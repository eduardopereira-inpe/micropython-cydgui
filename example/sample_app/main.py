from cydgui.driver import CYD
from cydgui.render.ili9341_renderer import ILI9341Renderer

from cydgui.app import App

from app_views.home import HomeView
from app_views.settings import SettingsView



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
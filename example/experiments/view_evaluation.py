from cydgui.driver import CYD
from cydgui.render.ili9341_renderer import ILI9341Renderer

from cydgui.app import App
from cydgui.core.view import View

from cydgui.widgets.label import Label
from cydgui.widgets.button import Button


# ============================================================
# Main View
# ============================================================

class MainView(View):

    def build(self):

        self.add(
            Label(
                x=0,
                y=20,
                width=240,
                height=20,
                text="View Test",
                align=Label.CENTER
            )
        )

        self.add(
            Button(
                x=60,
                y=100,
                width=120,
                height=40,
                text="Hello"
            )
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
    touch=cyd.touch,
    screen=MainView()
)

app.run()
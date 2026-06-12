from cydgui.driver import CYD
from cydgui.render.ili9341_renderer import ILI9341Renderer 

from cydgui.app import App
from cydgui.core.screen import Screen

from cydgui.widgets.button import Button
from cydgui.widgets.label import Label

cyd = CYD()

display = cyd.display

renderer = ILI9341Renderer(display)

touch = cyd.touch

screen = Screen("main")

def on_hello(button):
    print("Clicked")


screen.add(
    Label(
        x=10,
        y=40,
        width=220,
        height=(display.height // 2) - 10,
        text="Cheap Yellow Display",
        align=Label.CENTER
    )
)

screen.add(
    Button(
        x=(display.width - 120 )// 2,
        y=display.height // 2,
        width=120,
        height=40,
        text="Hello",
        on_press=on_hello
    )
)

app = App(
    renderer=renderer,
    touch=touch,
    screen=screen
)



app.run()

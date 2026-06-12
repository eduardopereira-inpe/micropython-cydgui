from cydgui.driver import CYD
from cydgui.render.ili9341_renderer import ILI9341Renderer 

from cydgui.app import App
from cydgui.core.screen import Screen

from cydgui.widgets.button import Button
from cydgui.widgets.label import Label
from cydgui.widgets.canvas import Canvas

cyd = CYD()

display = cyd.display

renderer = ILI9341Renderer(display)

touch = cyd.touch

screen = Screen("main")

def on_hello(button):
    print("Clicked")


canvas = Canvas(
    x=10,
    y=10,
    width=220,
    height=100,
    bg=0x0000,
    border_color=0xFFFF
)

screen.add(canvas)


screen.add(
    Label(
        x=10,
        y=50,
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

from cydgui.driver import CYD
from cydgui.render.ili9341_renderer import ILI9341Renderer

from cydgui.app import App
from cydgui.core.screen import Screen

from cydgui.widgets.button import Button
from cydgui.widgets.label import Label
from cydgui.widgets.canvas import Canvas
from cydgui.widgets.progressbar import ProgressBar

import uasyncio as asyncio


# ------------------------------------------------------------
# Hardware setup
# ------------------------------------------------------------
cyd = CYD()
display = cyd.display
renderer = ILI9341Renderer(display)
touch = cyd.touch

screen = Screen("main")


# ------------------------------------------------------------
# Progress Bar
# ------------------------------------------------------------
progress = ProgressBar(
    x=10,
    y=display.height - 40,
    width=220,
    height=12,
    value=0,
    min_value=0,
    max_value=100,
    bar_color=0x07E0,
    bg_color=0x0000,
    border_color=0xFFFF,
    show_border=True
)

screen.add(progress)


# ------------------------------------------------------------
# Canvas
# ------------------------------------------------------------
canvas = Canvas(
    x=10,
    y=10,
    width=220,
    height=100,
    bg=0x0000,
    border_color=0xFFFF
)

screen.add(canvas)


# ------------------------------------------------------------
# Label
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# Async demo task
# ------------------------------------------------------------
async def demo_progress():
    await asyncio.sleep(1)
    await progress.animate_to(100, step=2, delay_ms=20)
    await asyncio.sleep(1)
    await progress.animate_to(0, step=2, delay_ms=20)
    
# ------------------------------------------------------------
# Button callback (FIXED)
# ------------------------------------------------------------
def on_hello(button):
    # dispara animação sem bloquear callback
    asyncio.create_task(
        demo_progress()
    )


screen.add(
    Button(
        x=(display.width - 120) // 2,
        y=display.height // 2,
        width=120,
        height=40,
        text="Hello",
        on_press=on_hello
    )
)





# ------------------------------------------------------------
# App
# ------------------------------------------------------------
app = App(
    renderer=renderer,
    touch=touch,
    screen=screen
)


app.run()

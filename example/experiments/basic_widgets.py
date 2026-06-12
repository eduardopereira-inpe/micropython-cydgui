from cydgui.driver import CYD
from cydgui.render.ili9341_renderer import ILI9341Renderer

from cydgui.app import App
from cydgui.core.screen import Screen

from cydgui.widgets.label import Label
from cydgui.widgets.button import Button
from cydgui.widgets.textbox import TextBox
from cydgui.widgets.checkbox import Checkbox
from cydgui.widgets.switch import Switch
from cydgui.widgets.progressbar import ProgressBar

import uasyncio as asyncio


# ============================================================
# Hardware
# ============================================================

cyd = CYD()

display = cyd.display
touch = cyd.touch

renderer = ILI9341Renderer(display)


# ============================================================
# Screen
# ============================================================

screen = Screen(
    name="widgets"
)


# ============================================================
# Title
# ============================================================

title = Label(
    x=0,
    y=10,
    width=display.width,
    height=20,
    text="CYD GUI Widgets",
    align=Label.CENTER
)

screen.add(title)


# ============================================================
# TextBox
# ============================================================

textbox = TextBox(
    x=20,
    y=40,
    width=200,
    height=30
)

textbox.set_text("Ready")

screen.add(textbox)


# ============================================================
# Checkbox
# ============================================================

def on_checkbox(widget, checked):

    if checked:
        textbox.set_text("Checkbox ON")
    else:
        textbox.set_text("Checkbox OFF")


checkbox = Checkbox(
    x=20,
    y=90,
    text="Enable Feature",
    checked=False,
    on_change=on_checkbox
)

screen.add(checkbox)


# ============================================================
# Switch
# ============================================================

def on_switch(widget, checked):

    if checked:
        textbox.set_text("Switch ON")
    else:
        textbox.set_text("Switch OFF")


switch = Switch(
    x=20,
    y=130,
    checked=False,
    on_change=on_switch
)

screen.add(switch)


# ============================================================
# Progress Bar
# ============================================================

progress = ProgressBar(
    x=20,
    y=190,
    width=200,
    height=15,
    value=0
)

screen.add(progress)


# ============================================================
# Progress Animation
# ============================================================

async def animate_progress():

    textbox.set_text(
        "Running..."
    )

    await progress.animate_to(
        100,
        step=2,
        delay_ms=20
    )

    await asyncio.sleep(1)

    await progress.animate_to(
        0,
        step=2,
        delay_ms=20
    )

    textbox.set_text(
        "Finished"
    )


# ============================================================
# Button
# ============================================================

def on_start(button):

    asyncio.create_task(
        animate_progress()
    )


start_button = Button(
    x=60,
    y=240,
    width=120,
    height=40,
    text="Start",
    on_press=on_start
)

screen.add(start_button)


# ============================================================
# App
# ============================================================

app = App(
    renderer=renderer,
    touch=touch,
    screen=screen
)

app.run()
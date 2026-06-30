from machine import SPI, Pin
from ili9341 import Display
from cydgui.graphics.spritesheet import SpriteSheet
from cydgui.driver.tft_touch import TFTTouch


# -----------------------------
# DISPLAY SETUP (ILI9341)
# -----------------------------
tft_touch = TFTTouch(
    rotation=270

)

display = tft_touch.display
touch = tft_touch.touch


# -----------------------------
# SPRITESHEET SETUP
# -----------------------------

sheet = SpriteSheet(
    path="cat_spritesheet.rgb565",   # ajuste para seu storage
    frame_width=32,
    frame_height=32,
    sheet_width=160,
    sheet_height=64
)


# -----------------------------
# TEST FRAME DRAW
# -----------------------------

frame_index = 0

buf = sheet.get_frame(frame_index)

display.draw_sprite(
    buf,
    x=100,
    y=120,
    w=sheet.frame_width,
    h=sheet.frame_height
)
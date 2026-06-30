from time import ticks_ms

from cydgui.driver.ili9341 import color565
from cydgui.driver.tft_touch import TFTTouch

from cydgui.graphics.animation import Animation
from cydgui.graphics.animation_mode import AnimationMode
from cydgui.graphics.animator import Animator
from cydgui.graphics.spritesheet import SpriteSheet


# ---------------------------------------------------------
# Display setup
# ---------------------------------------------------------

tft_touch = TFTTouch(rotation=270)

display = tft_touch.display
touch = tft_touch.touch


# ---------------------------------------------------------
# SpriteSheet
# ---------------------------------------------------------

sheet = SpriteSheet(
    path="cat_spritesheet.rgb565",
    frame_width=32,
    frame_height=32,
    sheet_width=160,
    sheet_height=64,
    cache_size=8,
)


# ---------------------------------------------------------
# Animation
# ---------------------------------------------------------

animation = Animation(
    name="walk",
    frames=range(sheet.frame_count),
    fps=8,
    mode=AnimationMode.LOOP,
)


# ---------------------------------------------------------
# Animator
# ---------------------------------------------------------

animator = Animator(animation)


# ---------------------------------------------------------
# Sprite position
# ---------------------------------------------------------

x = 100
y = 120

background = color565(0, 0, 0)


# ---------------------------------------------------------
# Main loop
# ---------------------------------------------------------

try:

    while True:

        animator.update(ticks_ms())

        logical_frame = animator.frame

        sprite_frame = sheet.get_frame(logical_frame.index)

        display.fill_rectangle(
            x,
            y,
            sprite_frame.width,
            sprite_frame.height,
            background,
        )

        display.draw_sprite(
            sprite_frame.buffer,
            x,
            y,
            sprite_frame.width,
            sprite_frame.height,
        )

finally:

    sheet.close()
from time import ticks_ms

from cydgui.driver.tft_touch import TFTTouch

from cydgui.graphics.sprite import Sprite
from cydgui.graphics.spritesheet import SpriteSheet
from cydgui.graphics.sprite_atlas import SpriteAtlas
from cydgui.graphics.animation import Animation
from cydgui.graphics.animation_mode import AnimationMode


# ---------------------------------------------------------
# DISPLAY SETUP
# ---------------------------------------------------------

tft_touch = TFTTouch(rotation=270)

display = tft_touch.display
touch = tft_touch.touch


# ---------------------------------------------------------
# SPRITE SHEET
# ---------------------------------------------------------

sheet = SpriteSheet(
    path="cat_spritesheet.rgb565",
    frame_width=32,
    frame_height=32,
    sheet_width=192,
    sheet_height=96,
    cache_size=8,
)


# ---------------------------------------------------------
# SPRITE ATLAS
# ---------------------------------------------------------

atlas = SpriteAtlas()

# Idle animation (row 0)
atlas.add(
    Animation.row(
        sheet,
        name="idle",
        row=0,
        start=0,
        count=4,
        fps=3,
        mode=AnimationMode.LOOP,
    )
)

# Walk animation (row 1)
# atlas.add(
#     Animation.row(
#         sheet,
#         name="walk",
#         row=1,
#         start=0,
#         count=5,
#         fps=10,
#         mode=AnimationMode.LOOP,
#     )
# )
# 
# Jump animation (row 2)
# atlas.add(
#     Animation.row(
#         sheet,
#         name="jump",
#         row=2,
#         start=0,
#         count=4,
#         fps=12,
#         mode=AnimationMode.ONCE,
#     )
# )


# ---------------------------------------------------------
# SPRITE
# ---------------------------------------------------------

sprite = Sprite(
    sheet=sheet,
    atlas=atlas,
    x=100,
    y=120,
    opaque=True,
)


# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------

sprite.play("idle")

while True:

    sprite.update(ticks_ms())

    frame = sprite.frame

    if frame is not None:
        display.draw_sprite(
            frame.buffer,
            sprite.x,
            sprite.y,
            frame.width,
            frame.height,
        )
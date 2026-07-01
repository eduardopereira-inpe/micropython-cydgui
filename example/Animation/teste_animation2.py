from time import ticks_ms

from cydgui.driver.tft_touch import TFTTouch
from cydgui.utils.constants import Constants
from cydgui.utils.colors import Colors
from cydgui.graphics.sprite import Sprite
from cydgui.graphics.spritesheet import SpriteSheet
from cydgui.graphics.sprite_atlas import SpriteAtlas
from cydgui.graphics.animation import Animation
from cydgui.graphics.animation_mode import AnimationMode

from math import sqrt


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

# Sleeping animation (row 1)
atlas.add(
    Animation.row(
        sheet,
        name="sleeping",
        row=1,
        start=0,
        count=2,
        fps=2,
        mode=AnimationMode.LOOP,
    )
)

# Walk animation (row 2)
atlas.add(
    Animation.row(
        sheet,
        name="walk",
        row=2,
        start=0,
        count=2,
        fps=3,
        mode=AnimationMode.LOOP,
    )
)


# ---------------------------------------------------------
# SPRITE
# ---------------------------------------------------------

sprite = Sprite(
    sheet=sheet,
    atlas=atlas,
    x=100,
    y=Constants.DISPLAY_HEIGHT // 2,
    opaque=True,
)


# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------

sprite.play("walk")

sprite.set_velocity(vx=0.1, vy=0.0)
hflipt = False
vflipt = False



SPEED = 0.25   # pixels/ms


def update_velocity(sprite, target_x, target_y):

    dx = target_x - sprite.x
    dy = target_y - sprite.y

    dist = sqrt(dx * dx + dy * dy)

    if dist < 2:
        return 0.0, 0.0

    return (
        SPEED * dx / dist,
        SPEED * dy / dist,
    )

target = None
# display.fill_rectangle(0, Constants.DISPLAY_HEIGHT // 2 + 32, Constants.DISPLAY_WIDTH, Constants.DISPLAY_HEIGHT // 2 - 32 , Colors.WHITE)
is_walking = True
while True:
    sprite.update(ticks_ms())

    frame = sprite.frame

    if touch.touched:
        try:
            y, x = touch.get_touch()
            y = y - frame.height // 2
            x = x + frame.width
            
            if y > Constants.DISPLAY_HEIGHT:
                y = Constants.DISPLAY_HEIGHT
            if x > Constants.DISPLAY_WIDTH:
                x = Constants.DISPLAY_WIDTH
                
            target = (Constants.DISPLAY_WIDTH - x -1, y)
            
        except:
            pass

    if target is not None:

        vx, vy = update_velocity(
            sprite,
            target[0],
            target[1],
        )

        sprite.set_velocity(vx, vy)

        if abs(target[0] - sprite.x) < 2 and \
           abs(target[1] - sprite.y) < 2:

            sprite.set_velocity(0.0, 0.0)
            target = None

    
    if sprite.x  >= (Constants.DISPLAY_WIDTH - frame.width) or sprite.x  == 0:
        sprite.reverse_x()
        hflipt = not hflipt
        
    if sprite.y  >= (Constants.DISPLAY_HEIGHT - frame.height) or sprite.y  == 0:
        sprite.reverse_y()
        vflipt = not vflipt
        
    hflipt = not sprite.vx >= 0
    
    if (sprite.vx != 0 or sprite.vy != 0) and is_walking is False:
        sprite.play("walk")
        is_walking = True
        
        

    if (sprite.vx == 0 and sprite.vy == 0) and is_walking is True:
        sprite.play("idle")
        is_walking = False
    
        
    sprite.set_flip(horizontal=hflipt, vertical=vflipt)

    if frame is not None:
        
        
        display.draw_sprite(
            frame.buffer,
            sprite.x,
            sprite.y,
            frame.width,
            frame.height,
        )
        
#         display.fill_rectangle(sprite.x, sprite.y, frame.width, frame.height,Colors.WHITE)
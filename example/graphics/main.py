from time import ticks_ms
from math import sqrt
import random

from cydgui.driver.tft_touch import TFTTouch
from cydgui.utils.constants import Constants
from cydgui.graphics.sprite import Sprite
from cydgui.graphics.spritesheet import SpriteSheet
from cydgui.graphics.sprite_atlas import SpriteAtlas
from cydgui.graphics.animation import Animation
from cydgui.graphics.animation_mode import AnimationMode


# =========================================================
# CONFIGURAÇÕES
# =========================================================

SPEED = 0.25          # pixels/ms
IDLE_TIMEOUT = 10000  # ms


# =========================================================
# DISPLAY
# =========================================================

tft_touch = TFTTouch(rotation=270)

display = tft_touch.display
touch = tft_touch.touch


# =========================================================
# SPRITE SHEET
# =========================================================

sheet = SpriteSheet(
    path="cat_spritesheet.rgb565",
    frame_width=32,
    frame_height=32,
    sheet_width=192,
    sheet_height=96,
    cache_size=8,
)


# =========================================================
# ANIMAÇÕES
# =========================================================

atlas = SpriteAtlas()

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


# =========================================================
# SPRITE
# =========================================================

sprite = Sprite(
    sheet=sheet,
    atlas=atlas,
    x=100,
    y=Constants.DISPLAY_HEIGHT // 2,
    opaque=True,
)

sprite.play("walk")
sprite.set_velocity(vx=0.1, vy=0.0)


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def update_velocity(sprite, target_x, target_y):
    dx = target_x - sprite.x
    dy = target_y - sprite.y

    distance = sqrt(dx * dx + dy * dy)

    if distance < 2:
        return 0.0, 0.0

    return (
        SPEED * dx / distance,
        SPEED * dy / distance,
    )


def random_velocity():
    x_dir = random.randint(-1, 1)
    y_dir = random.randint(-1, 1)

    return (
        x_dir * random.random() * 0.5,
        y_dir * random.random() * 0.5,
    )


# =========================================================
# ESTADO
# =========================================================

target = None
is_walking = True

last_activity = ticks_ms()

hflip = False
vflip = False


# =========================================================
# LOOP PRINCIPAL
# =========================================================

# 
# display.load_background("./background.rgb565")
# 
# display.draw_background()
# xy_previous = None

while True:
    now = ticks_ms()

    sprite.update(now)
    frame = sprite.frame

    if frame is None:
        continue
    
#     if xy_previous is not None:
#         x, y, w, h = xy_previous
#         display.restore_background(x, y, w, h)

    # -----------------------------------------------------
    # TOUCH
    # -----------------------------------------------------

    if touch.touched:
        try:
            y, x = touch.get_touch()

            y -= frame.height // 2
            x += frame.width

            y = min(y, Constants.DISPLAY_HEIGHT)
            x = min(x, Constants.DISPLAY_WIDTH)

            target = (
                Constants.DISPLAY_WIDTH - x - 1,
                y,
            )

            last_activity = now

        except Exception:
            pass

    # -----------------------------------------------------
    # MOVIMENTO PARA ALVO
    # -----------------------------------------------------

    if target is not None:
        vx, vy = update_velocity(
            sprite,
            target[0],
            target[1],
        )

        sprite.set_velocity(vx, vy)

        if (
            abs(target[0] - sprite.x) < 2
            and abs(target[1] - sprite.y) < 2
        ):
            sprite.set_velocity(0.0, 0.0)
            target = None

    # -----------------------------------------------------
    # COLISÃO COM BORDAS
    # -----------------------------------------------------

    if (
        sprite.x >= Constants.DISPLAY_WIDTH - frame.width
        or sprite.x <= 0
    ):
        sprite.reverse_x()

    if (
        sprite.y >= Constants.DISPLAY_HEIGHT - frame.height
        or sprite.y <= 0
    ):
        sprite.reverse_y()

    # -----------------------------------------------------
    # ORIENTAÇÃO DO SPRITE
    # -----------------------------------------------------

    hflip = sprite.vx < 0

    # -----------------------------------------------------
    # ANIMAÇÕES
    # -----------------------------------------------------

    moving = sprite.vx != 0 or sprite.vy != 0

    if moving and not is_walking:
        sprite.play("walk")
        is_walking = True

    elif not moving and is_walking:

        if random.choice((True, False)):
            sprite.play("idle")
            is_walking = False
        else:
            vx, vy = random_velocity()
            sprite.set_velocity(vx, vy)

    # -----------------------------------------------------
    # MOVIMENTO AUTOMÁTICO
    # -----------------------------------------------------

    if now - last_activity > IDLE_TIMEOUT:
        last_activity = now

        vx, vy = random_velocity()
        sprite.set_velocity(vx, vy)

        if vx != 0 or vy != 0:
            sprite.play("walk")
            is_walking = True

    # -----------------------------------------------------
    # RENDER
    # -----------------------------------------------------

    sprite.set_flip(horizontal=hflip, vertical=False)

    display.draw_sprite(
        frame.buffer,
        sprite.x,
        sprite.y,
        frame.width,
        frame.height,
    )
    
#     xy_previous = (sprite.x, sprite.y, frame.width, frame.height)
    
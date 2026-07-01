"""
cydgui.behaviors.cat
====================

Cat autonomous behavior.

This module implements a simple finite-state behavior for a sprite.

Responsibilities
----------------
- Follow touch input.
- Wander randomly.
- Switch between walk and idle animations.
- Bounce on screen borders.
- Update sprite orientation.

The behavior is completely stateless externally. All runtime data
is stored inside ``widget.state``.
"""

from math import sqrt
from random import choice
from random import randint
from random import random
from time import ticks_ms

from cydgui.utils.constants import Constants


DEFAULT_SPEED = 0.25
DEFAULT_IDLE_TIMEOUT = 10000


def _random_velocity():
    """Generate a random velocity."""

    return (
        randint(-1, 1) * random() * 0.5,
        randint(-1, 1) * random() * 0.5,
    )


def _target_velocity(sprite, target, speed):
    """Compute velocity toward a target."""

    dx = target[0] - sprite.x
    dy = target[1] - sprite.y

    distance = sqrt(dx * dx + dy * dy)

    if distance < 2:
        return 0.0, 0.0

    return (
        speed * dx / distance,
        speed * dy / distance,
    )


def cat_behavior(widget):
    """Update cat behavior.

    Args:
        widget:
            SpriteWidget instance.
    """

    sprite = widget.sprite
    frame = sprite.frame

    if frame is None:
        return

    #
    # Initialize state once.
    #

    state = widget.state

    if not state:

        state["target"] = None
        state["walking"] = True
        state["last_activity"] = ticks_ms()

        state["speed"] = DEFAULT_SPEED
        state["idle_timeout"] = DEFAULT_IDLE_TIMEOUT

    now = ticks_ms()

    #
    # Touch.
    #

    touch = getattr(widget, "touch", None)

    if touch is not None and touch.touched:

        try:

            y, x = touch.get_touch()

            y -= frame.height // 2
            x += frame.width

            if y > Constants.DISPLAY_HEIGHT:
                y = Constants.DISPLAY_HEIGHT

            if x > Constants.DISPLAY_WIDTH:
                x = Constants.DISPLAY_WIDTH

            state["target"] = (
                Constants.DISPLAY_WIDTH - x - 1,
                y,
            )

            state["last_activity"] = now

        except Exception:
            pass

    #
    # Move toward target.
    #

    target = state["target"]

    if target is not None:

        vx, vy = _target_velocity(
            sprite,
            target,
            state["speed"],
        )

        sprite.set_velocity(vx, vy)

        if (
            abs(target[0] - sprite.x) < 2
            and
            abs(target[1] - sprite.y) < 2
        ):
            sprite.set_velocity(0.0, 0.0)
            state["target"] = None

    #
    # Bounce.
    #

    if (
        sprite.x <= 0
        or
        sprite.x >= Constants.DISPLAY_WIDTH - frame.width
    ):
        sprite.reverse_x()

    if (
        sprite.y <= 0
        or
        sprite.y >= Constants.DISPLAY_HEIGHT - frame.height
    ):
        sprite.reverse_y()

    #
    # Orientation.
    #

    sprite.set_flip(
        horizontal=sprite.vx < 0,
        vertical=False,
    )

    #
    # Animation.
    #

    moving = (
        sprite.vx != 0.0
        or
        sprite.vy != 0.0
    )

    if moving and not state["walking"]:

        sprite.play("walk")
        state["walking"] = True

    elif not moving and state["walking"]:

        if choice((True, False)):

            sprite.play("idle")
            state["walking"] = False

        else:

            sprite.set_velocity(
                *_random_velocity()
            )

    #
    # Random wandering.
    #

    if (
        now - state["last_activity"]
        >
        state["idle_timeout"]
    ):

        state["last_activity"] = now

        vx, vy = _random_velocity()

        sprite.set_velocity(
            vx,
            vy,
        )

        if vx != 0.0 or vy != 0.0:

            sprite.play("walk")
            state["walking"] = True
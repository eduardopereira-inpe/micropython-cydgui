import gc

from cydgui.core.view import View

from cydgui.widgets.button import Button
from cydgui.widgets.label import Label
from cydgui.widgets.clock_widget import ClockWidget
from cydgui.widgets.sprite_widget import SpriteWidget

from cydgui.graphics.sprite import Sprite
from cydgui.graphics.spritesheet import SpriteSheet
from cydgui.graphics.sprite_atlas import SpriteAtlas
from cydgui.graphics.animation import Animation
from cydgui.graphics.animation_mode import AnimationMode

from cydgui.behaviors.cat import cat_behavior

from cydgui.utils.constants import Constants


class CatView(View):
    """Animated cat demo view."""

    __slots__ = (
        "clock",
        "_clock_task",
        "cat",
        "_cat_task",
    )

    def __init__(self, app, parameters=None):
        super().__init__(app, "cat", parameters)

    # ---------------------------------------------------------
    # BUILD
    # ---------------------------------------------------------

    def build(self):
        """Build the view."""

        #
        # Header
        #

        self.add(
            Button(
                x=5,
                y=10,
                width=25,
                height=20,
                text="<",
                on_press=self.on_back,
            )
        )

        self.add(
            Label(
                x=35,
                y=10,
                width=80,
                height=20,
                text="Cat",
                align=Label.CENTER,
            )
        )

        self.clock = ClockWidget(
            x=150,
            y=10,
            width=85,
            height=20,
        )

        self.add(self.clock)

        self._clock_task = self.app.create_task(
            self.clock.start()
        )

        #
        # Sprite resources
        #

        sheet = SpriteSheet(
            path="cat_spritesheet.rgb565",
            frame_width=32,
            frame_height=32,
            sheet_width=192,
            sheet_height=96,
            cache_size=8,
        )

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

        #
        # Sprite
        #

        sprite = Sprite(
            sheet=sheet,
            atlas=atlas,
            x=(Constants.DISPLAY_WIDTH - sheet.frame_width) // 2,
            y=(Constants.DISPLAY_HEIGHT - sheet.frame_height) // 2,
            opaque=True,
        )

        sprite.play("idle")

        #
        # Sprite widget
        #

        self.cat = SpriteWidget(
            sprite=sprite,
            x=0,
            y=0,
            width=Constants.DISPLAY_WIDTH,
            height=Constants.DISPLAY_HEIGHT,
            touch=self.app.touch,
            behavior=cat_behavior,
        )

        self.add(self.cat)

        self._cat_task = self.app.create_task(
            self.cat.start()
        )

    # ---------------------------------------------------------
    # CLEANUP
    # ---------------------------------------------------------

    def destroy(self):
        """Release resources."""
        
        if self._cat_task is not None:

            try:
                self._cat_task.cancel()
            except Exception:
                pass

        self._cat_task = None

        if self._clock_task is not None:

            try:
                self._clock_task.cancel()
            except Exception:
                pass

            self._clock_task = None

        try:
            self.clock.stop()
        except Exception:
            pass

        super().destroy()

        gc.collect()

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    def on_back(self, button):
        """Return to the home view."""

        try:
            self.clock.stop()
        except Exception:
            pass

        if self.app is not None:
            self.app.navigate("home")
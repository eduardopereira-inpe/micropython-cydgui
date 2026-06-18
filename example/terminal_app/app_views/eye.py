import gc
import uasyncio as asyncio

from cydgui.core.view import View

from cydgui.widgets.button import Button
from cydgui.widgets.label import Label
from cydgui.widgets.eye import EyeWidget

from cydgui.utils.constants import Constants
from cydgui.utils.colors import Colors


class EyeView(View):

    def __init__(self, app, parameters=None):
        super().__init__(app, "eye_demo", parameters)

    # ---------------------------------------------------------
    # BUILD
    # ---------------------------------------------------------

    def build(self):

        self.add(Button(
            x=5,
            y=10,
            width=25,
            height=20,
            text="<",
            on_press=self.on_back
        ))

        self.add(Label(
            x=35,
            y=10,
            width=170,
            height=20,
            text="Eye Widget",
            align=Label.CENTER
        ))

        # -----------------------------------------------------
        # EYE
        # -----------------------------------------------------

        eye_size = 160

        self.eye = EyeWidget(
            x=(Constants.DISPLAY_WIDTH - eye_size) // 2,
            y=40,
            width=eye_size,
            height=eye_size,
            iris_color=Colors.GREEN,
            pupil_shape=EyeWidget.PUPIL_DIAMOND,
            bg=Colors.BLACK,
            interval_ms=50
        )

        self.add(self.eye)

        # -----------------------------------------------------
        # CONTROLES
        # -----------------------------------------------------

        self.add(Button(
            x=10,
            y=210,
            width=50,
            height=25,
            text="Verde",
            on_press=self.on_green
        ))

        self.add(Button(
            x=65,
            y=210,
            width=50,
            height=25,
            text="Azul",
            on_press=self.on_blue
        ))

        self.add(Button(
            x=120,
            y=210,
            width=50,
            height=25,
            text="Red",
            on_press=self.on_red
        ))

        self.add(Button(
            x=175,
            y=210,
            width=60,
            height=25,
            text="Pupil",
            on_press=self.toggle_pupil
        ))

        self.info = Label(
            x=0,
            y=180,
            width=Constants.DISPLAY_WIDTH,
            height=20,
            text="Pisca e observa...",
            align=Label.CENTER
        )

        self.add(self.info)

        # -----------------------------------------------------
        # TASKS
        # -----------------------------------------------------

        self._eye_task = self.app.create_task(
            self.eye.start()
        )

        self._wander_task = self.app.create_task(
            self.wander()
        )

    # ---------------------------------------------------------
    # MOVIMENTO AUTOMÁTICO
    # ---------------------------------------------------------

    async def wander(self):

        positions = [
            (-1.0, -1.0),
            ( 0.0, -1.0),
            ( 1.0, -1.0),
            (-1.0,  0.0),
            ( 0.0,  0.0),
            ( 1.0,  0.0),
            (-1.0,  1.0),
            ( 0.0,  1.0),
            ( 1.0,  1.0),
        ]

        idx = 0

        while True:

            dx, dy = positions[idx]

            self.eye.look_at(dx, dy)

            idx += 1

            if idx >= len(positions):
                idx = 0

            await asyncio.sleep_ms(1200)

    # ---------------------------------------------------------
    # CORES
    # ---------------------------------------------------------

    def on_green(self, button):
        self.eye.iris_color = Colors.GREEN
        self.eye.invalidate()

    def on_blue(self, button):
        self.eye.iris_color = Colors.BLUE
        self.eye.invalidate()

    def on_red(self, button):
        self.eye.iris_color = Colors.RED
        self.eye.invalidate()

    # ---------------------------------------------------------
    # PUPILA
    # ---------------------------------------------------------

    def toggle_pupil(self, button):

        if self.eye.pupil_shape == EyeWidget.PUPIL_ROUND:

            self.eye.pupil_shape = EyeWidget.PUPIL_DIAMOND

        else:

            self.eye.pupil_shape = EyeWidget.PUPIL_ROUND

        self.eye.invalidate()

    # ---------------------------------------------------------
    # CLEANUP
    # ---------------------------------------------------------

    def destroy(self):

        if hasattr(self, "_wander_task"):
            try:
                self._wander_task.cancel()
            except Exception:
                pass

        if hasattr(self, "_eye_task"):
            try:
                self._eye_task.cancel()
            except Exception:
                pass

        self.clear()

        if self.parent:
            try:
                self.parent.remove(self)
            except Exception:
                pass

        gc.collect()

    # ---------------------------------------------------------
    # NAV
    # ---------------------------------------------------------

    def on_back(self, button):

        self.destroy()
        self.navigate("home")
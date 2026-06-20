import gc
import uasyncio as asyncio

from cydgui.core.view import View

from cydgui.widgets.button import Button
from cydgui.widgets.label import Label
from cydgui.widgets.eye import EyeWidget

from cydgui.utils.constants import Constants
from cydgui.utils.colors import Colors


class EyeView(View):

    __slots__ = (
        "left_eye",
        "right_eye",
        "info",
        "_left_eye_task",
        "_right_eye_task",
        "_wander_task",
    )

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
            text="Eyes Demo",
            align=Label.CENTER
        ))

        # -----------------------------------------------------
        # EYES
        # -----------------------------------------------------

        eye_size = 25
        eye_gap = 30

        total_width = (eye_size * 2) + eye_gap
        start_x = (Constants.DISPLAY_WIDTH - total_width) // 2

        eye_y = 90

        self.left_eye = EyeWidget(
            x=start_x,
            y=eye_y,
            width=eye_size,
            height=eye_size,
            iris_color=Colors.GREEN,
            pupil_shape=EyeWidget.PUPIL_DIAMOND,
            bg=Colors.BLACK,
            interval_ms=1000
        )

        self.right_eye = EyeWidget(
            x=start_x + eye_size + eye_gap,
            y=eye_y,
            width=eye_size,
            height=eye_size,
            iris_color=Colors.GREEN,
            pupil_shape=EyeWidget.PUPIL_DIAMOND,
            bg=Colors.BLACK,
            interval_ms=1000
        )

        self.add(self.left_eye)
        self.add(self.right_eye)

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

        self._left_eye_task = self.app.create_task(
            self.left_eye.start()
        )

        self._right_eye_task = self.app.create_task(
            self.right_eye.start()
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

            # Pequena diferença entre os olhos
            self.left_eye.look_at(
                max(-1.0, min(1.0, dx - 0.05)),
                dy
            )

            self.right_eye.look_at(
                max(-1.0, min(1.0, dx + 0.05)),
                dy
            )

            idx += 1

            if idx >= len(positions):
                idx = 0

            await asyncio.sleep_ms(10000)

    # ---------------------------------------------------------
    # CORES
    # ---------------------------------------------------------

    def on_green(self, button):

        self.left_eye.iris_color = Colors.GREEN
        self.right_eye.iris_color = Colors.GREEN

        self.left_eye.invalidate()
        self.right_eye.invalidate()

    def on_blue(self, button):

        self.left_eye.iris_color = Colors.BLUE
        self.right_eye.iris_color = Colors.BLUE

        self.left_eye.invalidate()
        self.right_eye.invalidate()

    def on_red(self, button):

        self.left_eye.iris_color = Colors.RED
        self.right_eye.iris_color = Colors.RED

        self.left_eye.invalidate()
        self.right_eye.invalidate()

    # ---------------------------------------------------------
    # PUPILA
    # ---------------------------------------------------------

    def toggle_pupil(self, button):

        if self.left_eye.pupil_shape == EyeWidget.PUPIL_ROUND:

            new_shape = EyeWidget.PUPIL_DIAMOND

        else:

            new_shape = EyeWidget.PUPIL_ROUND

        self.left_eye.pupil_shape = new_shape
        self.right_eye.pupil_shape = new_shape

        self.left_eye.invalidate()
        self.right_eye.invalidate()

    # ---------------------------------------------------------
    # CLEANUP
    # ---------------------------------------------------------

    def destroy(self):

        for task_name in (
            "_wander_task",
            "_left_eye_task",
            "_right_eye_task"
        ):

            if hasattr(self, task_name):

                task = getattr(self, task_name)

                if task:

                    try:
                        task.cancel()
                    except Exception:
                        pass

        super().destroy()

        gc.collect()

    # ---------------------------------------------------------
    # NAV
    # ---------------------------------------------------------

    def on_back(self, button):
        app = self.app

        try:
            self.left_eye.stop()
        except Exception:
            pass

        try:
            self.right_eye.stop()
        except Exception:
            pass

        if app is not None:
            app.navigate("home")
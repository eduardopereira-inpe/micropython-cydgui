import gc
import uasyncio as asyncio

from cydgui.core.view import View
from cydgui.widgets.button import Button
from cydgui.widgets.label import Label
from cydgui.widgets.clock_widget import ClockWidget
from cydgui.widgets.speedometer import SpeedometerWidget
from cydgui.utils.constants import Constants
from cydgui.utils.colors import Colors


class SpeedometerView(View):

    __slots__ = (
        "clock",
        "_clock_task",
        "speedometer",
        "_speed_task",
        "info",
    )

    def __init__(self, app, parameters=None):
        super().__init__(app, "speedometer_test", parameters)

    # ---------------------------------------------------------
    # BUILD
    # ---------------------------------------------------------

    def build(self):

        self.parameters = self.parameters or {}

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        self.add(Button(
            x=10,
            y=10,
            width=25,
            height=20,
            text="<",
            on_press=self.on_back
        ))

        self.add(Label(
            x=35,
            y=10,
            width=Constants.DISPLAY_WIDTH - 140,
            height=20,
            text="Dash. Mon.",
            align=Label.CENTER
        ))

        self.clock = ClockWidget(
            x=Constants.DISPLAY_WIDTH - 85,
            y=10,
            width=80,
            height=20
        )

        self._clock_task = self.app.create_task(
            self.clock.start()
        )

        self.add(self.clock)

        # -----------------------------------------------------
        # SPEEDOMETER
        # -----------------------------------------------------

        sp_width = 240
        sp_height = 140
        sp_x = (Constants.DISPLAY_WIDTH - sp_width) // 2

        self.speedometer = SpeedometerWidget(
            x=sp_x,
            y=50,
            width=sp_width,
            height=140,
            bg=Colors.BLACK,
            border_color=Colors.DARK_GRAY,
            min_val=0,
            max_val=120
        )

        self.add(self.speedometer)

        # animação simples:
        # 0 -> 60 -> 120 -> 60 -> 0
        self._speed_task = self.app.create_task(
            self.demo_speedometer()
        )

        # -----------------------------------------------------
        # FOOTER
        # -----------------------------------------------------

        self.info = Label(
            x=0,
            y=210,
            width=Constants.DISPLAY_WIDTH,
            height=20,
            text="Demo do SpeedometerWidget",
            align=Label.CENTER
        )

        self.add(self.info)

    # ---------------------------------------------------------
    # SPEED DEMO
    # ---------------------------------------------------------

    async def demo_speedometer(self):

        sequence = (
            (0, 0),
            (60, 1250),
            (120, 1250),
            (60, 1250),
            (0, 1250),
        )

        while True:

            for value, delay_ms in sequence:

                try:
                    self.speedometer.set_value(value)
                except Exception as error:
                    print(error)
                    return

                if delay_ms > 0:
                    await asyncio.sleep_ms(delay_ms)

    # ---------------------------------------------------------
    # CLEANUP
    # ---------------------------------------------------------

    def destroy(self):

        if self._speed_task:
            try:
                self._speed_task.cancel()
            except Exception:
                pass
            self._speed_task = None

        if self._clock_task:
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
    # NAV
    # ---------------------------------------------------------

    def on_back(self, button):

        try:
            self.clock.stop()
        except Exception:
            pass

        if self.app:
            self.app.navigate("home")
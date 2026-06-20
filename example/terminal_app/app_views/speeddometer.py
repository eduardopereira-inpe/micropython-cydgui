import gc

from cydgui.core.view import View
from cydgui.widgets.button import Button
from cydgui.widgets.label import Label
from cydgui.widgets.clock_widget import ClockWidget
from cydgui.widgets.speedometer import SpeedometerWidget 
from cydgui.utils.constants import Constants
from cydgui.utils.colors import Colors


class SpeedometerView(View):
    """
    Dashboard interativo para demonstração do SpeedometerWidget.
    Gerencia o ciclo de vida do canvas assíncrono para evitar memory leaks.
    """

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
            x=20,
            y=10,
            width=Constants.DISPLAY_WIDTH - 100,
            height=20,
            text="Dashboard Monitor",
            align=Label.CENTER
        ))

        self.clock = ClockWidget(
            x=Constants.DISPLAY_WIDTH - 85,
            y=10,
            width=80,
            height=20
        )

        self._clock_task = self.app.create_task(self.clock.start())
        self.add(self.clock)

        # -----------------------------------------------------
        # SPEEDOMETER (CENTRAL FOCUS)
        # -----------------------------------------------------
        
        # Calculamos as dimensões para centralizar o velocímetro
        sp_width = 240
        sp_height = 140
        sp_x = int((Constants.DISPLAY_WIDTH - sp_width) / 2)

        self.speedometer = SpeedometerWidget(
            x=sp_x,
            y=50,
            width=sp_width,
            height=sp_height,
            bg=Colors.BLACK,
            border_color=Colors.DARK_GRAY,
            min_val=0,
            max_val=120,      # Escala de 0 a 120
            interval_ms=50    # Taxa de atualização fluida para a animação
        )

        self._speed_task = self.app.create_task(self.speedometer.start())
        self.add(self.speedometer)

        # -----------------------------------------------------
        # INFO FOOTER
        # -----------------------------------------------------

        self.info = Label(
            x=0,
            y=210,
            width=Constants.DISPLAY_WIDTH,
            height=20,
            text="Simulação de leitura em tempo real",
            align=Label.CENTER
        )

        self.add(self.info)

    # ---------------------------------------------------------
    # CLEANUP
    # ---------------------------------------------------------

    def destroy(self):
        # Cancelar a task do velocímetro de forma segura
        if hasattr(self, "_speed_task") and self._speed_task:
            try:
                self._speed_task.cancel()
            except Exception:
                pass
            self._speed_task = None

        # Cancelar a task do relógio
        if hasattr(self, "_clock_task") and self._clock_task:
            try:
                self._clock_task.cancel()
            except Exception:
                pass
            self._clock_task = None

        super().destroy()

        gc.collect()

    # ---------------------------------------------------------
    # NAV
    # ---------------------------------------------------------

    def on_back(self, button):
        app = self.app

        try:
            self.speedometer.stop()
        except Exception:
            pass

        try:
            self.clock.stop()
        except Exception:
            pass

        if app is not None:
            app.navigate("home")
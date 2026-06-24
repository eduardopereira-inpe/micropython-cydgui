import gc

from cydgui.core.view import View

from cydgui.widgets.button import Button
from cydgui.widgets.label import Label
from cydgui.widgets.slider import Slider

from cydgui.utils.constants import Constants


class SliderView(View):

    __slots__ = (
        "value_label",
        "slider",
    )

    def __init__(self, app, parameters=None):
        super().__init__(app, "slider_view", parameters)

    # ---------------------------------------------------------
    # BUILD
    # ---------------------------------------------------------

    def build(self):

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

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
            text="Teste Slider",
            align=Label.CENTER
        ))

        # -----------------------------------------------------
        # VALOR
        # -----------------------------------------------------

        self.value_label = Label(
            x=0,
            y=80,
            width=Constants.DISPLAY_WIDTH,
            height=30,
            text="Valor: 50",
            align=Label.CENTER
        )

        self.add(self.value_label)

        # -----------------------------------------------------
        # SLIDER
        # -----------------------------------------------------

        self.slider = Slider(
            x=20,
            y=140,
            width=200,
            height=30,
            min_value=0,
            max_value=100,
            value=50,
            on_change=self.on_slider_change
        )

        self.add(self.slider)

        # -----------------------------------------------------
        # FOOTER
        # -----------------------------------------------------

        self.add(Label(
            x=0,
            y=220,
            width=Constants.DISPLAY_WIDTH,
            height=20,
            text="Arraste o controle",
            align=Label.CENTER
        ))

    # ---------------------------------------------------------
    # EVENTS
    # ---------------------------------------------------------

    def on_slider_change(self, value):

        self.value_label.text = "Valor: {}".format(value)
        self.value_label.invalidate()

    # ---------------------------------------------------------
    # NAVIGATION
    # ---------------------------------------------------------

    def on_back(self, button):

        if self.app:
            self.app.navigate("home")

    # ---------------------------------------------------------
    # CLEANUP
    # ---------------------------------------------------------

    def destroy(self):

        super().destroy()
        gc.collect()
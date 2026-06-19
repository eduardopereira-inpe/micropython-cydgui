import gc
import uasyncio as asyncio

from cydgui.core.view import View
from cydgui.widgets.memory_graph import MemoryGraphWidget
from cydgui.widgets.button import Button
from cydgui.widgets.label import Label
from cydgui.widgets.clock_widget import ClockWidget
from cydgui.utils.constants import Constants
from cydgui.utils.colors import Colors


class MemoryGraphView(View):
    """
    Dedicated performance monitor view.
    No keyboard, no terminal -> maximum stability.
    """

    __slots__ = (
        "clock",
        "_clock_task",
        "graph",
        "_graph_task",
        "info",
    )

    def __init__(self, app, parameters=None):
        super().__init__(app, "memory_graph", parameters)

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
            text="Memory Monitor",
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
        # GRAPH (FULL SCREEN FOCUS)
        # -----------------------------------------------------

        self.graph = MemoryGraphWidget(
            x=10,
            y=40,
            width=Constants.DISPLAY_WIDTH - 20,
            height=180,
            bg=Colors.BLACK,
            border_color=Colors.DARK_GRAY,
            interval_ms=2000
        )

        self._graph_task = self.app.create_task(self.graph.start())
        self.add(self.graph)

        # -----------------------------------------------------
        # INFO FOOTER
        # -----------------------------------------------------

        self.info = Label(
            x=0,
            y=230,
            width=Constants.DISPLAY_WIDTH,
            height=20,
            text="Live GC memory usage",
            align=Label.CENTER
        )

        self.add(self.info)

    # ---------------------------------------------------------
    # CLEANUP
    # ---------------------------------------------------------

    def destroy(self):

        if hasattr(self, "_graph_task"):
            try:
                self._graph_task.cancel()
            except:
                pass
            self._graph_task = None

        if hasattr(self, "_clock_task"):
            try:
                self._clock_task.cancel()
            except:
                pass
            self._clock_task = None

        self.samples = []
        self.buf = None
        self.fbuf = None

        super().destroy()

        gc.collect()

    # ---------------------------------------------------------
    # NAV
    # ---------------------------------------------------------

    def on_back(self, button):
        gc.collect()
        self.navigate("home")
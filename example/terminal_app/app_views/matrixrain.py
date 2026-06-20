
import gc

from cydgui.core.view import View
from cydgui.widgets.memory_graph import MemoryGraphWidget
from cydgui.widgets.button import Button
from cydgui.widgets.label import Label
from cydgui.widgets.clock_widget import ClockWidget
from cydgui.utils.constants import Constants
from cydgui.utils.colors import Colors
from cydgui.widgets.matrixrain import MatrixRainWidget

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


class MatrixRainView(View):
    """
    Dedicated performance monitor view.
    No keyboard, no terminal -> maximum stability.
    """

    __slots__ = (

        "info",
        "matrix",
    )

    def __init__(self, app, parameters=None):
        super().__init__(app, "matrix_rain", parameters)

    def build(self):

        self.parameters = self.parameters or {}

        self.matrix = MatrixRainWidget(
            0, 0, 
            Constants.DISPLAY_WIDTH, 
            Constants.DISPLAY_HEIGHT
        )

        self.add(self.matrix)
        
        self._matrix_task = self.app.create_task(self.matrix.update())
        
    def destroy(self):

        if hasattr(self, "_matrix_task") and self._matrix_task:
            try:
                self._matrix_task.cancel()
            except Exception:
                pass
            self._matrix_task = None

        super().destroy()
        
        
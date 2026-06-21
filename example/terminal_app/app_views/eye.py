from cydgui.core.view import View
from cydgui.widgets.eye import EyeWidget
from cydgui.utils.constants import Constants


class EyeView(View):

    __slots__ = (
        "eyes",
        "_eyes_task",
    )

    def __init__(self, app, parameters=None):
        super().__init__(app, "eyes", parameters)

    def build(self):
        
        width_eyes = Constants.DISPLAY_WIDTH
        height_eyes = 150

        self.eyes = EyeWidget(0, 20, width_eyes, height_eyes)

        self.add(self.eyes)

        self._eyes_task = self.app.create_task(
            self.eyes.update()
        )

    def destroy(self):

        task = getattr(self, "_eyes_task", None)

        if task:

            try:
                task.cancel()
            except Exception:
                pass

            self._eyes_task = None

        super().destroy()

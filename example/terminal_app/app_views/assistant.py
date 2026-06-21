import gc

from cydgui.core.view import View
from cydgui.widgets.button import Button
from cydgui.widgets.label import Label
from cydgui.widgets.clock_widget import ClockWidget
from cydgui.widgets.crypto import CryptoWidget
from cydgui.widgets.eye import EyeWidget

from cydgui.utils.constants import Constants

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


class AssistantView(View):

    __slots__ = (
        "clock",
        "_clock_task",
        "crypto",
        "_crypto_task",
        "eyes",
        "_eyes_task",
        "info",
    )

    def __init__(self, app, parameters=None):
        super().__init__(app, "assistant", parameters)

    def build(self):

        self.parameters = self.parameters or {}

        # --------------------------------------------------
        # HEADER
        # --------------------------------------------------

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
            width=105,
            height=20,
            text="Assistant",
            align=Label.CENTER
        ))

        self.clock = ClockWidget(
            x=150,
            y=10,
            width=85,
            height=20
        )

        self.add(self.clock)

        self._clock_task = self.app.create_task(
            self.clock.start()
        )

        # --------------------------------------------------
        # CRYPTO STRIP
        # --------------------------------------------------

        crypto_width = 150
        crypto_height = 28

        self.crypto = CryptoWidget(
            x=(Constants.DISPLAY_WIDTH - crypto_width) // 2,
            y=38,
            width=crypto_width,
            height=crypto_height,
            interval_minutes=5,
            bg_color=0x1022
        )

        self.add(self.crypto)
        
        gc.collect()

        self._crypto_task = self.app.create_task(
            self.crypto.start()
        )
        
        

        # --------------------------------------------------
        # EYES
        # --------------------------------------------------

        self.eyes = EyeWidget(
            x=0,
            y=72,
            width=250,
            height=130
        )

        self.add(self.eyes)

        self._eyes_task = self.app.create_task(
            self.eyes.update()
        )

        # --------------------------------------------------
        # FOOTER
        # --------------------------------------------------

        self.info = Label(
            x=0,
            y=220,
            width=Constants.DISPLAY_WIDTH,
            height=20,
            text="Status: Online",
            align=Label.CENTER
        )

        self.add(self.info)

    def destroy(self):

        if self._eyes_task:
            try:
                self._eyes_task.cancel()
            except Exception:
                pass
            self._eyes_task = None

        if self._crypto_task:
            try:
                self._crypto_task.cancel()
            except Exception:
                pass
            self._crypto_task = None

        if self._clock_task:
            try:
                self._clock_task.cancel()
            except Exception:
                pass
            self._clock_task = None

        try:
            self.crypto.stop()
        except Exception:
            pass

        try:
            self.clock.stop()
        except Exception:
            pass

        super().destroy()

        gc.collect()

    def on_back(self, button):

        try:
            self.crypto.stop()
        except Exception:
            pass

        try:
            self.clock.stop()
        except Exception:
            pass

        self.app.navigate("home")
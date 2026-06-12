
from cydgui.core.view import View

from cydgui.widgets.textbox import TextBox
from cydgui.widgets.label import Label
from cydgui.widgets.button import Button
from cydgui.widgets.virtual_keyboard import VirtualKeyboard
from cydgui.utils.constants import Constants


# ============================================================
# Settings View
# ============================================================

class SettingsView(View):

    def __init__(self, app):
        self.app = app
        super().__init__("settings")

    def build(self):

        self.add(
            Label(
                x=0,
                y=40,
                width=240,
                height=20,
                text="SETTINGS SCREEN",
                align=Label.CENTER
            )
        )

        self.add(
            Button(
                x=60,
                y=60,
                width=120,
                height=40,
                text="Home",
                on_press=self.on_home
            )
        )

        # ----------------------------------------------------
        # TextBox
        # ----------------------------------------------------

        self.textbox = TextBox(
            x=20,
            y=120,
            width=200,
            height=30
        )
        self.textbox.set_text(" ")

        self.add(self.textbox)
        
        keyboard_width = Constants.DISPLAY_WIDTH 
        keyboard_height = 150

        keyboard = VirtualKeyboard(
            x=(Constants.DISPLAY_WIDTH - keyboard_width) // 2,
            y=Constants.DISPLAY_HEIGHT - keyboard_height,
            width=keyboard_width,
            height=keyboard_height,
            on_key=self.on_key
        )

        self.add(keyboard)



    def on_key(self,k):        

        if k == "BACKSPACE":
            if len(self.textbox.text) > 0 :
                self.textbox.backspace()

        else:
            if k is not None:
                self.textbox.insert(k)
     

    def on_home(self, button):

        self.navigate("home")
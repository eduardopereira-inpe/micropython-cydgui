import gc
from cydgui.core.view import View

from cydgui.widgets.textbox import TextBox
from cydgui.widgets.label import Label
from cydgui.widgets.button import Button
from cydgui.widgets.virtual_keyboard import VirtualKeyboard
from cydgui.utils.constants import Constants
# from connectivity import connect_to_wifi

# ============================================================
# WiFi Settings View (Improved Layout)
# ============================================================

class WiFiSettingsView(View):

    def __init__(self, app):
        self.app = app
        super().__init__("wifi_settings")

    def build(self):

        # ----------------------------------------------------
        # Top Navigation Button
        # ----------------------------------------------------
        self.add(
            Button(
                x=10,
                y=10,
                width=80,
                height=30,
                text="Home",
                on_press=self.on_home
            )
        )

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------
        self.add(
            Label(
                x=0,
                y=40,
                width=Constants.DISPLAY_WIDTH,
                height=20,
                text="WiFi Configuration",
                align=Label.CENTER
            )
        )

        # ====================================================
        # SSID Section
        # ====================================================
        self.add(
            Label(
                x=10,
                y=60,
                width=Constants.DISPLAY_WIDTH - 20,
                height=18,
                text="SSID",
                align=Label.LEFT
            )
        )

        self.textbox = TextBox(
            x=10,
            y=80,
            width=Constants.DISPLAY_WIDTH - 20,
            height=30
        )
        self.textbox.set_text("RedeGamer")
        self.add(self.textbox)

        # ====================================================
        # Password Section
        # ====================================================
        self.add(
            Label(
                x=10,
                y=120,
                width=Constants.DISPLAY_WIDTH - 20,
                height=18,
                text="Password",
                align=Label.LEFT
            )
        )

        self.textbox2 = TextBox(
            x=10,
            y=140,
            width=Constants.DISPLAY_WIDTH - 20,
            height=30
        )
        self.textbox2.set_text("Vick0508")
        self.add(self.textbox2)

        # ====================================================
        # Virtual Keyboard (Docked Bottom)
        # ====================================================
        keyboard_height = 140

        keyboard = VirtualKeyboard(
            x=0,
            y=Constants.DISPLAY_HEIGHT - keyboard_height,
            width=Constants.DISPLAY_WIDTH,
            height=keyboard_height,
            on_key=self.on_key
        )

        self.add(keyboard)

    # ========================================================
    # Input Handling
    # ========================================================
    def on_key(self, k):

        if self.textbox.focused and self.textbox2.focused:
            self.textbox2.blur()
            self.textbox.blur()

        if self.textbox.focused:
            target = self.textbox
            self.textbox2.blur()          
        else:
            target = self.textbox2  
            self.textbox.blur()

        

        if k == "BACKSPACE":
            if len(target.text) > 0:
                target.backspace()

        elif k == "\n":
            ssid = self.textbox.text
            password = self.textbox2.text

            gc.collect()  # Limpa memória antes de tentar conectar

#             if ssid and password:
#                 
#                 success = connect_to_wifi(ssid, password)
# 
#                 if success:
#                     self.textbox2.set_text("Connected!")
#                 else:
#                     self.textbox2.set_text("Connection Failed")
        else:
            if k is not None:
                target.insert(k)

    # ========================================================
    # Navigation
    # ========================================================
    def on_home(self, button):
        self.clear()
        self.navigate("home")
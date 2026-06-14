import gc

from cydgui.core.view import View

from cydgui.widgets.label import Label
from cydgui.widgets.button import Button
from cydgui.widgets.canvas import Canvas
from cydgui.widgets.virtual_keyboard import VirtualKeyboard
from cydgui.widgets.textbox import TextBox

from cydgui.utils.constants import Constants
from cydgui.utils.colors import Colors


class TerminalView(View):
    """Simple terminal application."""

    MAX_LINES = 10

    def __init__(self, app, parameters=None):
        self.lines = []

        super().__init__(
            app,
            "terminal",
            parameters
        )

    # ---------------------------------------------------------
    # Build
    # ---------------------------------------------------------

    def build(self):

        if self.parameters is None:
            self.parameters = {}

        self.add(
            Button(
                x=10,
                y=10,
                width=20,
                height=20,
                text="<",
                on_press=self.on_back
            )
        )

        self.add(
            Label(
                x=0,
                y=10,
                width=Constants.DISPLAY_WIDTH,
                height=20,
                text="Terminal",
                align=Label.CENTER
            )
        )

        # -----------------------------------------------------
        # Terminal output
        # -----------------------------------------------------

        self.canvas = Canvas(
            x=10,
            y=40,
            width=Constants.DISPLAY_WIDTH - 20,
            height=110,
            bg=Colors.BLACK,
            border_color=Colors.DARK_GRAY,
            touchable=False,
            on_draw=self.draw_terminal
        )

        self.add(self.canvas)

        # -----------------------------------------------------
        # Command input
        # -----------------------------------------------------

        self.textbox = TextBox(
            x=10,
            y=155,
            width=Constants.DISPLAY_WIDTH - 20,
            height=28
        )
        
        self.textbox.set_text("")

        self.add(self.textbox)

        # -----------------------------------------------------
        # Virtual keyboard
        # -----------------------------------------------------

        self.keyboard = VirtualKeyboard(
            x=10,
            y=188,
            width=Constants.DISPLAY_WIDTH - 20,
            height=122,
            on_key=self.on_key
        )

        self.add(self.keyboard)

        # -----------------------------------------------------
        # Startup messages
        # -----------------------------------------------------

        self.println("CYD Terminal")
        self.println("Type 'help'")
        self.println("")

    # ---------------------------------------------------------
    # Terminal output
    # ---------------------------------------------------------

    def println(self, text):

        text = str(text)

        if text == "":
            text = " "

        self.lines.append(text)

        while len(self.lines) > self.MAX_LINES:
            self.lines.pop(0)

        self.canvas.invalidate()

    # ---------------------------------------------------------
    # Canvas drawing
    # ---------------------------------------------------------

    def draw_terminal(self, canvas):

        y = 4

        for line in self.lines:

            text = str(line)

            if not text:
                y += 10
                continue

            canvas.draw_text(
                4,
                y,
                text,
                Colors.GREEN
            )

            y += 10
    # ---------------------------------------------------------
    # Command execution
    # ---------------------------------------------------------

    def execute(self, command):
        """Execute terminal command."""

        command = command.strip()

        if not command:
            return

        if command == "help":

            self.println("Commands:")
            self.println("help")
            self.println("mem")
            self.println("gc")
            self.println("clear")
            self.println("about")

        elif command == "mem":

            gc.collect()

            self.println(
                "Free: {}".format(
                    gc.mem_free()
                )
            )

        elif command == "gc":

            before = gc.mem_free()

            gc.collect()

            after = gc.mem_free()

            self.println(
                "Collected: {}".format(
                    after - before
                )
            )

            self.println(
                "Free: {}".format(after)
            )

        elif command == "clear":

            self.lines.clear()

        elif command == "about":

            self.println("CYD GUI")
            self.println("MicroPython")
            self.println("ESP32 CYD")
            self.println("240x320")

        else:

            self.println(
                "Command not found:"
            )

            self.println(command)

    # ---------------------------------------------------------
    # Keyboard handler
    # ---------------------------------------------------------

    def on_key(self, key):

        if key is None:
            return

        if key == "BACKSPACE":

            if self.textbox.text:
                self.textbox.backspace()

            return

        if key == "\n":

            command = self.textbox.text.strip()

            if command:

                self.println(
                    "> {}".format(command)
                )

                self.execute(command)

            self.textbox.set_text("")

            gc.collect()

            return

        self.textbox.insert(key)

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    def on_back(self, button):

        self.clear()

        gc.collect()

        self.navigate("home")
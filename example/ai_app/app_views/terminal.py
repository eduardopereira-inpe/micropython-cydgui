import gc
import uasyncio as asyncio

from cydgui.core.view import View

from cydgui.widgets.button import Button
from cydgui.widgets.canvas import Canvas
from cydgui.widgets.virtual_keyboard import VirtualKeyboard
from cydgui.widgets.textbox import TextBox
from cydgui.widgets.label import Label

from cydgui.utils.constants import Constants
from cydgui.utils.colors import Colors

from ullmtools import (
    OpenAI
)


from ullmtools import (
    ChatService
)

from ullmtools.tools import (
    TurnOnOffLedTool,
    LocalTimeTool,
    LocalDateTimeTool,
    Scheduler,
    ScheduleEventTool,
    GetLatLonTool,
    GetWeatherTool
)

from udotenv.dotenv import load_dotenv


# ============================================================
# LLM Tools
# ============================================================

def create_tools():
    llm = OpenAI(
        api_key=API_KEY
    )
    scheduler = Scheduler(
        tool_executor=
            llm.execute_tool
    )

    llm.set_scheduler(
        scheduler
    )

    schedule_event_tool = ScheduleEventTool(
        scheduler
    )

    turn_onoff_led = TurnOnOffLedTool(pin=0)
    get_local_time = LocalTimeTool()
    get_local_datetime = LocalDateTimeTool()
    get_lat_lon = GetLatLonTool()
    get_weather = GetWeatherTool()

    # ------------------------------
    # Register Tools
    # ------------------------------

    llm.register_tool(tool=schedule_event_tool)

    # self.llm.register_tool(
    #     tool=GetTemperatureTool()
    # )
    
    llm.register_tool(tool=turn_onoff_led)
    
    llm.register_tool(tool=get_local_time)

    llm.register_tool(tool=get_local_datetime)

    llm.register_tool(tool=get_lat_lon)

    llm.register_tool(tool=get_weather)

    # ------------------------------

    callback = (
        lambda message: print(message)
    )
    

    chat = ChatService(
        llm=llm,
        callback=callback
    )
    
    return chat, llm



config = load_dotenv("env.txt")

API_KEY = config.get("API_KEY")

CHAT, LLM = create_tools()

class TerminalView(View):
    """Simple terminal application."""

    MAX_LINES = 10

    def __init__(self, app,  parameters={"chat": CHAT, "llm": LLM}):
        self.lines = []
        self._question_task = None

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
            
            self.get_question(command)

    async def _ask_and_print(self, question):
        """Ask the chat service without blocking the UI loop."""
        try:
            chat = self.parameters.get("chat") if self.parameters else None
            llm = self.parameters.get("llm") if self.parameters else None

            if chat is None or llm is None:
                self.println("AI service unavailable")
                return

            response = await chat.ask(
                question,
                tools=llm.get_tools_schema()
            )

            if response is None:
                self.println("No response")
                return

            text = str(response)
            for line in text.split("\n"):
                self.println(line)
        except Exception as error:
            self.println("AI error: {}".format(error))

    # ---------------------------------------------------------
    # Keyboard handler
    # ---------------------------------------------------------
    
    def get_question(self, question:str):
        app = self.app

        if self._question_task is not None:
            try:
                self._question_task.cancel()
            except Exception:
                pass
            self._question_task = None

        if app is not None:
            self._question_task = app.create_task(self._ask_and_print(question))
        else:
            self._question_task = asyncio.create_task(self._ask_and_print(question))


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
        app = self.app

        if self._question_task is not None:
            try:
                self._question_task.cancel()
            except Exception:
                pass
            self._question_task = None

        if app is not None:
            app.navigate("home")

    def destroy(self):
        if self._question_task is not None:
            try:
                self._question_task.cancel()
            except Exception:
                pass
            self._question_task = None

        super().destroy()
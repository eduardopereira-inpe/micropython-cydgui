import gc
from connectivity.wifi import connect_to_wifi, WLAN

from cydgui.render.ili9341_renderer import ILI9341Renderer
from cydgui.app import App

from cydgui.driver.tft_touch import TFTTouch
from app_views.home import HomeView
from app_views.terminal import TerminalView

from udotenv.dotenv import load_dotenv


from ullmtools import (
    OpenAI
)


from ullmtools import (
    ChatService
)

from ullmtools.tools import (
    # GetTemperatureTool,
    TurnOnOffLedTool,
    LocalTimeTool,
    LocalDateTimeTool,
    Scheduler,
    ScheduleEventTool,
    DisplayMessageTool, 
    GetLatLonTool,
    GetWeatherTool

    
)

gc.collect()
config = load_dotenv("env.txt")

API_KEY = config.get("API_KEY")
SSID = config.get("WIFI_SSID")
PASSWORD = config.get("WIFI_PASS")

connect_to_wifi(ssid=SSID, password=PASSWORD, verbose=True)

if WLAN.isconnected():

    ip = WLAN.ifconfig()[0]
else:
    ip = '-'


gc.collect()

# ============================================================
# Hardware
# ============================================================

tft_touch = TFTTouch()
display = tft_touch.display
touch = tft_touch.touch

renderer = ILI9341Renderer(display)


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

    turn_onoff_led = TurnOnOffLedTool()
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


# ============================================================
# Application
# ============================================================

gc.collect()
app = App(
    renderer=renderer,
    touch=touch
)


chat, llm = create_tools()

question = await question_task


app.route("home", HomeView)
app.route("terminal", TerminalView, parameters={"chat": chat, "llm": llm})

app.navigate("home", parameters={"ssid": SSID, "ip": ip })

gc.collect()

app.run()

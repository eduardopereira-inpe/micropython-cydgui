import gc

from cydgui.core.view import View
from cydgui.widgets.label import Label
from cydgui.widgets.button import Button
from cydgui.widgets.clock_widget import ClockWidget
from cydgui.widgets.weather import WeatherWidget

from cydgui.utils.tools import get_lat_lon_from_my_ip
from cydgui.utils.constants import Constants
from cydgui.utils.colors import Colors

from cydgui.bl_state import BlState

import uasyncio as asyncio


class AssistantView(View):
    
    __slots__ = (
        "clock",
        "_clock_task",
        "_weather_task",
        "_startup_task",
        "weather",
        "info",
        "verbose",
        "bl_state",
        "_bl_task"
        )
    
    #Ponto de Atenção
    def __init__(self, app, parameters=None, verbose=True):
        # parameters é um dicionário
        # seu foco é transmitir dados entre views.
        # Usado como armazenador de estado entre uma
        # View e outra.
        # Atributos extras devem ser declarados
        # antes do super, pois o build é chamado no init
        # da classe mãe.
        
        self.verbose = verbose
        super().__init__(app, "assistant", parameters)
        
    def build(self):
        self.parameters = self.parameters or {}
        
        # Alterar de Acordo com sua configuração
        
        self.bl_state = BlState(
            pin_num=Constants.BL_PIN,
            pin_btn=Constants.BL_BTN_PIN
        )
        
        
        self._bl_task = self.app.create_task(
                self.bl_state.monitor()
            )
        
        self.add(
            Button(
                x=5,
                y=5,
                width=25,
                height=20,
                text="<",
                on_press=self.on_back
                )
            )
        
        
        self.add(
            Label(
                    x=35,
                    y=5,
                    width=105,
                    height=20,
                    text="Assistant",
                    align=Label.CENTER
                )
            )
        
        self.clock = ClockWidget(
                x=150,
                y=5,
                width=85,
                height=20
            )
        
        self.add(self.clock)
        
        # Criando rotina concorrente para rodar o relógio
        self._clock_task = self.app.create_task(
                self.clock.start()
            )
        
        weather_width = 230
        weater_height = 150
        
        self.weather = WeatherWidget(
                # Garante que está no centro da tela, em x
                x=(Constants.DISPLAY_WIDTH - weather_width) // 2,
                y=125,
                width=weather_width,
                height=weater_height,
                api_key=self.parameters.get("api_key"),
                bg_color=Colors.NAVY,
                interval_minutes=15,
                lat=0,
                lon=0,
            )
        self.add(self.weather)
        
        self.info = Label(
                x=0,
                y=295,
                width=Constants.DISPLAY_WIDTH,
                height=20,
                text="Inicializando...",
                align=Label.CENTER            
            )
        
        self.add(self.info)
        
        self._startup_task = self.app.create_task(
                self._startup_routine()
            )
        
    def _log(self, msg:str):
        if self.verbose is True:
            print(f"[AssistantView] {msg}")
        
    
    async def _startup_routine(self):
        
        # Aguardar um pouco para garantir limpeza de
        # Memória, antes de pegar informações da Web
        
        gc.collect()        
        await asyncio.sleep_ms(100)
        
        try:
            
            if (
                    self.parameters.get("lat") is not None
                    and
                    self.parameters.get("lon") is not None
                ):
                
                self.weather.lat = self.parameters.get("lat")
                self.weather.lon = self.parameters.get("lon")
            else:
                self.info.text= "Searching for Location..."
                
                await asyncio.sleep_ms(50)
                
                lat_lon = get_lat_lon_from_my_ip()
                if lat_lon and lat_lon.get("Error") is None:
                    self.weather.lat = lat_lon["Latitude"]
                    self.weather.lon = lat_lon["Longitude"]
                
                
        
        except Exception as e:
            self._log(e)
            self.info.text = "Get IP info Error"
            
        self.info.text = "Update from OpenWeatherMap"
        
        self._weather_task = self.app.create_task(
                self.weather.start()
            )
        
    def destroy(self):
        # Importante, para garantir limpeza de memória
        
        if hasattr(self, "_startup_task") and self._startup_task:
            try:
                self._startup_task.cancel()
            except:
                pass
            del self._startup_task
            self._startup_task = None
            
        if hasattr(self, "_weather_task") and self._weather_task:
            try:
                self._weather_task.cancel()
            except Exception:
                pass
            
            del self._weather_task
            self._weather_task = None
            
        if hasattr(self, "_clock_task") and self._clock_task:
            try:
                self._clock_task.cancel()
            except Exception:
                pass
            del self._clock_task
            self._clock_task = None
            
        if hasattr(self, "_bl_task") and self._bl_task:
            try:
                self._bl_task.cancel()
            except Exception:
                pass
            
            del self._bl_task
            self._bl_task = None
            
        super().destroy
        gc.collect()
        
    def on_back(self, button):
        self.app.navigate("vboot")
        
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
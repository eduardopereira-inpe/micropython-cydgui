import gc
import urequests
import uasyncio as asyncio

from cydgui.widgets.async_canvas import AsyncCanvas
from cydgui.utils.colors import Colors


class CryptoWidget(AsyncCanvas):
    """
    Widget compacto para exibir:

    - Bitcoin (BRL)
    - Dólar (BRL) via USDTBRL

    Layout:
    ╭─────────╮ ╭────────╮
    │ ₿ 642K  │ │ $ 5.42 │
    ╰─────────╯ ╰────────╯
    """

    __slots__ = (
        "_btc",
        "_usd",
    )

    # API unificada para trazer os dois preços em uma única requisição HTTP
    API_URL = 'https://api.binance.com/api/v3/ticker/price?symbols=["BTCBRL","USDTBRL"]'

    def __init__(
        self,
        x,
        y,
        width=150,
        height=28,
        interval_minutes=5,
        bg_color=Colors.BLACK,
        **kwargs
    ):
        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            interval_ms=interval_minutes * 60 * 1000,
            bg=bg_color,
            **kwargs
        )

        self._btc = "--"
        self._usd = "--"

    # ---------------------------------------------------------
    # HTTP
    # ---------------------------------------------------------

    def _fetch_json(self, url):
        response = None
        headers = {
            "User-Agent": "CYD-ESP32/1.0 (cydgui CryptoWidget)"
        }

        try:
            response = urequests.get(url, headers=headers)
            
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print("Binance Rate Limit atingido!")
                return "429"
        except Exception as error:
            print(error)
        finally:
            if response:
                print(response.text)
            
                try:
                    response.close()
                except Exception:
                    pass
        return None

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    async def update_async(self):
        gc.collect()
        
        await asyncio.sleep_ms(1000)

        try:
            data = self._fetch_json(self.API_URL)

            if data == "429":
                self._btc = "Wait"
                self._usd = "Wait"
                return

            if data and isinstance(data, list):
                # A Binance retorna uma lista de dicionários planos: 
                # [{'symbol': 'BTCBRL', 'price': '365000.00'}, {'symbol': 'USDTBRL', 'price': '5.42'}]
                for item in data:
                    symbol = item.get("symbol")
                    price_str = item.get("price")
                    
                    if not price_str:
                        continue
                        
                    value = float(price_str)

                    if symbol == "BTCBRL":
                        if value >= 1000000:
                            self._btc = str(round(value / 1000000, 1)) + "M"
                        elif value >= 1000:
                            self._btc = str(int(value / 1000)) + "K"
                        else:
                            self._btc = str(int(value))

                    elif symbol == "USDTBRL":
                        self._usd = "{:.2f}".format(value)

            else:
                # Caso o parse falhe ou venha vazio
                self._btc = "--"
                self._usd = "--"

        except Exception:
            self._btc = "Err"
            self._usd = "Err"

        gc.collect()

    # ---------------------------------------------------------
    # ROUNDBOX COM SOMBRA
    # ---------------------------------------------------------

    def _draw_shadow_round_box(
        self,
        x,
        y,
        w,
        h,
        radius,
        bg_color,
        border_color,
        shadow_color=0x2104,
        shadow_offset=2
    ):
        r = self.renderer

        # -------------------------
        # SOMBRA
        # -------------------------
        sx = x + shadow_offset
        sy = y + shadow_offset

        r.fill_rect(sx + radius, sy, w - radius * 2, h, shadow_color)
        r.fill_rect(sx, sy + radius, radius, h - radius * 2, shadow_color)
        r.fill_rect(sx + w - radius, sy + radius, radius, h - radius * 2, shadow_color)

        r.fill_circle(sx + radius, sy + radius, radius, shadow_color)
        r.fill_circle(sx + w - radius - 1, sy + radius, radius, shadow_color)
        r.fill_circle(sx + radius, sy + h - radius - 1, radius, shadow_color)
        r.fill_circle(sx + w - radius - 1, sy + h - radius - 1, radius, shadow_color)

        # -------------------------
        # CAIXA PRINCIPAL
        # -------------------------
        r.fill_rect(x + radius, y, w - radius * 2, h, bg_color)
        r.fill_rect(x, y + radius, radius, h - radius * 2, bg_color)
        r.fill_rect(x + w - radius, y + radius, radius, h - radius * 2, bg_color)

        r.fill_circle(x + radius, y + radius, radius, bg_color)
        r.fill_circle(x + w - radius - 1, y + radius, radius, bg_color)
        r.fill_circle(x + radius, y + h - radius - 1, radius, bg_color)
        r.fill_circle(x + w - radius - 1, y + h - radius - 1, radius, bg_color)

        r.draw_rect(x, y, w, h, border_color)

    # ---------------------------------------------------------
    # DRAW BITCOIN
    # ---------------------------------------------------------

    def _draw_bitcoin_icon(self, x, y, color=Colors.ORANGE):
        r = self.renderer
        r.draw_text(x, y, "B", color)
        r.draw_line(x + 2, y - 1, x + 2, y + 9, color)
        r.draw_line(x + 6, y - 1, x + 6, y + 9, color)

    # ---------------------------------------------------------
    # DRAW
    # ---------------------------------------------------------

    def on_draw(self):
        if not self.renderer:
            return

        ax = self.absolute_x
        ay = self.absolute_y

        btc_w = 74
        usd_w = 64
        box_h = 24
        radius = 6

        btc_x = ax
        usd_x = ax + btc_w + 8

        # -----------------------------------------------------
        # BTC
        # -----------------------------------------------------
        self._draw_shadow_round_box(
            btc_x, ay, btc_w, box_h, radius, 0x2965, Colors.DARK_GRAY
        )
        self._draw_bitcoin_icon(btc_x + 7, ay + 7)
        self.renderer.draw_text(btc_x + 22, ay + 7, self._btc, Colors.WHITE)

        # -----------------------------------------------------
        # USD
        # -----------------------------------------------------
        self._draw_shadow_round_box(
            usd_x, ay, usd_w, box_h, radius, 0x1A63, Colors.DARK_GRAY
        )
        self.renderer.draw_text(usd_x + 8, ay + 7, "$", Colors.GREEN)
        self.renderer.draw_text(usd_x + 20, ay + 7, self._usd, Colors.WHITE)

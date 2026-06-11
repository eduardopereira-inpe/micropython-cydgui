"""
cydgui.utils.colors
===================

Predefined colour constants in 16-bit RGB565 format and conversion helpers.

RGB565 packs a colour into two bytes:
- Bits 15–11 : Red   (5 bits)
- Bits 10–5  : Green (6 bits)
- Bits 4–0   : Blue  (5 bits)

This is the native pixel format for the ILI9341 and many other TFT
controllers, making these constants zero-cost: no conversion is needed before
writing to the display.

Usage
-----
::

    from cydgui.utils.colors import Colors

    RED = Colors.RED          # 0xF800
    custom = Colors.rgb(255, 128, 0)  # orange in RGB565
"""


class Colors:
    """Namespace for RGB565 colour constants and conversion helpers."""

    # ------------------------------------------------------------------
    # Basic colours
    # ------------------------------------------------------------------

    BLACK   = 0x0000
    WHITE   = 0xFFFF
    RED     = 0xF800
    GREEN   = 0x07E0
    BLUE    = 0x001F
    YELLOW  = 0xFFE0
    CYAN    = 0x07FF
    MAGENTA = 0xF81F
    ORANGE  = 0xFD20
    GRAY    = 0x8410
    DARK_GRAY  = 0x4208
    LIGHT_GRAY = 0xC618

    # ------------------------------------------------------------------
    # Conversion helpers
    # ------------------------------------------------------------------

    @staticmethod
    def rgb(r: int, g: int, b: int) -> int:
        """Convert 8-bit R, G, B values to a 16-bit RGB565 integer.

        Parameters
        ----------
        r, g, b:
            Colour components in the range 0–255.

        Returns
        -------
        int
            16-bit RGB565 colour value.

        TODO: implement conversion
              rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        """
        pass

    @staticmethod
    def from_rgb565(color: int) -> tuple:
        """Unpack a 16-bit RGB565 colour into (r8, g8, b8) 8-bit components.

        TODO: implement unpacking
        """
        pass

    @staticmethod
    def blend(color_a: int, color_b: int, alpha: int) -> int:
        """Linear blend between *color_a* and *color_b*.

        Parameters
        ----------
        alpha:
            Blend factor 0–255.  0 → color_a, 255 → color_b.

        TODO: implement per-channel linear interpolation in RGB565
        """
        pass

"""
cydgui.utils.colors
===================

RGB565 color definitions used throughout the cydgui framework.

All values are compatible with ILI9341 displays and most
MicroPython display drivers.

References
----------
RGB565 format:

RRRRRGGGGGGBBBBB
"""

class Colors:
    """Common RGB565 color constants."""

    # ---------------------------------------------------------
    # Basic colors
    # ---------------------------------------------------------

    BLACK = 0x0000
    WHITE = 0xFFFF

    RED = 0xF800
    GREEN = 0x07E0
    BLUE = 0x001F

    YELLOW = 0xFFE0
    CYAN = 0x07FF
    MAGENTA = 0xF81F

    # ---------------------------------------------------------
    # Gray scale
    # ---------------------------------------------------------

    DARK_GRAY = 0x4208
    GRAY = 0x8410
    LIGHT_GRAY = 0xC618

    # ---------------------------------------------------------
    # Orange / Brown
    # ---------------------------------------------------------

    ORANGE = 0xFD20
    BROWN = 0xA145

    # ---------------------------------------------------------
    # Purple / Pink
    # ---------------------------------------------------------

    PURPLE = 0x8010
    PINK = 0xFC18

    # ---------------------------------------------------------
    # Additional colors
    # ---------------------------------------------------------

    NAVY = 0x000F
    TEAL = 0x0410
    OLIVE = 0x8400

    SILVER = 0xC618
    MAROON = 0x8000

    LIME = 0x07E0
    AQUA = 0x07FF
    FUCHSIA = 0xF81F

    # ---------------------------------------------------------
    # CYD-friendly colors
    # ---------------------------------------------------------

    BACKGROUND = BLACK

    PRIMARY = BLUE
    SECONDARY = DARK_GRAY

    SUCCESS = GREEN
    WARNING = YELLOW
    ERROR = RED

    TEXT = WHITE

    BORDER = LIGHT_GRAY

    PANEL = DARK_GRAY

    DISABLED = GRAY

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @staticmethod
    def rgb(
        red: int,
        green: int,
        blue: int
    ) -> int:
        """
        Convert RGB888 to RGB565.

        Args:
            red: 0-255
            green: 0-255
            blue: 0-255

        Returns:
            RGB565 color.
        """

        return (
            ((red & 0xF8) << 8) |
            ((green & 0xFC) << 3) |
            (blue >> 3)
        )

    @staticmethod
    def from_rgb(
        red: int,
        green: int,
        blue: int
    ) -> int:
        """
        Alias for rgb().

        Args:
            red: 0-255
            green: 0-255
            blue: 0-255

        Returns:
            RGB565 color.
        """

        return Colors.rgb(
            red,
            green,
            blue
        )
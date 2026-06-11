"""
cydgui.core.theme
=================

Visual style definition for the entire application.

A ``Theme`` aggregates colours, font references, spacing constants, and any
other visual parameters that widgets read when they draw themselves.  Widgets
receive a theme reference from the renderer (or directly from the app) so they
never need to hard-code colours.

Design notes
------------
- Colours are stored as 16-bit RGB565 integers (native format for ILI9341 and
  similar displays).
- Font references are driver-agnostic: a font is anything with an ``id`` that
  the concrete renderer can interpret.
- Only one theme is active at a time; it is owned by ``App``.
- Themes are designed to be swapped at runtime (e.g., day / night mode).

See also
--------
:mod:`cydgui.utils.colors` for colour helper utilities.
:mod:`cydgui.utils.constants` for default values.
"""

from cydgui.utils.colors import Colors


class FontRef:
    """A driver-agnostic reference to a font resource.

    Parameters
    ----------
    name:
        Human-readable font name (e.g. ``"default"``, ``"monospace"``).
    size:
        Font size in points or pixel height, depending on the renderer.
    """

    def __init__(self, name: str = "default", size: int = 12) -> None:
        # TODO: store name and size
        pass


class Theme:
    """Defines the visual style for the entire application.

    All colour attributes are 16-bit RGB565 integers unless noted otherwise.

    Parameters
    ----------
    background:
        Screen / window background colour.
    foreground:
        Default text / foreground colour.
    primary:
        Primary accent colour (e.g., button fill).
    secondary:
        Secondary accent colour.
    border:
        Default border / outline colour.
    font:
        Default :class:`FontRef` for body text.
    font_title:
        :class:`FontRef` for heading / title text.
    """

    def __init__(
        self,
        background: int = Colors.BLACK,
        foreground: int = Colors.WHITE,
        primary: int = Colors.BLUE,
        secondary: int = Colors.CYAN,
        border: int = Colors.GRAY,
        font: FontRef = None,
        font_title: FontRef = None,
    ) -> None:
        # TODO: store all colour and font references
        # TODO: create default FontRef instances when None is passed
        pass

    # ------------------------------------------------------------------
    # Factory helpers
    # ------------------------------------------------------------------

    @staticmethod
    def dark() -> "Theme":
        """Return a ready-made dark theme.

        TODO: return Theme with dark-mode colour values
        """
        pass

    @staticmethod
    def light() -> "Theme":
        """Return a ready-made light theme.

        TODO: return Theme with light-mode colour values
        """
        pass

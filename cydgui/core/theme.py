"""
cydgui.core.theme
=================

Theme definitions used by cydgui widgets.

A Theme centralizes colors, dimensions and default visual
properties used throughout the framework.

Design goals
------------
- Lightweight.
- MicroPython friendly.
- No dynamic styling engine.
- Renderer agnostic.
"""

from cydgui.utils.colors import Colors
from cydgui.utils.constants import Constants


class Theme:
    """Framework theme."""

    __slots__ = (
        "background",
        "foreground",
        "primary",
        "secondary",
        "success",
        "warning",
        "error",
        "border",
        "disabled",
        "panel",
        "radius",
        "border_width",
        "padding_x",
        "padding_y",
        "spacing",
        "text_padding_x",
        "text_padding_y",
        "font",
    )

    def __init__(
        self,
        background: int = Colors.BACKGROUND,
        foreground: int = Colors.TEXT,
        primary: int = Colors.PRIMARY,
        secondary: int = Colors.SECONDARY,
        success: int = Colors.SUCCESS,
        warning: int = Colors.WARNING,
        error: int = Colors.ERROR,
        border: int = Colors.BORDER,
        disabled: int = Colors.DISABLED,
        panel: int = Colors.PANEL,
        radius: int = Constants.DEFAULT_RADIUS,
        border_width: int = Constants.DEFAULT_BORDER,
        padding_x: int = Constants.SPACING_MD,
        padding_y: int = Constants.SPACING_MD,
        spacing: int = Constants.SPACING_SM,
        text_padding_x: int = Constants.TEXT_PADDING_X,
        text_padding_y: int = Constants.TEXT_PADDING_Y,
        font=None,
    ) -> None:
        """
        Initialize theme.

        Args:
            background: Default background color.
            foreground: Default text color.
            primary: Primary accent color.
            secondary: Secondary accent color.
            success: Success color.
            warning: Warning color.
            error: Error color.
            border: Border color.
            disabled: Disabled widget color.
            panel: Panel background color.
            radius: Default corner radius.
            font: Default font.
        """

        self.background = background
        self.foreground = foreground

        self.primary = primary
        self.secondary = secondary

        self.success = success
        self.warning = warning
        self.error = error

        self.border = border
        self.disabled = disabled

        self.panel = panel

        self.radius = radius
        self.border_width = border_width
        self.padding_x = padding_x
        self.padding_y = padding_y
        self.spacing = spacing
        self.text_padding_x = text_padding_x
        self.text_padding_y = text_padding_y

        self.font = font

    # ------------------------------------------------------------------
    # Factory methods
    # ------------------------------------------------------------------

    @classmethod
    def dark(cls):
        """
        Create dark theme.

        Returns:
            Theme instance.
        """

        return cls(
            background=Colors.BLACK,
            foreground=Colors.WHITE,
            primary=Colors.BLUE,
            secondary=Colors.DARK_GRAY,
            success=Colors.GREEN,
            warning=Colors.YELLOW,
            error=Colors.RED,
            border=Colors.LIGHT_GRAY,
            disabled=Colors.GRAY,
            panel=Colors.DARK_GRAY,
        )

    @classmethod
    def light(cls):
        """
        Create light theme.

        Returns:
            Theme instance.
        """

        return cls(
            background=Colors.WHITE,
            foreground=Colors.BLACK,
            primary=Colors.BLUE,
            secondary=Colors.LIGHT_GRAY,
            success=Colors.GREEN,
            warning=Colors.ORANGE,
            error=Colors.RED,
            border=Colors.GRAY,
            disabled=Colors.LIGHT_GRAY,
            panel=Colors.WHITE,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def copy(self):
        """
        Create a copy of the theme.

        Returns:
            Theme instance.
        """

        return Theme(
            background=self.background,
            foreground=self.foreground,
            primary=self.primary,
            secondary=self.secondary,
            success=self.success,
            warning=self.warning,
            error=self.error,
            border=self.border,
            disabled=self.disabled,
            panel=self.panel,
            radius=self.radius,
            border_width=self.border_width,
            padding_x=self.padding_x,
            padding_y=self.padding_y,
            spacing=self.spacing,
            text_padding_x=self.text_padding_x,
            text_padding_y=self.text_padding_y,
            font=self.font,
        )

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"Theme("
            f"background=0x{self.background:04X}, "
            f"foreground=0x{self.foreground:04X})"
        )
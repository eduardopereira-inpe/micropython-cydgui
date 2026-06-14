"""
cydgui.utils.constants
======================

Framework-wide constants.

This module centralizes common values used throughout cydgui
to avoid magic numbers and improve consistency.
"""


class Constants:
    """Framework constants."""

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    DISPLAY_WIDTH = 240
    DISPLAY_HEIGHT = 320

    # ---------------------------------------------------------
    # Font metrics
    # ---------------------------------------------------------

    DEFAULT_FONT_WIDTH = 8
    DEFAULT_FONT_HEIGHT = 8

    # ---------------------------------------------------------
    # Spacing
    # ---------------------------------------------------------

    SPACING_XS = 2
    SPACING_SM = 4
    SPACING_MD = 8
    SPACING_LG = 12
    SPACING_XL = 16

    # ---------------------------------------------------------
    # Border radius
    # ---------------------------------------------------------

    RADIUS_NONE = 0
    RADIUS_SM = 2
    RADIUS_MD = 4
    RADIUS_LG = 8

    DEFAULT_RADIUS = RADIUS_MD

    # ---------------------------------------------------------
    # Border sizes
    # ---------------------------------------------------------

    BORDER_NONE = 0
    BORDER_THIN = 1
    BORDER_MEDIUM = 2
    BORDER_THICK = 3

    DEFAULT_BORDER = BORDER_THIN

    # ---------------------------------------------------------
    # Widget sizes
    # ---------------------------------------------------------

    BUTTON_WIDTH = 120
    BUTTON_HEIGHT = 40

    TEXTBOX_WIDTH = 180
    TEXTBOX_HEIGHT = 30

    CHECKBOX_SIZE = 20

    SWITCH_WIDTH = 50
    SWITCH_HEIGHT = 24

    PROGRESSBAR_HEIGHT = 12

    # ---------------------------------------------------------
    # Layout defaults
    # ---------------------------------------------------------

    ROW_SPACING = 4
    COLUMN_SPACING = 4
    GRID_SPACING = 4

    # ---------------------------------------------------------
    # Touch
    # ---------------------------------------------------------

    TOUCH_POLL_INTERVAL_MS = 20

    # ---------------------------------------------------------
    # Rendering
    # ---------------------------------------------------------

    FRAME_DELAY_MS = 16

    # ~60 FPS
    TARGET_FPS = 60

    # ---------------------------------------------------------
    # Text
    # ---------------------------------------------------------

    TEXT_PADDING_X = 4
    TEXT_PADDING_Y = 2

    # ---------------------------------------------------------
    # ProgressBar
    # ---------------------------------------------------------

    PROGRESS_MIN = 0
    PROGRESS_MAX = 100

    # ---------------------------------------------------------
    # TextBox
    # ---------------------------------------------------------

    TEXTBOX_MAX_LENGTH = 64

    # ---------------------------------------------------------
    # Canvas
    # ---------------------------------------------------------

    CANVAS_DEFAULT_WIDTH = 100
    CANVAS_DEFAULT_HEIGHT = 100

    # ---------------------------------------------------------
    # Animation
    # ---------------------------------------------------------

    ANIMATION_STEP = 1
    ANIMATION_DELAY_MS = 20

    # ---------------------------------------------------------
    # Theme
    # ---------------------------------------------------------

    THEME_LIGHT = "light"
    THEME_DARK = "dark"

    DEFAULT_THEME = THEME_DARK

    # ---------------------------------------------------------
    # Alignment
    # ---------------------------------------------------------

    ALIGN_LEFT = 0
    ALIGN_CENTER = 1
    ALIGN_RIGHT = 2

    ALIGN_TOP = 0
    ALIGN_MIDDLE = 1
    ALIGN_BOTTOM = 2

    # ---------------------------------------------------------
    # Widget states
    # ---------------------------------------------------------

    STATE_NORMAL = 0
    STATE_PRESSED = 1
    STATE_DISABLED = 2

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    MAX_SCREEN_STACK = 16

    TOUCH_INVERT_X = True
    TOUCH_INVERT_Y = False
    DISPLAY_ROTATION = 90
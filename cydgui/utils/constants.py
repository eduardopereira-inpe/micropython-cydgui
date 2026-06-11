"""
cydgui.utils.constants
======================

Framework-wide numeric and string constants.

Naming conventions
------------------
- Display geometry defaults are prefixed with ``DISPLAY_``.
- Widget defaults are prefixed with the widget name in upper-case.
- All colours are 16-bit RGB565 integers; import from
  :mod:`cydgui.utils.colors` for the full named-colour set.

Notes
-----
- These constants represent *default* values.  Every component that uses them
  accepts an explicit override so the defaults can be changed application-wide
  by editing this single file.
"""

# ---------------------------------------------------------------------------
# Display defaults (CYD: ESP32 + ILI9341)
# ---------------------------------------------------------------------------

DISPLAY_WIDTH  = 240   # pixels
DISPLAY_HEIGHT = 320   # pixels
DISPLAY_ROTATION = 0   # 0, 90, 180, 270 degrees

# ---------------------------------------------------------------------------
# Frame rate / timing
# ---------------------------------------------------------------------------

TARGET_FPS        = 30         # target frames per second
FRAME_INTERVAL_MS = 1000 // TARGET_FPS   # milliseconds per frame

# ---------------------------------------------------------------------------
# Widget geometry defaults
# ---------------------------------------------------------------------------

WIDGET_DEFAULT_WIDTH   = 80    # pixels
WIDGET_DEFAULT_HEIGHT  = 30    # pixels
WIDGET_DEFAULT_PADDING = 4     # pixels
WIDGET_DEFAULT_RADIUS  = 4     # corner radius in pixels

# ---------------------------------------------------------------------------
# Layout defaults
# ---------------------------------------------------------------------------

LAYOUT_DEFAULT_SPACING = 4     # pixels between children
LAYOUT_DEFAULT_PADDING = 4     # inner margin pixels

# ---------------------------------------------------------------------------
# CheckBox / Switch defaults
# ---------------------------------------------------------------------------

CHECKBOX_BOX_SIZE  = 18        # pixels
SWITCH_WIDTH       = 44        # pixels
SWITCH_HEIGHT      = 22        # pixels

# ---------------------------------------------------------------------------
# ProgressBar defaults
# ---------------------------------------------------------------------------

PROGRESSBAR_DEFAULT_WIDTH  = 100   # pixels
PROGRESSBAR_DEFAULT_HEIGHT = 16    # pixels

# ---------------------------------------------------------------------------
# TextBox defaults
# ---------------------------------------------------------------------------

TEXTBOX_DEFAULT_WIDTH  = 120   # pixels
TEXTBOX_DEFAULT_HEIGHT = 24    # pixels
TEXTBOX_CURSOR_WIDTH   = 2     # pixels

# ---------------------------------------------------------------------------
# Touch / input
# ---------------------------------------------------------------------------

TOUCH_DEBOUNCE_MS = 50   # milliseconds — ignore touch events within this window

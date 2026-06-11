"""
cydgui - Lightweight GUI framework for MicroPython.

Designed for the Cheap Yellow Display (ESP32 + ILI9341 + XPT2046) and similar
embedded targets.  The public surface is intentionally small so that only the
symbols that downstream code actually needs are imported.

Usage example::

    from cydgui import App

    app = App(renderer=my_renderer, theme=my_theme)
    app.run()
"""

# Re-export the top-level entry point so users can do ``from cydgui import App``.
from cydgui.app import App  # noqa: F401

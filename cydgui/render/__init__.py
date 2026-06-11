"""
cydgui.render
=============

Rendering layer for the cydgui framework.

Modules
-------
renderer          Abstract :class:`Renderer` interface.
ili9341_renderer  Concrete renderer for the ILI9341 TFT display.

All concrete renderers must implement the :class:`~cydgui.render.renderer.Renderer`
interface so that higher-level code (App, widgets) stays display-agnostic.
"""

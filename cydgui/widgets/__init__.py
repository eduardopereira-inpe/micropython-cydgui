"""
cydgui.widgets
==============

Ready-to-use widget library for the cydgui framework.

Every widget in this package is a concrete subclass of
:class:`~cydgui.core.widget.Widget`.  Widgets draw themselves via the
:class:`~cydgui.render.renderer.Renderer` passed to their ``draw()`` method
and must *never* access the display directly.

Available widgets
-----------------
label       Static or dynamic text display.
button      Clickable button with optional label.
image       Bitmap / raw image display.
canvas      Free-draw surface for custom graphics.
progressbar Horizontal or vertical progress indicator.
textbox     Single-line or multi-line editable text input.
checkbox    Boolean toggle with a check-mark indicator.
switch      Toggle switch (on/off).
"""

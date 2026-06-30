"""
cydgui.graphics.sprite_atlas
============================

Sprite animation catalog.

The SpriteAtlas is responsible only for storing and retrieving
Animation objects by name.

It contains no rendering logic and no knowledge of sprite sheet
geometry.

Responsibilities:
    - Store animations.
    - Retrieve animations by name.
    - Provide a lightweight registry for Sprite objects.
"""

from cydgui.graphics.animation import Animation


class SpriteAtlas:
    """Sprite animation registry."""

    __slots__ = (
        "_animations",
    )

    def __init__(self):
        """Initialize empty atlas."""
        self._animations = {}

    #################################################################
    # Collection API
    #################################################################

    def __len__(self):
        """Return number of animations."""
        return len(self._animations)

    def __contains__(self, name):
        """Return whether animation exists."""
        return name in self._animations

    def __getitem__(self, name):
        """Return animation by name.

        Raises:
            KeyError if animation does not exist.
        """
        return self._animations[name]

    def __iter__(self):
        """Iterate over animations."""
        return iter(self._animations.values())

    #################################################################
    # Management
    #################################################################

    def clear(self):
        """Remove all animations."""
        self._animations.clear()

    def add(self, animation):
        """Register an animation.

        Args:
            animation (Animation): Animation instance.

        Raises:
            ValueError: If animation name already exists.
        """
        name = animation.name

        if name in self._animations:
            raise ValueError(
                "Animation '{}' already exists.".format(name)
            )

        self._animations[name] = animation

    def animation(self, name):
        """Get animation by name.

        Args:
            name (str): Animation name.

        Returns:
            Animation or None if not found.
        """
        return self._animations.get(name)

    #################################################################
    # Convenience helpers
    #################################################################

    def add_animation(self, animation):
        """Alias for add()."""
        self.add(animation)

    def remove(self, name):
        """Remove animation by name."""
        if name in self._animations:
            del self._animations[name]

    def names(self):
        """Return list of animation names."""
        return list(self._animations.keys())
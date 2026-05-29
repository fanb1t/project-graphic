from pathlib import Path

import pygame


class AssetLoader:
    # Shared image cache so scenes do not reload the same asset repeatedly.
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self._images = {}

    def image(self, relative_path, size=None, alpha=True):
        key = (relative_path, size, alpha)
        if key in self._images:
            return self._images[key]

        path = self.root_path / relative_path
        surface = pygame.image.load(str(path))
        surface = surface.convert_alpha() if alpha else surface.convert()
        if size:
            surface = pygame.transform.scale(surface, size)

        self._images[key] = surface
        return surface


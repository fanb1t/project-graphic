import pygame


class Coin(pygame.sprite.Sprite):
    # Collectible coin used by advanced challenge levels.
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

import pygame


class Door(pygame.sprite.Sprite):
    # Door checks the level-clear condition for a key-holding player.
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def can_enter(self, player):
        return player.has_key and pygame.sprite.collide_rect(self, player)


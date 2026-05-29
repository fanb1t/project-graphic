import pygame


class Key(pygame.sprite.Sprite):
    # Key follows the player who picked it up.
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.following_player = None

    def follow(self, player):
        self.following_player = player

    def update(self):
        if self.following_player:
            self.rect.center = self.following_player.rect.center


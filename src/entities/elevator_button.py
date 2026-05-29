import pygame


class ElevatorButton(pygame.sprite.Sprite):
    # Button becomes active while either player touches it.
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_pressed = False

    def update(self, players):
        self.is_pressed = any(pygame.sprite.collide_rect(self, player) for player in players)


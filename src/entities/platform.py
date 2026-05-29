import pygame


class Platform(pygame.sprite.Sprite):
    # Static rectangle platform used for floors, blocks, and hazards.
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))


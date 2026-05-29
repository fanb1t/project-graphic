import pygame


class Elevator(pygame.sprite.Sprite):
    # Moving platform controlled by a paired button.
    def __init__(self, x, y, width, height, image, target_y, speed=5):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.original_y = y
        self.target_y = target_y
        self.speed = speed

    def update(self, is_active):
        destination = self.target_y if is_active else self.original_y
        if self.rect.y > destination:
            self.rect.y = max(destination, self.rect.y - self.speed)
        elif self.rect.y < destination:
            self.rect.y = min(destination, self.rect.y + self.speed)


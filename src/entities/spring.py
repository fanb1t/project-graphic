import pygame


class Spring(pygame.sprite.Sprite):
    # Bounce pad that launches a player upward when touched from above.
    def __init__(self, x, y, image, bounce_velocity=-17):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.bounce_velocity = bounce_velocity

    def bounce(self, player):
        if pygame.sprite.collide_rect(self, player) and player.velocity_y >= 0:
            player.rect.bottom = self.rect.top
            player.velocity_y = self.bounce_velocity
            player.is_jumping = True
            return True
        return False

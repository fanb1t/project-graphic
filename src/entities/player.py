import pygame

from src.core.settings import HEIGHT


class Player(pygame.sprite.Sprite):
    # Player owns movement, gravity, jumping, and platform collision.
    def __init__(self, x, y, image, controls):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.controls = controls
        self.speed = 5
        self.gravity = 0.4
        self.jump_velocity = -10
        self.velocity_y = 0
        self.is_jumping = False
        self.has_key = False

    def update(self, platforms, elevators=None, blockers=None):
        elevators = elevators or pygame.sprite.Group()
        blockers = blockers or []
        keys = pygame.key.get_pressed()

        if keys[self.controls["left"]]:
            self.rect.x -= self.speed
            self._handle_collision(platforms, elevators, "horizontal", blockers)
        if keys[self.controls["right"]]:
            self.rect.x += self.speed
            self._handle_collision(platforms, elevators, "horizontal", blockers)
        if keys[self.controls["jump"]] and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = self.jump_velocity

        previous_rect = self.rect.copy()
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.is_jumping = False
            self.velocity_y = 0

        self._handle_collision(platforms, elevators, "vertical", blockers, previous_rect)

    def _handle_collision(self, platforms, elevators, direction, blockers=None, previous_rect=None):
        blockers = blockers or []
        # Treat the other player like a solid body so characters cannot pass through each other.
        for obj in list(platforms) + list(elevators) + list(blockers):
            if not pygame.sprite.collide_rect(self, obj):
                continue

            if direction == "horizontal":
                if self.rect.centerx < obj.rect.centerx:
                    self.rect.right = obj.rect.left
                else:
                    self.rect.left = obj.rect.right
            else:
                was_above = previous_rect and previous_rect.bottom <= obj.rect.top
                was_below = previous_rect and previous_rect.top >= obj.rect.bottom
                if self.velocity_y > 0 and (was_above or self.rect.bottom <= obj.rect.top + 15):
                    self.rect.bottom = obj.rect.top
                    self.is_jumping = False
                    self.velocity_y = 0

    def pick_up_key(self, key):
        if pygame.sprite.collide_rect(self, key):
            self.has_key = True
            key.follow(self)

import pygame
import sys

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two Player Game")

# Load player images
player1_image = pygame.image.load("image/น้ำแข็งใpng").convert_alpha()
player2_image = pygame.image.load("image/ลาวา.png").convert_alpha()

# Scale images
player1_image = pygame.transform.scale(player1_image, (50, 50))
player2_image = pygame.transform.scale(player2_image, (50, 50))

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, controls):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.gravity = 0.5
        self.jump_velocity = -10
        self.velocity_y = 0
        self.is_jumping = False
        self.controls = controls

    def update(self):
        keys = pygame.key.get_pressed()

        # Move left
        if keys[self.controls['left']]:
            self.rect.x -= self.speed
        # Move right
        if keys[self.controls['right']]:
            self.rect.x += self.speed
        # Jump
        if keys[self.controls['jump']] and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = self.jump_velocity

        # Apply gravity
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

            # Land on the ground
            if self.rect.bottom >= HEIGHT - 50:
                self.rect.bottom = HEIGHT - 50
                self.is_jumping = False
                self.velocity_y = 0

# Initialize players with different controls
player1_controls = {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w}
player2_controls = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_SPACE}

player1 = Player(100, HEIGHT - 100, player1_image, player1_controls)
player2 = Player(600, HEIGHT - 100, player2_image, player2_controls)

# Create sprite groups
players = pygame.sprite.Group()
players.add(player1)
players.add(player2)

# Set up the game clock
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update players
    players.update()

    # Draw everything
    screen.fill(WHITE)
    players.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

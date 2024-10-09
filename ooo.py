import pygame
import sys
from set_up import level1_set_up, WIDTH, HEIGHT, FPS, GAME_OVER_TEXT_COLOR

# Load initial positions and sizes from level1_set_up
PLAYER1_START_POS = level1_set_up["PLAYER1_START_POS"]
PLAYER2_START_POS = level1_set_up["PLAYER2_START_POS"]
KEY_POS = level1_set_up["KEY_POS"]
DOOR_POS = level1_set_up["DOOR_POS"]
BOX_SIZES = level1_set_up["BOX_SIZES"]
BOX_POSITIONS = level1_set_up["BOX_POSITIONS"]
LAVA_SIZES = level1_set_up["LAVA_SIZES"]
LAVA_POSITIONS = level1_set_up["LAVA_POSITIONS"]
BUTTON_POSITION = [(560, HEIGHT - 100),(700, HEIGHT - 420)]
BUTTON_SIZES = [(50, 20),(50, 20)]


class CollisionHandler:
    def __init__(self, player):
        self.player = player

    def handle_horizontal(self, boxes, elevators):
        all_objects = list(boxes) + list(elevators)
        for obj in all_objects:
            if pygame.sprite.collide_rect(self.player, obj):
                if self.player.rect.right > obj.rect.left and self.player.rect.centerx < obj.rect.centerx:
                    self.player.rect.right = obj.rect.left
                elif self.player.rect.left < obj.rect.right and self.player.rect.centerx > obj.rect.centerx:
                    self.player.rect.left = obj.rect.right

    def handle_vertical(self, boxes, elevators):
        all_objects = list(boxes) + list(elevators)
        for obj in all_objects:
            if pygame.sprite.collide_rect(self.player, obj):
                if self.player.velocity_y > 0 and self.player.rect.bottom <= obj.rect.top + 10:
                    self.player.rect.bottom = obj.rect.top
                    self.player.is_jumping = False
                    self.player.velocity_y = 0
                elif self.player.velocity_y < 0 and self.player.rect.top >= obj.rect.bottom - 10:
                    self.player.rect.top = obj.rect.bottom
                    self.player.velocity_y = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, controls):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.gravity = 0.4
        self.jump_velocity = -10
        self.velocity_y = 0
        self.is_jumping = False
        self.has_key = False
        self.controls = controls
        self.collision_handler = CollisionHandler(self)

    def update(self, boxes, elevators):
        keys = pygame.key.get_pressed()
        if keys[self.controls['left']]:
            self.rect.x -= self.speed
            self.collision_handler.handle_horizontal(boxes, elevators)
        if keys[self.controls['right']]:
            self.rect.x += self.speed
            self.collision_handler.handle_horizontal(boxes, elevators)
        if keys[self.controls['jump']] and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = self.jump_velocity

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.is_jumping = False
            self.velocity_y = 0
        self.collision_handler.handle_vertical(boxes, elevators)

    def pick_up_key(self, key):
        if pygame.sprite.collide_rect(self, key):
            self.has_key = True
            key.following_player = self

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.following_player = None

    def update(self):
        if self.following_player:
            self.rect.center = self.following_player.rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_entry(self, player):
        return pygame.sprite.collide_rect(self, player) and player.has_key

class Elevator(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, target_y):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.original_y = y
        self.target_y = target_y
        self.speed = 5

    def update(self, button_pressed):
        if button_pressed:
            if self.rect.y > self.target_y:
                self.rect.y -= self.speed
            elif self.rect.y < self.target_y:
                self.rect.y += self.speed
        else:
            if self.rect.y < self.original_y:
                self.rect.y += self.speed
            elif self.rect.y > self.original_y:
                self.rect.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class ElevatorButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_pressed = False

    def update(self, player1, player2):
        self.is_pressed = pygame.sprite.collide_rect(self, player1) or pygame.sprite.collide_rect(self, player2)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def check_door_entry(door, player1, player2):
    """Check if either player can enter the door and trigger the next game level."""
    if door.check_entry(player1) or door.check_entry(player2):
        print("Both players can enter the door.")

def show_game_over(screen):
    font = pygame.font.SysFont(None, 74)
    game_over_surface = font.render('Game Over', True, GAME_OVER_TEXT_COLOR)
    screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2 - game_over_surface.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Wait for 2 seconds before quitting
    pygame.quit()
    sys.exit()

def run_game():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Two Player Game")

    # Load images
    background_image = pygame.image.load("image/ด่านที่1/Background.png").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    player1_image_ice = pygame.image.load("image/ตัวละคร/น้ำแข็ง.1.png").convert_alpha()
    player2_image_lava = pygame.image.load("image/ตัวละคร/ลาวา.1.png").convert_alpha()
    player1_image_ice = pygame.transform.scale(player1_image_ice, (50, 50))
    player2_image_lava = pygame.transform.scale(player2_image_lava, (50, 50))

    key_image = pygame.image.load("image/ด่านที่1/Image (2).png").convert_alpha()
    key_image = pygame.transform.scale(key_image, (50, 50))

    door_image = pygame.image.load("image/ด่านที่1/door.png").convert_alpha()
    door_image = pygame.transform.scale(door_image, (200, 200))

    box_image = pygame.image.load("image/ด่านที่1/tile2.1.png").convert_alpha()
    lava_image = pygame.image.load("image/ด่านที่1/lava_tile6.png").convert_alpha()
    elevator_image = pygame.image.load("image/ด่านที่1/tile2.1.png").convert_alpha()
    button_image = pygame.image.load("image/ด่านที่1/tile2.1.png").convert_alpha()

    # Create game objects
    player1 = Player(*PLAYER1_START_POS, player1_image_ice, {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w})
    player2 = Player(*PLAYER2_START_POS, player2_image_lava, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP})
    
    key = Key(*KEY_POS, key_image)
    door = Door(*DOOR_POS, door_image)
    
    boxes = pygame.sprite.Group(*[Box(x, y, width, height, box_image) for (x, y), (width, height) in zip(BOX_POSITIONS, BOX_SIZES)])
    elevators = pygame.sprite.Group(*[Elevator(x, y, width, height, elevator_image, target_y) for (x, y), (width, height, target_y) in zip(ELEVATOR_POSITIONS, ELEVATOR_SIZES, ELEVATOR_TARGET_Y)])

    elevator_button = ElevatorButton(*BUTTON_POSITION, *BUTTON_SIZES, button_image)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background_image, (0, 0))

        # Update objects
        player1.update(boxes, elevators)
        player2.update(boxes, elevators)

        key.update()
        elevator_button.update(player1, player2)

        # Draw objects
        for box in boxes:
            box.draw(screen)
        for elevator in elevators:
            elevator.update(elevator_button.is_pressed)
            elevator.draw(screen)

        player1.draw(screen)
        player2.draw(screen)
        key.draw(screen)
        door.draw(screen)

        # Check for key pickup
        player1.pick_up_key(key)
        player2.pick_up_key(key)

        # Check for door entry
        check_door_entry(door, player1, player2)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    run_game()
